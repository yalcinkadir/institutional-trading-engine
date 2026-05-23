#!/usr/bin/env python3
"""Build governance-compatible portfolio_state.json from a manual snapshot."""

from __future__ import annotations

import argparse
import sys

from src.operations.manual_portfolio_sync import (
    ManualPortfolioSyncError,
    build_manual_portfolio_state,
    load_manual_portfolio_snapshot,
    write_manual_portfolio_sync_outputs,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sync manual portfolio snapshot into runtime portfolio state")
    parser.add_argument("--snapshot", default="data/manual_portfolio_snapshot.example.json")
    parser.add_argument("--portfolio-state-out", default="data/portfolio_state.json")
    parser.add_argument("--report-json-out", default="reports/portfolio/manual-portfolio-sync.json")
    parser.add_argument("--report-md-out", default="reports/portfolio/manual-portfolio-sync.md")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        snapshot = load_manual_portfolio_snapshot(args.snapshot)
        result = build_manual_portfolio_state(snapshot)
        write_manual_portfolio_sync_outputs(
            result=result,
            portfolio_state_path=args.portfolio_state_out,
            report_json_path=args.report_json_out,
            report_md_path=args.report_md_out,
        )
    except ManualPortfolioSyncError as exc:
        print(f"manual_portfolio_sync_failed:{exc}", file=sys.stderr)
        return 2

    print("manual_portfolio_sync_completed")
    print(f"portfolio_state={args.portfolio_state_out}")
    print(f"report_json={args.report_json_out}")
    print(f"report_md={args.report_md_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
