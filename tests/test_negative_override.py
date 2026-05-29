from src.core.negative_override import (
    apply_negative_override,
    evaluate_negative_overrides,
)


def test_blocking_override_for_fallback_data():
    result = evaluate_negative_overrides(
        {
            "data_status": "FALLBACK",
            "report_quality_score": 90,
        }
    )

    assert result["max_recommendation"] == "AVOID"


def test_earnings_override_reduces_conviction():
    overrides = evaluate_negative_overrides(
        {
            "days_until_earnings": 1,
            "vix": 18,
        }
    )

    final = apply_negative_override("STRONG BUY", overrides)

    assert final["final_recommendation"] == "WATCH"


def test_vix_none_is_visible_and_not_treated_as_zero():
    overrides = evaluate_negative_overrides({"vix": None})

    assert overrides["has_overrides"] is True
    assert overrides["minor_count"] == 1
    assert overrides["max_recommendation"] == "BUY"
    assert [item["reason"] for item in overrides["overrides"]] == ["vix_unavailable"]


def test_missing_vix_key_remains_neutral_for_backwards_compatibility():
    overrides = evaluate_negative_overrides({})

    assert overrides["has_overrides"] is False
    assert overrides["max_recommendation"] == "STRONG BUY"


def test_invalid_vix_is_visible_and_not_treated_as_zero():
    overrides = evaluate_negative_overrides({"vix": "not-a-number"})

    assert overrides["minor_count"] == 1
    assert overrides["overrides"][0]["reason"] == "vix_unavailable"


def test_multiple_major_risks_force_avoid():
    overrides = evaluate_negative_overrides(
        {
            "days_until_earnings": 2,
            "vix": 35,
            "event_risk": "high",
        }
    )

    final = apply_negative_override("BUY", overrides)

    assert final["final_recommendation"] == "AVOID"


def test_minor_risks_reduce_strength():
    overrides = evaluate_negative_overrides(
        {
            "correlation": 0.91,
            "gap_percent": 6,
        }
    )

    final = apply_negative_override("STRONG BUY", overrides)

    assert final["final_recommendation"] == "HOLD"
