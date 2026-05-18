from __future__ import annotations


def adapt_strategy_weights(
    strategy_performance: dict[str, float],
) -> dict:
    positive = {
        strategy: max(score, 0)
        for strategy, score in strategy_performance.items()
    }

    total = sum(positive.values())

    if total <= 0:
        equal = round(1 / max(len(strategy_performance), 1), 4)
        return {
            strategy: equal
            for strategy in strategy_performance
        }

    return {
        strategy: round(score / total, 4)
        for strategy, score in positive.items()
    }
