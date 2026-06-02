from __future__ import annotations

from src.signals.stop_loss_quality import (
    MAX_ATR_STOP_DISTANCE,
    derive_stop_loss_quality,
)


def test_er14_short_side_is_explicitly_rejected_until_supported() -> None:
    result = derive_stop_loss_quality(
        setup_type="momentum_breakout",
        entry_trigger=102.0,
        close=100.0,
        atr=4.0,
        entry_type="breakout",
        side="short",
    )

    assert not result.is_valid
    assert result.stop_loss is None
    assert result.stop_model == "unsupported_side"
    assert result.reasons == ["unsupported_side:short"]


def test_er15_scanner_stop_farther_than_max_atr_distance_is_rejected() -> None:
    result = derive_stop_loss_quality(
        setup_type="momentum_breakout",
        entry_trigger=102.0,
        close=100.0,
        atr=4.0,
        entry_type="breakout",
        scanner_metrics={"stop_loss": 80.0},
    )

    assert not result.is_valid
    assert result.stop_loss == 80.0
    assert result.stop_model == "scanner_provided_stop"
    assert result.reasons == ["stop_distance_exceeds_max_atr"]


def test_er15_atr_fallback_stop_declares_and_respects_max_distance_cap() -> None:
    result = derive_stop_loss_quality(
        setup_type="momentum_breakout",
        entry_trigger=102.0,
        close=100.0,
        atr=4.0,
        entry_type="breakout",
    )

    assert result.is_valid
    assert result.stop_model == "atr_stop"
    assert (102.0 - result.stop_loss) / 4.0 <= MAX_ATR_STOP_DISTANCE
    assert "max 2.0 ATR" in result.stop_reason
