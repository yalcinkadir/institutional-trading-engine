#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.validation.daily_evidence_source_bootstrap import (  # noqa: E402
    bootstrap_daily_evidence_sources,
    write_daily_evidence_source_bootstrap_report,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Bootstrap observation-only daily evidence source files for Day-0 workflow activation.")
    parser.add_argument("--output-dir", type=Path, required=True, help="Directory where source JSON files are written.")
    parser.add_argument("--report-dir", type=Path, required=True, help="Directory where bootstrap JSON and Markdown reports are written.")
    parser.add_argument("--report-date", required=True, help="Report date YYYY-MM-DD used to anchor bootstrap dates.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = bootstrap_daily_evidence_sources(args.output_dir, report_date=args.report_date)
    write_daily_evidence_source_bootstrap_report(
        report,
        json_path=args.report_dir / "daily_evidence_source_bootstrap.json",
        markdown_path=args.report_dir / "daily_evidence_source_bootstrap.md",
    )
    print("Daily evidence source bootstrap status: PASS")
    print("Observation-only bootstrap seed created; not statistically meaningful forward evidence")
    print(f"Files written: {len(report.files)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
