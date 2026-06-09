from __future__ import annotations

import json
from pathlib import Path

from src.operations.outcome_run_status_link import build_outcome_run_status_link


def test_p165_outcome_status_link_reads_manifest_counts(tmp_path: Path) -> None:
    manifest = tmp_path / "outcome-run-manifest.json"
    manifest.write_text(
        json.dumps(
            {
                "run_status": "OK",
                "evaluable_signal_count": 2,
                "evaluated_outcome_count": 1,
                "skipped_count": 1,
                "skip_reasons": ["pending"],
            }
        ),
        encoding="utf-8",
    )

    link = build_outcome_run_status_link(manifest)

    assert link["outcome_manifest_available"] is True
    assert link["outcome_run_status"] == "OK"
    assert link["evaluable_signal_count"] == 2
    assert link["evaluated_outcome_count"] == 1
    assert link["skipped_count"] == 1
    assert link["skip_reasons"] == ["pending"]


def test_p165_outcome_status_link_blocks_missing_manifest(tmp_path: Path) -> None:
    link = build_outcome_run_status_link(tmp_path / "missing.json")

    assert link["outcome_manifest_available"] is False
    assert link["outcome_run_status"] == "BLOCKED_MISSING_OUTCOME_MANIFEST"
