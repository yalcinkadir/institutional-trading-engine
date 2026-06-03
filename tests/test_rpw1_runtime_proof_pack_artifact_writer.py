from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import json

from src.validation.runtime_proof_pack_artifact_writer import write_runtime_proof_pack_artifact


def _summary():
    return {
        "runtime_proof_pack_status": "REVIEW_READY",
        "proof_count": 3,
        "blocking_issue_count": 0,
        "live_trading_authorized": False,
        "broker_execution_mode": "paper_only",
    }


def test_rpw1_writes_runtime_proof_pack_artifact_and_retention_index(tmp_path: Path) -> None:
    result = write_runtime_proof_pack_artifact(
        output_dir=tmp_path,
        proof_pack_id="RGP13-2026-06-03",
        observation_window="2026-06-03",
        proof_pack_summary=_summary(),
        retention_days=730,
        created_at_utc="2026-06-03T10:00:00+00:00",
    )

    assert result.valid is True
    assert result.errors == ()
    assert result.summary["artifact_writer_status"] == "WRITTEN"
    assert result.summary["live_trading_authorized"] is False

    artifact = json.loads(Path(result.artifact_path).read_text(encoding="utf-8"))
    assert artifact["proof_pack_id"] == "RGP13-2026-06-03"
    assert artifact["proof_pack_summary"]["runtime_proof_pack_status"] == "REVIEW_READY"
    assert artifact["broker_execution_mode"] == "paper_only"

    index = json.loads(Path(result.retention_index_path).read_text(encoding="utf-8"))
    assert index["retention_index_status"] == "ACTIVE"
    assert index["artifact_count"] == 1
    assert index["artifacts"][0]["sha256"] == result.summary["artifact_sha256"]
    assert index["artifacts"][0]["retention_days"] == 730


def test_rpw1_updates_existing_retention_index_without_duplicate_ids(tmp_path: Path) -> None:
    kwargs = {
        "output_dir": tmp_path,
        "proof_pack_id": "RGP13-2026-06-03",
        "observation_window": "2026-06-03",
        "proof_pack_summary": _summary(),
        "created_at_utc": "2026-06-03T10:00:00+00:00",
    }

    first = write_runtime_proof_pack_artifact(**kwargs, retention_days=365)
    second = write_runtime_proof_pack_artifact(**kwargs, retention_days=730)

    assert first.valid is True
    assert second.valid is True
    index = json.loads(Path(second.retention_index_path).read_text(encoding="utf-8"))
    assert index["artifact_count"] == 1
    assert index["artifacts"][0]["retention_days"] == 730


def test_rpw1_blocks_missing_identity_or_summary() -> None:
    result = write_runtime_proof_pack_artifact(
        output_dir="reports",
        proof_pack_id="",
        observation_window="",
        proof_pack_summary={},
    )

    assert result.valid is False
    assert "missing_proof_pack_id" in result.errors
    assert "missing_observation_window" in result.errors
    assert "missing_proof_pack_summary" in result.errors
    assert result.summary["artifact_writer_status"] == "BLOCKED"


def test_rpw1_preserves_paper_only_safety_boundary(tmp_path: Path) -> None:
    result = write_runtime_proof_pack_artifact(
        output_dir=tmp_path,
        proof_pack_id="RGP13-unsafe",
        observation_window="2026-06-03",
        proof_pack_summary=_summary(),
        live_trading_authorized=True,
        broker_execution_mode="live",
    )

    assert result.valid is False
    assert "live_trading_must_remain_false" in result.errors
    assert "broker_execution_mode_must_be_paper_only" in result.errors
    assert result.summary["live_trading_authorized"] is False
    assert result.summary["broker_execution_mode"] == "paper_only"
