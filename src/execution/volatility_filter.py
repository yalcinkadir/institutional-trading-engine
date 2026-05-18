from __future__ import annotations


def evaluate_volatility_filter(
    atr_percent: float,
    vix: float,
) -> dict:
    score = 100
    warnings: list[str] = []

    if atr_percent > 7:
        score -= 40
        warnings.append("ATR volatility is elevated")
    elif atr_percent > 4:
        score -= 20
        warnings.append("ATR volatility is moderate")

    if vix > 30:
        score -= 40
        warnings.append("VIX indicates extreme market stress")
    elif vix > 20:
        score -= 20
        warnings.append("VIX indicates elevated market volatility")

    score = max(score, 0)

    if score >= 80:
        classification = "Stable"
    elif score >= 60:
        classification = "Tradable"
    elif score >= 40:
        classification = "Risky"
    else:
        classification = "Avoid"

    return {
        "volatility_score": score,
        "classification": classification,
        "warnings": warnings,
    }
