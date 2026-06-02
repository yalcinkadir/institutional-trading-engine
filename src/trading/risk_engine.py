from __future__ import annotations

from decimal import Decimal, ROUND_DOWN, ROUND_HALF_UP
from typing import Any

CENT = Decimal("0.01")


def _money(value: Any) -> Decimal:
    return Decimal(str(value)).quantize(CENT, rounding=ROUND_HALF_UP)


def _price(value: Any) -> Decimal:
    return Decimal(str(value)).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)


def _to_float(value: Decimal) -> float:
    return float(value.quantize(CENT, rounding=ROUND_HALF_UP))


def _whole_shares(value: Decimal) -> int:
    return int(value.to_integral_value(rounding=ROUND_DOWN))


def calculate_position_risk(
    account_size: float,
    risk_percent: float,
    entry_price: float,
    stop_price: float,
    buying_power: float | None = None,
    max_notional: float | None = None,
) -> dict:
    account = _money(account_size)
    risk_pct = Decimal(str(risk_percent)) / Decimal("100")
    entry = _price(entry_price)
    stop = _price(stop_price)
    risk_amount = (account * risk_pct).quantize(CENT, rounding=ROUND_HALF_UP)
    risk_per_share = abs(entry - stop).quantize(CENT, rounding=ROUND_HALF_UP)

    if risk_per_share <= 0 or entry <= 0:
        return {
            "shares": 0,
            "risk_amount": _to_float(risk_amount),
            "risk_per_share": 0.0,
            "notional": 0.0,
            "notional_cap": 0.0,
        }

    risk_capped_shares = _whole_shares(risk_amount / risk_per_share)

    notional_caps = [_money(cap) for cap in (buying_power, max_notional) if cap is not None]
    if any(cap <= 0 for cap in notional_caps):
        return {
            "shares": 0,
            "risk_amount": _to_float(risk_amount),
            "risk_per_share": _to_float(risk_per_share),
            "notional": 0.0,
            "notional_cap": 0.0,
        }

    notional_cap = min(notional_caps) if notional_caps else None

    if notional_cap is None:
        shares = risk_capped_shares
    else:
        notional_capped_shares = _whole_shares(notional_cap / entry)
        shares = min(risk_capped_shares, notional_capped_shares)

    notional = (Decimal(shares) * entry).quantize(CENT, rounding=ROUND_HALF_UP)

    return {
        "shares": shares,
        "risk_amount": _to_float(risk_amount),
        "risk_per_share": _to_float(risk_per_share),
        "notional": _to_float(notional),
        "notional_cap": _to_float(notional_cap) if notional_cap is not None else None,
    }
