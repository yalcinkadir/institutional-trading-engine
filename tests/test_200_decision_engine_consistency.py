from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pytest

from src.decision_engine import Decision, MarketContext, MarketState, SetupCandidate, SetupType, evaluate_candidate
from src.decision.probabilistic_decision_engine import probabilistic_decision_engine

CANONICAL_ENGINE_PATH = "src.decision_engine.evaluate_candidate"
PROBABILISTIC_ENGINE_PATH = "src.decision.probabilistic_decision_engine.probabilistic_decision_engine"
EXACT_MATCH_FIELDS = ("boundary",)
ALLOWED_DIFFERENCES = ("confidence_score", "probability_distribution", "position_size_multiplier", "risk_tier")


@dataclass(frozen=True)
class DecisionEngineSharedFixture:
    symbol: str
    market_state: str
    setup_type: str
    setup_score: float
    regime_alignment: float
    asymmetry_score: float
    data_confidence: float
    signal_score: float
    risk_score: float
    regime_confidence: float
    vix_term_structure_inverted: bool = False
    credit_spreads_widening: bool = False
    breadth_collapse: bool = False
    liquidity_stress: bool = False
    failed_breakout_cluster: bool = False
    max_portfolio_heat: float = 1.0


@dataclass(frozen=True)
class DecisionEngineConsistencyResult:
    is_consistent: bool
    canonical_boundary: str
    probabilistic_boundary: str
    canonical_engine: str
    probabilistic_engine: str
    exact_match_fields: tuple[str, ...]
    allowed_differences: tuple[str, ...]
    canonical_decision: str
    probabilistic_classification: str
    canonical_reasons: tuple[str, ...]


def _enum_value(value: Any) -> str:
    if hasattr(value, "value"):
        return str(value.value)
    return str(value)


def canonical_decision_boundary(decision_like: Any) -> str:
    if isinstance(decision_like, dict):
        decision = str(decision_like.get("decision") or "").strip().lower()
    else:
        decision = _enum_value(getattr(decision_like, "decision", "")).strip().lower()

    if decision in {Decision.APPROVED.value, Decision.REDUCED_SIZE.value}:
        return "actionable_bullish"
    if decision == Decision.WATCH.value:
        return "watch_or_neutral"
    return "defensive_or_blocked"


def probabilistic_decision_boundary(decision_like: Any) -> str:
    if isinstance(decision_like, dict):
        classification = str(decision_like.get("classification") or "").strip().lower()
    else:
        classification = str(getattr(decision_like, "classification", "")).strip().lower()

    if classification == "bullish":
        return "actionable_bullish"
    if classification == "neutral":
        return "watch_or_neutral"
    return "defensive_or_blocked"


def _canonical_context(fixture: DecisionEngineSharedFixture) -> MarketContext:
    return MarketContext(
        market_state=MarketState(str(fixture.market_state).strip().lower().replace("-", "_")),
        vix_term_structure_inverted=fixture.vix_term_structure_inverted,
        credit_spreads_widening=fixture.credit_spreads_widening,
        breadth_collapse=fixture.breadth_collapse,
        liquidity_stress=fixture.liquidity_stress,
        failed_breakout_cluster=fixture.failed_breakout_cluster,
        max_portfolio_heat=fixture.max_portfolio_heat,
    )


def _canonical_candidate(fixture: DecisionEngineSharedFixture) -> SetupCandidate:
    return SetupCandidate(
        symbol=fixture.symbol,
        setup_type=SetupType(str(fixture.setup_type).strip().lower().replace("-", "_")),
        setup_score=fixture.setup_score,
        regime_alignment=fixture.regime_alignment,
        asymmetry_score=fixture.asymmetry_score,
        data_confidence=fixture.data_confidence,
    )


def evaluate_decision_engine_consistency(
    fixture: DecisionEngineSharedFixture,
) -> DecisionEngineConsistencyResult:
    canonical_result = evaluate_candidate(
        _canonical_context(fixture),
        _canonical_candidate(fixture),
    )
    probabilistic_result = probabilistic_decision_engine.evaluate(
        signal_score=fixture.signal_score,
        risk_score=fixture.risk_score,
        regime_confidence=fixture.regime_confidence,
    )

    canonical_boundary = canonical_decision_boundary(canonical_result)
    probabilistic_boundary = probabilistic_decision_boundary(probabilistic_result)

    return DecisionEngineConsistencyResult(
        is_consistent=canonical_boundary == probabilistic_boundary,
        canonical_boundary=canonical_boundary,
        probabilistic_boundary=probabilistic_boundary,
        canonical_engine=CANONICAL_ENGINE_PATH,
        probabilistic_engine=PROBABILISTIC_ENGINE_PATH,
        exact_match_fields=EXACT_MATCH_FIELDS,
        allowed_differences=ALLOWED_DIFFERENCES,
        canonical_decision=canonical_result.decision.value,
        probabilistic_classification=probabilistic_result.classification,
        canonical_reasons=tuple(canonical_result.blocked_reasons),
    )


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
    assert result.canonical_engine == CANONICAL_ENGINE_PATH
    assert result.probabilistic_engine == PROBABILISTIC_ENGINE_PATH


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
