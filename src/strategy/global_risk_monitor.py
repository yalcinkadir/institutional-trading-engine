from __future__ import annotations


def evaluate_global_risk(
    vix: float,
    credit_spreads: str,
    geopolitical_risk: str,
) -> dict:
    score = 100
    warnings: list[str] = []

    if vix > 25:
        score -= 30
        warnings.append("VIX indicates elevated stress")

    if credit_spreads == "widening":
        score -= 25
        warnings.append("Credit spreads are widening")

    if geopolitical_risk == "high":
        score -= 25
        warnings.append("High geopolitical risk detected")

    if score >= 75:
        classification = "Stable"
    elif score >= 50:
        classification = "Elevated Risk"
    else:
        classification = "Global Stress"

    return {
        "global_risk_score": score,
        "classification": classification,
        "warnings": warnings,
    }
