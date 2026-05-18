from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from setup_scoring import score_setup  # noqa: E402


def _bars(start=100.0, drift=0.4, volume=1_000_000, count=240):
    bars = []
    close = start

    for index in range(count):
        close += drift
        bars.append(
            {
                "c": round(close, 2),
                "h": round(close + 1.5, 2),
                "l": round(close - 1.5, 2),
                "v": volume + (index * 1000),
            }
        )

    return bars


def test_score_setup_detects_strong_trend_and_positive_relative_strength():
    asset = _bars(drift=0.9)
    benchmark = _bars(drift=0.3)

    result = score_setup("NVDA", asset, benchmark)

    assert result.setup_score > 70
    assert result.regime_alignment > 0.6
    assert result.relative_strength_20d > 0
    assert result.trend_quality > 0.7
    assert "strong_trend_structure" in result.notes


def test_score_setup_handles_insufficient_history():
    short_asset = _bars(count=20)
    short_benchmark = _bars(count=20)

    result = score_setup("TEST", short_asset, short_benchmark)

    assert result.setup_score == 0.0
    assert result.data_confidence == 0.0
    assert "insufficient_history" in result.notes
