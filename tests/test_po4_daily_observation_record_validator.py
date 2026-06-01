from __future__ import annotations

from src.operations.daily_observation_record_validator import validate_daily_observation_record


def _accepted_record() -> dict[str, object]:
    return {
        "date": "2026-06-01",
        "status": "ACCEPTED",
        "missing_evidence": [],
        "incidents": [],
        "artifact_paths": [
            "reports/daily_evidence/2026-06-01.md",
            "reports/runtime_evidence/2026-06-01.json",
        ],
        "review_required": False,
        "review_notes": "",
        "live_trading_authorized": False,
        "broker_execution_mode": "paper_only",
        "created_at": "2026-06-01T00:00:00Z",
    }


def test_po4_accepts_complete_accepted_record() -> None:
    result = validate_daily_observation_record(_accepted_record())

    assert result.valid is True
    assert result.errors == ()


def test_po4_rejects_missing_required_fields() -> None:
    record = _accepted_record()
    del record["artifact_paths"]

    result = validate_daily_observation_record(record)

    assert result.valid is False
    assert "missing_fields:artifact_paths" in result.errors


def test_po4_rejects_invalid_status() -> None:
    record = _accepted_record()
    record["status"] = "PENDING"

    result = validate_daily_observation_record(record)

    assert result.valid is False
    assert "invalid_status" in result.errors


def test_po4_accepted_record_cannot_have_missing_evidence_or_incidents() -> None:
    record = _accepted_record()
    record["missing_evidence"] = ["Daily Evidence report"]
    record["incidents"] = ["provider degradation"]
    record["review_required"] = True

    result = validate_daily_observation_record(record)

    assert result.valid is False
    assert "accepted_record_cannot_have_missing_evidence" in result.errors
    assert "accepted_record_cannot_have_unresolved_incidents" in result.errors
    assert "accepted_record_review_required_must_be_false" in result.errors


def test_po4_rejected_record_requires_missing_evidence() -> None:
    record = _accepted_record()
    record["status"] = "REJECTED"

    result = validate_daily_observation_record(record)

    assert result.valid is False
    assert "rejected_record_requires_missing_evidence" in result.errors


def test_po4_accepts_rejected_record_with_missing_evidence() -> None:
    record = _accepted_record()
    record["status"] = "REJECTED"
    record["missing_evidence"] = ["Runtime Evidence manifest"]

    result = validate_daily_observation_record(record)

    assert result.valid is True
    assert result.errors == ()


def test_po4_needs_review_requires_incidents_and_review_flag() -> None:
    record = _accepted_record()
    record["status"] = "NEEDS_REVIEW"

    result = validate_daily_observation_record(record)

    assert result.valid is False
    assert "needs_review_record_requires_incidents" in result.errors
    assert "needs_review_record_review_required_must_be_true" in result.errors


def test_po4_accepts_needs_review_record_with_incident_and_review_flag() -> None:
    record = _accepted_record()
    record["status"] = "NEEDS_REVIEW"
    record["incidents"] = ["provider degradation documented"]
    record["review_required"] = True
    record["review_notes"] = "Manual review required before acceptance."

    result = validate_daily_observation_record(record)

    assert result.valid is True
    assert result.errors == ()


def test_po4_blocks_live_trading_and_non_paper_broker_mode() -> None:
    record = _accepted_record()
    record["live_trading_authorized"] = True
    record["broker_execution_mode"] = "live"

    result = validate_daily_observation_record(record)

    assert result.valid is False
    assert "live_trading_must_remain_false" in result.errors
    assert "broker_execution_mode_must_be_paper_only" in result.errors


def test_po4_rejects_invalid_dates_and_non_string_lists() -> None:
    record = _accepted_record()
    record["date"] = "01-06-2026"
    record["created_at"] = "not-a-date"
    record["artifact_paths"] = [123]

    result = validate_daily_observation_record(record)

    assert result.valid is False
    assert "invalid_date" in result.errors
    assert "invalid_created_at" in result.errors
    assert "invalid_artifact_paths" in result.errors
