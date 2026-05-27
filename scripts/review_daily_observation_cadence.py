#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.validation.daily_observation_cadence import (  # noqa: E402
    review_daily_observation_cadence,
    write_cadence_report,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Review daily paper observation capture and artifact completeness.")
    parser.add_argument("--report-date", required=True, help="Report date YYYY-MM-DD.")
    parser.add_argument(
        "--raw-source-dir",
        type=Path,
        required=True,
        help="Directory containing raw daily paper observation source files.",
    )
    parser.add_argument(
        "--artifact-root",
        type=Path,
        default=Path("reports"),
        help="Root directory containing daily evidence artifact folders.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Directory where cadence review JSON/Markdown files are written.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = review_daily_observation_cadence(
        report_date=args.report_date,
        raw_source_dir=args.raw_source_dir,
        artifact_root=args.artifact_root,
    )
    write_cadence_report(
        report,
        json_path=args.output_dir / "daily_observation_cadence_review.json",
        markdown_path=args.output_dir / "daily_observation_cadence_review.md",
    )
    print(f"Daily observation cadence review status: {'PASS' if report.passed else 'FAIL'}")
    for gate in report.gates:
        print(f"{gate.name}: {'PASS' if gate.passed else 'FAIL'} ({gate.value} / {gate.threshold})")
    return 0 if report.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
