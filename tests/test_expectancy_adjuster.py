import json
from pathlib import Path

from src.scoring.expectancy_adjuster import (
    apply_expectancy_to_score,
    default_entry_type_for_setup,
    find_expectancy_adjustment,
)


def _write_history(path: Path, outcomes: list[dict]) -> Path:
    payload = [{"signal_date": "2026-05-20", "outcomes": outcomes}]
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def _outcome(**overrides):
    payload = {
        "symbol": "NVDA",
        "setup_type": "momentum_breakout",
        "market_regime": "low_vol_bull",
        "entry_type": "break_above",
        "lifecycle_status": "TRIGGERED",
        "classification": "WIN",
        "result_5d": 2.0,
    }
    payload.update(overrides)
    return payload


def test_missing_history_returns_no_adjustment(tmp_path: Path):
    adjustment = find_expectancy_adjustment(
        setup_type="momentum_breakout",
        market_state="low_vol_bull",
        entry_type="break_above",
        outcome_history_path=tmp_path / "missing.json",
    )

    assert adjustment.score_delta == 0
    assert adjustment.size_multiplier == 1.0
    assert adjustment.reason == "missing_outcome_history"


def test_insufficient_sample_returns_no_adjustment(tmp_path: Path):
    history = _write_history(tmp_path / "history.json", [_outcome() for _ in range(4)])

    adjustment = find_expectancy_adjustment(
        setup_type="momentum_breakout",
        market_state="low_vol_bull",
        entry_type="break_above",
        outcome_history_path=history,
    )

    assert adjustment.score_delta == 0
    assert adjustment.reason == "no_profile_with_minimum_sample"


def test_positive_regime_setup_entry_profile_increases_score_without_size_below_size_floor(tmp_path: Path):
    history = _write_history(
        tmp_path / "history.json",
        [_outcome(result_5d=2.5) for _ in range(6)],
    )

    adjustment = find_expectancy_adjustment(
        setup_type="momentum_breakout",
        market_state="low_vol_bull",
        entry_type="break_above",
        outcome_history_path=history,
    )

    assert adjustment.source == "regime_setup_entry"
    assert adjustment.sample_size == 6
    assert adjustment.score_delta == 4.0
    assert adjustment.size_multiplier == 1.0
    assert adjustment.reason == "positive_expectancy_size_sample_guard"
    assert apply_expectancy_to_score(80, adjustment) == 84.0


def test_positive_regime_setup_entry_profile_changes_size_with_enough_samples(tmp_path: Path):
    history = _write_history(
        tmp_path / "history.json",
        [_outcome(result_5d=2.5) for _ in range(20)],
    )

    adjustment = find_expectancy_adjustment(
        setup_type="momentum_breakout",
        market_state="low_vol_bull",
        entry_type="break_above",
        outcome_history_path=history,
    )

    assert adjustment.sample_size == 20
    assert adjustment.score_delta == 4.0
    assert adjustment.size_multiplier == 1.05
    assert adjustment.reason == "positive_expectancy"


def test_strong_positive_profile_increases_score_without_size_below_size_floor(tmp_path: Path):
    history = _write_history(
        tmp_path / "history.json",
        [_outcome(result_5d=3.5) for _ in range(6)],
    )

    adjustment = find_expectancy_adjustment(
        setup_type="momentum_breakout",
        market_state="low_vol_bull",
        entry_type="break_above",
        outcome_history_path=history,
    )

    assert adjustment.score_delta == 8.0
    assert adjustment.size_multiplier == 1.0
    assert adjustment.recommendation == "increase_risk_selectively"
    assert adjustment.reason == "positive_expectancy_size_sample_guard"


def test_strong_positive_profile_changes_size_with_enough_samples(tmp_path: Path):
    history = _write_history(
        tmp_path / "history.json",
        [_outcome(result_5d=3.5) for _ in range(20)],
    )

    adjustment = find_expectancy_adjustment(
        setup_type="momentum_breakout",
        market_state="low_vol_bull",
        entry_type="break_above",
        outcome_history_path=history,
    )

    assert adjustment.sample_size == 20
    assert adjustment.score_delta == 8.0
    assert adjustment.size_multiplier == 1.15
    assert adjustment.recommendation == "increase_risk_selectively"
    assert adjustment.reason == "strong_positive_expectancy"


def test_negative_profile_reduces_score_without_size_below_size_floor(tmp_path: Path):
    history = _write_history(
        tmp_path / "history.json",
        [_outcome(classification="LOSS", result_5d=-2.5) for _ in range(6)],
    )

    adjustment = find_expectancy_adjustment(
        setup_type="momentum_breakout",
        market_state="low_vol_bull",
        entry_type="break_above",
        outcome_history_path=history,
    )

    assert adjustment.score_delta == -12.0
    assert adjustment.size_multiplier == 1.0
    assert adjustment.recommendation == "avoid_or_block"
    assert adjustment.reason == "negative_expectancy_size_sample_guard"
    assert apply_expectancy_to_score(8, adjustment) == 0.0


def test_negative_profile_reduces_size_with_enough_samples(tmp_path: Path):
    history = _write_history(
        tmp_path / "history.json",
        [_outcome(classification="LOSS", result_5d=-2.5) for _ in range(20)],
    )

    adjustment = find_expectancy_adjustment(
        setup_type="momentum_breakout",
        market_state="low_vol_bull",
        entry_type="break_above",
        outcome_history_path=history,
    )

    assert adjustment.sample_size == 20
    assert adjustment.score_delta == -12.0
    assert adjustment.size_multiplier == 0.50
    assert adjustment.recommendation == "avoid_or_block"
    assert adjustment.reason == "negative_expectancy"


def test_non_trading_lifecycle_statuses_are_ignored(tmp_path: Path):
    outcomes = [_outcome(lifecycle_status="EXPIRED", result_5d=-10.0) for _ in range(10)]
    history = _write_history(tmp_path / "history.json", outcomes)

    adjustment = find_expectancy_adjustment(
        setup_type="momentum_breakout",
        market_state="low_vol_bull",
        entry_type="break_above",
        outcome_history_path=history,
    )

    assert adjustment.score_delta == 0
    assert adjustment.reason == "no_profile_with_minimum_sample"


def test_falls_back_to_regime_setup_when_entry_profile_missing(tmp_path: Path):
    outcomes = [_outcome(entry_type="pullback_to", result_5d=2.0) for _ in range(6)]
    history = _write_history(tmp_path / "history.json", outcomes)

    adjustment = find_expectancy_adjustment(
        setup_type="momentum_breakout",
        market_state="low_vol_bull",
        entry_type="break_above",
        outcome_history_path=history,
    )

    assert adjustment.source == "regime_setup"
    assert adjustment.score_delta == 4.0
    assert adjustment.size_multiplier == 1.0


def test_default_entry_type_mapping():
    assert default_entry_type_for_setup("momentum_breakout") == "break_above"
    assert default_entry_type_for_setup("pullback_continuation") == "pullback_to"
    assert default_entry_type_for_setup("defensive_rotation") == "at_market"
    assert default_entry_type_for_setup("unknown") == "unknown"
