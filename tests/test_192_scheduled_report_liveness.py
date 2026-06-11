from __future__ import annotations

import json
from pathlib import Path

from src.operations.scheduled_report_liveness import (
    CURRENT_RUN_INCOMPLETE,
    CURRENT_RUN_MISSING,
    REPORT_LIVENESS_BLOCKED,
    REPORT_LIVENESS_DEGRADED,
    REPORT_LIVENESS_OK,
    STATUS_BLOCKED,
    STATUS_PASSED,
    build_report_family_freshness_summary,
    build_scheduled_report_liveness_artifact,
    build_scheduled_report_liveness_artifact_path,
    write_scheduled_report_liveness_artifact,
)


def _write_family_outputs(root: Path, day: str) -> None:
    files = {
        f"reports/signals/{day}-signals.json": "{}\n",
        f"reports/premarket/{day}-premarket.md": "# premarket\n",
        f"reports/intraday/{day}-intraday.md": "# intraday\n",
        f"reports/postmarket/{day}-postmarket.md": "# postmarket\n",
        f"reports/daily_evidence/{day}.json": "{}\n",
    }
    for relative_path, content in files.items():
        path = root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def test_192_blocks_missing_scheduled_market_report_outputs(tmp_path: Path) -> None:
    result = build_scheduled_report_liveness_artifact(
        report_type="postmarket",
        report_file=tmp_path / "reports/postmarket/2026-06-11-postmarket.md",
        latest_file=tmp_path / "reports/generated/postmarket-report.md",
        signals_file=tmp_path / "reports/signals/latest-signals.json",
        paper_health_file=tmp_path / "reports/validation/latest-paper-observation-health.json",
        run_timestamp="2026-06-11T21:00:00Z",
        workflow_name="Institutional Reports",
        commit_sha="abc123",
        run_date="2026-06-11",
        report_root=tmp_path,
    )

    assert result.valid is False
    assert result.artifact["scheduled_report_status"] == STATUS_BLOCKED
    assert result.artifact["report_liveness_status"] == REPORT_LIVENESS_BLOCKED
    assert result.artifact["current_run_state"] == CURRENT_RUN_MISSING
    assert result.artifact["productive_report_cycle"] is False
    assert "report_file_missing" in result.errors
    assert "latest_file_missing" in result.errors
    assert "signals_file_missing" in result.errors
    assert "paper_health_file_missing" in result.errors
    assert "workflow_did_not_produce_or_persist_current_output" in result.errors
    assert result.artifact["live_trading_authorized"] is False
    assert result.artifact["broker_execution_mode"] == "paper_only"


def test_192_blocks_empty_report_file_even_when_paths_exist(tmp_path: Path) -> None:
    _write_family_outputs(tmp_path, "2026-06-11")
    report_file = tmp_path / "reports/postmarket/2026-06-11-postmarket.md"
    latest_file = tmp_path / "reports/generated/postmarket-report.md"
    signals_file = tmp_path / "reports/signals/latest-signals.json"
    paper_health_file = tmp_path / "reports/validation/latest-paper-observation-health.json"
    for path in (latest_file, signals_file, paper_health_file):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("{}\n", encoding="utf-8")
    report_file.write_text("", encoding="utf-8")

    result = build_scheduled_report_liveness_artifact(
        report_type="postmarket",
        report_file=report_file,
        latest_file=latest_file,
        signals_file=signals_file,
        paper_health_file=paper_health_file,
        run_date="2026-06-11",
        report_root=tmp_path,
    )

    assert result.valid is False
    assert result.artifact["scheduled_report_status"] == STATUS_BLOCKED
    assert "report_file_empty" in result.errors
    assert "workflow_ran_but_validation_failed_or_incomplete" in result.errors
    assert result.artifact["current_run_state"] == CURRENT_RUN_INCOMPLETE
    assert result.artifact["file_evidence"]["report_file"]["exists"] is True
    assert result.artifact["file_evidence"]["report_file"]["non_empty"] is False


def test_192_passes_complete_market_report_evidence(tmp_path: Path) -> None:
    _write_family_outputs(tmp_path, "2026-06-11")
    report_file = tmp_path / "reports/postmarket/2026-06-11-postmarket.md"
    latest_file = tmp_path / "reports/generated/postmarket-report.md"
    signals_file = tmp_path / "reports/signals/latest-signals.json"
    paper_health_file = tmp_path / "reports/validation/latest-paper-observation-health.json"
    latest_file.parent.mkdir(parents=True, exist_ok=True)
    signals_file.parent.mkdir(parents=True, exist_ok=True)
    paper_health_file.parent.mkdir(parents=True, exist_ok=True)
    latest_file.write_text("# report\n", encoding="utf-8")
    signals_file.write_text(json.dumps({"signals": []}) + "\n", encoding="utf-8")
    paper_health_file.write_text(json.dumps({"passed": True}) + "\n", encoding="utf-8")

    result = build_scheduled_report_liveness_artifact(
        report_type="postmarket",
        report_file=report_file,
        latest_file=latest_file,
        signals_file=signals_file,
        paper_health_file=paper_health_file,
        run_timestamp="2026-06-11T21:00:00Z",
        workflow_name="Institutional Reports",
        commit_sha="abc123",
        run_date="2026-06-11",
        report_root=tmp_path,
    )

    assert result.valid is True
    assert result.errors == ()
    assert result.artifact["scheduled_report_status"] == STATUS_PASSED
    assert result.artifact["report_liveness_status"] == REPORT_LIVENESS_OK
    assert result.artifact["productive_report_cycle"] is True
    assert result.artifact["freshness_by_family"]["signals"]["freshness_status"] == REPORT_LIVENESS_OK
    assert result.artifact["file_evidence"]["signals_file"]["non_empty"] is True
    assert result.artifact["file_evidence"]["paper_health_file"]["non_empty"] is True


