from __future__ import annotations

import json
from pathlib import Path

from scripts.generate_module_inventory import build_inventory
from scripts.promote_arch106_runtime_delete_candidates import RUNTIME_DELETE_CANDIDATES, promote_candidates


def _write_base_classification(path: Path, *, baseline_limit: int = 1) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "allowed_classifications": [
                    "connected_runtime",
                    "test_only",
                    "experimental",
                    "quarantine",
                    "delete_candidate",
                ],
                "classified_modules": {},
                "grandfather_existing_modules": True,
                "unclassified_legacy_baseline_limit": baseline_limit,
                "policy": "test fixture",
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def test_arch106_runtime_delete_candidate_promotion_does_not_delete_module(tmp_path: Path) -> None:
    repo = tmp_path
    for candidate in RUNTIME_DELETE_CANDIDATES:
        module_path = repo / candidate
        module_path.parent.mkdir(parents=True, exist_ok=True)
        module_path.write_text("VALUE = 1\n", encoding="utf-8")

    classification_path = repo / "docs" / "architecture" / "module_classification.json"
    _write_base_classification(classification_path)

    classification = promote_candidates(classification_path)
    assert classification["classified_modules"] == RUNTIME_DELETE_CANDIDATES

    inventory = build_inventory(repo_root=repo, classification_path=classification_path)
    assert inventory["counters"]["classified_modules"] == 1
    assert inventory["counters"]["delete_candidate"] == 1
    assert inventory["counters"]["unclassified_legacy_modules"] == 0

    records = {record["path"]: record for record in inventory["modules"]}
    for candidate in RUNTIME_DELETE_CANDIDATES:
        assert (repo / candidate).exists(), "delete_candidate classification must not delete files"
        record = records[candidate]
        assert record["status"] == "classified"
        assert record["classification"] == "delete_candidate"
        assert record["runtime_entrypoint"] is None
        assert record["runtime_execution_proof"] is None
        assert "separate CI-proven removal PR" in record["notes"]
