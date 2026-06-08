#!/usr/bin/env python3
"""Promote ARCH106 memory helper modules as experimental.

These modules contain small analysis helpers that may be useful later, but they
have no current runtime execution proof and must not be treated as connected
runtime.
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


MEMORY_EXPERIMENTAL_CANDIDATES: dict[str, dict[str, str | None]] = {
    "src/memory/anomaly_memory.py": {
        "classification": "experimental",
        "runtime_entrypoint": None,
        "runtime_execution_proof": None,
        "notes": "ARCH106 strict triage: memory helper for anomaly summaries has no current runtime proof; keep as experimental analysis support.",
    },
    "src/memory/pattern_memory.py": {
        "classification": "experimental",
        "runtime_entrypoint": None,
        "runtime_execution_proof": None,
        "notes": "ARCH106 strict triage: memory helper for repeating pattern summaries has no current runtime proof; keep as experimental analysis support.",
    },
    "src/memory/regime_memory.py": {
        "classification": "experimental",
        "runtime_entrypoint": None,
        "runtime_execution_proof": None,
        "notes": "ARCH106 strict triage: memory helper for historical regime comparison has no current runtime proof; keep as experimental analysis support.",
    },
    "src/memory/trade_memory.py": {
        "classification": "experimental",
        "runtime_entrypoint": None,
        "runtime_execution_proof": None,
        "notes": "ARCH106 strict triage: memory helper for setup statistics has no current runtime proof; keep as experimental analysis support.",
    },
}


def promote_candidates(classification_path: Path = DEFAULT_CLASSIFICATION_PATH) -> dict[str, Any]:
    classification = json.loads(classification_path.read_text(encoding="utf-8"))
    allowed = set(classification.get("allowed_classifications", []))
    classified_modules = classification.setdefault("classified_modules", {})

    for module_path, record in MEMORY_EXPERIMENTAL_CANDIDATES.items():
        module_classification = str(record["classification"])
        if module_classification not in allowed:
            raise ValueError(f"Invalid ARCH106 candidate classification: {module_classification}")
        classified_modules[module_path] = dict(record)

    classification_path.write_text(json.dumps(classification, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return classification


def main() -> int:
    promote_candidates(DEFAULT_CLASSIFICATION_PATH)
    write_inventory(DEFAULT_OUTPUT_PATH)
    print("Promoted ARCH106 memory experimental candidates and regenerated module inventory.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
