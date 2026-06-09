#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

ALLOWED_STATUSES = {"OK", "NO_ELIGIBLE_SIGNALS", "BLOCKED_MISSING_INPUTS"}
REQUIRED_FIELDS = [
    "run_status",
    "evaluable_signal_count",
    "evaluated_outcome_count",
    "skipped_count",
    "skip_reasons",
    "manifest_contract_version",
]


def validate_manifest(path: Path) -> dict:
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

    for field in ["evaluable_signal_count", "evaluated_outcome_count", "skipped_count"]:
        value = manifest.get(field)
        if not isinstance(value, int) or value < 0:
            raise ValueError(f"{field} must be a non-negative integer")

    if not isinstance(manifest.get("skip_reasons"), list):
        raise ValueError("skip_reasons must be a list")

    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate P165 outcome run manifest contract.")
    parser.add_argument("--manifest", type=Path, default=Path("reports/outcomes/outcome-run-manifest.json"))
    args = parser.parse_args()

    manifest = validate_manifest(args.manifest)
    print(f"outcome run_status={manifest['run_status']}")
    print(f"evaluable_signal_count={manifest['evaluable_signal_count']}")
    print(f"evaluated_outcome_count={manifest['evaluated_outcome_count']}")
    print(f"skipped_count={manifest['skipped_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
