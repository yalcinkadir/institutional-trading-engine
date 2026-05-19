from src.portfolio.adaptive_portfolio_intelligence import (
    AdaptivePortfolioIntelligence,
    PortfolioExposure,
)


def test_adaptive_portfolio_high_risk():
    intelligence = AdaptivePortfolioIntelligence()

    result = intelligence.evaluate(
        PortfolioExposure(
            sector_exposure_percent=90,
            volatility_exposure_percent=80,
            concentration_percent=85,
            correlation_percent=75,
        )
    )

    assert result.classification == "high_risk"
    assert result.recommended_exposure_multiplier == 0.5


def test_adaptive_portfolio_healthy():
    intelligence = AdaptivePortfolioIntelligence()

    result = intelligence.evaluate(
        PortfolioExposure(
            sector_exposure_percent=20,
            volatility_exposure_percent=25,
            concentration_percent=20,
            correlation_percent=15,
        )
    )

    assert result.classification == "healthy"
    assert result.recommended_exposure_multiplier == 1.0
