from datetime import date

from src.outcomes.performance_attribution import PerformanceAttribution
from src.outcomes.real_outcome_evaluator import (
    PricePoint,
    evaluate_real_outcome,
)


def test_real_outcome_metrics():
    outcome = evaluate_real_outcome(
        entry_price=100,
        price_path=[
            PricePoint(date(2026, 5, 1), 102),
            PricePoint(date(2026, 5, 2), 105),
            PricePoint(date(2026, 5, 3), 103),
        ],
    )

    assert outcome.performance_percent == 3.0
    assert outcome.mfe_percent == 5.0
    assert outcome.classification == "WIN"


def test_performance_attribution_summary():
    attribution = PerformanceAttribution()

    outcome = evaluate_real_outcome(
        entry_price=100,
        price_path=[
            PricePoint(date(2026, 5, 1), 105),
        ],
    )

    summary = attribution.summarize(
        {
            "relative_strength": [outcome],
        }
    )

    assert summary["relative_strength"]["win_rate_percent"] == 100.0
