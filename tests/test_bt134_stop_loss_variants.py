from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.analyze_bt134_stop_loss_variants import analyze, render_markdown, write_report


def _row(
    signal_id: str,
    signal_date: str,
    *,
    r_multiple: float,
    stop_hit: bool,
    mfe: float,
    mae: float,
    same_bar: bool = False,
    atr: float | None = None,
    entry_hit: bool = True,
) -> dict:
    return {
        "signal_id": signal_id,
        "symbol": "AAA",
        "signal_date": signal_date,
        "outcome": "STOP_HIT" if stop_hit else "TARGET_1_HIT",
        "entry_hit": entry_hit,
        "target_1_hit": r_multiple > 0,
        "target_2_hit": r_multiple >= 2,
        "stop_hit": stop_hit,
        "false_breakout": stop_hit,
        "r_multiple": r_multiple,
        "bars_evaluated": 5,
        "entry_price": 100.0,
        "entry_trigger": 100.0,
        "initial_stop_loss": 95.0,
        "target_1": 110.0,
        "target_2": 115.0,
        "atr14_at_signal": atr,
        "max_favorable_excursion_r": mfe,
        "max_adverse_excursion_r": mae,
        "same_bar_ambiguous": same_bar,
        "missing_field_reasons": {},
        "signal_day_cluster_size": 1,
    }


def _evidence(tmp_path: Path, *, include_atr: bool = False) -> Path:
    atr = 2.5 if include_atr else None
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
            _row("s1", "2024-01-01", r_multiple=-1.0, stop_hit=True, mfe=0.2, mae=-1.1, atr=atr),
            _row("s2", "2024-02-01", r_multiple=1.5, stop_hit=False, mfe=1.2, mae=-0.2, atr=atr),
            _row("s3", "2024-03-01", r_multiple=1.0, stop_hit=False, mfe=1.0, mae=-0.3, same_bar=True, atr=atr),
            _row("s4", "2024-04-01", r_multiple=-1.0, stop_hit=True, mfe=0.4, mae=-1.2, atr=atr),
            _row("s5", "2024-05-01", r_multiple=2.0, stop_hit=False, mfe=2.0, mae=-0.1, atr=atr),
            _row("s6", "2024-06-01", r_multiple=1.0, stop_hit=False, mfe=1.2, mae=-0.4, same_bar=True, atr=atr),
        ],
    }
    path = tmp_path / "real-data-backtest-evidence.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def test_bt134_analyzer_produces_research_only_stop_variant_report(tmp_path: Path) -> None:
    report = analyze(_evidence(tmp_path))

    assert report.report_version == "bt134.v1"
    assert report.data_source == "real_data"
    assert report.is_demo is False
    assert report.live_trading_authorized is False
    assert report.broker_execution_mode == "paper_only"
    assert report.production_rule_change_allowed is False
    assert report.total_source_trades == 6
    assert set(report.walk_forward_periods) == {"training", "walk_forward", "out_of_sample"}
    assert any(item.variant_id == "baseline_fixed_stop" for item in report.variant_results)
    assert any(item.family == "wider_fixed_stop" for item in report.variant_results)
    assert any(item.family == "atr_stop" for item in report.variant_results)
    assert any(item.family == "same_bar_handling" for item in report.variant_results)
    assert "Research only. No production stop rule change." in report.safety_notes


def test_bt134_variant_grid_contains_multiple_parameter_levels(tmp_path: Path) -> None:
    report = analyze(_evidence(tmp_path, include_atr=True))

    wider_levels = [
        item.parameters["stop_risk_multiplier"]
        for item in report.variant_results
        if item.family == "wider_fixed_stop"
    ]
    atr_levels = [
        item.parameters["atr_multiple"]
        for item in report.variant_results
        if item.family == "atr_stop"
    ]
    same_bar_modes = [
        item.parameters["same_bar_mode"]
        for item in report.variant_results
        if item.family == "same_bar_handling"
    ]

    assert wider_levels == [1.0, 1.25, 1.5]
    assert atr_levels == [1.0, 1.5, 2.0]
    assert same_bar_modes == ["stop_first", "target_first", "conservative_blocked"]


