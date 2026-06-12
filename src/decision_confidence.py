"""Canonical confidence scoring for decision quality.

#196 makes confidence provenance explicit and prevents risk-tier derived values from
being presented as independent regime-alignment evidence.

Canonical components:
- asset setup score
- market health score
- independent regime-alignment score

Risk tier may be used only as an explicit discount/penalty. It must not be used as
an independent regime signal because risk tier is already derived from setup,
regime, asymmetry and data-confidence inputs.
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


# Deprecated compatibility map. Kept for legacy callers, but not used as
# independent regime evidence by canonical confidence provenance.
REGIME_ALIGNMENT_SCORES = {
    RegimeAlignmentTier.TIER_1: 100.0,
    RegimeAlignmentTier.TIER_2: 65.0,
    RegimeAlignmentTier.TIER_3: 35.0,
    RegimeAlignmentTier.NO_TRADE: 0.0,
}

RISK_TIER_DISCOUNTS = {
    RegimeAlignmentTier.TIER_1: 0.0,
    RegimeAlignmentTier.TIER_2: -5.0,
    RegimeAlignmentTier.TIER_3: -10.0,
    RegimeAlignmentTier.NO_TRADE: -20.0,
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
    provenance: dict[str, Any]


def clamp_score(value: float) -> float:
    return max(0.0, min(100.0, float(value)))


def _normalize_tier(tier: RegimeAlignmentTier | str | None) -> RegimeAlignmentTier:
    if tier is None:
        return RegimeAlignmentTier.NO_TRADE

    if isinstance(tier, RegimeAlignmentTier):
        return tier

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
    return aliases.get(normalized, RegimeAlignmentTier.NO_TRADE)


def regime_alignment_score_from_tier(tier: RegimeAlignmentTier | str | None) -> float:
    """Deprecated compatibility mapping.

    This function remains for legacy tests/callers, but #196 forbids using the
    returned value as independent regime evidence in canonical confidence output.
    Use `risk_tier_discount_score()` when tier information must influence
    confidence.
    """

    return REGIME_ALIGNMENT_SCORES[_normalize_tier(tier)]


def risk_tier_discount_score(tier: RegimeAlignmentTier | str | None) -> float:
    return RISK_TIER_DISCOUNTS[_normalize_tier(tier)]


def _coerce_alignment_value(value: Any) -> float | None:
    if value is None:
        return None
    try:
        score = float(value)
    except (TypeError, ValueError):
        return None
    if 0.0 <= score <= 1.0:
        score *= 100.0
    return clamp_score(score)


def regime_alignment_score_from_decision(decision: Any) -> float:
    """Extract independent regime-alignment score from a decision-like object.

    #196 intentionally ignores `risk_tier`, `tier`, `decision_tier`,
    `classification` and `action`. Those fields are downstream classifications,
    not independent regime evidence.
    """

    candidate_keys = (
        "regime_alignment_score",
        "regime_alignment",
        "market_regime_alignment",
        "independent_regime_alignment_score",
    )

    if isinstance(decision, dict):
        for key in candidate_keys:
            if key in decision:
                score = _coerce_alignment_value(decision.get(key))
                return 0.0 if score is None else score
        return 0.0

    for key in candidate_keys:
        if hasattr(decision, key):
            score = _coerce_alignment_value(getattr(decision, key))
            return 0.0 if score is None else score

    return 0.0


def _confidence_provenance(*, risk_tier_adjustment: float | None = None) -> dict[str, Any]:
    components: dict[str, Any] = {
        "asset_setup": {
            "source": "setup_score",
            "weight": ASSET_SETUP_WEIGHT,
        },
        "market_health": {
            "source": "market_health_score",
            "weight": MARKET_HEALTH_WEIGHT,
        },
        "regime_alignment": {
            "source": "independent_regime_alignment_score",
            "weight": REGIME_ALIGNMENT_WEIGHT,
        },
    }
    if risk_tier_adjustment is not None:
        components["risk_tier_adjustment"] = {
            "source": "risk_tier_discount",
            "weight": 0.0,
            "score_delta": risk_tier_adjustment,
            "used_as_independent_regime_evidence": False,
        }

    return {
        "canonical_confidence_path": "src.decision_confidence.calculate_confidence_score",
        "components": components,
        "risk_tier_used_as_regime_alignment": False,
        "legacy_tier_regime_mapping": "deprecated",
        "double_counting_guard": "risk_tier_must_not_be_used_as_independent_regime_evidence",
    }


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
        provenance=_confidence_provenance(),
    )


def calculate_confidence_from_components(
    *,
    setup_score: float,
    market_health_score: float,
    independent_regime_alignment_score: float,
) -> ConfidenceScore:
    return calculate_confidence_score(
        ConfidenceInput(
            setup_score=setup_score,
            market_health_score=market_health_score,
            regime_alignment_score=independent_regime_alignment_score,
        )
    )


def calculate_confidence_with_tier_discount(
    *,
    setup_score: float,
    market_health_score: float,
    independent_regime_alignment_score: float,
    risk_tier: RegimeAlignmentTier | str | None,
) -> ConfidenceScore:
    base = calculate_confidence_from_components(
        setup_score=setup_score,
        market_health_score=market_health_score,
        independent_regime_alignment_score=independent_regime_alignment_score,
    )
    discount = risk_tier_discount_score(risk_tier)
    confidence = clamp_score(base.confidence + discount)
    return ConfidenceScore(
        confidence=round(confidence, 4),
        setup_component=base.setup_component,
        market_component=base.market_component,
        regime_component=base.regime_component,
        weights=base.weights,
        provenance=_confidence_provenance(risk_tier_adjustment=discount),
    )


def calculate_confidence_from_tier(
    *,
    setup_score: float,
    market_health_score: float,
    tier: RegimeAlignmentTier | str | None,
) -> ConfidenceScore:
    """Legacy API retained as tier-discount confidence, not regime evidence.

    The old implementation used `tier` as the regime-alignment component. #196
    changes this to use neutral independent regime evidence plus an explicit tier
    discount so downstream users can see the dependency.
    """

    return calculate_confidence_with_tier_discount(
        setup_score=setup_score,
        market_health_score=market_health_score,
        independent_regime_alignment_score=50.0,
        risk_tier=tier,
    )
