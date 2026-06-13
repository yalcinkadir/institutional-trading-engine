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


def _neutral_factor(index: int) -> FactorWeightInput:
    return FactorWeightInput(
        factor=f"factor_{index}",
        current_weight=1.0,
        reliability_score=55,
        samples=25,
        expectancy=0.5,
        confidence=0.7,
    )


def _assert_exact_sum_for_factor_count(count: int) -> list[float]:
    result = build_dynamic_weighting_policy(
        [_neutral_factor(index) for index in range(count)],
        max_delta_per_update=0.0,
        max_weight=1.0,
    )
    weights = [item.new_weight for item in result.adjustments]

    assert result.total_weight == 1.0
    assert round(sum(weights), 4) == 1.0
    assert len(weights) == count
    return weights


def test_208_dynamic_weighting_sum_is_exact_after_rounding_remainder_for_3_factors():
    weights = _assert_exact_sum_for_factor_count(3)

    assert weights == [0.3333, 0.3333, 0.3334]


def test_208_dynamic_weighting_sum_is_exact_for_4_factors():
    weights = _assert_exact_sum_for_factor_count(4)

    assert weights == [0.25, 0.25, 0.25, 0.25]


def test_208_dynamic_weighting_sum_is_exact_after_rounding_remainder_for_6_factors():
    weights = _assert_exact_sum_for_factor_count(6)

    assert weights == [0.1667, 0.1667, 0.1667, 0.1667, 0.1667, 0.1665]


def test_208_dynamic_weighting_sum_is_exact_after_rounding_remainder_for_7_factors():
    weights = _assert_exact_sum_for_factor_count(7)

    assert weights == [0.1429, 0.1429, 0.1429, 0.1429, 0.1429, 0.1429, 0.1426]
