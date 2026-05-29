"""CL4 ATR calculation governance.

This module makes ATR semantics explicit and regression-testable.  It does not
claim that Wilder ATR is a better trading edge.  It provides a deterministic
contract so that any migration from simple rolling ATR to Wilder-smoothed ATR is
visible, versioned and evidence-invalidating.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from math import isclose
from typing import Iterable, Mapping, Sequence

try:  # Keep import optional for isolated/unit-test usage.
    from src.config.thresholds import ATR_CALCULATION_VERSION, THRESHOLDS_VERSION
except Exception:  # pragma: no cover - defensive fallback for standalone usage
    ATR_CALCULATION_VERSION = "unknown"
    THRESHOLDS_VERSION = "unknown"


class AtrMethod(str, Enum):
    """Supported public-demo ATR calculation methods."""

    SIMPLE = "simple"
    WILDER = "wilder"


@dataclass(frozen=True)
class AtrBar:
    """Minimal OHLC input required for true-range/ATR calculation."""

    high: float
    low: float
    close: float


@dataclass(frozen=True)
class AtrGovernanceReport:
    """Governance result for comparing current ATR semantics to a candidate method."""

    current_method: AtrMethod
    candidate_method: AtrMethod
    period: int
    threshold_version: str
    atr_calculation_version: str
    latest_current_atr: float | None
    latest_candidate_atr: float | None
    absolute_delta: float | None
    relative_delta_pct: float | None
    evidence_invalidation_required: bool
    migration_allowed: bool
    reasons: tuple[str, ...] = field(default_factory=tuple)
    notes: tuple[str, ...] = field(default_factory=tuple)


def _coerce_bar(bar: AtrBar | Mapping[str, float]) -> AtrBar:
    if isinstance(bar, AtrBar):
        return bar
    return AtrBar(high=float(bar["high"]), low=float(bar["low"]), close=float(bar["close"]))


def _validate_period(period: int) -> None:
    if period <= 0:
        raise ValueError("ATR period must be positive")


def true_ranges(bars: Iterable[AtrBar | Mapping[str, float]]) -> list[float]:
    """Calculate deterministic true ranges from ordered OHLC bars."""
    coerced = [_coerce_bar(bar) for bar in bars]
    ranges: list[float] = []
    previous_close: float | None = None

    for bar in coerced:
        if bar.high < bar.low:
            raise ValueError("ATR bar high must be greater than or equal to low")

        if previous_close is None:
            true_range = bar.high - bar.low
        else:
            true_range = max(
                bar.high - bar.low,
                abs(bar.high - previous_close),
                abs(bar.low - previous_close),
            )

        ranges.append(float(true_range))
        previous_close = bar.close

    return ranges


def simple_atr_from_true_ranges(ranges: Sequence[float], period: int = 14) -> list[float | None]:
    """Calculate rolling simple-average ATR from true ranges."""
    _validate_period(period)
    values: list[float | None] = []

    for index in range(len(ranges)):
        if index + 1 < period:
            values.append(None)
            continue
        window = ranges[index + 1 - period : index + 1]
        values.append(sum(window) / period)

    return values


def wilder_atr_from_true_ranges(ranges: Sequence[float], period: int = 14) -> list[float | None]:
    """Calculate Wilder-smoothed ATR from true ranges.

    The seed value is the simple average of the first ``period`` true ranges.
    Subsequent values use Wilder's recursive smoothing:
    ``previous_atr * (period - 1) + current_true_range) / period``.
    """
    _validate_period(period)
    values: list[float | None] = []
    previous_atr: float | None = None

    for index, current_range in enumerate(ranges):
        if index + 1 < period:
            values.append(None)
            continue

        if previous_atr is None:
            previous_atr = sum(ranges[:period]) / period
        else:
            previous_atr = ((previous_atr * (period - 1)) + current_range) / period

        values.append(previous_atr)

    return values


def calculate_atr(
    bars: Iterable[AtrBar | Mapping[str, float]],
    *,
    period: int = 14,
    method: AtrMethod | str = AtrMethod.WILDER,
) -> list[float | None]:
    """Calculate ATR values using an explicit method."""
    method = AtrMethod(method)
    ranges = true_ranges(bars)

    if method == AtrMethod.SIMPLE:
        return simple_atr_from_true_ranges(ranges, period=period)
    if method == AtrMethod.WILDER:
        return wilder_atr_from_true_ranges(ranges, period=period)

    raise ValueError(f"Unsupported ATR method: {method}")


def evaluate_atr_migration_governance(
    bars: Iterable[AtrBar | Mapping[str, float]],
    *,
    period: int = 14,
    current_method: AtrMethod | str = AtrMethod.SIMPLE,
    candidate_method: AtrMethod | str = AtrMethod.WILDER,
    relative_tolerance_pct: float = 0.0,
) -> AtrGovernanceReport:
    """Compare ATR methods and decide whether evidence invalidation is required."""
    current_method = AtrMethod(current_method)
    candidate_method = AtrMethod(candidate_method)
    bars_list = list(bars)
    notes: list[str] = []
    reasons: list[str] = []

    current_values = calculate_atr(bars_list, period=period, method=current_method)
    candidate_values = calculate_atr(bars_list, period=period, method=candidate_method)

    latest_current_atr = next((value for value in reversed(current_values) if value is not None), None)
    latest_candidate_atr = next((value for value in reversed(candidate_values) if value is not None), None)

    if latest_current_atr is None or latest_candidate_atr is None:
        reasons.append("insufficient_atr_history")
        return AtrGovernanceReport(
            current_method=current_method,
            candidate_method=candidate_method,
            period=period,
            threshold_version=THRESHOLDS_VERSION,
            atr_calculation_version=ATR_CALCULATION_VERSION,
            latest_current_atr=latest_current_atr,
            latest_candidate_atr=latest_candidate_atr,
            absolute_delta=None,
            relative_delta_pct=None,
            evidence_invalidation_required=False,
            migration_allowed=False,
            reasons=tuple(reasons),
            notes=("collect_more_history_before_migration",),
        )

    absolute_delta = latest_candidate_atr - latest_current_atr
    relative_delta_pct = 0.0
    if not isclose(latest_current_atr, 0.0, abs_tol=1e-12):
        relative_delta_pct = (absolute_delta / latest_current_atr) * 100.0

    method_changed = current_method != candidate_method
    material_delta = abs(relative_delta_pct) > relative_tolerance_pct
    evidence_invalidation_required = method_changed or material_delta

    if method_changed:
        reasons.append("atr_method_changed")
    if material_delta:
        reasons.append("atr_value_changed_beyond_tolerance")
    if evidence_invalidation_required:
        notes.append("invalidate_prior_atr_dependent_evidence")
        notes.append("threshold_version_bump_required")

    return AtrGovernanceReport(
        current_method=current_method,
        candidate_method=candidate_method,
        period=period,
        threshold_version=THRESHOLDS_VERSION,
        atr_calculation_version=ATR_CALCULATION_VERSION,
        latest_current_atr=latest_current_atr,
        latest_candidate_atr=latest_candidate_atr,
        absolute_delta=absolute_delta,
        relative_delta_pct=relative_delta_pct,
        evidence_invalidation_required=evidence_invalidation_required,
        migration_allowed=not evidence_invalidation_required,
        reasons=tuple(reasons),
        notes=tuple(notes),
    )
