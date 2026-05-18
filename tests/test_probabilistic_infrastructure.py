from src.analytics.probabilistic_signals import calculate_signal_probability
from src.analytics.walk_forward_validation import evaluate_walk_forward
from src.simulation.monte_carlo import run_monte_carlo_simulation
from src.strategy.regime_probability_engine import estimate_regime_probabilities


def test_monte_carlo():
    result = run_monte_carlo_simulation(
        initial_value=10000,
        expected_return_percent=8,
        volatility_percent=12,
        periods=10,
        simulations=200,
    )

    assert result["p95"] >= result["p50"]
    assert result["p50"] >= result["p5"]


def test_walk_forward_validation():
    result = evaluate_walk_forward(
        training_scores=[85, 88, 82],
        validation_scores=[80, 79, 78],
    )

    assert result["classification"] in {
        "Robust",
        "Moderate Overfit Risk",
    }


def test_probabilistic_signals():
    result = calculate_signal_probability(
        historical_success_rate=75,
        confidence_score=80,
        regime_alignment=70,
    )

    assert result["probability_score"] >= 70


def test_regime_probability_engine():
    result = estimate_regime_probabilities(
        bullish_signals=7,
        bearish_signals=2,
        neutral_signals=1,
    )

    assert result["dominant_regime"] == "bullish"
    assert result["bullish_probability"] > result["bearish_probability"]
