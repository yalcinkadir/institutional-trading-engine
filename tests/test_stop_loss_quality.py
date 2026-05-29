from __future__ import annotations

from src.signals.stop_loss_quality import derive_stop_loss_quality


def test_default_atr_stop_for_breakout() -> None:
    result = derive_stop_loss_quality(
        setup_type="momentum_breakout",
        entry_trigger=102.0,
        close=100.0,
        atr=4.0,
        entry_type="breakout",
    )

    assert result.is_valid
    assert result.stop_loss == 94.0
    assert result.stop_model == "atr_stop"
    assert "2 ATR below entry" in result.stop_reason


def test_valid_swing_low_structure_stop_is_preferred_over_atr() -> None:
    result = derive_stop_loss_quality(
        setup_type="momentum_breakout",
        entry_trigger=102.0,
        close=100.0,
        atr=4.0,
        entry_type="breakout",
        scanner_metrics={"swing_low_3bar": 96.0},
    )

    assert result.is_valid
    assert result.stop_loss == 95.81
    assert result.stop_model == "swing_low_structure_stop"
    assert "swing-low structure stop" in result.stop_reason


def test_missing_swing_low_falls_back_to_atr_stop() -> None:
    result = derive_stop_loss_quality(
        setup_type="momentum_breakout",
        entry_trigger=102.0,
        close=100.0,
        atr=4.0,
        entry_type="breakout",
        scanner_metrics={},
    )

    assert result.is_valid
    assert result.stop_loss == 94.0
    assert result.stop_model == "atr_stop"


def test_swing_low_above_entry_falls_back_to_atr_stop() -> None:
    result = derive_stop_loss_quality(
        setup_type="momentum_breakout",
        entry_trigger=102.0,
        close=100.0,
        atr=4.0,
        entry_type="breakout",
        scanner_metrics={"swing_low_3bar": 103.0},
    )

    assert result.is_valid
    assert result.stop_loss == 94.0
    assert result.stop_model == "atr_stop"


def test_too_wide_swing_low_falls_back_to_atr_stop() -> None:
    result = derive_stop_loss_quality(
        setup_type="momentum_breakout",
        entry_trigger=102.0,
        close=100.0,
        atr=4.0,
        entry_type="breakout",
        scanner_metrics={"swing_low_3bar": 80.0},
    )

    assert result.is_valid
    assert result.stop_loss == 94.0
    assert result.stop_model == "atr_stop"


def test_scanner_provided_stop_takes_precedence_over_swing_low() -> None:
    result = derive_stop_loss_quality(
        setup_type="momentum_breakout",
        entry_trigger=102.0,
        close=100.0,
        atr=4.0,
        entry_type="breakout",
        scanner_metrics={"stop_loss": 97.0, "swing_low_3bar": 96.0},
    )

    assert result.is_valid
    assert result.stop_loss == 97.0
    assert result.stop_model == "scanner_provided_stop"


def test_pullback_structure_stop() -> None:
    result = derive_stop_loss_quality(
        setup_type="pullback_continuation",
        entry_trigger=96.0,
        close=100.0,
        atr=4.0,
        entry_type="pullback",
    )

    assert result.is_valid
    assert result.stop_loss == 90.0
    assert result.stop_model == "pullback_structure_stop"
    assert "1.5 ATR below entry" in result.stop_reason


def test_pullback_structure_stop_rejects_non_positive_computed_stop() -> None:
    result = derive_stop_loss_quality(
        setup_type="pullback_continuation",
        entry_trigger=3.0,
        close=3.5,
        atr=2.0,
        entry_type="pullback",
    )

    assert not result.is_valid
    assert result.stop_loss is None
    assert result.stop_model == "pullback_structure_stop"
    assert result.reasons == ["computed_stop_non_positive"]


def test_retest_structure_stop() -> None:
    result = derive_stop_loss_quality(
        setup_type="retest_continuation",
        entry_trigger=98.0,
        close=100.0,
        atr=4.0,
        entry_type="retest",
    )

    assert result.is_valid
    assert result.stop_loss == 93.0
    assert result.stop_model == "retest_structure_stop"


def test_gap_fill_stop() -> None:
    result = derive_stop_loss_quality(
        setup_type="gap_fill",
        entry_trigger=97.0,
        close=100.0,
        atr=4.0,
        entry_type="gap_fill",
    )

    assert result.is_valid
    assert result.stop_loss == 91.0
    assert result.stop_model == "gap_fill_stop"


def test_scanner_provided_stop_is_used_when_valid() -> None:
    result = derive_stop_loss_quality(
        setup_type="momentum_breakout",
        entry_trigger=102.0,
        close=100.0,
        atr=4.0,
        entry_type="breakout",
        scanner_metrics={"stop_loss": 97.0},
    )

    assert result.is_valid
    assert result.stop_loss == 97.0
    assert result.stop_model == "scanner_provided_stop"
    assert result.stop_reason == "scanner provided stop below entry"


def test_scanner_stop_above_entry_is_rejected() -> None:
    result = derive_stop_loss_quality(
        setup_type="momentum_breakout",
        entry_trigger=102.0,
        close=100.0,
        atr=4.0,
        entry_type="breakout",
        scanner_metrics={"stop_loss": 103.0},
    )

    assert not result.is_valid
    assert result.stop_loss == 103.0
    assert result.stop_model == "scanner_provided_stop"
    assert result.reasons == ["scanner_stop_not_below_entry"]


def test_missing_entry_is_rejected() -> None:
    result = derive_stop_loss_quality(
        setup_type="momentum_breakout",
        entry_trigger=None,
        close=100.0,
        atr=4.0,
        entry_type="breakout",
    )

    assert not result.is_valid
    assert result.reasons == ["missing_entry_trigger"]


def test_non_positive_entry_is_rejected() -> None:
    result = derive_stop_loss_quality(
        setup_type="momentum_breakout",
        entry_trigger=0.0,
        close=100.0,
        atr=4.0,
        entry_type="breakout",
    )

    assert not result.is_valid
    assert result.reasons == ["invalid_entry_trigger"]


def test_missing_close_is_rejected() -> None:
    result = derive_stop_loss_quality(
        setup_type="momentum_breakout",
        entry_trigger=102.0,
        close=None,
        atr=4.0,
        entry_type="breakout",
    )

    assert not result.is_valid
    assert result.reasons == ["missing_close"]


def test_non_positive_close_is_rejected() -> None:
    result = derive_stop_loss_quality(
        setup_type="momentum_breakout",
        entry_trigger=102.0,
        close=0.0,
        atr=4.0,
        entry_type="breakout",
    )

    assert not result.is_valid
    assert result.reasons == ["missing_or_invalid_close"]


def test_missing_atr_is_rejected() -> None:
    result = derive_stop_loss_quality(
        setup_type="momentum_breakout",
        entry_trigger=102.0,
        close=100.0,
        atr=None,
        entry_type="breakout",
    )

    assert not result.is_valid
    assert result.reasons == ["missing_or_invalid_atr"]
