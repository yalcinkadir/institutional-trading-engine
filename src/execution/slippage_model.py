from __future__ import annotations


def estimate_slippage(
    spread_percent: float,
    volatility_percent: float,
    order_size_percent_of_volume: float,
) -> dict:
    slippage = (
        spread_percent * 0.4
        + volatility_percent * 0.3
        + order_size_percent_of_volume * 0.3
    )

    slippage = round(slippage, 2)

    if slippage <= 0.3:
        classification = "Low"
    elif slippage <= 0.8:
        classification = "Moderate"
    else:
        classification = "High"

    return {
        "estimated_slippage_percent": slippage,
        "classification": classification,
    }
