from __future__ import annotations


def generate_final_recommendation(
    conviction_score: float,
    conflict_resolution: str,
    setup_status: str,
) -> dict:
    if conflict_resolution == "Mixed Signals":
        recommendation = "HOLD"
    elif conviction_score >= 80 and setup_status == "READY":
        recommendation = "STRONG BUY"
    elif conviction_score >= 65:
        recommendation = "BUY"
    elif conviction_score >= 45:
        recommendation = "WATCH"
    else:
        recommendation = "AVOID"

    return {
        "recommendation": recommendation,
        "setup_status": setup_status,
        "conviction_score": conviction_score,
    }
