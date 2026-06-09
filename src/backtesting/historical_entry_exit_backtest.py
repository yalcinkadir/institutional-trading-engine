"""Small deterministic historical backtest core for P24."""

from __future__ import annotations

import json
from dataclasses import dataclass
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
    HistoricalTradePlanLoadReport,
    HistoricalTradePlanLoadResult,
    HistoricalTradePlanRejection,
)

SUPPORTED_STOP_MODELS = {None, "fixed", "percentage_stop", "breakeven_after_t1"}
SUPPORTED_EXIT_MODELS = {None, "t1_t2", "r_multiple_targets", "t1_only"}
DEMO_MARKERS = {"demo", "synthetic", "public_safe", "historical_demo", "placeholder"}


@dataclass(frozen=True)
class BacktestExecutionConfig:
    """Execution assumptions for deterministic historical plan simulation."""

    same_bar_stop_first: bool = True
    model_stop_gaps: bool = True
    model_entry_gaps: bool = True


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


def _has_demo_marker(value: Any) -> bool:
    if isinstance(value, str):
        lower = value.lower()
        return any(marker in lower for marker in DEMO_MARKERS)
    if isinstance(value, list):
        return any(_has_demo_marker(item) for item in value)
    if isinstance(value, dict):
        return any(_has_demo_marker(item) for item in value.values())
    return False


