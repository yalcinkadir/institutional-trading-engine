#!/usr/bin/env python3
"""Promote CI-proven ARCH106 reporting runtime candidates consistently.

This helper updates `module_classification.json` and regenerates
`module_inventory.generated.json` in one deterministic operation. It is intended
for the ARCH106 follow-up step after runtime reachability and execution proof
have been reviewed.
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


RUNTIME_ENTRYPOINT = "scripts/generate_report.py"
RUNTIME_PROOF = "tests/test_architecture_runtime_execution_guard.py::test_arch106_report_signal_path_has_runtime_execution_proof"

REPORTING_RUNTIME_CANDIDATES: dict[str, dict[str, str]] = {
    "src/reporting/cross_asset_report.py": {
        "classification": "connected_runtime",
        "runtime_entrypoint": RUNTIME_ENTRYPOINT,
        "runtime_execution_proof": RUNTIME_PROOF,
        "notes": "Cross-asset report payload is exercised by the report/signal runtime path in ARCH106.",
    },
    "src/reporting/report_formatter.py": {
        "classification": "connected_runtime",
        "runtime_entrypoint": RUNTIME_ENTRYPOINT,
        "runtime_execution_proof": RUNTIME_PROOF,
        "notes": "Report formatter receives and renders the market report payload on the ARCH106 runtime path.",
    },
}


def promote_candidates(classification_path: Path = DEFAULT_CLASSIFICATION_PATH) -> dict[str, Any]:
    classification = json.loads(classification_path.read_text(encoding="utf-8"))
    allowed = set(classification.get("allowed_classifications", []))
    classified_modules = classification.setdefault("classified_modules", {})

    for module_path, record in REPORTING_RUNTIME_CANDIDATES.items():
        module_classification = record["classification"]
        if module_classification not in allowed:
            raise ValueError(f"Invalid ARCH106 candidate classification: {module_classification}")
        classified_modules[module_path] = dict(record)

    classification_path.write_text(json.dumps(classification, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return classification


def main() -> int:
    promote_candidates(DEFAULT_CLASSIFICATION_PATH)
    write_inventory(DEFAULT_OUTPUT_PATH)
    print("Promoted ARCH106 reporting runtime candidates and regenerated module inventory.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
