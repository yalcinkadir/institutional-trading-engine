from __future__ import annotations

from pathlib import Path

WORKFLOW_PATH = Path(".github/workflows/po11_daily_observation.yml")


def _workflow_text() -> str:
    return WORKFLOW_PATH.read_text(encoding="utf-8")


def test_po11_workflow_exists() -> None:
    assert WORKFLOW_PATH.exists()


def test_po11_workflow_has_schedule_and_manual_dispatch() -> None:
    text = _workflow_text()

    assert "schedule:" in text
    assert 'cron: "15 22 * * 1-5"' in text
    assert "workflow_dispatch:" in text
    assert "observation_date:" in text
    assert "minimum_records:" in text


def test_po11_workflow_runs_po10_automation_runner() -> None:
    text = _workflow_text()

    assert "build_daily_observation_automation_artifact" in text
    assert "write_daily_observation_automation_artifact" in text
    assert "reports/daily_observation_automation/*.json" in text
    assert "po11-daily-observation-artifact" in text


def test_po11_workflow_preserves_paper_only_boundary() -> None:
    text = _workflow_text()

    assert "live_trading_authorized" in text
    assert "broker_execution_mode" in text
    assert "paper_only" in text
    assert "PO11 must not authorize live trading" in text
    assert "PO11 must remain paper_only" in text


def test_po11_workflow_uses_read_only_permissions() -> None:
    text = _workflow_text()

    assert "permissions:" in text
    assert "contents: read" in text
    assert "contents: write" not in text


def test_po11_workflow_does_not_reference_live_broker_or_secrets() -> None:
    text = _workflow_text().lower()

    forbidden_tokens = (
        "contents: write",
        "alpaca_api_key",
        "alpaca_secret",
        "broker_secret",
        "live_trading_authorized=true",
        "broker_execution_mode=live",
    )

    for token in forbidden_tokens:
        assert token not in text
