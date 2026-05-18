"""
Historical Regime Memory.

This layer stores and compares regime fingerprints. The purpose is not to claim
that history repeats perfectly. The purpose is to identify similar market
conditions and use them as contextual evidence.

A regime fingerprint may include breadth, volatility, liquidity, sector
rotation, cross-asset risk appetite and failure pressure.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import sqrt


@dataclass(frozen=True)
class RegimeFingerprint:
    label: str
    market_health_score: float
    breadth_score: float
    volatility_score: float
    liquidity_score: float
    cross_asset_risk_score: float
    sector_rotation_score: float
    failure_risk_score: float
    opportunity_density_score: float


@dataclass(frozen=True)
class RegimeAnalog:
    label: str
    similarity_score: float
    distance: float


@dataclass(frozen=True)
class HistoricalRegimeAssessment:
    closest_analogs: tuple[RegimeAnalog, ...]
    memory_state: str
    warnings: tuple[str, ...]
    confirmations: tuple[str, ...]


FEATURES = (
    "market_health_score",
    "breadth_score",
    "volatility_score",
    "liquidity_score",
    "cross_asset_risk_score",
    "sector_rotation_score",
    "failure_risk_score",
    "opportunity_density_score",
)


def _normalized_distance(current: RegimeFingerprint, historical: RegimeFingerprint) -> float:
    total = 0.0
    for feature in FEATURES:
        current_value = getattr(current, feature)
        historical_value = getattr(historical, feature)
        total += ((current_value - historical_value) / 100) ** 2
    return sqrt(total / len(FEATURES))


def find_historical_regime_analogs(
    current: RegimeFingerprint,
    history: list[RegimeFingerprint],
    *,
    top_n: int = 3,
) -> HistoricalRegimeAssessment:
    if not history:
        return HistoricalRegimeAssessment(
            closest_analogs=(),
            memory_state="insufficient_history",
            warnings=("no_historical_regime_memory_available",),
            confirmations=(),
        )

    analogs = []
    for item in history:
        distance = _normalized_distance(current, item)
        similarity = max(0.0, 1.0 - distance)
        analogs.append(
            RegimeAnalog(
                label=item.label,
                similarity_score=round(similarity, 4),
                distance=round(distance, 4),
            )
        )

    analogs = sorted(analogs, key=lambda analog: analog.similarity_score, reverse=True)[:top_n]

    warnings: list[str] = []
    confirmations: list[str] = []

    best = analogs[0]
    if best.similarity_score >= 0.85:
        memory_state = "strong_historical_analog"
        confirmations.append("high_similarity_regime_found")
    elif best.similarity_score >= 0.70:
        memory_state = "moderate_historical_analog"
        confirmations.append("usable_similarity_regime_found")
    else:
        memory_state = "weak_historical_analog"
        warnings.append("no_strong_historical_match")

    return HistoricalRegimeAssessment(
        closest_analogs=tuple(analogs),
        memory_state=memory_state,
        warnings=tuple(warnings),
        confirmations=tuple(confirmations),
    )
