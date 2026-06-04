import json
from pathlib import Path

from src.reporting.decision_report import build_decision_report


def _market_regime():
    return {
        "regime": "Bullish",
        "market_health_score": 80,
        "data_status": "LIVE",
        "breadth": {"breadth_percent": 60},
        "symbols": {"VIX": {"close": 18}},
    }


def _screener():
    return {"watchlist": ["NVDA"]}


def _write_history(path: Path, result_5d: float, classification: str = "WIN") -> Path:
    outcomes = []
    for _ in range(6):
        outcomes.append({
            "symbol": "NVDA",
            "setup_type": "momentum_breakout",
            "market_regime": "low_vol_bull",
            "entry_type": "break_above",
            "lifecycle_status": "TRIGGERED",
            "classification": classification,
            "result_5d": result_5d,
        })
    path.write_text(json.dumps([{"signal_date": "2026-05-20", "outcomes": outcomes}]), encoding="utf-8")
    return path


def test_decision_report_uses_positive_expectancy_adjustment(tmp_path: Path):
    history = _write_history(tmp_path / "outcome-history.json", result_5d=2.0)

    report = build_decision_report(
        _market_regime(),
        _screener(),
        outcome_history_path=history,
    )
    decision = report["decisions"][0]

    assert decision["base_setup_score"] != 82
    assert decision["setup_score"] == decision["base_setup_score"] + 4.0
    assert decision["expectancy"]["score_delta"] == 4.0
    assert decision["expectancy"]["source"] == "regime_setup_entry"
    assert decision["score_source"] == "evidence_adjusted"
    assert report["score_source"] == "evidence_adjusted"
    assert report["expectancy_adjustments_used"]


def test_decision_report_uses_negative_expectancy_adjustment(tmp_path: Path):
    history = _write_history(tmp_path / "outcome-history.json", result_5d=-2.5, classification="LOSS")

    report = build_decision_report(
        _market_regime(),
        _screener(),
        outcome_history_path=history,
    )
    decision = report["decisions"][0]

    assert decision["setup_score"] == decision["base_setup_score"] - 12.0
    assert decision["expectancy"]["score_delta"] == -12.0
    assert decision["score_source"] == "evidence_adjusted"
    assert decision["position_size_multiplier"] <= decision["base_position_size_multiplier"]


def test_positive_expectancy_is_ignored_when_data_quality_is_partial(tmp_path: Path):
    history = _write_history(tmp_path / "outcome-history.json", result_5d=2.0)

    market = _market_regime()
    market["data_status"] = "PARTIAL"

    report = build_decision_report(
        market,
        _screener(),
        outcome_history_path=history,
    )
    decision = report["decisions"][0]

    assert decision["setup_score"] == decision["base_setup_score"]
    assert decision["expectancy"]["reason"] == "positive_expectancy_ignored_due_to_partial_data"
