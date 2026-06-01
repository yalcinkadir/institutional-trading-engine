from __future__ import annotations

from pathlib import Path

from src.operations.daily_observation_artifact_review_index import build_daily_observation_artifact_review_index
from src.operations.daily_observation_automation_runner import build_daily_observation_automation_artifact
from src.operations.monthly_paper_observation_review_pack import (
    build_monthly_paper_observation_review_pack,
    build_monthly_paper_observation_review_pack_path,
    write_monthly_paper_observation_review_pack,
)


def _automation_artifact(day: str, **kwargs: object) -> dict[str, object]:
    result = build_daily_observation_automation_artifact(
        observation_date=day,
        created_at=f"{day}T00:00:00Z",
        **kwargs,
    )
    artifact = dict(result.artifact)
    artifact["artifact_path"] = result.artifact_path
    return artifact


def _review_index(*artifacts: dict[str, object]) -> dict[str, object]:
    result = build_daily_observation_artifact_review_index(artifacts)
    assert result.valid is True
    return result.index


def test_po13_builds_review_ready_monthly_pack() -> None:
    index = _review_index(
        _automation_artifact("2026-06-01"),
        _automation_artifact("2026-06-02"),
    )

    result = build_monthly_paper_observation_review_pack(
        index,
        month="2026-06",
        minimum_review_ready_days=2,
    )

    assert result.valid is True
    assert result.errors == ()
    assert result.pack_path == "reports/monthly_paper_observation_review/2026-06.json"
    assert result.pack["monthly_review_status"] == "REVIEW_READY"
    assert result.pack["total_days"] == 2
    assert result.pack["passed_days"] == ["2026-06-01", "2026-06-02"]
    assert result.pack["blocked_days"] == []
    assert result.pack["review_ready_days"] == ["2026-06-01", "2026-06-02"]
    assert result.pack["live_trading_authorized"] is False
    assert result.pack["broker_execution_mode"] == "paper_only"


def test_po13_filters_monthly_entries_only() -> None:
    index = _review_index(
        _automation_artifact("2026-06-01"),
        _automation_artifact("2026-07-01"),
    )

    result = build_monthly_paper_observation_review_pack(index, month="2026-06")

    assert result.valid is True
    assert result.pack["total_days"] == 1
    assert result.pack["review_ready_days"] == ["2026-06-01"]
    assert [entry["observation_date"] for entry in result.pack["artifacts"]] == ["2026-06-01"]


def test_po13_blocks_month_with_no_artifacts() -> None:
    index = _review_index(_automation_artifact("2026-06-01"))

    result = build_monthly_paper_observation_review_pack(index, month="2026-07")

    assert result.valid is False
    assert result.pack["monthly_review_status"] == "BLOCKED"
    assert "no_monthly_observation_artifacts" in result.errors
    assert "insufficient_review_ready_days" in result.errors


def test_po13_blocks_insufficient_review_ready_days() -> None:
    index = _review_index(_automation_artifact("2026-06-01"))

    result = build_monthly_paper_observation_review_pack(
        index,
        month="2026-06",
        minimum_review_ready_days=2,
    )

    assert result.valid is False
    assert result.pack["monthly_review_status"] == "BLOCKED"
    assert "insufficient_review_ready_days" in result.errors


def test_po13_blocks_blocked_observation_days() -> None:
    index = _review_index(
        _automation_artifact("2026-06-01"),
        _automation_artifact("2026-06-02", missing_evidence=["daily_report"]),
    )

    result = build_monthly_paper_observation_review_pack(index, month="2026-06")

    assert result.valid is False
    assert result.pack["monthly_review_status"] == "BLOCKED"
    assert result.pack["blocked_days"] == ["2026-06-02"]
    assert result.pack["gate_failure_days"] == ["2026-06-02"]
    assert "blocked_observation_days_present" in result.errors
    assert "gate_failures_present" in result.errors
    assert "monthly_blockers_present" in result.errors
    assert "rejected_records_present" in result.errors


def test_po13_blocks_needs_review_records() -> None:
    index = _review_index(
        _automation_artifact("2026-06-01", incidents=["manual review"]),
    )

    result = build_monthly_paper_observation_review_pack(index, month="2026-06")

    assert result.valid is False
    assert result.pack["monthly_review_status"] == "BLOCKED"
    assert "needs_review_records_present" in result.errors
    assert "gate_failures_present" in result.errors


def test_po13_rejects_invalid_month_format() -> None:
    index = _review_index(_automation_artifact("2026-06-01"))

    result = build_monthly_paper_observation_review_pack(index, month="2026-6")

    assert result.valid is False
    assert "month_must_use_yyyy_mm_format" in result.errors


def test_po13_rejects_invalid_minimum_review_ready_days() -> None:
    index = _review_index(_automation_artifact("2026-06-01"))

    result = build_monthly_paper_observation_review_pack(
        index,
        month="2026-06",
        minimum_review_ready_days=0,
    )

    assert result.valid is False
    assert "minimum_review_ready_days_must_be_positive" in result.errors


def test_po13_rejects_review_index_boundary_violation() -> None:
    index = _review_index(_automation_artifact("2026-06-01"))
    index["live_trading_authorized"] = True

    result = build_monthly_paper_observation_review_pack(index, month="2026-06")

    assert result.valid is False
    assert "review_index_live_trading_must_remain_false" in result.errors
    assert result.pack["live_trading_authorized"] is False


def test_po13_rejects_artifact_boundary_violation() -> None:
    index = _review_index(_automation_artifact("2026-06-01"))
    index["artifacts"][0]["broker_execution_mode"] = "live"

    result = build_monthly_paper_observation_review_pack(index, month="2026-06")

    assert result.valid is False
    assert "artifact:2026-06-01:broker_execution_mode_must_be_paper_only" in result.errors
    assert result.pack["broker_execution_mode"] == "paper_only"


def test_po13_builds_canonical_monthly_pack_path() -> None:
    assert build_monthly_paper_observation_review_pack_path("2026-06") == Path(
        "reports/monthly_paper_observation_review/2026-06.json"
    )


def test_po13_writes_monthly_pack_to_canonical_path(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    index = _review_index(_automation_artifact("2026-06-01"))
    result = build_monthly_paper_observation_review_pack(index, month="2026-06")

    write_result = write_monthly_paper_observation_review_pack(result=result)

    assert write_result.valid is True
    path = Path("reports/monthly_paper_observation_review/2026-06.json")
    assert path.exists()
    assert '"monthly_review_status": "REVIEW_READY"' in path.read_text(encoding="utf-8")


def test_po13_rejects_non_canonical_monthly_pack_output_path(tmp_path) -> None:
    index = _review_index(_automation_artifact("2026-06-01"))
    result = build_monthly_paper_observation_review_pack(index, month="2026-06")

    write_result = write_monthly_paper_observation_review_pack(
        result=result,
        output_path=tmp_path / "wrong.json",
    )

    assert write_result.valid is False
    assert "monthly_review_pack_path_must_be_canonical" in write_result.errors