def test_192_weekly_report_does_not_require_signals_or_paper_health(tmp_path: Path) -> None:
    _write_family_outputs(tmp_path, "2026-06-11")
    report_file = tmp_path / "reports/weekly/2026-W24-weekly.md"
    latest_file = tmp_path / "reports/generated/weekly-report.md"
    report_file.parent.mkdir(parents=True, exist_ok=True)
    latest_file.parent.mkdir(parents=True, exist_ok=True)
    report_file.write_text("# weekly\n", encoding="utf-8")
    latest_file.write_text("# weekly\n", encoding="utf-8")

    result = build_scheduled_report_liveness_artifact(
        report_type="weekly",
        report_file=report_file,
        latest_file=latest_file,
        signals_file=None,
        paper_health_file=None,
        run_date="2026-06-11",
        report_root=tmp_path,
    )

    assert result.valid is True
    assert result.artifact["scheduled_report_status"] == STATUS_PASSED
    assert result.errors == ()
    assert result.artifact["productive_report_cycle"] is True


def test_192_writes_dated_latest_and_health_liveness_artifacts(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    _write_family_outputs(tmp_path, "2026-06-11")
    report_file = Path("reports/postmarket/2026-06-11-postmarket.md")
    latest_file = Path("reports/generated/postmarket-report.md")
    signals_file = Path("reports/signals/latest-signals.json")
    paper_health_file = Path("reports/validation/latest-paper-observation-health.json")
    for path in (latest_file, signals_file, paper_health_file):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("ok\n", encoding="utf-8")

    result = build_scheduled_report_liveness_artifact(
        report_type="postmarket",
        report_file=report_file,
        latest_file=latest_file,
        signals_file=signals_file,
        paper_health_file=paper_health_file,
        run_date="2026-06-11",
    )
    write_result = write_scheduled_report_liveness_artifact(result=result)

    dated_path = Path(write_result.artifact_path)
    latest_path = Path(write_result.latest_artifact_path)
    health_latest_path = Path("reports/health/report-liveness-latest.json")
    assert dated_path == Path("reports/scheduled_report_liveness/2026-06-11-postmarket-liveness.json")
    assert latest_path == Path("reports/scheduled_report_liveness/latest-scheduled-report-liveness.json")
    assert dated_path.exists()
    assert latest_path.exists()
    assert health_latest_path.exists()
    payload = json.loads(health_latest_path.read_text(encoding="utf-8"))
    assert payload["scheduled_report_status"] == STATUS_PASSED


def test_192_detects_one_business_day_without_fresh_report_as_degraded(tmp_path: Path) -> None:
    _write_family_outputs(tmp_path, "2026-06-10")

    summary = build_report_family_freshness_summary(report_root=tmp_path, run_date="2026-06-11")

    assert summary["premarket"]["freshness_status"] == REPORT_LIVENESS_DEGRADED
    assert summary["premarket"]["business_days_without_fresh_output"] == 1


def test_192_blocks_two_consecutive_business_days_without_fresh_report_output(tmp_path: Path) -> None:
    _write_family_outputs(tmp_path, "2026-06-09")

    summary = build_report_family_freshness_summary(report_root=tmp_path, run_date="2026-06-11")

    assert summary["signals"]["freshness_status"] == REPORT_LIVENESS_BLOCKED
    assert summary["signals"]["business_days_without_fresh_output"] == 2
    assert summary["daily_evidence"]["freshness_status"] == REPORT_LIVENESS_BLOCKED


def test_192_current_run_complete_but_stale_family_blocks_productive_cycle(tmp_path: Path) -> None:
    _write_family_outputs(tmp_path, "2026-06-09")
    report_file = tmp_path / "reports/postmarket/2026-06-11-postmarket.md"
    latest_file = tmp_path / "reports/generated/postmarket-report.md"
    signals_file = tmp_path / "reports/signals/latest-signals.json"
    paper_health_file = tmp_path / "reports/validation/latest-paper-observation-health.json"
    for path in (report_file, latest_file, signals_file, paper_health_file):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("ok\n", encoding="utf-8")

    result = build_scheduled_report_liveness_artifact(
        report_type="postmarket",
        report_file=report_file,
        latest_file=latest_file,
        signals_file=signals_file,
        paper_health_file=paper_health_file,
        run_date="2026-06-11",
        report_root=tmp_path,
    )

    assert result.valid is False
    assert result.artifact["current_run_state"] == "WORKFLOW_RAN_VALIDATED"
    assert "signals_stale_or_missing:2" in result.errors
    assert "premarket_stale_or_missing:2" in result.errors
    assert result.artifact["productive_report_cycle"] is False


def test_192_builds_canonical_artifact_path() -> None:
    assert build_scheduled_report_liveness_artifact_path("premarket", "2026-06-11") == Path(
        "reports/scheduled_report_liveness/2026-06-11-premarket-liveness.json"
    )
