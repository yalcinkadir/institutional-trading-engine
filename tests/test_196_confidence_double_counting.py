from __future__ import annotations

import pytest

from src.decision_confidence import (
    ConfidenceInput,
    calculate_confidence_from_components,
    calculate_confidence_score,
    calculate_confidence_with_tier_discount,
    regime_alignment_score_from_decision,
    risk_tier_discount_score,
)


def test_196_confidence_output_includes_component_provenance() -> None:
    result = calculate_confidence_score(
        ConfidenceInput(
            setup_score=80,
            market_health_score=70,
            regime_alignment_score=60,
        )
    )

    assert result.provenance["canonical_confidence_path"] == "src.decision_confidence.calculate_confidence_score"
    assert result.provenance["components"]["asset_setup"]["source"] == "setup_score"
    assert result.provenance["components"]["market_health"]["source"] == "market_health_score"
    assert result.provenance["components"]["regime_alignment"]["source"] == "independent_regime_alignment_score"
    assert result.provenance["risk_tier_used_as_regime_alignment"] is False
    assert result.provenance["double_counting_guard"] == "risk_tier_must_not_be_used_as_independent_regime_evidence"


def test_196_risk_tier_is_discount_not_independent_regime_evidence() -> None:
    result = calculate_confidence_with_tier_discount(
        setup_score=90,
        market_health_score=80,
        independent_regime_alignment_score=75,
        risk_tier="tier_3",
    )

    assert result.provenance["components"]["risk_tier_adjustment"]["source"] == "risk_tier_discount"
    assert result.provenance["components"]["risk_tier_adjustment"]["used_as_independent_regime_evidence"] is False
    assert result.provenance["risk_tier_used_as_regime_alignment"] is False
    assert result.provenance["legacy_tier_regime_mapping"] == "deprecated"
    assert result.confidence < calculate_confidence_score(
        ConfidenceInput(
            setup_score=90,
            market_health_score=80,
            regime_alignment_score=75,
        )
    ).confidence


def test_196_regime_alignment_from_decision_requires_independent_field() -> None:
    assert regime_alignment_score_from_decision({"risk_tier": "tier_1"}) == 0.0
    assert regime_alignment_score_from_decision({"regime_alignment_score": 72}) == 72.0
    assert regime_alignment_score_from_decision({"regime_alignment": 0.82}) == 82.0


@pytest.mark.parametrize(
    ("tier", "expected"),
    [
        ("tier_1", 0.0),
        ("tier_2", -5.0),
        ("tier_3", -10.0),
        ("no_trade", -20.0),
        ("blocked", -20.0),
        (None, -20.0),
    ],
)
def test_196_risk_tier_discount_is_explicit(tier: str | None, expected: float) -> None:
    assert risk_tier_discount_score(tier) == expected


def test_196_component_api_is_canonical_and_rejects_tier_as_regime_input() -> None:
    result = calculate_confidence_from_components(
        setup_score=75,
        market_health_score=70,
        independent_regime_alignment_score=65,
    )

    assert result.confidence == calculate_confidence_score(
        ConfidenceInput(
            setup_score=75,
            market_health_score=70,
            regime_alignment_score=65,
        )
    ).confidence
    assert result.provenance["canonical_confidence_path"] == "src.decision_confidence.calculate_confidence_score"
