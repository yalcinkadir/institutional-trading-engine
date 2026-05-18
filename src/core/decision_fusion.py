from __future__ import annotations


def fuse_decision_signals(signals: dict[str, dict]) -> dict:
    weighted_score = 0.0
    total_weight = 0.0
    contributions: dict[str, float] = {}

    for name, signal in signals.items():
        score = float(signal.get("score", 0))
        weight = float(signal.get("weight", 1))
        contribution = score * weight

        weighted_score += contribution
        total_weight += weight
        contributions[name] = round(contribution, 2)

    final_score = 0 if total_weight == 0 else round(weighted_score / total_weight, 2)

    if final_score >= 80:
        classification = "Strong Bullish Bias"
    elif final_score >= 65:
        classification = "Bullish Bias"
    elif final_score >= 45:
        classification = "Neutral Bias"
    elif final_score >= 30:
        classification = "Bearish Bias"
    else:
        classification = "Strong Bearish Bias"

    return {
        "fusion_score": final_score,
        "classification": classification,
        "contributions": contributions,
    }
