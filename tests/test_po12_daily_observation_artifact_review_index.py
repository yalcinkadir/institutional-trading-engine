from __future__ import annotations

from pathlib import Path

from src.operations.daily_observation_artifact_review_index import (
    build_daily_observation_artifact_review_index,
    write_daily_observation_artifact_review_index,
)
from src.operations.daily_observation_automation_runner import build_daily_observation_automation_artifact


def _artifact(day: str, **kwargs: object) -> dict[str, object]:
    result = build_daily_observation_automation_artifact(
        observation_date=day,
        created_at=f"{day}T00:00:00Z",
        **kwargs,
    )
    artifact = dict(result.artifact)
    artifact["artifact_path"] = result.artifact_path
    return artifact


def test_po12_builds_review_index_for_passed_and_blocked_artifacts() -> None:
    artifacts = [
        _artifact("2026-06-01"),
        _artifact("2026-06-02", missing_evidence=["daily_report"]),
    ]

    result = build_daily_observation_artifact_review_index(artifacts)

    assert result.valid is True
    assert result.errors == ()
    assert result.index["index_path"] == "reports/daily_observation_automation/review_index.json"
    assert result.index["artifact_root"] == "reports/daily_observation_automation"
    assert result.index["retention_days"] == 180
    assert result.index["total_artifacts"] == 2
    assert result.index["passed_count"] == 1
    assert result.index["blocked_count"] == 1
    assert result.index["review_ready_count"] == 1
    assert result.index["status_counts"] == {"PASSED": 1, "BLOCKED": 1}
    assert result.index["live_trading_authorized"] is False
    assert result.index["broker_execution_mode"] == "paper_only"


def test_po12_entries_are_sorted_by_observation_date() -> None:
    artifacts = [
        _artifact("2026-06-03"),
        _artifact("2026-06-01"),
        _artifact("2026-06-02"),
    ]

    result = build_daily_observation_artifact_review_index(artifacts)

    assert [entry["observation_date"] for entry in result.index["artifacts"]] == [
        "2026-06-01",
        "2026-06-02",
        "2026-06-03",
    ]


def test_po12_rejects_duplicate_artifact_dates() -> None:
    artifacts = [
        _artifact("2026-06-01"),
        _artifact("2026-06-01"),
    ]

    result = build_daily_observation_artifact_review_index(artifacts)

    assert result.valid is False
    assert "duplicate_artifact_date:2026-06-01" in result.errors


def test_po12_rejects_invalid_retention_days() -> None:
    result = build_daily_observation_artifact_review_index(
        [_artifact("2026-06-01")],
        retention_days=0,
    )

    assert result.valid is False
    assert "retention_days_must_be_positive" in result.errors


def test_po12_rejects_live_trading_artifact_boundary_violation() -> None:
    artifact = _artifact("2026-06-01")
    artifact["live_trading_authorized"] = True

    result = build_daily_observation_artifact_review_index([artifact])

    assert result.valid is False
    assert "artifact:2026-06-01:live_trading_must_remain_false" in result.errors
    assert result.index["artifacts"][0]["live_trading_authorized"] is False


def test_po12_rejects_non_paper_broker_boundary_violation() -> None:
    artifact = _artifact("2026-06-01")
    artifact["broker_execution_mode"] = "live"

    result = build_daily_observation_artifact_review_index([artifact])

    assert result.valid is False
    assert "artifact:2026-06-01:broker_execution_mode_must_be_paper_only" in result.errors
    assert result.index["artifacts"][0]["broker_execution_mode"] == "paper_only"


def test_po12_rejects_gate_boundary_violation() -> None:
    artifact = _artifact("2026-06-01")
    artifact["gate"] = dict(artifact["gate"])
    artifact["gate"]["live_trading_authorized"] = True

    result = build_daily_observation_artifact_review_index([artifact])

    assert result.valid is False
    assert "artifact:2026-06-01:gate_live_trading_must_remain_false" in result.errors


def test_po12_rejects_non_canonical_artifact_path() -> None:
    artifact = _artifact("2026-06-01")
    artifact["artifact_path"] = "reports/wrong/2026-06-01.json"

    result = build_daily_observation_artifact_review_index([artifact])

    assert result.valid is False
    assert "artifact:2026-06-01:artifact_path_must_be_canonical" in result.errors


def test_po12_writes_review_index_to_canonical_path(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)

    result = write_daily_observation_artifact_review_index(
        artifacts=[_artifact("2026-06-01")],
    )

    assert result.valid is True
    path = Path("reports/daily_observation_automation/review_index.json")
    assert path.exists()
    assert '"total_artifacts": 1' in path.read_text(encoding="utf-8")


def test_po12_rejects_non_canonical_review_index_output_path(tmp_path) -> None:
    result = write_daily_observation_artifact_review_index(
        artifacts=[_artifact("2026-06-01")],
        output_path=tmp_path / "review_index.json",
    )

    assert result.valid is False
    assert result.errors == ("review_index_path_must_be_canonical",)
