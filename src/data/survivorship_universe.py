"""
Survivorship-Bias Universe Loader.

The single most important data-quality fix for any backtesting system.

Without delisted-ticker awareness, every historical backtest systematically
overstates edge because the universe only contains companies that survived.
Studies suggest 1-3% annual return overstatement is typical, and momentum
strategies are especially vulnerable because they tend to load up on names
that later fail.

This module:
- Loads a point-in-time universe snapshot (which tickers were tradeable on a given date)
- Tracks delisting events with date, reason, final price
- Provides a tradeable_universe(date) function for backtests
- Validates that backtest record dates fall within each ticker's active window

Storage format is deterministic JSON so it can be checked into git, diffed
in PRs, and reasoned about by humans. The data itself is loaded from a
canonical CSV that the user is responsible for maintaining (sourced from
Norgate, CRSP, Sharadar, or a manual research process).

This module does NOT fetch delisting data from an API. Polygon's delisted
ticker coverage is incomplete and inconsistent across plans. The user is
expected to provide a vetted dataset.
"""

from __future__ import annotations

import csv
import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, date, datetime
from enum import Enum
from pathlib import Path
from typing import Any, Iterable


DEFAULT_UNIVERSE_PATH = Path("data/universe/survivorship_universe.csv")
DEFAULT_METADATA_PATH = Path("data/universe/universe_metadata.json")


class DelistingReason(str, Enum):
    """
    Why a ticker stopped trading. Bankruptcy and acquisition have very
    different return profiles, so they are tracked separately.
    """

    BANKRUPTCY = "bankruptcy"
    ACQUISITION = "acquisition"
    MERGER = "merger"
    PRIVATIZATION = "privatization"
    SPINOFF = "spinoff"
    EXCHANGE_DELIST = "exchange_delist"
    REVERSE_MERGER = "reverse_merger"
    SYMBOL_CHANGE = "symbol_change"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class TickerLifecycle:
    """
    A single ticker's tradeable lifecycle.

    Notes on semantics:
    - active_from: first date the ticker existed under this symbol
    - active_to: last date the ticker traded. None means still trading.
    - delisting_reason: why it stopped. Required if active_to is set.
    - successor_symbol: for symbol_change/merger, the new ticker
    """

    symbol: str
    active_from: date
    active_to: date | None = None
    delisting_reason: DelistingReason | None = None
    successor_symbol: str | None = None
    final_close_price: float | None = None
    notes: str = ""

    def is_active_on(self, target: date) -> bool:
        if target < self.active_from:
            return False
        if self.active_to is None:
            return True
        return target <= self.active_to

    def to_dict(self) -> dict[str, Any]:
        return {
            "symbol": self.symbol,
            "active_from": self.active_from.isoformat(),
            "active_to": self.active_to.isoformat() if self.active_to else None,
            "delisting_reason": self.delisting_reason.value if self.delisting_reason else None,
            "successor_symbol": self.successor_symbol,
            "final_close_price": self.final_close_price,
            "notes": self.notes,
        }


@dataclass(frozen=True)
class UniverseSnapshot:
    """
    A point-in-time view of the tradeable universe.

    survivors_only_count is included specifically so backtest reports can
    show the size of the survivorship bias: how many tickers are missing
    from a forward-looking universe vs. a point-in-time universe.
    """

    as_of: date
    tradeable: tuple[str, ...]
    delisted_before: tuple[str, ...]
    not_yet_listed: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "as_of": self.as_of.isoformat(),
            "tradeable_count": len(self.tradeable),
            "delisted_before_count": len(self.delisted_before),
            "not_yet_listed_count": len(self.not_yet_listed),
            "tradeable": list(self.tradeable),
            "delisted_before": list(self.delisted_before),
            "not_yet_listed": list(self.not_yet_listed),
        }


