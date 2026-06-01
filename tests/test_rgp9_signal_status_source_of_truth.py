from __future__ import annotations

from datetime import date

from src.signals.signal_status import (
    ACTIONABLE_SIGNAL_ACTIONS,
    OPEN_SIGNAL_STATUSES,
    REGIME_INVALIDATION_ELIGIBLE_STATUSES,
    TERMINAL_SIGNAL_STATUSES,
    RunnerStatus,
    SignalEventType,
    SignalStatus,
    is_open_signal_status,
    is_regime_invalidation_eligible_status,
    is_terminal_signal_status,
    normalize_signal_status,
)
from src.watchers import entry_exit_watcher
from src.watchers import regime_invalidation
from src.watchers.entry_exit_watcher import PriceBar, evaluate_signal_against_bar
from src.watchers.trailing_stop_manager import apply_target_1_runner_management


def _signal(**overrides):
    payload = {
        "symbol": "NVDA",
        "action": "BUY_WATCH",
        "status": SignalStatus.PENDING.value,
        "entry_trigger": 101.0,
        "stop_loss": 95.0,
        "target_1": 110.0,
        "target_2": 120.0,
        "valid_until": "2026-05-25",
        "generated_at": "2026-05-20T21:00:00Z",
        "signal_id": "rgp9-stable-id",
    }
    payload.update(overrides)
    return payload


def test_terminal_signal_statuses_are_single_source_of_truth() -> None:
    assert TERMINAL_SIGNAL_STATUSES == {
        SignalStatus.INVALIDATED_BEFORE_ENTRY.value,
        SignalStatus.STOP_HIT.value,
        SignalStatus.TARGET_2_HIT.value,
        SignalStatus.EXPIRED.value,
        SignalStatus.CANCELLED_BY_REGIME_CHANGE.value,
    }
    assert entry_exit_watcher.TERMINAL_STATUSES is TERMINAL_SIGNAL_STATUSES
    assert regime_invalidation.TERMINAL_STATUSES is TERMINAL_SIGNAL_STATUSES


def test_open_and_regime_eligible_statuses_are_single_source_of_truth() -> None:
    assert OPEN_SIGNAL_STATUSES == {
        SignalStatus.PENDING.value,
        SignalStatus.TRIGGERED.value,
        SignalStatus.TARGET_1_HIT.value,
    }
    assert REGIME_INVALIDATION_ELIGIBLE_STATUSES == OPEN_SIGNAL_STATUSES
    assert regime_invalidation.ELIGIBLE_STATUSES is REGIME_INVALIDATION_ELIGIBLE_STATUSES
    assert ACTIONABLE_SIGNAL_ACTIONS == {"BUY_WATCH"}


def test_status_helpers_normalize_and_classify_states() -> None:
    assert normalize_signal_status(None) == SignalStatus.PENDING.value
    assert normalize_signal_status(" triggered ") == SignalStatus.TRIGGERED.value
    assert is_open_signal_status("target_1_hit") is True
    assert is_regime_invalidation_eligible_status("pending") is True
    assert is_terminal_signal_status("stop_hit") is True
    assert is_terminal_signal_status("TARGET_1_HIT") is False


def test_watcher_uses_shared_event_and_status_values_for_transitions() -> None:
    bar = PriceBar(
        symbol="NVDA",
        timestamp="2026-05-21T15:00:00Z",
        high=102.0,
        low=100.0,
        close=101.5,
    )

    alert, update = evaluate_signal_against_bar(_signal(), bar, today=date(2026, 5, 21))

    assert alert is not None
    assert update is not None
    assert alert.alert_type == SignalEventType.ENTRY_TRIGGERED.value
    assert update.event_type == SignalEventType.ENTRY_TRIGGERED.value
    assert update.signal["status"] == SignalStatus.TRIGGERED.value


def test_terminal_status_from_shared_source_blocks_retrigger() -> None:
    bar = PriceBar(
        symbol="NVDA",
        timestamp="2026-05-22T15:00:00Z",
        high=130.0,
        low=120.0,
        close=125.0,
    )

    alert, update = evaluate_signal_against_bar(
        _signal(status=SignalStatus.CANCELLED_BY_REGIME_CHANGE.value),
        bar,
        today=date(2026, 5, 22),
    )

    assert alert is None
    assert update is None


def test_runner_management_uses_shared_partial_exit_and_runner_status_values() -> None:
    result = apply_target_1_runner_management(
        _signal(status=SignalStatus.TARGET_1_HIT.value, atr14=4.0),
        latest_high=110.5,
        atr=4.0,
    )

    assert result.event_type == SignalEventType.PARTIAL_EXIT_FILLED.value
    assert result.signal["runner_status"] == RunnerStatus.ACTIVE.value
