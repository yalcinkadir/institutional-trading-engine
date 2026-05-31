"""
Generate daily fill-quality evidence from a JSON list of paper execution fills.

Input JSON shape:

[
  {
    "order_id": "paper-1",
    "signal_id": "sig-1",
    "symbol": "NVDA",
    "side": "BUY",
    "quantity": 10,
    "expected_price": 100.0,
    "actual_price": 100.1,
    "fill_status": "FILLED",
    "reconciliation_status": "RECONCILED",
    "timestamp": "2026-05-31T14:30:00+00:00"
  }
]
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.operations.fill_quality_evidence import (
    build_fill_quality_evidence,
    validate_fill_quality_evidence,
    write_fill_quality_evidence,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate daily fill-quality evidence for paper observation."
    )
    parser.add_argument("--trading-date", required=True)
    parser.add_argument(
        "--input",
        required=True,
        help="JSON file containing a list of raw fill records.",
    )
    parser.add_argument(
        "--output-dir",
        default="reports/evidence/fill_quality",
        help="Directory where fill-quality evidence JSON should be written.",
    )
    parser.add_argument(
        "--note",
        action="append",
        default=[],
        help="Optional note written into the evidence artifact.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    raw_payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    if not isinstance(raw_payload, list):
        raise SystemExit("Input JSON must be a list of fill records.")

    evidence = build_fill_quality_evidence(
        trading_date=args.trading_date,
        raw_records=[item for item in raw_payload if isinstance(item, dict)],
        notes=args.note,
    )
    output_path = write_fill_quality_evidence(
        evidence,
        output_dir=args.output_dir,
    )
    validation = validate_fill_quality_evidence(evidence)

    print(f"Fill-quality evidence written: {output_path}")
    print(f"Evidence status: {evidence.status}")

    if validation["status"] != "PASS":
        print(f"Evidence validation errors: {validation['errors']}")
        return 2

    return 0 if evidence.status in {"PASS", "WARN"} else 1


if __name__ == "__main__":
    raise SystemExit(main())