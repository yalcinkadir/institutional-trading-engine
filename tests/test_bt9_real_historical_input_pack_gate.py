from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

from scripts.validate_bt9_real_historical_input_pack import validate_bt9_input_pack

VALIDATOR_SCRIPT = Path("scripts/validate_bt9_real_historical_input_pack.py")
RUNNER_SCRIPT = Path("scripts/run_historical_entry_exit_backtest.py")
PIPELINE_GATES = [
    "scanner",
    "signal_generator",
    "quality_fusion",
    "trade_plan_validator",
]


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_trade_plans(
    path: Path,
    *,
    pipeline_coupled: bool = True,
    runtime_gates: list[str] | None = None,
    generation_source: str | None = None,
    include_metadata: bool = True,
    include_counts: bool = True,
) -> None:
    metadata = {
        "pipeline_coupled": pipeline_coupled,
        "pipeline_generation_source": generation_source
        or ("runtime_pipeline_adapter" if pipeline_coupled else "deterministic_historical_generator"),
        "runtime_gates_applied": runtime_gates if runtime_gates is not None else PIPELINE_GATES,
    }
    if include_counts:
        metadata.update(
            {
                "generated_signal_count": 1,
                "validated_trade_plan_count": 1 if pipeline_coupled else 0,
                "blocked_signal_count": 0 if pipeline_coupled else 1,
            }
        )

    payload = {
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
        ],
    }
    if include_metadata:
        payload["metadata"] = metadata
    path.write_text(json.dumps(payload), encoding="utf-8")


def _write_universe(path: Path) -> None:
    path.write_text(
        "symbol,effective_from,effective_to,active,asset_class,exchange,source,status,reason\n"
        "SPY,2024-01-01,,true,etf,NYSEARCA,initial_universe,active,initial test universe\n",
        encoding="utf-8",
    )


def _write_bars(root: Path) -> str:
    root.mkdir(parents=True, exist_ok=True)
    path = root / "SPY.csv"
    path.write_text(
        "date,open,high,low,close,volume\n"
        "2026-06-01,100,100,99,100,1000000\n"
        "2026-06-02,101,105,100,104,1100000\n",
        encoding="utf-8",
    )
    return _sha256(path)


