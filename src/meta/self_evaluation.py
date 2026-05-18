from __future__ import annotations


def perform_self_evaluation(
    system_health_score: float,
    signal_quality_score: float,
    drift_classification: str,
) -> dict:
    score = (system_health_score * 0.4) + (signal_quality_score * 0.6)

    recommendations: list[str] = []

    if drift_classification != "Stable":
        score -= 10
        recommendations.append("Review adaptive weighting and signal calibration")

    if system_health_score < 70:
        recommendations.append("Improve infrastructure stability")

    if signal_quality_score < 65:
        recommendations.append("Improve signal filtering and setup quality")

    score = round(max(0, min(score, 100)), 2)

    if score >= 85:
        classification = "Institutional Grade"
    elif score >= 70:
        classification = "Operationally Strong"
    elif score >= 55:
        classification = "Improving"
    else:
        classification = "Needs Major Improvement"

    return {
        "self_evaluation_score": score,
        "classification": classification,
        "recommendations": recommendations,
    }
