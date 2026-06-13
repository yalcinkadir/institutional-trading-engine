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
    assert report.input_checksums[(bars / "SPY.csv").as_posix()] == digest
    assert report.input_checksums[universe.as_posix()] == _sha256(universe)
    assert report.input_checksums[coverage_manifest.as_posix()] == _sha256(coverage_manifest)
    assert report.input_checksums[plans.as_posix()] == _sha256(plans)


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
    assert any(failure.startswith("trade_plans_invalid_pipeline_generation_source") for failure in report.failures)
