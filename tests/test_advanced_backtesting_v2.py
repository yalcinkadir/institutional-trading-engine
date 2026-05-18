from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.advanced_backtesting_v2 import (  # noqa: E402
    CostModel,
    run_advanced_backtest,
)
from src.backtesting_framework import BacktestSignal  # noqa: E402


def _bars(start=100.0, drift=1.2, count=80):
    bars = []
    close = start

    for index in range(count):
        close += drift
        bars.append(
            {
                "t": 1700000000000 + (index * 86400000),
                "c": round(close, 2),
                "h": round(close + 2, 2),
                "l": round(close - 2, 2),
            }
        )

    return bars


def _signals(count=40):
    signals = []
    for index in range(count):
        signals.append(
            BacktestSignal(
                timestamp_utc=f"2024-01-{(index % 28) + 1:02d}T00:00:00+00:00",
                symbol="NVDA",
                market_state="risk_on",
                setup_type="momentum_breakout",
                decision="approved",
                risk_tier="tier_1",
                entry_price=100.0 + index,
                position_size_multiplier=1.0,
                holding_days=5,
            )
        )
    return signals


def test_advanced_backtest_generates_validation_and_monte_carlo_outputs():
    report = run_advanced_backtest(
        _signals(),
        {"NVDA": _bars()},
        cost_model=CostModel(commission_percent=0.02, slippage_percent=0.08),
        monte_carlo_simulations=50,
    )

    assert report.validation_split.split_index > 0
    assert report.monte_carlo.simulations == 50
    assert len(report.walk_forward_windows) > 0


def test_cost_model_reduces_total_return():
    report = run_advanced_backtest(
        _signals(),
        {"NVDA": _bars()},
        cost_model=CostModel(commission_percent=0.5, slippage_percent=0.5),
        monte_carlo_simulations=10,
    )

    assert (
        report.cost_adjusted_report.summary.total_return
        <= report.base_report.summary.total_return
    )
