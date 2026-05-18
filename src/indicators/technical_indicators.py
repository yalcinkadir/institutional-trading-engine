from __future__ import annotations

from statistics import mean


def sma(values: list[float], period: int) -> float:
    if len(values) < period:
        raise ValueError(f"Not enough values for SMA{period}")

    return round(mean(values[-period:]), 2)


def calculate_atr(bars: list[dict], period: int = 14) -> float:
    if len(bars) < period + 1:
        raise ValueError("Not enough bars for ATR")

    true_ranges: list[float] = []

    for index in range(1, len(bars)):
        current = bars[index]
        previous = bars[index - 1]

        high = current["h"]
        low = current["l"]
        prev_close = previous["c"]

        tr = max(
            high - low,
            abs(high - prev_close),
            abs(low - prev_close),
        )

        true_ranges.append(tr)

    return round(mean(true_ranges[-period:]), 2)


def relative_volume(current_volume: float, average_volume: float) -> float:
    if average_volume <= 0:
        return 0.0

    return round(current_volume / average_volume, 2)