@dataclass(frozen=True)
class UniverseCoverageReport:
    """Backtest universe breadth gate.

    A validation backtest on a tiny 16-symbol universe is not acceptable
    evidence for institutional readiness. This report is intentionally simple
    so CI and validation jobs can fail fast when the point-in-time universe is
    too narrow.
    """

    as_of: date
    tradeable_count: int
    minimum_tradeable_count: int = 500

    @property
    def passed(self) -> bool:
        return self.tradeable_count >= self.minimum_tradeable_count

    @property
    def missing_count(self) -> int:
        return max(0, self.minimum_tradeable_count - self.tradeable_count)

    def to_dict(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "as_of": self.as_of.isoformat(),
            "tradeable_count": self.tradeable_count,
            "minimum_tradeable_count": self.minimum_tradeable_count,
            "missing_count": self.missing_count,
        }


def validate_universe_coverage(
    universe: "SurvivorshipUniverse",
    as_of: date,
    *,
    minimum_tradeable_count: int = 500,
) -> UniverseCoverageReport:
    """Fail a backtest universe that is too small to be serious evidence."""
    snapshot = universe.tradeable_universe(as_of)
    return UniverseCoverageReport(
        as_of=as_of,
        tradeable_count=len(snapshot.tradeable),
        minimum_tradeable_count=minimum_tradeable_count,
    )


@dataclass(frozen=True)
class SurvivorshipAuditReport:
    """
    Audit result when backtest records are validated against the universe.

    A clean backtest has zero out_of_window records. Any record outside its
    ticker's active window is either bad data or evidence of survivorship
    bias leaking into the universe.
    """

    total_records: int
    valid_records: int
    out_of_window_records: int
    unknown_ticker_records: int
    out_of_window_samples: list[dict[str, Any]] = field(default_factory=list)
    unknown_ticker_samples: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return self.out_of_window_records == 0 and self.unknown_ticker_records == 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "total_records": self.total_records,
            "valid_records": self.valid_records,
            "out_of_window_records": self.out_of_window_records,
            "unknown_ticker_records": self.unknown_ticker_records,
            "out_of_window_samples": self.out_of_window_samples,
            "unknown_ticker_samples": self.unknown_ticker_samples,
        }


class SurvivorshipUniverse:
    """
    Container for a vetted ticker lifecycle dataset.

    Lookup is O(1) per ticker after construction. Snapshot building is
    O(n) where n is total ticker count; for a 5000-ticker universe this
    is still trivially fast.
    """

    def __init__(self, lifecycles: Iterable[TickerLifecycle]) -> None:
        self._by_symbol: dict[str, TickerLifecycle] = {}
        for lifecycle in lifecycles:
            symbol = lifecycle.symbol.upper()
            if symbol in self._by_symbol:
                raise ValueError(f"duplicate ticker in universe: {symbol}")
            self._by_symbol[symbol] = lifecycle

    @property
    def ticker_count(self) -> int:
        return len(self._by_symbol)

    def lookup(self, symbol: str) -> TickerLifecycle | None:
        return self._by_symbol.get(symbol.upper())

    def is_tradeable_on(self, symbol: str, target: date) -> bool:
        lifecycle = self.lookup(symbol)
        if lifecycle is None:
            return False
        return lifecycle.is_active_on(target)

    def tradeable_universe(self, target: date) -> UniverseSnapshot:
        tradeable: list[str] = []
        delisted_before: list[str] = []
        not_yet_listed: list[str] = []

        for symbol, lifecycle in sorted(self._by_symbol.items()):
            if lifecycle.is_active_on(target):
                tradeable.append(symbol)
            elif target < lifecycle.active_from:
                not_yet_listed.append(symbol)
            else:
                delisted_before.append(symbol)

        return UniverseSnapshot(
            as_of=target,
            tradeable=tuple(tradeable),
            delisted_before=tuple(delisted_before),
            not_yet_listed=tuple(not_yet_listed),
        )

    def audit_backtest_records(
        self,
        records: Iterable[dict[str, Any]],
        *,
        symbol_field: str = "symbol",
        date_field: str = "signal_date",
        max_samples: int = 25,
    ) -> SurvivorshipAuditReport:
        total = 0
        valid = 0
        out_of_window = 0
        unknown = 0
        out_of_window_samples: list[dict[str, Any]] = []
        unknown_samples: list[str] = []

        for record in records:
            if not isinstance(record, dict):
                continue
            total += 1
            symbol = str(record.get(symbol_field, "")).upper()
            record_date = _parse_date(record.get(date_field))

            if record_date is None:
                # Cannot validate without a date; counted as out of window.
                out_of_window += 1
                if len(out_of_window_samples) < max_samples:
                    out_of_window_samples.append(
                        {"symbol": symbol, "reason": "missing_or_invalid_date"}
                    )
                continue

            lifecycle = self._by_symbol.get(symbol)
            if lifecycle is None:
                unknown += 1
                if len(unknown_samples) < max_samples and symbol not in unknown_samples:
                    unknown_samples.append(symbol)
                continue

            if not lifecycle.is_active_on(record_date):
                out_of_window += 1
                if len(out_of_window_samples) < max_samples:
                    out_of_window_samples.append(
                        {
                            "symbol": symbol,
                            "record_date": record_date.isoformat(),
                            "active_from": lifecycle.active_from.isoformat(),
                            "active_to": (
                                lifecycle.active_to.isoformat()
                                if lifecycle.active_to
                                else None
                            ),
                        }
                    )
                continue

            valid += 1

        return SurvivorshipAuditReport(
            total_records=total,
            valid_records=valid,
            out_of_window_records=out_of_window,
            unknown_ticker_records=unknown,
            out_of_window_samples=out_of_window_samples,
            unknown_ticker_samples=unknown_samples,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "ticker_count": self.ticker_count,
            "lifecycles": [
                lifecycle.to_dict()
                for lifecycle in sorted(self._by_symbol.values(), key=lambda x: x.symbol)
            ],
        }


