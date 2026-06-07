#!/usr/bin/env python3
"""Run the Entry / Exit Watcher.

Loads reports/signals/latest-signals.json, fetches latest daily bars from
Polygon for actionable signals, evaluates lifecycle events and persists:

- reports/alerts/YYYY-MM-DD-alerts.json
- reports/alerts/latest-alerts.json
- reports/runtime/entry_exit_watcher_market_data_health.json
- data/signal_lifecycle.jsonl
- updated reports/signals/latest-signals.json

The core watcher logic is pure/testable and lives in
src/watchers/entry_exit_watcher.py.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.data.polygon_client import PolygonClient
from src.signals.signal_status import ACTIONABLE_SIGNAL_ACTIONS, is_terminal_signal_status
from src.structured_logging import emit_structured_log
from src.watchers.entry_exit_watcher import (
    BLOCKED,
    DEFAULT_HEALTH_ARTIFACT,
    append_lifecycle_updates,
    build_watcher_market_data_health,
    evaluate_signals,
    latest_bars_to_price_map,
    load_signal_file,
    save_alerts,
    save_updated_signal_file,
    write_watcher_market_data_health_artifact,
)


class WatcherRuntimeConfigurationError(RuntimeError):
    """Raised when the watcher cannot safely start."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run entry/exit watcher.")
    parser.add_argument(
        "--signals-file",
        default="reports/signals/latest-signals.json",
        help="Signal JSON file to evaluate.",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=5,
        help="Number of recent daily bars to load per symbol.",
    )
    parser.add_argument(
        "--health-artifact",
        default=str(DEFAULT_HEALTH_ARTIFACT),
        help="Watcher market-data health artifact path.",
    )
    return parser.parse_args()


def _build_cycle_id() -> str:
    """Return a deterministic GitHub Actions-aware watcher cycle id."""

    run_id = os.getenv("GITHUB_RUN_ID")
    run_attempt = os.getenv("GITHUB_RUN_ATTEMPT", "1")
    if run_id:
        return f"entry-exit-watcher-{run_id}-{run_attempt}"
    return f"entry-exit-watcher-local-{datetime.now(UTC).strftime('%Y%m%dT%H%M%SZ')}"


def _log(
    *,
    level: str,
    event_type: str,
    message: str,
    cycle_id: str,
    context: dict | None = None,
) -> None:
    emit_structured_log(
        level=level,
        event_type=event_type,
        component="entry_exit_watcher_runner",
        message=message,
        cycle_id=cycle_id,
        context=context or {},
    )


def _extract_signal_records(payload: Any) -> list[dict[str, Any]]:
    """Return signal records from either legacy list or generated signal payload."""

    if isinstance(payload, list):
        signals = payload
    elif isinstance(payload, dict):
        if "signals" not in payload:
            raise WatcherRuntimeConfigurationError(
                "Signals object payload must contain a 'signals' list."
            )
        signals = payload["signals"]
    else:
        raise WatcherRuntimeConfigurationError(
            f"Signals file must contain a JSON list or object payload, got {type(payload).__name__}."
        )

    if not isinstance(signals, list):
        raise WatcherRuntimeConfigurationError(
            f"Signals payload must contain a JSON list or an object with a 'signals' list, got {type(signals).__name__}."
        )

    invalid_count = sum(1 for item in signals if not isinstance(item, dict))
    if invalid_count:
        raise WatcherRuntimeConfigurationError(
            f"Signals payload contains {invalid_count} non-object signal records."
        )

    return signals


