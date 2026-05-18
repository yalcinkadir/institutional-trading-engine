"""
Adaptive Expectancy Layer.

This layer transforms raw outcome tracking into regime-aware setup quality.
The goal is not machine learning hype. The goal is practical adaptive weighting.

Questions answered:
- Which setup types currently work?
- Which regimes have positive expectancy?
- Which combinations are deteriorating?
- Should risk be expanded or reduced?
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass


@dataclass(frozen=True)
class ExpectancyProfile:
    key: str
    trades: int
    win_rate: float
    average_result: float
    expectancy: float
    confidence: float
    recommendation: str


@dataclass(frozen=True)
class AdaptiveExpectancyReport:
    setup_profiles: tuple[ExpectancyProfile, ...]
    regime_profiles: tuple[ExpectancyProfile, ...]
    combined_profiles: tuple[ExpectancyProfile, ...]
    strongest_edges: tuple[str, ...]
    weakest_edges: tuple[str, ...]


MIN_SAMPLE_SIZE = 5


def _safe_float(value: object) -> float | None:
    try:
        if value in {None, "", "None"}:
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def _profile(key: str, results: list[float]) -> ExpectancyProfile:
    wins = [value for value in results if value > 0]
    losses = [value for value in results if value <= 0]

    trades = len(results)
    win_rate = len(wins) / trades if trades else 0.0
    average_result = sum(results) / trades if trades else 0.0

    average_win = sum(wins) / len(wins) if wins else 0.0
    average_loss = sum(losses) / len(losses) if losses else 0.0

    expectancy = (win_rate * average_win) + ((1 - win_rate) * average_loss)
    confidence = min(1.0, trades / 20)

    if trades < MIN_SAMPLE_SIZE:
        recommendation = "insufficient_data"
    elif expectancy >= 3:
        recommendation = "increase_risk_selectively"
    elif expectancy >= 1:
        recommendation = "maintain_exposure"
    elif expectancy > -1:
        recommendation = "reduce_size"
    else:
        recommendation = "avoid_or_block"

    return ExpectancyProfile(
        key=key,
        trades=trades,
        win_rate=round(win_rate, 4),
        average_result=round(average_result, 4),
        expectancy=round(expectancy, 4),
        confidence=round(confidence, 4),
        recommendation=recommendation,
    )


def build_adaptive_expectancy_report(records: list[dict]) -> AdaptiveExpectancyReport:
    by_setup: dict[str, list[float]] = defaultdict(list)
    by_regime: dict[str, list[float]] = defaultdict(list)
    by_combination: dict[str, list[float]] = defaultdict(list)

    for record in records:
        result = _safe_float(record.get("result_5d"))
        if result is None:
            continue

        setup = str(record.get("setup_type", "unknown"))
        regime = str(record.get("market_state", "unknown"))
        combo = f"{regime}::{setup}"

        by_setup[setup].append(result)
        by_regime[regime].append(result)
        by_combination[combo].append(result)

    setup_profiles = tuple(
        sorted(
            (_profile(key, values) for key, values in by_setup.items()),
            key=lambda profile: profile.expectancy,
            reverse=True,
        )
    )

    regime_profiles = tuple(
        sorted(
            (_profile(key, values) for key, values in by_regime.items()),
            key=lambda profile: profile.expectancy,
            reverse=True,
        )
    )

    combined_profiles = tuple(
        sorted(
            (_profile(key, values) for key, values in by_combination.items()),
            key=lambda profile: profile.expectancy,
            reverse=True,
        )
    )

    strongest_edges = tuple(
        profile.key
        for profile in combined_profiles[:3]
        if profile.trades >= MIN_SAMPLE_SIZE
    )

    weakest_edges = tuple(
        profile.key
        for profile in combined_profiles[-3:]
        if profile.trades >= MIN_SAMPLE_SIZE
    )

    return AdaptiveExpectancyReport(
        setup_profiles=setup_profiles,
        regime_profiles=regime_profiles,
        combined_profiles=combined_profiles,
        strongest_edges=strongest_edges,
        weakest_edges=weakest_edges,
    )
