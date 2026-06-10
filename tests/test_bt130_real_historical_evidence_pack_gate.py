from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from scripts.validate_real_data_backtest_evidence_gate import validate_real_data_backtest_evidence_artifact
from src.backtesting.historical_entry_exit_backtest import load_trade_plans_with_report

RUNNER_SCRIPT = Path("scripts/run_historical_entry_exit_backtest.py")


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
    path.write_text(json.dumps({"plans": [plan]}), encoding="utf-8")


def _write_bars(root: Path) -> None:
    root.mkdir(parents=True, exist_ok=True)
    (root / "SPY.csv").write_text(
        "date,open,high,low,close,volume\n"
        "2026-06-01,100,100,99,100,1000000\n"
        "2026-06-02,101,105,100,104,1100000\n",
        encoding="utf-8",
    )


def _write_universe(path: Path) -> None:
    path.write_text(
        "symbol,effective_from,effective_to,active,asset_class,exchange,source,status,reason\n"
        "SPY,2024-01-01,,true,etf,NYSEARCA,initial_universe,active,initial test universe\n",
        encoding="utf-8",
    )


def _write_coverage(path: Path) -> None:
    path.write_text(json.dumps({"source": "polygon", "symbols": ["SPY"]}), encoding="utf-8")


def _capacity_snapshot(*, trade_count: int) -> dict:
    return {
        "run_id": f"real-data-{trade_count}-trades",
        "strategy_id": "historical-entry-exit-v1",
        "dataset_id": "real-data-polygon-bt130",
        "parameter_version": "p179-real-data-min-trade-gate",
        "evidence_type": "capacity_turnover_realism",
        "proposed_capital_usd": 100000.0,
        "symbol_count": 2,
        "metrics": {
            "median_adv_usd": 75000000.0,
            "max_position_adv_pct": 1.25,
            "portfolio_adv_pct": 8.5,
            "average_daily_turnover_pct": 12.0,
            "annual_turnover_pct": 620.0,
            "round_trip_cost_bps": 7.5,
            "gross_expectancy_bps": 28.0,
            "net_expectancy_bps": 20.5,
            "average_holding_days": 4.2,
            "trade_count": trade_count,
            "slippage_model_coverage_pct": 100.0,
        },
        "artifact_hashes": {
            "real_data_backtest_evidence": "sha256:real-data-backtest-evidence",
            "capacity_turnover_snapshot": "sha256:capacity-turnover-snapshot",
        },
        "tags": ["real_data", "public_safe", "research_only"],
        "footer": "Research / Paper Observation Only. Execution is not authorized by this report.",
    }


def _real_data_evidence_payload(*, trade_count: int, status: str | None = None) -> dict:
    payload = {
        "run_id": f"real-data-{trade_count}-trades",
        "data_source": "real_data",
        "is_demo": False,
        "symbol_universe": ["SPY", "QQQ"],
        "date_range": {"start": "2024-01-01", "end": "2026-06-01"},
        "strategy_version": "historical-entry-exit-v1",
        "input_pack_gate_status": "PASSED",
        "input_completeness_status": "OK",
        "run_health_status": "OK",
        "sample_quality_status": "REVIEWABLE_SAMPLE" if trade_count >= 30 else "INSUFFICIENT_SAMPLE",
        "min_trade_count": 30,
        "coverage_manifest_path": "coverage.json",
        "survivorship_universe_path": "universe.csv",
        "trade_plans_path": "plans.json",
        "input_plan_count": trade_count,
        "accepted_plan_count": trade_count,
        "rejected_plan_count": 0,
        "rejection_reasons": [],
        "metrics": {"total": trade_count, "trade_count": trade_count, "expectancy_r": 0.12},
        "results": [{"signal_id": f"sig_{index}", "symbol": "SPY"} for index in range(trade_count)],
        "capacity_turnover_snapshot": _capacity_snapshot(trade_count=trade_count),
        "tags": ["real_data", "research_only"],
        "live_trading_authorized": False,
        "broker_execution_mode": "paper_only",
    }
    if status is not None:
        payload["evidence_status"] = status
    return payload


