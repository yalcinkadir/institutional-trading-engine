from __future__ import annotations


def evaluate_liquidity(
    average_volume: float,
    dollar_volume: float,
    min_average_volume: float = 1_000_000,
    min_dollar_volume: float = 50_000_000,
) -> dict:
    score = 0
    reasons: list[str] = []

    if average_volume >= min_average_volume:
        score += 50
        reasons.append("Average volume is sufficient")
    else:
        reasons.append("Average volume is below threshold")

    if dollar_volume >= min_dollar_volume:
        score += 50
        reasons.append("Dollar volume is sufficient")
    else:
        reasons.append("Dollar volume is below threshold")

    if score >= 90:
        classification = "Institutional Liquidity"
    elif score >= 50:
        classification = "Tradable"
    else:
        classification = "Illiquid"

    return {
        "liquidity_score": score,
        "classification": classification,
        "reasons": reasons,
    }
