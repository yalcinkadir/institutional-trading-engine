#!/usr/bin/env python3
"""Promote first ARCH106 runtime quarantine candidates.

Quarantine means the module may contain useful governance/runtime logic, but it
must not be treated as connected runtime until a dedicated runtime proof exists.
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


RUNTIME_QUARANTINE_CANDIDATES: dict[str, dict[str, str | None]] = {
    "src/runtime/governance_approval_gate.py": {
        "classification": "quarantine",
        "runtime_entrypoint": None,
        "runtime_execution_proof": None,
        "notes": "ARCH106 strict triage: governance-sensitive approval logic appears valuable but has no current proven runtime execution path. Keep isolated until a dedicated runtime proof promotes it.",
    },
    "src/runtime/runtime_proof_pack_summary.py": {
        "classification": "quarantine",
        "runtime_entrypoint": None,
        "runtime_execution_proof": None,
        "notes": "ARCH106 strict triage: runtime proof-pack summarization is governance-sensitive evidence logic without current runtime proof. Keep isolated until reviewed and proven.",
    },
}


def promote_candidates(classification_path: Path = DEFAULT_CLASSIFICATION_PATH) -> dict[str, Any]:
    classification = json.loads(classification_path.read_text(encoding="utf-8"))
    allowed = set(classification.get("allowed_classifications", []))
    classified_modules = classification.setdefault("classified_modules", {})

    for module_path, record in RUNTIME_QUARANTINE_CANDIDATES.items():
        module_classification = str(record["classification"])
        if module_classification not in allowed:
            raise ValueError(f"Invalid ARCH106 candidate classification: {module_classification}")
        classified_modules[module_path] = dict(record)

    classification_path.write_text(json.dumps(classification, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return classification


def main() -> int:
    promote_candidates(DEFAULT_CLASSIFICATION_PATH)
    write_inventory(DEFAULT_OUTPUT_PATH)
    print("Promoted ARCH106 runtime quarantine candidates and regenerated module inventory.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
