"""
Sector Rotation Engine.

Institutional capital rotates between sectors before the broad market structure
fully changes.

This engine identifies:
- offensive leadership
- defensive leadership
- narrow participation
- broad participation
- sector deterioration
- rotation pressure

The goal is understanding where institutional money is flowing.
"""

from __future__ import annotations

from dataclasses import dataclass


OFFENSIVE_SECTORS = {
    "XLK",
    "XLY",
    "SMH",
    "SOXX",
    "QQQ",
    "IWM",
}

DEFENSIVE_SECTORS = {
    "XLU",
    "XLP",
    "XLV",
}


@dataclass(frozen=True)
class SectorPerformance:
    symbol: str
    relative_strength_20d: float
    trend_score: float
    above_sma50: bool
    above_sma200: bool


@dataclass(frozen=True)
class SectorRotationAssessment:
    rotation_state: str
    offensive_score: int
    defensive_score: int
    participation_quality: str
    leaders: tuple[str, ...]
    laggards: tuple[str, ...]
    warnings: tuple[str, ...]
    confirmations: tuple[str, ...]


def evaluate_sector_rotation(
    sectors: list[SectorPerformance],
) -> SectorRotationAssessment:
    warnings: list[str] = []
    confirmations: list[str] = []

    offensive_score = 0
    defensive_score = 0

    leaders: list[str] = []
    laggards: list[str] = []

    broad_participation_count = 0

    for sector in sectors:
        strong = (
            sector.relative_strength_20d > 0
            and sector.trend_score >= 0.65
            and sector.above_sma50
            and sector.above_sma200
        )

        weak = (
            sector.relative_strength_20d < 0
            and sector.trend_score <= 0.45
        )

        if strong:
            leaders.append(sector.symbol)
            broad_participation_count += 1

            if sector.symbol in OFFENSIVE_SECTORS:
                offensive_score += 15

            if sector.symbol in DEFENSIVE_SECTORS:
                defensive_score += 12

        if weak:
            laggards.append(sector.symbol)

            if sector.symbol in OFFENSIVE_SECTORS:
                offensive_score -= 10

            if sector.symbol in DEFENSIVE_SECTORS:
                defensive_score -= 8

    offensive_score = max(0, min(100, offensive_score))
    defensive_score = max(0, min(100, defensive_score))

    if broad_participation_count >= 6:
        participation_quality = "broad_participation"
        confirmations.append("healthy_market_participation")
    elif broad_participation_count >= 3:
        participation_quality = "mixed_participation"
    else:
        participation_quality = "narrow_participation"
        warnings.append("narrow_market_leadership")

    if offensive_score >= 45 and defensive_score <= 20:
        rotation_state = "risk_on_offensive_leadership"
        confirmations.append("growth_and_semiconductor_leadership")

    elif defensive_score >= 35 and offensive_score <= 20:
        rotation_state = "defensive_rotation"
        warnings.append("capital_rotating_to_defense")

    elif offensive_score >= 30 and defensive_score >= 30:
        rotation_state = "mixed_rotation_transition"
        warnings.append("rotation_conflict")

    else:
        rotation_state = "unclear_rotation_environment"
        warnings.append("weak_sector_alignment")

    if "SMH" in laggards or "SOXX" in laggards:
        warnings.append("semiconductor_leadership_breakdown")

    if "XLK" in leaders and "SMH" in leaders:
        confirmations.append("technology_and_ai_leadership_confirmed")

    return SectorRotationAssessment(
        rotation_state=rotation_state,
        offensive_score=offensive_score,
        defensive_score=defensive_score,
        participation_quality=participation_quality,
        leaders=tuple(sorted(leaders)),
        laggards=tuple(sorted(laggards)),
        warnings=tuple(warnings),
        confirmations=tuple(confirmations),
    )
