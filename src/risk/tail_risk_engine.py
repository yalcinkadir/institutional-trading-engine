from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TailRiskInputs:
    vix_level: float
    gap_risk_percent: float
    liquidity_stress_percent: float
    correlation_risk_percent: float
    event_risk_percent: float


@dataclass(frozen=True)
class TailRiskAssessment:
    tail_risk_score: float
    regime: str
    exposure_multiplier: float


class TailRiskEngine:
    def assess(self, inputs: TailRiskInputs) -> TailRiskAssessment:
        score = (
            (inputs.vix_level * 1.2)
            + (inputs.gap_risk_percent * 0.2)
            + (inputs.liquidity_stress_percent * 0.25)
            + (inputs.correlation_risk_percent * 0.2)
            + (inputs.event_risk_percent * 0.15)
        )

        if score >= 85:
            regime = "panic"
            multiplier = 0.2
        elif score >= 70:
            regime = "crisis"
            multiplier = 0.35
        elif score >= 55:
            regime = "stress"
            multiplier = 0.5
        elif score >= 35:
            regime = "elevated"
            multiplier = 0.75
        else:
            regime = "normal"
            multiplier = 1.0

        return TailRiskAssessment(
            tail_risk_score=round(score, 2),
            regime=regime,
            exposure_multiplier=multiplier,
        )


tail_risk_engine = TailRiskEngine()
