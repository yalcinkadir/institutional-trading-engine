from src.regime.regime_similarity_engine import (
    MarketRegime,
    RegimeSimilarityEngine,
    normalize_regime_vector,
)


def test_identical_regimes_score_near_100() -> None:
    engine = RegimeSimilarityEngine()
    current = MarketRegime(
        name="current",
        market_health_score=75,
        volatility=18,
        breadth=70,
        momentum=30,
    )

    result = engine.compare(current, [current])[0]

    assert result.similarity_score == 100.0
    assert result.distance_similarity_score == 100.0
    assert result.cosine_similarity_score == 100.0
    assert result.weighted_distance == 0.0


def test_volatility_change_penalizes_more_than_equal_breadth_change() -> None:
    engine = RegimeSimilarityEngine()
    current = MarketRegime(
        name="current",
        market_health_score=70,
        volatility=20,
        breadth=70,
        momentum=20,
    )
    volatility_shift = MarketRegime(
        name="volatility_shift",
        market_health_score=70,
        volatility=52,
        breadth=70,
        momentum=20,
    )
    breadth_shift = MarketRegime(
        name="breadth_shift",
        market_health_score=70,
        volatility=20,
        breadth=38,
        momentum=20,
    )

    volatility_result = engine.compare(current, [volatility_shift])[0]
    breadth_result = engine.compare(current, [breadth_shift])[0]

    assert volatility_result.similarity_score < breadth_result.similarity_score
    assert volatility_result.weighted_distance > breadth_result.weighted_distance


def test_opposite_regime_scores_materially_lower_than_similar_regime() -> None:
    engine = RegimeSimilarityEngine()
    current = MarketRegime(
        name="low_vol_bull",
        market_health_score=85,
        volatility=12,
        breadth=82,
        momentum=60,
    )
    similar = MarketRegime(
        name="similar_low_vol_bull",
        market_health_score=80,
        volatility=14,
        breadth=78,
        momentum=50,
    )
    opposite = MarketRegime(
        name="panic_bear",
        market_health_score=10,
        volatility=75,
        breadth=12,
        momentum=-80,
    )

    results = engine.compare(current, [opposite, similar])

    assert results[0].historical_regime == "similar_low_vol_bull"
    assert results[0].similarity_score > 80
    assert results[1].historical_regime == "panic_bear"
    assert results[1].similarity_score < 50


def test_cosine_similarity_handles_zero_vector_safely() -> None:
    engine = RegimeSimilarityEngine()
    zero_like = MarketRegime(
        name="zero_like",
        market_health_score=0,
        volatility=0,
        breadth=0,
        momentum=-100,
    )
    normal = MarketRegime(
        name="normal",
        market_health_score=50,
        volatility=20,
        breadth=50,
        momentum=0,
    )

    cosine = engine._calculate_cosine_similarity(zero_like, normal)

    assert cosine == 0.0


def test_normalized_vector_clamps_values() -> None:
    regime = MarketRegime(
        name="extreme",
        market_health_score=150,
        volatility=120,
        breadth=-20,
        momentum=200,
    )

    vector = normalize_regime_vector(regime)

    assert vector.market_health_score == 1.0
    assert vector.volatility == 1.0
    assert vector.breadth == 0.0
    assert vector.momentum == 1.0
