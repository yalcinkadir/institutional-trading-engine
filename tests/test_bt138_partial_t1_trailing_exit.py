from __future__ import annotations

import json
from pathlib import Path

from scripts.bt138_partial_t1_trailing_exit import build_bt138_report, persist_bt138_report


def _records() -> list[dict]:
    base = {"entry_price": 100.0, "stop_price": 96.0, "target_1_price": 108.0, "target_2_price": 112.0, "atr14_at_signal": 4.0, "atr14_during_trade": 4.0, "broker_execution_mode": "paper_only", "live_trading_authorized": False, "fees_or_slippage_assumption": 0.0}
    return [
        {**base, "signal_id": "t1", "symbol": "AAA", "signal_date": "2026-01-01", "period": "training", "bars_after_entry": 5, "high_after_entry": 113.0, "low_after_entry": 99.0, "close_after_entry": 111.0, "first_t1_hit_at": "b2", "first_t2_hit_at": "b5", "first_stop_hit_at": None, "same_bar_stop_target_ambiguity": False, "mae_r": -0.25, "mfe_r": 3.25, "baseline_result_r": 2.0},
        {**base, "signal_id": "t2", "symbol": "BBB", "signal_date": "2026-02-01", "period": "validation", "bars_after_entry": 4, "high_after_entry": 109.0, "low_after_entry": 96.0, "close_after_entry": 97.0, "first_t1_hit_at": "b1", "first_t2_hit_at": None, "first_stop_hit_at": "b4", "same_bar_stop_target_ambiguity": False, "mae_r": -1.0, "mfe_r": 2.25, "baseline_result_r": -1.0},
        {**base, "signal_id": "t3", "symbol": "CCC", "signal_date": "2026-03-01", "period": "out_of_sample", "bars_after_entry": 3, "high_after_entry": 107.0, "low_after_entry": 95.0, "close_after_entry": 96.0, "first_t1_hit_at": None, "first_t2_hit_at": None, "first_stop_hit_at": "b2", "same_bar_stop_target_ambiguity": True, "mae_r": -1.25, "mfe_r": 1.75, "baseline_result_r": -1.0},
    ]


def test_bt138_variant_grid_and_safety_contract() -> None:
    report = build_bt138_report(_records(), github_run_id="unit-bt138")
    groups = {variant["group"] for variant in report["variant_grid"]}
    assert {"baseline", "partial_t1", "atr_runner", "breakeven_trail", "no_partial_runner", "same_bar_conservative"}.issubset(groups)
    assert {0.25, 0.33, 0.50, 0.66}.issubset({v["partial_size"] for v in report["variant_grid"] if v.get("partial_size") is not None})
    assert report["research_only"] is True
    assert report["broker_execution_mode"] == "paper_only"
    assert report["live_trading_authorized"] is False
    assert report["production_rule_change"] is False


def test_bt138_partial_runner_metrics_are_reported() -> None:
    report = build_bt138_report(_records(), github_run_id="unit-bt138")
    variant = next(v for v in report["variant_results"] if v["group"] == "partial_t1")
    assert any(p["t1_hit_count"] > 0 for p in variant["period_results"])
    assert any(p["t1_giveback_count"] > 0 for p in variant["period_results"])
    for period in variant["period_results"]:
        assert "accepted_runner_trades" in period
        assert "tail_contribution_r" in period
        assert "same_bar_ambiguity_count" in period
        assert "median_r" in period


def test_bt138_missing_fields_fail_closed() -> None:
    report = build_bt138_report([{"signal_id": "bad", "symbol": "AAA"}], github_run_id="unit-bt138")
    assert report["status"] == "SKIPPED_INSUFFICIENT_FIELDS"
    assert report["missing_fields"]
    assert report["variant_results"] == []


def test_bt138_persists_reports(tmp_path: Path) -> None:
    report = build_bt138_report(_records(), github_run_id="unit-bt138")
    paths = persist_bt138_report(report, output_root=tmp_path, github_run_id="unit-bt138")
    assert paths["latest_json"].exists()
    assert paths["latest_markdown"].exists()
    assert paths["run_json"].exists()
    assert paths["run_markdown"].exists()
    payload = json.loads(paths["latest_json"].read_text(encoding="utf-8"))
    assert payload["schema"] == "bt138_partial_t1_trailing_exit_report.v1"
    assert "# BT138 Partial-at-T1 + Trailing-Exit Report" in paths["latest_markdown"].read_text(encoding="utf-8")
