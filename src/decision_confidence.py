"""Orthogonal confidence scoring for decision quality.

P36 removes structural double counting by separating confidence into:
- asset-level setup quality
- market-level health
- regime-level alignment

The helper intentionally does not consume VIX or market breadth directly. Those inputs
belong inside market_health_score and must not be added a second time here.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


ASSET_SETUP_WEIGHT = 0.45
MARKET_HEALTH_WEIGHT = 0.35
REGIME_ALIGNMENT_WEIGHT = 0.20


class RegimeAlignmentTier(str, Enum):
    TIER_1 = "tier_1"
    TIER_2 = "tier_2"
    TIER_3 = "tier_3"
    NO_TRADE = "no_trade"


REGIME_ALIGNMENT_SCORES = {
    RegimeAlignmentTier.TIER_1: 100.0,
    RegimeAlignmentTier.TIER_2: 65.0,
    RegimeAlignmentTier.TIER_3: 35.0,
    RegimeAlignmentTier.NO_TRADE: 0.0,
}


@dataclass(frozen=True)
class ConfidenceInput:
    setup_score: float
    market_health_score: float
    regime_alignment_score: float


@dataclass(frozen=True)
class ConfidenceScore:
    confidence: float
    setup_component: float
    market_component: float
    regime_component: float
    weights: dict[str, float]


def clamp_score(value: float) -> float:
    return max(0.0, min(100.0, float(value)))


def regime_alignment_score_from_tier(tier: RegimeAlignmentTier | str | None) -> float:
    if tier is None:
        return REGIME_ALIGNMENT_SCORES[RegimeAlignmentTier.NO_TRADE]

    if isinstance(tier, RegimeAlignmentTier):
        return REGIME_ALIGNMENT_SCORES[tier]

    normalized = str(tier).strip().lower().replace(" ", "_").replace("-", "_")
    aliases = {
        "1": RegimeAlignmentTier.TIER_1,
        "tier1": RegimeAlignmentTier.TIER_1,
        "tier_1": RegimeAlignmentTier.TIER_1,
        "risk_tier_1": RegimeAlignmentTier.TIER_1,
        "2": RegimeAlignmentTier.TIER_2,
        "tier2": RegimeAlignmentTier.TIER_2,
        "tier_2": RegimeAlignmentTier.TIER_2,
        "risk_tier_2": RegimeAlignmentTier.TIER_2,
        "3": RegimeAlignmentTier.TIER_3,
        "tier3": RegimeAlignmentTier.TIER_3,
        "tier_3": RegimeAlignmentTier.TIER_3,
        "risk_tier_3": RegimeAlignmentTier.TIER_3,
        "no_trade": RegimeAlignmentTier.NO_TRADE,
        "notrade": RegimeAlignmentTier.NO_TRADE,
        "block": RegimeAlignmentTier.NO_TRADE,
        "blocked": RegimeAlignmentTier.NO_TRADE,
    }
    mapped = aliases.get(normalized)
    if mapped is None:
        return REGIME_ALIGNMENT_SCORES[RegimeAlignmentTier.NO_TRADE]
    return REGIME_ALIGNMENT_SCORES[mapped]


def regime_alignment_score_from_decision(decision: Any) -> float:
    """Extract a regime-alignment score from a decision-like object.

    Supports dictionaries and lightweight objects with common risk tier fields.
    Unknown or missing tiers are treated conservatively as no-trade alignment.
    """

    candidate_keys = (
        "risk_tier",
        "tier",
        "regime_tier",
        "decision_tier",
        "classification",
        "action",
    )

    if isinstance(decision, dict):
        for key in candidate_keys:
            if key in decision:
                return regime_alignment_score_from_tier(decision.get(key))
        return REGIME_ALIGNMENT_SCORES[RegimeAlignmentTier.NO_TRADE]

    for key in candidate_keys:
        if hasattr(decision, key):
            return regime_alignment_score_from_tier(getattr(decision, key))

    return REGIME_ALIGNMENT_SCORES[RegimeAlignmentTier.NO_TRADE]


def calculate_confidence_score(data: ConfidenceInput) -> ConfidenceScore:
    setup = clamp_score(data.setup_score)
    market = clamp_score(data.market_health_score)
    regime = clamp_score(data.regime_alignment_score)

    setup_component = setup * ASSET_SETUP_WEIGHT
    market_component = market * MARKET_HEALTH_WEIGHT
    regime_component = regime * REGIME_ALIGNMENT_WEIGHT
    confidence = clamp_score(setup_component + market_component + regime_component)

    return ConfidenceScore(
        confidence=round(confidence, 4),
        setup_component=round(setup_component, 4),
        market_component=round(market_component, 4),
        regime_component=round(regime_component, 4),
        weights={
            "asset_setup": ASSET_SETUP_WEIGHT,
            "market_health": MARKET_HEALTH_WEIGHT,
            "regime_alignment": REGIME_ALIGNMENT_WEIGHT,
        },
    )


def calculate_confidence_from_tier(
    *,
    setup_score: float,
    market_health_score: float,
    tier: RegimeAlignmentTier | str | None,
) -> ConfidenceScore:
    return calculate_confidence_score(
        ConfidenceInput(
            setup_score=setup_score,
            market_health_score=market_health_score,
            regime_alignment_score=regime_alignment_score_from_tier(tier),
        )
    )
