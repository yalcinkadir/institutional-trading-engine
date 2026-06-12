from __future__ import annotations

import pytest

from src.decision_engine import MarketContext, MarketState, SetupCandidate, SetupType, evaluate_candidate
from src.decision_engine_consistency import (
    DecisionEngineSharedFixture,
    canonical_decision_boundary,
    evaluate_decision_engine_consistency,
    probabilistic_decision_boundary,
)
from src.decision.probabilistic_decision_engine import probabilistic_decision_engine


def _canonical_fixture() -> DecisionEngineSharedFixture:
    return DecisionEngineSharedFixture(
        symbol="NVDA",
        market_state="low_vol_bull",
        setup_type="momentum_breakout",
        setup_score=86.0,
        regime_alignment=0.84,
        asymmetry_score=0.78,
        data_confidence=0.88,
        signal_score=86.0,
        risk_score=20.0,
        regime_confidence=84.0,
    )


def test_200_decision_engines_consistent_for_same_bullish_input() -> None:
    result = evaluate_decision_engine_consistency(_canonical_fixture())

    assert result.is_consistent is True
    assert result.canonical_boundary == "actionable_bullish"
    assert result.probabilistic_boundary == "actionable_bullish"
    assert result.exact_match_fields == ("boundary",)
    assert result.allowed_differences == ("confidence_score", "probability_distribution", "position_size_multiplier", "risk_tier")
    assert result.canonical_engine == "src.decision_engine.evaluate_candidate"
    assert result.probabilistic_engine == "src.decision.probabilistic_decision_engine.probabilistic_decision_engine"


def test_200_decision_engines_consistent_for_blocked_risk_input() -> None:
    fixture = DecisionEngineSharedFixture(
        symbol="QQQ",
        market_state="risk_off",
        setup_type="momentum_breakout",
        setup_score=88.0,
        regime_alignment=0.86,
        asymmetry_score=0.80,
        data_confidence=0.90,
        signal_score=88.0,
        risk_score=92.0,
        regime_confidence=25.0,
        failed_breakout_cluster=True,
    )

    result = evaluate_decision_engine_consistency(fixture)

    assert result.is_consistent is True
    assert result.canonical_boundary == "defensive_or_blocked"
    assert result.probabilistic_boundary == "defensive_or_blocked"
    assert "breakout_failure_in_risk_off" in result.canonical_reasons


def test_200_boundary_adapter_detects_undocumented_divergence() -> None:
    fixture = _canonical_fixture()
    canonical_context = MarketContext(market_state=MarketState.LOW_VOL_BULL)
    canonical_candidate = SetupCandidate(
        symbol=fixture.symbol,
        setup_type=SetupType.MOMENTUM_BREAKOUT,
        setup_score=fixture.setup_score,
        regime_alignment=fixture.regime_alignment,
        asymmetry_score=fixture.asymmetry_score,
        data_confidence=fixture.data_confidence,
    )
    canonical = evaluate_candidate(canonical_context, canonical_candidate)
    probabilistic = probabilistic_decision_engine.evaluate(
        signal_score=fixture.signal_score,
        risk_score=95.0,
        regime_confidence=5.0,
    )

    assert canonical_decision_boundary(canonical) == "actionable_bullish"
    assert probabilistic_decision_boundary(probabilistic) == "defensive_or_blocked"


@pytest.mark.parametrize(
    ("decision", "expected"),
    [
        ("approved", "actionable_bullish"),
        ("reduced_size", "actionable_bullish"),
        ("watch", "watch_or_neutral"),
        ("no_trade", "defensive_or_blocked"),
        ("blocked", "defensive_or_blocked"),
    ],
)
def test_200_canonical_boundary_contract_is_explicit(decision: str, expected: str) -> None:
    assert canonical_decision_boundary({"decision": decision}) == expected


@pytest.mark.parametrize(
    ("classification", "expected"),
    [
        ("bullish", "actionable_bullish"),
        ("neutral", "watch_or_neutral"),
        ("bearish", "defensive_or_blocked"),
    ],
)
def test_200_probabilistic_boundary_contract_is_explicit(classification: str, expected: str) -> None:
    assert probabilistic_decision_boundary({"classification": classification}) == expected
