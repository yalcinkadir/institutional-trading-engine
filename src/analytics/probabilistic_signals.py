from __future__ import annotations


def calculate_signal_probability(
    historical_success_rate: float,
    confidence_score: float,
    regime_alignment: float,
) -> dict:
    probability = (
        historical_success_rate * 0.5
        + confidence_score * 0.3
        + regime_alignment * 0.2
    )

    probability = round(max(0, min(probability, 100)), 2)

    if probability >= 80:
        classification = "Institutional Probability"
    elif probability >= 65:
        classification = "High Probability"
    elif probability >= 50:
        classification = "Moderate Probability"
    else:
        classification = "Low Probability"

    return {
        "probability_score": probability,
        "classification": classification,
    }
