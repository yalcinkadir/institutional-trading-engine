from __future__ import annotations


def calculate_setup_readiness(
    asset_score: int,
    above_sma50: bool,
    above_sma200: bool,
    relative_strength_class: str,
    rvol: float,
    atr_percent: float,
    market_regime: str,
) -> dict:
    points = 0
    reasons: list[str] = []

    if asset_score >= 75:
        points += 25
        reasons.append("Asset score is institutionally strong")
    elif asset_score >= 60:
        points += 15
        reasons.append("Asset score is acceptable but not elite")
    else:
        reasons.append("Asset score is weak")

    if above_sma50:
        points += 15
        reasons.append("Price is above SMA50")
    else:
        reasons.append("Price is below SMA50")

    if above_sma200:
        points += 15
        reasons.append("Price is above SMA200")
    else:
        reasons.append("Price is below SMA200")

    if relative_strength_class == "Leader":
        points += 20
        reasons.append("Relative Strength confirms leadership")
    elif relative_strength_class == "Neutral":
        points += 10
        reasons.append("Relative Strength is neutral")
    else:
        reasons.append("Relative Strength is weak")

    if rvol >= 1.2:
        points += 10
        reasons.append("Relative volume confirms participation")
    elif rvol >= 0.8:
        points += 5
        reasons.append("Relative volume is acceptable")
    else:
        reasons.append("Relative volume is weak")

    if atr_percent <= 4:
        points += 10
        reasons.append("ATR risk is controlled")
    elif atr_percent <= 7:
        points += 5
        reasons.append("ATR risk is elevated but manageable")
    else:
        reasons.append("ATR risk is too high")

    if market_regime in {"Strong Bullish", "Bullish"}:
        points += 5
        reasons.append("Market regime supports risk-on exposure")
    elif market_regime == "Neutral":
        reasons.append("Market regime is neutral")
    else:
        points -= 10
        reasons.append("Market regime does not support aggressive entries")

    points = max(0, min(points, 100))

    if points >= 80:
        status = "READY"
    elif points >= 65:
        status = "WATCH"
    elif points >= 50:
        status = "EARLY"
    elif points >= 35:
        status = "RISKY"
    else:
        status = "AVOID"

    return {
        "score": points,
        "status": status,
        "reasons": reasons,
    }
