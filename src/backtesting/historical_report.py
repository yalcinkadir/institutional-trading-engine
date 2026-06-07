"""Report rendering for historical backtests."""

from __future__ import annotations

import json
from pathlib import Path

from src.backtesting.historical_models import HistoricalBacktestReport


def render_markdown(report: HistoricalBacktestReport) -> str:
    metrics = report.metrics
    lines = [
        "# Historical Entry / Stop / Exit Backtest",
        "",
        "## Evidence Pack",
        "",
        f"- Run ID: {report.run_id}",
        f"- Data source: {report.data_source}",
        f"- Is demo: {report.is_demo}",
        f"- Strategy version: {report.strategy_version}",
        f"- Input pack gate status: {report.input_pack_gate_status}",
        f"- Input completeness status: {report.input_completeness_status}",
        f"- Run health status: {report.run_health_status}",
        f"- Coverage manifest: {report.coverage_manifest_path}",
        f"- Survivorship universe: {report.survivorship_universe_path}",
        f"- Trade plans: {report.trade_plans_path}",
        f"- Input plans: {report.input_plan_count}",
        f"- Accepted plans: {report.accepted_plan_count}",
        f"- Rejected plans: {report.rejected_plan_count}",
        f"- Live trading authorized: {report.live_trading_authorized}",
        f"- Broker execution mode: {report.broker_execution_mode}",
        "",
        "## Metrics",
        "",
        f"- Total plans: {metrics.total}",
        f"- Entry hit rate: {metrics.entry_hit_rate:.2%}",
        f"- Expired without entry rate: {metrics.expired_without_entry_rate:.2%}",
        f"- Stop hit rate: {metrics.stop_hit_rate:.2%}",
        f"- Target 1 hit rate: {metrics.target_1_hit_rate:.2%}",
        f"- Target 2 hit rate: {metrics.target_2_hit_rate:.2%}",
        f"- False breakout rate: {metrics.false_breakout_rate:.2%}",
        f"- Average R: {metrics.average_r:.4f}",
        f"- Expectancy R: {metrics.expectancy_r:.4f}",
        "",
        "## Rejected Trade Plans",
        "",
    ]
    if report.rejection_reasons:
        lines.extend(["| Index | Signal | Symbol | Reasons |", "|---:|---|---|---|"])
        for rejection in report.rejection_reasons:
            lines.append(
                f"| {rejection.get('plan_index')} | {rejection.get('signal_id') or ''} | "
                f"{rejection.get('symbol') or ''} | {', '.join(rejection.get('reasons', []))} |"
            )
    else:
        lines.append("No rejected trade plans.")
    lines.extend(
        [
            "",
            "## Results",
            "",
            "| Signal | Symbol | Date | Outcome | R | Reason |",
            "|---|---|---:|---|---:|---|",
        ]
    )
    for result in report.results:
        lines.append(
            f"| {result.signal_id} | {result.symbol} | {result.signal_date} | "
            f"{result.outcome} | {result.r_multiple:.4f} | {result.reason} |"
        )
    return "\n".join(lines) + "\n"


def write_report(report: HistoricalBacktestReport, *, json_path: Path, markdown_path: Path) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report.to_dict(), indent=2), encoding="utf-8")
    markdown_path.write_text(render_markdown(report), encoding="utf-8")
