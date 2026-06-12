from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from src.validation.historical_edge_validation import coerce_finite_float

BT134_REQUIRED_FIELDS = {
    "symbol",
    "date",
    "entry",
    "stop_loss",
    "target_1",
    "atr14",
    "high",
    "low",
    "close",
}
BT134_PERIODS = ("training", "validation", "out_of_sample")
BT134_REQUIRED_VARIANT_GROUPS = {
    "baseline_fixed_stop",
    "wider_fixed_stop",
    "atr_stop",
    "same_bar_handling",
}


@dataclass(frozen=True)
class StopVariant:
    name: str
    group: str
    level: str
    stop_multiplier: float | None = None
    atr_multiplier: float | None = None
    same_bar_policy: str = "stop_first"

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "group": self.group,
            "level": self.level,
            "stop_multiplier": self.stop_multiplier,
            "atr_multiplier": self.atr_multiplier,
            "same_bar_policy": self.same_bar_policy,
        }


def build_variant_grid() -> list[StopVariant]:
    return [
        StopVariant("baseline_fixed_stop_1_0x", "baseline_fixed_stop", "1.0x", stop_multiplier=1.0),
        StopVariant("baseline_fixed_stop_1_25x", "baseline_fixed_stop", "1.25x", stop_multiplier=1.25),
        StopVariant("wider_fixed_stop_1_0x", "wider_fixed_stop", "1.0x", stop_multiplier=1.0),
        StopVariant("wider_fixed_stop_1_25x", "wider_fixed_stop", "1.25x", stop_multiplier=1.25),
        StopVariant("wider_fixed_stop_1_5x", "wider_fixed_stop", "1.5x", stop_multiplier=1.5),
        StopVariant("atr_stop_1_0atr", "atr_stop", "1.0atr", atr_multiplier=1.0),
        StopVariant("atr_stop_1_5atr", "atr_stop", "1.5atr", atr_multiplier=1.5),
        StopVariant("atr_stop_2_0atr", "atr_stop", "2.0atr", atr_multiplier=2.0),
        StopVariant("same_bar_stop_first", "same_bar_handling", "stop_first", stop_multiplier=1.0, same_bar_policy="stop_first"),
        StopVariant("same_bar_target_first", "same_bar_handling", "target_first", stop_multiplier=1.0, same_bar_policy="target_first"),
        StopVariant("same_bar_conservative_blocked", "same_bar_handling", "conservative_blocked", stop_multiplier=1.0, same_bar_policy="conservative_blocked"),
    ]


def _missing_fields(record: dict[str, Any]) -> list[str]:
    missing = [field for field in sorted(BT134_REQUIRED_FIELDS) if record.get(field) in {None, ""}]
    for field in ["entry", "stop_loss", "target_1", "atr14", "high", "low", "close"]:
        if field not in missing and coerce_finite_float(record.get(field)) is None:
            missing.append(field)
    return sorted(set(missing))


def _period(record: dict[str, Any], index: int, total: int) -> str:
    explicit = str(record.get("period") or "").strip()
    if explicit in BT134_PERIODS:
        return explicit
    if total <= 1:
        return "out_of_sample"
    ratio = index / max(1, total - 1)
    if ratio < 0.6:
        return "training"
    if ratio < 0.8:
        return "validation"
    return "out_of_sample"


def _variant_stop(record: dict[str, Any], variant: StopVariant) -> float:
    entry = float(coerce_finite_float(record.get("entry")) or 0.0)
    original_stop = float(coerce_finite_float(record.get("stop_loss")) or entry)
    atr = float(coerce_finite_float(record.get("atr14")) or 0.0)
    if variant.atr_multiplier is not None:
        return entry - (atr * variant.atr_multiplier)
    risk_distance = abs(entry - original_stop)
    multiplier = variant.stop_multiplier or 1.0
    return entry - (risk_distance * multiplier)


