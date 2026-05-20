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


def main() -> int:
    args = parse_args()
    signals_file = Path(args.signals_file)

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
