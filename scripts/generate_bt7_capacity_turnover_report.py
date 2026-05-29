"""Generate BT7 capacity, turnover and realism reports."""

from __future__ import annotations

import argparse
from pathlib import Path

from src.validation.capacity_turnover_realism_gate import (
    build_capacity_turnover_realism_report,
    demo_capacity_turnover_snapshot,
    load_capacity_turnover_realism_json,
    render_capacity_turnover_realism_markdown,
    write_capacity_turnover_realism_report,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate BT7 capacity, turnover and realism report.")
    parser.add_argument("--input-json", type=Path, help="JSON file containing a BT7 snapshot.")
    parser.add_argument("--output-json", type=Path, default=Path("reports/bt7_capacity_turnover/report.json"))
    parser.add_argument("--output-md", type=Path, default=Path("reports/bt7_capacity_turnover/report.md"))
    parser.add_argument("--demo", action="store_true", help="Use built-in public-safe synthetic demo data.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.demo:
        snapshot = demo_capacity_turnover_snapshot()
    elif args.input_json:
        snapshot = load_capacity_turnover_realism_json(args.input_json)
    else:
        raise SystemExit("Provide --demo or --input-json.")

    report = build_capacity_turnover_realism_report(snapshot)
    write_capacity_turnover_realism_report(report, output_json=args.output_json, output_md=args.output_md)
    print(render_capacity_turnover_realism_markdown(report))
    return 0 if report.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
