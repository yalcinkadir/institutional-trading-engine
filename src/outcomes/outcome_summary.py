from __future__ import annotations


def summarize_outcomes(outcomes: list[dict]) -> dict:
    if not outcomes:
        return {
            "win_rate": 0,
            "average_performance": 0,
            "total_outcomes": 0,
        }

    wins = sum(1 for outcome in outcomes if outcome.get("classification") == "WIN")

    performances = [
        float(outcome.get("performance_percent", 0))
        for outcome in outcomes
    ]

    return {
        "win_rate": round((wins / len(outcomes)) * 100, 2),
        "average_performance": round(sum(performances) / len(performances), 2),
        "total_outcomes": len(outcomes),
    }
