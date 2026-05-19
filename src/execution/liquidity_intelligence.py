from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LiquidityInputs:
    average_daily_volume_millions: float
    bid_ask_spread_percent: float
    volatility_percent: float
    order_size_percent_adv: float


@dataclass(frozen=True)
class LiquidityAssessment:
    liquidity_score: float
    execution_risk: str
    recommended_execution_style: str


class LiquidityIntelligence:
    def evaluate(
        self,
        inputs: LiquidityInputs,
    ) -> LiquidityAssessment:
        score = (
            (inputs.average_daily_volume_millions * 0.4)
            - (inputs.bid_ask_spread_percent * 15)
            - (inputs.volatility_percent * 0.5)
            - (inputs.order_size_percent_adv * 0.8)
        )

        score = max(0.0, min(100.0, score))

        if score >= 70:
            risk = "low"
            execution = "aggressive"
        elif score >= 45:
            risk = "moderate"
            execution = "controlled"
        else:
            risk = "high"
            execution = "passive"

        return LiquidityAssessment(
            liquidity_score=round(score, 2),
            execution_risk=risk,
            recommended_execution_style=execution,
        )


liquidity_intelligence = LiquidityIntelligence()
