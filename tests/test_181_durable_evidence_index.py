from __future__ import annotations

from src.operations.daily_observation_artifact_review_index import (
    DURABLE_STATUS_BLOCKED,
    DURABLE_STATUS_DEGRADED,
    DURABLE_STATUS_FAILED,
    DURABLE_STATUS_NO_TRADE_VALID,
    DURABLE_STATUS_SUCCESS,
    build_daily_observation_artifact_review_index,
)
from src.operations.daily_observation_automation_runner import build_daily_observation_automation_artifact


def _artifact(day: str, **overrides: object) -> dict[str, object]:
    result = build_daily_observation_automation_artifact(
        observation_date=day,
        created_at=f"{day}T00:00:00Z",
    )
    artifact = dict(result.artifact)
    artifact["artifact_path"] = result.artifact_path
    artifact.update(overrides)
    return artifact


def test_181_durable_index_records_required_audit_fields() -> None:
    artifact = _artifact(
        "2026-06-01",
        workflow_run_id="27370000001",
        data_mode="polygon_real_data",
        artifact_pointer="reports/daily_observation_automation/2026-06-01.json",
        artifact_sha256="a" * 64,
    )

    result = build_daily_observation_artifact_review_index([artifact])

    assert result.valid is True
    assert result.index["schema_version"] == "paper_observation_durable_evidence_index.v1"
    assert result.index["github_actions_artifacts_are_audit_source"] is False
    assert result.index["large_runtime_artifacts_committed_to_main"] is False
    assert result.index["durable_history_reconstructable_after_artifact_expiry"] is True

    entry = result.index["artifacts"][0]
    assert entry["observation_date"] == "2026-06-01"
    assert entry["workflow_run_id"] == "27370000001"
    assert entry["artifact_pointer"] == "reports/daily_observation_automation/2026-06-01.json"
    assert entry["artifact_sha256"] == "a" * 64
    assert entry["data_mode"] == "polygon_real_data"
    assert entry["degradation_flags"] == []
    assert entry["durable_status"] == DURABLE_STATUS_SUCCESS


def test_181_durable_index_links_related_evidence_families_without_committing_large_artifacts() -> None:
    result = build_daily_observation_artifact_review_index([_artifact("2026-06-01")])
    references = result.index["related_evidence_references"]
    by_issue = {item["issue"]: item for item in references}

    assert result.index["large_runtime_artifacts_committed_to_main"] is False
    assert result.index["github_actions_artifacts_are_audit_source"] is False
    assert set(by_issue) == {"#204", "#205", "#206", "#207", "#208", "#209", "#210"}
    assert by_issue["#204"]["path"] == "reports/scheduled_report_liveness/latest-scheduled-report-liveness.json"
    assert by_issue["#206"]["path"] == "reports/backtests/real-data-backtest-evidence.json"
    assert by_issue["#207"]["path"] == "src/backtesting/watcher_coupled_backtest.py"
    assert by_issue["#209"]["path"] == "reports/runtime/entry_exit_watcher_runtime_health.json"
    assert by_issue["#210"]["path"] == "src/execution/broker_adapter.py"


def test_181_durable_index_uses_explicit_unknowns_when_metadata_is_not_available() -> None:
    result = build_daily_observation_artifact_review_index([_artifact("2026-06-01")])

    entry = result.index["artifacts"][0]
    assert entry["workflow_run_id"] == "UNKNOWN"
    assert entry["artifact_sha256"] == "not_available"
    assert entry["data_mode"] == "UNKNOWN"
    assert entry["artifact_pointer"] == "reports/daily_observation_automation/2026-06-01.json"


def test_181_durable_index_distinguishes_blocked_degraded_failed_and_no_trade_valid() -> None:
    success = _artifact("2026-06-01", workflow_run_id="run-success")

    blocked = _artifact("2026-06-02", workflow_run_id="run-blocked")
    blocked["automation_status"] = "BLOCKED"
    blocked["gate"] = dict(blocked["gate"])
    blocked["gate"]["gate_status"] = "BLOCKED"
    blocked["gate"]["approved_for_review"] = False

    degraded = _artifact(
        "2026-06-03",
        workflow_run_id="run-degraded",
        degradation_flags=["PROXY_DEGRADED"],
    )

    failed = _artifact("2026-06-04", workflow_run_id="run-failed")
    failed["errors"] = ("upstream_report_missing",)

    no_trade_valid = _artifact("2026-06-05", workflow_run_id="run-no-trade")
    no_trade_valid["summary"] = dict(no_trade_valid["summary"])
    no_trade_valid["summary"]["review_ready"] = False
    no_trade_valid["gate"] = dict(no_trade_valid["gate"])
    no_trade_valid["gate"]["approved_for_review"] = True

    result = build_daily_observation_artifact_review_index(
        [success, blocked, degraded, failed, no_trade_valid]
    )

    statuses = {
        entry["observation_date"]: entry["durable_status"]
        for entry in result.index["artifacts"]
    }
    assert statuses == {
        "2026-06-01": DURABLE_STATUS_SUCCESS,
        "2026-06-02": DURABLE_STATUS_BLOCKED,
        "2026-06-03": DURABLE_STATUS_DEGRADED,
        "2026-06-04": DURABLE_STATUS_FAILED,
        "2026-06-05": DURABLE_STATUS_NO_TRADE_VALID,
    }
    assert result.index["durable_status_counts"] == {
        DURABLE_STATUS_SUCCESS: 1,
        DURABLE_STATUS_BLOCKED: 1,
        DURABLE_STATUS_DEGRADED: 1,
        DURABLE_STATUS_FAILED: 1,
        DURABLE_STATUS_NO_TRADE_VALID: 1,
    }


def test_181_durable_index_rejects_large_runtime_artifact_boundary_violations() -> None:
    artifact = _artifact("2026-06-01")
    artifact["live_trading_authorized"] = True

    result = build_daily_observation_artifact_review_index([artifact])

    assert result.valid is False
    assert "artifact:2026-06-01:live_trading_must_remain_false" in result.errors
    assert result.index["large_runtime_artifacts_committed_to_main"] is False
    assert result.index["github_actions_artifacts_are_audit_source"] is False
