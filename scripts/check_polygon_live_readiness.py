#!/usr/bin/env python3
"""Check readiness for live Polygon data operations."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.operations.polygon_live_readiness import run_polygon_live_readiness


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check live Polygon data readiness.")
    parser.add_argument("--symbols", default=None, help="Comma-separated symbols. Defaults to core live symbols.")
    parser.add_argument("--end-date", default=None, help="YYYY-MM-DD. Defaults to today.")
    parser.add_argument("--lookback-days", type=int, default=5000)
    parser.add_argument("--signals-file", default="reports/signals/latest-signals.json")
    parser.add_argument("--portfolio-state-file", default="data/portfolio_state.json")
    parser.add_argument("--json", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    end_date = date.fromisoformat(args.end_date) if args.end_date else None
    result = run_polygon_live_readiness(
        symbols=args.symbols,
        end_date=end_date,
        lookback_days=args.lookback_days,
        signal_file=Path(args.signals_file),
        portfolio_state_file=Path(args.portfolio_state_file),
    )

    if args.json:
        print(json.dumps(result.to_dict(), indent=2))
    else:
        print(f"Polygon live readiness: {'PASS' if result.passed else 'FAIL'}")
        print(f"Historical window: {result.start_date} → {result.end_date}")
        print(f"Symbols: {', '.join(result.symbols)}")
        print("\nChecks:")
        for check in result.checks:
            mark = "✅" if check.passed else "❌"
            print(f"{mark} {check.name}: {check.message}")
        print("\nCommands to run after subscription/API key is active:")
        for command in result.commands:
            print(f"- {command}")
        print("\nLive gates:")
        for gate in result.gates:
            print(f"- {gate}")

    return 0 if result.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
