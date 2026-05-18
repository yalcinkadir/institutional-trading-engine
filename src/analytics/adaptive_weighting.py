from __future__ import annotations


def adjust_factor_weights(
    current_weights: dict[str, float],
    performance_metrics: dict[str, float],
) -> dict:
    updated: dict[str, float] = {}

    for factor, weight in current_weights.items():
        performance = performance_metrics.get(factor, 0)

        adjustment = performance / 100
        new_weight = max(0.05, min(weight + adjustment, 1.0))

        updated[factor] = round(new_weight, 2)

    total = sum(updated.values())

    if total > 0:
        updated = {
            factor: round(value / total, 2)
            for factor, value in updated.items()
        }

    return updated
