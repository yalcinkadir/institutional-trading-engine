"""Decision engine consistency boundary adapter.

#200 does not require the canonical decision engine and probabilistic decision
engine to have identical internals. It requires a documented output-boundary
contract so report/orchestration paths cannot drift silently.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from src.decision_engine import (
    Decision,
    MarketContext,
    MarketState,
    SetupCandidate,
    SetupType,
    evaluate_candidate,
)
from src.decision.probabilistic_decision_engine import probabilistic_decision_engine


CANONICAL_ENGINE_PATH = "src.decision_engine.evaluate_candidate"
PROBABILISTIC_ENGINE_PATH = "src.decision.probabilistic_decision_engine.probabilistic_decision_engine"
EXACT_MATCH_FIELDS = ("boundary",)
ALLOWED_DIFFERENCES = (
    "confidence_score",
    "probability_distribution",
    "position_size_multiplier",
    "risk_tier",
)


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


def _market_state(value: str) -> MarketState:
    normalized = str(value).strip().lower().replace("-", "_")
    return MarketState(normalized)


def _setup_type(value: str) -> SetupType:
    normalized = str(value).strip().lower().replace("-", "_")
    return SetupType(normalized)


def _canonical_context(fixture: DecisionEngineSharedFixture) -> MarketContext:
    return MarketContext(
        market_state=_market_state(fixture.market_state),
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
        setup_type=_setup_type(fixture.setup_type),
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
