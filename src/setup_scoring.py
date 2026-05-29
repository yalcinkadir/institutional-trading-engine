"""
Live setup scoring for Decision Engine v3.

This module converts market bars into deterministic setup-quality inputs for
Decision Engine. It is intentionally simple and explainable:

- trend quality from SMA50/SMA200 structure
- relative strength versus a benchmark
- volume confirmation
- asymmetry from distance to invalidation versus recent range potential
- data confidence from data completeness
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from statistics import mean
from typing import Any

from src.indicators.technical_indicators import calculate_atr, relative_volume, sma

CONSERVATIVE_MISSING_TREND_QUALITY = 0.0
CONSERVATIVE_MISSING_ASYMMETRY = 0.0
MIN_LONG_HORIZON_BARS = 200


@dataclass(frozen=True)
class SetupScore:
    symbol: str
    setup_score: float
    regime_alignment: float
    asymmetry_score: float
    data_confidence: float
    relative_strength_20d: float
    relative_volume: float
    trend_quality: float
    notes: tuple[str, ...]


def _clamp(value: float, minimum: float = 0.0, maximum: float = 1.0) -> float:
    return max(minimum, min(maximum, value))


def _safe_float(value: Any) -> float | None:
    try:
        result = float(value)
    except (TypeError, ValueError):
        return None
    return result if math.isfinite(result) else None


def _close_series(bars: list[dict]) -> list[float]:
    closes: list[float] = []
    for bar in bars:
        value = _safe_float(bar.get("c"))
        if value is not None:
            closes.append(value)
    return closes


def _volume_series(bars: list[dict]) -> list[float]:
    volumes: list[float] = []
    for bar in bars:
        value = _safe_float(bar.get("v", 0))
        volumes.append(value if value is not None else 0.0)
    return volumes


def _percent_change(values: list[float], lookback: int) -> float:
    if len(values) <= lookback or values[-lookback - 1] == 0:
        return 0.0
    return (values[-1] / values[-lookback - 1]) - 1


def calculate_relative_strength(asset_bars: list[dict], benchmark_bars: list[dict], lookback: int = 20) -> float:
    asset_return = _percent_change(_close_series(asset_bars), lookback)
    benchmark_return = _percent_change(_close_series(benchmark_bars), lookback)
    return round(asset_return - benchmark_return, 4)


def calculate_trend_quality(bars: list[dict]) -> float:
    closes = _close_series(bars)
    close = closes[-1]
    sma50 = sma(closes, 50)
    sma200 = sma(closes, 200)

    score = 0.0
    if close > sma50:
        score += 0.40
    if close > sma200:
        score += 0.35
    if sma50 > sma200:
        score += 0.25

    return round(_clamp(score), 4)


def calculate_asymmetry_score(bars: list[dict]) -> float:
    closes = _close_series(bars)
    close = closes[-1]
    sma50 = sma(closes, 50)
    atr14 = calculate_atr(bars, 14)

    if atr14 <= 0:
        return 0.0

    downside_to_sma50 = max(abs(close - sma50), atr14)
    recent_20_high = max(closes[-20:])
    upside_to_recent_high = max(recent_20_high - close, atr14)
    reward_risk = upside_to_recent_high / downside_to_sma50

    # 0.5 R/R is weak, 2.0+ is strong.
    normalized = (reward_risk - 0.5) / 1.5
    return round(_clamp(normalized), 4)


def calculate_data_confidence(asset_bars: list[dict], benchmark_bars: list[dict]) -> float:
    asset_len = len(asset_bars)
    benchmark_len = len(benchmark_bars)
    completeness = min(asset_len, benchmark_len) / 260
    has_required_history = 1.0 if min(asset_len, benchmark_len) >= 220 else 0.6
    return round(_clamp((completeness * 0.7) + (has_required_history * 0.3)), 4)


def score_setup(symbol: str, asset_bars: list[dict], benchmark_bars: list[dict]) -> SetupScore:
    if len(asset_bars) < 60 or len(benchmark_bars) < 60:
        return SetupScore(
            symbol=symbol,
            setup_score=0.0,
            regime_alignment=0.0,
            asymmetry_score=0.0,
            data_confidence=0.0,
            relative_strength_20d=0.0,
            relative_volume=0.0,
            trend_quality=0.0,
            notes=("insufficient_history",),
        )

    closes = _close_series(asset_bars)
    volumes = _volume_series(asset_bars)
    notes: list[str] = []

    if len(closes) < len(asset_bars):
        notes.append("missing_or_invalid_close_data")
    if len(closes) < 60:
        return SetupScore(
            symbol=symbol,
            setup_score=0.0,
            regime_alignment=0.0,
            asymmetry_score=0.0,
            data_confidence=0.0,
            relative_strength_20d=0.0,
            relative_volume=0.0,
            trend_quality=0.0,
            notes=tuple(notes + ["insufficient_valid_close_history"]),
        )

    has_long_horizon = len(asset_bars) >= MIN_LONG_HORIZON_BARS and len(closes) >= MIN_LONG_HORIZON_BARS
    if has_long_horizon:
        trend_quality = calculate_trend_quality(asset_bars)
        asymmetry = calculate_asymmetry_score(asset_bars)
    else:
        trend_quality = CONSERVATIVE_MISSING_TREND_QUALITY
        asymmetry = CONSERVATIVE_MISSING_ASYMMETRY
        notes.append("conservative_missing_long_horizon_trend")
        notes.append("conservative_missing_long_horizon_asymmetry")

    rs_20d = calculate_relative_strength(asset_bars, benchmark_bars, 20)
    rs_score = _clamp((rs_20d + 0.05) / 0.10)

    avg_volume_20 = mean(volumes[-20:]) if len(volumes) >= 20 else 0
    rv = relative_volume(volumes[-1], avg_volume_20) if volumes else 0.0
    rv_score = _clamp(rv / 1.5)

    data_confidence = calculate_data_confidence(asset_bars, benchmark_bars)
    if not has_long_horizon:
        data_confidence = round(min(data_confidence, 0.5), 4)

    setup_score = round(
        (
            trend_quality * 40
            + rs_score * 25
            + rv_score * 15
            + asymmetry * 20
        ),
        2,
    )

    if trend_quality >= 0.75:
        notes.append("strong_trend_structure")
    if rs_20d > 0:
        notes.append("outperforming_benchmark_20d")
    if rv >= 1.2:
        notes.append("volume_confirmation")
    if asymmetry < 0.4:
        notes.append("weak_asymmetry")

    return SetupScore(
        symbol=symbol,
        setup_score=setup_score,
        regime_alignment=round(_clamp((trend_quality + rs_score) / 2), 4),
        asymmetry_score=asymmetry,
        data_confidence=data_confidence,
        relative_strength_20d=rs_20d,
        relative_volume=rv,
        trend_quality=trend_quality,
        notes=tuple(notes),
    )
