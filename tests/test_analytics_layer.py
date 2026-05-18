from src.analytics.backtesting import simple_backtest
from src.analytics.performance_tracker import calculate_performance_statistics
from src.analytics.recommendation_tracker import create_recommendation
from src.analytics.trade_journal import create_trade_journal_entry


def test_create_recommendation():
    recommendation = create_recommendation(
        ticker="NVDA",
        action="ENTER",
        score=88,
        confidence=84.5,
        market_regime="Bullish",
        entry_price=100,
        stop_price=95,
        target_price=120,
    )

    assert recommendation["ticker"] == "NVDA"
    assert recommendation["action"] == "ENTER"
    assert recommendation["score"] == 88
    assert recommendation["confidence"] == 84.5


def test_trade_journal_profit_calculation():
    trade = create_trade_journal_entry(
        ticker="MSFT",
        entry_price=100,
        exit_price=110,
        shares=10,
    )

    assert trade["pnl"] == 100
    assert trade["pnl_percent"] == 10
    assert trade["outcome"] == "WIN"


def test_performance_statistics():
    trades = [
        {"pnl": 100, "pnl_percent": 10, "outcome": "WIN"},
        {"pnl": -50, "pnl_percent": -5, "outcome": "LOSS"},
    ]

    stats = calculate_performance_statistics(trades)

    assert stats["total_trades"] == 2
    assert stats["win_rate"] == 50
    assert stats["total_pnl"] == 50


def test_simple_backtest():
    recommendations = [
        {
            "ticker": "QQQ",
            "entry_price": 100,
        }
    ]

    results = simple_backtest(
        recommendations=recommendations,
        final_prices={"QQQ": 110},
    )

    assert results["tested_assets"] == 1
    assert results["average_pnl_percent"] == 10
