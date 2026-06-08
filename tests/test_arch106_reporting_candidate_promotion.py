from __future__ import annotations

import json
from pathlib import Path

from scripts.generate_module_inventory import build_inventory
from scripts.promote_arch106_reporting_runtime_candidates import (
    REPORTING_RUNTIME_CANDIDATES,
    promote_candidates,
)


def _write_base_classification(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
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
                "unclassified_legacy_baseline_limit": 2,
                "classified_modules": {},
            },
            indent=2,
        ),
        encoding="utf-8",
    )


def test_arch106_reporting_candidate_promotion_updates_classification_and_inventory(tmp_path: Path) -> None:
    repo = tmp_path
    src_reporting = repo / "src" / "reporting"
    src_reporting.mkdir(parents=True)
    (src_reporting / "cross_asset_report.py").write_text("VALUE = 1\n", encoding="utf-8")
    (src_reporting / "report_formatter.py").write_text("VALUE = 2\n", encoding="utf-8")

    classification_path = repo / "docs" / "architecture" / "module_classification.json"
    _write_base_classification(classification_path)

    classification = promote_candidates(classification_path)
    classified_modules = classification["classified_modules"]

    for module_path, expected_record in REPORTING_RUNTIME_CANDIDATES.items():
        assert classified_modules[module_path] == expected_record

    inventory = build_inventory(repo_root=repo, classification_path=classification_path)
    records = {record["path"]: record for record in inventory["modules"]}

    assert inventory["counters"]["classified_modules"] == 2
    assert inventory["counters"]["connected_runtime"] == 2
    assert inventory["counters"]["unclassified_legacy_modules"] == 0

    for module_path in REPORTING_RUNTIME_CANDIDATES:
        assert records[module_path]["status"] == "classified"
        assert records[module_path]["classification"] == "connected_runtime"
        assert records[module_path]["runtime_entrypoint"] == "scripts/generate_report.py"
        assert records[module_path]["runtime_execution_proof"]
