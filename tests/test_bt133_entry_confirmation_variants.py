from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.analyze_bt133_entry_confirmation_variants import analyze, render_markdown, write_report


def _row(signal_id: str, signal_date: str, *, r_multiple: float, false_breakout: bool, stop_hit: bool, mfe: float, mae: float, bars: int = 5, entry_hit: bool = True) -> dict:
    return {
        "signal_id": signal_id,
        "symbol": "AAA",
        "signal_date": signal_date,
        "outcome": "STOP_HIT" if stop_hit else "TARGET_1_HIT",
        "entry_hit": entry_hit,
        "target_1_hit": r_multiple > 0,
        "target_2_hit": r_multiple >= 2,
        "stop_hit": stop_hit,
        "false_breakout": false_breakout,
        "r_multiple": r_multiple,
        "bars_evaluated": bars,
        "entry_price": 100.0,
        "entry_trigger": 100.0,
        "initial_stop_loss": 95.0,
        "target_1": 110.0,
        "target_2": 115.0,
        "max_favorable_excursion_r": mfe,
        "max_adverse_excursion_r": mae,
        "same_bar_ambiguous": False,
        "missing_field_reasons": {},
        "signal_day_cluster_size": 1,
    }


def _evidence(tmp_path: Path) -> Path:
    payload = {
        "run_id": "bt131-real-data-manual",
        "data_source": "real_data",
        "is_demo": False,
        "input_pack_gate_status": "PASSED",
        "input_completeness_status": "OK",
        "run_health_status": "OK",
        "live_trading_authorized": False,
        "broker_execution_mode": "paper_only",
        "metrics": {"total": 6, "expectancy_r": 0.25},
        "results": [
            _row("s1", "2024-01-01", r_multiple=-1.0, false_breakout=True, stop_hit=True, mfe=0.2, mae=-1.1),
            _row("s2", "2024-02-01", r_multiple=1.5, false_breakout=False, stop_hit=False, mfe=1.2, mae=-0.2),
            _row("s3", "2024-03-01", r_multiple=1.0, false_breakout=False, stop_hit=False, mfe=1.0, mae=-0.3),
            _row("s4", "2024-04-01", r_multiple=-1.0, false_breakout=True, stop_hit=True, mfe=0.4, mae=-1.2),
            _row("s5", "2024-05-01", r_multiple=2.0, false_breakout=False, stop_hit=False, mfe=2.0, mae=-0.1),
            _row("s6", "2024-06-01", r_multiple=1.0, false_breakout=False, stop_hit=False, mfe=1.2, mae=-0.4),
        ],
    }
    path = tmp_path / "real-data-backtest-evidence.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def test_bt133_analyzer_produces_research_only_variant_report(tmp_path: Path) -> None:
    report = analyze(_evidence(tmp_path))

    assert report.report_version == "bt133.v1"
    assert report.data_source == "real_data"
    assert report.is_demo is False
    assert report.live_trading_authorized is False
    assert report.broker_execution_mode == "paper_only"
    assert report.total_source_trades == 6
    assert set(report.walk_forward_periods) == {"training", "walk_forward", "out_of_sample"}
    assert any(item.variant_id == "baseline_breakout_trigger" for item in report.variant_results)
    assert any(item.family == "next_bar_close_confirmation" for item in report.variant_results)
    assert any(item.family == "volume_confirmed_breakout" for item in report.variant_results)
    assert any(item.family == "volatility_adjusted_confirmation" for item in report.variant_results)
    assert "Research only. No production entry rule change." in report.safety_notes


def test_bt133_variant_grid_contains_multiple_parameter_levels(tmp_path: Path) -> None:
    report = analyze(_evidence(tmp_path))

    next_bar_levels = [
        item.parameters["confirmation_delay_bars"]
        for item in report.variant_results
        if item.family == "next_bar_close_confirmation"
    ]
    volume_levels = [
        item.parameters["entry_volume_to_avg_volume_20_min"]
        for item in report.variant_results
        if item.family == "volume_confirmed_breakout"
    ]
    volatility_levels = [
        item.variant_id
        for item in report.variant_results
        if item.family == "volatility_adjusted_confirmation"
    ]

    assert next_bar_levels == [1, 2, 3]
    assert volume_levels == [1.1, 1.25, 1.5]
    assert len(volatility_levels) == 3


def test_bt133_missing_volume_fields_are_explicitly_skipped(tmp_path: Path) -> None:
    report = analyze(_evidence(tmp_path))

    volume_variants = [item for item in report.variant_results if item.family == "volume_confirmed_breakout"]

    assert volume_variants
    assert all(item.status == "SKIPPED_INSUFFICIENT_FIELDS" for item in volume_variants)
    assert all(item.recommendation == "NEEDS_MORE_DATA" for item in volume_variants)
    assert all(set(item.missing_fields) == {"avg_volume_20", "entry_volume"} for item in volume_variants)


def test_bt133_writes_json_and_markdown(tmp_path: Path) -> None:
    report = analyze(_evidence(tmp_path))
    output_json = tmp_path / "bt133.json"
    output_md = tmp_path / "bt133.md"

    write_report(report, output_json=output_json, output_md=output_md)

    payload = json.loads(output_json.read_text(encoding="utf-8"))
    markdown = output_md.read_text(encoding="utf-8")

    assert payload["report_version"] == "bt133.v1"
    assert payload["broker_execution_mode"] == "paper_only"
    assert "# BT133 Entry Confirmation Variant Report" in markdown
    assert "## Walk-forward Periods" in markdown
    assert "## Variant Results" in markdown
    assert render_markdown(report) == markdown


def test_bt133_refuses_demo_evidence(tmp_path: Path) -> None:
    path = _evidence(tmp_path)
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["is_demo"] = True
    path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(SystemExit, match="BT133 refuses demo evidence"):
        analyze(path)


def test_bt133_refuses_live_trading_authorization(tmp_path: Path) -> None:
    path = _evidence(tmp_path)
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["live_trading_authorized"] = True
    path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(SystemExit, match="BT133 requires live_trading_authorized=false"):
        analyze(path)


def test_bt133_flags_oos_degradation_as_overfit_risk(tmp_path: Path) -> None:
    path = _evidence(tmp_path)
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["results"] = [
        _row("s1", "2024-01-01", r_multiple=-1.0, false_breakout=True, stop_hit=True, mfe=0.2, mae=-1.1),
        _row("s2", "2024-02-01", r_multiple=2.0, false_breakout=False, stop_hit=False, mfe=1.5, mae=-0.2),
        _row("s3", "2024-03-01", r_multiple=1.5, false_breakout=False, stop_hit=False, mfe=1.2, mae=-0.3),
        _row("s4", "2024-04-01", r_multiple=1.0, false_breakout=False, stop_hit=False, mfe=1.0, mae=-0.4),
        _row("s5", "2024-05-01", r_multiple=-1.0, false_breakout=True, stop_hit=True, mfe=1.0, mae=-0.2),
        _row("s6", "2024-06-01", r_multiple=-1.0, false_breakout=True, stop_hit=True, mfe=1.0, mae=-0.3),
    ]
    path.write_text(json.dumps(payload), encoding="utf-8")

    report = analyze(path)

    assert any(item.recommendation == "OVERFIT_RISK" for item in report.variant_results)
    assert report.final_recommendation == "OVERFIT_RISK"
