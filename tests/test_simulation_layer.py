from src.simulation.portfolio_simulator import simulate_portfolio_growth
from src.simulation.probability_engine import calculate_outcome_probability
from src.simulation.scenario_simulator import simulate_market_scenario
from src.simulation.stress_testing import run_stress_test


def test_scenario_simulator():
    result = simulate_market_scenario(
        base_price=100,
        expected_return_percent=10,
        volatility_percent=5,
    )

    assert result["bullish_price"] > result["base_case_price"]
    assert result["bearish_price"] < result["base_case_price"]


def test_stress_testing():
    result = run_stress_test(
        portfolio_value=100000,
        drawdown_percent=20,
        leverage=1.5,
    )

    assert result["stressed_value"] < 100000
    assert result["classification"] == "High Stress"


def test_portfolio_simulator():
    result = simulate_portfolio_growth(
        initial_capital=10000,
        annual_return_percent=10,
        years=5,
    )

    assert result["final_value"] > 10000
    assert len(result["portfolio_values"]) == 5


def test_probability_engine():
    result = calculate_outcome_probability(
        successful_cases=8,
        total_cases=10,
    )

    assert result["probability_percent"] == 80
    assert result["classification"] == "Very High Probability"
