"""Market-structure level helpers for signal quality engines."""

from __future__ import annotations

from typing import Any, Sequence


def _safe_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def latest_confirmed_swing_low_3bar(lows: Sequence[Any]) -> float | None:
    """Return the latest confirmed 3-bar pivot low.

    A 3-bar swing low is the middle low in a three-bar window where:

    previous_low > pivot_low < next_low

    The latest bar cannot confirm itself, so the helper only returns pivots that
    have a following bar.
    """
    if len(lows) < 3:
        return None

    pivot_low: float | None = None
    for idx in range(1, len(lows) - 1):
        left = _safe_float(lows[idx - 1])
        middle = _safe_float(lows[idx])
        right = _safe_float(lows[idx + 1])
        if left is None or middle is None or right is None:
            continue
        if middle < left and middle < right:
            pivot_low = middle

    return pivot_low
