from __future__ import annotations

from datetime import date
import json

from src.validation.historical_edge_validation import HistoricalEdgeValidationConfig
from src.validation.out_of_sample_lockbox import (
    OutOfSampleLockboxConfig,
    build_out_of_sample_lockbox,
    build_out_of_sample_lockbox_manifest,
    write_out_of_sample_lockbox_report,
)


EDGE_CONFIG = HistoricalEdgeValidationConfig(
    min_total_trades=3,
    min_profit_factor=1.0,
    min_expectancy_r=0.1,
    max_drawdown_limit=10.0,
    min_sharpe_ratio=-10.0,
    min_deflated_sharpe_probability=0.0,
    bootstrap_iterations=10,
)


def _config(**overrides: object) -> OutOfSampleLockboxConfig:
    values = {
        "split_date": date(2024, 1, 1),
        "edge_config": EDGE_CONFIG,
        "max_core_metric_degradation": 1.0,
    }
    values.update(overrides)
    return OutOfSampleLockboxConfig(**values)


def _record(signal_id: str, exit_date: str, result_r: float, symbol: str = "AAPL") -> dict:
    return {
        "signal_id": signal_id,
        "symbol": symbol,
        "entry_date": exit_date,
        "exit_date": exit_date,
        "result_r": result_r,
        "thresholds_version": "public-demo-v0.1",
    }


def test_oos_lockbox_basic_split() -> None:
    records = [
        _record("train-1", "2023-12-01", 1.0),
        _record("train-2", "2023-12-05", 1.2),
        _record("train-3", "2023-12-10", -0.2),
        _record("test-1", "2024-01-05", 1.0),
        _record("test-2", "2024-01-07", 1.1),
        _record("test-3", "2024-01-09", -0.1),
    ]

    report = build_out_of_sample_lockbox(records, config=_config())

    assert report.in_sample_count == 3
    assert report.out_of_sample_count == 3
    assert report.purged_records == 0
    assert report.embargoed_records == 0
    assert report.unassigned_records == 0
    assert "window_overlap" not in report.invalidation_reasons


def test_oos_lockbox_contamination_detection() -> None:
    records = [
        _record("dup-1", "2023-12-01", 1.0, symbol="AAPL"),
        _record("dup-1", "2024-01-05", 1.0, symbol="AAPL"),
        _record("train-2", "2023-12-02", 1.1, symbol="MSFT"),
        _record("train-3", "2023-12-03", 1.2, symbol="NVDA"),
        _record("test-2", "2024-01-05", 1.1, symbol="TSLA"),
        _record("test-3", "2024-01-06", 1.2, symbol="MSFT"),
    ]

    report = build_out_of_sample_lockbox(records, config=_config())

    assert report.passed is False
    assert "duplicate_signal_ids:dup-1" in report.invalidation_reasons
    assert "duplicate_record_dates:2024-01-05" in report.invalidation_reasons
    assert "leaked_symbols:AAPL,MSFT" in report.invalidation_reasons


def test_oos_lockbox_blocks_empty_or_tiny_samples() -> None:
    tiny_records = [
        _record("train-1", "2023-12-01", 1.0),
        _record("test-1", "2024-01-05", 1.0),
    ]

    report = build_out_of_sample_lockbox(tiny_records, config=_config())

    assert report.passed is False
    assert "insufficient_in_sample_records:1<3" in report.invalidation_reasons
    assert "insufficient_out_of_sample_records:1<3" in report.invalidation_reasons


def test_oos_lockbox_manifest_records_parameters(tmp_path) -> None:
    records = [
        _record("train-1", "2023-12-01", 1.0),
        _record("train-2", "2023-12-05", 1.2),
        _record("train-3", "2023-12-10", -0.2),
        _record("test-1", "2024-01-05", 1.0),
        _record("test-2", "2024-01-07", 1.1),
        _record("test-3", "2024-01-09", -0.1),
    ]
    config = _config(purge_days=2, embargo_days=1)
    report = build_out_of_sample_lockbox(records, config=config)
    manifest = build_out_of_sample_lockbox_manifest(report, source_records=records, config=config)

    assert manifest["schema"] == "out_of_sample_lockbox_manifest.v1"
    assert manifest["split_parameters"]["split_date"] == "2024-01-01"
    assert manifest["split_parameters"]["purge_days"] == 2
    assert manifest["split_parameters"]["embargo_days"] == 1
    assert manifest["date_ranges"]["in_sample"] == {"start": "2023-12-01", "end": "2023-12-10"}
    assert manifest["date_ranges"]["out_of_sample"] == {"start": "2024-01-05", "end": "2024-01-09"}
    assert len(manifest["checksums"]["source_records_sha256"]) == 64
    assert len(manifest["checksums"]["evidence_contract_hash"]) == 64

    json_path = tmp_path / "oos.json"
    md_path = tmp_path / "oos.md"
    manifest_path = tmp_path / "oos.manifest.json"
    write_out_of_sample_lockbox_report(
        report,
        json_path=json_path,
        markdown_path=md_path,
        manifest_path=manifest_path,
        source_records=records,
        config=config,
    )

    written_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert written_manifest == manifest
