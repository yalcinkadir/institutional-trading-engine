from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.breadth_engine_v2 import (  # noqa: E402
    BreadthV2Input,
    evaluate_breadth_v2,
)


def test_breadth_thrust_detected_when_participation_is_broad():
    result = evaluate_breadth_v2(
        BreadthV2Input(
            percent_above_sma50=82,
            percent_above_sma200=74,
            sector_participation_percent=78,
            new_highs=420,
            new_lows=55,
            equal_weight_return_20d=0.11,
            cap_weight_return_20d=0.07,
            mega_cap_contribution_percent=31,
            previous_percent_above_sma50=61,
        )
    )

    assert result.breadth_state == "breadth_thrust_or_broad_accumulation"
    assert result.breadth_score >= 80
    assert "breadth_thrust" in result.confirmations


def test_internal_market_deterioration_detected_when_market_is_narrow():
    result = evaluate_breadth_v2(
        BreadthV2Input(
            percent_above_sma50=34,
            percent_above_sma200=29,
            sector_participation_percent=33,
            new_highs=52,
            new_lows=241,
            equal_weight_return_20d=-0.08,
            cap_weight_return_20d=0.03,
            mega_cap_contribution_percent=67,
            previous_percent_above_sma50=58,
        )
    )

    assert result.breadth_state == "internal_market_deterioration"
    assert "mega_cap_dependency" in result.warnings
    assert "new_low_expansion" in result.warnings