def _extract_raw_trade_plans(path: Path) -> list[Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    raw = payload if isinstance(payload, list) else payload.get("plans") or payload.get("signals")
    if not isinstance(raw, list):
        raise ValueError("expected list, plans[] or signals[]")
    return raw


def _reject(index: int, item: Any, reasons: list[str]) -> HistoricalTradePlanRejection:
    signal_id = item.get("signal_id") if isinstance(item, dict) else None
    symbol = item.get("symbol") if isinstance(item, dict) else None
    return HistoricalTradePlanRejection(
        plan_index=index,
        signal_id=str(signal_id) if signal_id not in (None, "") else None,
        symbol=str(symbol).upper() if symbol not in (None, "") else None,
        reasons=reasons,
    )


def load_trade_plans_with_report(path: Path) -> HistoricalTradePlanLoadResult:
    raw = _extract_raw_trade_plans(path)
    plans: list[HistoricalTradePlan] = []
    rejections: list[HistoricalTradePlanRejection] = []

    for index, item in enumerate(raw):
        if not isinstance(item, dict):
            rejections.append(_reject(index, item, ["trade_plan_not_object"]))
            continue

        reasons: list[str] = []
        if item.get("action") not in (None, "BUY_WATCH"):
            reasons.append("non_buy_watch_action")
        if _has_demo_marker(item):
            reasons.append("demo_marker_detected")

        symbol = str(item.get("symbol") or "").upper()
        signal_date = item.get("signal_date") or item.get("date") or item.get("created_at")
        entry = _float_or_none(item.get("entry_trigger"))
        stop = _float_or_none(item.get("stop_loss"))
        target_1 = _float_or_none(item.get("target_1"))
        target_2 = _float_or_none(item.get("target_2"))

        if not symbol:
            reasons.append("missing_symbol")
        if not signal_date:
            reasons.append("missing_signal_date")
        if entry is None:
            reasons.append("missing_entry_trigger")
        if stop is None:
            reasons.append("missing_stop_loss")
        if target_1 is None:
            reasons.append("missing_target_1")
        if entry is not None and stop is not None and target_1 is not None and not stop < entry < target_1:
            reasons.append("invalid_entry_stop_target_order")

        if reasons:
            rejections.append(_reject(index, item, reasons))
            continue

        plans.append(
            HistoricalTradePlan(
                signal_id=str(item.get("signal_id") or f"historical_plan_{index}"),
                symbol=symbol,
                signal_date=str(signal_date)[:10],
                entry_trigger=float(entry),
                stop_loss=float(stop),
                target_1=float(target_1),
                target_2=target_2,
                valid_until=str(item.get("valid_until"))[:10] if item.get("valid_until") else None,
                entry_type=item.get("entry_type"),
                setup_type=item.get("setup_type"),
                stop_model=item.get("stop_model"),
                exit_model=item.get("exit_model"),
            )
        )

    report = HistoricalTradePlanLoadReport(
        input_plan_count=len(raw),
        accepted_plan_count=len(plans),
        rejected_plan_count=len(rejections),
        rejection_reasons=rejections,
    )
    return HistoricalTradePlanLoadResult(plans=plans, report=report)


def load_trade_plans(path: Path) -> list[HistoricalTradePlan]:
    return load_trade_plans_with_report(path).plans


def _initial_result_fields(plan: HistoricalTradePlan) -> dict[str, Any]:
    return {
        "entry_trigger": plan.entry_trigger,
        "initial_stop_loss": plan.stop_loss,
        "target_1": plan.target_1,
        "target_2": plan.target_2,
    }


def _missing_fields_for_result(*, entry_hit: bool, mae_mfe_available: bool) -> dict[str, str]:
    missing: dict[str, str] = {}
    if not entry_hit:
        missing["entry_price"] = "entry_not_hit"
    if not mae_mfe_available:
        missing["max_favorable_excursion_r"] = "entry_not_hit_or_no_post_signal_bars"
        missing["max_adverse_excursion_r"] = "entry_not_hit_or_no_post_signal_bars"
    return missing


def _excursion_fields(plan: HistoricalTradePlan, observed_bars: pd.DataFrame, entry_price: float | None) -> dict[str, float | None]:
    if entry_price is None or observed_bars.empty:
        return {"max_favorable_excursion_r": None, "max_adverse_excursion_r": None}

    risk = entry_price - plan.stop_loss
    if risk <= 0:
        return {"max_favorable_excursion_r": None, "max_adverse_excursion_r": None}

    highest_high = float(observed_bars["high"].max())
    lowest_low = float(observed_bars["low"].min())
    return {
        "max_favorable_excursion_r": round((highest_high - entry_price) / risk, 4),
        "max_adverse_excursion_r": round((lowest_low - entry_price) / risk, 4),
    }


def _enriched_result_fields(
    plan: HistoricalTradePlan,
    *,
    entry_price: float | None,
    observed_bars: pd.DataFrame,
    same_bar_ambiguous: bool,
    signal_day_cluster_size: int | None,
) -> dict[str, Any]:
    excursions = _excursion_fields(plan, observed_bars, entry_price)
    mae_mfe_available = excursions["max_favorable_excursion_r"] is not None and excursions["max_adverse_excursion_r"] is not None
    return {
        **_initial_result_fields(plan),
        "entry_price": entry_price,
        **excursions,
        "same_bar_ambiguous": same_bar_ambiguous,
        "missing_field_reasons": _missing_fields_for_result(entry_hit=entry_price is not None, mae_mfe_available=mae_mfe_available),
        "signal_day_cluster_size": signal_day_cluster_size,
    }


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
        **_initial_result_fields(plan),
        "entry_price": None,
        "max_favorable_excursion_r": None,
        "max_adverse_excursion_r": None,
        "same_bar_ambiguous": False,
        "missing_field_reasons": _missing_fields_for_result(entry_hit=False, mae_mfe_available=False),
        "signal_day_cluster_size": None,
    }
    base.update(kwargs)
    return HistoricalBacktestResult(**base)


def _r(plan: HistoricalTradePlan, price: float, entry_price: float | None = None) -> float:
    effective_entry = plan.entry_trigger if entry_price is None else entry_price
    distance = effective_entry - plan.stop_loss
    return 0.0 if distance <= 0 else round((price - effective_entry) / distance, 4)


def _entry_fill_price(plan: HistoricalTradePlan, bar_open: float, cfg: BacktestExecutionConfig) -> float:
    if cfg.model_entry_gaps and bar_open > plan.entry_trigger:
        return bar_open
    return plan.entry_trigger


def _stop_fill_price(plan: HistoricalTradePlan, bar_open: float, cfg: BacktestExecutionConfig) -> float:
    if cfg.model_stop_gaps and bar_open < plan.stop_loss:
        return bar_open
    return plan.stop_loss


def _effective_stop_fill_price(
    *,
    plan: HistoricalTradePlan,
    bar_open: float,
    effective_stop: float,
    cfg: BacktestExecutionConfig,
) -> float:
    if cfg.model_stop_gaps and bar_open < effective_stop:
        return bar_open
    return effective_stop


