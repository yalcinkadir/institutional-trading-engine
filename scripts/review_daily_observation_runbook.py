#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.validation.daily_observation_runbook import (  # noqa: E402
    review_daily_observation_runbook,
    write_runbook_report,
    write_runbook_template,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Review the daily real paper observation runbook checklist.")
    parser.add_argument("--checklist", type=Path, required=True, help="Daily runbook checklist JSON path.")
    parser.add_argument("--output-dir", type=Path, required=True, help="Directory where runbook review reports are written.")
    parser.add_argument("--report-date", required=True, help="Expected report date YYYY-MM-DD.")
    parser.add_argument("--write-template", action="store_true", help="Write a checklist template before review.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.write_template:
        path = write_runbook_template(args.checklist, report_date=args.report_date)
        print(f"Wrote daily observation runbook template: {path}")

    report = review_daily_observation_runbook(args.checklist, expected_report_date=args.report_date)
    write_runbook_report(
        report,
        json_path=args.output_dir / "daily_observation_runbook_review.json",
        markdown_path=args.output_dir / "daily_observation_runbook_review.md",
    )
    print(f"Daily observation runbook review status: {'PASS' if report.passed else 'FAIL'}")
    for issue in report.issues:
        print(f"ISSUE: {issue.field}: {issue.message}")
    for step in report.missing_steps:
        print(f"MISSING_STEP: {step}")
    return 0 if report.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
