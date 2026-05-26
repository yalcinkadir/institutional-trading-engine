#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.validation.daily_paper_observation_source import (  # noqa: E402
    build_daily_paper_observation_sources,
    write_daily_paper_observation_source_report,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build real daily paper observation source files for the persisted feed.")
    parser.add_argument("--source-dir", type=Path, required=True, help="Directory with real daily paper observation raw source files.")
    parser.add_argument("--output-dir", type=Path, required=True, help="Directory where feed-compatible source files are written.")
    parser.add_argument("--report-dir", type=Path, required=True, help="Directory where JSON/Markdown build reports are written.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = build_daily_paper_observation_sources(args.source_dir, args.output_dir)
    write_daily_paper_observation_source_report(
        report,
        json_path=args.report_dir / "daily_paper_observation_source.json",
        markdown_path=args.report_dir / "daily_paper_observation_source.md",
    )
    print(f"Daily paper observation source status: {'PASS' if report.passed else 'FAIL'}")
    print(f"Built files: {len(report.files)}")
    for error in report.errors:
        print(f"ERROR: {error}")
    return 0 if report.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
