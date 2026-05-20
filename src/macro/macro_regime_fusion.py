from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MacroRegimeInputs:
    market_regime_score: float
    cross_asset_score: float
    tail_risk_score: float
    liquidity_score: float
    volatility_level: float


@dataclass(frozen=True)
class MacroRegimeFusionResult:
    macro_score: float
    macro_regime: str
    portfolio_bias: str
    explanation: str


class MacroRegimeFusionEngine:
    def evaluate(self, inputs: MacroRegimeInputs) -> MacroRegimeFusionResult:
        macro_score = (
            (inputs.market_regime_score * 0.3)
            + (inputs.cross_asset_score * 0.3)
            + (inputs.liquidity_score * 0.2)
            - (inputs.tail_risk_score * 0.15)
            - (inputs.volatility_level * 0.05)
        )

        macro_score = max(0.0, min(100.0, macro_score))

        if macro_score >= 65:
            regime = "macro_risk_on"
            bias = "growth_offense"
            explanation = "market, liquidity and cross-asset conditions are strongly aligned"
        elif macro_score >= 50:
            regime = "macro_constructive"
            bias = "selective_risk"
            explanation = "macro conditions are supportive but not fully confirmed"
        elif macro_score >= 35:
            regime = "macro_uncertain"
            bias = "balanced_defense"
            explanation = "macro inputs are mixed and require reduced conviction"
        else:
            regime = "macro_risk_off"
            bias = "capital_preservation"
            explanation = "tail risk, volatility or weak cross-asset alignment dominate"

        return MacroRegimeFusionResult(
            macro_score=round(macro_score, 2),
            macro_regime=regime,
            portfolio_bias=bias,
            explanation=explanation,
        )


macro_regime_fusion_engine = MacroRegimeFusionEngine()
