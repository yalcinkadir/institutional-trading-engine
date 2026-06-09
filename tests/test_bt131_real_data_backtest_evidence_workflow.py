from __future__ import annotations

from pathlib import Path

WORKFLOW_PATH = Path(".github/workflows/bt131_real_data_backtest_evidence.yml")


def _workflow_text() -> str:
    return WORKFLOW_PATH.read_text(encoding="utf-8")


def test_bt131_workflow_exists_and_supports_manual_dispatch() -> None:
    text = _workflow_text()

    assert WORKFLOW_PATH.exists()
    assert "workflow_dispatch:" in text
    for input_name in ("symbols", "start_date", "end_date", "run_id", "strategy_version", "plans_file"):
        assert f"{input_name}:" in text


def test_bt131_workflow_uses_python_311_and_read_only_permissions() -> None:
    text = _workflow_text()

    assert "python-version: \"3.11\"" in text
    assert "permissions:" in text
    assert "contents: read" in text
    assert "contents: write" not in text
    assert "persist-credentials: false" in text


def test_bt131_workflow_orchestrates_real_data_gates_in_order() -> None:
    text = _workflow_text()

    ingestion = text.index("Ingest historical Polygon bars when API key is available")
    bt9 = text.index("Run BT9 input-pack gate")
    runner = text.index("Run real-data historical entry/exit backtest")
    gate = text.index("Validate accepted real-data evidence when backtest passed")

    assert ingestion < bt9 < runner < gate
    assert "scripts/ingest_historical_polygon.py" in text
    assert "scripts/validate_bt9_real_historical_input_pack.py" in text
    assert "scripts/run_historical_entry_exit_backtest.py" in text
    assert "scripts/validate_real_data_backtest_evidence_gate.py" in text


def test_bt131_workflow_forces_real_data_and_blocks_demo_claims() -> None:
    text = _workflow_text()

    assert "--real-data" in text
    assert "--data-source real_data" in text
    assert "data_source=real_data" in text
    assert "must not be demo" in text
    assert "historical_demo" not in text


def test_bt131_workflow_accepts_blocked_artifact_path_without_fake_success() -> None:
    text = _workflow_text()

    assert "Backtest did not pass; expecting explicit BLOCKED evidence artifact." in text
    assert "test -f reports/backtests/real-data-backtest-evidence.json" in text
    assert "run_health_status" in text
    assert "input_pack_gate_status" in text


def test_bt131_workflow_uploads_reviewable_evidence_artifacts() -> None:
    text = _workflow_text()

    assert "actions/upload-artifact@v4" in text
    assert "bt131-real-data-backtest-evidence" in text
    assert "reports/backtests/*.json" in text
    assert "reports/backtests/*.md" in text
    assert "retention-days: 90" in text


def test_bt131_workflow_preserves_research_only_safety_boundary() -> None:
    text = _workflow_text()

    assert "live_trading_authorized" in text
    assert "broker_execution_mode" in text
    assert "paper_only" in text
    forbidden_tokens = (
        "alpaca_api_key",
        "alpaca_secret",
        "broker_secret",
        "broker_execution_mode=live",
        "live_trading_authorized=true",
    )
    lower = text.lower()
    for token in forbidden_tokens:
        assert token not in lower
