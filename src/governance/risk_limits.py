from __future__ import annotations


def validate_risk_limits(
    portfolio_drawdown_percent: float,
    max_drawdown_percent: float,
    daily_loss_percent: float,
    max_daily_loss_percent: float,
) -> dict:
    breaches: list[str] = []

    if portfolio_drawdown_percent >= max_drawdown_percent:
        breaches.append("max_drawdown_breached")

    if daily_loss_percent >= max_daily_loss_percent:
        breaches.append("max_daily_loss_breached")

    status = "PASS" if not breaches else "BREACH"

    return {
        "status": status,
        "breaches": breaches,
    }
