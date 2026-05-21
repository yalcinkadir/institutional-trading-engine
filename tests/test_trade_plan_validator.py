from __future__ import annotations

from src.signals.trade_plan_validator import validate_long_trade_plan


def test_valid_long_trade_plan_passes() -> None:
    result = validate_long_trade_plan(
        entry_trigger=100.0,
        stop_loss=96.0,
        target_1=108.0,
        target_2=114.0,
        atr=4.0,
    )

    assert result.is_valid
    assert result.reasons == []
    assert result.risk_per_share == 4.0
    assert result.reward_per_share == 8.0
    assert result.risk_reward == 2.0
    assert result.stop_distance_atr == 1.0


def test_missing_required_levels_fail() -> None:
    result = validate_long_trade_plan(
        entry_trigger=None,
        stop_loss=None,
        target_1=None,
    )

    assert not result.is_valid
    assert result.reasons == [
        "missing_entry_trigger",
        "missing_stop_loss",
        "missing_target_1",
    ]


def test_stop_must_be_below_entry_for_long_signal() -> None:
    result = validate_long_trade_plan(
        entry_trigger=100.0,
        stop_loss=101.0,
        target_1=108.0,
        atr=4.0,
    )

    assert not result.is_valid
    assert "stop_loss_not_below_entry" in result.reasons
    assert "invalid_risk_per_share" in result.reasons


def test_target_1_must_be_above_entry_for_long_signal() -> None:
    result = validate_long_trade_plan(
        entry_trigger=100.0,
        stop_loss=96.0,
        target_1=99.0,
        atr=4.0,
    )

    assert not result.is_valid
    assert "target_1_not_above_entry" in result.reasons
    assert "invalid_reward_per_share" in result.reasons


def test_target_2_must_be_above_target_1_when_present() -> None:
    result = validate_long_trade_plan(
        entry_trigger=100.0,
        stop_loss=96.0,
        target_1=108.0,
        target_2=107.0,
        atr=4.0,
    )

    assert not result.is_valid
    assert "target_2_not_above_target_1" in result.reasons


def test_low_risk_reward_fails() -> None:
    result = validate_long_trade_plan(
        entry_trigger=100.0,
        stop_loss=96.0,
        target_1=103.0,
        atr=4.0,
        min_risk_reward=1.2,
    )

    assert not result.is_valid
    assert result.risk_reward == 0.75
    assert "risk_reward_below_minimum" in result.reasons


def test_stop_distance_too_tight_fails_when_atr_available() -> None:
    result = validate_long_trade_plan(
        entry_trigger=100.0,
        stop_loss=99.5,
        target_1=108.0,
        atr=4.0,
        min_stop_atr=0.25,
    )

    assert not result.is_valid
    assert result.stop_distance_atr == 0.125
    assert "stop_distance_too_tight" in result.reasons


def test_stop_distance_too_wide_fails_when_atr_available() -> None:
    result = validate_long_trade_plan(
        entry_trigger=100.0,
        stop_loss=80.0,
        target_1=130.0,
        atr=4.0,
        max_stop_atr=4.0,
    )

    assert not result.is_valid
    assert result.stop_distance_atr == 5.0
    assert "stop_distance_too_wide" in result.reasons


def test_atr_validation_is_skipped_when_atr_missing() -> None:
    result = validate_long_trade_plan(
        entry_trigger=100.0,
        stop_loss=96.0,
        target_1=108.0,
        atr=None,
    )

    assert result.is_valid
    assert result.stop_distance_atr is None
