import pytest

from src.fusion.multi_factor_fusion_engine import (
    OPPORTUNITY_WEIGHTS,
    FusionInputs,
    MultiFactorFusionEngine,
    calculate_risk_penalty,
    validate_opportunity_weights,
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
    assert result.risk_penalty > 0
    assert result.opportunity_points > result.risk_penalty


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


def test_opportunity_weights_sum_to_one() -> None:
    assert sum(OPPORTUNITY_WEIGHTS.values()) == pytest.approx(1.0)
    assert validate_opportunity_weights() is True


def test_fusion_score_separates_opportunity_from_risk_penalty() -> None:
    engine = MultiFactorFusionEngine()
    result = engine.evaluate(
        FusionInputs(
            regime_score=80,
            liquidity_score=70,
            feature_alpha_score=90,
            execution_confidence=75,
            tail_risk_score=20,
            portfolio_risk_score=10,
        )
    )

    assert result.opportunity_points == pytest.approx(80.0)
    assert result.risk_penalty == pytest.approx(5.0)
    assert result.fusion_score == pytest.approx(75.0)
    assert result.regime_gate_applied is False


def test_tail_risk_has_stronger_penalty_than_portfolio_risk() -> None:
    tail_only = calculate_risk_penalty(tail_risk_score=100, portfolio_risk_score=0)
    portfolio_only = calculate_risk_penalty(tail_risk_score=0, portfolio_risk_score=100)

    assert tail_only == pytest.approx(20.0)
    assert portfolio_only == pytest.approx(10.0)
    assert tail_only > portfolio_only


def test_risk_penalty_is_capped_at_30_points() -> None:
    assert calculate_risk_penalty(tail_risk_score=100, portfolio_risk_score=100) == 30.0


def test_fusion_score_is_clamped_to_0_to_100() -> None:
    engine = MultiFactorFusionEngine()
    low_result = engine.evaluate(
        FusionInputs(
            regime_score=0,
            liquidity_score=0,
            feature_alpha_score=0,
            execution_confidence=0,
            tail_risk_score=100,
            portfolio_risk_score=100,
        )
    )
    high_result = engine.evaluate(
        FusionInputs(
            regime_score=100,
            liquidity_score=100,
            feature_alpha_score=100,
            execution_confidence=100,
            tail_risk_score=0,
            portfolio_risk_score=0,
        )
    )

    assert low_result.fusion_score == 0.0
    assert high_result.fusion_score == 100.0


def test_regime_gate_caps_score_when_regime_is_weak() -> None:
    engine = MultiFactorFusionEngine()
    result = engine.evaluate(
        FusionInputs(
            regime_score=19,
            liquidity_score=100,
            feature_alpha_score=100,
            execution_confidence=100,
            tail_risk_score=0,
            portfolio_risk_score=0,
        )
    )

    assert result.regime_gate_applied is True
    assert result.regime_gate_cap == 40.0
    assert result.fusion_score == 40.0
    assert result.classification == "low_conviction"


def test_regime_gate_not_applied_at_threshold() -> None:
    engine = MultiFactorFusionEngine()
    result = engine.evaluate(
        FusionInputs(
            regime_score=20,
            liquidity_score=100,
            feature_alpha_score=100,
            execution_confidence=100,
            tail_risk_score=0,
            portfolio_risk_score=0,
        )
    )

    assert result.regime_gate_applied is False
    assert result.fusion_score > 40.0


def test_inputs_are_sanitized_to_score_bounds() -> None:
    engine = MultiFactorFusionEngine()
    result = engine.evaluate(
        FusionInputs(
            regime_score=150,
            liquidity_score=-10,
            feature_alpha_score=100,
            execution_confidence=50,
            tail_risk_score=500,
            portfolio_risk_score=-50,
        )
    )

    assert result.normalized_inputs["regime_score"] == 100.0
    assert result.normalized_inputs["liquidity_score"] == 0.0
    assert result.normalized_inputs["tail_risk_score"] == 100.0
    assert result.normalized_inputs["portfolio_risk_score"] == 0.0
