from __future__ import annotations

import hashlib
import json
from pathlib import Path

from scripts.export_historical_trade_plans import export_historical_trade_plans
from scripts.validate_bt9_real_historical_input_pack import validate_bt9_input_pack


RUNTIME_GATES = ["scanner", "signal_generator", "quality_fusion", "trade_plan_validator"]


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_bt9_coverage_manifest(path: Path, *, bars_path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "vendor": "polygon",
        "generated_at": "2026-06-11T00:00:00Z",
        "multiplier": 1,
        "timespan": "day",
        "requested_start_date": "2026-06-01",
        "requested_end_date": "2026-06-12",
        "symbol_count": 1,
        "ok_symbol_count": 1,
        "status": "ok",
        "missing_data_summary": [],
        "symbols": [
            {
                "symbol": "SPY",
                "start_date": "2026-06-01",
                "end_date": "2026-06-12",
                "bar_count": 2,
                "rows_fetched": 2,
                "status": "ok",
                "output_path": bars_path.as_posix(),
                "output_sha256": _sha256(bars_path),
                "missing_data_summary": [],
            }
        ],
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def _valid_record(**overrides):
    record = {
        "signal_id": "sig_SPY_001",
        "symbol": "SPY",
        "timestamp": "2026-06-01T14:30:00Z",
        "close": 100.0,
        "entry_trigger": 101.0,
        "stop_loss": 99.0,
        "target_1": 104.0,
        "target_2": 106.0,
        "valid_until": "2026-06-05",
        "entry_type": "breakout",
        "setup_type": "momentum_breakout",
        "data_source": "polygon",
        "data_status": "ok",
        "provenance": {"vendor": "polygon", "as_of": "2026-06-01T14:30:00Z"},
        "pipeline_coupled": True,
        "runtime_gates_applied": RUNTIME_GATES,
    }
    record.update(overrides)
    return record


def _decision_report(**decision_overrides):
    decision = {
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
    decision.update(decision_overrides)
    return {"decisions": [decision]}


def _scanner_metrics(**metric_overrides):
    metrics = {
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
    metrics.update(metric_overrides)
    return metrics


def _pipeline_payload(*, decision_overrides=None, metric_overrides=None):
    return {
        "market_regime": "Bullish",
        "decision_report": _decision_report(**(decision_overrides or {})),
        "scanner_metrics_map": {"SPY": _scanner_metrics(**(metric_overrides or {}))},
    }


def _write_source(path: Path, records: list[dict]) -> None:
    path.write_text(json.dumps({"observations": records}), encoding="utf-8")


def _write_pipeline_source(path: Path, *, decision_overrides=None, metric_overrides=None) -> None:
    path.write_text(json.dumps(_pipeline_payload(decision_overrides=decision_overrides, metric_overrides=metric_overrides)), encoding="utf-8")


def test_htp1_missing_close_blocks_export(tmp_path: Path) -> None:
    source = tmp_path / "observations.json"
    _write_source(source, [_valid_record(close=None)])

    report = export_historical_trade_plans(
        source_path=source,
        output_path=tmp_path / "historical_trade_plans.json",
        manifest_path=tmp_path / "manifest.json",
    )

    assert report.passed is False
    assert "record_0_missing:close" in report.failures
    assert "record_0_missing_close" in report.failures
    assert not (tmp_path / "historical_trade_plans.json").exists()


def test_htp1_missing_entry_stop_target_blocks_export(tmp_path: Path) -> None:
    source = tmp_path / "observations.json"
    _write_source(source, [_valid_record(entry_trigger=None, stop_loss=None, target_1=None)])

    report = export_historical_trade_plans(
        source_path=source,
        output_path=tmp_path / "historical_trade_plans.json",
        manifest_path=tmp_path / "manifest.json",
    )

    assert report.passed is False
    assert "record_0_missing:entry_trigger,stop_loss,target_1" in report.failures
    assert "record_0_missing_entry_trigger" in report.failures
    assert "record_0_missing_stop_loss" in report.failures
    assert "record_0_missing_target_1" in report.failures


def test_htp1_rejects_demo_synthetic_public_safe_records(tmp_path: Path) -> None:
    source = tmp_path / "observations.json"
    _write_source(source, [_valid_record(data_source="synthetic_demo", provenance={"vendor": "public_safe"})])

    report = export_historical_trade_plans(
        source_path=source,
        output_path=tmp_path / "historical_trade_plans.json",
        manifest_path=tmp_path / "manifest.json",
    )

    assert report.passed is False
    assert "record_0_demo_marker" in report.failures


def test_htp1_rejects_non_pipeline_coupled_observations(tmp_path: Path) -> None:
    source = tmp_path / "observations.json"
    _write_source(source, [_valid_record(pipeline_coupled=False)])

    report = export_historical_trade_plans(
        source_path=source,
        output_path=tmp_path / "historical_trade_plans.json",
        manifest_path=tmp_path / "manifest.json",
    )

    assert report.passed is False
    assert "record_0_not_pipeline_coupled" in report.failures
    assert not (tmp_path / "historical_trade_plans.json").exists()


def test_htp1_rejects_observations_missing_runtime_gates(tmp_path: Path) -> None:
    source = tmp_path / "observations.json"
    _write_source(source, [_valid_record(runtime_gates_applied=["scanner", "signal_generator"])])

    report = export_historical_trade_plans(
        source_path=source,
        output_path=tmp_path / "historical_trade_plans.json",
        manifest_path=tmp_path / "manifest.json",
    )

    assert report.passed is False
    assert "record_0_missing_runtime_gates:quality_fusion,trade_plan_validator" in report.failures
    assert not (tmp_path / "historical_trade_plans.json").exists()


def test_htp1_valid_observations_export_deterministic_trade_plans(tmp_path: Path) -> None:
    source = tmp_path / "observations.json"
    output = tmp_path / "historical_trade_plans.json"
    manifest = tmp_path / "manifest.json"
    _write_source(
        source,
        [
            _valid_record(signal_id="sig_QQQ_001", symbol="QQQ", timestamp="2026-06-02T14:30:00Z"),
            _valid_record(signal_id="sig_SPY_001", symbol="SPY", timestamp="2026-06-01T14:30:00Z"),
        ],
    )

    first = export_historical_trade_plans(source_path=source, output_path=output, manifest_path=manifest)
    first_bytes = output.read_bytes()
    second = export_historical_trade_plans(source_path=source, output_path=output, manifest_path=manifest)

    payload = json.loads(first_bytes.decode("utf-8"))
    manifest_payload = json.loads(manifest.read_text(encoding="utf-8"))

    assert first.passed is True
    assert second.passed is True
    assert output.read_bytes() == first_bytes
    assert payload["metadata"]["pipeline_coupled"] is True
    assert payload["metadata"]["pipeline_generation_source"] == "validated_paper_observation_export"
    assert payload["metadata"]["generated_signal_count"] == 2
    assert payload["metadata"]["validated_trade_plan_count"] == 2
    assert payload["metadata"]["blocked_signal_count"] == 0
    assert payload["metadata"]["runtime_gates_applied"] == RUNTIME_GATES
    assert [plan["signal_id"] for plan in payload["plans"]] == ["sig_SPY_001", "sig_QQQ_001"]
    assert manifest_payload["exported_count"] == 2
    assert manifest_payload["symbols"] == ["QQQ", "SPY"]
    assert manifest_payload["output_sha256"]
    assert manifest_payload["boundary"] == "paper_only_research_only"


def test_177_pipeline_payload_executes_scanner_signal_quality_validator_path(tmp_path: Path) -> None:
    source = tmp_path / "pipeline.json"
    output = tmp_path / "historical_trade_plans.json"
    manifest = tmp_path / "manifest.json"
    _write_pipeline_source(source)

    report = export_historical_trade_plans(source_path=source, output_path=output, manifest_path=manifest)
    payload = json.loads(output.read_text(encoding="utf-8"))
    manifest_payload = json.loads(manifest.read_text(encoding="utf-8"))
    plan = payload["plans"][0]

    assert report.passed is True
    assert report.pipeline_coupled is True
    assert report.pipeline_generation_source == "scanner_signal_quality_validator"
    assert report.runtime_gates_applied == RUNTIME_GATES
    assert payload["metadata"]["pipeline_generation_source"] == "scanner_signal_quality_validator"
    assert payload["metadata"]["generated_signal_count"] == 1
    assert payload["metadata"]["validated_trade_plan_count"] == 1
    assert payload["metadata"]["blocked_signal_count"] == 0
    assert plan["source"] == "scanner_signal_quality_validator"
    assert plan["symbol"] == "SPY"
    assert plan["entry_trigger"] > plan["close"]
    assert plan["stop_loss"] < plan["entry_trigger"] < plan["target_1"]
    assert plan["provenance"]["runtime_gates_applied"] == RUNTIME_GATES
    assert manifest_payload["pipeline_generation_source"] == "scanner_signal_quality_validator"


def test_177_pipeline_payload_blocks_missing_scanner_atr_before_backtest_plan_export(tmp_path: Path) -> None:
    source = tmp_path / "pipeline.json"
    output = tmp_path / "historical_trade_plans.json"
    manifest = tmp_path / "manifest.json"
    _write_pipeline_source(source, metric_overrides={"atr14": None})

    report = export_historical_trade_plans(source_path=source, output_path=output, manifest_path=manifest)
    manifest_payload = json.loads(manifest.read_text(encoding="utf-8"))

    assert report.passed is False
    assert "no_validated_buy_watch_signals" in report.failures
    assert "no_validated_trade_plans" in report.failures
    assert not output.exists()
    assert manifest_payload["pipeline_coupled"] is False
    assert manifest_payload["pipeline_generation_source"] == "scanner_signal_quality_validator"
    assert manifest_payload["validated_trade_plan_count"] == 0


def test_177_pipeline_payload_blocks_demo_provenance_before_real_data_backtest_claim(tmp_path: Path) -> None:
    source = tmp_path / "pipeline.json"
    output = tmp_path / "historical_trade_plans.json"
    manifest = tmp_path / "manifest.json"
    _write_pipeline_source(source, decision_overrides={"score_source": "demo"})

    report = export_historical_trade_plans(source_path=source, output_path=output, manifest_path=manifest)

    assert report.passed is False
    assert "pipeline_payload_demo_marker" in report.failures
    assert "no_validated_buy_watch_signals" in report.failures
    assert not output.exists()


def test_177_pipeline_export_is_bt9_compatible(tmp_path: Path) -> None:
    source = tmp_path / "pipeline.json"
    output = tmp_path / "data/trade_plans/historical_trade_plans.json"
    manifest = tmp_path / "data/trade_plans/historical_trade_plans_manifest.json"
    universe = tmp_path / "data/universe/survivorship_universe.csv"
    bars_root = tmp_path / "data/historical/bars/1day"
    coverage_manifest = tmp_path / "data/historical/metadata/coverage_manifest.json"
    _write_pipeline_source(source)
    export_report = export_historical_trade_plans(source_path=source, output_path=output, manifest_path=manifest)
    universe.parent.mkdir(parents=True, exist_ok=True)
    universe.write_text(
        "symbol,effective_from,effective_to,active,asset_class,exchange,source,status,reason\n"
        "SPY,2024-01-01,,true,etf,NYSEARCA,initial_universe,active,initial test universe\n",
        encoding="utf-8",
    )
    bars_root.mkdir(parents=True, exist_ok=True)
    bars_path = bars_root / "SPY.csv"
    bars_path.write_text(
        "date,open,high,low,close,volume\n"
        "2026-06-11,100,101,99,100,1000000\n"
        "2026-06-12,101,105,100,104,1100000\n",
        encoding="utf-8",
    )
    _write_bt9_coverage_manifest(coverage_manifest, bars_path=bars_path)

    bt9_report = validate_bt9_input_pack(
        universe_path=universe,
        bars_root=bars_root,
        trade_plans_path=output,
        coverage_manifest_path=coverage_manifest,
    )

    assert export_report.passed is True
    assert export_report.pipeline_generation_source == "scanner_signal_quality_validator"
    assert bt9_report.passed is True
    assert bt9_report.symbols == ["SPY"]
    assert bt9_report.input_checksums


def test_htp1_export_is_bt9_compatible(tmp_path: Path) -> None:
    source = tmp_path / "observations.json"
    output = tmp_path / "data/trade_plans/historical_trade_plans.json"
    manifest = tmp_path / "data/trade_plans/historical_trade_plans_manifest.json"
    universe = tmp_path / "data/universe/survivorship_universe.csv"
    bars_root = tmp_path / "data/historical/bars/1day"
    coverage_manifest = tmp_path / "data/historical/metadata/coverage_manifest.json"
    _write_source(source, [_valid_record()])
    export_report = export_historical_trade_plans(source_path=source, output_path=output, manifest_path=manifest)
    universe.parent.mkdir(parents=True, exist_ok=True)
    universe.write_text(
        "symbol,effective_from,effective_to,active,asset_class,exchange,source,status,reason\n"
        "SPY,2024-01-01,,true,etf,NYSEARCA,initial_universe,active,initial test universe\n",
        encoding="utf-8",
    )
    bars_root.mkdir(parents=True, exist_ok=True)
    bars_path = bars_root / "SPY.csv"
    bars_path.write_text(
        "date,open,high,low,close,volume\n"
        "2026-06-01,100,101,99,100,1000000\n"
        "2026-06-02,101,105,100,104,1100000\n",
        encoding="utf-8",
    )
    _write_bt9_coverage_manifest(coverage_manifest, bars_path=bars_path)

    bt9_report = validate_bt9_input_pack(
        universe_path=universe,
        bars_root=bars_root,
        trade_plans_path=output,
        coverage_manifest_path=coverage_manifest,
    )

    assert export_report.passed is True
    assert bt9_report.passed is True
    assert bt9_report.symbols == ["SPY"]
    assert bt9_report.input_checksums
