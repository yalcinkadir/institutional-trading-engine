from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from scripts.validate_real_data_backtest_evidence_gate import validate_real_data_backtest_evidence_artifact

VALIDATOR_SCRIPT = Path("scripts/validate_real_data_backtest_evidence_gate.py")
RUNNER_SCRIPT = Path("scripts/run_historical_entry_exit_backtest.py")


def _results(count: int) -> list[dict]:
    return [
        {"signal_id": f"sig_{index}", "symbol": "SPY", "r_multiple": 1.0}
        for index in range(count)
    ]


def _capacity_snapshot(*, trade_count: int = 30, max_position_adv_pct: float = 1.25) -> dict:
    return {
        "run_id": "real-bt-2026-06-05-001",
        "strategy_id": "historical-entry-exit-v1",
        "dataset_id": "real-data-polygon-bt131",
        "parameter_version": "p179-real-data-min-trade-gate",
        "evidence_type": "capacity_turnover_realism",
        "proposed_capital_usd": 100000.0,
        "symbol_count": 2,
        "metrics": {
            "median_adv_usd": 75000000.0,
            "max_position_adv_pct": max_position_adv_pct,
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


def _valid_real_payload(*, trade_count: int = 30) -> dict:
    return {
        "run_id": "real-bt-2026-06-05-001",
        "data_source": "real_data",
        "is_demo": False,
        "symbol_universe": ["SPY", "QQQ"],
        "date_range": {"start": "2024-06-01", "end": "2026-06-01"},
        "strategy_version": "historical-entry-exit-v1",
        "input_pack_gate_status": "PASSED",
        "input_completeness_status": "OK",
        "run_health_status": "OK",
        "sample_quality_status": "REVIEWABLE_SAMPLE",
        "min_trade_count": 30,
        "coverage_manifest_path": "coverage_manifest.json",
        "survivorship_universe_path": "survivorship_universe.csv",
        "trade_plans_path": "historical_trade_plans.json",
        "input_plan_count": trade_count,
        "accepted_plan_count": trade_count,
        "rejected_plan_count": 0,
        "rejection_reasons": [],
        "metrics": {"total": trade_count, "trade_count": trade_count, "expectancy_r": 0.42},
        "results": _results(trade_count),
        "capacity_turnover_snapshot": _capacity_snapshot(trade_count=trade_count),
        "tags": ["real_data", "research_only"],
        "live_trading_authorized": False,
        "broker_execution_mode": "paper_only",
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
                        "source": "paper_observation_validated",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )


def _write_bars(root: Path, *, malformed_volume: bool = False) -> None:
    root.mkdir(parents=True, exist_ok=True)
    if malformed_volume:
        volume_rows = ["", "not_available", "0"]
    else:
        volume_rows = ["1000000", "1100000", "1200000"]
    (root / "SPY.csv").write_text(
        "date,open,high,low,close,volume\n"
        f"2026-06-01,100,100,99,100,{volume_rows[0]}\n"
        f"2026-06-02,101,105,100,104,{volume_rows[1]}\n"
        f"2026-06-03,104,106,103,105,{volume_rows[2]}\n",
        encoding="utf-8",
    )


def _write_universe(path: Path) -> None:
    path.write_text(
        "symbol,effective_from,effective_to,active,asset_class,exchange,source,status,reason\n"
        "SPY,2024-01-01,,true,etf,NYSEARCA,initial_universe,active,initial test universe\n",
        encoding="utf-8",
    )


def _write_coverage_manifest(path: Path) -> None:
    path.write_text(json.dumps({"source": "polygon", "symbols": ["SPY"]}), encoding="utf-8")


def _run_real_data_runner(
    tmp_path: Path,
    *,
    proposed_capital_usd: float | None = None,
    round_trip_cost_bps: float | None = None,
    malformed_volume: bool = False,
) -> tuple[subprocess.CompletedProcess[str], Path, Path]:
    plans = tmp_path / "plans.json"
    bars_root = tmp_path / "bars"
    universe = tmp_path / "universe.csv"
    coverage_manifest = tmp_path / "coverage_manifest.json"
    output_json = tmp_path / "real-data-backtest-evidence.json"
    output_md = tmp_path / "real-data-backtest-evidence.md"
    _write_plan(plans)
    _write_bars(bars_root, malformed_volume=malformed_volume)
    _write_universe(universe)
    _write_coverage_manifest(coverage_manifest)

    command = [
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
    ]
    if proposed_capital_usd is not None:
        command.extend(["--proposed-capital-usd", str(proposed_capital_usd)])
    if round_trip_cost_bps is not None:
        command.extend(["--round-trip-cost-bps", str(round_trip_cost_bps)])

    result = subprocess.run(command, capture_output=True, text=True, check=False)
    return result, output_json, output_md


def test_p121_valid_real_data_backtest_evidence_passes_when_sample_is_reviewable(tmp_path: Path) -> None:
    artifact = tmp_path / "real-data-backtest-evidence.json"
    artifact.write_text(json.dumps(_valid_real_payload(trade_count=30)), encoding="utf-8")

    gate = validate_real_data_backtest_evidence_artifact(artifact)

    assert gate.passed is True
    assert gate.missing_fields == []
    assert gate.invalid_fields == []
    assert gate.observed_trade_count == 30
    assert gate.sample_quality_status == "REVIEWABLE_SAMPLE"
    assert gate.capacity_turnover_passed is True
    assert gate.capacity_turnover_failures == []


def test_p179_missing_capacity_turnover_snapshot_fails_real_data_evidence_gate(tmp_path: Path) -> None:
    artifact = tmp_path / "missing-capacity-snapshot.json"
    payload = _valid_real_payload(trade_count=30)
    del payload["capacity_turnover_snapshot"]
    artifact.write_text(json.dumps(payload), encoding="utf-8")

    gate = validate_real_data_backtest_evidence_artifact(artifact)

    assert gate.passed is False
    assert "capacity_turnover_snapshot" in gate.missing_fields
    assert "capacity_turnover_realism_gate" in gate.invalid_fields
    assert gate.capacity_turnover_passed is False
    assert gate.capacity_turnover_failures == ["capacity_turnover_snapshot_missing"]


def test_p179_capacity_turnover_failure_blocks_real_data_reviewability(tmp_path: Path) -> None:
    artifact = tmp_path / "failing-capacity-snapshot.json"
    payload = _valid_real_payload(trade_count=30)
    payload["capacity_turnover_snapshot"] = _capacity_snapshot(trade_count=30, max_position_adv_pct=7.0)
    artifact.write_text(json.dumps(payload), encoding="utf-8")

    gate = validate_real_data_backtest_evidence_artifact(artifact)

    assert gate.passed is False
    assert "capacity_turnover_realism_gate" in gate.invalid_fields
    assert gate.capacity_turnover_passed is False
    assert any("capacity_liquidity_limits" in failure for failure in gate.capacity_turnover_failures)


def test_p179_capacity_trade_count_must_match_backtest_trade_count(tmp_path: Path) -> None:
    artifact = tmp_path / "capacity-count-mismatch.json"
    payload = _valid_real_payload(trade_count=30)
    payload["capacity_turnover_snapshot"] = _capacity_snapshot(trade_count=31)
    artifact.write_text(json.dumps(payload), encoding="utf-8")

    gate = validate_real_data_backtest_evidence_artifact(artifact)

    assert gate.passed is False
    assert "capacity_turnover_realism_gate" in gate.invalid_fields
    assert gate.capacity_turnover_passed is False
    assert "capacity_trade_count_mismatch: capacity=31, evidence=30" in gate.capacity_turnover_failures


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


def test_p121_real_data_runner_writes_evidence_but_gate_blocks_insufficient_sample(tmp_path: Path) -> None:
    result, output_json, output_md = _run_real_data_runner(tmp_path)

    assert result.returncode == 0
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
    assert payload["sample_quality_status"] == "INSUFFICIENT_SAMPLE"
    assert payload["min_trade_count"] == 30
    assert payload["input_plan_count"] == 1
    assert payload["accepted_plan_count"] == 1
    assert payload["rejected_plan_count"] == 0
    assert payload["capacity_turnover_snapshot"]["metrics"]["trade_count"] == 1
    assert payload["live_trading_authorized"] is False
    assert payload["broker_execution_mode"] == "paper_only"
    gate = validate_real_data_backtest_evidence_artifact(output_json)
    assert gate.passed is False
    assert gate.observed_trade_count == 1
    assert gate.sample_quality_status == "INSUFFICIENT_SAMPLE"
    assert "insufficient_sample" in gate.invalid_fields
    assert "capacity_turnover_snapshot" not in gate.missing_fields
    assert "capacity_turnover_realism_gate" in gate.invalid_fields
    assert any("trade_count_floor" in failure for failure in gate.capacity_turnover_failures)


def test_p179_runner_derives_capacity_metrics_from_real_bars_and_results(tmp_path: Path) -> None:
    result, output_json, _ = _run_real_data_runner(tmp_path, proposed_capital_usd=1000.0, round_trip_cost_bps=1.0)

    assert result.returncode == 0
    payload = json.loads(output_json.read_text(encoding="utf-8"))
    metrics = payload["capacity_turnover_snapshot"]["metrics"]

    assert metrics["median_adv_usd"] == 114400000.0
    assert metrics["max_position_adv_pct"] == 0.0009
    assert metrics["portfolio_adv_pct"] == 0.0009
    assert metrics["average_daily_turnover_pct"] == 33.3333
    assert metrics["annual_turnover_pct"] == 8400.0
    assert metrics["gross_expectancy_bps"] == 495.0495
    assert metrics["net_expectancy_bps"] == 494.0495
    assert metrics["average_holding_days"] == 1.0
    assert payload["capacity_turnover_snapshot"]["proposed_capital_usd"] == 1000.0
    assert payload["capacity_turnover_snapshot"]["artifact_hashes"]["bars_root"].endswith("bars")


def test_p179_runner_fails_capacity_gate_when_adv_cannot_be_derived(tmp_path: Path) -> None:
    result, output_json, _ = _run_real_data_runner(tmp_path, malformed_volume=True)

    assert result.returncode == 0
    payload = json.loads(output_json.read_text(encoding="utf-8"))
    metrics = payload["capacity_turnover_snapshot"]["metrics"]
    assert metrics["median_adv_usd"] == 0.0
    assert metrics["max_position_adv_pct"] == 0.0
    assert metrics["portfolio_adv_pct"] == 0.0

    gate = validate_real_data_backtest_evidence_artifact(output_json)
    assert gate.passed is False
    assert "capacity_turnover_realism_gate" in gate.invalid_fields
    assert any("positive_scale" in failure for failure in gate.capacity_turnover_failures)
