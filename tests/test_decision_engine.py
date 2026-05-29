from src.config.thresholds import DEFAULT_THRESHOLDS, DecisionThresholds
from src.decision_engine import (
    Decision,
    MarketContext,
    MarketState,
    SetupCandidate,
    SetupType,
    evaluate_candidate,
    get_allowed_setups,
    rank_candidates,
)


def test_low_vol_bull_allows_momentum_breakout():
    context = MarketContext(market_state=MarketState.LOW_VOL_BULL)
    candidate = SetupCandidate(
        symbol="QQQ",
        setup_type=SetupType.MOMENTUM_BREAKOUT,
        setup_score=86,
        regime_alignment=0.88,
        asymmetry_score=0.78,
        data_confidence=0.91,
    )

    result = evaluate_candidate(context, candidate)

    assert result.decision == Decision.APPROVED
    assert result.risk_tier == "tier_1"
    assert result.position_size_multiplier == 1.0
    assert SetupType.MOMENTUM_BREAKOUT in result.allowed_setups
    assert f"thresholds_version={DEFAULT_THRESHOLDS.version}" in result.notes


def test_custom_thresholds_can_downgrade_candidate_without_code_change():
    context = MarketContext(market_state=MarketState.LOW_VOL_BULL)
    candidate = SetupCandidate(
        symbol="QQQ",
        setup_type=SetupType.MOMENTUM_BREAKOUT,
        setup_score=86,
        regime_alignment=0.88,
        asymmetry_score=0.78,
        data_confidence=0.91,
    )
    strict_thresholds = DecisionThresholds(
        tier1_setup_score=90.0,
        tier1_regime_alignment=0.90,
        tier1_asymmetry=0.85,
        tier1_data_confidence=0.95,
        version="test-strict-v1",
    )

    result = evaluate_candidate(context, candidate, strict_thresholds)

    assert result.decision == Decision.APPROVED
    assert result.risk_tier == "tier_2"
    assert result.position_size_multiplier == 0.5
    assert "thresholds_version=test-strict-v1" in result.notes


def test_custom_minimum_thresholds_can_reject_candidate():
    context = MarketContext(market_state=MarketState.LOW_VOL_BULL)
    candidate = SetupCandidate(
        symbol="AAPL",
        setup_type=SetupType.PULLBACK_CONTINUATION,
        setup_score=90,
        regime_alignment=0.90,
        asymmetry_score=0.45,
        data_confidence=0.93,
    )
    strict_thresholds = DecisionThresholds(min_asymmetry=0.50, version="test-min-v1")

    result = evaluate_candidate(context, candidate, strict_thresholds)

    assert result.decision == Decision.NO_TRADE
    assert result.risk_tier == "no_trade"
    assert "poor_asymmetry" in result.blocked_reasons
    assert "thresholds_version=test-min-v1" in result.notes


def test_systemic_risk_cluster_blocks_score_before_setup_quality():
    context = MarketContext(
        market_state=MarketState.LOW_VOL_BULL,
        vix_term_structure_inverted=True,
        credit_spreads_widening=True,
        breadth_collapse=True,
    )
    candidate = SetupCandidate(
        symbol="NVDA",
        setup_type=SetupType.MOMENTUM_BREAKOUT,
        setup_score=99,
        regime_alignment=0.95,
        asymmetry_score=0.90,
        data_confidence=0.95,
    )

    result = evaluate_candidate(context, candidate)

    assert result.decision == Decision.BLOCKED
    assert result.position_size_multiplier == 0.0
    assert "systemic_risk_cluster" in result.blocked_reasons
    assert "hard_override_before_score" in result.notes
    assert f"thresholds_version={DEFAULT_THRESHOLDS.version}" in result.notes


def test_risk_off_blocks_speculative_growth_even_with_good_score():
    context = MarketContext(market_state=MarketState.RISK_OFF)
    candidate = SetupCandidate(
        symbol="PLTR",
        setup_type=SetupType.SPECULATIVE_GROWTH,
        setup_score=88,
        regime_alignment=0.80,
        asymmetry_score=0.76,
        data_confidence=0.90,
    )

    result = evaluate_candidate(context, candidate)

    assert result.decision == Decision.BLOCKED
    assert "setup_not_allowed_in_current_regime" in result.blocked_reasons
    assert SetupType.SPECULATIVE_GROWTH not in get_allowed_setups(MarketState.RISK_OFF)


def test_poor_regime_alignment_returns_no_trade_before_tier_scoring():
    context = MarketContext(market_state=MarketState.LOW_VOL_BULL)
    candidate = SetupCandidate(
        symbol="NVDA",
        setup_type=SetupType.MOMENTUM_BREAKOUT,
        setup_score=99,
        regime_alignment=0.20,
        asymmetry_score=0.95,
        data_confidence=0.95,
    )

    result = evaluate_candidate(context, candidate)

    assert result.decision == Decision.NO_TRADE
    assert result.risk_tier == "no_trade"
    assert result.position_size_multiplier == 0.0
    assert "poor_regime_alignment" in result.blocked_reasons
    assert "regime_alignment_independent_gate" in result.notes


