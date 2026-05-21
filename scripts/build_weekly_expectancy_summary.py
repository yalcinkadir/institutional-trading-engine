#!/usr/bin/env python3
"""Build a compact weekly expectancy feedback summary.

The output is suitable for GitHub Actions logs, artifacts and optional Telegram
messages.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.expectancy_feedback_summary import build_weekly_expectancy_summary
from src.outcome_pipeline import build_expectancy_summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build weekly expectancy feedback summary.")
    parser.add_argument(
        "--decision-log",
        default="data/decision_log.csv",
        help="Decision log CSV or JSONL path.",
    )
    parser.add_argument(
        "--output",
        default="reports/weekly-expectancy-summary.txt",
        help="Text output path.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    summary = build_expectancy_summary(Path(args.decision_log))
    text = build_weekly_expectancy_summary(summary)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(text, encoding="utf-8")

    print(text)
    print(f"Weekly expectancy summary written to: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
