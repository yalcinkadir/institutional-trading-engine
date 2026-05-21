"""Trailing stop and partial-exit state management.

Pure helper functions for long-side runner management after TARGET_1_HIT.
No broker execution is performed here.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


DEFAULT_PARTIAL_EXIT_RATIO = 0.50
DEFAULT_ATR_TRAIL_MULTIPLIER = 1.5


@dataclass(frozen=True)
class TrailingStopResult:
    signal: dict[str, Any]
    event_type: str | None
    reasons: list[str] = field(default_factory=list)


def _safe_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _round_price(value: float) -> float:
    return round(value, 2)


def apply_target_1_runner_management(
    signal: dict[str, Any],
    *,
    latest_high: float | None = None,
    atr: float | None = None,
    partial_exit_ratio: float = DEFAULT_PARTIAL_EXIT_RATIO,
    atr_trail_multiplier: float = DEFAULT_ATR_TRAIL_MULTIPLIER,
) -> TrailingStopResult:
    """Apply deterministic long-side runner management after TARGET_1_HIT.

    Behavior:
    - marks partial exit as completed once
    - moves stop to at least breakeven
    - activates runner state
    - optionally moves trail stop upward using latest_high - multiplier * ATR
    - never moves stop/trail downward
    """
    updated = dict(signal)

    if updated.get("partial_exit_completed") is True:
        return TrailingStopResult(
            signal=updated,
            event_type=None,
            reasons=["partial_exit_already_completed"],
        )

    entry = _safe_float(updated.get("entry_trigger") or updated.get("entry_price"))
    current_stop = _safe_float(updated.get("stop_loss"))
    current_trail = _safe_float(updated.get("trail_stop"))

    if entry is None:
        return TrailingStopResult(
            signal=updated,
            event_type=None,
            reasons=["missing_entry_for_runner_management"],
        )

    base_stop = current_stop if current_stop is not None else entry
    breakeven_stop = max(base_stop, entry)

    trail_candidate = breakeven_stop
    if latest_high is not None and atr is not None and atr > 0:
        trail_candidate = max(trail_candidate, latest_high - atr_trail_multiplier * atr)

    previous_runner_stop = current_trail if current_trail is not None else breakeven_stop
    runner_stop = max(previous_runner_stop, trail_candidate, breakeven_stop)
    runner_stop = _round_price(runner_stop)

    updated["partial_exit_completed"] = True
    updated["partial_exit_ratio"] = partial_exit_ratio
    updated["runner_status"] = "active"
    updated["stop_loss"] = runner_stop
    updated["trail_stop"] = runner_stop
    updated["stop_adjustment_reason"] = "target_1_hit_breakeven_and_atr_trail"

    return TrailingStopResult(
        signal=updated,
        event_type="PARTIAL_EXIT_FILLED",
        reasons=["target_1_hit_runner_activated"],
    )
