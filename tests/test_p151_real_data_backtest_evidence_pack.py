from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

SCRIPT = Path("scripts/build_real_data_backtest_evidence_pack.py")
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


def _write_plan(path: Path) -> None:
    path.write_text(
        json.dumps(
            {
                "metadata": PIPELINE_METADATA,
                "plans": [
                    {
                        "signal_id": "sig_SPY_p151_real",
                        "symbol": "SPY",
                        "signal_date": "2026-06-01",
                        "entry_trigger": 101.0,
                        "stop_loss": 99.0,
                        "target_1": 104.0,
                        "target_2": 106.0,
                        "source": "scanner_signal_quality_validator",
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
        "2026-06-03,104,106,103,106,1200000\n",
        encoding="utf-8",
    )
    return path


def _write_universe(path: Path) -> None:
    path.write_text(
        "symbol,effective_from,effective_to,active,asset_class,exchange,source,status,reason\n"
        "SPY,2024-01-01,,true,etf,NYSEARCA,licensed_fixture,active,p151 test universe\n",
        encoding="utf-8",
    )


def _write_coverage(path: Path, *, bars_path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "vendor": "polygon",
                "generated_at": "2026-06-11T00:00:00Z",
                "multiplier": 1,
                "timespan": "day",
                "status": "ok",
                "requested_start_date": "2026-06-01",
                "requested_end_date": "2026-06-03",
                "symbol_count": 1,
                "ok_symbol_count": 1,
                "missing_data_summary": [],
                "symbols": [
                    {
                        "symbol": "SPY",
                        "start_date": "2026-06-01",
                        "end_date": "2026-06-03",
                        "status": "ok",
                        "bar_count": 3,
                        "rows_fetched": 3,
                        "output_path": bars_path.as_posix(),
                        "output_sha256": _sha256(bars_path),
                        "missing_data_summary": [],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )


def test_p151_blocks_when_approved_data_source_key_is_missing(tmp_path: Path) -> None:
    env = os.environ.copy()
    env.pop("POLYGON_API_KEY", None)
    output_dir = tmp_path / "pack"

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--symbols",
            "SPY",
            "--start-date",
            "2026-06-01",
            "--end-date",
            "2026-06-03",
            "--run-id",
            "p151-missing-key",
            "--output-dir",
            str(output_dir),
        ],
        capture_output=True,
        text=True,
        check=False,
        env=env,
    )

    assert result.returncode == 1
    package = json.loads((output_dir / "real-data-backtest-evidence-package.json").read_text(encoding="utf-8"))
    assert package["status"] == "BLOCKED"
    assert package["is_demo"] is False
    assert "missing_POLYGON_API_KEY" in package["block_reasons"]
    assert not (output_dir / "real-data-backtest-evidence.json").exists()


def test_p151_builds_valid_real_data_evidence_package_from_prepared_inputs(tmp_path: Path) -> None:
    plans = tmp_path / "plans.json"
    bars = tmp_path / "bars"
    universe = tmp_path / "universe.csv"
    coverage = tmp_path / "coverage.json"
    output_dir = tmp_path / "pack"
    _write_plan(plans)
    bars_path = _write_bars(bars)
    _write_universe(universe)
    _write_coverage(coverage, bars_path=bars_path)

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--symbols",
            "SPY",
            "--start-date",
            "2026-06-01",
            "--end-date",
            "2026-06-03",
            "--run-id",
            "p151-valid-real-data",
            "--plans-file",
            str(plans),
            "--bars-root",
            str(bars),
            "--universe",
            str(universe),
            "--coverage-manifest",
            str(coverage),
            "--output-dir",
            str(output_dir),
            "--skip-ingestion",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    package = json.loads((output_dir / "real-data-backtest-evidence-package.json").read_text(encoding="utf-8"))
    evidence = json.loads((output_dir / "real-data-backtest-evidence.json").read_text(encoding="utf-8"))

    assert package["status"] == "VALID"
    assert package["bt130_gate_status"] == "PASSED"
    assert package["data_source"] == "polygon"
    assert package["is_demo"] is False
    assert package["evidence_gate_report"]["passed"] is True
    assert evidence["data_source"] == "real_data"
    assert evidence["is_demo"] is False
    assert evidence["input_pack_gate_status"] == "PASSED"
    assert evidence["input_checksums"] == {bars_path.as_posix(): _sha256(bars_path)}
    assert evidence["pipeline_coupled"] is True
    assert evidence["runtime_gates_applied"] == PIPELINE_METADATA["runtime_gates_applied"]
    assert evidence["accepted_plan_count"] == 1
    assert evidence["broker_execution_mode"] == "paper_only"
    assert evidence["live_trading_authorized"] is False
