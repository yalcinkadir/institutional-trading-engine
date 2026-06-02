import json
from pathlib import Path

from src.scoring.expectancy_adjuster import find_expectancy_adjustment


def test_er5_zero_result_5d_is_not_replaced_by_performance_percent(tmp_path: Path) -> None:
    path = tmp_path / "history.json"
    outcomes = [
        {
            "symbol": "TEST",
            "setup_type": "momentum_breakout",
            "market_regime": "low_vol_bull",
            "entry_type": "break_above",
            "lifecycle_status": "TRIGGERED",
            "classification": "WIN",
            "result_5d": 0.0,
            "performance_percent": 10.0,
        }
        for _ in range(6)
    ]
    path.write_text(json.dumps([{"signal_date": "2026-06-01", "outcomes": outcomes}]), encoding="utf-8")

    adjustment = find_expectancy_adjustment(
        setup_type="momentum_breakout",
        market_state="low_vol_bull",
        entry_type="break_above",
        outcome_history_path=path,
    )

    assert adjustment.sample_size == 6
    assert adjustment.expectancy_r == 0.0
    assert not hasattr(adjustment, "expectancy")
    assert adjustment.win_rate == 0.0
    assert adjustment.score_delta == 0.0
    assert adjustment.reason == "flat_or_mixed_expectancy"
