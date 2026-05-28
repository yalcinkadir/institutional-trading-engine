#!/usr/bin/env python3
"""Generate a BT2 Strategy Test Matrix report."""

from __future__ import annotations

import argparse
from pathlib import Path

from src.validation.strategy_test_matrix import (
    build_strategy_test_matrix,
    demo_strategy_test_matrix_cases,
    load_strategy_test_matrix_json,
    write_strategy_test_matrix_report,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate BT2 Strategy Test Matrix report")
    parser.add_argument(
        "--input-json",
        default="data/demo_strategy_test_matrix.json",
        help="Input matrix JSON. If missing and --demo is passed, built-in demo cases are used.",
    )
    parser.add_argument("--output-json", default="reports/strategy_test_matrix/strategy_test_matrix.json")
    parser.add_argument("--output-md", default="reports/strategy_test_matrix/strategy_test_matrix.md")
    parser.add_argument("--demo", action="store_true", help="Use built-in public-safe demo cases")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_path = Path(args.input_json)
    if args.demo:
        cases = demo_strategy_test_matrix_cases()
    else:
        cases = load_strategy_test_matrix_json(input_path)

    report = build_strategy_test_matrix(cases)
    write_strategy_test_matrix_report(
        report,
        json_path=Path(args.output_json),
        markdown_path=Path(args.output_md),
    )

    print(f"BT2 Strategy Test Matrix status: {'PASS' if report.passed else 'FAIL'}")
    print(f"Cases: {report.metrics.total_cases}")
    print(f"Strategies: {report.metrics.strategy_count}")
    print(f"JSON: {args.output_json}")
    print(f"Markdown: {args.output_md}")
    return 0 if report.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
