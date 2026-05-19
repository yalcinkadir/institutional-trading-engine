from __future__ import annotations


def evaluate_regime_performance(outcomes: list[dict]) -> dict:
    grouped: dict[str, list[float]] = {}

    for outcome in outcomes:
        regime = outcome.get("regime", "unknown")
        performance = float(outcome.get("performance_percent", 0))

        grouped.setdefault(regime, []).append(performance)

    summary: dict[str, dict] = {}

    for regime, values in grouped.items():
        avg = round(sum(values) / len(values), 2)

        summary[regime] = {
            "count": len(values),
            "average_performance": avg,
        }

    return summary
