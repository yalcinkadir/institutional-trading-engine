"""Watcher missing-market-data health gate.

This module classifies whether actionable entry/exit watcher signals had market
bars available during a runtime cycle. The watcher must not silently preserve
open or actionable signals when no current market data was available.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable

from src.signals.signal_identity import ensure_signal_identity, signal_date_from_payload
from src.signals.signal_status import (
    ACTIONABLE_SIGNAL_ACTIONS,
    SignalStatus,
    is_terminal_signal_status,
    normalize_signal_status,
)

PASSED = "PASSED"
DEGRADED = "DEGRADED"
BLOCKED = "BLOCKED"
DEFAULT_HEALTH_ARTIFACT = Path("reports/runtime/entry_exit_watcher_market_data_health.json")
BLOCKING_STATUSES = {SignalStatus.TRIGGERED.value, SignalStatus.TARGET_1_HIT.value}


@dataclass(frozen=True)
class MissingMarketDataRecord:
    signal_id: str
    symbol: str
    signal_date: str
    status: str
    severity: str
    reason: str


@dataclass(frozen=True)
class WatcherMarketDataHealth:
    status: str
    generated_at: str
    checked_signal_count: int
    evaluated_symbol_count: int
    missing_market_data_count: int
    missing_market_data: list[MissingMarketDataRecord] = field(default_factory=list)
    cycle_id: str | None = None
    artifact_path: str | None = None
    notes: str = ""


def _utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


def _is_actionable_open_signal(signal: dict[str, Any]) -> bool:
    return (
        signal.get("action") in ACTIONABLE_SIGNAL_ACTIONS
        and not is_terminal_signal_status(signal.get("status"))
    )


def _missing_severity(status: str) -> str:
    if status in BLOCKING_STATUSES:
        return BLOCKED
    return DEGRADED


def build_watcher_market_data_health(
    signals: Iterable[dict[str, Any]],
    evaluated_symbols: Iterable[str],
    *,
    generated_at: str | None = None,
    cycle_id: str | None = None,
    artifact_path: str | Path | None = None,
) -> WatcherMarketDataHealth:
    """Build a health payload for actionable signals without market data.

    PASSED means every actionable open signal with a symbol had a price bar.
    DEGRADED means a non-position signal could not be evaluated.
    BLOCKED means an already-triggered / runner signal could not be checked for
    stop or exit risk and the runtime cycle must not be treated as healthy.
    """

    evaluated = {str(symbol) for symbol in evaluated_symbols if symbol}
    checked_signal_count = 0
    missing_records: list[MissingMarketDataRecord] = []

    for raw_signal in signals:
        if not isinstance(raw_signal, dict):
            continue
        signal = ensure_signal_identity(raw_signal)
        if not _is_actionable_open_signal(signal):
            continue

        checked_signal_count += 1
        symbol = str(signal.get("symbol") or "")
        if symbol and symbol in evaluated:
            continue

        status = normalize_signal_status(signal.get("status"))
        severity = _missing_severity(status)
        reason = (
            "missing_bar_for_active_stop_or_exit_risk"
            if severity == BLOCKED
            else "missing_bar_for_actionable_signal"
        )
        missing_records.append(
            MissingMarketDataRecord(
                signal_id=str(signal["signal_id"]),
                symbol=symbol,
                signal_date=signal_date_from_payload(signal),
                status=status,
                severity=severity,
                reason=reason,
            )
        )

    if any(record.severity == BLOCKED for record in missing_records):
        status = BLOCKED
        notes = "Missing market data blocks watcher health for active stop/exit risk."
    elif missing_records:
        status = DEGRADED
        notes = "Missing market data degraded watcher coverage for actionable signals."
    else:
        status = PASSED
        notes = "All actionable open signals had market data coverage."

    return WatcherMarketDataHealth(
        status=status,
        generated_at=generated_at or _utc_now_iso(),
        checked_signal_count=checked_signal_count,
        evaluated_symbol_count=len(evaluated),
        missing_market_data_count=len(missing_records),
        missing_market_data=missing_records,
        cycle_id=cycle_id,
        artifact_path=str(artifact_path) if artifact_path else None,
        notes=notes,
    )


def market_data_health_to_dict(health: WatcherMarketDataHealth) -> dict[str, Any]:
    """Return a JSON-serialisable health payload."""

    return asdict(health)


def write_watcher_market_data_health_artifact(
    health: WatcherMarketDataHealth,
    *,
    artifact_path: str | Path | None = None,
) -> Path:
    """Persist the watcher market-data health artifact."""

    target = Path(artifact_path or health.artifact_path or DEFAULT_HEALTH_ARTIFACT)
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = market_data_health_to_dict(health)
    payload["artifact_path"] = str(target)
    target.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return target
