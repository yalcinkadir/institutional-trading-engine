from __future__ import annotations

import json
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from src.validation.historical_edge_validation import coerce_finite_float

BT135_REQUIRED_FIELDS = {"symbol", "date", "period", "r", "signal_day"}
BT135_PERIODS = ("training", "validation", "out_of_sample")
BT135_ALLOWED_RECOMMENDATIONS = {
    "KEEP_FULL_UNIVERSE",
    "PROMOTE_TO_GUARDED_EXPERIMENT",
    "NEEDS_MORE_DATA",
    "REJECT_EXCLUSION",
    "OVERFIT_RISK",
}
MIN_TRADES_PER_SYMBOL = 10
MIN_SIGNAL_DAY_CLUSTERS = 10


def _missing_fields(record: dict[str, Any]) -> list[str]:
    missing = [
        field
        for field in sorted(BT135_REQUIRED_FIELDS)
        if record.get(field) in {None, ""}
    ]
    if "r" not in missing and coerce_finite_float(record.get("r")) is None:
        missing.append("r")
    return sorted(set(missing))


def _period(record: dict[str, Any], index: int, total: int) -> str:
    explicit = str(record.get("period") or "").strip()
    if explicit in BT135_PERIODS:
        return explicit
    if total <= 1:
        return "out_of_sample"
    ratio = index / max(1, total - 1)
    if ratio < 0.6:
        return "training"
    if ratio < 0.8:
        return "validation"
    return "out_of_sample"


