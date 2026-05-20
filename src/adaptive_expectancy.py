"""
Adaptive Expectancy Layer.

This layer transforms raw outcome tracking into regime-aware setup quality.
The goal is not machine learning hype. The goal is practical adaptive weighting.

Questions answered:
- Which setup types currently work?
- Which regimes have positive expectancy?
- Which entry types work best?
- Which setup/regime/entry combinations are deteriorating?
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
    entry_type_profiles: tuple[ExpectancyProfile, ...]
    combined_profiles: tuple[ExpectancyProfile, ...]
    setup_regime_entry_profiles: tuple[ExpectancyProfile, ...]
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


def _sorted_profiles(groups: dict[str, list[float]]) -> tuple[ExpectancyProfile, ...]:
    return tuple(
        sorted(
            (_profile(key, values) for key, values in groups.items()),
            key=lambda profile: profile.expectancy,
            reverse=True,
        )
    )


def _qualified_profile_keys(
    profiles: tuple[ExpectancyProfile, ...],
) -> tuple[str, ...]:
    return tuple(
        profile.key
        for profile in profiles
        if profile.trades >= MIN_SAMPLE_SIZE
    )


def build_adaptive_expectancy_report(records: list[dict]) -> AdaptiveExpectancyReport:
    by_setup: dict[str, list[float]] = defaultdict(list)
    by_regime: dict[str, list[float]] = defaultdict(list)
    by_entry_type: dict[str, list[float]] = defaultdict(list)
    by_combination: dict[str, list[float]] = defaultdict(list)
    by_setup_regime_entry: dict[str, list[float]] = defaultdict(list)

    for record in records:
        # Use 5d as primary adaptive horizon.
        result = _safe_float(record.get("result_5d"))
        if result is None:
            continue

        # Only evaluate signals/trades that actually triggered.
        lifecycle_status = str(record.get("lifecycle_status") or record.get("status") or "").upper()
        if lifecycle_status and lifecycle_status in {"PENDING", "EXPIRED", "UNTRIGGERED"}:
            continue

        setup = str(record.get("setup_type", "unknown"))
        regime = str(record.get("market_state") or record.get("market_regime") or "unknown")
        entry_type = str(record.get("entry_type") or "unknown")

        combo = f"{regime}::{setup}"
        setup_regime_entry = f"{regime}::{setup}::{entry_type}"

        by_setup[setup].append(result)
        by_regime[regime].append(result)
        by_entry_type[entry_type].append(result)
        by_combination[combo].append(result)
        by_setup_regime_entry[setup_regime_entry].append(result)

    setup_profiles = _sorted_profiles(by_setup)
    regime_profiles = _sorted_profiles(by_regime)
    entry_type_profiles = _sorted_profiles(by_entry_type)
    combined_profiles = _sorted_profiles(by_combination)
    setup_regime_entry_profiles = _sorted_profiles(by_setup_regime_entry)

    # Public edge keys remain regime::setup for backward compatibility.
    # The more granular regime::setup::entry_type profiles stay available in
    # setup_regime_entry_profiles for newer adaptive-scoring consumers.
    strongest_edges = _qualified_profile_keys(combined_profiles[:5])
    weakest_edges = _qualified_profile_keys(combined_profiles[-5:])

    return AdaptiveExpectancyReport(
        setup_profiles=setup_profiles,
        regime_profiles=regime_profiles,
        entry_type_profiles=entry_type_profiles,
        combined_profiles=combined_profiles,
        setup_regime_entry_profiles=setup_regime_entry_profiles,
        strongest_edges=strongest_edges,
        weakest_edges=weakest_edges,
    )
