from src.fusion.multi_factor_fusion_engine import (
    FusionInputs,
    MultiFactorFusionEngine,
)


def test_multi_factor_high_conviction():
    engine = MultiFactorFusionEngine()

    result = engine.evaluate(
        FusionInputs(
            regime_score=90,
            tail_risk_score=15,
            liquidity_score=85,
            feature_alpha_score=88,
            portfolio_risk_score=20,
            execution_confidence=92,
        )
    )

    assert result.classification == "high_conviction"
    assert result.confidence >= 75


def test_multi_factor_avoid_environment():
    engine = MultiFactorFusionEngine()

    result = engine.evaluate(
        FusionInputs(
            regime_score=35,
            tail_risk_score=90,
            liquidity_score=30,
            feature_alpha_score=25,
            portfolio_risk_score=80,
            execution_confidence=20,
        )
    )

    assert result.classification == "avoid"