def _symbol_stats(records: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        grouped[str(record["symbol"])].append(record)

    stats: dict[str, dict[str, Any]] = {}
    for symbol, rows in grouped.items():
        r_values = [float(coerce_finite_float(row["r"])) for row in rows]
        stats[symbol] = {
            "trades": len(rows),
            "expectancy_r": round(sum(r_values) / len(r_values), 6) if r_values else 0.0,
            "signal_day_clusters": len({str(row.get("signal_day")) for row in rows}),
        }
    return stats


def _base_variants(stats: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    symbols = sorted(stats)
    ranked = sorted(symbols, key=lambda item: stats[item]["expectancy_r"])
    worst = ranked[0] if ranked else None
    best = ranked[-1] if ranked else None
    negative = [
        symbol for symbol in symbols
        if float(stats[symbol]["expectancy_r"]) < 0
    ]

    variants = [
        {
            "variant": "baseline_full_universe",
            "group": "baseline",
            "symbols_included": symbols,
            "symbols_excluded": [],
            "weights": {symbol: 1.0 for symbol in symbols},
            "downweight_level": None,
        },
        {
            "variant": "exclude_worst_symbol_only",
            "group": "exclude_worst",
            "symbols_included": [symbol for symbol in symbols if symbol != worst],
            "symbols_excluded": [worst] if worst else [],
            "weights": {symbol: 1.0 for symbol in symbols if symbol != worst},
            "downweight_level": None,
        },
        {
            "variant": "exclude_negative_expectancy_symbols",
            "group": "exclude_negative",
            "symbols_included": [symbol for symbol in symbols if symbol not in negative],
            "symbols_excluded": negative,
            "weights": {symbol: 1.0 for symbol in symbols if symbol not in negative},
            "downweight_level": None,
        },
        {
            "variant": "best_symbol_only_sanity_check",
            "group": "best_symbol_only",
            "symbols_included": [best] if best else [],
            "symbols_excluded": [symbol for symbol in symbols if symbol != best],
            "weights": {best: 1.0} if best else {},
            "downweight_level": None,
        },
    ]

    for level in (0.25, 0.50, 0.75):
        weights = {symbol: (level if symbol == worst else 1.0) for symbol in symbols}
        variants.append(
            {
                "variant": f"downweight_worst_symbols_{level:.2f}x",
                "group": "downweight_worst_symbols",
                "symbols_included": symbols,
                "symbols_excluded": [],
                "weights": weights,
                "downweight_level": level,
            }
        )

    return variants


def _period_result(
    records: list[dict[str, Any]],
    variant: dict[str, Any],
    period: str,
) -> dict[str, Any]:
    included = set(variant["symbols_included"])
    rows = [
        row for row in records
        if _period(row, 0, 1) == period and str(row["symbol"]) in included
    ]

    weighted_r: list[float] = []
    stop_count = 0
    target_count = 0
    false_breakout_count = 0

    for row in rows:
        weight = float(variant["weights"].get(str(row["symbol"]), 0.0))
        r_value = float(coerce_finite_float(row["r"])) * weight
        weighted_r.append(r_value)

        outcome = str(row.get("outcome") or "").lower()
        if r_value < 0 or outcome in {"loss", "stop"}:
            stop_count += 1
        if r_value > 0 or outcome in {"win", "target_1", "target_2"}:
            target_count += 1
        if r_value < 0 and outcome in {"loss", "stop", "false_breakout"}:
            false_breakout_count += 1

    denominator = len(rows) or 1
    average_r = sum(weighted_r) / denominator if rows else 0.0

    return {
        "period": period,
        "symbols_included": sorted(included),
        "symbols_excluded": sorted(set(variant["symbols_excluded"])),
        "total_trades": len(rows),
        "expectancy_r": round(average_r, 6),
        "average_r": round(average_r, 6),
        "stop_rate": round(stop_count / denominator, 6),
        "target_rate": round(target_count / denominator, 6),
        "false_breakout_rate": round(false_breakout_count / denominator, 6),
    }


def _recommendation(
    period_results: list[dict[str, Any]],
    *,
    small_sample: bool,
    low_clusters: bool,
    variant: str,
) -> str:
    if small_sample or low_clusters:
        return "NEEDS_MORE_DATA"

    by_period = {item["period"]: item for item in period_results}
    training = float(by_period.get("training", {}).get("expectancy_r", 0.0))
    validation = float(by_period.get("validation", {}).get("expectancy_r", 0.0))
    oos = float(by_period.get("out_of_sample", {}).get("expectancy_r", 0.0))

    if variant == "baseline_full_universe":
        return "KEEP_FULL_UNIVERSE"
    if training > 0 and oos < 0:
        return "OVERFIT_RISK"
    if validation < 0 or oos < 0:
        return "REJECT_EXCLUSION"
    if validation >= 0 and oos > 0:
        return "PROMOTE_TO_GUARDED_EXPERIMENT"
    return "NEEDS_MORE_DATA"


def build_bt135_report(
    records: list[dict[str, Any]],
    *,
    github_run_id: str | None = None,
) -> dict[str, Any]:
    github_run_id = github_run_id or "local"

    all_missing: dict[str, list[str]] = {}
    for record in records:
        missing = _missing_fields(record)
        if missing:
            key = str(record.get("symbol") or record.get("date") or len(all_missing))
            all_missing[key] = missing

    if all_missing:
        return {
            "schema": "bt135_symbol_selection_sensitivity_report.v1",
            "status": "SKIPPED_INSUFFICIENT_FIELDS",
            "research_only": True,
            "broker_execution_mode": "paper_only",
            "production_rule_change": False,
            "github_run_id": github_run_id,
            "missing_fields": all_missing,
            "variant_results": [],
            "periods": list(BT135_PERIODS),
        }

    stats = _symbol_stats(records)
    small_sample = any(
        int(item["trades"]) < MIN_TRADES_PER_SYMBOL
        for item in stats.values()
    )
    cluster_count = len({str(row.get("signal_day")) for row in records})
    low_clusters = cluster_count < MIN_SIGNAL_DAY_CLUSTERS

    variant_results = []
    for variant in _base_variants(stats):
        period_results = [
            _period_result(records, variant, period)
            for period in BT135_PERIODS
        ]
        variant_results.append(
            {
                "variant": variant["variant"],
                "group": variant["group"],
                "downweight_level": variant["downweight_level"],
                "symbols_included": sorted(variant["symbols_included"]),
                "symbols_excluded": sorted(variant["symbols_excluded"]),
                "period_results": period_results,
                "recommendation": _recommendation(
                    period_results,
                    small_sample=small_sample,
                    low_clusters=low_clusters,
                    variant=variant["variant"],
                ),
            }
        )

    return {
        "schema": "bt135_symbol_selection_sensitivity_report.v1",
        "status": "COMPLETED",
        "generated_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
        "github_run_id": github_run_id,
        "research_only": True,
        "broker_execution_mode": "paper_only",
        "production_rule_change": False,
        "periods": list(BT135_PERIODS),
        "symbol_stats": stats,
        "concentration_risk_warning": small_sample,
        "low_effective_sample_size_warning": low_clusters,
        "effective_signal_day_clusters": cluster_count,
        "missing_fields": {},
        "variant_results": variant_results,
    }


def render_bt135_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# BT135 Symbol Selection Sensitivity Report",
        "",
        f"Status: {report.get('status')}",
        f"Research only: {report.get('research_only')}",
        f"Broker execution mode: {report.get('broker_execution_mode')}",
        f"Production rule change: {report.get('production_rule_change')}",
        f"Concentration risk warning: {report.get('concentration_risk_warning')}",
        f"Low effective sample warning: {report.get('low_effective_sample_size_warning')}",
        "",
    ]

    if report.get("missing_fields"):
        lines.extend(
            [
                "## Missing Fields",
                "",
                "```json",
                json.dumps(report["missing_fields"], indent=2, sort_keys=True),
                "```",
                "",
            ]
        )

    lines.extend(["## Variant Results", ""])

    for variant in report.get("variant_results", []):
        lines.append(f"### {variant['variant']} — {variant['recommendation']}")
        lines.append("")
        lines.append(
            "| Period | Trades | Expectancy R | Avg R | Stop Rate | Target Rate | False Breakout Rate |"
        )
        lines.append("|---|---:|---:|---:|---:|---:|---:|")

        for period in variant.get("period_results", []):
            lines.append(
                f"| {period['period']} | {period['total_trades']} | "
                f"{period['expectancy_r']:.4f} | "
                f"{period['average_r']:.4f} | "
                f"{period['stop_rate']:.2%} | "
                f"{period['target_rate']:.2%} | "
                f"{period['false_breakout_rate']:.2%} |"
            )
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def persist_bt135_report(
    report: dict[str, Any],
    *,
    output_root: Path = Path("reports/backtests/real_data"),
    github_run_id: str | None = None,
) -> dict[str, Path]:
    run_id = github_run_id or str(report.get("github_run_id") or "local")
    latest_dir = output_root / "latest"
    run_dir = output_root / "runs" / run_id

    latest_dir.mkdir(parents=True, exist_ok=True)
    run_dir.mkdir(parents=True, exist_ok=True)

    latest_json = latest_dir / "bt135-symbol-selection-sensitivity-report.json"
    latest_markdown = latest_dir / "bt135-symbol-selection-sensitivity-report.md"
    run_json = run_dir / "bt135-symbol-selection-sensitivity-report.json"
    run_markdown = run_dir / "bt135-symbol-selection-sensitivity-report.md"

    payload = json.dumps(report, indent=2, sort_keys=True)
    markdown = render_bt135_markdown(report)

    for path in [latest_json, run_json]:
        path.write_text(payload, encoding="utf-8")
    for path in [latest_markdown, run_markdown]:
        path.write_text(markdown, encoding="utf-8")

    return {
        "latest_json": latest_json,
        "latest_markdown": latest_markdown,
        "run_json": run_json,
        "run_markdown": run_markdown,
    }