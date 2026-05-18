from __future__ import annotations


def evaluate_kill_switch(
    vix: float,
    drawdown_percent: float,
    severe_anomaly_count: int,
) -> dict:
    activated = False
    reasons: list[str] = []

    if vix >= 40:
        activated = True
        reasons.append("extreme_volatility")

    if drawdown_percent >= 20:
        activated = True
        reasons.append("portfolio_drawdown_limit")

    if severe_anomaly_count >= 5:
        activated = True
        reasons.append("market_instability")

    return {
        "kill_switch": activated,
        "reasons": reasons,
    }