def test_bt130_loader_reports_rejected_trade_plan_reasons(tmp_path: Path) -> None:
    plans_file = tmp_path / "plans.json"
    _write_plan(plans_file, valid=False)

    result = load_trade_plans_with_report(plans_file)

    assert result.report.input_plan_count == 1
    assert result.report.accepted_plan_count == 0
    assert result.report.rejected_plan_count == 1
    assert result.report.rejection_reasons[0].reasons == ["missing_stop_loss"]


def test_p179_real_data_24_trade_evidence_fails_insufficient_sample_gate(tmp_path: Path) -> None:
    artifact = tmp_path / "real-data-24-trades.json"
    artifact.write_text(json.dumps(_real_data_evidence_payload(trade_count=24)), encoding="utf-8")

    gate = validate_real_data_backtest_evidence_artifact(artifact)

    assert gate.passed is False
    assert gate.observed_trade_count == 24
    assert gate.min_trade_count == 30
    assert gate.sample_quality_status == "INSUFFICIENT_SAMPLE"
    assert "insufficient_sample" in gate.invalid_fields
    assert "capacity_turnover_realism_gate" in gate.invalid_fields
    assert any("trade_count_floor" in failure for failure in gate.capacity_turnover_failures)


def test_p179_insufficient_sample_cannot_claim_ready_for_review(tmp_path: Path) -> None:
    artifact = tmp_path / "real-data-24-ready-for-review.json"
    payload = _real_data_evidence_payload(trade_count=24, status="READY_FOR_REVIEW")
    payload["sample_quality_status"] = "REVIEWABLE_SAMPLE"
    artifact.write_text(json.dumps(payload), encoding="utf-8")

    gate = validate_real_data_backtest_evidence_artifact(artifact)

    assert gate.passed is False
    assert "insufficient_sample" in gate.invalid_fields
    assert "sample_quality_status" in gate.invalid_fields
    assert "evidence_status_sample_size_mismatch" in gate.invalid_fields
    assert "capacity_turnover_realism_gate" in gate.invalid_fields


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
    assert payload["input_pack_gate_status"] == "PASSED"
    assert payload["input_completeness_status"] == "BLOCKED_MISSING_COVERAGE_MANIFEST"
    assert payload["run_health_status"] == "BLOCKED"
    assert payload["sample_quality_status"] == "INSUFFICIENT_SAMPLE"
    assert payload["rejection_reasons"][0]["reasons"] == ["missing_coverage_manifest"]


def test_bt130_real_data_runner_blocks_fully_rejected_plans(tmp_path: Path) -> None:
    plans = tmp_path / "plans.json"
    bars = tmp_path / "bars"
    universe = tmp_path / "universe.csv"
    coverage = tmp_path / "coverage.json"
    out = tmp_path / "evidence.json"
    _write_plan(plans, unsupported_action=True)
    _write_bars(bars)
    _write_universe(universe)
    _write_coverage(coverage)

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
    assert payload["sample_quality_status"] == "INSUFFICIENT_SAMPLE"
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
                "sample_quality_status": "INSUFFICIENT_SAMPLE",
                "min_trade_count": 30,
                "coverage_manifest_path": "coverage.json",
                "survivorship_universe_path": "universe.csv",
                "trade_plans_path": "plans.json",
                "input_plan_count": 2,
                "accepted_plan_count": 2,
                "rejected_plan_count": 1,
                "rejection_reasons": [],
                "metrics": {"total": 2},
                "results": [{"signal_id": "sig"}],
                "capacity_turnover_snapshot": _capacity_snapshot(trade_count=2),
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
    assert "capacity_turnover_realism_gate" in gate.invalid_fields
