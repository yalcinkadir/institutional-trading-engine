#!/usr/bin/env python3
"""Promote ARCH106 reporting support modules conservatively.

These modules are useful reporting support/research helpers, but they are not
classified as connected_runtime until a runtime execution proof exists.
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


REPORTING_SUPPORT_CANDIDATES: dict[str, dict[str, str | None]] = {
    "src/reporting/report_quality.py": {
        "classification": "experimental",
        "runtime_entrypoint": None,
        "runtime_execution_proof": None,
        "notes": "Report quality validator is available as a reporting support helper but has no ARCH106 runtime execution proof yet.",
    },
    "src/reporting/tg2_tg3_report_templates.py": {
        "classification": "experimental",
        "runtime_entrypoint": None,
        "runtime_execution_proof": None,
        "notes": "TG2/TG3 Telegram report templates are reporting support helpers; promote to connected_runtime only after a delivery-path proof exists.",
    },
    "src/reporting/trade_summary.py": {
        "classification": "experimental",
        "runtime_entrypoint": None,
        "runtime_execution_proof": None,
        "notes": "Trade summary builder is a lightweight reporting support helper without ARCH106 runtime proof yet.",
    },
    "src/reporting/weekly_summary.py": {
        "classification": "experimental",
        "runtime_entrypoint": None,
        "runtime_execution_proof": None,
        "notes": "Weekly summary builder is a reporting support helper without ARCH106 runtime proof yet.",
    },
}


def promote_candidates(classification_path: Path = DEFAULT_CLASSIFICATION_PATH) -> dict[str, Any]:
    classification = json.loads(classification_path.read_text(encoding="utf-8"))
    allowed = set(classification.get("allowed_classifications", []))
    classified_modules = classification.setdefault("classified_modules", {})

    for module_path, record in REPORTING_SUPPORT_CANDIDATES.items():
        module_classification = str(record["classification"])
        if module_classification not in allowed:
            raise ValueError(f"Invalid ARCH106 candidate classification: {module_classification}")
        classified_modules[module_path] = dict(record)

    classification_path.write_text(json.dumps(classification, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return classification


def main() -> int:
    promote_candidates(DEFAULT_CLASSIFICATION_PATH)
    write_inventory(DEFAULT_OUTPUT_PATH)
    print("Promoted ARCH106 reporting support modules and regenerated module inventory.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
