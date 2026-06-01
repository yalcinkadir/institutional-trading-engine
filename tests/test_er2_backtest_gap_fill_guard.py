from __future__ import annotations

import pandas as pd

from src.backtesting.historical_entry_exit_backtest import simulate_plan
from src.backtesting.historical_models import OUTCOME_TARGET_2_HIT, HistoricalTradePlan


def test_er2_gap_entry_uses_open_for_r_multiple() -> None:
    plan = HistoricalTradePlan(
        signal_id="er2",
        symbol="TEST",
        signal_date="2026-01-01",
        entry_trigger=100.0,
        stop_loss=95.0,
        target_1=110.0,
        target_2=120.0,
        exit_model="t1_t2",
    )
    bars = pd.DataFrame([
        {"date": "2026-01-02", "open": 105, "high": 121, "low": 104, "close": 120, "volume": 1},
    ])

    result = simulate_plan(plan, bars)

    assert result.outcome == OUTCOME_TARGET_2_HIT
    assert result.exit_price == 120
    assert result.r_multiple == 1.5
