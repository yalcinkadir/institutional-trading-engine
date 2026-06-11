from __future__ import annotations

import json
from pathlib import Path

from scripts.augment_outcome_manifest_p165 import augment_manifest


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_p165_augmenter_adds_required_manifest_counts(tmp_path: Path) -> None:
    outcomes_dir = tmp_path / "outcomes"
    _write_json(
        outcomes_dir / "outcome-run-manifest.json",
        {
            "run_status": "SUCCESS",
            "artifact_date": "2026-06-01",
            "total_input_signals": 0,
            "skip_reasons": [],
        },
    )
    _write_json(
        outcomes_dir / "2026-06-01-outcomes.json",
        [
            {"symbol": "AAPL", "lifecycle_status": "TRIGGERED", "classification": "WIN"},
            {"symbol": "MSFT", "lifecycle_status": "PENDING", "classification": "PENDING"},
        ],
    )

    manifest = augment_manifest(outcomes_dir)

    assert manifest["manifest_contract_version"] == "p165.v2_186"
    assert manifest["run_status"] == "SUCCESS"
    assert manifest["total_input_signals"] == 2
    assert manifest["evaluable_signal_count"] == 1
    assert manifest["evaluated_outcome_count"] == 1
    assert manifest["skipped_count"] == 1
    assert manifest["skip_reasons"] == ["pending"]
    assert manifest["broker_execution_mode"] == "paper_only"
    assert (outcomes_dir / "2026-06-01-outcome-run.json").exists()


def test_p165_augmenter_preserves_blocked_status_as_zero_counts(tmp_path: Path) -> None:
    outcomes_dir = tmp_path / "outcomes"
    _write_json(
        outcomes_dir / "outcome-run-manifest.json",
        {
            "run_status": "BLOCKED_MISSING_INPUTS",
            "artifact_date": "2026-06-02",
            "skip_reasons": ["signals_directory_missing"],
        },
    )

    manifest = augment_manifest(outcomes_dir)

    assert manifest["manifest_contract_version"] == "p165.v2_186"
    assert manifest["run_status"] == "BLOCKED_MISSING_INPUTS"
    assert manifest["evaluable_signal_count"] == 0
    assert manifest["evaluated_outcome_count"] == 0
    assert manifest["skipped_count"] == 0
    assert manifest["skip_reasons"] == ["signals_directory_missing"]
    assert (outcomes_dir / "2026-06-02-outcome-run.json").exists()
