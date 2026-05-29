from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from outcome_tracking import (  # noqa: E402
    append_decision_record,
    build_decision_record,
    calculate_basic_expectancy,
    read_decision_records,
)
from src.outcomes.outcome_summary import summarize_outcomes
from src.outcomes.regime_outcome import evaluate_regime_performance
from src.outcomes.signal_outcome import classify_signal_outcome


def test_append_and_read_decision_records(tmp_path):
    output = tmp_path / "decision_log.csv"

    record = build_decision_record(
        symbol="QQQ",
        market_state="low_vol_bull",
        setup_type="momentum_breakout",
        decision="approved",
        risk_tier="tier_1",
        position_size_multiplier=1.0,
        setup_score=86,
        regime_alignment=0.82,
        asymmetry_score=0.77,
        data_confidence=0.91,
        blocked_reasons=[],
        notes=["full_alignment"],
        price_at_decision=520.12,
    )

    append_decision_record(output, record)

    rows = read_decision_records(output)

    assert len(rows) == 1
    assert rows[0]["symbol"] == "QQQ"
    assert rows[0]["decision"] == "approved"
    assert rows[0]["notes"] == "full_alignment"


def test_expectancy_calculation_uses_positive_and_negative_results():
    records = [
        {"result_5d": 5.0},
        {"result_5d": -2.0},
        {"result_5d": 7.0},
        {"result_5d": -1.0},
    ]

    stats = calculate_basic_expectancy(records)

    assert stats["count"] == 4
    assert stats["win_rate"] == 0.5
    assert stats["expectancy"] > 0


def test_expectancy_treats_breakeven_as_neutral_not_loss():
    records = [
        {"result_5d": 4.0},
        {"result_5d": 0.0},
        {"result_5d": -2.0},
    ]

    stats = calculate_basic_expectancy(records)

    assert stats["count"] == 3
    assert stats["win_rate"] == 0.3333
    assert stats["average_result"] == 0.6667
    assert stats["expectancy"] == 0.6667


def test_expectancy_returns_zero_stats_without_results():
    stats = calculate_basic_expectancy([])

    assert stats["count"] == 0
    assert stats["expectancy"] == 0.0


def test_signal_outcome():
    result = classify_signal_outcome(
        entry_price=100,
        current_price=110,
    )

    assert result["classification"] == "WIN"


def test_regime_outcomes():
    result = evaluate_regime_performance(
        [
            {"regime": "bullish", "performance_percent": 10},
            {"regime": "bullish", "performance_percent": 6},
            {"regime": "bearish", "performance_percent": -5},
        ]
    )

    assert result["bullish"]["average_performance"] == 8


def test_outcome_summary():
    result = summarize_outcomes(
        [
            {"classification": "WIN", "performance_percent": 10},
            {"classification": "LOSS", "performance_percent": -5},
            {"classification": "WIN", "performance_percent": 8},
        ]
    )

    assert result["win_rate"] > 60
