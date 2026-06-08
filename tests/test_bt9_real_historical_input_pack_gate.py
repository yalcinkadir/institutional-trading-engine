from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from scripts.validate_bt9_real_historical_input_pack import validate_bt9_input_pack

VALIDATOR_SCRIPT = Path("scripts/validate_bt9_real_historical_input_pack.py")
RUNNER_SCRIPT = Path("scripts/run_historical_entry_exit_backtest.py")


def _write_trade_plans(path: Path) -> None:
    path.write_text(
        json.dumps(
            {
                "plans": [
                    {
                        "signal_id": "bt9-plan-1",
                        "symbol": "SPY",
                        "signal_date": "2026-06-01",
                        "entry_trigger": 101.0,
                        "stop_loss": 99.0,
                        "target_1": 104.0,
                        "action": "BUY_WATCH",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )


def _write_universe(path: Path) -> None:
    path.write_text(
        "symbol,effective_from,effective_to,active,asset_class,exchange,source,status,reason\n"
        "SPY,2024-01-01,,true,etf,NYSEARCA,initial_universe,active,initial test universe\n",
        encoding="utf-8",
    )


def _write_bars(root: Path) -> None:
    root.mkdir(parents=True, exist_ok=True)
    (root / "SPY.csv").write_text(
        "date,open,high,low,close,volume\n"
        "2026-06-01,100,100,99,100,1000000\n"
        "2026-06-02,101,105,100,104,1100000\n",
        encoding="utf-8",
    )


def test_bt9_input_pack_passes_with_valid_files(tmp_path: Path) -> None:
    universe = tmp_path / "universe.csv"
    bars = tmp_path / "bars"
    plans = tmp_path / "plans.json"
    _write_universe(universe)
    _write_bars(bars)
    _write_trade_plans(plans)

    report = validate_bt9_input_pack(universe_path=universe, bars_root=bars, trade_plans_path=plans)

    assert report.passed is True
    assert report.failures == []


def test_bt9_input_pack_fails_when_files_are_missing(tmp_path: Path) -> None:
    report = validate_bt9_input_pack(
        universe_path=tmp_path / "missing-universe.csv",
        bars_root=tmp_path / "missing-bars",
        trade_plans_path=tmp_path / "missing-plans.json",
    )

    assert report.passed is False
    assert "missing_universe_file" in report.failures
    assert "missing_bars_root" in report.failures
    assert "missing_trade_plans_file" in report.failures


def test_bt9_validator_cli_fails_closed_when_pack_missing(tmp_path: Path) -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(VALIDATOR_SCRIPT),
            "--universe",
            str(tmp_path / "missing-universe.csv"),
            "--bars-root",
            str(tmp_path / "missing-bars"),
            "--trade-plans",
            str(tmp_path / "missing-plans.json"),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    assert "BT9 real historical input pack gate status: FAIL" in result.stdout
    assert "missing_universe_file" in result.stdout
    assert "missing_trade_plans_file" in result.stdout


def test_bt9_runner_fails_closed_and_writes_blocked_evidence_when_pack_missing(tmp_path: Path) -> None:
    plans = tmp_path / "plans.json"
    json_output = tmp_path / "blocked-evidence.json"
    markdown_output = tmp_path / "blocked-evidence.md"
    _write_trade_plans(plans)

    result = subprocess.run(
        [
            sys.executable,
            str(RUNNER_SCRIPT),
            "--plans-file",
            str(plans),
            "--bars-root",
            str(tmp_path / "missing-bars"),
            "--universe",
            str(tmp_path / "missing-universe.csv"),
            "--real-data",
            "--json-output",
            str(json_output),
            "--markdown-output",
            str(markdown_output),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    assert "BT9 real historical input pack gate status: FAIL" in result.stdout
    assert json_output.exists()
    assert markdown_output.exists()
    payload = json.loads(json_output.read_text(encoding="utf-8"))
    assert payload["data_source"] == "real_data"
    assert payload["is_demo"] is False
    assert payload["input_pack_gate_status"] == "FAILED"
    assert payload["input_completeness_status"] == "BLOCKED_INPUT_PACK"
    assert payload["run_health_status"] == "BLOCKED"