def test_bt134_missing_atr_fields_are_explicitly_skipped(tmp_path: Path) -> None:
    report = analyze(_evidence(tmp_path, include_atr=False))

    atr_variants = [item for item in report.variant_results if item.family == "atr_stop"]

    assert atr_variants
    assert all(item.status == "SKIPPED_INSUFFICIENT_FIELDS" for item in atr_variants)
    assert all(item.recommendation == "NEEDS_MORE_DATA" for item in atr_variants)
    assert all(item.missing_fields == ["atr14_at_signal"] for item in atr_variants)


def test_bt134_same_bar_handling_reports_blocked_and_ambiguous_counts(tmp_path: Path) -> None:
    report = analyze(_evidence(tmp_path, include_atr=True))

    blocked_variant = next(
        item
        for item in report.variant_results
        if item.variant_id == "same_bar_handling_conservative_blocked"
    )

    assert blocked_variant.status == "EVALUATED"
    assert sum(period.same_bar_ambiguous_trades for period in blocked_variant.periods) == 2
    assert sum(period.blocked_trades for period in blocked_variant.periods) == 2


def test_bt134_flags_oos_degradation_as_overfit_risk(tmp_path: Path) -> None:
    path = _evidence(tmp_path, include_atr=True)
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["results"] = [
        _row("s1", "2024-01-01", r_multiple=-1.0, stop_hit=True, mfe=0.2, mae=-1.1, atr=2.5),
        _row("s2", "2024-02-01", r_multiple=2.0, stop_hit=False, mfe=1.5, mae=-0.2, atr=2.5),
        _row("s3", "2024-03-01", r_multiple=1.5, stop_hit=False, mfe=1.2, mae=-0.3, atr=2.5),
        _row("s4", "2024-04-01", r_multiple=1.0, stop_hit=False, mfe=1.0, mae=-0.4, atr=2.5),
        _row("s5", "2024-05-01", r_multiple=-1.0, stop_hit=True, mfe=0.4, mae=-1.5, atr=2.5),
        _row("s6", "2024-06-01", r_multiple=-1.0, stop_hit=True, mfe=0.4, mae=-1.4, atr=2.5),
    ]
    path.write_text(json.dumps(payload), encoding="utf-8")

    report = analyze(path)

    assert any(item.recommendation == "OVERFIT_RISK" for item in report.variant_results)
    assert report.final_recommendation == "OVERFIT_RISK"


def test_bt134_writes_json_and_markdown(tmp_path: Path) -> None:
    report = analyze(_evidence(tmp_path, include_atr=True))
    output_json = tmp_path / "bt134.json"
    output_md = tmp_path / "bt134.md"

    write_report(report, output_json=output_json, output_md=output_md)

    payload = json.loads(output_json.read_text(encoding="utf-8"))
    markdown = output_md.read_text(encoding="utf-8")

    assert payload["report_version"] == "bt134.v1"
    assert payload["broker_execution_mode"] == "paper_only"
    assert payload["production_rule_change_allowed"] is False
    assert "# BT134 Stop-Loss Variant Report" in markdown
    assert "## Walk-forward Periods" in markdown
    assert "## Variant Results" in markdown
    assert render_markdown(report) == markdown


def test_bt134_refuses_demo_evidence(tmp_path: Path) -> None:
    path = _evidence(tmp_path)
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["is_demo"] = True
    path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(SystemExit, match="BT134 refuses demo evidence"):
        analyze(path)


def test_bt134_refuses_live_trading_authorization(tmp_path: Path) -> None:
    path = _evidence(tmp_path)
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["live_trading_authorized"] = True
    path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(SystemExit, match="BT134 requires live_trading_authorized=false"):
        analyze(path)
