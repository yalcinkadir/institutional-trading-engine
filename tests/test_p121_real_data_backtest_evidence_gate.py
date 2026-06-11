from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

from scripts.validate_real_data_backtest_evidence_gate import validate_real_data_backtest_evidence_artifact

VALIDATOR_SCRIPT = Path("scripts/validate_real_data_backtest_evidence_gate.py")
RUNNER_SCRIPT = Path("scripts/run_historical_entry_exit_backtest.py")
PIPELINE_METADATA = {
    "pipeline_coupled": True,
    "pipeline_generation_source": "scanner_signal_quality_validator_fixture",
    "generated_signal_count": 1,
    "validated_trade_plan_count": 1,
    "blocked_signal_count": 0,
    "runtime_gates_applied": [
        "scanner",
        "signal_generator",
        "quality_fusion",
        "trade_plan_validator",
    ],
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _valid_real_payload() -> dict:
    payload = {
        "run_id": "real-bt-2026-06-05-001",
        "data_source": "real_data",
        "is_demo": False,
        "symbol_universe": ["SPY", "QQQ"],
        "date_range": {"start": "2024-06-01", "end": "2026-06-01"},
        "strategy_version": "historical-entry-exit-v1",
        "input_pack_gate_status": "PASSED",
        "input_completeness_status": "OK",
        "run_health_status": "OK",
        "coverage_manifest_path": "coverage_manifest.json",
        "survivorship_universe_path": "survivorship_universe.csv",
        "trade_plans_path": "historical_trade_plans.json",
        "input_checksums": {"bars/SPY.csv": "a" * 64},
        "input_plan_count": 1,
        "accepted_plan_count": 1,
        "rejected_plan_count": 0,
        "rejection_reasons": [],
        "metrics": {"total": 1, "expectancy_r": 0.42},
        "results": [{"signal_id": "sig_1", "symbol": "SPY", "r_multiple": 1.0}],
        "tags": ["real_data", "research_only"],
        "live_trading_authorized": False,
        "broker_execution_mode": "paper_only",
    }
    payload.update(PIPELINE_METADATA)
    return payload


def _write_plan(path: Path) -> None:
    path.write_text(
        json.dumps(
            {
                "metadata": PIPELINE_METADATA,
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
                        "source": "paper_observation_validated",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )


def _write_bars(root: Path) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    path = root / "SPY.csv"
    path.write_text(
        "date,open,high,low,close,volume\n"
        "2026-06-01,100,100,99,100,1000000\n"
        "2026-06-02,101,105,100,104,1100000\n"
        "2026-06-03,104,106,103,105,1200000\n",
        encoding="utf-8",
    )
    return path


def _write_universe(path: Path) -> None:
    path.write_text(
        "symbol,effective_from,effective_to,active,asset_class,exchange,source,status,reason\n"
        "SPY,2024-01-01,,true,etf,NYSEARCA,initial_universe,active,initial test universe\n",
        encoding="utf-8",
    )


def _write_coverage_manifest(path: Path, *, bars_path: Path) -> None:
    path.write_text(
        json.dumps(
            {
                "vendor": "polygon",
                "generated_at": "2026-06-11T00:00:00Z",
                "multiplier": 1,
                "timespan": "day",
                "requested_start_date": "2026-06-01",
                "requested_end_date": "2026-06-03",
                "symbol_count": 1,
                "ok_symbol_count": 1,
                "status": "ok",
                "missing_data_summary": [],
                "symbols": [
                    {
                        "symbol": "SPY",
                        "start_date": "2026-06-01",
                        "end_date": "2026-06-03",
                        "bar_count": 3,
                        "rows_fetched": 3,
                        "status": "ok",
                        "output_path": bars_path.as_posix(),
                        "output_sha256": _sha256(bars_path),
                        "missing_data_summary": [],
                    }
                ],
            }
        ),
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
    universe = tmp_path / "universe.csv"
    coverage_manifest = tmp_path / "coverage_manifest.json"
    output_json = tmp_path / "real-data-backtest-evidence.json"
    output_md = tmp_path / "real-data-backtest-evidence.md"
    _write_plan(plans)
    bars_path = _write_bars(bars_root)
    _write_universe(universe)
    _write_coverage_manifest(coverage_manifest, bars_path=bars_path)

    result = subprocess.run(
        [
            sys.executable,
            str(RUNNER_SCRIPT),
            "--plans-file",
            str(plans),
            "--bars-root",
            str(bars_root),
            "--universe",
            str(universe),
            "--coverage-manifest",
            str(coverage_manifest),
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

    assert result.returncode == 0, result.stdout + result.stderr
    assert output_json.exists()
    assert output_md.exists()
    payload = json.loads(output_json.read_text(encoding="utf-8"))
    assert payload["run_id"] == "real-bt-runner-001"
    assert payload["data_source"] == "real_data"
    assert payload["is_demo"] is False
    assert payload["symbol_universe"] == ["SPY"]
    assert payload["strategy_version"] == "historical-entry-exit-v1"
    assert payload["input_pack_gate_status"] == "PASSED"
    assert payload["input_completeness_status"] == "OK"
    assert payload["run_health_status"] == "OK"
    assert payload["coverage_manifest_path"] == str(coverage_manifest)
    assert payload["input_checksums"] == {bars_path.as_posix(): _sha256(bars_path)}
    assert payload["pipeline_coupled"] is True
    assert payload["runtime_gates_applied"] == PIPELINE_METADATA["runtime_gates_applied"]
    assert payload["input_plan_count"] == 1
    assert payload["accepted_plan_count"] == 1
    assert payload["rejected_plan_count"] == 0
    assert payload["live_trading_authorized"] is False
    assert payload["broker_execution_mode"] == "paper_only"
    assert validate_real_data_backtest_evidence_artifact(output_json).passed is True
