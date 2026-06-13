"""Watcher-coupled historical lifecycle backtest.

BT207 purpose: replay historical trade plans through the same pure watcher
lifecycle engine used by Paper Observation instead of evaluating only proxy
MAE/MFE summaries. This module intentionally keeps market-data loading outside
of the watcher and injects completed historical bars as PriceBar objects.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import date
from typing import Any, Iterable

import pandas as pd

from src.backtesting.historical_models import HistoricalTradePlan
from src.signals.signal_status import SignalStatus, is_terminal_signal_status, normalize_signal_status
from src.watchers.entry_exit_watcher import PriceBar, SignalLifecycleUpdate, evaluate_signals


@dataclass(frozen=True)
class WatcherCoupledBacktestResult:
    signal_id: str
    symbol: str
    signal_date: str
    final_status: str
    lifecycle_event_count: int
    lifecycle_events: list[dict[str, Any]] = field(default_factory=list)
    watcher_engine: str = "src.watchers.entry_exit_watcher.evaluate_signals"
    backtest_coupling: str = "watcher_lifecycle_replay"

    @property
    def terminal(self) -> bool:
        return is_terminal_signal_status(self.final_status)

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["terminal"] = self.terminal
        return payload


@dataclass(frozen=True)
class WatcherCoupledBacktestReport:
    run_id: str
    data_source: str
    is_demo: bool
    live_trading_authorized: bool
    broker_execution_mode: str
    backtest_coupling: str
    watcher_engine: str
    input_plan_count: int
    evaluated_plan_count: int
    lifecycle_event_count: int
    terminal_signal_count: int
    results: list[WatcherCoupledBacktestResult]
    limitations: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "data_source": self.data_source,
            "is_demo": self.is_demo,
            "live_trading_authorized": self.live_trading_authorized,
            "broker_execution_mode": self.broker_execution_mode,
            "backtest_coupling": self.backtest_coupling,
            "watcher_engine": self.watcher_engine,
            "input_plan_count": self.input_plan_count,
            "evaluated_plan_count": self.evaluated_plan_count,
            "lifecycle_event_count": self.lifecycle_event_count,
            "terminal_signal_count": self.terminal_signal_count,
            "limitations": self.limitations,
            "results": [result.to_dict() for result in self.results],
        }


def _plan_to_watcher_signal(plan: HistoricalTradePlan) -> dict[str, Any]:
    return {
        "signal_id": plan.signal_id,
        "symbol": plan.symbol,
        "signal_date": plan.signal_date,
        "date": plan.signal_date,
        "action": "BUY_WATCH",
        "status": SignalStatus.PENDING.value,
        "entry_trigger": plan.entry_trigger,
        "stop_loss": plan.stop_loss,
        "target_1": plan.target_1,
        "target_2": plan.target_2,
        "valid_until": plan.valid_until,
        "entry_type": plan.entry_type,
        "setup_type": plan.setup_type,
        "backtest_source": "historical_trade_plan",
    }


def _normalise_bars(symbol: str, bars: pd.DataFrame) -> list[PriceBar]:
    required = {"date", "open", "high", "low", "close"}
    missing = sorted(required - set(bars.columns))
    if missing:
        raise ValueError(f"missing historical bar columns for {symbol}: {','.join(missing)}")

    frame = bars.copy()
    frame["date"] = pd.to_datetime(frame["date"]).dt.date.astype(str)
    for column in ["open", "high", "low", "close"]:
        frame[column] = pd.to_numeric(frame[column], errors="coerce")
    frame = frame.dropna(subset=["date", "open", "high", "low", "close"]).sort_values("date")

    return [
        PriceBar(
            symbol=symbol,
            timestamp=str(row["date"]),
            open=float(row["open"]),
            high=float(row["high"]),
            low=float(row["low"]),
            close=float(row["close"]),
            is_complete=True,
            completion_source="historical_completed_bar",
        )
        for _, row in frame.iterrows()
    ]


def _bar_dates(bars_by_symbol: dict[str, list[PriceBar]]) -> list[str]:
    return sorted({bar.timestamp[:10] for bars in bars_by_symbol.values() for bar in bars})


def _bars_for_day(bars_by_symbol: dict[str, list[PriceBar]], current_day: str) -> dict[str, PriceBar]:
    return {
        symbol: bar
        for symbol, bars in bars_by_symbol.items()
        for bar in bars
        if bar.timestamp[:10] == current_day
    }


def _today_for_bar_day(current_day: str) -> date | None:
    try:
        return date.fromisoformat(current_day[:10])
    except ValueError:
        return None


def run_watcher_coupled_backtest(
    plans: Iterable[HistoricalTradePlan],
    *,
    bars_by_symbol: dict[str, pd.DataFrame],
    run_id: str = "watcher-coupled-backtest",
    data_source: str = "real_data",
    is_demo: bool = False,
    live_trading_authorized: bool = False,
    broker_execution_mode: str = "paper_only",
) -> WatcherCoupledBacktestReport:
    """Replay historical plans through the production watcher lifecycle engine."""

    plans_list = list(plans)
    if live_trading_authorized:
        raise ValueError("watcher-coupled backtest must not authorize live trading")
    if broker_execution_mode != "paper_only":
        raise ValueError("watcher-coupled backtest must remain paper_only")

    watcher_signals = [_plan_to_watcher_signal(plan) for plan in plans_list]
    normalized_bars = {
        symbol.upper(): _normalise_bars(symbol.upper(), bars)
        for symbol, bars in bars_by_symbol.items()
    }
    lifecycle_by_signal: dict[str, list[dict[str, Any]]] = {signal["signal_id"]: [] for signal in watcher_signals}

    current_signals = watcher_signals
    for current_day in _bar_dates(normalized_bars):
        day_bars = _bars_for_day(normalized_bars, current_day)
        if not day_bars:
            continue
        _, updates, current_signals = evaluate_signals(
            current_signals,
            day_bars,
            today=_today_for_bar_day(current_day),
        )
        for update in updates:
            update_payload = _lifecycle_update_to_dict(update)
            lifecycle_by_signal.setdefault(update.signal_id, []).append(update_payload)
            for supplemental in update.supplemental_events:
                lifecycle_by_signal.setdefault(update.signal_id, []).append(dict(supplemental))

    results = []
    final_by_signal = {str(signal.get("signal_id")): signal for signal in current_signals}
    for plan in plans_list:
        final_signal = final_by_signal.get(plan.signal_id, {})
        final_status = normalize_signal_status(final_signal.get("status"))
        events = lifecycle_by_signal.get(plan.signal_id, [])
        results.append(
            WatcherCoupledBacktestResult(
                signal_id=plan.signal_id,
                symbol=plan.symbol,
                signal_date=plan.signal_date,
                final_status=final_status,
                lifecycle_event_count=len(events),
                lifecycle_events=events,
            )
        )

    return WatcherCoupledBacktestReport(
        run_id=run_id,
        data_source=data_source,
        is_demo=is_demo,
        live_trading_authorized=live_trading_authorized,
        broker_execution_mode=broker_execution_mode,
        backtest_coupling="watcher_lifecycle_replay",
        watcher_engine="src.watchers.entry_exit_watcher.evaluate_signals",
        input_plan_count=len(plans_list),
        evaluated_plan_count=len(results),
        lifecycle_event_count=sum(result.lifecycle_event_count for result in results),
        terminal_signal_count=sum(1 for result in results if result.terminal),
        results=results,
        limitations=[
            "Historical bars are completed-bar replay inputs; no live broker execution is performed.",
            "Intrabar ordering follows the production watcher conservative ordering.",
        ],
    )


def _lifecycle_update_to_dict(update: SignalLifecycleUpdate) -> dict[str, Any]:
    payload = asdict(update)
    payload.pop("supplemental_events", None)
    return payload
