#!/usr/bin/env python3
"""Run historical Entry / Stop / Exit backtest from JSON trade plans."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.backtesting.historical_entry_exit_backtest import load_trade_plans, run_backtest
from src.backtesting.historical_report import write_report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run historical Entry / Stop / Exit backtest.")
    parser.add_argument("--plans-file", required=True, help="JSON list, plans[] or signals[] with trade plans.")
    parser.add_argument("--bars-root", default="data/historical/bars/1day")
    parser.add_argument("--max-bars", type=int, default=20)
    parser.add_argument("--json-output", default="reports/backtests/historical-entry-exit-backtest.json")
    parser.add_argument("--markdown-output", default="reports/backtests/historical-entry-exit-backtest.md")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    plans = load_trade_plans(Path(args.plans_file))
    report = run_backtest(plans, bars_root=Path(args.bars_root), max_bars=args.max_bars)
    write_report(report, json_path=Path(args.json_output), markdown_path=Path(args.markdown_output))

    print("Historical Entry / Stop / Exit backtest completed")
    print(f"Plans: {report.metrics.total}")
    print(f"Entry hit rate: {report.metrics.entry_hit_rate:.2%}")
    print(f"Target 1 hit rate: {report.metrics.target_1_hit_rate:.2%}")
    print(f"Target 2 hit rate: {report.metrics.target_2_hit_rate:.2%}")
    print(f"Stop hit rate: {report.metrics.stop_hit_rate:.2%}")
    print(f"Expectancy R: {report.metrics.expectancy_r:.4f}")
    print(f"JSON: {args.json_output}")
    print(f"Markdown: {args.markdown_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
