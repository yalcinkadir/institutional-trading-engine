#!/usr/bin/env python3
"""Evaluate the Evidence Quality Gate (#188) from a JSON input file."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.evidence_quality_gate import evaluate_evidence_quality_gate


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate Evidence Quality Gate #188.")
    parser.add_argument(
        "--input",
        required=True,
        help="Path to JSON input containing evidence-quality gate fields.",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Optional path to write the machine-readable gate result JSON.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_path = Path(args.input)
    payload = json.loads(input_path.read_text(encoding="utf-8"))
    result = evaluate_evidence_quality_gate(payload)
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")

    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
