#!/usr/bin/env python3
"""ARCH106 inventory ratchet guard.

This guard is intentionally stricter than a stale-inventory check and narrower
than a full legacy cleanup. It enforces the architectural ratchet required by
#106:

* the committed module inventory must match the current checkout;
* the grandfathered unclassified-legacy baseline may not grow;
* production-connected modules must have runtime entrypoint and execution proof;
* known critical runtime modules must be classified as connected runtime;
* classification states must stay within the approved vocabulary.

Existing legacy modules are allowed only as a bounded baseline. New production
architecture debt must fail closed.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from scripts.generate_module_inventory import (
    DEFAULT_CLASSIFICATION_PATH,
    DEFAULT_OUTPUT_PATH,
    REPO_ROOT,
    check_inventory,
    load_classification,
)

PRODUCTION_CLASSIFICATIONS = {"connected_runtime", "runtime_entrypoint"}
NON_PRODUCTION_CLASSIFICATIONS = {"test_only", "experimental", "quarantine", "delete_candidate"}
REQUIRED_ALLOWED_CLASSIFICATIONS = PRODUCTION_CLASSIFICATIONS | NON_PRODUCTION_CLASSIFICATIONS

# These are the currently proven report/signal runtime modules. They are the
# core executable path covered by tests/test_architecture_runtime_execution_guard.py
# and related ARCH106 signal-runtime tests. Adding a new critical runtime module
# should update this list and the classification proof together.
CRITICAL_RUNTIME_MODULES = {
    "src/reporting/cross_asset_report.py",
    "src/reporting/decision_report.py",
    "src/reporting/market_regime.py",
    "src/reporting/report_formatter.py",
    "src/reporting/screener_engine.py",
    "src/signals/entry_quality.py",
    "src/signals/exit_target_quality.py",
    "src/signals/scanner_metrics_pipeline.py",
    "src/signals/signal_generator.py",
    "src/signals/signal_identity.py",
    "src/signals/stop_loss_quality.py",
    "src/signals/trade_plan_validator.py",
}


@dataclass(frozen=True)
class RatchetResult:
    ok: bool
    messages: tuple[str, ...]

    def as_text(self) -> str:
        if self.ok:
            return "ARCH106 ratchet guard passed.\n"
        return "ARCH106 ratchet guard failed:\n" + "".join(f"- {m}\n" for m in self.messages)


def _records_by_path(inventory: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {str(record.get("path")): record for record in inventory.get("modules", [])}


def _missing_runtime_evidence(record: dict[str, Any]) -> list[str]:
    missing: list[str] = []
    if not record.get("runtime_entrypoint"):
        missing.append("runtime_entrypoint")
    if not record.get("runtime_execution_proof"):
        missing.append("runtime_execution_proof")
    return missing


def _validate_allowed_classifications(classification: dict[str, Any]) -> list[str]:
    allowed = set(classification.get("allowed_classifications", []))
    missing = sorted(REQUIRED_ALLOWED_CLASSIFICATIONS - allowed)
    if missing:
        return [f"classification vocabulary is missing required states: {', '.join(missing)}"]
    return []


def _validate_baseline_limit(inventory: dict[str, Any], classification: dict[str, Any]) -> list[str]:
    baseline_limit = classification.get("unclassified_legacy_baseline_limit")
    if baseline_limit is None:
        return ["unclassified_legacy_baseline_limit is required for ARCH106 ratchet enforcement"]

    current = int(inventory.get("counters", {}).get("unclassified_legacy_modules", 0))
    limit = int(baseline_limit)
    if current > limit:
        return [
            "unclassified legacy baseline grew: "
            f"current={current}, allowed={limit}; classify new modules before merge"
        ]
    return []


def _validate_inventory_records(inventory: dict[str, Any], classification: dict[str, Any]) -> list[str]:
    messages: list[str] = []
    allowed = set(classification.get("allowed_classifications", [])) | {"unclassified_legacy"}

    for path, record in sorted(_records_by_path(inventory).items()):
        module_classification = record.get("classification")
        if module_classification not in allowed:
            messages.append(f"{path}: invalid classification {module_classification!r}")
            continue

        if module_classification in PRODUCTION_CLASSIFICATIONS:
            missing = _missing_runtime_evidence(record)
            if missing:
                messages.append(f"{path}: production classification missing {', '.join(missing)}")

        if module_classification in NON_PRODUCTION_CLASSIFICATIONS and record.get("status") != "classified":
            messages.append(f"{path}: non-production module must be explicitly classified")

    return messages


def _validate_critical_runtime_modules(inventory: dict[str, Any]) -> list[str]:
    messages: list[str] = []
    records = _records_by_path(inventory)

    for module_path in sorted(CRITICAL_RUNTIME_MODULES):
        record = records.get(module_path)
        if not record:
            messages.append(f"{module_path}: critical runtime module missing from inventory")
            continue
        if record.get("classification") != "connected_runtime":
            messages.append(
                f"{module_path}: critical runtime module must be connected_runtime, "
                f"got {record.get('classification')!r}"
            )
            continue
        missing = _missing_runtime_evidence(record)
        if missing:
            messages.append(f"{module_path}: critical runtime module missing {', '.join(missing)}")

    return messages


def validate_ratchet(inventory: dict[str, Any], classification: dict[str, Any]) -> RatchetResult:
    messages: list[str] = []
    messages.extend(_validate_allowed_classifications(classification))
    messages.extend(_validate_baseline_limit(inventory, classification))
    messages.extend(_validate_inventory_records(inventory, classification))
    messages.extend(_validate_critical_runtime_modules(inventory))
    return RatchetResult(ok=not messages, messages=tuple(messages))


def validate_current_checkout(
    *,
    inventory_path: Path = DEFAULT_OUTPUT_PATH,
    classification_path: Path = DEFAULT_CLASSIFICATION_PATH,
) -> RatchetResult:
    inventory_ok, inventory_message = check_inventory(inventory_path, classification_path=classification_path)
    if not inventory_ok:
        return RatchetResult(ok=False, messages=(inventory_message.strip(),))

    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    classification = load_classification(classification_path)
    return validate_ratchet(inventory, classification)


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate ARCH106 inventory ratchet constraints.")
    parser.add_argument(
        "--inventory",
        default=str(DEFAULT_OUTPUT_PATH),
        help="Committed module inventory artifact path.",
    )
    parser.add_argument(
        "--classification",
        default=str(DEFAULT_CLASSIFICATION_PATH),
        help="Module classification policy path.",
    )
    return parser.parse_args(argv)


def _resolve_repo_path(path: str) -> Path:
    resolved = Path(path)
    if resolved.is_absolute():
        return resolved
    return REPO_ROOT / resolved


def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(argv)
    result = validate_current_checkout(
        inventory_path=_resolve_repo_path(args.inventory),
        classification_path=_resolve_repo_path(args.classification),
    )
    print(result.as_text(), end="")
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
