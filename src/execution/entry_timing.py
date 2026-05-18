from __future__ import annotations


def evaluate_entry_timing(
    minutes_after_open: int,
    relative_volume: float,
    volatility_percent: float,
) -> dict:
    score = 0

    if 15 <= minutes_after_open <= 120:
        score += 40
    elif minutes_after_open < 15:
        score += 10
    else:
        score += 25

    if relative_volume >= 1.2:
        score += 35
    elif relative_volume >= 0.8:
        score += 20

    if volatility_percent <= 3:
        score += 25
    elif volatility_percent <= 6:
        score += 15

    if score >= 80:
        classification = "Optimal"
    elif score >= 60:
        classification = "Good"
    elif score >= 40:
        classification = "Acceptable"
    else:
        classification = "Poor"

    return {
        "timing_score": score,
        "classification": classification,
    }
