from __future__ import annotations


def simulate_portfolio_growth(
    initial_capital: float,
    annual_return_percent: float,
    years: int,
) -> dict:
    portfolio_values: list[float] = []
    value = initial_capital

    for _ in range(years):
        value *= 1 + (annual_return_percent / 100)
        portfolio_values.append(round(value, 2))

    return {
        "years": years,
        "final_value": round(value, 2),
        "portfolio_values": portfolio_values,
    }
