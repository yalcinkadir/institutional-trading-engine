#!/usr/bin/env python3
"""Run P27 operational readiness review."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.operations.operational_readiness_review import (
    run_operational_readiness_review,
    write_operational_readiness_report,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run operational readiness review.")
    parser.add_argument("--backtest-report", default="reports/backtests/historical-entry-exit-backtest.json")
    parser.add_argument("--oos-report", default="reports/backtests/out-of-sample-validation.json")
    parser.add_argument("--paper-live-report", default="reports/paper-live/paper-live-observation.json")
    parser.add_argument("--portfolio-state", default="data/portfolio_state.json")
    parser.add_argument("--min-backtest-plans", type=int, default=1)
    parser.add_argument("--min-oos-plans", type=int, default=1)
    parser.add_argument("--json-output", default="reports/readiness/operational-readiness-review.json")
    parser.add_argument("--markdown-output", default="reports/readiness/operational-readiness-review.md")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = run_operational_readiness_review(
        backtest_report=Path(args.backtest_report),
        oos_report=Path(args.oos_report),
        paper_live_report=Path(args.paper_live_report),
        portfolio_state=Path(args.portfolio_state),
        min_backtest_plans=args.min_backtest_plans,
        min_oos_plans=args.min_oos_plans,
    )
    write_operational_readiness_report(
        report,
        json_path=Path(args.json_output),
        markdown_path=Path(args.markdown_output),
    )

    print("Operational readiness review completed")
    print(f"Ready for live Decision-Support review: {report.ready_for_live_decision_support_review}")
    for gate in report.gates:
        status = "PASS" if gate.passed else "FAIL"
        print(f"{status}: {gate.name} - {gate.message}")
    print(f"JSON: {args.json_output}")
    print(f"Markdown: {args.markdown_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
