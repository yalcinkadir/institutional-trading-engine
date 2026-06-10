from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.analyze_bt176_guarded_entry_confirmation_experiment import (
    analyze,
    render_markdown,
    write_report,
)


def _row(
    signal_id: str,
    *,
    r_multiple: float,
    false_breakout: bool,
    stop_hit: bool,
    mfe: float,
    mae: float,
    bars: int = 5,
    entry_hit: bool = True,
) -> dict:
    return {
        "signal_id": signal_id,
        "symbol": "AAA",
        "signal_date": "2024-01-01",
        "entry_hit": entry_hit,
        "target_1_hit": r_multiple > 0,
        "target_2_hit": r_multiple >= 2,
        "stop_hit": stop_hit,
        "false_breakout": false_breakout,
        "r_multiple": r_multiple,
        "bars_evaluated": bars,
        "max_favorable_excursion_r": mfe,
        "max_adverse_excursion_r": mae,
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
        "results": [
            _row("s1", r_multiple=-1.0, false_breakout=True, stop_hit=True, mfe=0.2, mae=-1.2),
            _row("s2", r_multiple=1.5, false_breakout=False, stop_hit=False, mfe=1.2, mae=-0.2),
            _row("s3", r_multiple=2.0, false_breakout=False, stop_hit=False, mfe=2.0, mae=-0.1),
            _row("s4", r_multiple=-1.0, false_breakout=True, stop_hit=True, mfe=0.1, mae=-1.1),
        ],
    }
    path = tmp_path / "real-data-backtest-evidence.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def _variant_report(tmp_path: Path) -> Path:
    payload = {
        "final_recommendation": "PROMOTE_TO_GUARDED_EXPERIMENT",
        "live_trading_authorized": False,
        "broker_execution_mode": "paper_only",
        "variant_results": [
            {
                "variant_id": "next_bar_close_confirmation_1bar",
                "family": "next_bar_close_confirmation",
                "status": "EVALUATED",
                "recommendation": "PROMOTE_TO_GUARDED_EXPERIMENT",
                "missing_fields": [],
                "parameters": {"confirmation_delay_bars": 1, "minimum_mfe_r": 0.25},
            },
            {
                "variant_id": "next_bar_close_confirmation_3bar",
                "family": "next_bar_close_confirmation",
                "status": "EVALUATED",
                "recommendation": "PROMOTE_TO_GUARDED_EXPERIMENT",
                "missing_fields": [],
                "parameters": {"confirmation_delay_bars": 3, "minimum_mfe_r": 0.75},
            },
        ],
    }
    path = tmp_path / "bt133-entry-confirmation-variant-report.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def test_bt176_selects_simplest_promoted_next_bar_candidate_and_reports_before_after(tmp_path: Path) -> None:
    report = analyze(evidence_path=_evidence(tmp_path), variant_report_path=_variant_report(tmp_path))

    assert report.report_version == "bt176.v1"
    assert report.candidate_variant_id == "next_bar_close_confirmation_1bar"
    assert report.candidate_family == "next_bar_close_confirmation"
    assert report.guard_status == "READY_FOR_PAPER_SHADOW"
    assert report.experiment_scope == "paper_observation_shadow_only"
    assert report.production_rule_change_allowed is False
    assert report.live_trading_authorized is False
    assert report.broker_execution_mode == "paper_only"
    assert report.baseline_metrics.total_trades_considered == 4
    assert report.baseline_metrics.accepted_trades == 4
    assert report.guarded_experiment_metrics.accepted_trades == 2
    assert report.guarded_experiment_metrics.filtered_trades == 2
    assert report.guarded_experiment_metrics.false_breakout_rate == 0.0
    assert report.guarded_experiment_metrics.stop_hit_rate == 0.0
    assert report.guarded_experiment_metrics.expectancy_r == 1.75


def test_bt176_writes_reviewable_json_and_markdown(tmp_path: Path) -> None:
    report = analyze(evidence_path=_evidence(tmp_path), variant_report_path=_variant_report(tmp_path))
    output_json = tmp_path / "bt176.json"
    output_md = tmp_path / "bt176.md"

    write_report(report, output_json=output_json, output_md=output_md)

    payload = json.loads(output_json.read_text(encoding="utf-8"))
    markdown = output_md.read_text(encoding="utf-8")

    assert payload["report_version"] == "bt176.v1"
    assert payload["broker_execution_mode"] == "paper_only"
    assert payload["production_rule_change_allowed"] is False
    assert "# BT176 Guarded Entry Confirmation Experiment" in markdown
    assert "Baseline vs Guarded Experiment" in markdown
    assert "No live trading authorization" in markdown
    assert render_markdown(report) == markdown


def test_bt176_blocks_candidate_when_guarded_metrics_are_worse_than_baseline(tmp_path: Path) -> None:
    evidence_path = _evidence(tmp_path)
    payload = json.loads(evidence_path.read_text(encoding="utf-8"))
    payload["results"] = [
        _row("s1", r_multiple=1.0, false_breakout=False, stop_hit=False, mfe=0.1, mae=-0.2),
        _row("s2", r_multiple=-1.0, false_breakout=True, stop_hit=True, mfe=1.0, mae=-0.2),
        _row("s3", r_multiple=-1.0, false_breakout=True, stop_hit=True, mfe=1.2, mae=-0.2),
    ]
    evidence_path.write_text(json.dumps(payload), encoding="utf-8")

    report = analyze(evidence_path=evidence_path, variant_report_path=_variant_report(tmp_path))

    assert report.guard_status == "BLOCKED"
    assert "candidate_variant_worsens_stop_hit_rate" in report.guard_reasons
    assert "candidate_variant_worsens_false_breakout_rate" in report.guard_reasons
    assert "candidate_variant_expectancy_below_baseline" in report.guard_reasons


def test_bt176_refuses_demo_or_live_authorized_evidence(tmp_path: Path) -> None:
    evidence_path = _evidence(tmp_path)
    payload = json.loads(evidence_path.read_text(encoding="utf-8"))
    payload["is_demo"] = True
    evidence_path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(SystemExit, match="BT176 refuses demo evidence"):
        analyze(evidence_path=evidence_path, variant_report_path=_variant_report(tmp_path))

    payload["is_demo"] = False
    payload["live_trading_authorized"] = True
    evidence_path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(SystemExit, match="BT176 requires live_trading_authorized=false"):
        analyze(evidence_path=evidence_path, variant_report_path=_variant_report(tmp_path))


def test_bt176_refuses_unpromoted_or_missing_field_candidate(tmp_path: Path) -> None:
    variant_path = _variant_report(tmp_path)
    payload = json.loads(variant_path.read_text(encoding="utf-8"))
    payload["variant_results"][0]["recommendation"] = "NEEDS_MORE_DATA"
    variant_path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(SystemExit, match="candidate variant is not promoted"):
        analyze(evidence_path=_evidence(tmp_path), variant_report_path=variant_path)

    payload["variant_results"][0]["recommendation"] = "PROMOTE_TO_GUARDED_EXPERIMENT"
    payload["variant_results"][0]["missing_fields"] = ["max_favorable_excursion_r"]
    variant_path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(SystemExit, match="candidate variant has missing fields"):
        analyze(evidence_path=_evidence(tmp_path), variant_report_path=variant_path)
