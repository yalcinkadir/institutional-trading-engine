"""Run the gated edge-evidence backtest pipeline.

This command activates backtesting only when evidence gates pass.
It writes reports into reports/edge_evidence by default and exits with
status 1 when any gate fails.
"""

from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.backtesting.edge_evidence_backtest import (
    EdgeEvidenceBacktestConfig,
    run_edge_evidence_backtest,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run gated edge-evidence backtest")
    parser.add_argument("--universe", type=Path, default=Path("data/universe/survivorship_universe.csv"))
    parser.add_argument("--plans", type=Path, default=Path("data/trade_plans/historical_trade_plans.json"))
    parser.add_argument("--bars-root", type=Path, default=Path("data/historical_bars"))
    parser.add_argument("--output-dir", type=Path, default=Path("reports/edge_evidence"))
    parser.add_argument("--as-of", default="2026-05-24")
    parser.add_argument("--minimum-assets", type=int, default=500)
    parser.add_argument("--oos-split-date", default="2024-01-01")
    parser.add_argument("--max-bars-per-plan", type=int, default=20)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config = EdgeEvidenceBacktestConfig(
        universe_path=args.universe,
        trade_plans_path=args.plans,
        bars_root=args.bars_root,
        output_dir=args.output_dir,
        as_of=date.fromisoformat(args.as_of),
        minimum_tradeable_count=args.minimum_assets,
        oos_split_date=date.fromisoformat(args.oos_split_date),
        max_bars_per_plan=args.max_bars_per_plan,
    )
    report = run_edge_evidence_backtest(config)
    print(f"Edge evidence backtest status: {'PASS' if report.passed else 'FAIL'}")
    print(f"Summary written to: {config.output_dir / 'edge-evidence-summary.md'}")
    if report.reasons:
        print("Reasons:")
        for reason in report.reasons:
            print(f"- {reason}")
    return 0 if report.passed else 1


if __name__ == "__main__":
    sys.exit(main())
