from __future__ import annotations

import hashlib
import json
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable

from src.signals.signal_identity import ensure_signal_identity, signal_date_from_payload
from src.signals.signal_status import ACTIONABLE_SIGNAL_ACTIONS, is_terminal_signal_status, normalize_signal_status
from src.watchers.entry_exit_watcher import SignalLifecycleUpdate, WatcherMarketDataHealth

WATCHER_LIFECYCLE_SUMMARY_DIR = Path("reports/watchers/lifecycle")
NO_ACTIONABLE_SIGNALS = "NO_ACTIONABLE_SIGNALS"
NO_EVENTS_DETECTED = "NO_EVENTS_DETECTED"
EVENTS_RECORDED = "EVENTS_RECORDED"
BLOCKED = "BLOCKED"
DEGRADED = "DEGRADED"


def _utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


def _sha256(path: Path) -> str | None:
    if not path.exists() or not path.is_file():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _summary_date(generated_at: str) -> str:
    return str(generated_at)[:10]


def _is_actionable_open_signal(signal: dict[str, Any]) -> bool:
    return (
        signal.get("action") in ACTIONABLE_SIGNAL_ACTIONS
        and not is_terminal_signal_status(signal.get("status"))
    )


def _missing_market_data_by_signal_id(health: WatcherMarketDataHealth) -> dict[str, dict[str, Any]]:
    return {
        record.signal_id: asdict(record)
        for record in health.missing_market_data
        if record.signal_id
    }


def _update_by_signal_id(updates: Iterable[SignalLifecycleUpdate]) -> dict[str, SignalLifecycleUpdate]:
    return {update.signal_id: update for update in updates}


def _lifecycle_event_payloads(update: SignalLifecycleUpdate) -> list[dict[str, Any]]:
    payload = asdict(update)
    supplemental_events = payload.pop("supplemental_events", []) or []
    return [payload, *supplemental_events]


def _events_by_signal_id(updates: Iterable[SignalLifecycleUpdate]) -> dict[str, list[dict[str, Any]]]:
    events: dict[str, list[dict[str, Any]]] = {}
    for update in updates:
        for payload in _lifecycle_event_payloads(update):
            signal_id = str(payload.get("signal_id") or payload.get("signal", {}).get("signal_id") or "")
            if not signal_id:
                continue
            events.setdefault(signal_id, []).append(payload)
    for signal_events in events.values():
        signal_events.sort(key=lambda item: (str(item.get("timestamp") or ""), str(item.get("event_type") or "")))
    return events


def _record_for_signal(
    signal: dict[str, Any],
    *,
    update: SignalLifecycleUpdate | None,
    lifecycle_events: list[dict[str, Any]],
    missing_market_data: dict[str, Any] | None,
    data_completeness_status: str,
    signal_file_path: Path,
    signal_file_sha256: str | None,
) -> dict[str, Any]:
    signal = ensure_signal_identity(signal)
    signal_id = str(signal["signal_id"])
    initial_action = str(signal.get("action") or "")
    initial_status = normalize_signal_status(signal.get("status"))
    actionable_open = _is_actionable_open_signal(signal)

    watcher_status = NO_EVENTS_DETECTED
    trigger_expiry_block_reason = "no_entry_exit_event_detected"
    event_type = None
    previous_status = initial_status
    new_status = initial_status

    if update is not None:
        watcher_status = update.new_status
        trigger_expiry_block_reason = update.event_type
        event_type = update.event_type
        previous_status = update.previous_status
        new_status = update.new_status
    elif missing_market_data is not None:
        watcher_status = str(missing_market_data.get("severity") or data_completeness_status)
        trigger_expiry_block_reason = str(missing_market_data.get("reason") or "missing_market_data")
    elif not actionable_open:
        watcher_status = NO_ACTIONABLE_SIGNALS
        trigger_expiry_block_reason = "not_actionable_or_terminal_signal"

    return {
        "signal_id": signal_id,
        "signal_batch_date": signal_date_from_payload(signal),
        "symbol": str(signal.get("symbol") or ""),
        "initial_action": initial_action,
        "initial_status": initial_status,
        "watcher_status": watcher_status,
        "event_type": event_type,
        "previous_status": previous_status,
        "new_status": new_status,
        "trigger_expiry_block_reason": trigger_expiry_block_reason,
        "data_completeness_status": data_completeness_status,
        "signal_file_path": signal_file_path.as_posix(),
        "signal_file_sha256": signal_file_sha256,
        "lifecycle_event_count": len(lifecycle_events),
        "lifecycle_events": lifecycle_events,
    }


