import json
import subprocess
import sys
from pathlib import Path

import pytest

from src.operations.manual_portfolio_sync import (
    ManualPortfolioSyncError,
    build_manual_portfolio_state,
    load_manual_portfolio_snapshot,
    write_manual_portfolio_sync_outputs,
)


def _write_snapshot(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_manual_portfolio_sync_calculates_risk_fields(tmp_path: Path):
    snapshot_path = tmp_path / "snapshot.json"
    _write_snapshot(
        snapshot_path,
        {
            "equity_start": 100000,
            "equity_peak": 105000,
            "equity_previous_close": 102000,
            "equity_current": 100000,
            "cash": 90000,
            "positions": [
                {
                    "symbol": "spy",
                    "quantity": 10,
                    "market_value": 5200,
                    "unrealized_pnl": 100,
                }
            ],
        },
    )

    snapshot = load_manual_portfolio_snapshot(snapshot_path)
    result = build_manual_portfolio_state(snapshot)

    assert result.portfolio_state["drawdown_percent"] == 4.7619
    assert result.portfolio_state["daily_loss_percent"] == 1.9608
    assert result.portfolio_state["open_positions"][0]["symbol"] == "SPY"
    assert result.report["broker_api_used"] is False
    assert result.report["calculated_fields"]["total_position_value"] == 5200


def test_manual_portfolio_sync_writes_state_and_reports(tmp_path: Path):
    snapshot_path = tmp_path / "snapshot.json"
    state_path = tmp_path / "data" / "portfolio_state.json"
    report_json = tmp_path / "reports" / "portfolio" / "manual.json"
    report_md = tmp_path / "reports" / "portfolio" / "manual.md"
    _write_snapshot(
        snapshot_path,
        {
            "equity_start": 100000,
            "equity_peak": 100000,
            "equity_previous_close": 100000,
            "equity_current": 100000,
            "positions": [],
        },
    )

    result = build_manual_portfolio_state(load_manual_portfolio_snapshot(snapshot_path))
    write_manual_portfolio_sync_outputs(result, state_path, report_json, report_md)

    state = json.loads(state_path.read_text(encoding="utf-8"))
    report = json.loads(report_json.read_text(encoding="utf-8"))
    markdown = report_md.read_text(encoding="utf-8")

    assert state["source"] == "manual_portfolio_sync"
    assert state["metadata"]["broker_api_used"] is False
    assert report["status"] == "PASS"
    assert "Broker API used: `false`" in markdown


def test_manual_portfolio_sync_cli_runs_from_repo_root(tmp_path: Path):
    snapshot_path = tmp_path / "snapshot.json"
    state_path = tmp_path / "portfolio_state.json"
    report_json = tmp_path / "manual.json"
    report_md = tmp_path / "manual.md"
    _write_snapshot(
        snapshot_path,
        {
            "equity_start": 100000,
            "equity_peak": 100000,
            "equity_previous_close": 100000,
            "equity_current": 99500,
            "positions": [],
        },
    )

    repo_root = Path(__file__).resolve().parents[1]
    completed = subprocess.run(
        [
            sys.executable,
            "scripts/sync_manual_portfolio_state.py",
            "--snapshot",
            str(snapshot_path),
            "--portfolio-state-out",
            str(state_path),
            "--report-json-out",
            str(report_json),
            "--report-md-out",
            str(report_md),
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr
    assert "manual_portfolio_sync_completed" in completed.stdout
    assert json.loads(state_path.read_text(encoding="utf-8"))["daily_loss_percent"] == 0.5


def test_manual_portfolio_sync_rejects_missing_required_equity_field(tmp_path: Path):
    snapshot_path = tmp_path / "snapshot.json"
    _write_snapshot(
        snapshot_path,
        {
            "equity_start": 100000,
            "equity_peak": 100000,
            "equity_current": 100000,
            "positions": [],
        },
    )

    with pytest.raises(ManualPortfolioSyncError, match="missing_required_field:equity_previous_close"):
        load_manual_portfolio_snapshot(snapshot_path)


def test_manual_portfolio_sync_rejects_invalid_position_side(tmp_path: Path):
    snapshot_path = tmp_path / "snapshot.json"
    _write_snapshot(
        snapshot_path,
        {
            "equity_start": 100000,
            "equity_peak": 100000,
            "equity_previous_close": 100000,
            "equity_current": 100000,
            "positions": [
                {
                    "symbol": "SPY",
                    "quantity": 1,
                    "market_value": 500,
                    "side": "unknown",
                }
            ],
        },
    )

    with pytest.raises(ManualPortfolioSyncError, match="position_0:invalid_side"):
        load_manual_portfolio_snapshot(snapshot_path)


def test_manual_portfolio_sync_warns_when_peak_is_below_current(tmp_path: Path):
    snapshot_path = tmp_path / "snapshot.json"
    _write_snapshot(
        snapshot_path,
        {
            "equity_start": 100000,
            "equity_peak": 99000,
            "equity_previous_close": 100000,
            "equity_current": 101000,
            "positions": [],
        },
    )

    result = build_manual_portfolio_state(load_manual_portfolio_snapshot(snapshot_path))

    assert result.portfolio_state["drawdown_percent"] == 0.0
    assert "equity_peak_below_current_equity_adjusted_for_drawdown_reference" in result.warnings
