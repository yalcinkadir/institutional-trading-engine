import json
from pathlib import Path

from src.scoring.expectancy_adjuster import find_expectancy_adjustment


def _write_history(path: Path, outcomes: list[dict]) -> Path:
    payload = [{"signal_date": "2026-06-02", "outcomes": outcomes}]
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


def test_er7_positive_profile_below_size_sample_floor_can_score_but_not_change_size(tmp_path: Path):
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

    assert adjustment.sample_size == 6
    assert adjustment.score_delta == 4.0
    assert adjustment.size_multiplier == 1.0
    assert adjustment.reason == "positive_expectancy_size_sample_guard"


def test_er7_negative_profile_below_size_sample_floor_can_reduce_score_but_not_size(tmp_path: Path):
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

    assert adjustment.sample_size == 6
    assert adjustment.score_delta == -12.0
    assert adjustment.size_multiplier == 1.0
    assert adjustment.recommendation == "avoid_or_block"
    assert adjustment.reason == "negative_expectancy_size_sample_guard"


def test_er8_positive_asymmetric_profile_is_not_blocked_by_low_win_rate(tmp_path: Path):
    wins = [_outcome(classification="WIN", result_5d=5.0) for _ in range(6)]
    losses = [_outcome(classification="LOSS", result_5d=-0.5) for _ in range(14)]
    history = _write_history(tmp_path / "history.json", wins + losses)

    adjustment = find_expectancy_adjustment(
        setup_type="momentum_breakout",
        market_state="low_vol_bull",
        entry_type="break_above",
        outcome_history_path=history,
    )

    assert adjustment.sample_size == 20
    assert adjustment.win_rate == 0.3
    assert adjustment.expectancy_r == 1.15
    assert adjustment.score_delta == 4.0
    assert adjustment.size_multiplier == 1.05
    assert adjustment.recommendation == "maintain_or_slightly_increase"
    assert adjustment.reason == "positive_asymmetric_expectancy"
