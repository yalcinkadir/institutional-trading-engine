from __future__ import annotations

from src.expectancy_feedback_summary import build_weekly_expectancy_summary


def test_weekly_summary_reports_insufficient_data_when_empty() -> None:
    text = build_weekly_expectancy_summary(
        {
            "setup_profiles": [],
            "regime_profiles": [],
            "entry_type_profiles": [],
            "strongest_edges": [],
            "weakest_edges": [],
        }
    )

    assert "Weekly Expectancy Feedback" in text
    assert "Evaluated profile samples: 0" in text
    assert "Insufficient evaluated data" in text
    assert "No evaluated samples yet" in text


def test_weekly_summary_includes_edges_and_sample_quality() -> None:
    text = build_weekly_expectancy_summary(
        {
            "setup_profiles": [
                {
                    "key": "momentum_breakout",
                    "trades": 12,
                    "win_rate": "58.33%",
                }
            ],
            "regime_profiles": [],
            "entry_type_profiles": [],
            "strongest_edges": ["momentum_breakout: expectancy +1.25"],
            "weakest_edges": ["extended_chase: expectancy -0.75"],
        }
    )

    assert "Evaluated profile samples: 12" in text
    assert "momentum_breakout: expectancy +1.25" in text
    assert "extended_chase: expectancy -0.75" in text
    assert "Sample size available" in text


def test_weekly_summary_limits_edges() -> None:
    text = build_weekly_expectancy_summary(
        {
            "setup_profiles": [{"key": "setup", "trades": 20}],
            "regime_profiles": [],
            "entry_type_profiles": [],
            "strongest_edges": [f"edge-{i}" for i in range(10)],
            "weakest_edges": [f"weak-{i}" for i in range(10)],
        },
        max_edges=3,
    )

    assert "edge-0" in text
    assert "edge-2" in text
    assert "edge-3" not in text
    assert "weak-0" in text
    assert "weak-2" in text
    assert "weak-3" not in text


def test_weekly_summary_warns_on_low_sample_size() -> None:
    text = build_weekly_expectancy_summary(
        {
            "setup_profiles": [{"key": "setup", "trades": 3}],
            "regime_profiles": [],
            "entry_type_profiles": [],
            "strongest_edges": ["setup: expectancy +0.3"],
            "weakest_edges": [],
        }
    )

    assert "Evaluated profile samples: 3" in text
    assert "Low sample size" in text
