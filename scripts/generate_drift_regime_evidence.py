"""
Generate daily drift/regime evidence from JSON.

Input JSON shape:

{
  "previous_regime": "BULL",
  "current_regime": "NEUTRAL",
  "cumulative_drift_value": 0.12,
  "metrics": [
    {
      "name": "decision_score_mean",
      "observed_value": 0.63,
      "expected_value": 0.60,
      "warn_threshold": 0.05,
      "fail_threshold": 0.15
    }
  ]
}
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.operations.drift_regime_evidence import (
    build_drift_metric,
    build_drift_regime_evidence,
    validate_drift_regime_evidence,
    write_drift_regime_evidence,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate daily drift/regime evidence for paper observation."
    )
    parser.add_argument("--trading-date", required=True)
    parser.add_argument(
        "--input",
        required=True,
        help="JSON file containing drift metrics and regime state.",
    )
    parser.add_argument(
        "--output-dir",
        default="reports/evidence/drift_regime",
        help="Directory where drift/regime evidence JSON should be written.",
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

    payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise SystemExit("Input JSON must be an object.")

    metrics = [
        build_drift_metric(
            name=str(item["name"]),
            observed_value=float(item["observed_value"]),
            expected_value=float(item["expected_value"]),
            warn_threshold=float(item.get("warn_threshold", 0.05)),
            fail_threshold=float(item.get("fail_threshold", 0.15)),
        )
        for item in payload.get("metrics", [])
        if isinstance(item, dict)
    ]

    evidence = build_drift_regime_evidence(
        trading_date=args.trading_date,
        drift_metrics=metrics,
        previous_regime=payload.get("previous_regime"),
        current_regime=payload.get("current_regime"),
        cumulative_drift_value=float(payload.get("cumulative_drift_value", 0.0)),
        cumulative_drift_warn_threshold=float(
            payload.get("cumulative_drift_warn_threshold", 0.10)
        ),
        cumulative_drift_fail_threshold=float(
            payload.get("cumulative_drift_fail_threshold", 0.30)
        ),
        notes=args.note,
    )

    output_path = write_drift_regime_evidence(evidence, output_dir=args.output_dir)
    validation = validate_drift_regime_evidence(evidence)

    print(f"Drift/regime evidence written: {output_path}")
    print(f"Evidence status: {evidence.status}")

    if validation["status"] != "PASS":
        print(f"Evidence validation errors: {validation['errors']}")
        return 2

    return 0 if evidence.status in {"PASS", "WARN"} else 1


if __name__ == "__main__":
    raise SystemExit(main())