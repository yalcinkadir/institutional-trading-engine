"""
Multi-Timeframe Structure Engine.

Institutional-quality decisions should not rely on a single timeframe.
This module evaluates whether weekly, daily and intraday-like structure are
aligned, extended or deteriorating.

The engine stays deterministic and explainable:
- weekly trend controls structural bias
- daily trend controls setup quality
- short-term structure controls timing risk
- extension and failure pressure reduce confidence
"""

from __future__ import annotations

from dataclasses import dataclass
from statistics import mean


@dataclass(frozen=True)
class TimeframeStructureInput:
    timeframe: str
    close: float
    sma20: float
    sma50: float
    sma200: float
    return_20: float
    atr_percent: float
    failed_breakout: bool = False


@dataclass(frozen=True)
class MultiTimeframeAssessment:
    structure: str
    alignment_score: int
    timing_quality: str
    warnings: tuple[str, ...]
    confirmations: tuple[str, ...]


def _trend_score(frame: TimeframeStructureInput) -> float:
    score = 0.0
    if frame.close > frame.sma20:
        score += 0.25
    if frame.close > frame.sma50:
        score += 0.35
    if frame.close > frame.sma200:
        score += 0.25
    if frame.sma50 > frame.sma200:
        score += 0.15
    return score


def _is_extended(frame: TimeframeStructureInput) -> bool:
    if frame.atr_percent <= 0:
        return False
    distance_from_sma20 = abs(frame.close - frame.sma20) / frame.close
    return distance_from_sma20 > frame.atr_percent * 2.5


def evaluate_multi_timeframe_structure(
    *,
    weekly: TimeframeStructureInput,
    daily: TimeframeStructureInput,
    short_term: TimeframeStructureInput,
) -> MultiTimeframeAssessment:
    warnings: list[str] = []
    confirmations: list[str] = []

    weekly_score = _trend_score(weekly)
    daily_score = _trend_score(daily)
    short_score = _trend_score(short_term)

    alignment = round((weekly_score * 0.45 + daily_score * 0.40 + short_score * 0.15) * 100)

    if weekly_score >= 0.75:
        confirmations.append("weekly_trend_supportive")
    elif weekly_score <= 0.35:
        warnings.append("weekly_structure_weak")

    if daily_score >= 0.75:
        confirmations.append("daily_trend_supportive")
    elif daily_score <= 0.35:
        warnings.append("daily_structure_weak")

    if short_score >= 0.65:
        confirmations.append("short_term_timing_supportive")
    elif short_score <= 0.35:
        warnings.append("short_term_timing_weak")

    if any(frame.failed_breakout for frame in (weekly, daily, short_term)):
        alignment -= 15
        warnings.append("failed_breakout_pressure")

    if _is_extended(daily):
        alignment -= 10
        warnings.append("daily_extension_risk")

    if _is_extended(weekly):
        alignment -= 10
        warnings.append("weekly_extension_risk")

    alignment = max(0, min(100, alignment))

    if alignment >= 80:
        structure = "full_alignment"
        timing_quality = "high"
    elif alignment >= 65:
        structure = "constructive_alignment"
        timing_quality = "medium"
    elif alignment >= 45:
        structure = "mixed_structure"
        timing_quality = "low"
    else:
        structure = "structure_deterioration"
        timing_quality = "avoid"

    return MultiTimeframeAssessment(
        structure=structure,
        alignment_score=alignment,
        timing_quality=timing_quality,
        warnings=tuple(warnings),
        confirmations=tuple(confirmations),
    )
