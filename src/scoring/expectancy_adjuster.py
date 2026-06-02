"""
Expectancy-Based Scoring Adjuster.

This module closes the loop between historical outcomes and future scoring.

It reads lifecycle-aware outcome history and produces deterministic score and
size adjustments for the Decision Engine. The adjustment is conservative by
design: no evidence means no change; insufficient samples produce no change;
negative expectancy reduces scores more aggressively than positive expectancy
increases them.

Integration point:
- src/reporting/decision_report.py calls apply_expectancy_adjustment()
  before ranking candidates.

Primary profile hierarchy:
1. market_state::setup_type::entry_type
2. market_state::setup_type
3. setup_type

The most specific profile wins when it has enough evaluated samples.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

DEFAULT_OUTCOME_HISTORY = Path("reports/outcomes/outcome-history.json")
MIN_SAMPLES = 5

TRADING_CLASSIFICATIONS = {"WIN", "LOSS", "NEUTRAL"}
NON_TRADING_LIFECYCLE_STATUSES = {"PENDING", "EXPIRED", "UNTRIGGERED"}


@dataclass(frozen=True)
class ExpectancyAdjustment:
    profile_key: str
    source: str
    sample_size: int
    win_rate: float
    expectancy_r: float
    score_delta: float
    size_multiplier: float
    recommendation: str
    reason: str


def no_adjustment(reason: str = "no_expectancy_profile") -> ExpectancyAdjustment:
    return ExpectancyAdjustment(
        profile_key="none",
        source="none",
        sample_size=0,
        win_rate=0.0,
        expectancy_r=0.0,
        score_delta=0.0,
        size_multiplier=1.0,
        recommendation="neutral",
        reason=reason,
    )


def _safe_float(value: Any) -> float | None:
    if value in {None, "", "None"}:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _first_present_float(payload: dict[str, Any], keys: tuple[str, ...]) -> float | None:
    for key in keys:
        if key in payload:
            value = _safe_float(payload.get(key))
            if value is not None:
                return value
    return None


def _setup_to_default_entry_type(setup_type: str) -> str:
    return {
        "momentum_breakout": "break_above",
        "pullback_continuation": "pullback_to",
        "defensive_rotation": "at_market",
        "mean_reversion": "at_market",
        "reversal_asymmetry": "break_above",
        "speculative_growth": "break_above",
    }.get(setup_type, "unknown")


def default_entry_type_for_setup(setup_type: str) -> str:
    """Public wrapper used by decision report integration."""
    return _setup_to_default_entry_type(setup_type)


def _iter_outcomes(history: list[dict[str, Any]]) -> list[dict[str, Any]]:
    outcomes: list[dict[str, Any]] = []
    for batch in history:
        batch_outcomes = batch.get("outcomes", [])
        if isinstance(batch_outcomes, list):
            outcomes.extend(item for item in batch_outcomes if isinstance(item, dict))
    return outcomes


def load_outcome_history(path: str | Path = DEFAULT_OUTCOME_HISTORY) -> list[dict[str, Any]]:
    input_path = Path(path)
    if not input_path.exists():
        return []
    try:
        payload = json.loads(input_path.read_text(encoding="utf-8"))
        if isinstance(payload, list):
            return payload
    except json.JSONDecodeError:
        return []
    return []


def _usable_result(outcome: dict[str, Any]) -> float | None:
    classification = str(outcome.get("classification") or "").upper()
    lifecycle_status = str(outcome.get("lifecycle_status") or "").upper()

    if classification not in TRADING_CLASSIFICATIONS:
        return None
    if lifecycle_status in NON_TRADING_LIFECYCLE_STATUSES:
        return None

    return _first_present_float(outcome, ("result_5d", "performance_percent"))


def _build_profiles(outcomes: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    groups: dict[str, list[float]] = {}

    for outcome in outcomes:
        result = _usable_result(outcome)
        if result is None:
            continue

        setup_type = str(outcome.get("setup_type") or "unknown")
        market_state = str(outcome.get("market_state") or outcome.get("market_regime") or "unknown")
        entry_type = str(outcome.get("entry_type") or _setup_to_default_entry_type(setup_type))

        keys = [
            f"setup::{setup_type}",
            f"regime_setup::{market_state}::{setup_type}",
            f"regime_setup_entry::{market_state}::{setup_type}::{entry_type}",
        ]

        for key in keys:
            groups.setdefault(key, []).append(result)

    profiles: dict[str, dict[str, Any]] = {}
    for key, results in groups.items():
        wins = [value for value in results if value > 0]
        trades = len(results)
        win_rate = len(wins) / trades if trades else 0.0
        expectancy_r = sum(results) / trades if trades else 0.0
        profiles[key] = {
            "key": key,
            "sample_size": trades,
            "win_rate": round(win_rate, 4),
            "expectancy_r": round(expectancy_r, 4),
        }

    return profiles


def _adjustment_from_profile(profile: dict[str, Any], source: str) -> ExpectancyAdjustment:
    sample_size = int(profile.get("sample_size", 0))
    win_rate = float(profile.get("win_rate", 0.0))
    expectancy_r = float(profile.get("expectancy_r", 0.0))
    profile_key = str(profile.get("key", "unknown"))

    if sample_size < MIN_SAMPLES:
        return no_adjustment("insufficient_expectancy_sample")

    if expectancy_r >= 3.0 and win_rate >= 0.60:
        return ExpectancyAdjustment(
            profile_key=profile_key,
            source=source,
            sample_size=sample_size,
            win_rate=win_rate,
            expectancy_r=expectancy_r,
            score_delta=8.0,
            size_multiplier=1.15,
            recommendation="increase_risk_selectively",
            reason="strong_positive_expectancy",
        )

    if expectancy_r >= 1.0 and win_rate >= 0.52:
        return ExpectancyAdjustment(
            profile_key=profile_key,
            source=source,
            sample_size=sample_size,
            win_rate=win_rate,
            expectancy_r=expectancy_r,
            score_delta=4.0,
            size_multiplier=1.05,
            recommendation="maintain_or_slightly_increase",
            reason="positive_expectancy",
        )

    if expectancy_r <= -2.0 or (expectancy_r < 0.0 and win_rate <= 0.35):
        return ExpectancyAdjustment(
            profile_key=profile_key,
            source=source,
            sample_size=sample_size,
            win_rate=win_rate,
            expectancy_r=expectancy_r,
            score_delta=-12.0,
            size_multiplier=0.50,
            recommendation="avoid_or_block",
            reason="negative_expectancy",
        )

    if expectancy_r < -0.5:
        return ExpectancyAdjustment(
            profile_key=profile_key,
            source=source,
            sample_size=sample_size,
            win_rate=win_rate,
            expectancy_r=expectancy_r,
            score_delta=-6.0,
            size_multiplier=0.75,
            recommendation="reduce_size",
            reason="weak_expectancy",
        )

    return ExpectancyAdjustment(
        profile_key=profile_key,
        source=source,
        sample_size=sample_size,
        win_rate=win_rate,
        expectancy_r=expectancy_r,
        score_delta=0.0,
        size_multiplier=1.0,
        recommendation="neutral",
        reason="flat_or_mixed_expectancy",
    )


def find_expectancy_adjustment(
    *,
    setup_type: str,
    market_state: str,
    entry_type: str | None = None,
    outcome_history_path: str | Path = DEFAULT_OUTCOME_HISTORY,
) -> ExpectancyAdjustment:
    """Find the best available expectancy adjustment for a setup context."""
    history = load_outcome_history(outcome_history_path)
    if not history:
        return no_adjustment("missing_outcome_history")

    outcomes = _iter_outcomes(history)
    if not outcomes:
        return no_adjustment("empty_outcome_history")

    profiles = _build_profiles(outcomes)
    resolved_entry_type = entry_type or _setup_to_default_entry_type(setup_type)

    candidates = [
        ("regime_setup_entry", f"regime_setup_entry::{market_state}::{setup_type}::{resolved_entry_type}"),
        ("regime_setup", f"regime_setup::{market_state}::{setup_type}"),
        ("setup", f"setup::{setup_type}"),
    ]

    for source, key in candidates:
        profile = profiles.get(key)
        if profile and int(profile.get("sample_size", 0)) >= MIN_SAMPLES:
            return _adjustment_from_profile(profile, source)

    return no_adjustment("no_profile_with_minimum_sample")


def apply_expectancy_to_score(base_score: float, adjustment: ExpectancyAdjustment) -> float:
    """Apply score delta and clamp to [0, 100]."""
    return round(max(0.0, min(100.0, base_score + adjustment.score_delta)), 2)
