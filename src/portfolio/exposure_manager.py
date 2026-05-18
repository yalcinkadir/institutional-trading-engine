from __future__ import annotations


def calculate_exposure(positions: list[dict]) -> dict:
    total_value = round(sum(position.get("market_value", 0) for position in positions), 2)

    if total_value <= 0:
        return {
            "total_value": 0,
            "positions": [],
            "largest_position_percent": 0,
        }

    enriched = []
    for position in positions:
        market_value = position.get("market_value", 0)
        exposure_percent = round((market_value / total_value) * 100, 2)
        enriched.append({**position, "exposure_percent": exposure_percent})

    largest = max(position["exposure_percent"] for position in enriched)

    return {
        "total_value": total_value,
        "positions": enriched,
        "largest_position_percent": largest,
    }


def classify_exposure_risk(largest_position_percent: float) -> str:
    if largest_position_percent >= 35:
        return "High Concentration Risk"
    if largest_position_percent >= 25:
        return "Elevated Concentration Risk"
    if largest_position_percent >= 15:
        return "Moderate Concentration Risk"
    return "Balanced"
