from __future__ import annotations

from src.signals.exit_target_quality import derive_exit_target_quality


def test_momentum_targets_are_risk_based() -> None:
    result = derive_exit_target_quality(
        setup_type="momentum_breakout",
        entry_trigger=102.0,
        stop_loss=94.0,
        atr=4.0,
    )

    assert result.is_valid
    assert result.target_1 == 114.0
    assert result.target_2 == 122.0
    assert result.exit_model == "momentum_targets"
    assert "1.5R" in result.exit_reason


def test_pullback_targets_are_risk_based() -> None:
    result = derive_exit_target_quality(
        setup_type="pullback_continuation",
        entry_trigger=96.0,
        stop_loss=90.0,
        atr=4.0,
    )

    assert result.is_valid
    assert result.target_1 == 104.1
    assert result.target_2 == 109.5
    assert result.exit_model == "pullback_targets"


def test_retest_targets_are_risk_based() -> None:
    result = derive_exit_target_quality(
        setup_type="retest_continuation",
        entry_trigger=98.0,
        stop_loss=93.0,
        atr=4.0,
    )

    assert result.is_valid
    assert result.target_1 == 105.0
    assert result.target_2 == 109.5
    assert result.exit_model == "retest_targets"


def test_gap_fill_targets_are_risk_based() -> None:
    result = derive_exit_target_quality(
        setup_type="gap_fill",
        entry_trigger=97.0,
        stop_loss=91.0,
        atr=4.0,
    )

    assert result.is_valid
    assert result.target_1 == 105.1
    assert result.target_2 == 109.0
    assert result.exit_model == "gap_fill_targets"


def test_scanner_provided_targets_are_used_when_valid() -> None:
    result = derive_exit_target_quality(
        setup_type="momentum_breakout",
        entry_trigger=102.0,
        stop_loss=94.0,
        atr=4.0,
        scanner_metrics={"exit_1": 116.0, "exit_2": 124.0},
    )

    assert result.is_valid
    assert result.target_1 == 116.0
    assert result.target_2 == 124.0
    assert result.exit_model == "scanner_provided_targets"


def test_target_1_below_entry_is_rejected() -> None:
    result = derive_exit_target_quality(
        setup_type="momentum_breakout",
        entry_trigger=102.0,
        stop_loss=94.0,
        atr=4.0,
        scanner_metrics={"exit_1": 101.0},
    )

    assert not result.is_valid
    assert result.reasons == ["target_1_not_above_entry"]


def test_target_2_below_target_1_is_rejected() -> None:
    result = derive_exit_target_quality(
        setup_type="momentum_breakout",
        entry_trigger=102.0,
        stop_loss=94.0,
        atr=4.0,
        scanner_metrics={"exit_1": 116.0, "exit_2": 115.0},
    )

    assert not result.is_valid
    assert result.reasons == ["target_2_not_above_target_1"]


def test_missing_entry_is_rejected() -> None:
    result = derive_exit_target_quality(
        setup_type="momentum_breakout",
        entry_trigger=None,
        stop_loss=94.0,
        atr=4.0,
    )

    assert not result.is_valid
    assert result.reasons == ["missing_entry_trigger"]


def test_missing_stop_is_rejected() -> None:
    result = derive_exit_target_quality(
        setup_type="momentum_breakout",
        entry_trigger=102.0,
        stop_loss=None,
        atr=4.0,
    )

    assert not result.is_valid
    assert result.reasons == ["missing_stop_loss"]


def test_stop_above_entry_is_rejected() -> None:
    result = derive_exit_target_quality(
        setup_type="momentum_breakout",
        entry_trigger=102.0,
        stop_loss=103.0,
        atr=4.0,
    )

    assert not result.is_valid
    assert result.reasons == ["stop_loss_not_below_entry"]
