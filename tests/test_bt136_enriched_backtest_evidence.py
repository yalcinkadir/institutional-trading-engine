from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.backtesting.historical_entry_exit_backtest import run_backtest, simulate_plan
from src.backtesting.historical_models import HistoricalTradePlan


def _bars() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "date": "2024-01-01",
                "open": 100,
                "high": 101,
                "low": 99,
                "close": 100,
                "volume": 1000,
            },
            {
                "date": "2024-01-02",
                "open": 103,
                "high": 107,
                "low": 101,
                "close": 106,
                "volume": 1200,
            },
            {
                "date": "2024-01-03",
                "open": 106,
                "high": 112,
                "low": 104,
                "close": 111,
                "volume": 1300,
            },
        ]
    )


def test_bt136_result_contains_enriched_entry_stop_and_excursion_fields() -> None:
    plan = HistoricalTradePlan(
        signal_id="s1",
        symbol="AAPL",
        signal_date="2024-01-01",
        entry_trigger=102.0,
        stop_loss=98.0,
        target_1=110.0,
        target_2=115.0,
    )

    result = simulate_plan(plan, _bars(), signal_day_cluster_size=2)
    payload = result.to_dict()

    assert payload["entry_price"] == 103.0
    assert payload["entry_trigger"] == 102.0
    assert payload["initial_stop_loss"] == 98.0
    assert payload["target_1"] == 110.0
    assert payload["target_2"] == 115.0

    # Entry is filled at 103.0 because the first executable bar opens above the trigger.
    # Risk = 103.0 - 98.0 = 5.0
    # MFE = (112.0 - 103.0) / 5.0 = 1.8R
    # MAE = (101.0 - 103.0) / 5.0 = -0.4R
    assert payload["max_favorable_excursion_r"] == 1.8
    assert payload["max_adverse_excursion_r"] == -0.4

    assert payload["missing_field_reasons"] == {}
    assert payload["signal_day_cluster_size"] == 2
    assert payload["same_bar_ambiguous"] is False


def test_bt136_entry_not_hit_keeps_fields_null_with_missing_reasons() -> None:
    plan = HistoricalTradePlan(
        signal_id="s2",
        symbol="AAPL",
        signal_date="2024-01-01",
        entry_trigger=120.0,
        stop_loss=110.0,
        target_1=130.0,
    )

    result = simulate_plan(plan, _bars())
    payload = result.to_dict()

    assert payload["entry_hit"] is False
    assert payload["entry_price"] is None
    assert payload["max_favorable_excursion_r"] is None
    assert payload["max_adverse_excursion_r"] is None

    assert payload["missing_field_reasons"]["entry_price"] == "entry_not_hit"
    assert (
        payload["missing_field_reasons"]["max_favorable_excursion_r"]
        == "entry_not_hit_or_no_post_signal_bars"
    )
    assert (
        payload["missing_field_reasons"]["max_adverse_excursion_r"]
        == "entry_not_hit_or_no_post_signal_bars"
    )


def test_bt136_same_bar_ambiguity_is_marked_when_stop_and_target_are_inside_entry_bar() -> None:
    bars = pd.DataFrame(
        [
            {
                "date": "2024-01-01",
                "open": 100,
                "high": 101,
                "low": 99,
                "close": 100,
                "volume": 1000,
            },
            {
                "date": "2024-01-02",
                "open": 102,
                "high": 112,
                "low": 96,
                "close": 101,
                "volume": 1200,
            },
        ]
    )

    plan = HistoricalTradePlan(
        signal_id="s3",
        symbol="AAPL",
        signal_date="2024-01-01",
        entry_trigger=102.0,
        stop_loss=98.0,
        target_1=110.0,
        target_2=115.0,
    )

    result = simulate_plan(plan, bars)
    payload = result.to_dict()

    assert payload["entry_hit"] is True
    assert payload["stop_hit"] is True
    assert payload["same_bar_ambiguous"] is True
    assert payload["reason"] == "same_bar_stop_first"


def test_bt136_run_backtest_populates_signal_day_cluster_size(tmp_path: Path) -> None:
    bars_root = tmp_path / "bars"
    bars_root.mkdir()
    _bars().to_csv(bars_root / "AAPL.csv", index=False)

    plans = [
        HistoricalTradePlan(
            signal_id="s1",
            symbol="AAPL",
            signal_date="2024-01-01",
            entry_trigger=102.0,
            stop_loss=98.0,
            target_1=110.0,
        ),
        HistoricalTradePlan(
            signal_id="s2",
            symbol="AAPL",
            signal_date="2024-01-01",
            entry_trigger=103.0,
            stop_loss=98.0,
            target_1=110.0,
        ),
    ]

    report = run_backtest(
        plans,
        bars_root=bars_root,
        is_demo=False,
        data_source="real_data",
    )

    assert report.metrics.total == 2
    assert {result.signal_day_cluster_size for result in report.results} == {2}

    for result in report.results:
        payload = result.to_dict()
        assert "entry_price" in payload
        assert "max_favorable_excursion_r" in payload
        assert "max_adverse_excursion_r" in payload
        assert "missing_field_reasons" in payload