from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.data_quality_engine import (  # noqa: E402
    DataFeedSnapshot,
    evaluate_data_quality,
)


def test_high_quality_data_detected_under_clean_conditions():
    result = evaluate_data_quality(
        [
            DataFeedSnapshot(
                source="polygon",
                symbol="SPY",
                timestamp_utc="2026-05-18T12:00:00+00:00",
                close=735.2,
                volume=1200000,
                bars_count=100,
                expected_bars_count=100,
                price_change_percent=1.2,
                volume_zscore=1.1,
            ),
            DataFeedSnapshot(
                source="backup",
                symbol="SPY",
                timestamp_utc="2026-05-18T12:00:00+00:00",
                close=735.5,
                volume=1180000,
                bars_count=100,
                expected_bars_count=100,
                price_change_percent=1.1,
                volume_zscore=1.0,
            ),
        ],
        now_utc="2026-05-18T13:00:00+00:00",
    )

    assert result.quality_state in {
        "data_quality_high",
        "data_quality_acceptable",
    }
    assert result.confidence_multiplier >= 0.85


def test_data_quality_blocking_detected_under_stale_and_inconsistent_conditions():
    result = evaluate_data_quality(
        [
            DataFeedSnapshot(
                source="polygon",
                symbol="QQQ",
                timestamp_utc="2026-05-10T12:00:00+00:00",
                close=700,
                volume=-1,
                bars_count=40,
                expected_bars_count=100,
                price_change_percent=34,
                volume_zscore=6,
            ),
            DataFeedSnapshot(
                source="backup",
                symbol="QQQ",
                timestamp_utc="2026-05-10T12:00:00+00:00",
                close=730,
                volume=None,
                bars_count=30,
                expected_bars_count=100,
                price_change_percent=29,
                volume_zscore=7,
            ),
        ],
        now_utc="2026-05-18T13:00:00+00:00",
    )

    assert result.quality_state in {
        "data_quality_poor",
        "data_quality_blocking",
    }
    assert result.require_manual_review is True
    assert any("stale_data" in item for item in result.warnings)
