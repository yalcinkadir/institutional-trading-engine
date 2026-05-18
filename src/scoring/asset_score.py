from __future__ import annotations


def calculate_asset_score(
    trend_score: int,
    relative_strength_score: int,
    volume_score: int,
    volatility_score: int,
    risk_score: int,
) -> dict:
    total = (
        trend_score
        + relative_strength_score
        + volume_score
        + volatility_score
        + risk_score
    )

    total = max(0, min(total, 100))

    if total >= 85:
        status = "Strong Ready"
    elif total >= 75:
        status = "Ready"
    elif total >= 60:
        status = "Watch"
    elif total >= 45:
        status = "Neutral"
    else:
        status = "Weak"

    return {
        "score": total,
        "status": status,
    }
