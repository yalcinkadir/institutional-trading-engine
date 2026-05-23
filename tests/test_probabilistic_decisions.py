from src.decision.confidence_weighted_execution import (
    ConfidenceWeightedExecution,
)
from src.decision.probabilistic_decision_engine import (
    ProbabilityLogits,
    ProbabilisticDecisionEngine,
    stable_softmax_percentages,
)


def probability_total(decision) -> float:
    return round(
        decision.bullish_probability
        + decision.bearish_probability
        + decision.neutral_probability,
        2,
    )


def test_probabilistic_decision_bullish():
    engine = ProbabilisticDecisionEngine()

    decision = engine.evaluate(
        signal_score=90,
        risk_score=20,
        regime_confidence=85,
    )

    assert decision.classification == "bullish"
    assert decision.bullish_probability > decision.bearish_probability


def test_confidence_weighted_execution_high():
    decision_engine = ProbabilisticDecisionEngine()
    execution_engine = ConfidenceWeightedExecution()

    decision = decision_engine.evaluate(
        signal_score=95,
        risk_score=10,
        regime_confidence=90,
    )

    execution = execution_engine.generate(decision)

    assert execution.execution_aggressiveness == "high"
    assert execution.exposure_percent == 100


def test_probabilities_sum_to_one_hundred() -> None:
    engine = ProbabilisticDecisionEngine()

    cases = [
        {"signal_score": 0, "risk_score": 0, "regime_confidence": 0},
        {"signal_score": 100, "risk_score": 0, "regime_confidence": 100},
        {"signal_score": 0, "risk_score": 100, "regime_confidence": 0},
        {"signal_score": 50, "risk_score": 50, "regime_confidence": 50},
        {"signal_score": 75, "risk_score": 90, "regime_confidence": 20},
    ]

    for case in cases:
        decision = engine.evaluate(**case)
        assert probability_total(decision) == 100.0
        assert abs(decision.probability_sum - 100.0) <= 0.01


def test_high_risk_low_signal_is_bearish_dominant() -> None:
    engine = ProbabilisticDecisionEngine()

    decision = engine.evaluate(
        signal_score=0,
        risk_score=100,
        regime_confidence=0,
    )

    assert decision.classification == "bearish"
    assert decision.bearish_probability > decision.bullish_probability
    assert decision.bearish_probability > decision.neutral_probability


def test_high_signal_low_risk_strong_regime_is_bullish_dominant() -> None:
    engine = ProbabilisticDecisionEngine()

    decision = engine.evaluate(
        signal_score=100,
        risk_score=0,
        regime_confidence=100,
    )

    assert decision.classification == "bullish"
    assert decision.bullish_probability > decision.bearish_probability
    assert decision.bullish_probability > decision.neutral_probability


def test_no_negative_probability_possible() -> None:
    engine = ProbabilisticDecisionEngine()

    decision = engine.evaluate(
        signal_score=-100,
        risk_score=500,
        regime_confidence=-50,
    )

    assert decision.bullish_probability >= 0.0
    assert decision.bearish_probability >= 0.0
    assert decision.neutral_probability >= 0.0
    assert probability_total(decision) == 100.0


def test_classification_follows_highest_probability() -> None:
    engine = ProbabilisticDecisionEngine()

    decision = engine.evaluate(
        signal_score=30,
        risk_score=30,
        regime_confidence=50,
    )

    probabilities = {
        "bullish": decision.bullish_probability,
        "bearish": decision.bearish_probability,
        "neutral": decision.neutral_probability,
    }

    assert decision.classification == max(probabilities, key=probabilities.get)


def test_softmax_is_numerically_stable_for_large_logits() -> None:
    bullish, bearish, neutral = stable_softmax_percentages(
        ProbabilityLogits(
            bullish=10000,
            bearish=9999,
            neutral=9998,
        )
    )

    assert round(bullish + bearish + neutral, 2) == 100.0
    assert bullish > bearish > neutral
