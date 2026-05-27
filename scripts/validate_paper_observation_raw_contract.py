#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.validation.paper_observation_raw_contract import (  # noqa: E402
    validate_raw_observation_contract,
    write_raw_contract_report,
    write_raw_contract_template,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate or create real paper observation raw data contract files.")
    parser.add_argument("--source-dir", type=Path, required=True, help="Directory containing raw paper observation files.")
    parser.add_argument("--report-dir", type=Path, required=True, help="Directory where validation reports are written.")
    parser.add_argument("--write-template", action="store_true", help="Write a daily raw source template before validation.")
    parser.add_argument("--report-date", default="2026-05-27", help="Report date used for generated templates.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.write_template:
        paths = write_raw_contract_template(args.source_dir, report_date=args.report_date)
        print("Wrote raw paper observation templates:")
        for path in paths:
            print(f"- {path}")

    report = validate_raw_observation_contract(args.source_dir)
    write_raw_contract_report(
        report,
        json_path=args.report_dir / "paper_observation_raw_contract.json",
        markdown_path=args.report_dir / "paper_observation_raw_contract.md",
    )
    print(f"Raw paper observation contract status: {'PASS' if report.passed else 'FAIL'}")
    for issue in report.issues:
        print(f"ISSUE: {issue.file_name} {issue.record_index} {issue.field}: {issue.message}")
    return 0 if report.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
