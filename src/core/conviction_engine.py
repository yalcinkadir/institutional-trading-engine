from __future__ import annotations


def calculate_conviction(
    fusion_score: float,
    confidence_score: float,
    signal_quality_score: float,
    macro_score: float,
) -> dict:
    conviction = (
        fusion_score * 0.35
        + confidence_score * 0.25
        + signal_quality_score * 0.2
        + macro_score * 0.2
    )

    conviction = round(max(0, min(conviction, 100)), 2)

    if conviction >= 85:
        level = "Institutional High Conviction"
    elif conviction >= 70:
        level = "High Conviction"
    elif conviction >= 55:
        level = "Moderate Conviction"
    else:
        level = "Low Conviction"

    return {
        "conviction_score": conviction,
        "level": level,
    }
