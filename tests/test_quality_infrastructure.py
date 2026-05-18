from src.analytics.explainability import explain_signal_decision
from src.analytics.performance_attribution import attribute_performance
from src.analytics.shadow_validation import compare_shadow_models
from src.data.data_validator import validate_price_bars


def test_data_validator():
    result = validate_price_bars(
        [
            {"o": 100, "h": 110, "l": 95, "c": 105, "v": 1000},
            {"o": 105, "h": 112, "l": 101, "c": 108, "v": 1500},
        ],
        min_bars=1,
    )

    assert result["valid"] is True


def test_performance_attribution():
    result = attribute_performance(
        [
            {"factor": "momentum", "pnl_percent": 10},
            {"factor": "momentum", "pnl_percent": 5},
            {"factor": "macro", "pnl_percent": -2},
        ]
    )

    assert result["top_contributors"][0][0] == "momentum"


def test_explainability():
    result = explain_signal_decision(
        {
            "relative_strength": 15,
            "macro_regime": 8,
            "earnings_risk": -10,
        }
    )

    assert len(result["explanations"]) >= 2


def test_shadow_validation():
    result = compare_shadow_models(
        {"score": 80},
        {"score": 74},
    )

    assert result["classification"] in {
        "Aligned",
        "Moderate Divergence",
    }
