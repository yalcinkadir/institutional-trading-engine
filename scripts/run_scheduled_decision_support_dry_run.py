#!/usr/bin/env python3
"""Run P28 scheduled/manual Live Decision-Support dry-run report."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.operations.scheduled_decision_support_dry_run import (
    run_scheduled_decision_support_dry_run,
    write_scheduled_dry_run_report,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run scheduled Live Decision-Support dry-run report.")
    parser.add_argument("--run-mode", default="manual")
    parser.add_argument("--backtest-report", default="reports/backtests/historical-entry-exit-backtest.json")
    parser.add_argument("--oos-report", default="reports/backtests/out-of-sample-validation.json")
    parser.add_argument("--paper-live-report", default="reports/paper-live/paper-live-observation.json")
    parser.add_argument("--portfolio-state", default="data/portfolio_state.json")
    parser.add_argument("--min-backtest-plans", type=int, default=1)
    parser.add_argument("--min-oos-plans", type=int, default=1)
    parser.add_argument("--json-output", default="reports/scheduled-runs/scheduled-decision-support-dry-run.json")
    parser.add_argument("--markdown-output", default="reports/scheduled-runs/scheduled-decision-support-dry-run.md")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = run_scheduled_decision_support_dry_run(
        run_mode=args.run_mode,
        backtest_report=Path(args.backtest_report),
        oos_report=Path(args.oos_report),
        paper_live_report=Path(args.paper_live_report),
        portfolio_state=Path(args.portfolio_state),
        min_backtest_plans=args.min_backtest_plans,
        min_oos_plans=args.min_oos_plans,
    )
    write_scheduled_dry_run_report(
        report,
        json_path=Path(args.json_output),
        markdown_path=Path(args.markdown_output),
    )

    print("Scheduled Live Decision-Support dry run completed")
    print(f"Run mode: {report.run_mode}")
    print(f"Generated at UTC: {report.generated_at_utc}")
    print(f"Ready for live Decision-Support review: {report.ready_for_live_decision_support_review}")
    print(f"JSON: {args.json_output}")
    print(f"Markdown: {args.markdown_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