def _write_coverage_manifest(path: Path, *, bars_root: Path, sha256: str | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    bars_path = bars_root / "SPY.csv"
    digest = sha256 or _sha256(bars_path)
    path.write_text(
        json.dumps(
            {
                "vendor": "polygon",
                "generated_at": "2026-06-01T00:00:00Z",
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
                        "output_sha256": digest,
                        "missing_data_summary": [],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )


def test_bt9_input_pack_passes_with_valid_pipeline_coupled_files(tmp_path: Path) -> None:
    universe = tmp_path / "universe.csv"
    bars = tmp_path / "bars"
    plans = tmp_path / "plans.json"
    coverage_manifest = tmp_path / "coverage_manifest.json"
    _write_universe(universe)
    digest = _write_bars(bars)
    _write_coverage_manifest(coverage_manifest, bars_root=bars, sha256=digest)
    _write_trade_plans(plans)

    report = validate_bt9_input_pack(
        universe_path=universe,
        bars_root=bars,
        trade_plans_path=plans,
        coverage_manifest_path=coverage_manifest,
    )

    assert report.passed is True
    assert report.failures == []
    assert report.input_checksums == {(bars / "SPY.csv").as_posix(): digest}


def test_bt9_input_pack_fails_when_files_are_missing(tmp_path: Path) -> None:
    report = validate_bt9_input_pack(
        universe_path=tmp_path / "missing-universe.csv",
        bars_root=tmp_path / "missing-bars",
        trade_plans_path=tmp_path / "missing-plans.json",
        coverage_manifest_path=tmp_path / "missing-coverage-manifest.json",
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
            "--coverage-manifest",
            str(tmp_path / "missing-coverage-manifest.json"),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    assert "BT9 real historical input pack gate status: FAIL" in result.stdout
    assert "missing_universe_file" in result.stdout
    assert "missing_trade_plans_file" in result.stdout


def test_bt9_input_pack_blocks_missing_pipeline_metadata(tmp_path: Path) -> None:
    universe = tmp_path / "universe.csv"
    bars = tmp_path / "bars"
    plans = tmp_path / "plans.json"
    coverage_manifest = tmp_path / "coverage_manifest.json"
    _write_universe(universe)
    _write_bars(bars)
    _write_coverage_manifest(coverage_manifest, bars_root=bars)
    _write_trade_plans(plans, include_metadata=False)

    report = validate_bt9_input_pack(
        universe_path=universe,
        bars_root=bars,
        trade_plans_path=plans,
        coverage_manifest_path=coverage_manifest,
    )

    assert report.passed is False
    assert "trade_plans_missing_pipeline_metadata" in report.failures


def test_bt9_input_pack_blocks_non_pipeline_coupled_metadata(tmp_path: Path) -> None:
    universe = tmp_path / "universe.csv"
    bars = tmp_path / "bars"
    plans = tmp_path / "plans.json"
    coverage_manifest = tmp_path / "coverage_manifest.json"
    _write_universe(universe)
    _write_bars(bars)
    _write_coverage_manifest(coverage_manifest, bars_root=bars)
    _write_trade_plans(plans, pipeline_coupled=False)

    report = validate_bt9_input_pack(
        universe_path=universe,
        bars_root=bars,
        trade_plans_path=plans,
        coverage_manifest_path=coverage_manifest,
    )

    assert report.passed is False
    assert "trade_plans_not_pipeline_coupled" in report.failures
    assert "trade_plans_invalid_pipeline_generation_source:deterministic_historical_generator" in report.failures
    assert "trade_plans_forbidden_pipeline_generation_source:deterministic_historical_generator" in report.failures


def test_bt9_input_pack_blocks_missing_runtime_gates(tmp_path: Path) -> None:
    universe = tmp_path / "universe.csv"
    bars = tmp_path / "bars"
    plans = tmp_path / "plans.json"
    coverage_manifest = tmp_path / "coverage_manifest.json"
    _write_universe(universe)
    _write_bars(bars)
    _write_coverage_manifest(coverage_manifest, bars_root=bars)
    _write_trade_plans(plans, runtime_gates=["scanner", "signal_generator"])

    report = validate_bt9_input_pack(
        universe_path=universe,
        bars_root=bars,
        trade_plans_path=plans,
        coverage_manifest_path=coverage_manifest,
    )

    assert report.passed is False
    assert "trade_plans_missing_runtime_gates:quality_fusion,trade_plan_validator" in report.failures


def test_bt9_input_pack_blocks_forbidden_observation_export_source(tmp_path: Path) -> None:
    universe = tmp_path / "universe.csv"
    bars = tmp_path / "bars"
    plans = tmp_path / "plans.json"
    coverage_manifest = tmp_path / "coverage_manifest.json"
    _write_universe(universe)
    _write_bars(bars)
    _write_coverage_manifest(coverage_manifest, bars_root=bars)
    _write_trade_plans(plans, generation_source="validated_paper_observation_export")

    report = validate_bt9_input_pack(
        universe_path=universe,
        bars_root=bars,
        trade_plans_path=plans,
        coverage_manifest_path=coverage_manifest,
    )

    assert report.passed is False
    assert "trade_plans_invalid_pipeline_generation_source:validated_paper_observation_export" in report.failures
    assert "trade_plans_forbidden_pipeline_generation_source:validated_paper_observation_export" in report.failures


def test_bt9_input_pack_blocks_missing_pipeline_counts(tmp_path: Path) -> None:
    universe = tmp_path / "universe.csv"
    bars = tmp_path / "bars"
    plans = tmp_path / "plans.json"
    coverage_manifest = tmp_path / "coverage_manifest.json"
    _write_universe(universe)
    _write_bars(bars)
    _write_coverage_manifest(coverage_manifest, bars_root=bars)
    _write_trade_plans(plans, include_counts=False)

    report = validate_bt9_input_pack(
        universe_path=universe,
        bars_root=bars,
        trade_plans_path=plans,
        coverage_manifest_path=coverage_manifest,
    )

    assert report.passed is False
    assert "trade_plans_missing_generated_signal_count" in report.failures
    assert "trade_plans_missing_validated_trade_plan_count" in report.failures


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
            "--coverage-manifest",
            str(tmp_path / "missing-coverage-manifest.json"),
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
    assert "input_checksums" in payload


def test_real_data_runner_blocks_trade_plans_not_generated_by_runtime_pipeline(tmp_path: Path) -> None:
    universe = tmp_path / "universe.csv"
    bars = tmp_path / "bars"
    plans = tmp_path / "plans.json"
    coverage_manifest = tmp_path / "coverage_manifest.json"
    json_output = tmp_path / "blocked-evidence.json"
    markdown_output = tmp_path / "blocked-evidence.md"
    _write_universe(universe)
    _write_bars(bars)
    _write_coverage_manifest(coverage_manifest, bars_root=bars)
    _write_trade_plans(plans, pipeline_coupled=False)

    result = subprocess.run(
        [
            sys.executable,
            str(RUNNER_SCRIPT),
            "--plans-file",
            str(plans),
            "--bars-root",
            str(bars),
            "--universe",
            str(universe),
            "--coverage-manifest",
            str(coverage_manifest),
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
    payload = json.loads(json_output.read_text(encoding="utf-8"))
    assert payload["input_pack_gate_status"] == "FAILED"
    assert payload["input_completeness_status"] == "BLOCKED_INPUT_PACK"
    assert payload["run_health_status"] == "BLOCKED"
    assert "trade_plans_not_pipeline_coupled" in payload["rejection_reasons"][0]["reasons"]
    assert "trade_plans_forbidden_pipeline_generation_source:deterministic_historical_generator" in payload["rejection_reasons"][0]["reasons"]


def test_real_data_runner_requires_all_runtime_gates_for_pipeline_claim(tmp_path: Path) -> None:
    universe = tmp_path / "universe.csv"
    bars = tmp_path / "bars"
    plans = tmp_path / "plans.json"
    coverage_manifest = tmp_path / "coverage_manifest.json"
    json_output = tmp_path / "blocked-evidence.json"
    markdown_output = tmp_path / "blocked-evidence.md"
    _write_universe(universe)
    _write_bars(bars)
    _write_coverage_manifest(coverage_manifest, bars_root=bars)
    _write_trade_plans(plans, pipeline_coupled=True, runtime_gates=["scanner", "signal_generator"])

    result = subprocess.run(
        [
            sys.executable,
            str(RUNNER_SCRIPT),
            "--plans-file",
            str(plans),
            "--bars-root",
            str(bars),
            "--universe",
            str(universe),
            "--coverage-manifest",
            str(coverage_manifest),
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
    payload = json.loads(json_output.read_text(encoding="utf-8"))
    assert payload["input_pack_gate_status"] == "FAILED"
    assert "trade_plans_missing_runtime_gates:quality_fusion,trade_plan_validator" in payload["rejection_reasons"][0]["reasons"]


def test_real_data_runner_blocks_validated_observation_export_as_strategy_evidence(tmp_path: Path) -> None:
    universe = tmp_path / "universe.csv"
    bars = tmp_path / "bars"
    plans = tmp_path / "plans.json"
    coverage_manifest = tmp_path / "coverage_manifest.json"
    json_output = tmp_path / "blocked-evidence.json"
    markdown_output = tmp_path / "blocked-evidence.md"
    _write_universe(universe)
    _write_bars(bars)
    _write_coverage_manifest(coverage_manifest, bars_root=bars)
    _write_trade_plans(
        plans,
        pipeline_coupled=True,
        runtime_gates=PIPELINE_GATES,
        generation_source="validated_paper_observation_export",
    )

    result = subprocess.run(
        [
            sys.executable,
            str(RUNNER_SCRIPT),
            "--plans-file",
            str(plans),
            "--bars-root",
            str(bars),
            "--universe",
            str(universe),
            "--coverage-manifest",
            str(coverage_manifest),
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
    payload = json.loads(json_output.read_text(encoding="utf-8"))
    assert payload["input_pack_gate_status"] == "FAILED"
    assert "trade_plans_forbidden_pipeline_generation_source:validated_paper_observation_export" in payload["rejection_reasons"][0]["reasons"]


def test_real_data_runner_accepts_pipeline_coupled_trade_plans_and_reports_pipeline_evidence(tmp_path: Path) -> None:
    universe = tmp_path / "universe.csv"
    bars = tmp_path / "bars"
    plans = tmp_path / "plans.json"
    coverage_manifest = tmp_path / "coverage_manifest.json"
    json_output = tmp_path / "evidence.json"
    markdown_output = tmp_path / "evidence.md"
    _write_universe(universe)
    _write_bars(bars)
    _write_coverage_manifest(coverage_manifest, bars_root=bars)
    _write_trade_plans(plans, pipeline_coupled=True, runtime_gates=PIPELINE_GATES)

    result = subprocess.run(
        [
            sys.executable,
            str(RUNNER_SCRIPT),
            "--plans-file",
            str(plans),
            "--bars-root",
            str(bars),
            "--universe",
            str(universe),
            "--coverage-manifest",
            str(coverage_manifest),
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

    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(json_output.read_text(encoding="utf-8"))
    assert payload["data_source"] == "real_data"
    assert payload["is_demo"] is False
    assert payload["pipeline_coupled"] is True
    assert payload["pipeline_generation_source"] == "runtime_pipeline_adapter"
    assert payload["generated_signal_count"] == 1
    assert payload["validated_trade_plan_count"] == 1
    assert payload["blocked_signal_count"] == 0
    assert payload["runtime_gates_applied"] == PIPELINE_GATES
    assert payload["accepted_plan_count"] == 1
    assert payload["input_checksums"]
    assert payload["broker_execution_mode"] == "paper_only"
    assert payload["live_trading_authorized"] is False
