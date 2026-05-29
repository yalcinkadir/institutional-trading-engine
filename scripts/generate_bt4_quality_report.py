"""Generate BT4 backtest result quality reports."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.validation.backtest_result_quality_gate import (  # noqa: E402
    build_backtest_result_quality_report,
    demo_backtest_result_quality_cases,
    load_backtest_result_quality_json,
    write_backtest_result_quality_report,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a BT4 backtest result quality report.")
    parser.add_argument("--input-json", default="data/demo_backtest_result_quality.json")
    parser.add_argument("--output-json", default="reports/backtest_result_quality/backtest_result_quality.json")
    parser.add_argument("--output-md", default="reports/backtest_result_quality/backtest_result_quality.md")
    parser.add_argument("--demo", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    cases = demo_backtest_result_quality_cases() if args.demo else load_backtest_result_quality_json(args.input_json)
    report = build_backtest_result_quality_report(cases)
    write_backtest_result_quality_report(report, output_json=args.output_json, output_md=args.output_md)
    return 0 if report.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
