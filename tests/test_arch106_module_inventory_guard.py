from __future__ import annotations

import json
from pathlib import Path

from scripts.generate_module_inventory import check_inventory, write_inventory


def _write_classification(path: Path, *, baseline_limit: int, classified_modules: dict | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": 1,
        "policy": "test policy",
        "allowed_classifications": [
            "connected_runtime",
            "runtime_entrypoint",
            "test_only",
            "experimental",
            "quarantine",
            "delete_candidate",
        ],
        "grandfather_existing_modules": True,
        "unclassified_legacy_baseline_limit": baseline_limit,
        "classified_modules": classified_modules or {},
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def test_arch106_inventory_check_blocks_growth_of_unclassified_legacy_modules(tmp_path: Path) -> None:
    repo = tmp_path
    src = repo / "src"
    src.mkdir()
    (src / "legacy_one.py").write_text("VALUE = 1\n", encoding="utf-8")
    (src / "new_unclassified_module.py").write_text("VALUE = 2\n", encoding="utf-8")

    classification_path = repo / "docs" / "architecture" / "module_classification.json"
    output_path = repo / "docs" / "architecture" / "module_inventory.generated.json"
    _write_classification(classification_path, baseline_limit=1)

    write_inventory(output_path=output_path)

    is_current, message = check_inventory(
        output_path,
        repo_root=repo,
        classification_path=classification_path,
    )

    assert is_current is False
    assert "ARCH106 unclassified legacy baseline exceeded" in message
    assert "Current unclassified legacy modules: 2" in message
    assert "Allowed baseline: 1" in message
    assert "must be explicitly classified" in message


def test_arch106_inventory_check_allows_new_module_when_explicitly_classified(tmp_path: Path) -> None:
    repo = tmp_path
    src = repo / "src"
    src.mkdir()
    (src / "legacy_one.py").write_text("VALUE = 1\n", encoding="utf-8")
    (src / "classified_experimental.py").write_text("VALUE = 2\n", encoding="utf-8")

    classification_path = repo / "docs" / "architecture" / "module_classification.json"
    output_path = repo / "docs" / "architecture" / "module_inventory.generated.json"
    _write_classification(
        classification_path,
        baseline_limit=1,
        classified_modules={
            "src/classified_experimental.py": {
                "classification": "experimental",
                "notes": "Explicitly classified test module.",
            }
        },
    )

    write_inventory(output_path=output_path)

    is_current, message = check_inventory(
        output_path,
        repo_root=repo,
        classification_path=classification_path,
    )

    assert is_current is True
    assert message == "ARCH106 module inventory artifact is current.\n"
