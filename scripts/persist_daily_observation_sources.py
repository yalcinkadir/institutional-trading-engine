#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.validation.daily_observation_source_feed import (  # noqa: E402
    persist_daily_observation_sources,
    write_daily_observation_source_feed_report,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Persist incoming daily observation source records into the observation source feed.")
    parser.add_argument("--incoming-dir", type=Path, required=True, help="Directory with incoming daily source JSON files.")
    parser.add_argument("--feed-dir", type=Path, required=True, help="Persistent source feed directory.")
    parser.add_argument("--report-dir", type=Path, required=True, help="Directory where feed JSON and Markdown reports are written.")
    parser.add_argument("--report-date", required=True, help="Report date YYYY-MM-DD used for feed metadata.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = persist_daily_observation_sources(args.incoming_dir, args.feed_dir, report_date=args.report_date)
    write_daily_observation_source_feed_report(
        report,
        json_path=args.report_dir / "daily_observation_source_feed.json",
        markdown_path=args.report_dir / "daily_observation_source_feed.md",
    )
    print(f"Daily observation source feed status: {'PASS' if report.passed else 'FAIL'}")
    print(f"Files persisted: {len(report.files)}")
    if report.errors:
        print("Errors:")
        for error in report.errors:
            print(f"- {error}")
    return 0 if report.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
