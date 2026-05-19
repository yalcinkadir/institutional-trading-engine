from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class PricePoint:
    trade_date: date
    close: float


@dataclass(frozen=True)
class OutcomeEvaluation:
    entry_price: float
    exit_price: float
    performance_percent: float
    holding_days: int
    mfe_percent: float
    mae_percent: float
    max_drawdown_percent: float
    classification: str


def evaluate_real_outcome(
    entry_price: float,
    price_path: list[PricePoint],
    bullish: bool = True,
    neutral_threshold_percent: float = 1.0,
) -> OutcomeEvaluation:
    if entry_price <= 0:
        raise ValueError("entry_price must be positive")

    if not price_path:
        raise ValueError("price_path must not be empty")

    exit_price = price_path[-1].close
    raw_performance = ((exit_price - entry_price) / entry_price) * 100
    performance = raw_performance if bullish else -raw_performance

    path_returns = [
        (((point.close - entry_price) / entry_price) * 100) * (1 if bullish else -1)
        for point in price_path
    ]

    mfe = max(path_returns)
    mae = min(path_returns)

    peak = path_returns[0]
    max_drawdown = 0.0

    for value in path_returns:
        peak = max(peak, value)
        drawdown = value - peak
        max_drawdown = min(max_drawdown, drawdown)

    if performance > neutral_threshold_percent:
        classification = "WIN"
    elif performance < -neutral_threshold_percent:
        classification = "LOSS"
    else:
        classification = "NEUTRAL"

    holding_days = max(
        (price_path[-1].trade_date - price_path[0].trade_date).days,
        1,
    )

    return OutcomeEvaluation(
        entry_price=round(entry_price, 4),
        exit_price=round(exit_price, 4),
        performance_percent=round(performance, 2),
        holding_days=holding_days,
        mfe_percent=round(mfe, 2),
        mae_percent=round(mae, 2),
        max_drawdown_percent=round(max_drawdown, 2),
        classification=classification,
    )
