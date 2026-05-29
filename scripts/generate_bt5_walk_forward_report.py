#!/usr/bin/env python
from __future__ import annotations

import argparse
from pathlib import Path

from src.validation.walk_forward_robustness_gate import (
    build_walk_forward_robustness_report,
    demo_walk_forward_folds,
    load_walk_forward_folds_json,
    write_walk_forward_robustness_report,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a BT5 walk-forward / out-of-sample robustness gate report.")
    parser.add_argument("--input-json", type=Path, help="Input JSON with a 'folds' list.")
    parser.add_argument("--output-json", type=Path, default=Path("reports/bt5_walk_forward/robustness_report.json"))
    parser.add_argument("--output-md", type=Path, default=Path("reports/bt5_walk_forward/robustness_report.md"))
    parser.add_argument("--demo", action="store_true", help="Use public-safe synthetic demo folds.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.demo:
        folds = demo_walk_forward_folds()
    elif args.input_json:
        folds = load_walk_forward_folds_json(args.input_json)
    else:
        raise SystemExit("Provide --demo or --input-json.")

    report = build_walk_forward_robustness_report(folds)
    write_walk_forward_robustness_report(report, output_json=args.output_json, output_md=args.output_md)
    print(f"BT5 walk-forward robustness report written to {args.output_json} and {args.output_md}")
    return 0 if report.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
