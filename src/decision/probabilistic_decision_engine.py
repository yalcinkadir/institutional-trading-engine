from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ProbabilisticDecision:
    bullish_probability: float
    bearish_probability: float
    neutral_probability: float
    confidence_score: float
    classification: str


class ProbabilisticDecisionEngine:
    def evaluate(
        self,
        signal_score: float,
        risk_score: float,
        regime_confidence: float,
    ) -> ProbabilisticDecision:
        bullish = max(
            0.0,
            min(
                100.0,
                (signal_score * 0.5)
                + (regime_confidence * 0.3)
                - (risk_score * 0.2),
            ),
        )

        bearish = max(0.0, min(100.0, risk_score * 0.8))

        neutral = max(0.0, 100 - bullish - bearish)

        confidence = max(bullish, bearish, neutral)

        if bullish >= bearish and bullish >= neutral:
            classification = "bullish"
        elif bearish >= bullish and bearish >= neutral:
            classification = "bearish"
        else:
            classification = "neutral"

        return ProbabilisticDecision(
            bullish_probability=round(bullish, 2),
            bearish_probability=round(bearish, 2),
            neutral_probability=round(neutral, 2),
            confidence_score=round(confidence, 2),
            classification=classification,
        )


probabilistic_decision_engine = ProbabilisticDecisionEngine()
