from src.decision.confidence_weighted_execution import (
    ConfidenceWeightedExecution,
)
from src.decision.probabilistic_decision_engine import (
    ProbabilisticDecisionEngine,
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
