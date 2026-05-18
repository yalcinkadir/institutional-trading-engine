from __future__ import annotations


def calculate_portfolio_correlation(positions: list[dict]) -> dict:
    if not positions:
        return {
            "average_correlation": 0,
            "classification": "Unknown",
        }

    correlations = [
        position.get("correlation", 0)
        for position in positions
        if "correlation" in position
    ]

    if not correlations:
        return {
            "average_correlation": 0,
            "classification": "Unknown",
        }

    average = round(sum(correlations) / len(correlations), 2)

    if average >= 0.8:
        classification = "Highly Correlated"
    elif average >= 0.6:
        classification = "Moderately Correlated"
    elif average >= 0.4:
        classification = "Diversified"
    else:
        classification = "Strongly Diversified"

    return {
        "average_correlation": average,
        "classification": classification,
    }
