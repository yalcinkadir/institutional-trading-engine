from __future__ import annotations


def detect_model_drift(
    historical_accuracy: float,
    current_accuracy: float,
    tolerance: float = 10,
) -> dict:
    drift = round(historical_accuracy - current_accuracy, 2)

    if drift <= tolerance:
        classification = "Stable"
    elif drift <= tolerance * 2:
        classification = "Moderate Drift"
    else:
        classification = "Severe Drift"

    return {
        "drift_percent": drift,
        "classification": classification,
    }
