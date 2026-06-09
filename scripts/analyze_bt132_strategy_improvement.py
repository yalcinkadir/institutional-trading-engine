#!/usr/bin/env python3
"""Analyze BT131 evidence and produce BT132 strategy-improvement reports.

BT132 is intentionally report-only. It does not change entry/exit/stop rules.
It converts validated real-data backtest evidence into reviewable findings that
can drive the next evidence-oriented improvement cycle.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from statistics import mean
from typing import Any


@dataclass(frozen=True)
class SymbolStats:
    symbol: str
    total: int
    average_r: float
    expectancy_r: float
    entry_hit_rate: float
    stop_hit_rate: float
    target_1_hit_rate: float
    target_2_hit_rate: float
    false_breakout_rate: float


@dataclass(frozen=True)
class BT132Report:
    report_version: str
    source_evidence: str
    run_id: str
    data_source: str
    is_demo: bool
    input_pack_gate_status: str
    input_completeness_status: str
    run_health_status: str
    total_trades: int
    portfolio_metrics: dict[str, Any]
    best_symbols_by_expectancy: list[dict[str, Any]]
    worst_symbols_by_expectancy: list[dict[str, Any]]
    stop_loss_findings: dict[str, Any]
    entry_findings: dict[str, Any]
    exit_findings: dict[str, Any]
    false_breakout_findings: dict[str, Any]
    recommendations: list[dict[str, Any]]
    review_status: str


def _rate(count: int, total: int) -> float:
    return round(count / total, 4) if total else 0.0


def _avg(values: list[float]) -> float:
    return round(mean(values), 4) if values else 0.0


def _load_evidence(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise SystemExit("BT132 source evidence must be a JSON object")
    if payload.get("data_source") != "real_data":
        raise SystemExit("BT132 requires data_source=real_data")
    if payload.get("is_demo") is not False:
        raise SystemExit("BT132 refuses demo evidence")
    if payload.get("input_pack_gate_status") != "PASSED":
        raise SystemExit("BT132 requires input_pack_gate_status=PASSED")
    if payload.get("run_health_status") != "OK":
        raise SystemExit("BT132 requires run_health_status=OK")
    return payload


def _symbol_stats(results: list[dict[str, Any]]) -> list[SymbolStats]:
    by_symbol: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in results:
        by_symbol[str(row.get("symbol") or "UNKNOWN")].append(row)

    stats: list[SymbolStats] = []
    for symbol, rows in sorted(by_symbol.items()):
        total = len(rows)
        r_values = [float(row.get("r_multiple") or 0.0) for row in rows]
        stats.append(
            SymbolStats(
                symbol=symbol,
                total=total,
                average_r=_avg(r_values),
                expectancy_r=_avg(r_values),
                entry_hit_rate=_rate(sum(bool(row.get("entry_hit")) for row in rows), total),
                stop_hit_rate=_rate(sum(bool(row.get("stop_hit")) for row in rows), total),
                target_1_hit_rate=_rate(sum(bool(row.get("target_1_hit")) for row in rows), total),
                target_2_hit_rate=_rate(sum(bool(row.get("target_2_hit")) for row in rows), total),
                false_breakout_rate=_rate(sum(bool(row.get("false_breakout")) for row in rows), total),
            )
        )
    return stats


def _top_problem_rows(results: list[dict[str, Any]], *, predicate: str, limit: int = 10) -> list[dict[str, Any]]:
    if predicate == "stop_hit":
        filtered = [row for row in results if bool(row.get("stop_hit"))]
    elif predicate == "false_breakout":
        filtered = [row for row in results if bool(row.get("false_breakout"))]
    elif predicate == "entry_not_hit":
        filtered = [row for row in results if not bool(row.get("entry_hit"))]
    elif predicate == "target1_without_target2":
        filtered = [row for row in results if bool(row.get("target_1_hit")) and not bool(row.get("target_2_hit"))]
    else:
        filtered = []

    filtered = sorted(filtered, key=lambda row: (float(row.get("r_multiple") or 0.0), str(row.get("symbol") or "")))
    return [
        {
            "signal_id": row.get("signal_id"),
            "symbol": row.get("symbol"),
            "signal_date": row.get("signal_date"),
            "outcome": row.get("outcome"),
            "r_multiple": row.get("r_multiple"),
            "reason": row.get("reason"),
            "bars_evaluated": row.get("bars_evaluated"),
        }
        for row in filtered[:limit]
    ]


def analyze(evidence_path: Path) -> BT132Report:
    evidence = _load_evidence(evidence_path)
    results = evidence.get("results")
    if not isinstance(results, list) or not results:
        raise SystemExit("BT132 requires non-empty results")

    total = len(results)
    stats = _symbol_stats(results)
    best = sorted(stats, key=lambda item: item.expectancy_r, reverse=True)
    worst = sorted(stats, key=lambda item: item.expectancy_r)
    outcomes = Counter(str(row.get("outcome") or "UNKNOWN") for row in results)
    reasons = Counter(str(row.get("reason") or "UNKNOWN") for row in results)

    stop_hits = sum(bool(row.get("stop_hit")) for row in results)
    false_breakouts = sum(bool(row.get("false_breakout")) for row in results)
    entry_not_hit = sum(not bool(row.get("entry_hit")) for row in results)
    target1_without_target2 = sum(bool(row.get("target_1_hit")) and not bool(row.get("target_2_hit")) for row in results)
    target2_hits = sum(bool(row.get("target_2_hit")) for row in results)

    recommendations: list[dict[str, Any]] = []
    if _rate(false_breakouts, total) >= 0.35:
        recommendations.append(
            {
                "area": "entry",
                "priority": "HIGH",
                "finding": "False-breakout rate is elevated.",
                "next_test": "Compare current breakout trigger against stricter confirmation variants before changing production rules.",
            }
        )
    if _rate(stop_hits, total) >= 0.4:
        recommendations.append(
            {
                "area": "stop_loss",
                "priority": "HIGH",
                "finding": "Stop-hit rate is elevated.",
                "next_test": "Run a guarded comparison of fixed stop vs wider ATR-based stop and same-bar stop handling.",
            }
        )
    if target1_without_target2 > target2_hits:
        recommendations.append(
            {
                "area": "exit",
                "priority": "MEDIUM",
                "finding": "More trades reach target 1 without target 2 than full target-2 completions.",
                "next_test": "Compare full target-2 exit with partial profit at target 1 plus trailing remainder.",
            }
        )
    if worst and worst[0].expectancy_r < 0:
        recommendations.append(
            {
                "area": "symbol_selection",
                "priority": "MEDIUM",
                "finding": f"Worst symbol by expectancy is {worst[0].symbol}.",
                "next_test": "Run symbol-level exclusion/sizing sensitivity before excluding any symbol.",
            }
        )
    if not recommendations:
        recommendations.append(
            {
                "area": "monitoring",
                "priority": "LOW",
                "finding": "No high-priority degradation detected in current small sample.",
                "next_test": "Accumulate more real-data runs before changing rules.",
            }
        )

    return BT132Report(
        report_version="bt132.v1",
        source_evidence=str(evidence_path),
        run_id=str(evidence.get("run_id")),
        data_source=str(evidence.get("data_source")),
        is_demo=bool(evidence.get("is_demo")),
        input_pack_gate_status=str(evidence.get("input_pack_gate_status")),
        input_completeness_status=str(evidence.get("input_completeness_status")),
        run_health_status=str(evidence.get("run_health_status")),
        total_trades=total,
        portfolio_metrics={
            **dict(evidence.get("metrics") or {}),
            "outcomes": dict(outcomes),
            "reasons": dict(reasons),
        },
        best_symbols_by_expectancy=[asdict(item) for item in best[:5]],
        worst_symbols_by_expectancy=[asdict(item) for item in worst[:5]],
        stop_loss_findings={
            "stop_hit_count": stop_hits,
            "stop_hit_rate": _rate(stop_hits, total),
            "problem_examples": _top_problem_rows(results, predicate="stop_hit"),
        },
        entry_findings={
            "entry_not_hit_count": entry_not_hit,
            "entry_not_hit_rate": _rate(entry_not_hit, total),
            "false_breakout_count": false_breakouts,
            "false_breakout_rate": _rate(false_breakouts, total),
            "false_breakout_examples": _top_problem_rows(results, predicate="false_breakout"),
            "entry_not_hit_examples": _top_problem_rows(results, predicate="entry_not_hit"),
        },
        exit_findings={
            "target_1_without_target_2_count": target1_without_target2,
            "target_1_without_target_2_rate": _rate(target1_without_target2, total),
            "target_2_hit_count": target2_hits,
            "target_2_hit_rate": _rate(target2_hits, total),
            "target_1_without_target_2_examples": _top_problem_rows(results, predicate="target1_without_target2"),
        },
        false_breakout_findings={
            "false_breakout_count": false_breakouts,
            "false_breakout_rate": _rate(false_breakouts, total),
            "by_symbol": [asdict(item) for item in sorted(stats, key=lambda item: item.false_breakout_rate, reverse=True)],
        },
        recommendations=recommendations,
        review_status="READY_FOR_REVIEW",
    )


def _markdown_table(headers: list[str], rows: list[list[Any]]) -> list[str]:
    lines = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    for row in rows:
        lines.append("| " + " | ".join(str(cell) for cell in row) + " |")
    return lines


def render_markdown(report: BT132Report) -> str:
    lines: list[str] = [
        "# BT132 Strategy Improvement Report",
        "",
        "## Evidence Contract",
        "",
        f"- Report version: {report.report_version}",
        f"- Source evidence: {report.source_evidence}",
        f"- Run ID: {report.run_id}",
        f"- Data source: {report.data_source}",
        f"- Is demo: {report.is_demo}",
        f"- Input pack gate: {report.input_pack_gate_status}",
        f"- Input completeness: {report.input_completeness_status}",
        f"- Run health: {report.run_health_status}",
        f"- Total trades: {report.total_trades}",
        f"- Review status: {report.review_status}",
        "",
        "## Portfolio Metrics",
        "",
    ]
    for key in ["expectancy_r", "average_r", "entry_hit_rate", "stop_hit_rate", "target_1_hit_rate", "target_2_hit_rate", "false_breakout_rate"]:
        if key in report.portfolio_metrics:
            lines.append(f"- {key}: {report.portfolio_metrics[key]}")

    lines.extend(["", "## Best Symbols by Expectancy", ""])
    lines.extend(
        _markdown_table(
            ["Symbol", "Trades", "Expectancy R", "Stop Rate", "T2 Rate", "False Breakout Rate"],
            [
                [row["symbol"], row["total"], row["expectancy_r"], row["stop_hit_rate"], row["target_2_hit_rate"], row["false_breakout_rate"]]
                for row in report.best_symbols_by_expectancy
            ],
        )
    )
    lines.extend(["", "## Worst Symbols by Expectancy", ""])
    lines.extend(
        _markdown_table(
            ["Symbol", "Trades", "Expectancy R", "Stop Rate", "T2 Rate", "False Breakout Rate"],
            [
                [row["symbol"], row["total"], row["expectancy_r"], row["stop_hit_rate"], row["target_2_hit_rate"], row["false_breakout_rate"]]
                for row in report.worst_symbols_by_expectancy
            ],
        )
    )
    lines.extend(
        [
            "",
            "## Entry Findings",
            "",
            f"- Entry not hit count: {report.entry_findings['entry_not_hit_count']}",
            f"- Entry not hit rate: {report.entry_findings['entry_not_hit_rate']}",
            f"- False breakout count: {report.entry_findings['false_breakout_count']}",
            f"- False breakout rate: {report.entry_findings['false_breakout_rate']}",
            "",
            "## Stop-Loss Findings",
            "",
            f"- Stop hit count: {report.stop_loss_findings['stop_hit_count']}",
            f"- Stop hit rate: {report.stop_loss_findings['stop_hit_rate']}",
            "",
            "## Exit Findings",
            "",
            f"- Target 1 without Target 2 count: {report.exit_findings['target_1_without_target_2_count']}",
            f"- Target 1 without Target 2 rate: {report.exit_findings['target_1_without_target_2_rate']}",
            f"- Target 2 hit count: {report.exit_findings['target_2_hit_count']}",
            f"- Target 2 hit rate: {report.exit_findings['target_2_hit_rate']}",
            "",
            "## Recommendations",
            "",
        ]
    )
    for item in report.recommendations:
        lines.extend(
            [
                f"### {item['priority']} - {item['area']}",
                "",
                f"- Finding: {item['finding']}",
                f"- Next test: {item['next_test']}",
                "",
            ]
        )
    lines.append("Research only. No live trading authorization.")
    return "\n".join(lines).rstrip() + "\n"


def write_report(report: BT132Report, *, output_json: Path, output_md: Path) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(asdict(report), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    output_md.write_text(render_markdown(report), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze BT131 evidence into BT132 strategy-improvement reports")
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = analyze(args.evidence)
    write_report(report, output_json=args.output_json, output_md=args.output_md)
    print(json.dumps({"status": report.review_status, "recommendations": len(report.recommendations)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
