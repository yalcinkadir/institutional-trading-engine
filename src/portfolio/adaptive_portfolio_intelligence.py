from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PortfolioExposure:
    sector_exposure_percent: float
    volatility_exposure_percent: float
    concentration_percent: float
    correlation_percent: float


@dataclass(frozen=True)
class PortfolioRiskAdjustment:
    risk_score: float
    recommended_exposure_multiplier: float
    classification: str


class AdaptivePortfolioIntelligence:
    def evaluate(
        self,
        exposure: PortfolioExposure,
    ) -> PortfolioRiskAdjustment:
        risk_score = (
            (exposure.sector_exposure_percent * 0.25)
            + (exposure.volatility_exposure_percent * 0.3)
            + (exposure.concentration_percent * 0.25)
            + (exposure.correlation_percent * 0.2)
        )

        if risk_score >= 75:
            multiplier = 0.5
            classification = "high_risk"
        elif risk_score >= 50:
            multiplier = 0.75
            classification = "moderate_risk"
        else:
            multiplier = 1.0
            classification = "healthy"

        return PortfolioRiskAdjustment(
            risk_score=round(risk_score, 2),
            recommended_exposure_multiplier=multiplier,
            classification=classification,
        )


adaptive_portfolio_intelligence = AdaptivePortfolioIntelligence()
