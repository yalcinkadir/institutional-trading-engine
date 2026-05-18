from __future__ import annotations


def analyze_sector_risk(positions: list[dict]) -> dict:
    sector_totals: dict[str, float] = {}
    total_value = sum(position.get("market_value", 0) for position in positions)

    if total_value <= 0:
        return {
            "sectors": {},
            "highest_sector_exposure": 0,
        }

    for position in positions:
        sector = position.get("sector", "Unknown")
        sector_totals[sector] = sector_totals.get(sector, 0) + position.get("market_value", 0)

    normalized = {
        sector: round((value / total_value) * 100, 2)
        for sector, value in sector_totals.items()
    }

    highest = max(normalized.values()) if normalized else 0

    return {
        "sectors": normalized,
        "highest_sector_exposure": highest,
    }


def classify_sector_risk(highest_sector_exposure: float) -> str:
    if highest_sector_exposure >= 50:
        return "Extreme Sector Concentration"
    if highest_sector_exposure >= 35:
        return "High Sector Concentration"
    if highest_sector_exposure >= 20:
        return "Moderate Sector Concentration"
    return "Balanced Sector Exposure"
