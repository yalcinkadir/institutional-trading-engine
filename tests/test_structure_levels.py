from __future__ import annotations

from src.signals.structure_levels import latest_confirmed_swing_low_3bar


def test_latest_confirmed_swing_low_3bar_returns_latest_pivot() -> None:
    lows = [105.0, 101.0, 104.0, 103.0, 98.0, 102.0]

    assert latest_confirmed_swing_low_3bar(lows) == 98.0


def test_latest_confirmed_swing_low_3bar_requires_three_bars() -> None:
    assert latest_confirmed_swing_low_3bar([100.0, 99.0]) is None


def test_latest_confirmed_swing_low_3bar_ignores_missing_values() -> None:
    lows = [105.0, None, 104.0, 103.0, 98.0, 102.0]

    assert latest_confirmed_swing_low_3bar(lows) == 98.0


def test_latest_confirmed_swing_low_3bar_returns_none_without_pivot() -> None:
    lows = [105.0, 104.0, 103.0, 102.0]

    assert latest_confirmed_swing_low_3bar(lows) is None
