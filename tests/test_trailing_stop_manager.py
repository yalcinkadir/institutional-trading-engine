from __future__ import annotations

from src.watchers.trailing_stop_manager import apply_target_1_runner_management


def _signal() -> dict:
    return {
        "symbol": "NVDA",
        "signal_id": "sig_NVDA_test",
        "entry_trigger": 100.0,
        "stop_loss": 94.0,
        "target_1": 112.0,
        "target_2": 120.0,
    }


def test_target_1_runner_management_sets_partial_exit_and_breakeven() -> None:
    result = apply_target_1_runner_management(_signal())

    assert result.event_type == "PARTIAL_EXIT_FILLED"
    assert result.signal["partial_exit_completed"] is True
    assert result.signal["partial_exit_ratio"] == 0.5
    assert result.signal["runner_status"] == "active"
    assert result.signal["stop_loss"] == 100.0
    assert result.signal["trail_stop"] == 100.0
    assert result.signal["stop_adjustment_reason"] == "target_1_hit_breakeven_and_atr_trail"


def test_target_1_runner_management_applies_atr_trail_above_breakeven() -> None:
    result = apply_target_1_runner_management(
        _signal(),
        latest_high=115.0,
        atr=4.0,
    )

    assert result.signal["stop_loss"] == 109.0
    assert result.signal["trail_stop"] == 109.0


def test_target_1_runner_management_never_moves_stop_downward() -> None:
    signal = _signal()
    signal["stop_loss"] = 106.0
    signal["trail_stop"] = 106.0

    result = apply_target_1_runner_management(
        signal,
        latest_high=105.0,
        atr=4.0,
    )

    assert result.signal["stop_loss"] == 106.0
    assert result.signal["trail_stop"] == 106.0


def test_target_1_runner_management_does_not_duplicate_partial_exit() -> None:
    signal = _signal()
    signal["partial_exit_completed"] = True
    signal["runner_status"] = "active"
    signal["stop_loss"] = 100.0

    result = apply_target_1_runner_management(signal, latest_high=120.0, atr=4.0)

    assert result.event_type is None
    assert result.reasons == ["partial_exit_already_completed"]
    assert result.signal["stop_loss"] == 100.0


def test_target_1_runner_management_requires_entry() -> None:
    signal = _signal()
    signal.pop("entry_trigger")

    result = apply_target_1_runner_management(signal)

    assert result.event_type is None
    assert result.reasons == ["missing_entry_for_runner_management"]
