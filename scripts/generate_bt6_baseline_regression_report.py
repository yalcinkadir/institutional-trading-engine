"""Generate BT6 evidence baseline regression reports."""

from __future__ import annotations

import argparse
from pathlib import Path

from src.validation.evidence_baseline_regression_gate import (
    build_evidence_baseline_regression_report,
    demo_evidence_baseline_pair,
    load_evidence_baseline_regression_json,
    render_evidence_baseline_regression_markdown,
    write_evidence_baseline_regression_report,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate BT6 evidence baseline regression report.")
    parser.add_argument("--input-json", type=Path, help="JSON file containing baseline and current snapshots.")
    parser.add_argument("--output-json", type=Path, default=Path("reports/bt6_baseline_regression/report.json"))
    parser.add_argument("--output-md", type=Path, default=Path("reports/bt6_baseline_regression/report.md"))
    parser.add_argument("--demo", action="store_true", help="Use built-in public-safe synthetic demo data.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.demo:
        baseline, current = demo_evidence_baseline_pair()
    elif args.input_json:
        baseline, current = load_evidence_baseline_regression_json(args.input_json)
    else:
        raise SystemExit("Provide --demo or --input-json.")

    report = build_evidence_baseline_regression_report(baseline, current)
    write_evidence_baseline_regression_report(report, output_json=args.output_json, output_md=args.output_md)
    print(render_evidence_baseline_regression_markdown(report))
    return 0 if report.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
