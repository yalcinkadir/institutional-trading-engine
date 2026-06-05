from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from scripts.validate_real_data_backtest_evidence_gate import validate_real_data_backtest_evidence_artifact

VALIDATOR_SCRIPT = Path("scripts/validate_real_data_backtest_evidence_gate.py")


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
