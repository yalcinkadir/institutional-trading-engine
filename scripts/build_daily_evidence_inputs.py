#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.validation.daily_evidence_input_builder import (  # noqa: E402
    build_daily_evidence_inputs,
    write_daily_evidence_input_build_report,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build daily evidence input files from raw observation source files.")
    parser.add_argument("--source-dir", type=Path, required=True, help="Directory containing raw daily evidence source JSON files.")
    parser.add_argument("--output-dir", type=Path, required=True, help="Directory where normalized daily evidence input files are written.")
    parser.add_argument("--report-dir", type=Path, required=True, help="Directory where build JSON and Markdown reports are written.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = build_daily_evidence_inputs(args.source_dir, args.output_dir)
    write_daily_evidence_input_build_report(
        report,
        json_path=args.report_dir / "daily_evidence_input_build.json",
        markdown_path=args.report_dir / "daily_evidence_input_build.md",
    )
    print(f"Daily evidence input build status: {'PASS' if report.passed else 'FAIL'}")
    print(f"Built files: {len(report.files)}")
    if report.errors:
        print("Errors:")
        for error in report.errors:
            print(f"- {error}")
    return 0 if report.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
