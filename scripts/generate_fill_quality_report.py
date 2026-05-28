#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.validation.fill_quality_report import (  # noqa: E402
    analyze_fill_quality,
    load_fill_quality_records,
    write_fill_quality_report,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a C6 fill-quality audit report from observed fill records.")
    parser.add_argument("--input-file", type=Path, required=True, help="JSON file with fill-quality records or records[].")
    parser.add_argument("--output-dir", type=Path, required=True, help="Directory for JSON and Markdown output.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    records = load_fill_quality_records(args.input_file)
    report = analyze_fill_quality(records)
    write_fill_quality_report(
        report,
        json_path=args.output_dir / "fill_quality_report.json",
        markdown_path=args.output_dir / "fill_quality_report.md",
    )
    print(f"Fill quality status: {report.status.value}")
    print(f"Records: {report.metrics.record_count}")
    print(f"Fill rate: {report.metrics.fill_rate:.2%}")
    print(f"Average absolute slippage: {report.metrics.avg_abs_slippage_bps:.4f} bps")
    print(f"Report written: {args.output_dir / 'fill_quality_report.json'}")
    return 0 if report.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
