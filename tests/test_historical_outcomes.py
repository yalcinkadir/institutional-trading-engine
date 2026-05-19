from datetime import date

from src.outcomes.historical_outcome_store import HistoricalOutcomeStore
from src.outcomes.real_outcome_evaluator import (
    PricePoint,
    evaluate_real_outcome,
)
from src.outcomes.regime_outcome_analysis import RegimeOutcomeAnalysis


def test_historical_outcome_storage():
    store = HistoricalOutcomeStore()

    outcome = evaluate_real_outcome(
        entry_price=100,
        price_path=[
            PricePoint(date(2026, 5, 1), 105),
        ],
    )

    store.append(
        module="relative_strength",
        regime="bull",
        outcome=outcome,
    )

    results = store.load_all()

    assert len(results) >= 1


def test_regime_outcome_analysis():
    analysis = RegimeOutcomeAnalysis()

    summary = analysis.summarize(
        [
            {
                "regime": "bull",
                "outcome": {
                    "performance_percent": 5.0,
                },
            },
            {
                "regime": "bull",
                "outcome": {
                    "performance_percent": 3.0,
                },
            },
        ]
    )

    assert summary["bull"]["average_return_percent"] == 4.0
