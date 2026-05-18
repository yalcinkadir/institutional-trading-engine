from __future__ import annotations


def simulate_market_scenario(
    base_price: float,
    expected_return_percent: float,
    volatility_percent: float,
) -> dict:
    bullish_price = round(base_price * (1 + (expected_return_percent + volatility_percent) / 100), 2)
    base_case_price = round(base_price * (1 + expected_return_percent / 100), 2)
    bearish_price = round(base_price * (1 + (expected_return_percent - volatility_percent) / 100), 2)

    return {
        "bullish_price": bullish_price,
        "base_case_price": base_case_price,
        "bearish_price": bearish_price,
    }
