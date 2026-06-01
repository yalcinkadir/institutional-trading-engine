from __future__ import annotations

import json
from pathlib import Path

from src.operations.daily_observation_record_writer import (
    build_daily_observation_record,
    determine_daily_observation_status,
    write_daily_observation_record,
)


def test_po5_status_mapping_accepts_clean_day() -> None:
    status, review_required = determine_daily_observation_status(
        missing_evidence=[],
        incidents=[],
    )

    assert status == "ACCEPTED"
    assert review_required is False


def test_po5_status_mapping_rejects_missing_evidence() -> None:
    status, review_required = determine_daily_observation_status(
        missing_evidence=["Daily Evidence report"],
        incidents=[],
    )

    assert status == "REJECTED"
    assert review_required is False


def test_po5_status_mapping_needs_review_for_incidents() -> None:
    status, review_required = determine_daily_observation_status(
        missing_evidence=[],
        incidents=["provider degradation documented"],
    )

    assert status == "NEEDS_REVIEW"
    assert review_required is True


def test_po5_builds_valid_accepted_record() -> None:
    record = build_daily_observation_record(
        observation_date="2026-06-01",
        artifact_paths=["reports/daily_evidence/2026-06-01.md"],
        created_at="2026-06-01T00:00:00Z",
    )

    assert record["status"] == "ACCEPTED"
    assert record["missing_evidence"] == []
    assert record["incidents"] == []
    assert record["review_required"] is False
    assert record["live_trading_authorized"] is False
    assert record["broker_execution_mode"] == "paper_only"


def test_po5_builds_valid_rejected_record() -> None:
    record = build_daily_observation_record(
        observation_date="2026-06-01",
        missing_evidence=["Runtime Evidence manifest"],
        artifact_paths=[],
        created_at="2026-06-01T00:00:00Z",
    )

    assert record["status"] == "REJECTED"
    assert record["missing_evidence"] == ["Runtime Evidence manifest"]
    assert record["review_required"] is False
    assert record["live_trading_authorized"] is False


def test_po5_builds_valid_needs_review_record() -> None:
    record = build_daily_observation_record(
        observation_date="2026-06-01",
        incidents=["drift threshold touched"],
        artifact_paths=["reports/drift_regime/2026-06-01.json"],
        review_notes="Manual review required before acceptance.",
        created_at="2026-06-01T00:00:00Z",
    )

    assert record["status"] == "NEEDS_REVIEW"
    assert record["incidents"] == ["drift threshold touched"]
    assert record["review_required"] is True
    assert record["review_notes"] == "Manual review required before acceptance."
    assert record["live_trading_authorized"] is False


def test_po5_writes_valid_record_json(tmp_path: Path) -> None:
    output_path = tmp_path / "daily_observation" / "2026-06-01.json"
    record = build_daily_observation_record(
        observation_date="2026-06-01",
        artifact_paths=["reports/daily_evidence/2026-06-01.md"],
        created_at="2026-06-01T00:00:00Z",
    )

    result = write_daily_observation_record(record=record, output_path=output_path)

    assert result.valid is True
    written = json.loads(output_path.read_text(encoding="utf-8"))
    assert written == record
    assert written["live_trading_authorized"] is False
    assert written["broker_execution_mode"] == "paper_only"


def test_po5_does_not_write_invalid_record(tmp_path: Path) -> None:
    output_path = tmp_path / "daily_observation" / "invalid.json"
    record = build_daily_observation_record(
        observation_date="2026-06-01",
        artifact_paths=["reports/daily_evidence/2026-06-01.md"],
        created_at="2026-06-01T00:00:00Z",
    )
    record["live_trading_authorized"] = True

    result = write_daily_observation_record(record=record, output_path=output_path)

    assert result.valid is False
    assert "live_trading_must_remain_false" in result.errors
    assert not output_path.exists()
