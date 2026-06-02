import json
from pathlib import Path

from src.reporting.decision_report import build_decision_report
from src.scoring.expectancy_adjuster import find_expectancy_adjustment


def _write_history(path: Path) -> Path:
    outcomes = [
        {
            "symbol": "TEST",
            "setup_type": "momentum_breakout",
            "market_regime": "low_vol_bull",
            "entry_type": "break_above",
            "lifecycle_status": "TRIGGERED",
            "classification": "WIN",
            "result_5d": 2.0,
        }
        for _ in range(6)
    ]
    path.write_text(json.dumps([{"signal_date": "2026-06-01", "outcomes": outcomes}]), encoding="utf-8")
    return path


def _market_regime() -> dict:
    return {
        "regime": "Bullish",
        "market_health_score": 82,
        "data_status": "LIVE",
        "breadth": {"breadth_percent": 70},
        "symbols": {"VIX": {"close": 14}},
    }


def test_er11_expectancy_adjustment_uses_explicit_r_unit(tmp_path: Path) -> None:
    history = _write_history(tmp_path / "history.json")

    adjustment = find_expectancy_adjustment(
        setup_type="momentum_breakout",
        market_state="low_vol_bull",
        entry_type="break_above",
        outcome_history_path=history,
    )

    assert adjustment.expectancy_r == 2.0
    assert not hasattr(adjustment, "expectancy")


def test_er11_decision_report_expectancy_payload_uses_explicit_r_unit(tmp_path: Path) -> None:
    history = _write_history(tmp_path / "history.json")

    report = build_decision_report(
        _market_regime(),
        {"watchlist": ["TEST"]},
        outcome_history_path=history,
    )

    payload = report["decisions"][0]["expectancy"]

    assert payload["expectancy_r"] == 2.0
    assert "expectancy" not in payload
