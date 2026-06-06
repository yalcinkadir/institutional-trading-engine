from pathlib import Path

from src.operations.daily_observation_automation_runner import (
    AUTOMATION_STATUS_BLOCKED,
    AUTOMATION_STATUS_PASSED,
    build_daily_observation_automation_artifact,
)
from src.operations.daily_observation_record_validator import validate_daily_observation_record
from src.operations.daily_observation_record_writer import build_daily_observation_record


OBSERVATION_DATE = "2026-06-05"
DAILY_EVIDENCE_PATH = f"reports/daily_evidence/{OBSERVATION_DATE}.json"


def test_daily_observation_record_rejects_missing_artifact_path_when_required(tmp_path: Path) -> None:
    record = build_daily_observation_record(
        observation_date=OBSERVATION_DATE,
        artifact_paths=[DAILY_EVIDENCE_PATH],
        require_artifact_paths_exist=True,
        artifact_root=tmp_path,
        created_at=f"{OBSERVATION_DATE}T00:00:00Z",
    )

    assert record["status"] == "REJECTED"
    assert record["review_required"] is False
    assert record["missing_evidence"] == [f"missing_artifact:{DAILY_EVIDENCE_PATH}"]
    assert validate_daily_observation_record(record).valid is True


def test_daily_observation_record_accepts_existing_artifact_path_when_required(tmp_path: Path) -> None:
    evidence_path = tmp_path / DAILY_EVIDENCE_PATH
    evidence_path.parent.mkdir(parents=True)
    evidence_path.write_text('{"passed": true}\n', encoding="utf-8")

    record = build_daily_observation_record(
        observation_date=OBSERVATION_DATE,
        artifact_paths=[DAILY_EVIDENCE_PATH],
        require_artifact_paths_exist=True,
        artifact_root=tmp_path,
        created_at=f"{OBSERVATION_DATE}T00:00:00Z",
    )

    assert record["status"] == "ACCEPTED"
    assert record["missing_evidence"] == []
    assert validate_daily_observation_record(record).valid is True


def test_daily_observation_automation_blocks_missing_daily_evidence_artifact(tmp_path: Path) -> None:
    result = build_daily_observation_automation_artifact(
        observation_date=OBSERVATION_DATE,
        artifact_paths=[DAILY_EVIDENCE_PATH],
        minimum_records=1,
        created_at=f"{OBSERVATION_DATE}T00:00:00Z",
        require_artifact_paths_exist=True,
        artifact_root=tmp_path,
    )

    assert result.valid is False
    assert result.artifact["automation_status"] == AUTOMATION_STATUS_BLOCKED
    assert result.artifact["summary"]["accepted_records"] == 0
    assert result.artifact["summary"]["rejected_records"] == 1


def test_daily_observation_automation_passes_when_daily_evidence_artifact_exists(tmp_path: Path) -> None:
    evidence_path = tmp_path / DAILY_EVIDENCE_PATH
    evidence_path.parent.mkdir(parents=True)
    evidence_path.write_text('{"passed": true}\n', encoding="utf-8")

    result = build_daily_observation_automation_artifact(
        observation_date=OBSERVATION_DATE,
        artifact_paths=[DAILY_EVIDENCE_PATH],
        minimum_records=1,
        created_at=f"{OBSERVATION_DATE}T00:00:00Z",
        require_artifact_paths_exist=True,
        artifact_root=tmp_path,
    )

    assert result.valid is True
    assert result.artifact["automation_status"] == AUTOMATION_STATUS_PASSED
    assert result.artifact["summary"]["accepted_records"] == 1
    assert result.artifact["summary"]["rejected_records"] == 0
