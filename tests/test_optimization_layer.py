from src.optimization.adaptive_optimizer import adapt_strategy_weights
from src.optimization.capital_allocator import allocate_capital
from src.optimization.portfolio_optimizer import optimize_portfolio_weights
from src.optimization.risk_reward_optimizer import calculate_risk_reward


def test_portfolio_optimizer():
    result = optimize_portfolio_weights(
        [
            {"ticker": "NVDA", "score": 90},
            {"ticker": "MSFT", "score": 70},
            {"ticker": "GLD", "score": 40},
        ]
    )

    assert result["total_weight"] > 0.99
    assert "NVDA" in result["weights"]


def test_risk_reward_optimizer():
    result = calculate_risk_reward(
        entry_price=100,
        target_price=130,
        stop_price=90,
    )

    assert result["risk_reward_ratio"] == 3
    assert result["classification"] == "Excellent"


def test_capital_allocator():
    result = allocate_capital(
        total_capital=100000,
        allocations={
            "NVDA": 0.5,
            "MSFT": 0.3,
            "GLD": 0.2,
        },
    )

    assert result["allocations"]["NVDA"] == 50000


def test_adaptive_optimizer():
    result = adapt_strategy_weights(
        {
            "momentum": 12,
            "mean_reversion": 5,
            "defensive": 3,
        }
    )

    assert result["momentum"] > result["defensive"]
