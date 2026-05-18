from __future__ import annotations


def find_similar_regimes(
    current_regime: dict,
    historical_regimes: list[dict],
    tolerance: float = 10,
) -> list[dict]:
    current_score = current_regime.get("market_health_score", 0)
    current_label = current_regime.get("regime")

    matches: list[dict] = []

    for regime in historical_regimes:
        score = regime.get("market_health_score", 0)
        label = regime.get("regime")

        if label == current_label and abs(score - current_score) <= tolerance:
            matches.append(regime)

    return matches


def summarize_regime_memory(similar_regimes: list[dict]) -> dict:
    if not similar_regimes:
        return {
            "matches": 0,
            "average_forward_return": 0,
            "memory_signal": "No Historical Match",
        }

    returns = [regime.get("forward_return_percent", 0) for regime in similar_regimes]
    average_return = round(sum(returns) / len(returns), 2)

    if average_return > 2:
        memory_signal = "Historically Positive"
    elif average_return < -2:
        memory_signal = "Historically Negative"
    else:
        memory_signal = "Historically Neutral"

    return {
        "matches": len(similar_regimes),
        "average_forward_return": average_return,
        "memory_signal": memory_signal,
    }
