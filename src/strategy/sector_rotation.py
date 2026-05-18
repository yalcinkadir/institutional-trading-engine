from __future__ import annotations


def detect_sector_rotation(sector_performance: dict[str, float]) -> dict:
    leaders = sorted(
        sector_performance.items(),
        key=lambda item: item[1],
        reverse=True,
    )[:3]

    laggards = sorted(
        sector_performance.items(),
        key=lambda item: item[1],
    )[:3]

    rotation_type = "Balanced"

    if leaders and leaders[0][0] in {"Technology", "Consumer Discretionary"}:
        rotation_type = "Growth Rotation"
    elif leaders and leaders[0][0] in {"Utilities", "Healthcare", "Consumer Staples"}:
        rotation_type = "Defensive Rotation"

    return {
        "rotation_type": rotation_type,
        "leaders": leaders,
        "laggards": laggards,
    }
