from __future__ import annotations

import json
from pathlib import Path

from scripts.bt135_symbol_selection_sensitivity import (
    BT135_ALLOWED_RECOMMENDATIONS,
    build_bt135_report,
    persist_bt135_report,
)


def _records_many_per_symbol() -> list[dict]:
    records: list[dict] = []
    for i in range(12):
        period = "training" if i < 8 else "out_of_sample"
        records.append({"symbol": "AAA", "date": f"2026-01-{i+1:02d}", "period": period, "r": 1.0, "outcome": "win", "signal_day": f"d{i}"})
        records.append({"symbol": "BBB", "date": f"2026-01-{i+1:02d}", "period": period, "r": -0.8, "outcome": "loss", "signal_day": f"d{i}"})
    return records


def test_bt135_reports_required_variants_and_downweight_levels() -> None:
    report = build_bt135_report(_records_many_per_symbol(), github_run_id="unit-bt135")
    variant_names = {variant["variant"] for variant in report["variant_results"]}
    assert "baseline_full_universe" in variant_names
    assert "exclude_worst_symbol_only" in variant_names
    assert "exclude_negative_expectancy_symbols" in variant_names
    assert "best_symbol_only_sanity_check" in variant_names
    downweight_levels = {variant["downweight_level"] for variant in report["variant_results"] if variant["group"] == "downweight_worst_symbols"}
    assert {0.25, 0.50, 0.75}.issubset(downweight_levels)
    assert report["research_only"] is True
    assert report["broker_execution_mode"] == "paper_only"
    assert report["production_rule_change"] is False


def test_bt135_negative_expectancy_exclusion_is_reported() -> None:
    report = build_bt135_report(_records_many_per_symbol(), github_run_id="unit-bt135")
    exclude_variant = next(item for item in report["variant_results"] if item["variant"] == "exclude_negative_expectancy_symbols")
    assert "BBB" in exclude_variant["symbols_excluded"]
    assert "AAA" in exclude_variant["symbols_included"]
    assert exclude_variant["recommendation"] in BT135_ALLOWED_RECOMMENDATIONS


def test_bt135_small_sample_forces_needs_more_data() -> None:
    report = build_bt135_report([
        {"symbol": "AAA", "date": "2026-01-01", "period": "training", "r": 1.0, "outcome": "win", "signal_day": "d1"},
        {"symbol": "BBB", "date": "2026-01-02", "period": "out_of_sample", "r": -1.0, "outcome": "loss", "signal_day": "d2"},
    ], github_run_id="unit-bt135")
    assert report["concentration_risk_warning"] is True
    assert report["low_effective_sample_size_warning"] is True
    for variant in report["variant_results"]:
        assert variant["recommendation"] == "NEEDS_MORE_DATA"


def test_bt135_missing_fields_are_blocked_not_guessed() -> None:
    report = build_bt135_report([{"symbol": "AAA", "date": "2026-01-01"}], github_run_id="unit-bt135")
    assert report["status"] == "SKIPPED_INSUFFICIENT_FIELDS"
    assert report["missing_fields"]
    assert report["variant_results"] == []


def test_bt135_persists_latest_and_run_reports(tmp_path: Path) -> None:
    report = build_bt135_report(_records_many_per_symbol(), github_run_id="unit-bt135")
    paths = persist_bt135_report(report, output_root=tmp_path, github_run_id="unit-bt135")
    assert paths["latest_json"].exists()
    assert paths["latest_markdown"].exists()
    assert paths["run_json"].exists()
    assert paths["run_markdown"].exists()
    payload = json.loads(paths["latest_json"].read_text(encoding="utf-8"))
    assert payload["schema"] == "bt135_symbol_selection_sensitivity_report.v1"
    assert "# BT135 Symbol Selection Sensitivity Report" in paths["latest_markdown"].read_text(encoding="utf-8")
