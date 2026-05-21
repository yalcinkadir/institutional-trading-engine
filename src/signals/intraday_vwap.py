"""Intraday VWAP helpers for entry-quality context."""

from __future__ import annotations

from typing import Any, Iterable


def _safe_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _bar_value(bar: dict[str, Any], *keys: str) -> float | None:
    for key in keys:
        if key in bar:
            value = _safe_float(bar.get(key))
            if value is not None:
                return value
    return None


def calculate_intraday_vwap(bars: Iterable[dict[str, Any]]) -> float | None:
    """Calculate VWAP from intraday bars.

    Formula:

    typical_price = (high + low + close) / 3
    vwap = sum(typical_price * volume) / sum(volume)

    Supports both normalized keys (`high`, `low`, `close`, `volume`) and
    Polygon aggregate keys (`h`, `l`, `c`, `v`). Invalid bars are ignored.
    """
    numerator = 0.0
    denominator = 0.0

    for bar in bars:
        if not isinstance(bar, dict):
            continue

        high = _bar_value(bar, "high", "h")
        low = _bar_value(bar, "low", "l")
        close = _bar_value(bar, "close", "c")
        volume = _bar_value(bar, "volume", "v")

        if high is None or low is None or close is None or volume is None:
            continue
        if volume <= 0:
            continue

        typical_price = (high + low + close) / 3
        numerator += typical_price * volume
        denominator += volume

    if denominator <= 0:
        return None

    return round(numerator / denominator, 4)


def enrich_metrics_with_vwap(
    metrics: dict[str, Any] | None,
    intraday_bars: Iterable[dict[str, Any]] | None,
) -> dict[str, Any] | None:
    """Return metrics enriched with VWAP when intraday bars are usable."""
    if metrics is None:
        return None

    enriched = dict(metrics)
    if intraday_bars is None:
        return enriched

    vwap = calculate_intraday_vwap(intraday_bars)
    if vwap is not None:
        enriched["vwap"] = vwap
    return enriched
