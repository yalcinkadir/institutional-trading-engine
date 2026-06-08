from __future__ import annotations

import copy

from scripts.generate_module_inventory import build_inventory, load_classification
from scripts.validate_arch106_ratchet import (
    CRITICAL_RUNTIME_MODULES,
    validate_ratchet,
)


def _inventory_and_classification():
    classification = load_classification()
    inventory = build_inventory()
    return inventory, classification


def test_arch106_current_inventory_satisfies_ratchet() -> None:
    inventory, classification = _inventory_and_classification()

    result = validate_ratchet(inventory, classification)

    assert result.ok, result.as_text()


def test_arch106_ratchet_blocks_baseline_growth() -> None:
    inventory, classification = _inventory_and_classification()
    classification = copy.deepcopy(classification)
    classification["unclassified_legacy_baseline_limit"] = 0

    result = validate_ratchet(inventory, classification)

    assert not result.ok
    assert "unclassified legacy baseline grew" in result.as_text()


def test_arch106_ratchet_blocks_connected_runtime_without_execution_proof() -> None:
    inventory, classification = _inventory_and_classification()
    inventory = copy.deepcopy(inventory)

    first_connected = next(
        record for record in inventory["modules"] if record["classification"] == "connected_runtime"
    )
    first_connected["runtime_execution_proof"] = None

    result = validate_ratchet(inventory, classification)

    assert not result.ok
    assert "production classification missing runtime_execution_proof" in result.as_text()


def test_arch106_ratchet_blocks_critical_runtime_demotion() -> None:
    inventory, classification = _inventory_and_classification()
    inventory = copy.deepcopy(inventory)
    critical_path = sorted(CRITICAL_RUNTIME_MODULES)[0]

    for record in inventory["modules"]:
        if record["path"] == critical_path:
            record["classification"] = "experimental"
            record["runtime_entrypoint"] = None
            record["runtime_execution_proof"] = None
            break
    else:  # pragma: no cover - defensive assertion for stale test setup
        raise AssertionError(f"critical path not present in inventory: {critical_path}")

    result = validate_ratchet(inventory, classification)

    assert not result.ok
    assert "critical runtime module must be connected_runtime" in result.as_text()


def test_arch106_critical_runtime_modules_have_entrypoint_and_proof() -> None:
    inventory, _classification = _inventory_and_classification()
    records = {record["path"]: record for record in inventory["modules"]}

    for path in sorted(CRITICAL_RUNTIME_MODULES):
        record = records[path]
        assert record["classification"] == "connected_runtime"
        assert record["runtime_entrypoint"]
        assert record["runtime_execution_proof"]
