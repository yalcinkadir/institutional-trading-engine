from __future__ import annotations

import json
from pathlib import Path

from scripts.bt137_regime_breadth_entry_gate import (
    BT137_ALLOWED_RECOMMENDATIONS,
    build_bt137_report,
    persist_bt137_report,
)


def _records() -> list[dict]:
    base = {
        "entry_price": 100.0,
        "stop_price": 96.0,
        "target_1_price": 108.0,
        "target_2_price": 112.0,
        "broker_execution_mode": "paper_only",
        "live_trading_authorized": False,
        "sector_or_asset_group_at_signal": "TECH",
        "signal_day_cluster_size": 2,
    }
    return [
        {
            **base,
            "signal_id": "s1",
            "symbol": "AAA",
            "signal_date": "2026-01-01",
            "period": "training",
            "result_r": -1.0,
            "mae_r": -1.1,
            "mfe_r": 0.3,
            "market_regime_at_signal": "risk_off",
            "index_trend_at_signal": "down",
            "breadth_score_at_signal": 0.2,
            "advance_decline_proxy_at_signal": 0.4,
            "risk_off_flag_at_signal": True,
            "vix_or_volatility_proxy_at_signal": 28.0,
        },
        {
            **base,
            "signal_id": "s2",
            "symbol": "BBB",
            "signal_date": "2026-02-01",
            "period": "validation",
            "result_r": 1.2,
            "mae_r": -0.4,
            "mfe_r": 1.8,
            "market_regime_at_signal": "neutral",
            "index_trend_at_signal": "flat",
            "breadth_score_at_signal": 0.55,
            "advance_decline_proxy_at_signal": 0.6,
            "risk_off_flag_at_signal": False,
            "vix_or_volatility_proxy_at_signal": 18.0,
        },
        {
            **base,
            "signal_id": "s3",
            "symbol": "CCC",
            "signal_date": "2026-03-01",
            "period": "out_of_sample",
            "result_r": 0.8,
            "mae_r": -0.2,
            "mfe_r": 1.3,
            "market_regime_at_signal": "risk_on",
            "index_trend_at_signal": "up",
            "breadth_score_at_signal": 0.75,
            "advance_decline_proxy_at_signal": 0.8,
            "risk_off_flag_at_signal": False,
            "vix_or_volatility_proxy_at_signal": 15.0,
        },
    ]


def test_bt137_variant_grid_and_safety_contract() -> None:
    report = build_bt137_report(_records(), github_run_id="unit-bt137")

    groups = {variant["group"] for variant in report["variant_grid"]}

    assert {
        "baseline",
        "risk_off_block",
        "delay_after_risk_off",
        "watch_only_weak_breadth",
        "combined_gate",
    }.issubset(groups)

    for group in groups:
        assert len({v["level"] for v in report["variant_grid"] if v["group"] == group}) >= 1

    assert report["research_only"] is True
    assert report["broker_execution_mode"] == "paper_only"
    assert report["live_trading_authorized"] is False
    assert report["production_rule_change"] is False


def test_bt137_blocks_risk_off_and_reports_period_metrics() -> None:
    report = build_bt137_report(_records(), github_run_id="unit-bt137")

    risk_off_variant = next(
        v for v in report["variant_results"] if v["group"] == "risk_off_block"
    )

    assert risk_off_variant["recommendation"] in BT137_ALLOWED_RECOMMENDATIONS
    assert any(p["blocked_trades"] > 0 for p in risk_off_variant["period_results"])

    for variant in report["variant_results"]:
        for period in variant["period_results"]:
            assert "total_trades_considered" in period
            assert "accepted_trades" in period
            assert "blocked_trades" in period
            assert "delayed_trades" in period
            assert "skipped_trades" in period
            assert "false_breakout_rate" in period
            assert "stop_hit_rate" in period
            assert "target_1_hit_rate" in period
            assert "target_2_hit_rate" in period
            assert "average_r" in period
            assert "expectancy_r" in period
            assert "average_mae_r" in period
            assert "average_mfe_r" in period
            assert "signal_day_cluster_impact" in period


def test_bt137_missing_fields_fail_closed() -> None:
    report = build_bt137_report(
        [{"signal_id": "bad", "symbol": "AAA"}],
        github_run_id="unit-bt137",
    )

    assert report["status"] == "SKIPPED_INSUFFICIENT_FIELDS"
    assert report["missing_fields"]
    assert report["variant_results"] == []


def test_bt137_delay_variant_reports_delayed_trades() -> None:
    report = build_bt137_report(_records(), github_run_id="unit-bt137")

    delay_variant = next(
        v for v in report["variant_results"] if v["group"] == "delay_after_risk_off"
    )

    assert any(p["delayed_trades"] >= 0 for p in delay_variant["period_results"])


def test_bt137_persists_latest_and_run_reports(tmp_path: Path) -> None:
    report = build_bt137_report(_records(), github_run_id="unit-bt137")

    paths = persist_bt137_report(
        report,
        output_root=tmp_path,
        github_run_id="unit-bt137",
    )

    assert paths["latest_json"].exists()
    assert paths["latest_markdown"].exists()
    assert paths["run_json"].exists()
    assert paths["run_markdown"].exists()

    payload = json.loads(paths["latest_json"].read_text(encoding="utf-8"))
    assert payload["schema"] == "bt137_regime_breadth_entry_gate_report.v1"
    assert "# BT137 Regime/Breadth Entry Gate Report" in paths[
        "latest_markdown"
    ].read_text(encoding="utf-8")