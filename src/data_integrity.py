"""
Provider-neutral data integrity contracts.

This module starts Phase B without binding the system to a specific vendor.
The goal is to make data-quality failure modes explicit before wiring real
survivorship-safe or secondary data providers.

Core principles:
- historical evidence must be able to include delisted symbols
- OHLCV data from two providers must be comparable
- critical provider divergence should fail closed
- provider-specific implementation details stay outside this contract layer
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import Iterable


class ListingStatus(str, Enum):
    """Point-in-time listing status for a tradable symbol."""

    ACTIVE = "active"
    DELISTED = "delisted"
    MERGED = "merged"
    UNKNOWN = "unknown"


class DataIntegrityDecision(str, Enum):
    """Decision produced by data integrity checks."""

    PASS = "pass"
    WARN = "warn"
    FAIL_CLOSED = "fail_closed"


@dataclass(frozen=True)
class HistoricalSymbol:
    """Point-in-time symbol metadata used for survivorship-safe research."""

    symbol: str
    name: str
    listing_status: ListingStatus
    listed_from: date | None = None
    listed_to: date | None = None
    successor_symbol: str | None = None

    @property
    def is_survivorship_sensitive(self) -> bool:
        """Return True when excluding this symbol could bias historical tests."""
        return self.listing_status in {ListingStatus.DELISTED, ListingStatus.MERGED}


@dataclass(frozen=True)
class OhlcvBar:
    """Provider-neutral daily OHLCV bar."""

    symbol: str
    as_of: date
    open: float
    high: float
    low: float
    close: float
    volume: int
    provider: str
    adjusted: bool = True

    def validate_shape(self) -> tuple[str, ...]:
        """Return structural data-quality issues for this bar."""
        issues: list[str] = []

        if not self.symbol:
            issues.append("missing_symbol")
        if not self.provider:
            issues.append("missing_provider")
        if self.open <= 0 or self.high <= 0 or self.low <= 0 or self.close <= 0:
            issues.append("non_positive_price")
        if self.high < max(self.open, self.close, self.low):
            issues.append("high_below_price_component")
        if self.low > min(self.open, self.close, self.high):
            issues.append("low_above_price_component")
        if self.volume < 0:
            issues.append("negative_volume")

        return tuple(issues)


@dataclass(frozen=True)
class ProviderComparisonTolerance:
    """Allowed cross-provider divergence before warnings or fail-closed."""

    max_price_pct_warn: float = 0.0025
    max_price_pct_fail: float = 0.01
    max_volume_pct_warn: float = 0.05
    max_volume_pct_fail: float = 0.20


@dataclass(frozen=True)
class ProviderComparisonResult:
    """Result of comparing the same OHLCV bar across two providers."""

    decision: DataIntegrityDecision
    reasons: tuple[str, ...]
    max_price_pct_diff: float
    volume_pct_diff: float


@dataclass(frozen=True)
class HistoricalUniverse:
    """A point-in-time universe that can include inactive securities."""

    symbols: tuple[HistoricalSymbol, ...]

    def active_on(self, as_of: date) -> tuple[HistoricalSymbol, ...]:
        """Return symbols that were part of the universe on a given date."""
        result: list[HistoricalSymbol] = []

        for symbol in self.symbols:
            if symbol.listed_from and as_of < symbol.listed_from:
                continue
            if symbol.listed_to and as_of > symbol.listed_to:
                continue
            result.append(symbol)

        return tuple(result)

    def survivorship_sensitive_symbols(self) -> tuple[HistoricalSymbol, ...]:
        """Return symbols whose omission could create survivorship bias."""
        return tuple(symbol for symbol in self.symbols if symbol.is_survivorship_sensitive)


def _pct_diff(left: float, right: float) -> float:
    denominator = max(abs(left), abs(right))
    if denominator == 0:
        return 0.0
    return abs(left - right) / denominator


def compare_provider_bars(
    primary: OhlcvBar,
    secondary: OhlcvBar,
    tolerance: ProviderComparisonTolerance | None = None,
) -> ProviderComparisonResult:
    """Compare two provider bars and fail closed on critical divergence."""
    tolerance = tolerance or ProviderComparisonTolerance()
    reasons: list[str] = []

    primary_shape_issues = primary.validate_shape()
    secondary_shape_issues = secondary.validate_shape()

    if primary_shape_issues:
        reasons.extend(f"primary_{issue}" for issue in primary_shape_issues)
    if secondary_shape_issues:
        reasons.extend(f"secondary_{issue}" for issue in secondary_shape_issues)

    if primary.symbol != secondary.symbol:
        reasons.append("symbol_mismatch")
    if primary.as_of != secondary.as_of:
        reasons.append("date_mismatch")
    if primary.adjusted != secondary.adjusted:
        reasons.append("adjustment_policy_mismatch")

    price_diffs = (
        _pct_diff(primary.open, secondary.open),
        _pct_diff(primary.high, secondary.high),
        _pct_diff(primary.low, secondary.low),
        _pct_diff(primary.close, secondary.close),
    )
    max_price_pct_diff = max(price_diffs)
    volume_pct_diff = _pct_diff(float(primary.volume), float(secondary.volume))

    if max_price_pct_diff >= tolerance.max_price_pct_fail:
        reasons.append("critical_price_divergence")
    elif max_price_pct_diff >= tolerance.max_price_pct_warn:
        reasons.append("price_divergence_warning")

    if volume_pct_diff >= tolerance.max_volume_pct_fail:
        reasons.append("critical_volume_divergence")
    elif volume_pct_diff >= tolerance.max_volume_pct_warn:
        reasons.append("volume_divergence_warning")

    hard_fail_reasons = {
        "symbol_mismatch",
        "date_mismatch",
        "adjustment_policy_mismatch",
        "critical_price_divergence",
        "critical_volume_divergence",
    }

    if any(reason in hard_fail_reasons for reason in reasons):
        decision = DataIntegrityDecision.FAIL_CLOSED
    elif reasons:
        decision = DataIntegrityDecision.WARN
    else:
        decision = DataIntegrityDecision.PASS

    return ProviderComparisonResult(
        decision=decision,
        reasons=tuple(reasons),
        max_price_pct_diff=round(max_price_pct_diff, 8),
        volume_pct_diff=round(volume_pct_diff, 8),
    )


def require_survivorship_safe_universe(universe: HistoricalUniverse) -> DataIntegrityDecision:
    """Return FAIL_CLOSED when a historical universe has no inactive securities."""
    if not universe.symbols:
        return DataIntegrityDecision.FAIL_CLOSED
    if not universe.survivorship_sensitive_symbols():
        return DataIntegrityDecision.FAIL_CLOSED
    return DataIntegrityDecision.PASS


def has_missing_bars(expected_dates: Iterable[date], bars: Iterable[OhlcvBar]) -> bool:
    """Return True if expected dates are not represented in the bar set."""
    observed_dates = {bar.as_of for bar in bars}
    return any(expected_date not in observed_dates for expected_date in expected_dates)
