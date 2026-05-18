from __future__ import annotations


def classify_macro_regime(
    dollar_trend: str,
    yields_trend: str,
    gold_trend: str,
    equity_regime: str,
) -> dict:
    risk_score = 50
    signals: list[str] = []

    if dollar_trend == "rising":
        risk_score -= 10
        signals.append("Rising dollar pressures risk assets")
    elif dollar_trend == "falling":
        risk_score += 10
        signals.append("Falling dollar supports risk assets")

    if yields_trend == "rising":
        risk_score -= 10
        signals.append("Rising yields reduce equity multiple support")
    elif yields_trend == "falling":
        risk_score += 10
        signals.append("Falling yields support duration-sensitive assets")

    if gold_trend == "rising" and equity_regime in {"Defensive", "Risk-Off"}:
        risk_score -= 10
        signals.append("Gold strength confirms defensive demand")

    if equity_regime in {"Strong Bullish", "Bullish"}:
        risk_score += 15
        signals.append("Equity regime is risk-on")
    elif equity_regime in {"Defensive", "Risk-Off"}:
        risk_score -= 20
        signals.append("Equity regime is defensive")

    risk_score = max(0, min(risk_score, 100))

    if risk_score >= 70:
        regime = "Macro Risk-On"
    elif risk_score >= 45:
        regime = "Macro Neutral"
    else:
        regime = "Macro Risk-Off"

    return {
        "macro_score": risk_score,
        "macro_regime": regime,
        "signals": signals,
    }
