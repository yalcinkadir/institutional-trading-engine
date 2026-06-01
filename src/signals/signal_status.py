"""Shared signal lifecycle status and event definitions.

RGP9 centralizes terminal/open signal-state semantics so watcher, regime
invalidation, runner-management and reporting paths cannot drift by keeping
parallel string sets.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Any


class SignalStatus(StrEnum):
    PENDING = "PENDING"
    TRIGGERED = "TRIGGERED"
    TARGET_1_HIT = "TARGET_1_HIT"
    INVALIDATED_BEFORE_ENTRY = "INVALIDATED_BEFORE_ENTRY"
    STOP_HIT = "STOP_HIT"
    TARGET_2_HIT = "TARGET_2_HIT"
    EXPIRED = "EXPIRED"
    CANCELLED_BY_REGIME_CHANGE = "CANCELLED_BY_REGIME_CHANGE"


class SignalEventType(StrEnum):
    ENTRY_TRIGGERED = "ENTRY_TRIGGERED"
    INVALIDATED_BEFORE_ENTRY = "INVALIDATED_BEFORE_ENTRY"
    STOP_HIT = "STOP_HIT"
    TARGET_1_HIT = "TARGET_1_HIT"
    TARGET_2_HIT = "TARGET_2_HIT"
    EXPIRED = "EXPIRED"
    REGIME_INVALIDATION_EXIT = "REGIME_INVALIDATION_EXIT"
    PARTIAL_EXIT_FILLED = "PARTIAL_EXIT_FILLED"


class RunnerStatus(StrEnum):
    INACTIVE = "inactive"
    ACTIVE = "active"


ACTIONABLE_SIGNAL_ACTIONS: frozenset[str] = frozenset({"BUY_WATCH"})
OPEN_SIGNAL_STATUSES: frozenset[str] = frozenset(
    {
        SignalStatus.PENDING.value,
        SignalStatus.TRIGGERED.value,
        SignalStatus.TARGET_1_HIT.value,
    }
)
TERMINAL_SIGNAL_STATUSES: frozenset[str] = frozenset(
    {
        SignalStatus.INVALIDATED_BEFORE_ENTRY.value,
        SignalStatus.STOP_HIT.value,
        SignalStatus.TARGET_2_HIT.value,
        SignalStatus.EXPIRED.value,
        SignalStatus.CANCELLED_BY_REGIME_CHANGE.value,
    }
)
REGIME_INVALIDATION_ELIGIBLE_STATUSES: frozenset[str] = OPEN_SIGNAL_STATUSES


def normalize_signal_status(value: Any, *, default: SignalStatus = SignalStatus.PENDING) -> str:
    """Return a normalized signal status string with a conservative default."""
    normalized = str(value or default.value).strip().upper()
    return normalized or default.value


def is_terminal_signal_status(value: Any) -> bool:
    """Return True when a signal status is terminal and must not re-open."""
    return normalize_signal_status(value) in TERMINAL_SIGNAL_STATUSES


def is_open_signal_status(value: Any) -> bool:
    """Return True when a signal may still receive lifecycle updates."""
    return normalize_signal_status(value) in OPEN_SIGNAL_STATUSES


def is_regime_invalidation_eligible_status(value: Any) -> bool:
    """Return True when a signal can be cancelled by a risk-off regime."""
    return normalize_signal_status(value) in REGIME_INVALIDATION_ELIGIBLE_STATUSES
