import pytest

from src.validation.statistical_robustness import (
    bootstrap_confidence_interval,
    calculate_kurtosis,
    calculate_skewness,
    calculate_statistical_robustness,
    deflated_sharpe_probability,
)


def test_deflated_sharpe_probability_penalizes_multiple_trials() -> None:
    single_trial = deflated_sharpe_probability(
        observed_sharpe=2.0,
        n_trials=1,
        n_observations=100,
    )
    many_trials = deflated_sharpe_probability(
        observed_sharpe=2.0,
        n_trials=100,
        n_observations=100,
    )

    assert single_trial > many_trials
    assert 0.0 <= many_trials <= 1.0


def test_deflated_sharpe_probability_returns_zero_for_tiny_sample() -> None:
    assert deflated_sharpe_probability(
        observed_sharpe=2.0,
        n_trials=10,
        n_observations=1,
    ) == 0.0


def test_bootstrap_confidence_interval_is_deterministic() -> None:
    values = [1.0, 1.0, 1.0, -0.5, -0.5]

    first = bootstrap_confidence_interval(
        values,
        metric="expectancy_r",
        reducer=lambda sample: sum(sample) / len(sample),
        iterations=200,
        seed=42,
    )
    second = bootstrap_confidence_interval(
        values,
        metric="expectancy_r",
        reducer=lambda sample: sum(sample) / len(sample),
        iterations=200,
        seed=42,
    )

    assert first == second
    assert first.lower <= first.upper
    assert first.metric == "expectancy_r"


def test_bootstrap_confidence_interval_handles_empty_values() -> None:
    interval = bootstrap_confidence_interval(
        [],
        metric="expectancy_r",
        reducer=lambda sample: sum(sample) / len(sample),
    )

    assert interval.lower == 0.0
    assert interval.upper == 0.0


def test_skewness_and_kurtosis_are_safe_for_small_or_constant_samples() -> None:
    assert calculate_skewness([1.0, 1.0]) == 0.0
    assert calculate_kurtosis([1.0, 1.0, 1.0]) == 3.0
    assert calculate_skewness([1.0, 1.0, 1.0]) == 0.0
    assert calculate_kurtosis([1.0, 1.0, 1.0, 1.0]) == 3.0


def test_calculate_statistical_robustness_returns_expected_fields() -> None:
    values = [1.0] * 20 + [-0.5] * 5

    robustness = calculate_statistical_robustness(
        values,
        observed_sharpe=2.0,
        estimated_trials=10,
        bootstrap_iterations=200,
        seed=11,
    )

    assert robustness.observations == 25
    assert robustness.estimated_trials == 10
    assert 0.0 <= robustness.deflated_sharpe_probability <= 1.0
    assert robustness.expectancy_ci.lower <= robustness.expectancy_ci.upper
    assert robustness.win_rate_ci.lower <= robustness.win_rate_ci.upper
    assert robustness.to_dict()["expectancy_ci"]["metric"] == "expectancy_r"
