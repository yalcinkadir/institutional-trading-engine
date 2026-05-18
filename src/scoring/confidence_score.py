from __future__ import annotations


def calculate_confidence_score(
    setup_score: int,
    market_health_score: int,
    vix: float,
    breadth_percent: float,
) -> dict:
    confidence = setup_score * 0.5
    confidence += market_health_score * 0.3

    if vix < 15:
        confidence += 10
    elif vix < 20:
        confidence += 5
    else:
        confidence -= 10

    if breadth_percent >= 70:
        confidence += 10
    elif breadth_percent >= 50:
        confidence += 5
    else:
        confidence -= 5

    confidence = round(max(0, min(confidence, 100)), 1)

    if confidence >= 85:
        level = "Very High"
    elif confidence >= 70:
        level = "High"
    elif confidence >= 55:
        level = "Moderate"
    elif confidence >= 40:
        level = "Low"
    else:
        level = "Very Low"

    return {
        "confidence": confidence,
        "level": level,
    }