def build_watcher_lifecycle_summary(
    *,
    signals: list[dict[str, Any]],
    updates: list[SignalLifecycleUpdate],
    health: WatcherMarketDataHealth,
    cycle_id: str,
    signals_file: str | Path,
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Build a deterministic, lightweight dated watcher lifecycle summary."""

    timestamp = generated_at or _utc_now_iso()
    signals_path = Path(signals_file)
    signal_file_sha256 = _sha256(signals_path)
    signals_with_identity = [ensure_signal_identity(signal) for signal in signals]
    actionable_open_count = sum(1 for signal in signals_with_identity if _is_actionable_open_signal(signal))
    updates_by_signal_id = _update_by_signal_id(updates)
    events_by_signal_id = _events_by_signal_id(updates)
    missing_by_signal_id = _missing_market_data_by_signal_id(health)
    lifecycle_event_count = sum(len(events) for events in events_by_signal_id.values())

    if health.status == BLOCKED:
        status = BLOCKED
    elif health.status == DEGRADED:
        status = DEGRADED
    elif actionable_open_count == 0:
        status = NO_ACTIONABLE_SIGNALS
    elif lifecycle_event_count:
        status = EVENTS_RECORDED
    else:
        status = NO_EVENTS_DETECTED

    records = [
        _record_for_signal(
            signal,
            update=updates_by_signal_id.get(str(signal["signal_id"])),
            lifecycle_events=events_by_signal_id.get(str(signal["signal_id"]), []),
            missing_market_data=missing_by_signal_id.get(str(signal["signal_id"])),
            data_completeness_status=health.status,
            signal_file_path=signals_path,
            signal_file_sha256=signal_file_sha256,
        )
        for signal in signals_with_identity
    ]

    return {
        "schema_version": "watcher_lifecycle_summary.v1",
        "generated_at": timestamp,
        "summary_date": _summary_date(timestamp),
        "run_id": cycle_id,
        "cycle_id": cycle_id,
        "status": status,
        "signal_file_path": signals_path.as_posix(),
        "signal_file_sha256": signal_file_sha256,
        "signal_count": len(signals_with_identity),
        "actionable_open_count": actionable_open_count,
        "lifecycle_event_count": lifecycle_event_count,
        "data_completeness_status": health.status,
        "market_data_health": asdict(health),
        "records": records,
    }


def write_watcher_lifecycle_summary(
    *,
    signals: list[dict[str, Any]],
    updates: list[SignalLifecycleUpdate],
    health: WatcherMarketDataHealth,
    cycle_id: str,
    signals_file: str | Path,
    output_dir: str | Path | None = None,
    generated_at: str | None = None,
) -> tuple[Path, Path]:
    """Persist dated and latest watcher lifecycle summaries."""

    summary = build_watcher_lifecycle_summary(
        signals=signals,
        updates=updates,
        health=health,
        cycle_id=cycle_id,
        signals_file=signals_file,
        generated_at=generated_at,
    )
    target_dir = Path(output_dir or WATCHER_LIFECYCLE_SUMMARY_DIR)
    target_dir.mkdir(parents=True, exist_ok=True)
    dated_path = target_dir / f"{summary['summary_date']}.json"
    latest_path = target_dir / "latest.json"
    payload = json.dumps(summary, indent=2, sort_keys=True) + "\n"
    dated_path.write_text(payload, encoding="utf-8")
    latest_path.write_text(payload, encoding="utf-8")
    return dated_path, latest_path
