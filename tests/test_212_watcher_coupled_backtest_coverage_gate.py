from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from src.backtesting.historical_models import HistoricalTradePlan
from src.backtesting.watcher_coupled_backtest import run_watcher_coupled_backtest

BT207_LATEST_REPORT = Path("reports/backtests/real_data/latest/bt207-watcher-coupled-lifecycle-report.json")


def _plan(index: int, symbol: str = "AAPL") -> HistoricalTradePlan:
    return HistoricalTradePlan(
        signal_id=f"bt212-{symbol.lower()}-{index:03d}",
        symbol=symbol,
        signal_date="2026-01-01",
        entry_trigger=100.0,
        stop_loss=95.0,
        target_1=110.0,
        target_2=120.0,
        valid_until="2026-01-10",
    )


def _bars_target_2() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {"date": "2026-01-02", "open": 99.0, "high": 101.0, "low": 98.0, "close": 100.5},
            {"date": "2026-01-03", "open": 106.0, "high": 111.0, "low": 104.0, "close": 110.0},
            {"date": "2026-01-04", "open": 116.0, "high": 121.0, "low": 114.0, "close": 120.5},
        ]
    )


def test_212_latest_one_plan_report_is_explicitly_not_production_ready() -> None:
    payload = json.loads(BT207_LATEST_REPORT.read_text(encoding="utf-8"))

    assert payload["input_plan_count"] == 1
    assert payload["production_rule_promotion_authorized"] is False
    assert payload["production_readiness_status"] == "BLOCKED_LOW_COVERAGE"
    assert "sample_below_minimum" in payload["production_readiness_blockers"]
    assert payload["coverage_metrics"]["min_required_plan_count"] == 30
    assert payload["coverage_metrics"]["input_plan_count"] == 1
    assert payload["coverage_metrics"]["distinct_symbol_count"] < 5


def test_212_runtime_report_marks_small_samples_as_low_coverage() -> None:
    report = run_watcher_coupled_backtest(
        [_plan(1)],
        bars_by_symbol={"AAPL": _bars_target_2()},
        run_id="bt212-small-sample",
    ).to_dict()

    assert report["production_readiness_status"] == "BLOCKED_LOW_COVERAGE"
    assert report["production_rule_promotion_authorized"] is False
    assert "sample_below_minimum" in report["production_readiness_blockers"]
    assert "symbol_coverage_below_minimum" in report["production_readiness_blockers"]
    assert report["coverage_metrics"]["input_plan_count"] == 1
    assert report["coverage_metrics"]["distinct_symbol_count"] == 1
    assert report["coverage_metrics"]["final_status_distribution"]["TARGET_2_HIT"] == 1


def test_212_runtime_report_exposes_distribution_metrics_for_large_samples() -> None:
    symbols = ["AAPL", "MSFT", "NVDA", "QQQ", "SPY"]
    plans = [_plan(index, symbols[index % len(symbols)]) for index in range(30)]
    bars_by_symbol = {symbol: _bars_target_2() for symbol in symbols}

    report = run_watcher_coupled_backtest(
        plans,
        bars_by_symbol=bars_by_symbol,
        run_id="bt212-large-sample",
    ).to_dict()

    assert report["coverage_metrics"]["input_plan_count"] == 30
    assert report["coverage_metrics"]["evaluated_plan_count"] == 30
    assert report["coverage_metrics"]["distinct_symbol_count"] == 5
    assert report["coverage_metrics"]["terminal_signal_count"] == 30
    assert report["coverage_metrics"]["final_status_distribution"]["TARGET_2_HIT"] == 30
    assert report["coverage_metrics"]["lifecycle_event_distribution"]["ENTRY_TRIGGERED"] == 30
    assert report["coverage_metrics"]["lifecycle_event_distribution"]["TARGET_1_HIT"] == 30
    assert report["coverage_metrics"]["lifecycle_event_distribution"]["TARGET_2_HIT"] == 30
    assert report["production_rule_promotion_authorized"] is False