def test_custom_regime_alignment_floor_can_reject_candidate():
    context = MarketContext(market_state=MarketState.LOW_VOL_BULL)
    candidate = SetupCandidate(
        symbol="MSFT",
        setup_type=SetupType.PULLBACK_CONTINUATION,
        setup_score=90,
        regime_alignment=0.52,
        asymmetry_score=0.82,
        data_confidence=0.91,
    )
    strict_thresholds = DecisionThresholds(
        tier3_regime_alignment=0.60,
        version="test-regime-floor-v1",
    )

    result = evaluate_candidate(context, candidate, strict_thresholds)

    assert result.decision == Decision.NO_TRADE
    assert result.risk_tier == "no_trade"
    assert "poor_regime_alignment" in result.blocked_reasons
    assert "thresholds_version=test-regime-floor-v1" in result.notes


def test_high_vol_transition_reduces_position_size():
    context = MarketContext(market_state=MarketState.HIGH_VOL_TRANSITION)
    candidate = SetupCandidate(
        symbol="SPY",
        setup_type=SetupType.MEAN_REVERSION,
        setup_score=82,
        regime_alignment=0.77,
        asymmetry_score=0.74,
        data_confidence=0.86,
    )

    result = evaluate_candidate(context, candidate)

    assert result.decision == Decision.REDUCED_SIZE
    assert result.risk_tier == "tier_1"
    assert result.position_size_multiplier == 0.5
    assert "high_vol_transition_size_reduction" in result.notes


def test_poor_asymmetry_returns_no_trade():
    context = MarketContext(market_state=MarketState.LOW_VOL_BULL)
    candidate = SetupCandidate(
        symbol="AAPL",
        setup_type=SetupType.PULLBACK_CONTINUATION,
        setup_score=90,
        regime_alignment=0.90,
        asymmetry_score=0.25,
        data_confidence=0.93,
    )

    result = evaluate_candidate(context, candidate)

    assert result.decision == Decision.NO_TRADE
    assert result.risk_tier == "no_trade"
    assert "poor_asymmetry" in result.blocked_reasons


def test_ranking_prefers_approved_asymmetric_candidate_over_blocked_high_score():
    context = MarketContext(market_state=MarketState.LOW_VOL_BULL)
    approved = SetupCandidate(
        symbol="MSFT",
        setup_type=SetupType.PULLBACK_CONTINUATION,
        setup_score=82,
        regime_alignment=0.80,
        asymmetry_score=0.82,
        data_confidence=0.85,
    )
    blocked = SetupCandidate(
        symbol="DEF",
        setup_type=SetupType.DEFENSIVE_ROTATION,
        setup_score=99,
        regime_alignment=0.95,
        asymmetry_score=0.95,
        data_confidence=0.95,
    )

    ranked = rank_candidates(context, [blocked, approved])

    assert ranked[0][0].symbol == "MSFT"
    assert ranked[0][1].decision == Decision.APPROVED
    assert ranked[1][1].decision == Decision.BLOCKED


def test_ranking_puts_poor_regime_alignment_below_approved_candidate():
    context = MarketContext(market_state=MarketState.LOW_VOL_BULL)
    approved = SetupCandidate(
        symbol="MSFT",
        setup_type=SetupType.PULLBACK_CONTINUATION,
        setup_score=82,
        regime_alignment=0.80,
        asymmetry_score=0.82,
        data_confidence=0.85,
    )
    poor_regime = SetupCandidate(
        symbol="NVDA",
        setup_type=SetupType.MOMENTUM_BREAKOUT,
        setup_score=99,
        regime_alignment=0.20,
        asymmetry_score=0.95,
        data_confidence=0.95,
    )

    ranked = rank_candidates(context, [poor_regime, approved])

    assert ranked[0][0].symbol == "MSFT"
    assert ranked[0][1].decision == Decision.APPROVED
    assert ranked[1][0].symbol == "NVDA"
    assert ranked[1][1].decision == Decision.NO_TRADE
    assert "poor_regime_alignment" in ranked[1][1].blocked_reasons


def test_ranking_uses_custom_thresholds():
    context = MarketContext(market_state=MarketState.LOW_VOL_BULL)
    candidate = SetupCandidate(
        symbol="MSFT",
        setup_type=SetupType.PULLBACK_CONTINUATION,
        setup_score=82,
        regime_alignment=0.80,
        asymmetry_score=0.82,
        data_confidence=0.85,
    )
    strict_thresholds = DecisionThresholds(
        tier1_setup_score=90.0,
        tier1_regime_alignment=0.90,
        tier1_asymmetry=0.90,
        tier1_data_confidence=0.90,
        version="rank-test-v1",
    )

    ranked = rank_candidates(context, [candidate], strict_thresholds)

    assert ranked[0][1].risk_tier == "tier_2"
    assert "thresholds_version=rank-test-v1" in ranked[0][1].notes
