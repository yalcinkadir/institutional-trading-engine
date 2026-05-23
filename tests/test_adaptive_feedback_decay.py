import pytest

from src.feedback.adaptive_feedback_decay import (
    DECAY_HALF_LIFE_REGIME_SHIFT,
    DECAY_HALF_LIFE_STABLE,
    MIN_WEIGHT_FLOOR,
    FeedbackDecayConfig,
    apply_feedback_decay,
    calculate_decay_weight,
    calculate_weighted_performance,
    half_life_for_regime_state,
)


def test_stable_half_life_weights_30_and_60_day_observations() -> None:
    assert calculate_decay_weight(0) == 1.0
    assert calculate_decay_weight(30) == pytest.approx(0.5)
    assert calculate_decay_weight(60) == pytest.approx(0.25)


def test_newer_records_receive_higher_weights_than_older_records() -> None:
    records = [
        {"closed_at": "2026-01-31", "result_r": 1.0},
        {"closed_at": "2026-01-02", "result_r": 1.0},
    ]

    weighted = apply_feedback_decay(records, as_of="2026-02-01")

    assert weighted[0].weight > weighted[1].weight
    assert weighted[0].age_in_days == 1
    assert weighted[1].age_in_days == 30


def test_min_weight_floor_prevents_complete_forgetting() -> None:
    weight = calculate_decay_weight(3650)

    assert weight == MIN_WEIGHT_FLOOR


def test_regime_shift_uses_shorter_half_life_before_recovery() -> None:
    assert half_life_for_regime_state(regime_shift_active=False) == DECAY_HALF_LIFE_STABLE
    assert (
        half_life_for_regime_state(
            regime_shift_active=True,
            days_since_regime_shift=2,
        )
        == DECAY_HALF_LIFE_REGIME_SHIFT
    )


def test_regime_shift_returns_to_stable_half_life_after_recovery() -> None:
    assert (
        half_life_for_regime_state(
            regime_shift_active=True,
            days_since_regime_shift=5,
        )
        == DECAY_HALF_LIFE_STABLE
    )


def test_regime_shift_mode_downweights_old_records_faster() -> None:
    stable_weight = calculate_decay_weight(30, half_life_days=DECAY_HALF_LIFE_STABLE)
    shift_weight = calculate_decay_weight(30, half_life_days=DECAY_HALF_LIFE_REGIME_SHIFT)

    assert shift_weight < stable_weight


def test_weighted_performance_emphasizes_recent_results() -> None:
    records = [
        {"closed_at": "2026-01-31", "result_r": 1.0},
        {"closed_at": "2025-12-03", "result_r": -1.0},
    ]

    performance = calculate_weighted_performance(records, as_of="2026-02-01")

    assert performance.record_count == 2
    assert performance.total_weight > 0
    assert performance.adjusted_performance > 0


def test_invalid_half_life_raises_error() -> None:
    with pytest.raises(ValueError):
        calculate_decay_weight(10, half_life_days=0)


def test_custom_config_is_supported() -> None:
    config = FeedbackDecayConfig(stable_half_life_days=15, min_weight_floor=0.10)
    records = [{"closed_at": "2026-01-17", "result_r": 1.0}]

    weighted = apply_feedback_decay(records, as_of="2026-02-01", config=config)

    assert weighted[0].half_life_days == 15
    assert weighted[0].weight == pytest.approx(0.5)
