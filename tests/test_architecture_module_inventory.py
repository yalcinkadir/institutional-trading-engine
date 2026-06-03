from __future__ import annotations

import json
from pathlib import Path

from scripts.generate_module_inventory import build_inventory, discover_src_modules


INVENTORY_ARTIFACT_PATH = Path("docs/architecture/module_inventory.generated.json")

ALLOWED_INVENTORY_CLASSIFICATIONS = {
    "connected_runtime",
    "runtime_entrypoint",
    "test_only",
    "experimental",
    "quarantine",
    "delete_candidate",
    "unclassified_legacy",
}


def test_arch106_inventory_discovers_current_src_modules() -> None:
    modules = discover_src_modules()

    assert modules
    assert modules == sorted(modules)
    assert all(module.startswith("src/") for module in modules)
    assert all(module.endswith(".py") for module in modules)
    assert "src/signals/signal_generator.py" in modules
    assert "src/signals/scanner_metrics_pipeline.py" in modules
    assert "src/reporting/decision_report.py" in modules


def test_arch106_inventory_covers_every_current_src_module() -> None:
    inventory = build_inventory()
    discovered_modules = set(discover_src_modules())
    inventoried_modules = {record["path"] for record in inventory["modules"]}

    assert inventory["schema_version"] == 1
    assert inventory["source"] == "scripts/generate_module_inventory.py"
    assert inventory["classification_source"] == "docs/architecture/module_classification.json"
    assert inventory["grandfather_existing_modules"] is True
    assert inventoried_modules == discovered_modules
    assert inventory["counters"]["total_src_modules"] == len(discovered_modules)


def test_arch106_inventory_records_classified_and_legacy_module_status() -> None:
    inventory = build_inventory()
    records = {record["path"]: record for record in inventory["modules"]}

    for record in inventory["modules"]:
        assert record["classification"] in ALLOWED_INVENTORY_CLASSIFICATIONS
        assert record["status"] in {"classified", "unclassified_legacy"}
        if record["classification"] in {"connected_runtime", "runtime_entrypoint"}:
            assert record["runtime_entrypoint"], record["path"]
            assert record["runtime_execution_proof"], record["path"]
        if record["status"] == "unclassified_legacy":
            assert record["classification"] == "unclassified_legacy"
            assert record["runtime_entrypoint"] is None
            assert record["runtime_execution_proof"] is None

    assert records["src/signals/signal_generator.py"]["status"] == "classified"
    assert records["src/signals/signal_generator.py"]["classification"] == "connected_runtime"

    assert inventory["counters"]["classified_modules"] >= 5
    assert inventory["counters"]["unclassified_legacy_modules"] >= 0
    assert (
        inventory["counters"]["classified_modules"]
        + inventory["counters"]["unclassified_legacy_modules"]
        == inventory["counters"]["total_src_modules"]
    )


def test_arch106_committed_inventory_artifact_exists_and_has_schema() -> None:
    assert INVENTORY_ARTIFACT_PATH.exists(), (
        "ARCH106 requires a committed inventory artifact at "
        "docs/architecture/module_inventory.generated.json"
    )

    artifact = json.loads(INVENTORY_ARTIFACT_PATH.read_text(encoding="utf-8"))
    assert artifact["schema_version"] == 1
    assert artifact["source"] == "scripts/generate_module_inventory.py"
    assert artifact["classification_source"] == "docs/architecture/module_classification.json"
    assert artifact["grandfather_existing_modules"] is True
    assert isinstance(artifact["counters"], dict)
    assert isinstance(artifact["modules"], list)


def test_arch106_committed_inventory_artifact_matches_generator_output() -> None:
    expected = build_inventory()
    actual = json.loads(INVENTORY_ARTIFACT_PATH.read_text(encoding="utf-8"))

    assert actual == expected, (
        "ARCH106 inventory artifact is stale. Regenerate it with: "
        "python scripts/generate_module_inventory.py && "
        "git add docs/architecture/module_inventory.generated.json"
    )


def test_arch106_inventory_can_be_written_without_missing_paths(tmp_path) -> None:
    output_path = tmp_path / "module_inventory.generated.json"
    inventory = build_inventory()
    output_path.write_text(json.dumps(inventory, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    assert output_path.exists()
    assert Path(inventory["classification_source"]).as_posix() == "docs/architecture/module_classification.json"
