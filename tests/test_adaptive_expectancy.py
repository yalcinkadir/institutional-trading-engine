from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from adaptive_expectancy import build_adaptive_expectancy_report  # noqa: E402


def test_expectancy_layer_detects_strong_and_weak_edges():
    records = []

    for result in [5, 4, 6, 3, 7, 4]:
        records.append(
            {
                "setup_type": "momentum_breakout",
                "market_state": "low_vol_bull",
                "result_5d": result,
            }
        )

    for result in [-4, -3, -2, -5, -1, -3]:
        records.append(
            {
                "setup_type": "speculative_growth",
                "market_state": "risk_off",
                "result_5d": result,
            }
        )

    report = build_adaptive_expectancy_report(records)

    assert len(report.setup_profiles) >= 2
    assert "low_vol_bull::momentum_breakout" in report.strongest_edges
    assert "risk_off::speculative_growth" in report.weakest_edges

    top_profile = report.setup_profiles[0]

    assert top_profile.expectancy > 0
    assert top_profile.recommendation in {
        "increase_risk_selectively",
        "maintain_exposure",
    }


def test_expectancy_layer_marks_small_samples_as_insufficient():
    records = [
        {
            "setup_type": "mean_reversion",
            "market_state": "neutral",
            "result_5d": 1,
        },
        {
            "setup_type": "mean_reversion",
            "market_state": "neutral",
            "result_5d": -1,
        },
    ]

    report = build_adaptive_expectancy_report(records)

    profile = report.setup_profiles[0]

    assert profile.trades == 2
    assert profile.recommendation == "insufficient_data"
