from __future__ import annotations


def run_stress_test(
    portfolio_value: float,
    drawdown_percent: float,
    leverage: float = 1.0,
) -> dict:
    stressed_loss = round(portfolio_value * (drawdown_percent / 100) * leverage, 2)
    stressed_value = round(portfolio_value - stressed_loss, 2)

    if drawdown_percent >= 30:
        classification = "Extreme Stress"
    elif drawdown_percent >= 15:
        classification = "High Stress"
    else:
        classification = "Moderate Stress"

    return {
        "stressed_loss": stressed_loss,
        "stressed_value": stressed_value,
        "classification": classification,
    }
