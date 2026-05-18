from __future__ import annotations


def evaluate_signal_quality(signals: list[dict]) -> dict:
    if not signals:
        return {
            "signals": 0,
            "quality_score": 0,
            "classification": "Unknown",
        }

    profitable = [signal for signal in signals if signal.get("pnl_percent", 0) > 0]
    avg_pnl = sum(signal.get("pnl_percent", 0) for signal in signals) / len(signals)

    quality_score = round(
        ((len(profitable) / len(signals)) * 60) + max(avg_pnl, 0) * 4,
        2,
    )

    quality_score = min(quality_score, 100)

    if quality_score >= 80:
        classification = "Institutional Grade"
    elif quality_score >= 65:
        classification = "High Quality"
    elif quality_score >= 50:
        classification = "Moderate"
    else:
        classification = "Weak"

    return {
        "signals": len(signals),
        "quality_score": quality_score,
        "classification": classification,
    }
