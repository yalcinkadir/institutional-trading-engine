from __future__ import annotations


def calculate_risk_reward(
    entry_price: float,
    target_price: float,
    stop_price: float,
) -> dict:
    reward = target_price - entry_price
    risk = entry_price - stop_price

    if risk <= 0:
        ratio = 0
    else:
        ratio = round(reward / risk, 2)

    if ratio >= 3:
        classification = "Excellent"
    elif ratio >= 2:
        classification = "Good"
    elif ratio >= 1:
        classification = "Acceptable"
    else:
        classification = "Poor"

    return {
        "risk_reward_ratio": ratio,
        "classification": classification,
    }
