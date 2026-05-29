import pandas as pd
import pytest

from src.backtesting.historical_entry_exit_backtest import (
    BacktestExecutionConfig,
    simulate_plan,
)
from src.backtesting.historical_models import (
    OUTCOME_STOP_HIT,
    OUTCOME_TARGET_1_HIT,
    HistoricalTradePlan,
)


def _plan(**overrides):
    base = dict(
        signal_id="s1",
        symbol="X",
        signal_date="2024-01-01",
        entry_trigger=100.0,
        stop_loss=95.0,
        target_1=110.0,
        target_2=120.0,
    )
    base.update(overrides)
    return HistoricalTradePlan(**base)


def _bars(rows):
    return pd.DataFrame(rows, columns=["date", "open", "high", "low", "close", "volume"])


def test_unsupported_stop_model_fails_closed() -> None:
    plan = _plan(stop_model="trailing_chandelier")

    with pytest.raises(ValueError, match="unsupported stop_model"):
        simulate_plan(plan, _bars([["2024-01-02", 100, 101, 99, 100, 1]]))


def test_unsupported_exit_model_fails_closed() -> None:
    plan = _plan(exit_model="scale_out_unknown")

    with pytest.raises(ValueError, match="unsupported exit_model"):
        simulate_plan(plan, _bars([["2024-01-02", 100, 101, 99, 100, 1]]))


def test_gap_through_stop_is_worse_than_minus_1r() -> None:
    plan = _plan()
    bars = _bars(
        [
            ["2024-01-02", 100, 105, 99, 104, 1],
            ["2024-01-03", 80, 82, 78, 81, 1],
        ]
    )

    result = simulate_plan(plan, bars, cfg=BacktestExecutionConfig(model_stop_gaps=True))

    assert result.outcome == OUTCOME_STOP_HIT
    assert result.exit_price == 80.0
    assert result.r_multiple < -1.0


def test_breakeven_after_t1_caps_loss_at_zero() -> None:
    plan = _plan(stop_model="breakeven_after_t1")
    bars = _bars(
        [
            ["2024-01-02", 100, 111, 99, 109, 1],
            ["2024-01-03", 108, 109, 90, 95, 1],
        ]
    )

    result = simulate_plan(plan, bars)

    assert result.outcome == OUTCOME_STOP_HIT
    assert result.target_1_hit is True
    assert result.exit_price == 100.0
    assert result.r_multiple == 0.0
    assert result.reason == "breakeven_stop_after_t1"


def test_target_1_only_exit_date_is_actual_hit_bar() -> None:
    plan = _plan(exit_model="t1_only")
    bars = _bars(
        [
            ["2024-01-02", 100, 111, 99, 110, 1],
            ["2024-01-03", 110, 112, 108, 111, 1],
            ["2024-01-04", 111, 113, 109, 112, 1],
        ]
    )

    result = simulate_plan(plan, bars)

    assert result.outcome == OUTCOME_TARGET_1_HIT
    assert result.exit_date == "2024-01-02"
    assert result.reason == "target_1_only_exit"
