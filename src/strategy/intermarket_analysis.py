from __future__ import annotations


def analyze_intermarket_signals(
    spy_trend: str,
    bonds_trend: str,
    dollar_trend: str,
    gold_trend: str,
) -> dict:
    alignment_score = 0
    signals: list[str] = []

    if spy_trend == "bullish":
        alignment_score += 30
        signals.append("Equities support risk appetite")

    if bonds_trend == "bullish":
        alignment_score -= 10
        signals.append("Bond strength may indicate defensive positioning")

    if dollar_trend == "bearish":
        alignment_score += 20
        signals.append("Weak dollar supports global liquidity")

    if gold_trend == "bullish":
        alignment_score -= 10
        signals.append("Gold strength may signal uncertainty")

    if alignment_score >= 30:
        classification = "Risk-On Alignment"
    elif alignment_score >= 10:
        classification = "Mixed Alignment"
    else:
        classification = "Risk-Off Alignment"

    return {
        "alignment_score": alignment_score,
        "classification": classification,
        "signals": signals,
    }
