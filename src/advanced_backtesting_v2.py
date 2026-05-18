"""
Advanced Backtesting v2.

This module extends the basic backtesting framework with institutional research
validation tools:

- transaction costs and slippage adjustment
- in-sample / out-of-sample split
- walk-forward validation
- Monte Carlo trade-order stress testing

It is designed as a research validation layer, not a broker simulator.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from statistics import mean

from src.backtesting_framework import BacktestReport, BacktestSignal, BacktestSummary, BacktestTrade, run_backtest


@dataclass(frozen=True)
class CostModel:
    commission_percent: float = 0.0
    slippage_percent: float = 0.05


@dataclass(frozen=True)
class ValidationSplit:
    in_sample: BacktestReport
    out_of_sample: BacktestReport
    split_index: int


@dataclass(frozen=True)
class MonteCarloResult:
    simulations: int
    median_total_return: float
    worst_total_return: float
    best_total_return: float
    median_max_drawdown: float
    worst_max_drawdown: float


@dataclass(frozen=True)
class WalkForwardWindow:
    train_start: int
    train_end: int
    test_start: int
    test_end: int
    train_summary: BacktestSummary
    test_summary: BacktestSummary


@dataclass(frozen=True)
class AdvancedBacktestReport:
    base_report: BacktestReport
    cost_adjusted_report: BacktestReport
    validation_split: ValidationSplit
    monte_carlo: MonteCarloResult
    walk_forward_windows: tuple[WalkForwardWindow, ...]


def apply_cost_model_to_trade(trade: BacktestTrade, cost_model: CostModel) -> BacktestTrade:
    total_cost = cost_model.commission_percent + cost_model.slippage_percent
    adjusted_sized_return = trade.sized_return_percent - total_cost
    adjusted_raw_return = trade.raw_return_percent - total_cost

    return BacktestTrade(
        symbol=trade.symbol,
        market_state=trade.market_state,
        setup_type=trade.setup_type,
        decision=trade.decision,
        risk_tier=trade.risk_tier,
        entry_price=trade.entry_price,
        exit_price=trade.exit_price,
        raw_return_percent=round(adjusted_raw_return, 4),
        sized_return_percent=round(adjusted_sized_return, 4),
        mfe_percent=trade.mfe_percent,
        mae_percent=trade.mae_percent,
        holding_days=trade.holding_days,
    )


def _equity_curve(trades: list[BacktestTrade], initial_equity: float = 100.0) -> tuple[float, ...]:
    equity = initial_equity
    curve = [round(equity, 4)]
    for trade in trades:
        equity *= 1 + trade.sized_return_percent / 100
        curve.append(round(equity, 4))
    return tuple(curve)


def _max_drawdown(curve: tuple[float, ...]) -> float:
    peak = curve[0] if curve else 100.0
    max_dd = 0.0
    for value in curve:
        peak = max(peak, value)
        drawdown = ((value / peak) - 1) * 100 if peak else 0.0
        max_dd = min(max_dd, drawdown)
    return round(max_dd, 4)


def _summary_from_trades(trades: list[BacktestTrade]) -> BacktestSummary:
    if not trades:
        return BacktestSummary(0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)

    returns = [trade.sized_return_percent for trade in trades]
    wins = [value for value in returns if value > 0]
    losses = [value for value in returns if value <= 0]
    curve = _equity_curve(trades)
    gross_profit = sum(wins)
    gross_loss = abs(sum(losses))
    profit_factor = gross_profit / gross_loss if gross_loss else 999.0
    win_rate = len(wins) / len(returns)
    avg_win = mean(wins) if wins else 0.0
    avg_loss = mean(losses) if losses else 0.0
    expectancy = (win_rate * avg_win) + ((1 - win_rate) * avg_loss)

    return BacktestSummary(
        trades=len(trades),
        win_rate=round(win_rate, 4),
        average_return=round(mean(returns), 4),
        total_return=round(((curve[-1] / curve[0]) - 1) * 100, 4),
        max_drawdown=_max_drawdown(curve),
        profit_factor=round(profit_factor, 4),
        expectancy=round(expectancy, 4),
    )


def _report_from_trades(trades: list[BacktestTrade]) -> BacktestReport:
    by_setup: dict[str, list[BacktestTrade]] = {}
    by_regime: dict[str, list[BacktestTrade]] = {}

    for trade in trades:
        by_setup.setdefault(trade.setup_type, []).append(trade)
        by_regime.setdefault(trade.market_state, []).append(trade)

    return BacktestReport(
        summary=_summary_from_trades(trades),
        trades=tuple(trades),
        performance_by_setup={key: _summary_from_trades(value) for key, value in by_setup.items()},
        performance_by_regime={key: _summary_from_trades(value) for key, value in by_regime.items()},
        equity_curve=_equity_curve(trades),
    )


def apply_cost_model(report: BacktestReport, cost_model: CostModel) -> BacktestReport:
    adjusted = [apply_cost_model_to_trade(trade, cost_model) for trade in report.trades]
    return _report_from_trades(adjusted)


def split_in_sample_out_of_sample(report: BacktestReport, split_ratio: float = 0.7) -> ValidationSplit:
    trades = list(report.trades)
    split_index = int(len(trades) * split_ratio)
    return ValidationSplit(
        in_sample=_report_from_trades(trades[:split_index]),
        out_of_sample=_report_from_trades(trades[split_index:]),
        split_index=split_index,
    )


def run_monte_carlo_trade_order_stress(
    report: BacktestReport,
    *,
    simulations: int = 250,
    seed: int = 42,
) -> MonteCarloResult:
    trades = list(report.trades)
    if not trades:
        return MonteCarloResult(simulations, 0.0, 0.0, 0.0, 0.0, 0.0)

    rng = random.Random(seed)
    total_returns: list[float] = []
    max_drawdowns: list[float] = []

    for _ in range(simulations):
        shuffled = trades[:]
        rng.shuffle(shuffled)
        summary = _summary_from_trades(shuffled)
        total_returns.append(summary.total_return)
        max_drawdowns.append(summary.max_drawdown)

    total_returns_sorted = sorted(total_returns)
    drawdowns_sorted = sorted(max_drawdowns)
    mid = simulations // 2

    return MonteCarloResult(
        simulations=simulations,
        median_total_return=round(total_returns_sorted[mid], 4),
        worst_total_return=round(min(total_returns), 4),
        best_total_return=round(max(total_returns), 4),
        median_max_drawdown=round(drawdowns_sorted[mid], 4),
        worst_max_drawdown=round(min(max_drawdowns), 4),
    )


def run_walk_forward_validation(
    signals: list[BacktestSignal],
    bars_by_symbol: dict[str, list[dict]],
    *,
    train_size: int = 20,
    test_size: int = 10,
) -> tuple[WalkForwardWindow, ...]:
    windows: list[WalkForwardWindow] = []
    start = 0

    while start + train_size + test_size <= len(signals):
        train_start = start
        train_end = start + train_size
        test_start = train_end
        test_end = test_start + test_size

        train_report = run_backtest(signals[train_start:train_end], bars_by_symbol)
        test_report = run_backtest(signals[test_start:test_end], bars_by_symbol)

        windows.append(
            WalkForwardWindow(
                train_start=train_start,
                train_end=train_end,
                test_start=test_start,
                test_end=test_end,
                train_summary=train_report.summary,
                test_summary=test_report.summary,
            )
        )
        start += test_size

    return tuple(windows)


def run_advanced_backtest(
    signals: list[BacktestSignal],
    bars_by_symbol: dict[str, list[dict]],
    *,
    cost_model: CostModel | None = None,
    split_ratio: float = 0.7,
    monte_carlo_simulations: int = 250,
) -> AdvancedBacktestReport:
    cost_model = cost_model or CostModel()
    base_report = run_backtest(signals, bars_by_symbol)
    cost_adjusted = apply_cost_model(base_report, cost_model)

    return AdvancedBacktestReport(
        base_report=base_report,
        cost_adjusted_report=cost_adjusted,
        validation_split=split_in_sample_out_of_sample(cost_adjusted, split_ratio),
        monte_carlo=run_monte_carlo_trade_order_stress(cost_adjusted, simulations=monte_carlo_simulations),
        walk_forward_windows=run_walk_forward_validation(signals, bars_by_symbol),
    )