def simulate_plan(
    plan: HistoricalTradePlan,
    bars: pd.DataFrame,
    *,
    max_bars: int = 20,
    cfg: BacktestExecutionConfig = BacktestExecutionConfig(),
    signal_day_cluster_size: int | None = None,
) -> HistoricalBacktestResult:
    if plan.stop_model not in SUPPORTED_STOP_MODELS:
        raise ValueError(f"unsupported stop_model: {plan.stop_model!r}")
    if plan.exit_model not in SUPPORTED_EXIT_MODELS:
        raise ValueError(f"unsupported exit_model: {plan.exit_model!r}")

    breakeven_after_t1 = plan.stop_model == "breakeven_after_t1"
    t1_only = plan.exit_model == "t1_only"

    future = bars[bars["date"] > plan.signal_date]
    if plan.valid_until:
        future = future[future["date"] <= plan.valid_until]
    else:
        future = future.head(max_bars)
    future = future.reset_index(drop=True)

    entered = False
    t1 = False
    entry_date: str | None = None
    entry_fill_price: float | None = None
    entry_index: int | None = None

    def enriched(count: int, same_bar_ambiguous: bool = False) -> dict[str, Any]:
        observed = future.iloc[entry_index:count] if entry_index is not None else pd.DataFrame()
        return _enriched_result_fields(
            plan,
            entry_price=entry_fill_price,
            observed_bars=observed,
            same_bar_ambiguous=same_bar_ambiguous,
            signal_day_cluster_size=signal_day_cluster_size,
        )

    for index, row in future.iterrows():
        current_date = str(row["date"])
        bar_open = float(row["open"])
        high = float(row["high"])
        low = float(row["low"])
        count = index + 1
        effective_stop = (entry_fill_price or plan.entry_trigger) if (t1 and breakeven_after_t1) else plan.stop_loss

        if not entered and high >= plan.entry_trigger:
            entered = True
            entry_date = current_date
            entry_index = index
            entry_fill_price = _entry_fill_price(plan, bar_open, cfg)
            same_bar_ambiguous = low <= plan.stop_loss and high >= plan.target_1
            if cfg.same_bar_stop_first and low <= plan.stop_loss:
                fill = _stop_fill_price(plan, bar_open, cfg)
                return _result(
                    plan,
                    outcome=OUTCOME_STOP_HIT,
                    entry_hit=True,
                    target_1_hit=False,
                    target_2_hit=False,
                    stop_hit=True,
                    false_breakout=True,
                    entry_date=entry_date,
                    exit_date=current_date,
                    exit_price=fill,
                    r_multiple=_r(plan, fill, entry_fill_price),
                    bars_evaluated=count,
                    reason="same_bar_stop_first",
                    **enriched(count, same_bar_ambiguous=same_bar_ambiguous),
                )
            if high >= plan.target_1:
                t1 = True
                if t1_only:
                    return _result(
                        plan,
                        outcome=OUTCOME_TARGET_1_HIT,
                        entry_hit=True,
                        target_1_hit=True,
                        target_2_hit=False,
                        stop_hit=False,
                        false_breakout=False,
                        entry_date=entry_date,
                        exit_date=current_date,
                        exit_price=plan.target_1,
                        r_multiple=_r(plan, plan.target_1, entry_fill_price),
                        bars_evaluated=count,
                        reason="target_1_only_exit",
                        **enriched(count, same_bar_ambiguous=same_bar_ambiguous),
                    )
                if plan.target_2 and high >= plan.target_2:
                    return _result(
                        plan,
                        outcome=OUTCOME_TARGET_2_HIT,
                        entry_hit=True,
                        target_1_hit=True,
                        target_2_hit=True,
                        stop_hit=False,
                        false_breakout=False,
                        entry_date=entry_date,
                        exit_date=current_date,
                        exit_price=plan.target_2,
                        r_multiple=_r(plan, plan.target_2, entry_fill_price),
                        bars_evaluated=count,
                        reason="target_2_hit",
                        **enriched(count, same_bar_ambiguous=same_bar_ambiguous),
                    )
            continue

        if entered:
            if low <= effective_stop:
                fill = _effective_stop_fill_price(plan=plan, bar_open=bar_open, effective_stop=effective_stop, cfg=cfg)
                return _result(
                    plan,
                    outcome=OUTCOME_STOP_HIT,
                    entry_hit=True,
                    target_1_hit=t1,
                    target_2_hit=False,
                    stop_hit=True,
                    false_breakout=not t1,
                    entry_date=entry_date,
                    exit_date=current_date,
                    exit_price=fill,
                    r_multiple=_r(plan, fill, entry_fill_price),
                    bars_evaluated=count,
                    reason="breakeven_stop_after_t1" if (t1 and breakeven_after_t1) else "stop_hit",
                    **enriched(count),
                )
            if high >= plan.target_1 and not t1:
                t1 = True
                if t1_only:
                    return _result(
                        plan,
                        outcome=OUTCOME_TARGET_1_HIT,
                        entry_hit=True,
                        target_1_hit=True,
                        target_2_hit=False,
                        stop_hit=False,
                        false_breakout=False,
                        entry_date=entry_date,
                        exit_date=current_date,
                        exit_price=plan.target_1,
                        r_multiple=_r(plan, plan.target_1, entry_fill_price),
                        bars_evaluated=count,
                        reason="target_1_only_exit",
                        **enriched(count),
                    )
            if t1 and not t1_only and plan.target_2 and high >= plan.target_2:
                return _result(
                    plan,
                    outcome=OUTCOME_TARGET_2_HIT,
                    entry_hit=True,
                    target_1_hit=True,
                    target_2_hit=True,
                    stop_hit=False,
                    false_breakout=False,
                    entry_date=entry_date,
                    exit_date=current_date,
                    exit_price=plan.target_2,
                    r_multiple=_r(plan, plan.target_2, entry_fill_price),
                    bars_evaluated=count,
                    reason="target_2_hit",
                    **enriched(count),
                )

    if not entered:
        return _result(
            plan,
            outcome=OUTCOME_EXPIRED if plan.valid_until else OUTCOME_ENTRY_NOT_HIT,
            entry_hit=False,
            target_1_hit=False,
            target_2_hit=False,
            stop_hit=False,
            false_breakout=False,
            bars_evaluated=len(future),
            reason="entry_not_hit",
            signal_day_cluster_size=signal_day_cluster_size,
        )

    close = float(future.iloc[-1]["close"]) if not future.empty else (entry_fill_price or plan.entry_trigger)
    if t1 and plan.exit_model != "t1_t2":
        return _result(
            plan,
            outcome=OUTCOME_TARGET_1_HIT,
            entry_hit=True,
            target_1_hit=True,
            target_2_hit=False,
            stop_hit=False,
            false_breakout=False,
            entry_date=entry_date,
            exit_date=entry_date,
            exit_price=plan.target_1,
            r_multiple=_r(plan, plan.target_1, entry_fill_price),
            bars_evaluated=len(future),
            reason="target_1_only",
            **enriched(len(future)),
        )
    if t1:
        return _result(
            plan,
            outcome=OUTCOME_EXPIRED,
            entry_hit=True,
            target_1_hit=True,
            target_2_hit=False,
            stop_hit=False,
            false_breakout=False,
            entry_date=entry_date,
            exit_date=str(future.iloc[-1]["date"]) if not future.empty else entry_date,
            exit_price=close,
            r_multiple=_r(plan, close, entry_fill_price),
            bars_evaluated=len(future),
            reason="expired_after_target_1_without_target_2",
            **enriched(len(future)),
        )
    return _result(
        plan,
        outcome=OUTCOME_EXPIRED,
        entry_hit=True,
        target_1_hit=False,
        target_2_hit=False,
        stop_hit=False,
        false_breakout=True,
        entry_date=entry_date,
        exit_date=str(future.iloc[-1]["date"]) if not future.empty else entry_date,
        exit_price=close,
        r_multiple=_r(plan, close, entry_fill_price),
        bars_evaluated=len(future),
        reason="no_exit_level_hit",
        **enriched(len(future)),
    )


