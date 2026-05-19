from src.cross_asset.cross_asset_intelligence import (
    CrossAssetInputs,
    CrossAssetIntelligence,
)


def test_cross_asset_risk_on_environment():
    engine = CrossAssetIntelligence()

    result = engine.evaluate(
        CrossAssetInputs(
            equity_strength=90,
            bond_strength=20,
            dollar_strength=25,
            gold_strength=20,
            volatility_level=15,
        )
    )

    assert result.regime_alignment == "risk_on"
    assert result.risk_bias == "bullish"


def test_cross_asset_risk_off_environment():
    engine = CrossAssetIntelligence()

    result = engine.evaluate(
        CrossAssetInputs(
            equity_strength=25,
            bond_strength=80,
            dollar_strength=85,
            gold_strength=75,
            volatility_level=40,
        )
    )

    assert result.regime_alignment == "risk_off"
    assert result.risk_bias == "defensive"
