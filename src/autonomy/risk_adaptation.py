from __future__ import annotations


def adapt_risk_profile(
    market_regime: str,
    vix: float,
    portfolio_correlation: float,
) -> dict:
    risk_multiplier = 1.0
    recommendations: list[str] = []

    if market_regime in {"Defensive", "Risk-Off"}:
        risk_multiplier *= 0.5
        recommendations.append("Reduce exposure")

    if vix > 25:
        risk_multiplier *= 0.7
        recommendations.append("Reduce position sizing")

    if portfolio_correlation > 0.8:
        risk_multiplier *= 0.8
        recommendations.append("Increase diversification")

    if risk_multiplier >= 1:
        profile = "Aggressive"
    elif risk_multiplier >= 0.7:
        profile = "Moderate"
    else:
        profile = "Defensive"

    return {
        "risk_multiplier": round(risk_multiplier, 2),
        "profile": profile,
        "recommendations": recommendations,
    }
