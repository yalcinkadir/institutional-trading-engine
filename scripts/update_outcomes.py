#!/usr/bin/env python3
"""Update decision outcomes and generate an expectancy report.

Usage:
    python scripts/update_outcomes.py \
      --decision-log data/decision_log.csv \
      --output reports/expectancy-report.md
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.data.polygon_client import PolygonClient
from src.outcome_pipeline import build_expectancy_summary, update_outcomes
from src.outcome_tracking import read_decision_records


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Update outcome metrics for stored decisions.")
    parser.add_argument(
        "--decision-log",
        default="data/decision_log.csv",
        help="Path to the persistent decision log CSV.",
    )
    parser.add_argument(
        "--output",
        default="reports/expectancy-report.md",
        help="Markdown output path for the expectancy summary.",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=120,
        help="Number of daily bars to load per symbol.",
    )
    return parser.parse_args()


def _format_profile_table(title: str, profiles: list[dict]) -> list[str]:
    lines: list[str] = []
    lines.append(f"## {title}")
    lines.append("")

    if not profiles:
        lines.append("No evaluated profiles yet.")
        lines.append("")
        return lines

    lines.append("| Key | Trades | Win Rate | Avg Result | Expectancy | Confidence | Recommendation |")
    lines.append("|---|---:|---:|---:|---:|---:|---|")

    for profile in profiles[:15]:
        lines.append(
            "| {key} | {trades} | {win_rate} | {average_result} | {expectancy} | {confidence} | {recommendation} |".format(
                **profile
            )
        )

    lines.append("")
    return lines


def write_expectancy_report(summary: dict, output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    lines: list[str] = []
    lines.append("# Adaptive Expectancy Report")
    lines.append("")
    lines.append("This report evaluates historical Decision Engine outcomes by setup, regime and setup-regime combination.")
    lines.append("")

    lines.append("## Strongest Edges")
    if summary["strongest_edges"]:
        for edge in summary["strongest_edges"]:
            lines.append(f"- {edge}")
    else:
        lines.append("- Insufficient evaluated data.")
    lines.append("")

    lines.append("## Weakest Edges")
    if summary["weakest_edges"]:
        for edge in summary["weakest_edges"]:
            lines.append(f"- {edge}")
    else:
        lines.append("- Insufficient evaluated data.")
    lines.append("")

    lines.extend(_format_profile_table("Setup Profiles", summary["setup_profiles"]))
    lines.extend(_format_profile_table("Regime Profiles", summary["regime_profiles"]))
    lines.extend(_format_profile_table("Combined Setup-Regime Profiles", summary["combined_profiles"]))

    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def main() -> int:
    args = parse_args()
    decision_log = Path(args.decision_log)

    records = read_decision_records(decision_log)
    if not records:
        print(f"No decision records found at {decision_log}. Nothing to update.")
        summary = build_expectancy_summary(decision_log)
        output = write_expectancy_report(summary, args.output)
        print(f"Expectancy report written to {output}")
        return 0

    symbols = sorted({record["symbol"] for record in records if record.get("symbol")})
    client = PolygonClient()

    bars_by_symbol = {}
    for symbol in symbols:
        try:
            bars_by_symbol[symbol] = client.get_daily_bars(symbol, days=args.days)
        except Exception as exc:
            print(f"WARNING: Could not load bars for {symbol}: {type(exc).__name__}: {exc}")
            bars_by_symbol[symbol] = []

    update_outcomes(path=decision_log, bars_by_symbol=bars_by_symbol)
    summary = build_expectancy_summary(decision_log)
    output = write_expectancy_report(summary, args.output)

    print(f"Updated outcomes for {len(records)} records.")
    print(f"Expectancy report written to {output}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
