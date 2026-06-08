#!/usr/bin/env python3
"""Promote CI-proven ARCH106 signal helper modules consistently.

This helper updates `module_classification.json` and regenerates
`module_inventory.generated.json` in one deterministic operation. It is intended
for the ARCH106 follow-up step after the signal helper runtime proof is green.
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


RUNTIME_ENTRYPOINT = "src/signals/signal_generator.py"
RUNTIME_PROOF = "tests/test_arch106_signal_runtime_helper_proof.py::test_arch106_signal_runtime_helpers_execute_on_buy_watch_path"

SIGNAL_HELPER_RUNTIME_CANDIDATES: dict[str, dict[str, str]] = {
    "src/signals/entry_quality.py": {
        "classification": "connected_runtime",
        "runtime_entrypoint": RUNTIME_ENTRYPOINT,
        "runtime_execution_proof": RUNTIME_PROOF,
        "notes": "Entry trigger quality is executed by build_signals on the ARCH106 BUY_WATCH signal runtime path.",
    },
    "src/signals/exit_target_quality.py": {
        "classification": "connected_runtime",
        "runtime_entrypoint": RUNTIME_ENTRYPOINT,
        "runtime_execution_proof": RUNTIME_PROOF,
        "notes": "Exit target quality is executed by build_signals on the ARCH106 BUY_WATCH signal runtime path.",
    },
    "src/signals/signal_identity.py": {
        "classification": "connected_runtime",
        "runtime_entrypoint": RUNTIME_ENTRYPOINT,
        "runtime_execution_proof": RUNTIME_PROOF,
        "notes": "Deterministic signal identity generation is executed by build_signals on the ARCH106 BUY_WATCH signal runtime path.",
    },
    "src/signals/stop_loss_quality.py": {
        "classification": "connected_runtime",
        "runtime_entrypoint": RUNTIME_ENTRYPOINT,
        "runtime_execution_proof": RUNTIME_PROOF,
        "notes": "Stop-loss quality is executed by build_signals on the ARCH106 BUY_WATCH signal runtime path.",
    },
    "src/signals/trade_plan_validator.py": {
        "classification": "connected_runtime",
        "runtime_entrypoint": RUNTIME_ENTRYPOINT,
        "runtime_execution_proof": RUNTIME_PROOF,
        "notes": "Trade-plan validation is executed by build_signals as the final executable signal gate on the ARCH106 BUY_WATCH runtime path.",
    },
}


def promote_candidates(classification_path: Path = DEFAULT_CLASSIFICATION_PATH) -> dict[str, Any]:
    classification = json.loads(classification_path.read_text(encoding="utf-8"))
    allowed = set(classification.get("allowed_classifications", []))
    classified_modules = classification.setdefault("classified_modules", {})

    for module_path, record in SIGNAL_HELPER_RUNTIME_CANDIDATES.items():
        module_classification = record["classification"]
        if module_classification not in allowed:
            raise ValueError(f"Invalid ARCH106 candidate classification: {module_classification}")
        classified_modules[module_path] = dict(record)

    classification_path.write_text(json.dumps(classification, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return classification


def main() -> int:
    promote_candidates(DEFAULT_CLASSIFICATION_PATH)
    write_inventory(DEFAULT_OUTPUT_PATH)
    print("Promoted ARCH106 signal helper runtime candidates and regenerated module inventory.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
