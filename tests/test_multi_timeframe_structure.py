from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from multi_timeframe_structure import (  # noqa: E402
    TimeframeStructureInput,
    evaluate_multi_timeframe_structure,
)


def test_full_alignment_detected_across_timeframes():
    weekly = TimeframeStructureInput(
        timeframe="weekly",
        close=220,
        sma20=205,
        sma50=190,
        sma200=150,
        return_20=0.18,
        atr_percent=0.03,
    )

    daily = TimeframeStructureInput(
        timeframe="daily",
        close=225,
        sma20=218,
        sma50=205,
        sma200=170,
        return_20=0.09,
        atr_percent=0.025,
    )

    short_term = TimeframeStructureInput(
        timeframe="4h",
        close=226,
        sma20=223,
        sma50=219,
        sma200=200,
        return_20=0.03,
        atr_percent=0.02,
    )

    result = evaluate_multi_timeframe_structure(
        weekly=weekly,
        daily=daily,
        short_term=short_term,
    )

    assert result.structure in {"full_alignment", "constructive_alignment"}
    assert result.alignment_score >= 65
    assert result.timing_quality in {"high", "medium"}
    assert "weekly_trend_supportive" in result.confirmations


def test_structure_deterioration_detected_with_failed_breakouts():
    weekly = TimeframeStructureInput(
        timeframe="weekly",
        close=100,
        sma20=105,
        sma50=110,
        sma200=120,
        return_20=-0.12,
        atr_percent=0.05,
        failed_breakout=True,
    )

    daily = TimeframeStructureInput(
        timeframe="daily",
        close=96,
        sma20=101,
        sma50=108,
        sma200=118,
        return_20=-0.08,
        atr_percent=0.04,
        failed_breakout=True,
    )

    short_term = TimeframeStructureInput(
        timeframe="4h",
        close=95,
        sma20=99,
        sma50=104,
        sma200=112,
        return_20=-0.04,
        atr_percent=0.03,
    )

    result = evaluate_multi_timeframe_structure(
        weekly=weekly,
        daily=daily,
        short_term=short_term,
    )

    assert result.structure == "structure_deterioration"
    assert result.alignment_score < 45
    assert "failed_breakout_pressure" in result.warnings
