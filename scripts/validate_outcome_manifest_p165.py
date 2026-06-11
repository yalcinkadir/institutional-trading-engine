#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

ALLOWED_STATUSES = {"SUCCESS", "BLOCKED_NO_VALID_SIGNALS", "DEMO_NO_DATA", "BLOCKED_MISSING_INPUTS"}
REQUIRED_FIELDS = [
    "run_status",
    "mode",
    "scanned_signal_files",
    "total_input_signals",
    "valid_signal_count",
    "invalid_signal_count",
    "evaluable_signal_count",
    "evaluated_outcome_count",
    "skipped_count",
    "skip_reasons",
    "upstream_dependency_status",
    "outcome_learning_claim_allowed",
    "manifest_contract_version",
]
COUNT_FIELDS = [
    "scanned_signal_files",
    "total_input_signals",
    "valid_signal_count",
    "invalid_signal_count",
    "evaluable_signal_count",
    "evaluated_outcome_count",
    "skipped_count",
]


def validate_manifest(path: Path, *, allow_demo_no_data: bool = False) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"missing outcome manifest: {path}")

    manifest = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict):
        raise ValueError("outcome manifest must be a JSON object")

    missing = [field for field in REQUIRED_FIELDS if field not in manifest]
    if missing:
        raise ValueError(f"missing outcome manifest fields: {missing}")

    status = manifest.get("run_status")
    if status not in ALLOWED_STATUSES:
        raise ValueError(f"unexpected outcome run_status: {status}")

    for field in COUNT_FIELDS:
        value = manifest.get(field)
        if not isinstance(value, int) or value < 0:
            raise ValueError(f"{field} must be a non-negative integer")

    if not isinstance(manifest.get("skip_reasons"), list):
        raise ValueError("skip_reasons must be a list")

    if not isinstance(manifest.get("outcome_learning_claim_allowed"), bool):
        raise ValueError("outcome_learning_claim_allowed must be boolean")

    mode = str(manifest.get("mode") or "")
    valid_signal_count = int(manifest.get("valid_signal_count") or 0)
    evaluated_count = int(manifest.get("evaluated_outcome_count") or 0)

    if status == "SUCCESS":
        if mode != "production":
            raise ValueError("SUCCESS outcome manifests must be production mode")
        if valid_signal_count <= 0:
            raise ValueError("SUCCESS requires at least one valid upstream signal")
        if not manifest["outcome_learning_claim_allowed"]:
            raise ValueError("SUCCESS must allow outcome-learning claims")

    if status == "BLOCKED_NO_VALID_SIGNALS":
        if mode != "production":
            raise ValueError("BLOCKED_NO_VALID_SIGNALS is reserved for production mode")
        if valid_signal_count != 0:
            raise ValueError("BLOCKED_NO_VALID_SIGNALS requires zero valid upstream signals")
        if evaluated_count != 0:
            raise ValueError("BLOCKED_NO_VALID_SIGNALS cannot evaluate outcomes")
        if manifest["outcome_learning_claim_allowed"]:
            raise ValueError("blocked no-valid-signal runs cannot allow outcome-learning claims")
        if "no_valid_signals_in_window" not in manifest["skip_reasons"] and "no_signal_files_in_window" not in manifest["skip_reasons"]:
            raise ValueError("blocked no-valid-signal runs must include a clear skip reason")

    if status == "DEMO_NO_DATA":
        if mode != "demo":
            raise ValueError("DEMO_NO_DATA requires demo mode")
        if not allow_demo_no_data:
            raise ValueError("DEMO_NO_DATA is not allowed unless --allow-demo-no-data is set")
        if valid_signal_count != 0:
            raise ValueError("DEMO_NO_DATA requires zero valid upstream signals")
        if manifest["outcome_learning_claim_allowed"]:
            raise ValueError("demo no-data runs cannot allow outcome-learning claims")

    if status == "BLOCKED_MISSING_INPUTS":
        if valid_signal_count != 0:
            raise ValueError("missing-input runs cannot have valid signals")
        if manifest["outcome_learning_claim_allowed"]:
            raise ValueError("missing-input runs cannot allow outcome-learning claims")

    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate P165/#186 outcome run manifest contract.")
    parser.add_argument("--manifest", type=Path, default=Path("reports/outcomes/outcome-run-manifest.json"))
    parser.add_argument("--allow-demo-no-data", action="store_true", help="Allow explicit local/demo no-data manifests.")
    args = parser.parse_args()

    manifest = validate_manifest(args.manifest, allow_demo_no_data=args.allow_demo_no_data)
    print(f"outcome run_status={manifest['run_status']}")
    print(f"mode={manifest['mode']}")
    print(f"scanned_signal_files={manifest['scanned_signal_files']}")
    print(f"total_input_signals={manifest['total_input_signals']}")
    print(f"valid_signal_count={manifest['valid_signal_count']}")
    print(f"invalid_signal_count={manifest['invalid_signal_count']}")
    print(f"evaluable_signal_count={manifest['evaluable_signal_count']}")
    print(f"evaluated_outcome_count={manifest['evaluated_outcome_count']}")
    print(f"outcome_learning_claim_allowed={manifest['outcome_learning_claim_allowed']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
