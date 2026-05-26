#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.validation.daily_evidence_input_validation import (  # noqa: E402
    validate_daily_evidence_inputs,
    write_daily_evidence_input_validation_report,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate daily evidence input JSON files before component generation.")
    parser.add_argument("--input-dir", type=Path, required=True, help="Directory containing daily evidence input JSON files.")
    parser.add_argument("--output-dir", type=Path, required=True, help="Directory for validation JSON and Markdown reports.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = validate_daily_evidence_inputs(args.input_dir)
    write_daily_evidence_input_validation_report(
        report,
        json_path=args.output_dir / "daily_evidence_input_validation.json",
        markdown_path=args.output_dir / "daily_evidence_input_validation.md",
    )
    print(f"Daily evidence input validation status: {'PASS' if report.passed else 'FAIL'}")
    print(f"Files present: {report.metrics.files_present}/{report.metrics.files_expected}")
    print(f"Validation report written: {args.output_dir / 'daily_evidence_input_validation.json'}")
    return 0 if report.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
