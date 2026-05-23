from __future__ import annotations

from dataclasses import dataclass
from typing import Any

OPPORTUNITY_WEIGHTS = {
    "regime_score": 0.30,
    "feature_alpha_score": 0.30,
    "execution_confidence": 0.20,
    "liquidity_score": 0.20,
}

RISK_PENALTY_WEIGHTS = {
    "tail_risk_score": 0.20,
    "portfolio_risk_score": 0.10,
}

REGIME_GATE_THRESHOLD = 20.0
REGIME_GATE_SCORE_CAP = 40.0


@dataclass(frozen=True)
class FusionInputs:
    regime_score: float
    tail_risk_score: float
    liquidity_score: float
    feature_alpha_score: float
    portfolio_risk_score: float
    execution_confidence: float


@dataclass(frozen=True)
class FusionDecision:
    fusion_score: float
    confidence: float
    classification: str
    reasoning: str
    opportunity_score: float = 0.0
    opportunity_points: float = 0.0
    risk_penalty: float = 0.0
    regime_gate_applied: bool = False
    regime_gate_cap: float | None = None
    normalized_inputs: dict[str, float] | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "fusion_score": self.fusion_score,
            "confidence": self.confidence,
            "classification": self.classification,
            "reasoning": self.reasoning,
            "opportunity_score": self.opportunity_score,
            "opportunity_points": self.opportunity_points,
            "risk_penalty": self.risk_penalty,
            "regime_gate_applied": self.regime_gate_applied,
            "regime_gate_cap": self.regime_gate_cap,
            "normalized_inputs": self.normalized_inputs or {},
        }


class MultiFactorFusionEngine:
    def evaluate(
        self,
        inputs: FusionInputs,
    ) -> FusionDecision:
        normalized_inputs = normalize_fusion_inputs(inputs)
        opportunity_score = calculate_opportunity_score(**normalized_inputs)
        opportunity_points = opportunity_score * 100.0
        risk_penalty = calculate_risk_penalty(**normalized_inputs)
        raw_fusion_score = opportunity_points - risk_penalty
        fusion_score = _clamp_score(raw_fusion_score)

        regime_gate_applied = normalized_inputs["regime_score"] < REGIME_GATE_THRESHOLD
        regime_gate_cap: float | None = None
        if regime_gate_applied:
            regime_gate_cap = REGIME_GATE_SCORE_CAP
            fusion_score = min(fusion_score, regime_gate_cap)

        confidence = fusion_score
        classification, reasoning = classify_fusion_score(
            confidence,
            regime_gate_applied=regime_gate_applied,
        )

        return FusionDecision(
            fusion_score=round(fusion_score, 2),
            confidence=round(confidence, 2),
            classification=classification,
            reasoning=reasoning,
            opportunity_score=round(opportunity_score, 6),
            opportunity_points=round(opportunity_points, 2),
            risk_penalty=round(risk_penalty, 2),
            regime_gate_applied=regime_gate_applied,
            regime_gate_cap=regime_gate_cap,
            normalized_inputs=normalized_inputs,
        )


def normalize_fusion_inputs(inputs: FusionInputs) -> dict[str, float]:
    return {
        "regime_score": _clamp_score(inputs.regime_score),
        "liquidity_score": _clamp_score(inputs.liquidity_score),
        "feature_alpha_score": _clamp_score(inputs.feature_alpha_score),
        "execution_confidence": _clamp_score(inputs.execution_confidence),
        "tail_risk_score": _clamp_score(inputs.tail_risk_score),
        "portfolio_risk_score": _clamp_score(inputs.portfolio_risk_score),
    }


def calculate_opportunity_score(
    *,
    regime_score: float,
    liquidity_score: float,
    feature_alpha_score: float,
    execution_confidence: float,
    **_: float,
) -> float:
    weighted_points = (
        _clamp_score(regime_score) * OPPORTUNITY_WEIGHTS["regime_score"]
        + _clamp_score(feature_alpha_score) * OPPORTUNITY_WEIGHTS["feature_alpha_score"]
        + _clamp_score(execution_confidence) * OPPORTUNITY_WEIGHTS["execution_confidence"]
        + _clamp_score(liquidity_score) * OPPORTUNITY_WEIGHTS["liquidity_score"]
    )
    return _clamp_score(weighted_points) / 100.0


def calculate_risk_penalty(
    *,
    tail_risk_score: float,
    portfolio_risk_score: float,
    **_: float,
) -> float:
    penalty = (
        _clamp_score(tail_risk_score) * RISK_PENALTY_WEIGHTS["tail_risk_score"]
        + _clamp_score(portfolio_risk_score)
        * RISK_PENALTY_WEIGHTS["portfolio_risk_score"]
    )
    return min(30.0, max(0.0, penalty))


def classify_fusion_score(
    confidence: float,
    *,
    regime_gate_applied: bool = False,
) -> tuple[str, str]:
    if regime_gate_applied:
        return "low_conviction", "regime gate caps otherwise favorable inputs"
    if confidence >= 70:
        return "high_conviction", "strong opportunity after explicit risk penalty"
    if confidence >= 55:
        return "moderate_conviction", "mixed but favorable opportunity-risk balance"
    if confidence >= 35:
        return "low_conviction", "uncertain opportunity-risk balance"
    return "avoid", "risk penalty or weak opportunity dominates"


def validate_opportunity_weights() -> bool:
    return abs(sum(OPPORTUNITY_WEIGHTS.values()) - 1.0) < 0.000001


def _clamp_score(value: float) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        number = 0.0
    return max(0.0, min(100.0, number))


multi_factor_fusion_engine = MultiFactorFusionEngine()
