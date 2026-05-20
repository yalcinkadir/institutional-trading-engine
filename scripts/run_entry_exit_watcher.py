#!/usr/bin/env python3
"""Run the Entry / Exit Watcher.

Loads reports/signals/latest-signals.json, fetches latest daily bars from
Polygon for actionable signals, evaluates lifecycle events and persists:

- reports/alerts/YYYY-MM-DD-alerts.json
- reports/alerts/latest-alerts.json
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

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.data.polygon_client import PolygonClient
from src.watchers.entry_exit_watcher import (
    append_lifecycle_updates,
    evaluate_signals,
    latest_bars_to_price_map,
    load_signal_file,
    save_alerts,
    save_updated_signal_file,
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
    return parser.parse_args()


def _build_cycle_id() -> str:
    """Return a deterministic GitHub Actions-aware watcher cycle id."""

    run_id = os.getenv("GITHUB_RUN_ID")
    run_attempt = os.getenv("GITHUB_RUN_ATTEMPT", "1")
    if run_id:
        return f"entry-exit-watcher-{run_id}-{run_attempt}"
    return f"entry-exit-watcher-local-{datetime.now(UTC).strftime('%Y%m%dT%H%M%SZ')}"


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

    if not isinstance(payload, list):
        raise WatcherRuntimeConfigurationError(
            f"Signals file must contain a JSON list, got {type(payload).__name__}: {signals_file}"
        )


def main() -> int:
    args = parse_args()
    signals_file = Path(args.signals_file)
    cycle_id = _build_cycle_id()

    print(f"WATCHER_CYCLE_ID={cycle_id}")
    print(f"Using signals file: {signals_file}")
    print(f"Using lookback days: {args.days}")

    try:
        _validate_runtime(signals_file=signals_file, days=args.days)
    except WatcherRuntimeConfigurationError as exc:
        print(f"WATCHER_RUNTIME_CONFIGURATION_ERROR: {exc}", file=sys.stderr)
        return 2

    signals = load_signal_file(signals_file)
    actionable = [
        signal for signal in signals
        if signal.get("action") == "BUY_WATCH"
        and signal.get("status", "PENDING") not in {"STOP_HIT", "TARGET_2_HIT", "EXPIRED"}
    ]

    if not actionable:
        print("No actionable open signals found.")
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
            bars_by_symbol[symbol] = []

    price_map = latest_bars_to_price_map(bars_by_symbol)
    alerts, updates, updated_signals = evaluate_signals(signals, price_map)

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
    else:
        print("No entry/exit events detected.")
        save_updated_signal_file(signals_file, updated_signals)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())