from src.macro.macro_regime_fusion import (
    MacroRegimeFusionEngine,
    MacroRegimeInputs,
)


def test_macro_risk_on_environment():
    engine = MacroRegimeFusionEngine()

    result = engine.evaluate(
        MacroRegimeInputs(
            market_regime_score=90,
            cross_asset_score=85,
            tail_risk_score=15,
            liquidity_score=88,
            volatility_level=12,
        )
    )

    assert result.macro_regime == "macro_risk_on"
    assert result.portfolio_bias == "growth_offense"


def test_macro_risk_off_environment():
    engine = MacroRegimeFusionEngine()

    result = engine.evaluate(
        MacroRegimeInputs(
            market_regime_score=25,
            cross_asset_score=30,
            tail_risk_score=90,
            liquidity_score=20,
            volatility_level=45,
        )
    )

    assert result.macro_regime == "macro_risk_off"
    assert result.portfolio_bias == "capital_preservation"
