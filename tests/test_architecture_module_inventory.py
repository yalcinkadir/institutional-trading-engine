from __future__ import annotations

import json
from pathlib import Path

from scripts.generate_module_inventory import (
    build_inventory,
    check_inventory,
    discover_src_modules,
    format_inventory_diff,
    inventory_diff,
    render_inventory,
)


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
    is_current, message = check_inventory(INVENTORY_ARTIFACT_PATH)

    assert is_current, message


def test_arch106_inventory_diff_reports_added_removed_and_changed_modules() -> None:
    expected = {
        "counters": {"total_src_modules": 2, "classified_modules": 1},
        "modules": [
            {
                "path": "src/a.py",
                "classification": "connected_runtime",
                "status": "classified",
                "runtime_entrypoint": "scripts/a.py",
                "runtime_execution_proof": "tests/test_a.py",
            },
            {
                "path": "src/b.py",
                "classification": "unclassified_legacy",
                "status": "unclassified_legacy",
                "runtime_entrypoint": None,
                "runtime_execution_proof": None,
            },
        ],
    }
    actual = {
        "counters": {"total_src_modules": 2, "classified_modules": 2},
        "modules": [
            {
                "path": "src/a.py",
                "classification": "experimental",
                "status": "classified",
                "runtime_entrypoint": None,
                "runtime_execution_proof": None,
            },
            {
                "path": "src/c.py",
                "classification": "unclassified_legacy",
                "status": "unclassified_legacy",
                "runtime_entrypoint": None,
                "runtime_execution_proof": None,
            },
        ],
    }

    diff = inventory_diff(expected, actual)
    rendered = format_inventory_diff(diff)

    assert diff["added_modules"] == ["src/b.py"]
    assert diff["removed_modules"] == ["src/c.py"]
    assert diff["changed_modules"] == [
        {
            "path": "src/a.py",
            "changes": {
                "classification": {"expected": "connected_runtime", "actual": "experimental"},
                "runtime_entrypoint": {"expected": "scripts/a.py", "actual": None},
                "runtime_execution_proof": {"expected": "tests/test_a.py", "actual": None},
            },
        }
    ]
    assert "Added src modules missing from committed inventory" in rendered
    assert "Removed src modules still present in committed inventory" in rendered
    assert "Changed module classifications/status" in rendered
    assert "python scripts/generate_module_inventory.py" in rendered


def test_arch106_inventory_check_reports_stale_artifact(tmp_path) -> None:
    stale_path = tmp_path / "module_inventory.generated.json"
    stale_path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "source": "scripts/generate_module_inventory.py",
                "classification_source": "docs/architecture/module_classification.json",
                "grandfather_existing_modules": True,
                "counters": {"total_src_modules": 0},
                "modules": [],
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    is_current, message = check_inventory(stale_path)

    assert is_current is False
    assert "ARCH106 module inventory artifact is stale" in message
    assert "Added src modules missing from committed inventory" in message


def test_arch106_inventory_can_be_written_without_missing_paths(tmp_path) -> None:
    output_path = tmp_path / "module_inventory.generated.json"
    inventory = build_inventory()
    output_path.write_text(render_inventory(inventory), encoding="utf-8")

    assert output_path.exists()
    assert Path(inventory["classification_source"]).as_posix() == "docs/architecture/module_classification.json"