def calculate_metrics(results: list[HistoricalBacktestResult]) -> HistoricalBacktestMetrics:
    total = len(results)
    if total == 0:
        return HistoricalBacktestMetrics(0, 0, 0, 0, 0, 0, 0, 0, 0)
    rate = lambda fn: round(sum(1 for item in results if fn(item)) / total, 4)
    avg_r = round(sum(item.r_multiple for item in results) / total, 4)
    return HistoricalBacktestMetrics(total=total, entry_hit_rate=rate(lambda item: item.entry_hit), expired_without_entry_rate=rate(lambda item: not item.entry_hit), stop_hit_rate=rate(lambda item: item.stop_hit), target_1_hit_rate=rate(lambda item: item.target_1_hit), target_2_hit_rate=rate(lambda item: item.target_2_hit), false_breakout_rate=rate(lambda item: item.false_breakout), average_r=avg_r, expectancy_r=avg_r)


def _date_range(results: list[HistoricalBacktestResult], plans: list[HistoricalTradePlan]) -> dict[str, str]:
    dates = [plan.signal_date for plan in plans]
    dates.extend(result.exit_date for result in results if result.exit_date)
    dates = sorted(date for date in dates if date)
    return {"start": dates[0], "end": dates[-1]} if dates else {}


def _derive_backtest_input_health(
    *,
    load_report: HistoricalTradePlanLoadReport,
    results: list[HistoricalBacktestResult],
    input_pack_gate_status: str,
    is_demo: bool,
) -> tuple[str, str]:
    if input_pack_gate_status == "FAILED":
        return "FAILED", "FAILED"
    if load_report.input_plan_count <= 0 or load_report.accepted_plan_count <= 0 or not results:
        return "EMPTY_INPUT", "EMPTY_INPUT"
    if is_demo:
        return "OK", "FALLBACK_ACTIVE"
    if load_report.rejected_plan_count > 0:
        return "DEGRADED_DATA", "DEGRADED_DATA"
    return "OK", "OK"


