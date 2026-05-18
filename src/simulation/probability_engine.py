from __future__ import annotations


def calculate_outcome_probability(
    successful_cases: int,
    total_cases: int,
) -> dict:
    if total_cases <= 0:
        return {
            "probability_percent": 0,
            "classification": "Unknown",
        }

    probability = round((successful_cases / total_cases) * 100, 2)

    if probability >= 80:
        classification = "Very High Probability"
    elif probability >= 60:
        classification = "High Probability"
    elif probability >= 40:
        classification = "Moderate Probability"
    else:
        classification = "Low Probability"

    return {
        "probability_percent": probability,
        "classification": classification,
    }
