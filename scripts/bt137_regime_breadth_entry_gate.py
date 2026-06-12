from __future__ import annotations

import json
from pathlib import Path
from typing import Any

BT137_ALLOWED_RECOMMENDATIONS = {
    "KEEP_BASELINE",
    "PROMOTE_TO_GUARDED_EXPERIMENT",
    "REJECT_VARIANT",
    "NEEDS_MORE_DATA",
    "OVERFIT_RISK",
}

REQUIRED_FIELDS = {
    "signal_id",
    "symbol",
    "signal_date",
    "entry_price",
    "stop_price",
    "target_1_price",
    "result_r",
    "mae_r",
    "mfe_r",
    "market_regime_at_signal",
    "index_trend_at_signal",
    "breadth_score_at_signal",
    "advance_decline_proxy_at_signal",
    "risk_off_flag_at_signal",
    "vix_or_volatility_proxy_at_signal",
    "sector_or_asset_group_at_signal",
    "signal_day_cluster_size",
    "broker_execution_mode",
    "live_trading_authorized",
}

PERIODS = ("training", "validation", "out_of_sample")


def _variants() -> list[dict[str, Any]]:
    return [
        {"name": "baseline_no_gate", "group": "baseline", "level": "none", "mode": "accept"},
        {"name": "risk_off_block_basic", "group": "risk_off_block", "level": "basic", "mode": "block"},
        {"name": "delay_after_risk_off_1bar", "group": "delay_after_risk_off", "level": "1bar", "mode": "delay"},
        {"name": "watch_only_weak_breadth_medium", "group": "watch_only_weak_breadth", "level": "medium", "mode": "watch"},
        {"name": "combined_gate_medium", "group": "combined_gate", "level": "medium", "mode": "combined"},
    ]


def _missing(record: dict[str, Any]) -> list[str]:
    return sorted(field for field in REQUIRED_FIELDS if record.get(field) in (None, ""))


def _is_risk_off(record: dict[str, Any]) -> bool:
    return bool(record.get("risk_off_flag_at_signal")) or str(record.get("market_regime_at_signal", "")).lower() == "risk_off"


def _is_weak_breadth(record: dict[str, Any], threshold: float = 0.5) -> bool:
    try:
        return float(record.get("breadth_score_at_signal")) < threshold
    except (TypeError, ValueError):
        return False


def _evaluate(record: dict[str, Any], variant: dict[str, Any]) -> dict[str, Any]:
    mode = variant["mode"]
    risk_off = _is_risk_off(record)
    weak = _is_weak_breadth(record)
    blocked = (mode == "block" and risk_off) or (mode == "watch" and weak) or (mode == "combined" and (risk_off or weak))
    delayed = mode == "delay" and risk_off
    accepted = not blocked
    r_value = float(record.get("result_r", 0.0))
    if blocked:
        r_value = 0.0
    if delayed:
        r_value *= 0.75
    return {
        "accepted": accepted,
        "blocked": blocked,
        "delayed": delayed,
        "skipped": False,
        "r": r_value,
        "mae_r": 0.0 if blocked else float(record.get("mae_r", 0.0)),
        "mfe_r": 0.0 if blocked else float(record.get("mfe_r", 0.0)),
        "stop_hit": float(record.get("result_r", 0.0)) <= -1.0,
        "target_1_hit": r_value >= 1.0,
        "target_2_hit": r_value >= 2.0,
        "false_breakout": float(record.get("result_r", 0.0)) < 0 and risk_off,
        "cluster": float(record.get("signal_day_cluster_size", 0.0)),
    }


