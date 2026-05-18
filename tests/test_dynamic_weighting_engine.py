from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.dynamic_weighting_engine import (  # noqa: E402
    FactorWeightInput,
    build_dynamic_weighting_policy,
)


def test_dynamic_weighting_increases_and_decreases_weights_based_on_outcomes():
    result = build_dynamic_weighting_policy(
        [
            FactorWeightInput(
                factor="breadth_confirmation",
                current_weight=0.20,
                reliability_score=82,
                samples=25,
                expectancy=2.5,
                confidence=0.8,
            ),
            FactorWeightInput(
                factor="extended_entry",
                current_weight=0.20,
                reliability_score=28,
                samples=25,
                expectancy=-2.0,
                confidence=0.7,
            ),
        ]
    )

    by_factor = {item.factor: item for item in result.adjustments}

    assert by_factor["breadth_confirmation"].action in {
        "increase_weight",
        "slightly_increase_weight",
    }

    assert by_factor["extended_entry"].action in {
        "decrease_weight",
        "slightly_decrease_weight",
    }


def test_dynamic_weighting_warns_on_insufficient_samples():
    result = build_dynamic_weighting_policy(
        [
            FactorWeightInput(
                factor="new_factor",
                current_weight=0.10,
                reliability_score=90,
                samples=3,
                expectancy=4.0,
                confidence=0.9,
            )
        ]
    )

    assert any("insufficient_samples" in item for item in result.warnings)
