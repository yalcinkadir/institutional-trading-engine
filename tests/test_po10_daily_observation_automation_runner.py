from __future__ import annotations

from pathlib import Path

from src.operations.daily_observation_automation_runner import (
    build_daily_observation_automation_artifact,
    build_daily_observation_automation_artifact_path,
    write_daily_observation_automation_artifact,
)
from src.operations.daily_observation_record_writer import build_daily_observation_record


def _record(day: str, **kwargs: object) -> dict[str, object]:
    return build_daily_observation_record(
        observation_date=day,
        created_at=f"{day}T00:00:00Z",
        **kwargs,
    )


def test_po10_builds_passed_automation_artifact_for_clean_observation_day() -> None:
    result = build_daily_observation_automation_artifact(
        observation_date="2026-06-01",
        artifact_paths=["reports/daily_evidence/2026-06-01.json"],
        minimum_records=1,
        created_at="2026-06-01T00:00:00Z",
    )

    assert result.valid is True
    assert result.errors == ()
    assert result.artifact_path == "reports/daily_observation_automation/2026-06-01.json"
    assert result.artifact["automation_status"] == "PASSED"
    assert result.artifact["record_path"] == "reports/daily_observation_records/2026-06-01.json"
    assert result.artifact["summary"]["review_ready"] is True
    assert result.artifact["gate"]["gate_status"] == "PASSED"
    assert result.artifact["live_trading_authorized"] is False
    assert result.artifact["broker_execution_mode"] == "paper_only"


def test_po10_blocks_when_minimum_record_requirement_is_not_met() -> None:
    result = build_daily_observation_automation_artifact(
        observation_date="2026-06-01",
        minimum_records=2,
        created_at="2026-06-01T00:00:00Z",
    )

    assert result.valid is False
    assert result.errors == ()
    assert result.artifact["automation_status"] == "BLOCKED"
    assert result.artifact["gate"]["gate_status"] == "BLOCKED"
    assert "insufficient_observation_records" in result.artifact["gate"]["blockers"]


def test_po10_blocks_rejected_observation_day() -> None:
    result = build_daily_observation_automation_artifact(
        observation_date="2026-06-01",
        missing_evidence=["daily_report"],
        minimum_records=1,
        created_at="2026-06-01T00:00:00Z",
    )

    assert result.valid is False
    assert result.artifact["automation_status"] == "BLOCKED"
    assert result.artifact["summary"]["rejected_dates"] == ["2026-06-01"]
    assert "rejected_observation_days_present" in result.artifact["gate"]["blockers"]


def test_po10_blocks_needs_review_observation_day() -> None:
    result = build_daily_observation_automation_artifact(
        observation_date="2026-06-01",
        incidents=["manual evidence check needed"],
        minimum_records=1,
        created_at="2026-06-01T00:00:00Z",
    )

    assert result.valid is False
    assert result.artifact["automation_status"] == "BLOCKED"
    assert result.artifact["summary"]["needs_review_dates"] == ["2026-06-01"]
    assert result.artifact["summary"]["review_required_dates"] == ["2026-06-01"]
    assert "needs_review_observation_days_present" in result.artifact["gate"]["blockers"]
    assert "manual_review_required_dates_present" in result.artifact["gate"]["blockers"]


def test_po10_includes_existing_records_before_running_summary_and_gate() -> None:
    existing = [_record("2026-06-01")]

    result = build_daily_observation_automation_artifact(
        observation_date="2026-06-02",
        existing_records=existing,
        minimum_records=2,
        created_at="2026-06-02T00:00:00Z",
    )

    assert result.valid is True
    assert result.artifact["automation_status"] == "PASSED"
    assert result.artifact["summary"]["total_records"] == 2
    assert result.artifact["summary"]["accepted_count"] == 2
    assert result.artifact["gate"]["minimum_records"] == 2


def test_po10_surfaces_index_errors_for_duplicate_record_dates() -> None:
    existing = [_record("2026-06-01")]

    result = build_daily_observation_automation_artifact(
        observation_date="2026-06-01",
        existing_records=existing,
        minimum_records=1,
        created_at="2026-06-01T00:00:00Z",
    )

    assert result.valid is False
    assert result.artifact["automation_status"] == "PASSED"
    assert "index:duplicate_record_date:2026-06-01" in result.errors
    assert result.artifact["errors"] == result.errors


def test_po10_builds_canonical_automation_artifact_path() -> None:
    assert build_daily_observation_automation_artifact_path("2026-06-01") == Path(
        "reports/daily_observation_automation/2026-06-01.json"
    )


def test_po10_writes_automation_artifact_to_canonical_path(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    result = build_daily_observation_automation_artifact(
        observation_date="2026-06-01",
        created_at="2026-06-01T00:00:00Z",
    )

    write_result = write_daily_observation_automation_artifact(result=result)

    assert write_result.valid is True
    path = Path(write_result.artifact_path)
    assert path.exists()
    assert '"automation_status": "PASSED"' in path.read_text(encoding="utf-8")


def test_po10_rejects_non_canonical_automation_artifact_output_path(tmp_path) -> None:
    result = build_daily_observation_automation_artifact(
        observation_date="2026-06-01",
        created_at="2026-06-01T00:00:00Z",
    )

    write_result = write_daily_observation_automation_artifact(
        result=result,
        output_path=tmp_path / "wrong.json",
    )

    assert write_result.valid is False
    assert "automation_artifact_path_must_be_canonical" in write_result.errors