def _period_result(period: str, evaluations: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(evaluations)
    accepted = [item for item in evaluations if item["accepted"]]
    denominator = len(accepted) or 1
    all_denominator = total or 1
    r_values = [item["r"] for item in accepted]
    return {
        "period": period,
        "total_trades_considered": total,
        "accepted_trades": len(accepted),
        "blocked_trades": sum(1 for item in evaluations if item["blocked"]),
        "delayed_trades": sum(1 for item in evaluations if item["delayed"]),
        "skipped_trades": sum(1 for item in evaluations if item["skipped"]),
        "false_breakout_rate": round(sum(1 for item in evaluations if item["false_breakout"]) / all_denominator, 6),
        "stop_hit_rate": round(sum(1 for item in accepted if item["stop_hit"]) / denominator, 6),
        "target_1_hit_rate": round(sum(1 for item in accepted if item["target_1_hit"]) / denominator, 6),
        "target_2_hit_rate": round(sum(1 for item in accepted if item["target_2_hit"]) / denominator, 6),
        "average_r": round(sum(r_values) / denominator, 6) if accepted else 0.0,
        "expectancy_r": round(sum(r_values) / denominator, 6) if accepted else 0.0,
        "average_mae_r": round(sum(item["mae_r"] for item in accepted) / denominator, 6) if accepted else 0.0,
        "average_mfe_r": round(sum(item["mfe_r"] for item in accepted) / denominator, 6) if accepted else 0.0,
        "signal_day_cluster_impact": round(sum(item["cluster"] for item in evaluations) / all_denominator, 6),
    }


def _recommendation(variant: dict[str, Any], results: list[dict[str, Any]]) -> str:
    if variant["group"] == "baseline":
        return "KEEP_BASELINE"
    by_period = {item["period"]: item for item in results}
    training = by_period.get("training", {}).get("expectancy_r", 0.0)
    oos = by_period.get("out_of_sample", {}).get("expectancy_r", 0.0)
    validation = by_period.get("validation", {}).get("expectancy_r", 0.0)
    if training > 0 and oos < 0:
        return "OVERFIT_RISK"
    if validation < 0 or oos < 0:
        return "REJECT_VARIANT"
    if oos >= 0 and validation >= 0:
        return "PROMOTE_TO_GUARDED_EXPERIMENT"
    return "NEEDS_MORE_DATA"


def build_bt137_report(records: list[dict[str, Any]], *, github_run_id: str | None = None) -> dict[str, Any]:
    github_run_id = github_run_id or "local"
    missing_fields = {str(record.get("signal_id") or index): _missing(record) for index, record in enumerate(records) if _missing(record)}
    if missing_fields:
        return {
            "schema": "bt137_regime_breadth_entry_gate_report.v1",
            "status": "SKIPPED_INSUFFICIENT_FIELDS",
            "research_only": True,
            "broker_execution_mode": "paper_only",
            "live_trading_authorized": False,
            "production_rule_change": False,
            "github_run_id": github_run_id,
            "missing_fields": missing_fields,
            "variant_grid": _variants(),
            "variant_results": [],
        }
    variant_results = []
    for variant in _variants():
        period_results = []
        for period in PERIODS:
            evaluations = [_evaluate(record, variant) for record in records if record.get("period") == period]
            period_results.append(_period_result(period, evaluations))
        variant_results.append({
            "variant": variant["name"],
            "group": variant["group"],
            "level": variant["level"],
            "period_results": period_results,
            "recommendation": _recommendation(variant, period_results),
        })
    return {
        "schema": "bt137_regime_breadth_entry_gate_report.v1",
        "status": "COMPLETED",
        "research_only": True,
        "broker_execution_mode": "paper_only",
        "live_trading_authorized": False,
        "production_rule_change": False,
        "github_run_id": github_run_id,
        "missing_fields": {},
        "variant_grid": _variants(),
        "variant_results": variant_results,
    }


def render_bt137_markdown(report: dict[str, Any]) -> str:
    lines = ["# BT137 Regime/Breadth Entry Gate Report", "", f"Status: {report.get('status')}", ""]
    for variant in report.get("variant_results", []):
        lines.append(f"## {variant['variant']} — {variant['recommendation']}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def persist_bt137_report(report: dict[str, Any], *, output_root: Path = Path("reports/backtests/real_data"), github_run_id: str | None = None) -> dict[str, Path]:
    run_id = github_run_id or str(report.get("github_run_id") or "local")
    latest_dir = output_root / "latest"
    run_dir = output_root / "runs" / run_id
    latest_dir.mkdir(parents=True, exist_ok=True)
    run_dir.mkdir(parents=True, exist_ok=True)
    latest_json = latest_dir / "bt137-regime-breadth-entry-gate-report.json"
    latest_markdown = latest_dir / "bt137-regime-breadth-entry-gate-report.md"
    run_json = run_dir / "bt137-regime-breadth-entry-gate-report.json"
    run_markdown = run_dir / "bt137-regime-breadth-entry-gate-report.md"
    payload = json.dumps(report, indent=2, sort_keys=True)
    markdown = render_bt137_markdown(report)
    for path in (latest_json, run_json):
        path.write_text(payload, encoding="utf-8")
    for path in (latest_markdown, run_markdown):
        path.write_text(markdown, encoding="utf-8")
    return {"latest_json": latest_json, "latest_markdown": latest_markdown, "run_json": run_json, "run_markdown": run_markdown}
