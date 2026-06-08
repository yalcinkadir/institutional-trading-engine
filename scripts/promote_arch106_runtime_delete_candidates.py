#!/usr/bin/env python3
"""Promote first ARCH106 runtime delete candidates without deleting them.

A delete_candidate classification is not deletion approval. It only records that
a module appears unreferenced/replaceable and should be removed in a separate PR
after CI proves no breakage.
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


RUNTIME_DELETE_CANDIDATES: dict[str, dict[str, str | None]] = {
    "src/runtime/distributed_tasks.py": {
        "classification": "delete_candidate",
        "runtime_entrypoint": None,
        "runtime_execution_proof": None,
        "notes": "ARCH106 strict triage: generic in-memory distributed task stub has no current code-search references and no proven runtime path. Candidate only; deletion requires a separate CI-proven removal PR.",
    }
}


def promote_candidates(classification_path: Path = DEFAULT_CLASSIFICATION_PATH) -> dict[str, Any]:
    classification = json.loads(classification_path.read_text(encoding="utf-8"))
    allowed = set(classification.get("allowed_classifications", []))
    classified_modules = classification.setdefault("classified_modules", {})

    for module_path, record in RUNTIME_DELETE_CANDIDATES.items():
        module_classification = str(record["classification"])
        if module_classification not in allowed:
            raise ValueError(f"Invalid ARCH106 candidate classification: {module_classification}")
        classified_modules[module_path] = dict(record)

    classification_path.write_text(json.dumps(classification, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return classification


def main() -> int:
    promote_candidates(DEFAULT_CLASSIFICATION_PATH)
    write_inventory(DEFAULT_OUTPUT_PATH)
    print("Promoted ARCH106 runtime delete candidates and regenerated module inventory.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
