"""Small deterministic historical backtest core for P24."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

from src.backtesting.historical_models import (
    OUTCOME_ENTRY_NOT_HIT,
    OUTCOME_EXPIRED,
    OUTCOME_STOP_HIT,
    OUTCOME_TARGET_1_HIT,
    OUTCOME_TARGET_2_HIT,
    HistoricalBacktestMetrics,
    HistoricalBacktestReport,
    HistoricalBacktestResult,
    HistoricalTradePlan,
)


def load_historical_bars(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(str(path))
    df = pd.read_csv(path)
    required = {"date", "open", "high", "low", "close", "volume"}
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"missing columns: {','.join(missing)}")
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"]).dt.date.astype(str)
    for column in ["open", "high", "low", "close", "volume"]:
        df[column] = pd.to_numeric(df[column], errors="coerce")
    return df.dropna(subset=["date", "open", "high", "low", "close"]).sort_values("date").reset_index(drop=True)


def _float_or_none(value: Any) -> float | None:
    try:
        if value in (None, ""):
            return None
        converted = float(value)
        return None if pd.isna(converted) else converted
    except (TypeError, ValueError):
        return None


def load_trade_plans(path: Path) -> list[HistoricalTradePlan]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    raw = payload if isinstance(payload, list) else payload.get("plans") or payload.get("signals")
    if not isinstance(raw, list):
        raise ValueError("expected list, plans[] or signals[]")
    plans: list[HistoricalTradePlan] = []
    for index, item in enumerate(raw):
        if not isinstance(item, dict):
            continue
        if item.get("action") not in (None, "BUY_WATCH"):
            continue
        symbol = str(item.get("symbol") or "").upper()
        signal_date = item.get("signal_date") or item.get("date") or item.get("created_at")
        entry = _float_or_none(item.get("entry_trigger"))
        stop = _float_or_none(item.get("stop_loss"))
        target_1 = _float_or_none(item.get("target_1"))
        target_2 = _float_or_none(item.get("target_2"))
        if not symbol or not signal_date or entry is None or stop is None or target_1 is None:
            continue
        if not stop < entry < target_1:
            continue
        plans.append(
            HistoricalTradePlan(
                signal_id=str(item.get("signal_id") or f"historical_plan_{index}"),
                symbol=symbol,
                signal_date=str(signal_date)[:10],
                entry_trigger=entry,
                stop_loss=stop,
                target_1=target_1,
                target_2=target_2,
                valid_until=str(item.get("valid_until"))[:10] if item.get("valid_until") else None,
                entry_type=item.get("entry_type"),
                setup_type=item.get("setup_type"),
                stop_model=item.get("stop_model"),
                exit_model=item.get("exit_model"),
            )
        )
    return plans


def _result(plan: HistoricalTradePlan, **kwargs: Any) -> HistoricalBacktestResult:
    base = {
        "signal_id": plan.signal_id,
        "symbol": plan.symbol,
        "signal_date": plan.signal_date,
        "entry_type": plan.entry_type,
        "setup_type": plan.setup_type,
        "stop_model": plan.stop_model,
        "exit_model": plan.exit_model,
        "entry_date": None,
        "exit_date": None,
        "exit_price": None,
        "r_multiple": 0.0,
        "bars_evaluated": 0,
        "reason": "",
    }
    base.update(kwargs)
    return HistoricalBacktestResult(**base)


def _r(plan: HistoricalTradePlan, price: float) -> float:
    distance = plan.entry_trigger - plan.stop_loss
    return 0.0 if distance <= 0 else round((price - plan.entry_trigger) / distance, 4)


def simulate_plan(plan: HistoricalTradePlan, bars: pd.DataFrame, *, max_bars: int = 20) -> HistoricalBacktestResult:
    future = bars[bars["date"] > plan.signal_date]
    if plan.valid_until:
        future = future[future["date"] <= plan.valid_until]
    else:
        future = future.head(max_bars)
    future = future.reset_index(drop=True)

    entered = False
    t1 = False
    entry_date: str | None = None

    for index, row in future.iterrows():
        current_date = str(row["date"])
        high = float(row["high"])
        low = float(row["low"])
        count = index + 1
        if not entered and high >= plan.entry_trigger:
            entered = True
            entry_date = current_date
            if low <= plan.stop_loss:
                return _result(plan, outcome=OUTCOME_STOP_HIT, entry_hit=True, target_1_hit=False, target_2_hit=False, stop_hit=True, false_breakout=True, entry_date=entry_date, exit_date=current_date, exit_price=plan.stop_loss, r_multiple=-1.0, bars_evaluated=count, reason="same_bar_stop_first")
            if high >= plan.target_1:
                t1 = True
                if plan.target_2 and high >= plan.target_2:
                    return _result(plan, outcome=OUTCOME_TARGET_2_HIT, entry_hit=True, target_1_hit=True, target_2_hit=True, stop_hit=False, false_breakout=False, entry_date=entry_date, exit_date=current_date, exit_price=plan.target_2, r_multiple=_r(plan, plan.target_2), bars_evaluated=count, reason="target_2_hit")
            continue
        if entered:
            if low <= plan.stop_loss:
                return _result(plan, outcome=OUTCOME_STOP_HIT, entry_hit=True, target_1_hit=t1, target_2_hit=False, stop_hit=True, false_breakout=not t1, entry_date=entry_date, exit_date=current_date, exit_price=plan.stop_loss, r_multiple=-1.0, bars_evaluated=count, reason="stop_hit")
            if high >= plan.target_1:
                t1 = True
            if t1 and plan.target_2 and high >= plan.target_2:
                return _result(plan, outcome=OUTCOME_TARGET_2_HIT, entry_hit=True, target_1_hit=True, target_2_hit=True, stop_hit=False, false_breakout=False, entry_date=entry_date, exit_date=current_date, exit_price=plan.target_2, r_multiple=_r(plan, plan.target_2), bars_evaluated=count, reason="target_2_hit")

    if not entered:
        return _result(plan, outcome=OUTCOME_EXPIRED if plan.valid_until else OUTCOME_ENTRY_NOT_HIT, entry_hit=False, target_1_hit=False, target_2_hit=False, stop_hit=False, false_breakout=False, bars_evaluated=len(future), reason="entry_not_hit")
    if t1:
        return _result(plan, outcome=OUTCOME_TARGET_1_HIT, entry_hit=True, target_1_hit=True, target_2_hit=False, stop_hit=False, false_breakout=False, entry_date=entry_date, exit_date=str(future.iloc[-1]["date"]), exit_price=plan.target_1, r_multiple=_r(plan, plan.target_1), bars_evaluated=len(future), reason="target_1_only")
    close = float(future.iloc[-1]["close"]) if not future.empty else plan.entry_trigger
    return _result(plan, outcome=OUTCOME_EXPIRED, entry_hit=True, target_1_hit=False, target_2_hit=False, stop_hit=False, false_breakout=True, entry_date=entry_date, exit_date=str(future.iloc[-1]["date"]) if not future.empty else entry_date, exit_price=close, r_multiple=_r(plan, close), bars_evaluated=len(future), reason="no_exit_level_hit")


def calculate_metrics(results: list[HistoricalBacktestResult]) -> HistoricalBacktestMetrics:
    total = len(results)
    if total == 0:
        return HistoricalBacktestMetrics(0, 0, 0, 0, 0, 0, 0, 0, 0)
    rate = lambda fn: round(sum(1 for item in results if fn(item)) / total, 4)
    avg_r = round(sum(item.r_multiple for item in results) / total, 4)
    return HistoricalBacktestMetrics(
        total=total,
        entry_hit_rate=rate(lambda item: item.entry_hit),
        expired_without_entry_rate=rate(lambda item: not item.entry_hit),
        stop_hit_rate=rate(lambda item: item.stop_hit),
        target_1_hit_rate=rate(lambda item: item.target_1_hit),
        target_2_hit_rate=rate(lambda item: item.target_2_hit),
        false_breakout_rate=rate(lambda item: item.false_breakout),
        average_r=avg_r,
        expectancy_r=avg_r,
    )


def run_backtest(plans: list[HistoricalTradePlan], *, bars_root: Path, max_bars: int = 20) -> HistoricalBacktestReport:
    cache: dict[str, pd.DataFrame] = {}
    results: list[HistoricalBacktestResult] = []
    for plan in plans:
        if plan.symbol not in cache:
            cache[plan.symbol] = load_historical_bars(bars_root / f"{plan.symbol}.csv")
        results.append(simulate_plan(plan, cache[plan.symbol], max_bars=max_bars))
    return HistoricalBacktestReport(metrics=calculate_metrics(results), results=results)
