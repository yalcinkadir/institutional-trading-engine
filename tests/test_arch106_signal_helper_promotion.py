from __future__ import annotations

import json
from pathlib import Path

from scripts.generate_module_inventory import build_inventory
from scripts.promote_arch106_signal_helpers import SIGNAL_HELPER_RUNTIME_CANDIDATES, promote_candidates


def _write_base_classification(path: Path, *, baseline_limit: int = 5) -> None:
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


def test_arch106_signal_helper_promotion_updates_classification_and_inventory(tmp_path: Path) -> None:
    repo = tmp_path
    signals_dir = repo / "src" / "signals"
    signals_dir.mkdir(parents=True)
    for candidate in SIGNAL_HELPER_RUNTIME_CANDIDATES:
        module_path = repo / candidate
        module_path.parent.mkdir(parents=True, exist_ok=True)
        module_path.write_text("VALUE = 1\n", encoding="utf-8")

    classification_path = repo / "docs" / "architecture" / "module_classification.json"
    _write_base_classification(classification_path)

    classification = promote_candidates(classification_path)
    assert classification["classified_modules"] == SIGNAL_HELPER_RUNTIME_CANDIDATES

    inventory = build_inventory(repo_root=repo, classification_path=classification_path)
    assert inventory["counters"]["classified_modules"] == 5
    assert inventory["counters"]["connected_runtime"] == 5
    assert inventory["counters"]["unclassified_legacy_modules"] == 0

    records = {record["path"]: record for record in inventory["modules"]}
    for candidate, expected in SIGNAL_HELPER_RUNTIME_CANDIDATES.items():
        record = records[candidate]
        assert record["status"] == "classified"
        assert record["classification"] == "connected_runtime"
        assert record["runtime_entrypoint"] == expected["runtime_entrypoint"]
        assert record["runtime_execution_proof"] == expected["runtime_execution_proof"]
