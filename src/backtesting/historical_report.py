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
        "## Results",
        "",
        "| Signal | Symbol | Date | Outcome | R | Reason |",
        "|---|---|---:|---|---:|---|",
    ]
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
