#!/usr/bin/env python3
"""Build BT140 historical trade-plan sample coverage expansion report.

BT140 is an evidence-expansion layer. It reviews generated historical trade
plans before BT131 simulation and measures whether the sample is broad enough to
help BT139 move toward REVIEWABLE_SAMPLE. It does not change production rules.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


TARGET_EARLY_TRADE_COUNT = 50
TARGET_REVIEWABLE_TRADE_COUNT = 100
TARGET_REVIEWABLE_SIGNAL_DAYS = 30
TARGET_REVIEWABLE_SETUP_FAMILIES = 2


@dataclass(frozen=True)
class BT140Report:
    report_version: str
    source_trade_plans: str
    expansion_status: str
    generated_plan_count: int
    accepted_candidate_count: int
    candidate_signal_day_count: int
    signal_day_cluster_count: int
    max_signal_day_cluster_size: int
    symbol_count: int
    setup_family_count: int
    asset_group_count: int
    per_symbol_plan_count: dict[str, int]
    per_setup_plan_count: dict[str, int]
    per_asset_group_plan_count: dict[str, int]
    concentrated_signal_days: list[dict[str, Any]]
    unsupported_setup_skips: list[dict[str, str]]
    missing_field_reasons: dict[str, list[str]]
    targets: dict[str, int]
    broker_execution_mode: str
    live_trading_authorized: bool
    production_rule_change_allowed: bool
    safety_notes: list[str]


def _load_plans(path: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return payload, {}
    if not isinstance(payload, dict):
        raise SystemExit("BT140 trade-plan input must be a JSON object or list")
    plans = payload.get("plans") or payload.get("signals")
    if not isinstance(plans, list):
        raise SystemExit("BT140 trade-plan input requires plans[] or signals[]")
    return plans, dict(payload.get("metadata") or {})


def _asset_group(symbol: str, plan: dict[str, Any]) -> str:
    explicit = plan.get("asset_group")
    if explicit:
        return str(explicit)
    symbol = symbol.upper()
    if symbol in {"QQQ", "SPY", "IWM", "DIA"}:
        return "index_etf"
    if symbol in {"GLD", "SLV", "PPLT", "IAU"}:
        return "metals_etf"
    if symbol in {"NVDA", "MU", "AMD", "AVGO", "INTC"}:
        return "semiconductor_or_hardware"
    if symbol in {"MSFT", "AAPL", "META", "GOOGL", "AMZN", "NFLX"}:
        return "mega_cap_tech"
    return "unknown"


def _plan_id(plan: dict[str, Any], index: int) -> str:
    return str(plan.get("signal_id") or f"plan_{index}")


def _missing_fields(plans: list[dict[str, Any]]) -> dict[str, list[str]]:
    required = [
        "signal_id",
        "symbol",
        "signal_date",
        "entry_trigger",
        "stop_loss",
        "target_1",
        "target_2",
        "valid_until",
        "entry_type",
        "setup_type",
        "stop_model",
        "exit_model",
    ]
    optional_but_desired = [
        "atr14_at_signal",
        "volume",
        "avg_volume_20",
        "asset_group",
        "market_regime",
    ]
    missing: dict[str, list[str]] = {}
    for field in required + optional_but_desired:
        ids = [_plan_id(plan, i) for i, plan in enumerate(plans) if plan.get(field) in (None, "")]
        if ids:
            missing[field] = ids[:25]
    return missing


def _clusters(plans: list[dict[str, Any]]) -> tuple[int, int, list[dict[str, Any]]]:
    by_day: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for plan in plans:
        by_day[str(plan.get("signal_date") or "UNKNOWN")].append(plan)
    concentrated: list[dict[str, Any]] = []
    max_size = 0
    for signal_day, day_plans in sorted(by_day.items()):
        max_size = max(max_size, len(day_plans))
        if len(day_plans) < 2:
            continue
        concentrated.append(
            {
                "signal_date": signal_day,
                "cluster_size": len(day_plans),
                "symbols": sorted({str(plan.get("symbol") or "UNKNOWN") for plan in day_plans}),
                "setup_types": dict(Counter(str(plan.get("setup_type") or "UNKNOWN") for plan in day_plans)),
            }
        )
    return len(by_day), max_size, concentrated


def _expansion_status(plan_count: int, signal_day_count: int, setup_count: int) -> str:
    if plan_count >= TARGET_REVIEWABLE_TRADE_COUNT and signal_day_count >= TARGET_REVIEWABLE_SIGNAL_DAYS and setup_count >= TARGET_REVIEWABLE_SETUP_FAMILIES:
        return "REVIEWABLE_COVERAGE_CANDIDATE"
    if plan_count >= TARGET_EARLY_TRADE_COUNT:
        return "EXPANDED_EARLY_SAMPLE"
    return "NEEDS_MORE_GENERATED_PLANS"


def analyze(plans_path: Path) -> BT140Report:
    plans, metadata = _load_plans(plans_path)
    symbols = [str(plan.get("symbol") or "UNKNOWN").upper() for plan in plans]
    setups = [str(plan.get("setup_type") or "UNKNOWN_SETUP") for plan in plans]
    asset_groups = [_asset_group(symbol, plan) for symbol, plan in zip(symbols, plans)]
    signal_day_count, max_cluster, concentrated = _clusters(plans)
    status = _expansion_status(len(plans), signal_day_count, len(set(setups)))
    return BT140Report(
        report_version="bt140.v1",
        source_trade_plans=str(plans_path),
        expansion_status=status,
        generated_plan_count=int(metadata.get("generated_plans") or len(plans)),
        accepted_candidate_count=len(plans),
        candidate_signal_day_count=signal_day_count,
        signal_day_cluster_count=len(concentrated),
        max_signal_day_cluster_size=max_cluster,
        symbol_count=len(set(symbols)),
        setup_family_count=len(set(setups)),
        asset_group_count=len(set(asset_groups)),
        per_symbol_plan_count=dict(sorted(Counter(symbols).items())),
        per_setup_plan_count=dict(sorted(Counter(setups).items())),
        per_asset_group_plan_count=dict(sorted(Counter(asset_groups).items())),
        concentrated_signal_days=concentrated,
        unsupported_setup_skips=[],
        missing_field_reasons=_missing_fields(plans),
        targets={
            "early_min_trade_count": TARGET_EARLY_TRADE_COUNT,
            "reviewable_min_trade_count": TARGET_REVIEWABLE_TRADE_COUNT,
            "reviewable_min_signal_day_count": TARGET_REVIEWABLE_SIGNAL_DAYS,
            "reviewable_min_setup_family_count": TARGET_REVIEWABLE_SETUP_FAMILIES,
        },
        broker_execution_mode="paper_only",
        live_trading_authorized=False,
        production_rule_change_allowed=False,
        safety_notes=[
            "BT140 expands evidence coverage only and does not modify trading rules.",
            "BT139 remains the promotion gate.",
            "No live trading authorization.",
            "broker_execution_mode remains paper_only.",
        ],
    )


def render_markdown(report: BT140Report) -> str:
    lines = [
        "# BT140 Sample Coverage Expansion Report",
        "",
        f"- Expansion status: {report.expansion_status}",
        f"- Generated plan count: {report.generated_plan_count}",
        f"- Candidate signal-day count: {report.candidate_signal_day_count}",
        f"- Signal-day cluster count: {report.signal_day_cluster_count}",
        f"- Max signal-day cluster size: {report.max_signal_day_cluster_size}",
        f"- Symbol count: {report.symbol_count}",
        f"- Setup family count: {report.setup_family_count}",
        f"- Asset group count: {report.asset_group_count}",
        f"- Production rule change allowed: {report.production_rule_change_allowed}",
        "",
        "## Per-symbol plan count",
        "",
    ]
    for symbol, count in report.per_symbol_plan_count.items():
        lines.append(f"- {symbol}: {count}")
    lines.extend(["", "## Per-setup plan count", ""])
    for setup, count in report.per_setup_plan_count.items():
        lines.append(f"- {setup}: {count}")
    lines.extend(["", "## Safety Notes", ""])
    for note in report.safety_notes:
        lines.append(f"- {note}")
    return "\n".join(lines).rstrip() + "\n"


def write_report(report: BT140Report, *, output_json: Path, output_md: Path) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(asdict(report), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    output_md.write_text(render_markdown(report), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build BT140 sample coverage expansion report")
    parser.add_argument("--trade-plans", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = analyze(args.trade_plans)
    write_report(report, output_json=args.output_json, output_md=args.output_md)
    print(json.dumps({"expansion_status": report.expansion_status, "generated_plan_count": report.generated_plan_count}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