def _validate_runtime(signals_file: Path, days: int) -> None:
    """Fail fast for missing runtime inputs instead of crashing later."""

    if days <= 0:
        raise WatcherRuntimeConfigurationError("--days must be a positive integer.")

    if not os.getenv("POLYGON_API_KEY"):
        raise WatcherRuntimeConfigurationError(
            "Missing POLYGON_API_KEY. Configure it locally or as a GitHub Actions secret "
            "before running the entry-exit watcher."
        )

    if not signals_file.exists():
        raise WatcherRuntimeConfigurationError(
            f"Signals file not found: {signals_file}. Generate signals before running the watcher."
        )

    if not signals_file.is_file():
        raise WatcherRuntimeConfigurationError(f"Signals path is not a file: {signals_file}")

    try:
        payload = json.loads(signals_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise WatcherRuntimeConfigurationError(
            f"Signals file contains invalid JSON: {signals_file}: {exc}"
        ) from exc

    _extract_signal_records(payload)


def main() -> int:
    args = parse_args()
    signals_file = Path(args.signals_file)
    health_artifact = Path(args.health_artifact)
    cycle_id = _build_cycle_id()

    print(f"WATCHER_CYCLE_ID={cycle_id}")
    print(f"Using signals file: {signals_file}")
    print(f"Using lookback days: {args.days}")
    print(f"Using health artifact: {health_artifact}")
    _log(
        level="INFO",
        event_type="watcher_runner_started",
        message="Entry/exit watcher runner started.",
        cycle_id=cycle_id,
        context={
            "signals_file": str(signals_file),
            "days": args.days,
            "health_artifact": str(health_artifact),
        },
    )

    try:
        _validate_runtime(signals_file=signals_file, days=args.days)
    except WatcherRuntimeConfigurationError as exc:
        print(f"WATCHER_RUNTIME_CONFIGURATION_ERROR: {exc}", file=sys.stderr)
        _log(
            level="ERROR",
            event_type="watcher_runtime_validation_failed",
            message="Watcher runtime validation failed.",
            cycle_id=cycle_id,
            context={"error": str(exc), "signals_file": str(signals_file), "days": args.days},
        )
        return 2

    _log(
        level="INFO",
        event_type="watcher_runtime_validation_succeeded",
        message="Watcher runtime validation succeeded.",
        cycle_id=cycle_id,
        context={"signals_file": str(signals_file)},
    )

    signals = load_signal_file(signals_file)
    actionable = [
        signal for signal in signals
        if signal.get("action") in ACTIONABLE_SIGNAL_ACTIONS
        and not is_terminal_signal_status(signal.get("status"))
    ]
    _log(
        level="INFO",
        event_type="watcher_signals_loaded",
        message="Watcher signals loaded.",
        cycle_id=cycle_id,
        context={"signals": len(signals), "actionable": len(actionable)},
    )

    if not actionable:
        print("No actionable open signals found.")
        health = build_watcher_market_data_health(
            signals,
            evaluated_symbols=set(),
            cycle_id=cycle_id,
            artifact_path=health_artifact,
        )
        written_health_artifact = write_watcher_market_data_health_artifact(
            health,
            artifact_path=health_artifact,
        )
        print(f"Watcher market-data health: {health.status} ({written_health_artifact})")
        _log(
            level="INFO",
            event_type="watcher_no_actionable_signals",
            message="No actionable open signals found.",
            cycle_id=cycle_id,
            context={"signals": len(signals), "health_artifact": str(written_health_artifact)},
        )
        return 0

    client = PolygonClient()
    bars_by_symbol = {}

    for signal in actionable:
        symbol = signal.get("symbol")
        if not symbol:
            continue
        try:
            bars_by_symbol[symbol] = client.get_daily_bars(symbol, days=args.days)
        except Exception as exc:
            print(f"WARNING: Could not fetch bars for {symbol}: {type(exc).__name__}: {exc}")
            _log(
                level="WARNING",
                event_type="watcher_symbol_fetch_failed",
                message="Could not fetch daily bars for symbol.",
                cycle_id=cycle_id,
                context={"symbol": symbol, "error_type": type(exc).__name__, "error": str(exc)},
            )
            bars_by_symbol[symbol] = []

    price_map = latest_bars_to_price_map(bars_by_symbol)
    health = build_watcher_market_data_health(
        signals,
        evaluated_symbols=price_map.keys(),
        cycle_id=cycle_id,
        artifact_path=health_artifact,
    )
    written_health_artifact = write_watcher_market_data_health_artifact(
        health,
        artifact_path=health_artifact,
    )
    print(f"Watcher market-data health: {health.status} ({written_health_artifact})")
    _log(
        level="ERROR" if health.status == BLOCKED else "WARNING" if health.missing_market_data_count else "INFO",
        event_type="watcher_market_data_health_evaluated",
        message="Watcher market-data health evaluated.",
        cycle_id=cycle_id,
        context={
            "status": health.status,
            "checked_signal_count": health.checked_signal_count,
            "evaluated_symbol_count": health.evaluated_symbol_count,
            "missing_market_data_count": health.missing_market_data_count,
            "health_artifact": str(written_health_artifact),
        },
    )

    alerts, updates, updated_signals = evaluate_signals(signals, price_map)
    _log(
        level="INFO",
        event_type="watcher_evaluation_completed",
        message="Watcher evaluation completed.",
        cycle_id=cycle_id,
        context={"alerts": len(alerts), "updates": len(updates), "price_symbols": len(price_map)},
    )

    if alerts:
        current_date = datetime.now(UTC).strftime("%Y-%m-%d")
        alerts_path, latest_path = save_alerts(alerts, date_str=current_date)
        lifecycle_path = append_lifecycle_updates(updates)
        save_updated_signal_file(signals_file, updated_signals)

        print(f"Alerts written: {alerts_path}, {latest_path}")
        print(f"Lifecycle updated: {lifecycle_path}")
        print(f"Events: {len(alerts)}")
        for alert in alerts:
            print(f"- {alert.symbol}: {alert.alert_type} ({alert.previous_status} -> {alert.new_status})")
        _log(
            level="INFO",
            event_type="watcher_events_persisted",
            message="Watcher events persisted.",
            cycle_id=cycle_id,
            context={
                "alerts": len(alerts),
                "alerts_path": str(alerts_path),
                "latest_path": str(latest_path),
                "lifecycle_path": str(lifecycle_path),
            },
        )
    else:
        print("No entry/exit events detected.")
        save_updated_signal_file(signals_file, updated_signals)
        _log(
            level="INFO",
            event_type="watcher_no_events_detected",
            message="No entry/exit events detected.",
            cycle_id=cycle_id,
            context={"updated_signals": len(updated_signals)},
        )

    if health.status == BLOCKED:
        print("WATCHER_MARKET_DATA_HEALTH_BLOCKED: missing data for active stop/exit risk", file=sys.stderr)
        _log(
            level="ERROR",
            event_type="watcher_market_data_health_blocked",
            message="Watcher blocked because active stop/exit risk could not be evaluated.",
            cycle_id=cycle_id,
            context={"health_artifact": str(written_health_artifact)},
        )
        return 3

    _log(
        level="INFO",
        event_type="watcher_runner_completed",
        message="Entry/exit watcher runner completed.",
        cycle_id=cycle_id,
        context={"alerts": len(alerts), "updates": len(updates), "health_status": health.status},
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
