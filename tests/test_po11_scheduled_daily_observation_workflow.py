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
    assert "selected_symbols:" in text


def test_po11_manual_dispatch_inputs_are_prefilled() -> None:
    text = _workflow_text()

    assert 'default: "auto"' in text
    assert 'default: "1"' in text
    assert 'default: "MSFT,NVDA,META,AAPL,MU,QQQ,GLD,SLV"' in text
    assert 'Observation date in YYYY-MM-DD format, or auto for current UTC date.' in text
    assert "if [ \"$observation_date\" = \"auto\" ]; then" in text
    assert 'raw_observation_date = os.environ.get("OBSERVATION_DATE") or "auto"' in text


def test_po11_workflow_sets_pythonpath_for_src_imports() -> None:
    text = _workflow_text()

    assert "PYTHONPATH: ${{ github.workspace }}" in text


def test_po11_workflow_runs_p166_producer_before_po10_automation_runner() -> None:
    text = _workflow_text()

    producer_index = text.index("Produce P166 daily observation evidence")
    automation_index = text.index("Run PO10 daily observation automation")

    assert producer_index < automation_index
    assert "scripts/produce_daily_observation_evidence_p166.py" in text
    assert "reports/daily_evidence/*.json" in text
    assert "p166-daily-observation-evidence" in text


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
    assert "persist-credentials: false" in text


def test_po11_workflow_passes_vix_proxy_configuration() -> None:
    text = _workflow_text()

    assert "VOLATILITY_PROXY_SYMBOL" in text
    assert "VIXY" in text


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
