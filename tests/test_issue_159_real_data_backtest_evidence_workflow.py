from __future__ import annotations

from pathlib import Path


WORKFLOW_PATH = Path(".github/workflows/real-data-backtest-evidence.yml")


def _workflow() -> str:
    return WORKFLOW_PATH.read_text(encoding="utf-8")


def test_real_data_backtest_evidence_workflow_runs_real_data_runner() -> None:
    workflow = _workflow()

    assert "name: Real Data Backtest Evidence" in workflow
    assert "workflow_dispatch:" in workflow
    assert "python scripts/run_historical_entry_exit_backtest.py" in workflow
    assert "--real-data" in workflow
    assert "--data-source real_data" in workflow
    assert "--json-output reports/backtests/real-data-backtest-evidence.json" in workflow
    assert "--markdown-output reports/backtests/real-data-backtest-evidence.md" in workflow


def test_real_data_backtest_evidence_workflow_uploads_required_artifacts_fail_loudly() -> None:
    workflow = _workflow()

    assert "Upload real-data backtest evidence pack" in workflow
    assert "if-no-files-found: error" in workflow
    assert "reports/backtests/real-data-backtest-evidence.json" in workflow
    assert "reports/backtests/real-data-backtest-evidence.md" in workflow
    assert "reports/backtests/real-data-backtest-exit-code.txt" in workflow


def test_real_data_backtest_evidence_workflow_fails_after_blocked_artifact_upload() -> None:
    workflow = _workflow()

    upload_index = workflow.index("Upload real-data backtest evidence pack")
    fail_index = workflow.index("Fail workflow when real-data backtest is blocked or failed")

    assert upload_index < fail_index
    assert "steps.backtest.outputs.exit_code != '0'" in workflow
    assert "Review uploaded artifact" in workflow
