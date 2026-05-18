from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.meta_learning_engine import (  # noqa: E402
    MetaLearningRecord,
    build_meta_learning_assessment,
)


def test_meta_learning_detects_strong_and_weak_factors():
    records = []

    for _ in range(8):
        records.append(
            MetaLearningRecord(
                setup_type="momentum_breakout",
                market_state="risk_on",
                factor_tags=("breadth_confirmation", "relative_strength"),
                confidence=0.85,
                risk_tier="tier_1",
                result_5d=4.0,
            )
        )

    for _ in range(8):
        records.append(
            MetaLearningRecord(
                setup_type="extended_breakout",
                market_state="fragile_transition",
                factor_tags=("extended_entry",),
                confidence=0.88,
                risk_tier="tier_1",
                result_5d=-3.5,
            )
        )

    result = build_meta_learning_assessment(records)

    assert "breadth_confirmation" in result.strongest_factors
    assert "extended_entry" in result.weakest_factors


def test_meta_learning_detects_overconfident_mapping():
    records = []

    for _ in range(10):
        records.append(
            MetaLearningRecord(
                setup_type="weak_setup",
                market_state="fragile",
                factor_tags=("weak_momentum",),
                confidence=0.92,
                risk_tier="tier_1",
                result_5d=-2.5,
            )
        )

    result = build_meta_learning_assessment(records)

    assert any(
        "lower_confidence_mapping" in item
        for item in result.recommended_weight_adjustments
    )
