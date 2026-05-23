#!/usr/bin/env python3
"""Run Entry/Exit Watcher health diagnostics."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.operations.entry_exit_watcher_health import (
    run_entry_exit_watcher_health_check,
    write_watcher_health_report,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Entry/Exit Watcher health diagnostics.")
    parser.add_argument("--signals-file", default="reports/signals/latest-signals.json")
    parser.add_argument("--lifecycle-file", default="data/signal_lifecycle.jsonl")
    parser.add_argument("--min-signals", type=int, default=1)
    parser.add_argument("--min-lifecycle-events", type=int, default=1)
    parser.add_argument("--require-terminal-event", action="store_true")
    parser.add_argument("--json-output", default="reports/watcher/entry-exit-watcher-health.json")
    parser.add_argument("--markdown-output", default="reports/watcher/entry-exit-watcher-health.md")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = run_entry_exit_watcher_health_check(
        signals_file=Path(args.signals_file),
        lifecycle_file=Path(args.lifecycle_file),
        min_signals=args.min_signals,
        min_lifecycle_events=args.min_lifecycle_events,
        require_terminal_event=args.require_terminal_event,
    )
    write_watcher_health_report(
        report,
        json_path=Path(args.json_output),
        markdown_path=Path(args.markdown_output),
    )

    print("Entry/Exit Watcher health check completed")
    print(f"Healthy: {report.healthy}")
    print(f"Signals: {report.signal_count}")
    print(f"BUY_WATCH signals: {report.buy_watch_count}")
    print(f"Lifecycle events: {report.lifecycle_event_count}")
    print(f"Terminal events: {report.terminal_event_count}")
    print(f"Malformed lifecycle lines: {report.malformed_lifecycle_lines}")
    print(f"JSON: {args.json_output}")
    print(f"Markdown: {args.markdown_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
