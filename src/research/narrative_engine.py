from __future__ import annotations


def detect_market_narratives(topics: list[dict]) -> dict:
    grouped: dict[str, int] = {}

    for topic in topics:
        narrative = topic.get("narrative", "Unknown")
        grouped[narrative] = grouped.get(narrative, 0) + 1

    dominant = sorted(
        grouped.items(),
        key=lambda item: item[1],
        reverse=True,
    )

    dominant_narrative = dominant[0][0] if dominant else "Unknown"

    return {
        "narrative_count": len(grouped),
        "dominant_narrative": dominant_narrative,
        "narratives": dominant[:5],
    }
