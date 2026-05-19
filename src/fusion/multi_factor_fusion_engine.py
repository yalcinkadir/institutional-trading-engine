from __future__ import annotations

from dataclasses import dataclass


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


class MultiFactorFusionEngine:
    def evaluate(
        self,
        inputs: FusionInputs,
    ) -> FusionDecision:
        fusion_score = (
            (inputs.regime_score * 0.25)
            + (inputs.liquidity_score * 0.15)
            + (inputs.feature_alpha_score * 0.25)
            + (inputs.execution_confidence * 0.2)
            - (inputs.tail_risk_score * 0.1)
            - (inputs.portfolio_risk_score * 0.05)
        )

        confidence = max(0.0, min(100.0, fusion_score))

        if confidence >= 75:
            classification = "high_conviction"
            reasoning = "strong multi-factor alignment"
        elif confidence >= 55:
            classification = "moderate_conviction"
            reasoning = "mixed but favorable conditions"
        elif confidence >= 35:
            classification = "low_conviction"
            reasoning = "uncertain multi-factor environment"
        else:
            classification = "avoid"
            reasoning = "risk dominates opportunity"

        return FusionDecision(
            fusion_score=round(fusion_score, 2),
            confidence=round(confidence, 2),
            classification=classification,
            reasoning=reasoning,
        )


multi_factor_fusion_engine = MultiFactorFusionEngine()
