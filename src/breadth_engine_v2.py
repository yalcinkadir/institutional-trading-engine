"""
Breadth Engine v2.

Breadth v2 evaluates the internal quality of a market move. It is designed to
identify whether a rally is broad and healthy or narrow and fragile.

It evaluates:
- sector breadth
- new highs / new lows expansion
- equal-weight vs cap-weight participation
- mega-cap dependency
- breadth thrusts
- hidden weakness
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BreadthV2Input:
    percent_above_sma50: float
    percent_above_sma200: float
    sector_participation_percent: float
    new_highs: int
    new_lows: int
    equal_weight_return_20d: float
    cap_weight_return_20d: float
    mega_cap_contribution_percent: float
    previous_percent_above_sma50: float


@dataclass(frozen=True)
class BreadthV2Assessment:
    breadth_state: str
    breadth_score: int
    participation_quality: str
    warnings: tuple[str, ...]
    confirmations: tuple[str, ...]


def evaluate_breadth_v2(data: BreadthV2Input) -> BreadthV2Assessment:
    warnings: list[str] = []
    confirmations: list[str] = []
    score = 50

    breadth_delta = data.percent_above_sma50 - data.previous_percent_above_sma50
    equal_vs_cap = data.equal_weight_return_20d - data.cap_weight_return_20d

    if data.percent_above_sma50 >= 70:
        score += 15
        confirmations.append("strong_sma50_breadth")
    elif data.percent_above_sma50 <= 40:
        score -= 18
        warnings.append("weak_sma50_breadth")

    if data.percent_above_sma200 >= 65:
        score += 12
        confirmations.append("strong_long_term_breadth")
    elif data.percent_above_sma200 <= 35:
        score -= 16
        warnings.append("weak_long_term_breadth")

    if data.sector_participation_percent >= 70:
        score += 12
        confirmations.append("broad_sector_participation")
    elif data.sector_participation_percent <= 40:
        score -= 15
        warnings.append("narrow_sector_participation")

    if data.new_highs > data.new_lows * 2:
        score += 10
        confirmations.append("new_high_expansion")
    elif data.new_lows > data.new_highs:
        score -= 15
        warnings.append("new_low_expansion")

    if equal_vs_cap >= 0.02:
        score += 10
        confirmations.append("equal_weight_confirming")
    elif equal_vs_cap <= -0.02:
        score -= 15
        warnings.append("cap_weight_dependency")

    if data.mega_cap_contribution_percent >= 55:
        score -= 15
        warnings.append("mega_cap_dependency")
    elif data.mega_cap_contribution_percent <= 35:
        score += 8
        confirmations.append("healthy_non_mega_cap_participation")

    if breadth_delta >= 12:
        score += 15
        confirmations.append("breadth_thrust")
    elif breadth_delta <= -12:
        score -= 15
        warnings.append("breadth_deterioration_rate_high")

    score = max(0, min(100, score))

    if score >= 80:
        breadth_state = "breadth_thrust_or_broad_accumulation"
        participation_quality = "excellent"
    elif score >= 65:
        breadth_state = "healthy_breadth_confirmation"
        participation_quality = "strong"
    elif score >= 50:
        breadth_state = "mixed_breadth"
        participation_quality = "mixed"
    elif score >= 35:
        breadth_state = "fragile_narrow_breadth"
        participation_quality = "weak"
    else:
        breadth_state = "internal_market_deterioration"
        participation_quality = "poor"

    return BreadthV2Assessment(
        breadth_state=breadth_state,
        breadth_score=score,
        participation_quality=participation_quality,
        warnings=tuple(warnings),
        confirmations=tuple(confirmations),
    )
