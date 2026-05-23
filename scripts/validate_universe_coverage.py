"""Validate that a point-in-time universe is wide enough for backtesting.

Usage:
    python scripts/validate_universe_coverage.py \
        --universe data/universe/survivorship_universe.csv \
        --as-of 2024-01-02 \
        --minimum 500

Exits with status 1 when the tradeable universe is below the minimum.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

from src.data.survivorship_universe import load_survivorship_universe, validate_universe_coverage


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate backtest universe breadth")
    parser.add_argument("--universe", type=Path, required=True, help="Path to survivorship_universe.csv")
    parser.add_argument("--as-of", type=str, required=True, help="Point-in-time date, YYYY-MM-DD")
    parser.add_argument("--minimum", type=int, default=500, help="Minimum tradeable symbols required")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    universe = load_survivorship_universe(args.universe)
    report = validate_universe_coverage(
        universe,
        date.fromisoformat(args.as_of),
        minimum_tradeable_count=args.minimum,
    )
    print(json.dumps(report.to_dict(), indent=2))
    return 0 if report.passed else 1


if __name__ == "__main__":
    sys.exit(main())
