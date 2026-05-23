#!/usr/bin/env python3
"""Run P25 historical reconstruction and out-of-sample validation."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.backtesting.out_of_sample_validation import (
    reconstruct_plans_for_symbols,
    validate_out_of_sample,
    write_reconstructed_plans,
    write_validation_report,
)


def _symbols(value: str) -> list[str]:
    return [symbol.strip().upper() for symbol in value.split(",") if symbol.strip()]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run historical out-of-sample validation.")
    parser.add_argument("--symbols", default="SPY,QQQ,NVDA,AAPL,MSFT,AMD,TSLA,META,GOOGL,AMZN")
    parser.add_argument("--bars-root", default="data/historical/bars/1day")
    parser.add_argument("--split-date", required=True)
    parser.add_argument("--lookback-bars", type=int, default=20)
    parser.add_argument("--every-nth-signal", type=int, default=20)
    parser.add_argument("--max-bars", type=int, default=20)
    parser.add_argument("--plans-output", default="reports/backtests/reconstructed-historical-plans.json")
    parser.add_argument("--json-output", default="reports/backtests/out-of-sample-validation.json")
    parser.add_argument("--markdown-output", default="reports/backtests/out-of-sample-validation.md")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    symbols = _symbols(args.symbols)
    if not symbols:
        raise SystemExit("No symbols provided")

    plans = reconstruct_plans_for_symbols(
        symbols=symbols,
        bars_root=Path(args.bars_root),
        lookback_bars=args.lookback_bars,
        every_nth_signal=args.every_nth_signal,
    )
    report = validate_out_of_sample(
        plans=plans,
        bars_root=Path(args.bars_root),
        split_date=args.split_date,
        max_bars=args.max_bars,
    )
    write_reconstructed_plans(plans, Path(args.plans_output))
    write_validation_report(report, json_path=Path(args.json_output), markdown_path=Path(args.markdown_output))

    print("Out-of-sample historical validation completed")
    print(f"Symbols: {','.join(symbols)}")
    print(f"Reconstructed plans: {report.reconstructed_plan_count}")
    print(f"Split date: {report.split_date}")
    print(f"In-sample plans: {report.in_sample_count}")
    print(f"Out-of-sample plans: {report.out_of_sample_count}")
    print(f"In-sample expectancy R: {report.in_sample_metrics.expectancy_r:.4f}")
    print(f"Out-of-sample expectancy R: {report.out_of_sample_metrics.expectancy_r:.4f}")
    print(f"Plans: {args.plans_output}")
    print(f"JSON: {args.json_output}")
    print(f"Markdown: {args.markdown_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
