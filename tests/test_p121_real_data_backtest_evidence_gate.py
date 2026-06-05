from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from scripts.validate_real_data_backtest_evidence_gate import validate_real_data_backtest_evidence_artifact

VALIDATOR_SCRIPT = Path("scripts/validate_real_data_backtest_evidence_gate.py")
RUNNER_SCRIPT = Path("scripts/run_historical_entry_exit_backtest.py")


def _valid_real_payload() -> dict:
    return {
        "run_id": "real-bt-2026-06-05-001",
        "data_source": "real_data",
        "is_demo": False,
        "symbol_universe": ["SPY", "QQQ"],
        "date_range": {"start": "2024-06-01", "end": "2026-06-01"},
        "strategy_version": "historical-entry-exit-v1",
        "metrics": {"total": 2, "expectancy_r": 0.42},
        "results": [{"signal_id": "sig_1", "symbol": "SPY", "r_multiple": 1.0}],
        "tags": ["real_data", "research_only"],
    }


def _write_plan(path: Path) -> None:
    path.write_text(
        json.dumps(
            {
                "plans": [
                    {
                        "signal_id": "sig_SPY_real_001",
                        "symbol": "SPY",
                        "signal_date": "2026-06-01",
                        "entry_trigger": 101.0,
                        "stop_loss": 99.0,
                        "target_1": 104.0,
                        "target_2": 106.0,
                        "valid_until": "2026-06-04",
                        "entry_type": "breakout",
                        "setup_type": "momentum_breakout",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )


def _write_bars(root: Path) -> None:
    root.mkdir(parents=True, exist_ok=True)
    (root / "SPY.csv").write_text(
        "date,open,high,low,close,volume\n"
        "2026-06-01,100,100,99,100,1000000\n"
        "2026-06-02,101,105,100,104,1100000\n"
        "2026-06-03,104,106,103,105,1200000\n",
        encoding="utf-8",
    )


def test_p121_valid_real_data_backtest_evidence_passes(tmp_path: Path) -> None:
    artifact = tmp_path / "real-data-backtest-evidence.json"
    artifact.write_text(json.dumps(_valid_real_payload()), encoding="utf-8")

    gate = validate_real_data_backtest_evidence_artifact(artifact)

    assert gate.passed is True
    assert gate.missing_fields == []
    assert gate.invalid_fields == []


def test_p121_demo_backtest_cannot_pass_as_real_evidence(tmp_path: Path) -> None:
    payload = _valid_real_payload()
    payload["data_source"] = "historical_demo"
    payload["is_demo"] = True
    payload["tags"] = ["demo", "public_safe"]
    artifact = tmp_path / "demo-backtest.json"
    artifact.write_text(json.dumps(payload), encoding="utf-8")

    gate = validate_real_data_backtest_evidence_artifact(artifact)

    assert gate.passed is False
    assert "data_source" in gate.invalid_fields
    assert "is_demo" in gate.invalid_fields
    assert "demo_marker" in gate.invalid_fields


def test_p121_missing_date_range_fails_schema(tmp_path: Path) -> None:
    payload = _valid_real_payload()
    del payload["date_range"]
    artifact = tmp_path / "missing-date-range.json"
    artifact.write_text(json.dumps(payload), encoding="utf-8")

    gate = validate_real_data_backtest_evidence_artifact(artifact)

    assert gate.passed is False
    assert gate.missing_fields == ["date_range"]


def test_p121_real_data_runner_writes_valid_evidence_artifact(tmp_path: Path) -> None:
    plans = tmp_path / "plans.json"
    bars_root = tmp_path / "bars"
    output_json = tmp_path / "real-data-backtest-evidence.json"
    output_md = tmp_path / "real-data-backtest-evidence.md"
    _write_plan(plans)
    _write_bars(bars_root)

    result = subprocess.run(
        [
            sys.executable,
            str(RUNNER_SCRIPT),
            "--plans-file",
            str(plans),
            "--bars-root",
            str(bars_root),
            "--run-id",
            "real-bt-runner-001",
            "--real-data",
            "--json-output",
            str(output_json),
            "--markdown-output",
            str(output_md),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert output_json.exists()
    assert output_md.exists()
    payload = json.loads(output_json.read_text(encoding="utf-8"))
    assert payload["run_id"] == "real-bt-runner-001"
    assert payload["data_source"] == "real_data"
    assert payload["is_demo"] is False
    assert payload["symbol_universe"] == ["SPY"]
    assert payload["strategy_version"] == "historical-entry-exit-v1"
    assert validate_real_data_backtest_evidence_artifact(output_json).passed is True


def test_p121_validator_cli_fails_when_artifact_missing(tmp_path: Path) -> None:
    result = subprocess.run(
        [sys.executable, str(VALIDATOR_SCRIPT), "--artifact", str(tmp_path / "missing.json")],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    assert "Real-data backtest evidence gate status: FAIL" in result.stdout
    assert "artifact_missing" in result.stdout