def _signal_day_cluster_sizes(plans: list[HistoricalTradePlan]) -> dict[tuple[str, str], int]:
    counts: dict[tuple[str, str], int] = {}
    for plan in plans:
        key = (plan.symbol, plan.signal_date)
        counts[key] = counts.get(key, 0) + 1
    return counts


def run_backtest(
    plans: list[HistoricalTradePlan],
    *,
    bars_root: Path,
    max_bars: int = 20,
    cfg: BacktestExecutionConfig = BacktestExecutionConfig(),
    run_id: str = "historical-demo-run",
    data_source: str = "historical_demo",
    is_demo: bool = True,
    strategy_version: str = "historical-entry-exit-v1",
    tags: list[str] | None = None,
    input_pack_gate_status: str = "NOT_RUN",
    coverage_manifest_path: str = "",
    survivorship_universe_path: str = "",
    trade_plans_path: str = "",
    plan_load_report: HistoricalTradePlanLoadReport | None = None,
) -> HistoricalBacktestReport:
    cache: dict[str, pd.DataFrame] = {}
    results: list[HistoricalBacktestResult] = []
    cluster_sizes = _signal_day_cluster_sizes(plans)
    for plan in plans:
        if plan.symbol not in cache:
            cache[plan.symbol] = load_historical_bars(bars_root / f"{plan.symbol}.csv")
        results.append(
            simulate_plan(
                plan,
                cache[plan.symbol],
                max_bars=max_bars,
                cfg=cfg,
                signal_day_cluster_size=cluster_sizes.get((plan.symbol, plan.signal_date)),
            )
        )

    load_report = plan_load_report or HistoricalTradePlanLoadReport(
        input_plan_count=len(plans),
        accepted_plan_count=len(plans),
        rejected_plan_count=0,
        rejection_reasons=[],
    )
    input_completeness_status, run_health_status = _derive_backtest_input_health(
        load_report=load_report,
        results=results,
        input_pack_gate_status=input_pack_gate_status,
        is_demo=is_demo,
    )

    return HistoricalBacktestReport(
        metrics=calculate_metrics(results),
        results=results,
        run_id=run_id,
        data_source=data_source,
        is_demo=is_demo,
        symbol_universe=sorted({plan.symbol for plan in plans}),
        date_range=_date_range(results, plans),
        strategy_version=strategy_version,
        tags=tags or (["demo", "public_safe", "research_only"] if is_demo else ["real_data", "research_only"]),
        input_pack_gate_status=input_pack_gate_status,
        input_completeness_status=input_completeness_status,
        run_health_status=run_health_status,
        coverage_manifest_path=coverage_manifest_path,
        survivorship_universe_path=survivorship_universe_path,
        trade_plans_path=trade_plans_path,
        input_plan_count=load_report.input_plan_count,
        accepted_plan_count=load_report.accepted_plan_count,
        rejected_plan_count=load_report.rejected_plan_count,
        rejection_reasons=[rejection.to_dict() for rejection in load_report.rejection_reasons],
    )
