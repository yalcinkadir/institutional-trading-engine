from __future__ import annotations


def analyze_earnings_risk(
    days_until_earnings: int,
    implied_move_percent: float,
) -> dict:
    score = 100
    warnings: list[str] = []

    if days_until_earnings <= 3:
        score -= 40
        warnings.append("Earnings event is imminent")
    elif days_until_earnings <= 7:
        score -= 20
        warnings.append("Earnings event approaching")

    if implied_move_percent >= 10:
        score -= 30
        warnings.append("High implied move expected")
    elif implied_move_percent >= 5:
        score -= 15
        warnings.append("Moderate implied move expected")

    score = max(score, 0)

    if score >= 80:
        classification = "Low Earnings Risk"
    elif score >= 55:
        classification = "Moderate Earnings Risk"
    else:
        classification = "High Earnings Risk"

    return {
        "earnings_risk_score": score,
        "classification": classification,
        "warnings": warnings,
    }
