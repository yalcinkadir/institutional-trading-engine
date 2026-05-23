"""Historical plan reconstruction and out-of-sample validation for P25."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from src.backtesting.historical_entry_exit_backtest import calculate_metrics, load_historical_bars, run_backtest
from src.backtesting.historical_models import HistoricalBacktestMetrics, HistoricalBacktestReport, HistoricalTradePlan


@dataclass(frozen=True)
class OutOfSampleValidationReport:
    split_date: str
    all_metrics: HistoricalBacktestMetrics
    in_sample_metrics: HistoricalBacktestMetrics
    out_of_sample_metrics: HistoricalBacktestMetrics
    reconstructed_plan_count: int
    in_sample_count: int
    out_of_sample_count: int

    def to_dict(self) -> dict:
        return asdict(self)


def reconstruct_breakout_plans_from_bars(
    *,
    symbol: str,
    bars_path: Path,
    lookback_bars: int = 20,
    every_nth_signal: int = 20,
    stop_pct: float = 0.05,
    target_1_r: float = 2.0,
    target_2_r: float = 4.0,
) -> list[HistoricalTradePlan]:
    """Create deterministic historical breakout-style plans from daily bars.

    For each selected historical day, the plan uses the previous lookback high as
    entry trigger. This is intentionally simple and reproducible. It is validation
    infrastructure, not a profitability claim.
    """
    if lookback_bars < 2:
        raise ValueError("lookback_bars must be >= 2")
    if every_nth_signal < 1:
        raise ValueError("every_nth_signal must be >= 1")
    if stop_pct <= 0 or stop_pct >= 1:
        raise ValueError("stop_pct must be between 0 and 1")

    bars = load_historical_bars(bars_path)
    plans: list[HistoricalTradePlan] = []
    symbol = symbol.upper()

    for index in range(lookback_bars, len(bars) - 1, every_nth_signal):
        history = bars.iloc[index - lookback_bars : index]
        signal_row = bars.iloc[index]
        entry = round(float(history["high"].max()), 4)
        stop = round(entry * (1 - stop_pct), 4)
        risk = entry - stop
        if risk <= 0:
            continue
        target_1 = round(entry + target_1_r * risk, 4)
        target_2 = round(entry + target_2_r * risk, 4)
        signal_date = str(signal_row["date"])
        plans.append(
            HistoricalTradePlan(
                signal_id=f"reconstructed_{symbol}_{signal_date}",
                symbol=symbol,
                signal_date=signal_date,
                entry_trigger=entry,
                stop_loss=stop,
                target_1=target_1,
                target_2=target_2,
                entry_type="historical_breakout_reconstruction",
                setup_type="p25_reconstructed_daily_breakout",
                stop_model="percentage_stop",
                exit_model="r_multiple_targets",
            )
        )
    return plans


def reconstruct_plans_for_symbols(
    *,
    symbols: list[str],
    bars_root: Path,
    lookback_bars: int = 20,
    every_nth_signal: int = 20,
    stop_pct: float = 0.05,
    target_1_r: float = 2.0,
    target_2_r: float = 4.0,
) -> list[HistoricalTradePlan]:
    plans: list[HistoricalTradePlan] = []
    for symbol in symbols:
        plans.extend(
            reconstruct_breakout_plans_from_bars(
                symbol=symbol,
                bars_path=bars_root / f"{symbol.upper()}.csv",
                lookback_bars=lookback_bars,
                every_nth_signal=every_nth_signal,
                stop_pct=stop_pct,
                target_1_r=target_1_r,
                target_2_r=target_2_r,
            )
        )
    return plans


def validate_out_of_sample(
    *,
    plans: list[HistoricalTradePlan],
    bars_root: Path,
    split_date: str,
    max_bars: int = 20,
) -> OutOfSampleValidationReport:
    backtest = run_backtest(plans, bars_root=bars_root, max_bars=max_bars)
    in_sample_results = [result for result in backtest.results if result.signal_date < split_date]
    out_of_sample_results = [result for result in backtest.results if result.signal_date >= split_date]
    return OutOfSampleValidationReport(
        split_date=split_date,
        all_metrics=backtest.metrics,
        in_sample_metrics=calculate_metrics(in_sample_results),
        out_of_sample_metrics=calculate_metrics(out_of_sample_results),
        reconstructed_plan_count=len(plans),
        in_sample_count=len(in_sample_results),
        out_of_sample_count=len(out_of_sample_results),
    )


def render_validation_markdown(report: OutOfSampleValidationReport) -> str:
    def rows(name: str, metrics: HistoricalBacktestMetrics) -> list[str]:
        return [
            f"| {name} | total | {metrics.total} |",
            f"| {name} | entry_hit_rate | {metrics.entry_hit_rate:.2%} |",
            f"| {name} | target_1_hit_rate | {metrics.target_1_hit_rate:.2%} |",
            f"| {name} | target_2_hit_rate | {metrics.target_2_hit_rate:.2%} |",
            f"| {name} | stop_hit_rate | {metrics.stop_hit_rate:.2%} |",
            f"| {name} | false_breakout_rate | {metrics.false_breakout_rate:.2%} |",
            f"| {name} | expectancy_r | {metrics.expectancy_r:.4f} |",
        ]

    lines = [
        "# Out-of-Sample Historical Validation",
        "",
        f"Split date: `{report.split_date}`",
        "",
        f"Reconstructed plans: {report.reconstructed_plan_count}",
        f"In-sample plans: {report.in_sample_count}",
        f"Out-of-sample plans: {report.out_of_sample_count}",
        "",
        "| Segment | Metric | Value |",
        "|---|---|---:|",
    ]
    lines.extend(rows("all", report.all_metrics))
    lines.extend(rows("in_sample", report.in_sample_metrics))
    lines.extend(rows("out_of_sample", report.out_of_sample_metrics))
    lines.extend(
        [
            "",
            "## Guardrail",
            "",
            "This report is validation evidence only. It does not change adaptive scoring and does not authorize trading.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_validation_report(report: OutOfSampleValidationReport, *, json_path: Path, markdown_path: Path) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report.to_dict(), indent=2), encoding="utf-8")
    markdown_path.write_text(render_validation_markdown(report), encoding="utf-8")


def write_reconstructed_plans(plans: list[HistoricalTradePlan], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"plans": [plan.__dict__ for plan in plans]}, indent=2), encoding="utf-8")
