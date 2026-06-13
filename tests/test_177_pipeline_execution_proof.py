from __future__ import annotations

import hashlib
import json
from pathlib import Path

from scripts.export_historical_trade_plans import export_historical_trade_plans
from scripts.validate_bt9_real_historical_input_pack import validate_bt9_input_pack

PIPELINE_GATES = [
    "scanner",
    "signal_generator",
    "quality_fusion",
    "trade_plan_validator",
]


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_universe(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "symbol,effective_from,effective_to,active,asset_class,exchange,source,status,reason\n"
        "SPY,2024-01-01,,true,etf,NYSEARCA,initial_universe,active,initial test universe\n",
        encoding="utf-8",
    )


def _write_bars(root: Path) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    path = root / "SPY.csv"
    path.write_text(
        "date,open,high,low,close,volume\n"
        "2026-06-01,100,101,99,100,1000000\n"
        "2026-06-02,101,105,100,104,1100000\n",
        encoding="utf-8",
    )
    return path


def _write_coverage_manifest(path: Path, *, bars_path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "vendor": "polygon",
                "generated_at": "2026-06-13T00:00:00Z",
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
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )


def _write_fake_scanner_pipeline_trade_plans_without_execution_proof(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "metadata": {
                    "pipeline_coupled": True,
                    "pipeline_generation_source": "scanner_signal_quality_validator",
                    "runtime_gates_applied": PIPELINE_GATES,
                    "generated_signal_count": 1,
                    "validated_trade_plan_count": 1,
                    "blocked_signal_count": 0,
                },
                "plans": [
                    {
                        "signal_id": "fake-spy-1",
                        "symbol": "SPY",
                        "signal_date": "2026-06-01",
                        "entry_trigger": 101.0,
                        "stop_loss": 99.0,
                        "target_1": 104.0,
                    }
                ],
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )


def _pipeline_payload() -> dict:
    return {
        "market_regime": "Bullish",
        "decision_report": {
            "decisions": [
                {
                    "symbol": "SPY",
                    "decision": "approved",
                    "setup_type": "momentum_breakout",
                    "risk_tier": "tier_1",
                    "position_size_multiplier": 1.0,
                    "setup_score": 82.0,
                    "regime_alignment": 0.9,
                    "score_source": "scanner_runtime",
                    "data_source": "polygon",
                    "thresholds_version": "v1_real_runtime",
                    "blocked_reasons": [],
                    "notes": [],
                }
            ]
        },
        "scanner_metrics_map": {
            "SPY": {
                "symbol": "SPY",
                "close": 100.0,
                "high": 100.5,
                "low": 98.5,
                "atr14": 1.0,
                "atr_pct": 1.0,
                "rvol": 1.2,
                "vwap": 99.5,
                "swing_low_3bar": 99.0,
                "data_status": "OK",
                "source": "polygon",
                "source_timestamp": "2026-06-01T21:00:00Z",
                "fallback_level": "none",
            }
        },
    }


def test_177_bt9_blocks_fake_scanner_pipeline_metadata_without_execution_proof(tmp_path: Path) -> None:
    universe = tmp_path / "data/universe/survivorship_universe.csv"
    bars_root = tmp_path / "data/historical/bars/1day"
    coverage_manifest = tmp_path / "data/historical/metadata/coverage_manifest.json"
    trade_plans = tmp_path / "data/trade_plans/historical_trade_plans.json"

    _write_universe(universe)
    bars_path = _write_bars(bars_root)
    _write_coverage_manifest(coverage_manifest, bars_path=bars_path)
    _write_fake_scanner_pipeline_trade_plans_without_execution_proof(trade_plans)

    report = validate_bt9_input_pack(
        universe_path=universe,
        bars_root=bars_root,
        trade_plans_path=trade_plans,
        coverage_manifest_path=coverage_manifest,
    )

    assert report.passed is False
    assert "trade_plans_missing_pipeline_execution_proof" in report.failures


def test_177_exporter_emits_scanner_pipeline_execution_proof_accepted_by_bt9(tmp_path: Path) -> None:
    source = tmp_path / "pipeline_payload.json"
    universe = tmp_path / "data/universe/survivorship_universe.csv"
    bars_root = tmp_path / "data/historical/bars/1day"
    coverage_manifest = tmp_path / "data/historical/metadata/coverage_manifest.json"
    trade_plans = tmp_path / "data/trade_plans/historical_trade_plans.json"
    manifest = tmp_path / "data/trade_plans/historical_trade_plans_manifest.json"

    source.write_text(json.dumps(_pipeline_payload(), indent=2, sort_keys=True), encoding="utf-8")
    export_report = export_historical_trade_plans(source_path=source, output_path=trade_plans, manifest_path=manifest)

    payload = json.loads(trade_plans.read_text(encoding="utf-8"))
    proof = payload["metadata"]["pipeline_execution_proof"]

    assert export_report.passed is True
    assert payload["metadata"]["pipeline_generation_source"] == "scanner_signal_quality_validator"
    assert proof["proof_version"] == "2026.06.13-v1"
    assert proof["adapter"] == "historical_scanner_signal_quality_validator_export"
    assert len(proof["source_payload_sha256"]) == 64
    assert "src.signals.signal_generator.build_signals" in proof["executed_runtime_entrypoints"]
    assert "scripts.export_historical_trade_plans._signal_to_plan" in proof["executed_runtime_entrypoints"]
    assert proof["runtime_gates_applied"] == PIPELINE_GATES
    assert proof["proof_boundary"] == "generated_by_exporter_runtime_path"

    _write_universe(universe)
    bars_path = _write_bars(bars_root)
    _write_coverage_manifest(coverage_manifest, bars_path=bars_path)

    bt9_report = validate_bt9_input_pack(
        universe_path=universe,
        bars_root=bars_root,
        trade_plans_path=trade_plans,
        coverage_manifest_path=coverage_manifest,
    )

    assert bt9_report.passed is True
    assert bt9_report.failures == []
