from src.regime.regime_similarity_engine import (
    MarketRegime,
    RegimeSimilarityEngine,
)


def test_regime_similarity_ranking():
    engine = RegimeSimilarityEngine()

    current = MarketRegime(
        name="current",
        market_health_score=80,
        volatility=15,
        breadth=75,
        momentum=82,
    )

    historical = [
        MarketRegime(
            name="bull_2024",
            market_health_score=79,
            volatility=16,
            breadth=74,
            momentum=81,
        ),
        MarketRegime(
            name="crash_2022",
            market_health_score=35,
            volatility=45,
            breadth=30,
            momentum=20,
        ),
    ]

    results = engine.compare(current, historical)

    assert results[0].historical_regime == "bull_2024"
    assert results[0].similarity_score > results[1].similarity_score
