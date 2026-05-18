from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from decision_engine import (  # noqa: E402
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