def load_survivorship_universe(path: Path = DEFAULT_UNIVERSE_PATH) -> SurvivorshipUniverse:
    """
    Load a universe from a CSV with columns:
        symbol, active_from, active_to, delisting_reason, successor_symbol,
        final_close_price, notes

    active_to may be empty for active tickers.
    delisting_reason must be set if active_to is set, otherwise validation fails.
    Dates are ISO-8601 (YYYY-MM-DD).
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(
            f"survivorship universe file not found at {path}. "
            "Provide a vetted CSV from Norgate, CRSP, Sharadar, or manual research."
        )

    lifecycles: list[TickerLifecycle] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {"symbol", "active_from"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"survivorship CSV missing required columns: {sorted(missing)}")

        for line_number, row in enumerate(reader, start=2):
            symbol = (row.get("symbol") or "").strip().upper()
            if not symbol:
                continue

            active_from = _parse_date(row.get("active_from"))
            if active_from is None:
                raise ValueError(f"line {line_number}: invalid active_from for {symbol}")

            active_to_raw = (row.get("active_to") or "").strip()
            active_to = _parse_date(active_to_raw) if active_to_raw else None

            reason_raw = (row.get("delisting_reason") or "").strip().lower()
            if active_to is not None and not reason_raw:
                raise ValueError(
                    f"line {line_number}: {symbol} has active_to but no delisting_reason"
                )
            reason = DelistingReason(reason_raw) if reason_raw else None

            successor = (row.get("successor_symbol") or "").strip().upper() or None

            final_close_raw = (row.get("final_close_price") or "").strip()
            final_close = float(final_close_raw) if final_close_raw else None

            notes = (row.get("notes") or "").strip()

            lifecycles.append(
                TickerLifecycle(
                    symbol=symbol,
                    active_from=active_from,
                    active_to=active_to,
                    delisting_reason=reason,
                    successor_symbol=successor,
                    final_close_price=final_close,
                    notes=notes,
                )
            )

    return SurvivorshipUniverse(lifecycles)


def write_universe_metadata(
    universe: SurvivorshipUniverse,
    *,
    metadata_path: Path = DEFAULT_METADATA_PATH,
) -> None:
    """Write a JSON metadata file summarizing the universe for inspection."""
    metadata_path = Path(metadata_path)
    metadata_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "generated_at": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        **universe.to_dict(),
    }
    metadata_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _parse_date(value: Any) -> date | None:
    if value is None:
        return None
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return None
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"
        try:
            return datetime.fromisoformat(text).date()
        except ValueError:
            try:
                return date.fromisoformat(text[:10])
            except ValueError:
                return None
    return None
