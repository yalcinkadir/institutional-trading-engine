#!/usr/bin/env python3
"""Run P26 paper-live observation report."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.operations.paper_live_observation import observe_paper_live, write_paper_live_report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run paper-live observation readiness report.")
    parser.add_argument("--signals-file", default="reports/signals/latest-signals.json")
    parser.add_argument("--lifecycle-file", default="data/signal_lifecycle.jsonl")
    parser.add_argument("--alerts-file", default="reports/alerts/latest-alerts.json")
    parser.add_argument("--min-lifecycle-events", type=int, default=5)
    parser.add_argument("--require-alerts", action="store_true")
    parser.add_argument("--json-output", default="reports/paper-live/paper-live-observation.json")
    parser.add_argument("--markdown-output", default="reports/paper-live/paper-live-observation.md")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = observe_paper_live(
        signals_file=Path(args.signals_file),
        lifecycle_file=Path(args.lifecycle_file),
        alerts_file=Path(args.alerts_file),
        min_lifecycle_events=args.min_lifecycle_events,
        require_alerts=args.require_alerts,
    )
    write_paper_live_report(report, json_path=Path(args.json_output), markdown_path=Path(args.markdown_output))

    print("Paper-live observation completed")
    print(f"Ready for review: {report.ready_for_review}")
    print(f"Signals: {report.signal_count}")
    print(f"BUY_WATCH signals: {report.buy_watch_count}")
    print(f"Lifecycle events: {report.lifecycle_event_count}")
    print(f"Terminal events: {report.terminal_event_count}")
    print(f"Alerts: {report.alert_count}")
    print(f"JSON: {args.json_output}")
    print(f"Markdown: {args.markdown_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
