from __future__ import annotations


def detect_repeating_patterns(patterns: list[dict]) -> dict:
    occurrences: dict[str, int] = {}

    for pattern in patterns:
        name = pattern.get("pattern", "Unknown")
        occurrences[name] = occurrences.get(name, 0) + 1

    sorted_patterns = sorted(
        occurrences.items(),
        key=lambda item: item[1],
        reverse=True,
    )

    return {
        "pattern_count": len(sorted_patterns),
        "top_patterns": sorted_patterns[:5],
    }


def classify_pattern_strength(frequency: int) -> str:
    if frequency >= 20:
        return "Institutional Pattern"
    if frequency >= 10:
        return "Strong Pattern"
    if frequency >= 5:
        return "Moderate Pattern"
    return "Weak Pattern"