def _evaluate_record(record: dict[str, Any], variant: StopVariant) -> dict[str, Any]:
    missing = _missing_fields(record)
    if missing:
        return {
            "status": "SKIPPED_INSUFFICIENT_FIELDS",
            "r": 0.0,
            "stop_hit": False,
            "target_1_hit": False,
            "target_2_hit": False,
            "same_bar_ambiguous": False,
            "missing_fields": missing,
        }

    entry = float(coerce_finite_float(record["entry"]))
    stop = _variant_stop(record, variant)
    target_1 = float(coerce_finite_float(record["target_1"]))
    target_2 = coerce_finite_float(record.get("target_2"))
    high = float(coerce_finite_float(record["high"]))
    low = float(coerce_finite_float(record["low"]))
    close = float(coerce_finite_float(record["close"]))
    risk = abs(entry - stop)
    if risk <= 0:
        return {
            "status": "BLOCKED_INVALID_RISK",
            "r": 0.0,
            "stop_hit": False,
            "target_1_hit": False,
            "target_2_hit": False,
            "same_bar_ambiguous": False,
            "missing_fields": [],
        }

    stop_hit = low <= stop
    target_1_hit = high >= target_1
    target_2_hit = target_2 is not None and high >= float(target_2)
    same_bar_ambiguous = stop_hit and target_1_hit

    if same_bar_ambiguous and variant.same_bar_policy == "conservative_blocked":
        return {
            "status": "BLOCKED_SAME_BAR_AMBIGUITY",
            "r": 0.0,
            "stop_hit": False,
            "target_1_hit": False,
            "target_2_hit": False,
            "same_bar_ambiguous": True,
            "missing_fields": [],
        }

    if same_bar_ambiguous and variant.same_bar_policy == "target_first":
        r_value = (target_1 - entry) / risk
        outcome = "TARGET_FIRST"
    elif stop_hit:
        r_value = -1.0
        outcome = "STOP"
    elif target_2_hit:
        r_value = (float(target_2) - entry) / risk
        outcome = "TARGET_2"
    elif target_1_hit:
        r_value = (target_1 - entry) / risk
        outcome = "TARGET_1"
    else:
        r_value = (close - entry) / risk
        outcome = "CLOSE_MARK"

    return {
        "status": outcome,
        "r": round(float(r_value), 6),
        "stop_hit": stop_hit,
        "target_1_hit": target_1_hit,
        "target_2_hit": bool(target_2_hit),
        "same_bar_ambiguous": same_bar_ambiguous,
        "missing_fields": [],
    }


