from __future__ import annotations


def forecast_regime_shift(
    current_regime: str,
    vix_trend: str,
    breadth_trend: str,
) -> dict:
    confidence = 50
    forecast = current_regime

    if vix_trend == "rising":
        confidence += 15
        if current_regime in {"Strong Bullish", "Bullish"}:
            forecast = "Neutral"

    if breadth_trend == "weakening":
        confidence += 15
        if forecast == "Neutral":
            forecast = "Defensive"

    if vix_trend == "falling" and breadth_trend == "strengthening":
        forecast = "Bullish"
        confidence += 10

    confidence = min(confidence, 95)

    return {
        "forecast_regime": forecast,
        "forecast_confidence": confidence,
    }
