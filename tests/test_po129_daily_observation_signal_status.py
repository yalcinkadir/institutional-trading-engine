from __future__ import annotations

from src.operations.daily_observation_automation_runner import build_daily_observation_automation_artifact
from src.operations.daily_observation_record_validator import validate_daily_observation_record
from src.operations.daily_observation_record_writer import build_daily_observation_record


OBSERVATION_DATE = "2026-06-06"


def _failed_signal_health() -> dict[str, object]:
    return {
        "stage": "signal_generation",
        "status": "FAILED",
        "exception_type": "RuntimeError",
        "exception_message": "build_signals exploded",
        "live_trading_authorized": False,
        "broker_execution_mode": "paper_only",
    }


def test_daily_observation_record_rejects_failed_signal_generation() -> None:
    record = build_daily_observation_record(
        observation_date=OBSERVATION_DATE,
        signal_generation_status="FAILED",
        signal_generation_health=_failed_signal_health(),
        created_at=f"{OBSERVATION_DATE}T00:00:00Z",
    )

    assert record["status"] == "REJECTED"
    assert record["signal_generation_status"] == "FAILED"
    assert record["signal_generation_health"] == _failed_signal_health()
    assert record["missing_evidence"] == ["signal_generation_status:FAILED"]
    assert validate_daily_observation_record(record).valid is True


def test_daily_observation_validator_rejects_accepted_failed_signal_generation() -> None:
    record = build_daily_observation_record(
        observation_date=OBSERVATION_DATE,
        signal_generation_status="FAILED",
        signal_generation_health=_failed_signal_health(),
        created_at=f"{OBSERVATION_DATE}T00:00:00Z",
    )
    record["status"] = "ACCEPTED"
    record["missing_evidence"] = []

    validation = validate_daily_observation_record(record)

    assert validation.valid is False
    assert "accepted_record_requires_signal_generation_passed" in validation.errors


def test_daily_observation_automation_blocks_failed_signal_generation() -> None:
    result = build_daily_observation_automation_artifact(
        observation_date=OBSERVATION_DATE,
        signal_generation_status="FAILED",
        signal_generation_health=_failed_signal_health(),
        minimum_records=1,
        created_at=f"{OBSERVATION_DATE}T00:00:00Z",
    )

    assert result.valid is False
    assert result.artifact["automation_status"] == "BLOCKED"
    assert result.artifact["signal_generation_status"] == "FAILED"
    assert result.artifact["signal_generation_health"] == _failed_signal_health()
    assert result.artifact["summary"]["rejected_dates"] == [OBSERVATION_DATE]
    assert "rejected_observation_days_present" in result.artifact["gate"]["blockers"]


def test_daily_observation_record_keeps_valid_no_trade_day_accepted() -> None:
    record = build_daily_observation_record(
        observation_date=OBSERVATION_DATE,
        signal_generation_status="PASSED",
        created_at=f"{OBSERVATION_DATE}T00:00:00Z",
    )

    assert record["status"] == "ACCEPTED"
    assert record["missing_evidence"] == []
    assert record["signal_generation_status"] == "PASSED"
    assert validate_daily_observation_record(record).valid is True
