from __future__ import annotations

import math
from dataclasses import dataclass


SOFTMAX_TEMPERATURE = 20.0


@dataclass(frozen=True)
class ProbabilityLogits:
    bullish: float
    bearish: float
    neutral: float


@dataclass(frozen=True)
class ProbabilisticDecision:
    bullish_probability: float
    bearish_probability: float
    neutral_probability: float
    confidence_score: float
    classification: str
    logits: ProbabilityLogits

    @property
    def probability_sum(self) -> float:
        return round(
            self.bullish_probability
            + self.bearish_probability
            + self.neutral_probability,
            4,
        )


def clamp_score(value: float) -> float:
    return max(0.0, min(100.0, float(value)))


def calculate_probability_logits(
    *,
    signal_score: float,
    risk_score: float,
    regime_confidence: float,
) -> ProbabilityLogits:
    signal = clamp_score(signal_score)
    risk = clamp_score(risk_score)
    regime = clamp_score(regime_confidence)

    raw_bullish = (signal * 0.5) + (regime * 0.3) - (risk * 0.1)
    raw_bearish = (risk * 0.6) + (max(0.0, 50.0 - regime) * 0.2)
    raw_neutral = 50.0 - (abs(raw_bullish - raw_bearish) * 0.3)

    return ProbabilityLogits(
        bullish=raw_bullish,
        bearish=raw_bearish,
        neutral=raw_neutral,
    )


def stable_softmax_percentages(logits: ProbabilityLogits) -> tuple[float, float, float]:
    scaled_logits = (
        logits.bullish / SOFTMAX_TEMPERATURE,
        logits.bearish / SOFTMAX_TEMPERATURE,
        logits.neutral / SOFTMAX_TEMPERATURE,
    )
    max_logit = max(scaled_logits)
    exp_values = tuple(math.exp(value - max_logit) for value in scaled_logits)
    total = sum(exp_values)

    if total <= 0.0:
        return (33.3333, 33.3333, 33.3334)

    bullish = (exp_values[0] / total) * 100.0
    bearish = (exp_values[1] / total) * 100.0
    neutral = 100.0 - bullish - bearish
    return bullish, bearish, neutral


def classify_probabilities(
    *,
    bullish_probability: float,
    bearish_probability: float,
    neutral_probability: float,
) -> str:
    if bullish_probability >= bearish_probability and bullish_probability >= neutral_probability:
        return "bullish"
    if bearish_probability >= bullish_probability and bearish_probability >= neutral_probability:
        return "bearish"
    return "neutral"


class ProbabilisticDecisionEngine:
    def evaluate(
        self,
        signal_score: float,
        risk_score: float,
        regime_confidence: float,
    ) -> ProbabilisticDecision:
        logits = calculate_probability_logits(
            signal_score=signal_score,
            risk_score=risk_score,
            regime_confidence=regime_confidence,
        )
        bullish, bearish, neutral = stable_softmax_percentages(logits)
        confidence = max(bullish, bearish, neutral)
        classification = classify_probabilities(
            bullish_probability=bullish,
            bearish_probability=bearish,
            neutral_probability=neutral,
        )

        return ProbabilisticDecision(
            bullish_probability=round(bullish, 4),
            bearish_probability=round(bearish, 4),
            neutral_probability=round(neutral, 4),
            confidence_score=round(confidence, 4),
            classification=classification,
            logits=logits,
        )


probabilistic_decision_engine = ProbabilisticDecisionEngine()
