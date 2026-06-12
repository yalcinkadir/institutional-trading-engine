from __future__ import annotations

import json
from pathlib import Path

from src.backtesting.bt134_stop_loss_variant import (
    BT134_REQUIRED_VARIANT_GROUPS,
    build_bt134_report,
    persist_bt134_report,
)


def _sample_records() -> list[dict]:
    return [
        {
            "symbol": "AAPL",
            "date": "2026-01-10",
            "entry": 100.0,
            "stop_loss": 96.0,
            "target_1": 108.0,
            "target_2": 112.0,
            "atr14": 4.0,
            "high": 109.0,
            "low": 97.0,
            "close": 106.0,
            "period": "training",
        },
        {
            "symbol": "NVDA",
            "date": "2026-02-10",
            "entry": 200.0,
            "stop_loss": 190.0,
            "target_1": 220.0,
            "target_2": 230.0,
            "atr14": 9.0,
            "high": 221.0,
            "low": 188.0,
            "close": 194.0,
            "period": "validation",
        },
        {
            "symbol": "QQQ",
            "date": "2026-03-10",
            "entry": 500.0,
            "stop_loss": 490.0,
            "target_1": 520.0,
            "target_2": 530.0,
            "atr14": 8.0,
            "high": 515.0,
            "low": 492.0,
            "close": 510.0,
            "period": "out_of_sample",
        },
    ]


def test_bt134_variant_grid_contains_required_groups_and_multiple_levels() -> None:
    report = build_bt134_report(_sample_records(), github_run_id="unit-bt134")

    groups = {variant["group"] for variant in report["variant_grid"]}
    assert BT134_REQUIRED_VARIANT_GROUPS.issubset(groups)

    for group in BT134_REQUIRED_VARIANT_GROUPS:
        levels = {variant["level"] for variant in report["variant_grid"] if variant["group"] == group}
        assert len(levels) >= 2

    assert report["research_only"] is True
    assert report["broker_execution_mode"] == "paper_only"
    assert report["production_rule_change"] is False


def test_bt134_reports_each_period_and_same_bar_ambiguity() -> None:
    report = build_bt134_report(_sample_records(), github_run_id="unit-bt134")

    assert set(report["periods"]) == {"training", "validation", "out_of_sample"}
    assert report["same_bar_ambiguity_policy"] == "explicitly_reported"

    for variant in report["variant_results"]:
        period_names = {period["period"] for period in variant["period_results"]}
        assert {"training", "validation", "out_of_sample"}.issubset(period_names)
        for period in variant["period_results"]:
            assert "total" in period
            assert "stop_hit_rate" in period
            assert "target_1_hit_rate" in period
            assert "average_r" in period
            assert "expectancy_r" in period
            assert "skipped_count" in period
            assert "blocked_count" in period
            assert "same_bar_ambiguous_count" in period


def test_bt134_missing_fields_are_blocked_not_guessed() -> None:
    report = build_bt134_report(
        [{"symbol": "AAPL", "date": "2026-01-10", "entry": 100.0}],
        github_run_id="unit-bt134",
    )

    assert report["status"] == "SKIPPED_INSUFFICIENT_FIELDS"
    assert report["missing_fields"]
    assert report["variant_results"] == []


def test_bt134_oos_degradation_marks_overfit_or_reject() -> None:
    records = [
        {
            "symbol": "AAPL",
            "date": "2026-01-10",
            "entry": 100.0,
            "stop_loss": 96.0,
            "target_1": 108.0,
            "target_2": 112.0,
            "atr14": 4.0,
            "high": 112.0,
            "low": 98.0,
            "close": 111.0,
            "period": "training",
        },
        {
            "symbol": "AAPL",
            "date": "2026-02-10",
            "entry": 100.0,
            "stop_loss": 96.0,
            "target_1": 108.0,
            "target_2": 112.0,
            "atr14": 4.0,
            "high": 112.0,
            "low": 98.0,
            "close": 111.0,
            "period": "validation",
        },
        {
            "symbol": "AAPL",
            "date": "2026-03-10",
            "entry": 100.0,
            "stop_loss": 96.0,
            "target_1": 108.0,
            "target_2": 112.0,
            "atr14": 4.0,
            "high": 102.0,
            "low": 95.0,
            "close": 96.0,
            "period": "out_of_sample",
        },
    ]

    report = build_bt134_report(records, github_run_id="unit-bt134")

    recommendations = {variant["recommendation"] for variant in report["variant_results"]}
    assert "OVERFIT_RISK" in recommendations or "REJECT_VARIANT" in recommendations


def test_bt134_persists_latest_and_run_reports(tmp_path: Path) -> None:
    report = build_bt134_report(_sample_records(), github_run_id="unit-bt134")

    paths = persist_bt134_report(report, output_root=tmp_path, github_run_id="unit-bt134")

    assert paths["latest_json"].exists()
    assert paths["latest_markdown"].exists()
    assert paths["run_json"].exists()
    assert paths["run_markdown"].exists()

    payload = json.loads(paths["latest_json"].read_text(encoding="utf-8"))
    assert payload["schema"] == "bt134_stop_loss_variant_report.v1"
    assert "# BT134 Stop-Loss Variant Report" in paths["latest_markdown"].read_text(encoding="utf-8")
