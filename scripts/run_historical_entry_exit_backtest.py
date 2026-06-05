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
    parser.add_argument("--run-id", default="historical-demo-run")
    parser.add_argument("--data-source", default="historical_demo", choices=["historical_demo", "real_data"])
    parser.add_argument("--strategy-version", default="historical-entry-exit-v1")
    parser.add_argument("--real-data", action="store_true", help="Mark output as real historical-data evidence.")
    parser.add_argument("--json-output", default="reports/backtests/historical-entry-exit-backtest.json")
    parser.add_argument("--markdown-output", default="reports/backtests/historical-entry-exit-backtest.md")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    plans = load_trade_plans(Path(args.plans_file))
    data_source = "real_data" if args.real_data else args.data_source
    is_demo = data_source != "real_data"
    report = run_backtest(
        plans,
        bars_root=Path(args.bars_root),
        max_bars=args.max_bars,
        run_id=args.run_id,
        data_source=data_source,
        is_demo=is_demo,
        strategy_version=args.strategy_version,
    )
    write_report(report, json_path=Path(args.json_output), markdown_path=Path(args.markdown_output))

    print("Historical Entry / Stop / Exit backtest completed")
    print(f"Run ID: {report.run_id}")
    print(f"Data source: {report.data_source}")
    print(f"Is demo: {report.is_demo}")
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