def _period_result(period: str, evaluations: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(evaluations)
    skipped = sum(1 for item in evaluations if item["status"] == "SKIPPED_INSUFFICIENT_FIELDS")
    blocked = sum(1 for item in evaluations if str(item["status"]).startswith("BLOCKED"))
    eligible = [item for item in evaluations if item["status"] not in {"SKIPPED_INSUFFICIENT_FIELDS"} and not str(item["status"]).startswith("BLOCKED")]
    r_values = [float(item["r"]) for item in eligible]
    denominator = len(eligible) or 1
    return {
        "period": period,
        "total": total,
        "eligible_count": len(eligible),
        "stop_hit_rate": round(sum(1 for item in eligible if item["stop_hit"]) / denominator, 6),
        "target_1_hit_rate": round(sum(1 for item in eligible if item["target_1_hit"]) / denominator, 6),
        "target_2_hit_rate": round(sum(1 for item in eligible if item["target_2_hit"]) / denominator, 6),
        "average_r": round(sum(r_values) / denominator, 6) if eligible else 0.0,
        "expectancy_r": round(sum(r_values) / denominator, 6) if eligible else 0.0,
        "skipped_count": skipped,
        "blocked_count": blocked,
        "same_bar_ambiguous_count": sum(1 for item in evaluations if item["same_bar_ambiguous"]),
    }


def _recommendation(period_results: list[dict[str, Any]]) -> str:
    by_period = {item["period"]: item for item in period_results}
    training = float(by_period.get("training", {}).get("expectancy_r", 0.0))
    validation = float(by_period.get("validation", {}).get("expectancy_r", 0.0))
    oos = float(by_period.get("out_of_sample", {}).get("expectancy_r", 0.0))
    if training > 0 and oos < 0:
        return "OVERFIT_RISK"
    if validation > 0 and oos < 0:
        return "REJECT_VARIANT"
    if oos > 0 and validation >= 0:
        return "PROMOTE_TO_REVIEW"
    return "NEEDS_MORE_DATA"


def build_bt134_report(records: list[dict[str, Any]], *, github_run_id: str | None = None) -> dict[str, Any]:
    github_run_id = github_run_id or "local"
    all_missing: dict[str, list[str]] = {}
    for record in records:
        missing = _missing_fields(record)
        if missing:
            key = str(record.get("symbol") or record.get("date") or len(all_missing))
            all_missing[key] = missing
    if all_missing:
        return {
            "schema": "bt134_stop_loss_variant_report.v1",
            "status": "SKIPPED_INSUFFICIENT_FIELDS",
            "research_only": True,
            "broker_execution_mode": "paper_only",
            "production_rule_change": False,
            "github_run_id": github_run_id,
            "missing_fields": all_missing,
            "variant_grid": [variant.to_dict() for variant in build_variant_grid()],
            "variant_results": [],
            "periods": list(BT134_PERIODS),
            "same_bar_ambiguity_policy": "explicitly_reported",
        }

    variant_results = []
    periods_by_index = [_period(record, index, len(records)) for index, record in enumerate(records)]
    for variant in build_variant_grid():
        period_results = []
        for period_name in BT134_PERIODS:
            evaluations = [
                _evaluate_record(record, variant)
                for record, period in zip(records, periods_by_index)
                if period == period_name
            ]
            period_results.append(_period_result(period_name, evaluations))
        variant_results.append(
            {
                "variant": variant.name,
                "group": variant.group,
                "level": variant.level,
                "same_bar_policy": variant.same_bar_policy,
                "period_results": period_results,
                "recommendation": _recommendation(period_results),
            }
        )

    return {
        "schema": "bt134_stop_loss_variant_report.v1",
        "status": "COMPLETED",
        "generated_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
        "github_run_id": github_run_id,
        "research_only": True,
        "broker_execution_mode": "paper_only",
        "production_rule_change": False,
        "periods": list(BT134_PERIODS),
        "same_bar_ambiguity_policy": "explicitly_reported",
        "missing_fields": {},
        "variant_grid": [variant.to_dict() for variant in build_variant_grid()],
        "variant_results": variant_results,
    }


def render_bt134_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# BT134 Stop-Loss Variant Report",
        "",
        f"Status: {report.get('status')}",
        f"Research only: {report.get('research_only')}",
        f"Broker execution mode: {report.get('broker_execution_mode')}",
        f"Production rule change: {report.get('production_rule_change')}",
        "",
    ]
    if report.get("missing_fields"):
        lines.extend(["## Missing Fields", "", "```json", json.dumps(report["missing_fields"], indent=2, sort_keys=True), "```", ""])
    lines.extend(["## Variant Results", ""])
    for variant in report.get("variant_results", []):
        lines.append(f"### {variant['variant']} — {variant['recommendation']}")
        lines.append("")
        lines.append("| Period | Total | Stop Hit Rate | T1 Hit Rate | Avg R | Expectancy R | Skipped | Blocked | Same-Bar |")
        lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|")
        for period in variant.get("period_results", []):
            lines.append(
                f"| {period['period']} | {period['total']} | {period['stop_hit_rate']:.2%} | "
                f"{period['target_1_hit_rate']:.2%} | {period['average_r']:.4f} | "
                f"{period['expectancy_r']:.4f} | {period['skipped_count']} | "
                f"{period['blocked_count']} | {period['same_bar_ambiguous_count']} |"
            )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def persist_bt134_report(
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

    latest_json = latest_dir / "bt134-stop-loss-variant-report.json"
    latest_markdown = latest_dir / "bt134-stop-loss-variant-report.md"
    run_json = run_dir / "bt134-stop-loss-variant-report.json"
    run_markdown = run_dir / "bt134-stop-loss-variant-report.md"
    payload = json.dumps(report, indent=2, sort_keys=True)
    markdown = render_bt134_markdown(report)
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
