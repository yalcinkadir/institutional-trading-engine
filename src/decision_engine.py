"""
Decision Engine v3.

This module is intentionally small and deterministic. It models the key
institutional decision principles before adding more market-data complexity:

- hierarchy before additive scoring
- hard risk overrides before setup approval
- regime-to-setup mapping
- no-trade logic
- risk-tier based capital allocation

The goal is not to predict the market. The goal is to reject low-quality
risk and only allow setups whose context, asymmetry and confidence are aligned.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable


class MarketState(str, Enum):
    LOW_VOL_BULL = "low_vol_bull"
    HIGH_VOL_TRANSITION = "high_vol_transition"
    RISK_OFF = "risk_off"
    PANIC_DISLOCATION = "panic_dislocation"
    NEUTRAL = "neutral"


class SetupType(str, Enum):
    MOMENTUM_BREAKOUT = "momentum_breakout"
    PULLBACK_CONTINUATION = "pullback_continuation"
    MEAN_REVERSION = "mean_reversion"
    DEFENSIVE_ROTATION = "defensive_rotation"
    REVERSAL_ASYMMETRY = "reversal_asymmetry"
    SPECULATIVE_GROWTH = "speculative_growth"


class Decision(str, Enum):
    APPROVED = "approved"
    WATCH = "watch"
    REDUCED_SIZE = "reduced_size"
    BLOCKED = "blocked"
    NO_TRADE = "no_trade"


@dataclass(frozen=True)
class MarketContext:
    market_state: MarketState
    vix_term_structure_inverted: bool = False
    credit_spreads_widening: bool = False
    breadth_collapse: bool = False
    liquidity_stress: bool = False
    failed_breakout_cluster: bool = False
    max_portfolio_heat: float = 1.0


@dataclass(frozen=True)
class SetupCandidate:
    symbol: str
    setup_type: SetupType
    setup_score: float
    regime_alignment: float
    asymmetry_score: float
    data_confidence: float
    event_risk: bool = False
    sector_crowding: bool = False


@dataclass(frozen=True)
class DecisionResult:
    decision: Decision
    risk_tier: str
    position_size_multiplier: float
    allowed_setups: tuple[SetupType, ...]
    blocked_reasons: tuple[str, ...] = field(default_factory=tuple)
    notes: tuple[str, ...] = field(default_factory=tuple)


REGIME_SETUP_MAP: dict[MarketState, tuple[SetupType, ...]] = {
    MarketState.LOW_VOL_BULL: (
        SetupType.MOMENTUM_BREAKOUT,
        SetupType.PULLBACK_CONTINUATION,
        SetupType.SPECULATIVE_GROWTH,
    ),
    MarketState.HIGH_VOL_TRANSITION: (
        SetupType.MEAN_REVERSION,
        SetupType.PULLBACK_CONTINUATION,
        SetupType.DEFENSIVE_ROTATION,
    ),
    MarketState.RISK_OFF: (
        SetupType.DEFENSIVE_ROTATION,
        SetupType.MEAN_REVERSION,
    ),
    MarketState.PANIC_DISLOCATION: (
        SetupType.REVERSAL_ASYMMETRY,
        SetupType.DEFENSIVE_ROTATION,
    ),
    MarketState.NEUTRAL: (
        SetupType.PULLBACK_CONTINUATION,
        SetupType.MEAN_REVERSION,
    ),
}


def get_allowed_setups(market_state: MarketState) -> tuple[SetupType, ...]:
    """Return strategy types that are allowed in a given market state."""
    return REGIME_SETUP_MAP.get(market_state, REGIME_SETUP_MAP[MarketState.NEUTRAL])


def detect_hard_overrides(context: MarketContext) -> tuple[str, ...]:
    """Detect hard risk conditions that should override normal setup scoring."""
    reasons: list[str] = []

    if context.liquidity_stress:
        reasons.append("liquidity_stress")

    if (
        context.vix_term_structure_inverted
        and context.credit_spreads_widening
        and context.breadth_collapse
    ):
        reasons.append("systemic_risk_cluster")

    if context.market_state == MarketState.RISK_OFF and context.failed_breakout_cluster:
        reasons.append("breakout_failure_in_risk_off")

    if context.market_state == MarketState.PANIC_DISLOCATION and context.credit_spreads_widening:
        reasons.append("panic_credit_stress")

    return tuple(reasons)


def _base_risk_tier(candidate: SetupCandidate) -> str:
    if (
        candidate.setup_score >= 80
        and candidate.regime_alignment >= 0.75
        and candidate.asymmetry_score >= 0.70
        and candidate.data_confidence >= 0.80
    ):
        return "tier_1"

    if (
        candidate.setup_score >= 65
        and candidate.regime_alignment >= 0.55
        and candidate.asymmetry_score >= 0.55
        and candidate.data_confidence >= 0.65
    ):
        return "tier_2"

    if (
        candidate.setup_score >= 50
        and candidate.regime_alignment >= 0.40
        and candidate.asymmetry_score >= 0.40
        and candidate.data_confidence >= 0.50
    ):
        return "tier_3"

    return "no_trade"


def _size_for_tier(risk_tier: str) -> float:
    return {
        "tier_1": 1.0,
        "tier_2": 0.5,
        "tier_3": 0.25,
        "no_trade": 0.0,
    }[risk_tier]


def evaluate_candidate(context: MarketContext, candidate: SetupCandidate) -> DecisionResult:
    """
    Evaluate a setup with hierarchy-first logic.

    The order is deliberate:
    1. Determine regime-allowed setup types.
    2. Detect hard overrides.
    3. Reject setup types that do not belong to the current regime.
    4. Reject weak asymmetry/data-confidence candidates.
    5. Assign risk tier and size multiplier.
    """
    allowed_setups = get_allowed_setups(context.market_state)
    hard_overrides = detect_hard_overrides(context)
    notes: list[str] = []

    if hard_overrides:
        return DecisionResult(
            decision=Decision.BLOCKED,
            risk_tier="no_trade",
            position_size_multiplier=0.0,
            allowed_setups=allowed_setups,
            blocked_reasons=hard_overrides,
            notes=("hard_override_before_score",),
        )

    if candidate.setup_type not in allowed_setups:
        return DecisionResult(
            decision=Decision.BLOCKED,
            risk_tier="no_trade",
            position_size_multiplier=0.0,
            allowed_setups=allowed_setups,
            blocked_reasons=("setup_not_allowed_in_current_regime",),
        )

    if candidate.asymmetry_score < 0.40:
        return DecisionResult(
            decision=Decision.NO_TRADE,
            risk_tier="no_trade",
            position_size_multiplier=0.0,
            allowed_setups=allowed_setups,
            blocked_reasons=("poor_asymmetry",),
        )

    if candidate.data_confidence < 0.50:
        return DecisionResult(
            decision=Decision.NO_TRADE,
            risk_tier="no_trade",
            position_size_multiplier=0.0,
            allowed_setups=allowed_setups,
            blocked_reasons=("low_data_confidence",),
        )

    risk_tier = _base_risk_tier(candidate)
    size = _size_for_tier(risk_tier)

    if candidate.event_risk:
        size *= 0.5
        notes.append("event_risk_size_reduction")

    if candidate.sector_crowding:
        size *= 0.75
        notes.append("sector_crowding_size_reduction")

    if context.market_state == MarketState.HIGH_VOL_TRANSITION:
        size *= 0.5
        notes.append("high_vol_transition_size_reduction")

    size *= max(0.0, min(1.0, context.max_portfolio_heat))

    if risk_tier == "no_trade" or size == 0:
        return DecisionResult(
            decision=Decision.NO_TRADE,
            risk_tier="no_trade",
            position_size_multiplier=0.0,
            allowed_setups=allowed_setups,
            blocked_reasons=("insufficient_quality_threshold",),
            notes=tuple(notes),
        )

    if context.market_state == MarketState.HIGH_VOL_TRANSITION or size < _size_for_tier(risk_tier):
        decision = Decision.REDUCED_SIZE
    elif risk_tier == "tier_3":
        decision = Decision.WATCH
    else:
        decision = Decision.APPROVED

    return DecisionResult(
        decision=decision,
        risk_tier=risk_tier,
        position_size_multiplier=round(size, 4),
        allowed_setups=allowed_setups,
        notes=tuple(notes),
    )


def rank_candidates(
    context: MarketContext, candidates: Iterable[SetupCandidate]
) -> list[tuple[SetupCandidate, DecisionResult]]:
    """Evaluate and sort candidates by decision quality and risk allocation."""
    evaluated = [(candidate, evaluate_candidate(context, candidate)) for candidate in candidates]

    decision_priority = {
        Decision.APPROVED: 4,
        Decision.REDUCED_SIZE: 3,
        Decision.WATCH: 2,
        Decision.NO_TRADE: 1,
        Decision.BLOCKED: 0,
    }

    return sorted(
        evaluated,
        key=lambda item: (
            decision_priority[item[1].decision],
            item[1].position_size_multiplier,
            item[0].asymmetry_score,
            item[0].regime_alignment,
            item[0].setup_score,
        ),
        reverse=True,
    )
