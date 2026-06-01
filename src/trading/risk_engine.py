from __future__ import annotations


def calculate_position_risk(
    account_size: float,
    risk_percent: float,
    entry_price: float,
    stop_price: float,
    buying_power: float | None = None,
    max_notional: float | None = None,
) -> dict:
    risk_amount = account_size * (risk_percent / 100)
    risk_per_share = abs(entry_price - stop_price)

    if risk_per_share <= 0 or entry_price <= 0:
        return {
            "shares": 0,
            "risk_amount": round(risk_amount, 2),
            "risk_per_share": 0,
            "notional": 0,
            "notional_cap": 0,
        }

    risk_capped_shares = int(risk_amount / risk_per_share)

    notional_caps = [cap for cap in (buying_power, max_notional) if cap is not None]
    positive_notional_caps = [cap for cap in notional_caps if cap > 0]
    notional_cap = min(positive_notional_caps) if positive_notional_caps else None

    if notional_cap is None:
        shares = risk_capped_shares
    else:
        notional_capped_shares = int(notional_cap / entry_price)
        shares = min(risk_capped_shares, notional_capped_shares)

    notional = shares * entry_price

    return {
        "shares": shares,
        "risk_amount": round(risk_amount, 2),
        "risk_per_share": round(risk_per_share, 2),
        "notional": round(notional, 2),
        "notional_cap": round(notional_cap, 2) if notional_cap is not None else None,
    }
