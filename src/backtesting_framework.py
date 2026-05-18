"""
Real Backtesting Framework.

This module validates Decision Engine outputs against historical bars.
It is deliberately simple, deterministic and extensible.

Core goals:
- simulate decisions as historical trades
- calculate returns, MFE, MAE and holding-period outcomes
- build an equity curve
- measure drawdown
- evaluate performance by setup type and market regime

This is not a broker simulator. It is a research validation layer.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import UTC, datetime
from statistics import mean
from typing import Iterable


@dataclass(frozen=True)
class BacktestSignal:
    timestamp_utc: str
    symbol: str
    market_state: str
    setup_type: str
    decision: str
    risk_tier: str
    entry_price: float
    position_size_multiplier: float
    holding_days: int = 5


@dataclass(frozen=True)
class BacktestTrade:
    symbol: str
    market_state: str
    setup_type: str
    decision: str
    risk_tier: str
    entry_price: float
    exit_price: float
    raw_return_percent: float
    sized_return_percent: float
    mfe_percent: float
    mae_percent: float
    holding_days: int


@dataclass(frozen=True)
class BacktestSummary:
    trades: int
    win_rate: float
    average_return: float
    total_return: float
    max_drawdown: float
    profit_factor: float
    expectancy: float


@dataclass(frozen=True)
class BacktestReport:
    summary: BacktestSummary
    trades: tuple[BacktestTrade, ...]
    performance_by_setup: dict[str, BacktestSummary]
    performance_by_regime: dict[str, BacktestSummary]
    equity_curve: tuple[float, ...]


def _parse_timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _find_bar_index(bars: list[dict], timestamp_utc: str) -> int | None:
    decision_date = _parse_timestamp(timestamp_utc).date()

    for index, bar in enumerate(bars):
        raw_time = bar.get("t")
        if raw_time is None:
            continue
        bar_date = datetime.fromtimestamp(int(raw_time) / 1000, tz=UTC).date()
        if bar_date >= decision_date:
            return index

    return None


def _simulate_trade(signal: BacktestSignal, bars: list[dict]) -> BacktestTrade | None:
    if signal.decision not in {"approved", "reduced_size", "watch"}:
        return None

    start_index = _find_bar_index(bars, signal.timestamp_utc)
    if start_index is None:
        return None

    exit_index = min(start_index + signal.holding_days, len(bars) - 1)
    if exit_index <= start_index:
        return None

    entry_price = signal.entry_price or float(bars[start_index]["c"])
    exit_price = float(bars[exit_index]["c"])
    raw_return = ((exit_price / entry_price) - 1) * 100
    sized_return = raw_return * signal.position_size_multiplier

    window = bars[start_index : exit_index + 1]
    highs = [float(bar["h"]) for bar in window]
    lows = [float(bar["l"]) for bar in window]

    mfe = ((max(highs) / entry_price) - 1) * 100 if highs else 0.0
    mae = ((min(lows) / entry_price) - 1) * 100 if lows else 0.0

    return BacktestTrade(
        symbol=signal.symbol,
        market_state=signal.market_state,
        setup_type=signal.setup_type,
        decision=signal.decision,
        risk_tier=signal.risk_tier,
        entry_price=round(entry_price, 4),
        exit_price=round(exit_price, 4),
        raw_return_percent=round(raw_return, 4),
        sized_return_percent=round(sized_return, 4),
        mfe_percent=round(mfe, 4),
        mae_percent=round(mae, 4),
        holding_days=signal.holding_days,
    )


def _equity_curve_from_trades(trades: Iterable[BacktestTrade], initial_equity: float = 100.0) -> tuple[float, ...]:
    equity = initial_equity
    curve = [round(equity, 4)]

    for trade in trades:
        equity *= 1 + (trade.sized_return_percent / 100)
        curve.append(round(equity, 4))

    return tuple(curve)


def _max_drawdown(equity_curve: tuple[float, ...]) -> float:
    if not equity_curve:
        return 0.0

    peak = equity_curve[0]
    max_dd = 0.0

    for value in equity_curve:
        peak = max(peak, value)
        drawdown = ((value / peak) - 1) * 100 if peak else 0.0
        max_dd = min(max_dd, drawdown)

    return round(max_dd, 4)


def _summary(trades: list[BacktestTrade]) -> BacktestSummary:
    if not trades:
        return BacktestSummary(
            trades=0,
            win_rate=0.0,
            average_return=0.0,
            total_return=0.0,
            max_drawdown=0.0,
            profit_factor=0.0,
            expectancy=0.0,
        )

    returns = [trade.sized_return_percent for trade in trades]
    wins = [value for value in returns if value > 0]
    losses = [value for value in returns if value <= 0]
    curve = _equity_curve_from_trades(trades)

    gross_profit = sum(wins)
    gross_loss = abs(sum(losses))
    profit_factor = gross_profit / gross_loss if gross_loss else float("inf")
    win_rate = len(wins) / len(returns)
    average_win = mean(wins) if wins else 0.0
    average_loss = mean(losses) if losses else 0.0
    expectancy = (win_rate * average_win) + ((1 - win_rate) * average_loss)

    return BacktestSummary(
        trades=len(trades),
        win_rate=round(win_rate, 4),
        average_return=round(mean(returns), 4),
        total_return=round(((curve[-1] / curve[0]) - 1) * 100, 4),
        max_drawdown=_max_drawdown(curve),
        profit_factor=round(profit_factor, 4) if profit_factor != float("inf") else 999.0,
        expectancy=round(expectancy, 4),
    )


def run_backtest(
    signals: list[BacktestSignal],
    bars_by_symbol: dict[str, list[dict]],
) -> BacktestReport:
    simulated: list[BacktestTrade] = []

    for signal in signals:
        bars = bars_by_symbol.get(signal.symbol, [])
        trade = _simulate_trade(signal, bars)
        if trade is not None:
            simulated.append(trade)

    by_setup: dict[str, list[BacktestTrade]] = defaultdict(list)
    by_regime: dict[str, list[BacktestTrade]] = defaultdict(list)

    for trade in simulated:
        by_setup[trade.setup_type].append(trade)
        by_regime[trade.market_state].append(trade)

    return BacktestReport(
        summary=_summary(simulated),
        trades=tuple(simulated),
        performance_by_setup={key: _summary(value) for key, value in by_setup.items()},
        performance_by_regime={key: _summary(value) for key, value in by_regime.items()},
        equity_curve=_equity_curve_from_trades(simulated),
    )
