from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

from scripts.validate_real_data_backtest_evidence_gate import validate_real_data_backtest_evidence_artifact
from src.backtesting.historical_entry_exit_backtest import load_trade_plans_with_report

RUNNER_SCRIPT = Path("scripts/run_historical_entry_exit_backtest.py")
PIPELINE_METADATA = {
    "pipeline_coupled": True,
    "pipeline_generation_source": "scanner_signal_quality_validator",
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


def _write_plan(path: Path, *, valid: bool = True, unsupported_action: bool = False) -> None:
    plan = {
        "signal_id": "sig_SPY_bt130",
        "symbol": "SPY",
        "signal_date": "2026-06-01",
        "entry_trigger": 101.0,
        "target_1": 104.0,
        "source": "paper_observation_validated",
    }
    if valid or unsupported_action:
        plan["stop_loss"] = 99.0
    if unsupported_action:
        plan["action"] = "SELL"
    path.write_text(json.dumps({"metadata": PIPELINE_METADATA, "plans": [plan]}), encoding="utf-8")


def _write_bars(root: Path) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    path = root / "SPY.csv"
    path.write_text(
        "date,open,high,low,close,volume\n"
        "2026-06-01,100,100,99,100,1000000\n"
        "2026-06-02,101,105,100,104,1100000\n",
        encoding="utf-8",
    )
    return path


def _write_universe(path: Path) -> None:
    path.write_text(
        "symbol,effective_from,effective_to,active,asset_class,exchange,source,status,reason\n"
        "SPY,2024-01-01,,true,etf,NYSEARCA,initial_universe,active,initial test universe\n",
        encoding="utf-8",
    )


def _write_coverage(path: Path, *, bars_path: Path) -> None:
    path.write_text(
        json.dumps(
            {
                "vendor": "polygon",
                "generated_at": "2026-06-11T00:00:00Z",
                "multiplier": 1,
                "timespan": "day",
                "requested_start_date": "2026-06-01",
                "requested_end_date": "2026-06-02",
                "symbol_count": 1,
                "ok_symbol_count": 1,
                "status": "ok",
                "missing_data_summary": [],
                "symbols": [
                    {
                        "symbol": "SPY",
                        "start_date": "2026-06-01",
                        "end_date": "2026-06-02",
                        "bar_count": 2,
                        "rows_fetched": 2,
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


def test_bt130_loader_reports_rejected_trade_plan_reasons(tmp_path: Path) -> None:
    plans_file = tmp_path / "plans.json"
    _write_plan(plans_file, valid=False)

    result = load_trade_plans_with_report(plans_file)

    assert result.report.input_plan_count == 1
    assert result.report.accepted_plan_count == 0
    assert result.report.rejected_plan_count == 1
    assert result.report.rejection_reasons[0].reasons == ["missing_stop_loss"]


def test_bt130_real_data_runner_blocks_missing_coverage_manifest(tmp_path: Path) -> None:
    plans = tmp_path / "plans.json"
    bars = tmp_path / "bars"
    universe = tmp_path / "universe.csv"
    out = tmp_path / "evidence.json"
    _write_plan(plans)
    _write_bars(bars)
    _write_universe(universe)

    result = subprocess.run(
        [
            sys.executable,
            str(RUNNER_SCRIPT),
            "--plans-file", str(plans),
            "--bars-root", str(bars),
            "--universe", str(universe),
            "--coverage-manifest", str(tmp_path / "missing.json"),
            "--real-data",
            "--json-output", str(out),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    assert "missing_coverage_manifest" in result.stdout
    assert out.exists()
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["data_source"] == "real_data"
    assert payload["is_demo"] is False
    assert payload["input_pack_gate_status"] == "FAILED"
    assert payload["input_completeness_status"] == "BLOCKED_INPUT_PACK"
    assert payload["run_health_status"] == "BLOCKED"
    assert any("missing_coverage_manifest" in item["reasons"] for item in payload["rejection_reasons"])


def test_bt130_real_data_runner_blocks_fully_rejected_plans(tmp_path: Path) -> None:
    plans = tmp_path / "plans.json"
    bars = tmp_path / "bars"
    universe = tmp_path / "universe.csv"
    coverage = tmp_path / "coverage.json"
    out = tmp_path / "evidence.json"
    _write_plan(plans, unsupported_action=True)
    bars_path = _write_bars(bars)
    _write_universe(universe)
    _write_coverage(coverage, bars_path=bars_path)

    result = subprocess.run(
        [
            sys.executable,
            str(RUNNER_SCRIPT),
            "--plans-file", str(plans),
            "--bars-root", str(bars),
            "--universe", str(universe),
            "--coverage-manifest", str(coverage),
            "--real-data",
            "--json-output", str(out),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    assert "accepted_plan_count=0" in result.stdout
    assert out.exists()
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["data_source"] == "real_data"
    assert payload["is_demo"] is False
    assert payload["input_pack_gate_status"] == "PASSED"
    assert payload["input_completeness_status"] == "EMPTY_INPUT"
    assert payload["run_health_status"] == "BLOCKED"
    assert payload["input_checksums"] == {bars_path.as_posix(): _sha256(bars_path)}
    assert payload["input_plan_count"] == 1
    assert payload["accepted_plan_count"] == 0
    assert payload["rejected_plan_count"] == 1


def test_bt130_evidence_gate_rejects_plan_count_mismatch(tmp_path: Path) -> None:
    artifact = tmp_path / "bad-counts.json"
    artifact.write_text(
        json.dumps(
            {
                "run_id": "bad-counts",
                "data_source": "real_data",
                "is_demo": False,
                "symbol_universe": ["SPY"],
                "date_range": {"start": "2026-06-01", "end": "2026-06-02"},
                "strategy_version": "historical-entry-exit-v1",
                "input_pack_gate_status": "PASSED",
                "input_completeness_status": "OK",
                "run_health_status": "OK",
                "coverage_manifest_path": "coverage.json",
                "survivorship_universe_path": "universe.csv",
                "trade_plans_path": "plans.json",
                "input_checksums": {"bars/SPY.csv": "a" * 64},
                "input_plan_count": 2,
                "accepted_plan_count": 2,
                "rejected_plan_count": 1,
                "rejection_reasons": [],
                "metrics": {"total": 2},
                "results": [{"signal_id": "sig"}],
                "live_trading_authorized": False,
                "broker_execution_mode": "paper_only",
            }
        ),
        encoding="utf-8",
    )

    gate = validate_real_data_backtest_evidence_artifact(artifact)

    assert gate.passed is False
    assert "plan_count_mismatch" in gate.invalid_fields
    assert "rejection_reason_count_mismatch" in gate.invalid_fields
