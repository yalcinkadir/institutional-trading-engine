from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CrossAssetInputs:
    equity_strength: float
    bond_strength: float
    dollar_strength: float
    gold_strength: float
    volatility_level: float


@dataclass(frozen=True)
class CrossAssetAssessment:
    cross_asset_score: float
    regime_alignment: str
    risk_bias: str
    reasoning: str


class CrossAssetIntelligence:
    def evaluate(
        self,
        inputs: CrossAssetInputs,
    ) -> CrossAssetAssessment:
        risk_on_score = (
            (inputs.equity_strength * 0.4)
            - (inputs.bond_strength * 0.15)
            - (inputs.dollar_strength * 0.15)
            - (inputs.gold_strength * 0.1)
            - (inputs.volatility_level * 0.2)
        )

        score = max(0.0, min(100.0, risk_on_score + 50))

        if score >= 70:
            alignment = "risk_on"
            bias = "bullish"
            reasoning = "equities leading while defensive assets weaken"
        elif score >= 45:
            alignment = "mixed"
            bias = "neutral"
            reasoning = "cross-asset conditions are mixed"
        else:
            alignment = "risk_off"
            bias = "defensive"
            reasoning = "defensive assets outperform risk assets"

        return CrossAssetAssessment(
            cross_asset_score=round(score, 2),
            regime_alignment=alignment,
            risk_bias=bias,
            reasoning=reasoning,
        )


cross_asset_intelligence = CrossAssetIntelligence()
