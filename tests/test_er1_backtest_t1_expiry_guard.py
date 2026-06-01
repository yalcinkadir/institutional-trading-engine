from __future__ import annotations

import pandas as pd

from src.backtesting.historical_entry_exit_backtest import simulate_plan
from src.backtesting.historical_models import OUTCOME_EXPIRED, HistoricalTradePlan


def test_er1_t1_without_t2_uses_final_close() -> None:
    plan = HistoricalTradePlan(
        signal_id="er1",
        symbol="TEST",
        signal_date="2026-01-01",
        entry_trigger=100.0,
        stop_loss=95.0,
        target_1=110.0,
        target_2=120.0,
        exit_model="t1_t2",
    )
    bars = pd.DataFrame([
        {"date": "2026-01-02", "open": 99, "high": 105, "low": 99, "close": 104, "volume": 1},
        {"date": "2026-01-03", "open": 104, "high": 111, "low": 103, "close": 110, "volume": 1},
        {"date": "2026-01-04", "open": 106, "high": 109, "low": 97, "close": 98, "volume": 1},
    ])

    result = simulate_plan(plan, bars, max_bars=3)

    assert result.outcome == OUTCOME_EXPIRED
    assert result.target_1_hit is True
    assert result.target_2_hit is False
    assert result.exit_price == 98
    assert result.r_multiple == -0.4
    assert result.reason == "expired_after_target_1_without_target_2"
