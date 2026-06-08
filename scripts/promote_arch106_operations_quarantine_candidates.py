#!/usr/bin/env python3
"""Promote ARCH106 operations quarantine candidates.

These modules contain audit/evidence or operational guard logic. They should not
be deleted, but they also must not be treated as connected runtime until an
explicit runtime execution proof exists.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.generate_module_inventory import DEFAULT_CLASSIFICATION_PATH, DEFAULT_OUTPUT_PATH, write_inventory


OPERATIONS_QUARANTINE_CANDIDATES: dict[str, dict[str, str | None]] = {
    "src/operations/runtime_evidence_manifest.py": {
        "classification": "quarantine",
        "runtime_entrypoint": None,
        "runtime_execution_proof": None,
        "notes": "ARCH106 strict triage: audit/evidence manifest logic is valuable and fail-safe oriented, but has no current proven runtime execution path. Keep isolated until an operations runtime proof exists.",
    },
    "src/operations/runtime_evidence_manifest_guard.py": {
        "classification": "quarantine",
        "runtime_entrypoint": None,
        "runtime_execution_proof": None,
        "notes": "ARCH106 strict triage: manifest guard is fail-closed operational safety logic, but has no current proven runtime execution path. Keep isolated until an operations runtime proof exists.",
    },
}


def promote_candidates(classification_path: Path = DEFAULT_CLASSIFICATION_PATH) -> dict[str, Any]:
    classification = json.loads(classification_path.read_text(encoding="utf-8"))
    allowed = set(classification.get("allowed_classifications", []))
    classified_modules = classification.setdefault("classified_modules", {})

    for module_path, record in OPERATIONS_QUARANTINE_CANDIDATES.items():
        module_classification = str(record["classification"])
        if module_classification not in allowed:
            raise ValueError(f"Invalid ARCH106 candidate classification: {module_classification}")
        classified_modules[module_path] = dict(record)

    classification_path.write_text(json.dumps(classification, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return classification


def main() -> int:
    promote_candidates(DEFAULT_CLASSIFICATION_PATH)
    write_inventory(DEFAULT_OUTPUT_PATH)
    print("Promoted ARCH106 operations quarantine candidates and regenerated module inventory.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
