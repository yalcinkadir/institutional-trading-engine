from __future__ import annotations

import pandas as pd
import pytest

from src.backtesting.historical_models import HistoricalTradePlan
from src.backtesting.watcher_coupled_backtest import run_watcher_coupled_backtest


def _plan() -> HistoricalTradePlan:
    return HistoricalTradePlan(
        signal_id="sig-watch-001",
        symbol="AAPL",
        signal_date="2026-01-01",
        entry_trigger=100.0,
        stop_loss=95.0,
        target_1=110.0,
        target_2=120.0,
        valid_until="2026-01-10",
    )


def _bars() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {"date": "2026-01-02", "open": 99.0, "high": 101.0, "low": 98.0, "close": 100.5},
            {"date": "2026-01-03", "open": 106.0, "high": 111.0, "low": 104.0, "close": 110.0},
            {"date": "2026-01-04", "open": 116.0, "high": 121.0, "low": 114.0, "close": 120.5},
        ]
    )


def test_207_replays_historical_bars_through_watcher_lifecycle_engine() -> None:
    report = run_watcher_coupled_backtest(
        [_plan()],
        bars_by_symbol={"AAPL": _bars()},
        run_id="bt207-unit",
    )

    payload = report.to_dict()
    result = payload["results"][0]

    assert payload["backtest_coupling"] == "watcher_lifecycle_replay"
    assert payload["watcher_engine"] == "src.watchers.entry_exit_watcher.evaluate_signals"
    assert payload["live_trading_authorized"] is False
    assert payload["broker_execution_mode"] == "paper_only"
    assert payload["input_plan_count"] == 1
    assert payload["evaluated_plan_count"] == 1
    assert payload["lifecycle_event_count"] >= 3
    assert payload["terminal_signal_count"] == 1
    assert result["final_status"] == "TARGET_2_HIT"
    assert result["terminal"] is True
    assert [event["event_type"] for event in result["lifecycle_events"][:3]] == [
        "ENTRY_TRIGGERED",
        "TARGET_1_HIT",
        "TARGET_2_HIT",
    ]


def test_207_uses_conservative_watcher_ordering() -> None:
    ambiguous_bars = pd.DataFrame(
        [
            {"date": "2026-01-02", "open": 100.0, "high": 111.0, "low": 94.0, "close": 96.0},
        ]
    )

    report = run_watcher_coupled_backtest([_plan()], bars_by_symbol={"AAPL": ambiguous_bars})
    result = report.to_dict()["results"][0]

    assert result["final_status"] == "INVALIDATED_BEFORE_ENTRY"
    assert result["terminal"] is True
    assert result["lifecycle_events"][0]["event_type"] == "INVALIDATED_BEFORE_ENTRY"


def test_207_blocks_runtime_authorization_flag() -> None:
    with pytest.raises(ValueError, match="must not authorize"):
        run_watcher_coupled_backtest(
            [_plan()],
            bars_by_symbol={"AAPL": _bars()},
            live_trading_authorized=True,
        )


def test_207_blocks_non_paper_mode() -> None:
    with pytest.raises(ValueError, match="paper_only"):
        run_watcher_coupled_backtest(
            [_plan()],
            bars_by_symbol={"AAPL": _bars()},
            broker_execution_mode="production",
        )
