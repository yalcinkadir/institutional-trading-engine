from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.backtesting_framework import (  # noqa: E402
    BacktestSignal,
    run_backtest,
)

JAN_1_2024_MS = 1704067200000
DAY_MS = 86400000


def _bars(start=100.0, drift=1.5, count=30):
    bars = []
    close = start

    for index in range(count):
        close += drift
        bars.append(
            {
                "t": JAN_1_2024_MS + (index * DAY_MS),
                "c": round(close, 2),
                "h": round(close + 2, 2),
                "l": round(close - 2, 2),
            }
        )

    return bars


def test_backtest_generates_positive_equity_curve_for_winning_signals():
    report = run_backtest(
        signals=[
            BacktestSignal(
                timestamp_utc="2024-01-01T00:00:00+00:00",
                symbol="NVDA",
                market_state="low_vol_bull",
                setup_type="momentum_breakout",
                decision="approved",
                risk_tier="tier_1",
                entry_price=100.0,
                position_size_multiplier=1.0,
                holding_days=5,
            )
        ],
        bars_by_symbol={"NVDA": _bars()},
    )

    assert report.summary.trades == 1
    assert report.summary.total_return > 0
    assert report.equity_curve[-1] > report.equity_curve[0]


def test_backtest_groups_performance_by_setup_and_regime():
    report = run_backtest(
        signals=[
            BacktestSignal(
                timestamp_utc="2024-01-01T00:00:00+00:00",
                symbol="NVDA",
                market_state="low_vol_bull",
                setup_type="momentum_breakout",
                decision="approved",
                risk_tier="tier_1",
                entry_price=100.0,
                position_size_multiplier=1.0,
                holding_days=5,
            ),
            BacktestSignal(
                timestamp_utc="2024-01-02T00:00:00+00:00",
                symbol="MSFT",
                market_state="low_vol_bull",
                setup_type="pullback_continuation",
                decision="approved",
                risk_tier="tier_2",
                entry_price=100.0,
                position_size_multiplier=0.5,
                holding_days=5,
            ),
        ],
        bars_by_symbol={
            "NVDA": _bars(),
            "MSFT": _bars(start=90.0, drift=1.0),
        },
    )

    assert "momentum_breakout" in report.performance_by_setup
    assert "pullback_continuation" in report.performance_by_setup
    assert "low_vol_bull" in report.performance_by_regime
