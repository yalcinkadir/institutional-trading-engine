import pandas as pd

from src.backtesting.historical_entry_exit_backtest import simulate_plan
from src.backtesting.historical_models import OUTCOME_EXPIRED, OUTCOME_STOP_HIT, HistoricalTradePlan


def _bars(rows: list[dict]) -> pd.DataFrame:
    return pd.DataFrame(rows)


def _plan(**overrides) -> HistoricalTradePlan:
    values = {
        "signal_id": "er_guard",
        "symbol": "TEST",
        "signal_date": "2026-01-01",
        "entry_trigger": 100.0,
        "stop_loss": 95.0,
        "target_1": 110.0,
        "target_2": 120.0,
        "exit_model": "t1_t2",
    }
    values.update(overrides)
    return HistoricalTradePlan(**values)


def test_er1_t1_t2_expiry_after_t1_closes_remaining_exposure_at_final_close() -> None:
    result = simulate_plan(
        _plan(),
        _bars(
            [
                {
                    "date": "2026-01-02",
                    "open": 99,
                    "high": 111,
                    "low": 99,
                    "close": 109,
                    "volume": 1,
                },
                {
                    "date": "2026-01-03",
                    "open": 109,
                    "high": 115,
                    "low": 108,
                    "close": 112,
                    "volume": 1,
                },
            ]
        ),
    )

    assert result.outcome == OUTCOME_EXPIRED
    assert result.entry_hit is True
    assert result.target_1_hit is True
    assert result.target_2_hit is False
    assert result.exit_date == "2026-01-03"
    assert result.exit_price == 112.0
    assert result.r_multiple == 2.4
    assert result.reason == "expired_after_target_1_without_target_2"


def test_er2_gap_through_entry_fills_at_worse_open_and_recomputes_risk() -> None:
    result = simulate_plan(
        _plan(target_1=120.0, target_2=130.0),
        _bars(
            [
                {
                    "date": "2026-01-02",
                    "open": 105,
                    "high": 121,
                    "low": 104,
                    "close": 120,
                    "volume": 1,
                }
            ]
        ),
    )

    assert result.entry_hit is True
    assert result.entry_date == "2026-01-02"
    assert result.exit_price == 120.0
    assert result.r_multiple == 1.5


def test_er2_breakeven_after_t1_gap_down_fills_at_worse_open_not_exact_entry() -> None:
    result = simulate_plan(
        _plan(stop_model="breakeven_after_t1"),
        _bars(
            [
                {
                    "date": "2026-01-02",
                    "open": 99,
                    "high": 111,
                    "low": 99,
                    "close": 110,
                    "volume": 1,
                },
                {
                    "date": "2026-01-03",
                    "open": 98,
                    "high": 100,
                    "low": 97,
                    "close": 98,
                    "volume": 1,
                },
            ]
        ),
    )

    assert result.outcome == OUTCOME_STOP_HIT
    assert result.target_1_hit is True
    assert result.stop_hit is True
    assert result.exit_price == 98.0
    assert result.r_multiple == -0.4
    assert result.reason == "breakeven_stop_after_t1"
