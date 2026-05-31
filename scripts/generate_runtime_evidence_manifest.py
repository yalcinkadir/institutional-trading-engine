"""
Generate a daily runtime evidence manifest.

Example:

python scripts/generate_runtime_evidence_manifest.py \
  --trading-date 2026-05-31 \
  --required-input reports/signals/latest-signals.json \
  --required-output reports/alerts/latest-alerts.json \
  --required-governance-state data/portfolio_state.json \
  --required-governance-state data/anomaly_state.json
"""

from __future__ import annotations

import argparse
from pathlib import Path

from src.operations.runtime_evidence_manifest import (
    build_runtime_evidence_manifest,
    validate_runtime_evidence_manifest,
    write_runtime_evidence_manifest,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a daily runtime evidence manifest."
    )
    parser.add_argument("--trading-date", required=True)
    parser.add_argument(
        "--required-input",
        action="append",
        default=[],
        help="Required input artifact path. May be supplied multiple times.",
    )
    parser.add_argument(
        "--required-output",
        action="append",
        default=[],
        help="Required output artifact path. May be supplied multiple times.",
    )
    parser.add_argument(
        "--required-governance-state",
        action="append",
        default=[],
        help="Required governance-state artifact path. May be supplied multiple times.",
    )
    parser.add_argument(
        "--optional-artifact",
        action="append",
        default=[],
        help="Optional artifact path. May be supplied multiple times.",
    )
    parser.add_argument(
        "--output-dir",
        default="reports/evidence/manifests",
        help="Directory where the manifest should be written.",
    )
    parser.add_argument(
        "--observation-mode",
        default="paper_observation",
        help="Observation mode label written into the manifest.",
    )
    parser.add_argument(
        "--note",
        action="append",
        default=[],
        help="Optional manifest note. May be supplied multiple times.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    manifest = build_runtime_evidence_manifest(
        trading_date=args.trading_date,
        required_inputs=[Path(item) for item in args.required_input],
        required_outputs=[Path(item) for item in args.required_output],
        required_governance_state=[
            Path(item) for item in args.required_governance_state
        ],
        optional_artifacts=[Path(item) for item in args.optional_artifact],
        observation_mode=args.observation_mode,
        notes=args.note,
    )

    output_path = write_runtime_evidence_manifest(
        manifest,
        output_dir=args.output_dir,
    )

    validation = validate_runtime_evidence_manifest(manifest)
    print(f"Runtime evidence manifest written: {output_path}")
    print(f"Manifest status: {manifest.status}")

    if validation["status"] != "PASS":
        print(f"Manifest validation errors: {validation['errors']}")
        return 2

    return 0 if manifest.status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())