from __future__ import annotations

from dataclasses import dataclass

from src.decision_confidence import (
    ASSET_SETUP_WEIGHT,
    MARKET_HEALTH_WEIGHT,
    REGIME_ALIGNMENT_WEIGHT,
    ConfidenceInput,
    RegimeAlignmentTier,
    calculate_confidence_from_tier,
    calculate_confidence_score,
    regime_alignment_score_from_decision,
    regime_alignment_score_from_tier,
)


def test_confidence_score_uses_orthogonal_three_layer_formula() -> None:
    result = calculate_confidence_score(
        ConfidenceInput(
            setup_score=80,
            market_health_score=70,
            regime_alignment_score=100,
        )
    )

    expected = (80 * 0.45) + (70 * 0.35) + (100 * 0.20)
    assert result.confidence == expected
    assert result.setup_component == 36.0
    assert result.market_component == 24.5
    assert result.regime_component == 20.0
    assert result.weights == {
        "asset_setup": ASSET_SETUP_WEIGHT,
        "market_health": MARKET_HEALTH_WEIGHT,
        "regime_alignment": REGIME_ALIGNMENT_WEIGHT,
    }


def test_confidence_weights_sum_to_one() -> None:
    assert ASSET_SETUP_WEIGHT + MARKET_HEALTH_WEIGHT + REGIME_ALIGNMENT_WEIGHT == 1.0


def test_regime_alignment_tier_mapping() -> None:
    assert regime_alignment_score_from_tier(RegimeAlignmentTier.TIER_1) == 100.0
    assert regime_alignment_score_from_tier(RegimeAlignmentTier.TIER_2) == 65.0
    assert regime_alignment_score_from_tier(RegimeAlignmentTier.TIER_3) == 35.0
    assert regime_alignment_score_from_tier(RegimeAlignmentTier.NO_TRADE) == 0.0


def test_regime_alignment_tier_aliases() -> None:
    assert regime_alignment_score_from_tier("Tier 1") == 100.0
    assert regime_alignment_score_from_tier("risk-tier-2") == 65.0
    assert regime_alignment_score_from_tier("tier3") == 35.0
    assert regime_alignment_score_from_tier("blocked") == 0.0
    assert regime_alignment_score_from_tier("unknown") == 0.0
    assert regime_alignment_score_from_tier(None) == 0.0


def test_calculate_confidence_from_tier() -> None:
    result = calculate_confidence_from_tier(
        setup_score=90,
        market_health_score=80,
        tier="tier_2",
    )

    expected = (90 * 0.45) + (80 * 0.35) + (65 * 0.20)
    assert result.confidence == expected


def test_confidence_is_clamped_to_zero_to_hundred() -> None:
    high = calculate_confidence_score(
        ConfidenceInput(
            setup_score=150,
            market_health_score=150,
            regime_alignment_score=150,
        )
    )
    low = calculate_confidence_score(
        ConfidenceInput(
            setup_score=-50,
            market_health_score=-10,
            regime_alignment_score=-1,
        )
    )

    assert high.confidence == 100.0
    assert high.setup_component == 45.0
    assert high.market_component == 35.0
    assert high.regime_component == 20.0
    assert low.confidence == 0.0


def test_no_trade_regime_alignment_reduces_confidence() -> None:
    tier_1 = calculate_confidence_from_tier(
        setup_score=80,
        market_health_score=80,
        tier="tier_1",
    )
    no_trade = calculate_confidence_from_tier(
        setup_score=80,
        market_health_score=80,
        tier="no_trade",
    )

    assert tier_1.confidence == 84.0
    assert no_trade.confidence == 64.0
    assert tier_1.confidence - no_trade.confidence == 20.0


def test_regime_alignment_score_from_decision_dict() -> None:
    assert regime_alignment_score_from_decision({"risk_tier": "tier_1"}) == 100.0
    assert regime_alignment_score_from_decision({"tier": "tier_2"}) == 65.0
    assert regime_alignment_score_from_decision({"action": "NO_TRADE"}) == 0.0
    assert regime_alignment_score_from_decision({}) == 0.0


def test_regime_alignment_score_from_decision_object() -> None:
    @dataclass(frozen=True)
    class Decision:
        risk_tier: str

    assert regime_alignment_score_from_decision(Decision(risk_tier="tier_3")) == 35.0
