from __future__ import annotations


def calculate_position_risk(
    account_size: float,
    risk_percent: float,
    entry_price: float,
    stop_price: float,
) -> dict:
    risk_amount = account_size * (risk_percent / 100)
    risk_per_share = abs(entry_price - stop_price)

    if risk_per_share <= 0:
        return {
            "shares": 0,
            "risk_amount": round(risk_amount, 2),
            "risk_per_share": 0,
        }

    shares = int(risk_amount / risk_per_share)

    return {
        "shares": shares,
        "risk_amount": round(risk_amount, 2),
        "risk_per_share": round(risk_per_share, 2),
    }
