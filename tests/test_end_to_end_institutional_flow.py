from src.orchestration.institutional_decision_orchestrator import (
    InstitutionalDecisionInputs,
    institutional_decision_orchestrator,
)


def test_full_institutional_decision_flow():
    result = institutional_decision_orchestrator.evaluate(
        InstitutionalDecisionInputs(
            market_regime_score=85,
            equity_strength=90,
            bond_strength=20,
            dollar_strength=25,
            gold_strength=20,
            volatility_level=15,
            gap_risk_percent=15,
            liquidity_stress_percent=10,
            correlation_risk_percent=20,
            event_risk_percent=10,
            average_daily_volume_millions=50,
            bid_ask_spread_percent=0.05,
            order_size_percent_adv=2,
            feature_alpha_score=88,
            portfolio_sector_exposure_percent=35,
            portfolio_volatility_exposure_percent=30,
            portfolio_concentration_percent=25,
            portfolio_correlation_percent=30,
        )
    )

    assert result.macro_regime in [
        "macro_risk_on",
        "macro_constructive",
    ]

    assert result.cross_asset_regime == "risk_on"

    assert result.fusion_classification in [
        "high_conviction",
        "moderate_conviction",
    ]

    assert result.final_exposure_percent > 0

    assert "macro=" in result.explanation
