"""Generate BT3 reproducibility contract reports."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.validation.backtest_run_contract import (  # noqa: E402
    build_backtest_run_contract_report,
    demo_backtest_run_contracts,
    load_backtest_run_contracts_json,
    write_backtest_run_contract_report,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a BT3 reproducibility contract report.")
    parser.add_argument("--input-json", default="data/demo_backtest_run_contracts.json")
    parser.add_argument("--output-json", default="reports/backtest_run_contract/backtest_run_contract.json")
    parser.add_argument("--output-md", default="reports/backtest_run_contract/backtest_run_contract.md")
    parser.add_argument("--demo", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    items = demo_backtest_run_contracts() if args.demo else load_backtest_run_contracts_json(args.input_json)
    report = build_backtest_run_contract_report(items)
    write_backtest_run_contract_report(report, output_json=args.output_json, output_md=args.output_md)
    return 0 if report.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
