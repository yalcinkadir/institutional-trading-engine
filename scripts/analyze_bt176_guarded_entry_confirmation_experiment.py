#!/usr/bin/env python3
"""Build the BT176 guarded entry-confirmation experiment contract.

BT176 promotes the BT133 research finding into a guarded, paper-only shadow
experiment. It does not change production entry rules, broker execution, sizing
or live-trading authorization.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from statistics import mean
from typing import Any


STATUS_READY = "READY_FOR_PAPER_SHADOW"
STATUS_BLOCKED = "BLOCKED"
EXPERIMENT_SCOPE = "paper_observation_shadow_only"
DEFAULT_VARIANT_ID = "next_bar_close_confirmation_1bar"


@dataclass(frozen=True)
class ExperimentMetrics:
    total_trades_considered: int
    accepted_trades: int
    filtered_trades: int
    false_breakout_rate: float
    stop_hit_rate: float
    target_1_hit_rate: float
    target_2_hit_rate: float
    average_r: float
    expectancy_r: float


@dataclass(frozen=True)
class BT176Report:
    report_version: str
    source_evidence: str
    source_variant_report: str
    run_id: str
    candidate_variant_id: str
    candidate_family: str
    candidate_parameters: dict[str, Any]
    guard_status: str
    experiment_scope: str
    production_rule_change_allowed: bool
    live_trading_authorized: bool
    broker_execution_mode: str
    baseline_metrics: ExperimentMetrics
    guarded_experiment_metrics: ExperimentMetrics
    acceptance_criteria: list[str]
    guard_reasons: list[str] = field(default_factory=list)
    safety_notes: list[str] = field(default_factory=list)


def _rate(count: int, total: int) -> float:
    return round(count / total, 4) if total else 0.0


def _avg(values: list[float]) -> float:
    return round(mean(values), 4) if values else 0.0


def _as_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise SystemExit(f"{path} must contain a JSON object")
    return payload


def _require_evidence_contract(evidence: dict[str, Any]) -> list[dict[str, Any]]:
    if evidence.get("data_source") != "real_data":
        raise SystemExit("BT176 requires source evidence data_source=real_data")
    if evidence.get("is_demo") is not False:
        raise SystemExit("BT176 refuses demo evidence")
    if evidence.get("input_pack_gate_status") != "PASSED":
        raise SystemExit("BT176 requires input_pack_gate_status=PASSED")
    if evidence.get("run_health_status") != "OK":
        raise SystemExit("BT176 requires run_health_status=OK")
    if evidence.get("live_trading_authorized") is not False:
        raise SystemExit("BT176 requires live_trading_authorized=false")
    if evidence.get("broker_execution_mode") != "paper_only":
        raise SystemExit("BT176 requires broker_execution_mode=paper_only")

    rows = evidence.get("results")
    if not isinstance(rows, list) or not rows:
        raise SystemExit("BT176 requires non-empty real-data evidence results")
    return [dict(row) for row in rows if isinstance(row, dict)]


def _select_variant(variant_report: dict[str, Any], variant_id: str) -> dict[str, Any]:
    if variant_report.get("final_recommendation") != "PROMOTE_TO_GUARDED_EXPERIMENT":
        raise SystemExit("BT176 requires BT133 final_recommendation=PROMOTE_TO_GUARDED_EXPERIMENT")
    if variant_report.get("live_trading_authorized") is not False:
        raise SystemExit("BT176 requires BT133 live_trading_authorized=false")
    if variant_report.get("broker_execution_mode") != "paper_only":
        raise SystemExit("BT176 requires BT133 broker_execution_mode=paper_only")

    variants = variant_report.get("variant_results")
    if not isinstance(variants, list):
        raise SystemExit("BT176 requires BT133 variant_results")

    for item in variants:
        if not isinstance(item, dict):
            continue
        if item.get("variant_id") == variant_id:
            if item.get("status") != "EVALUATED":
                raise SystemExit(f"BT176 candidate variant is not evaluated: {variant_id}")
            if item.get("recommendation") != "PROMOTE_TO_GUARDED_EXPERIMENT":
                raise SystemExit(f"BT176 candidate variant is not promoted: {variant_id}")
            if item.get("missing_fields"):
                raise SystemExit(f"BT176 candidate variant has missing fields: {variant_id}")
            return dict(item)

    raise SystemExit(f"BT176 candidate variant not found: {variant_id}")


def _accepted_by_variant(row: dict[str, Any], variant: dict[str, Any]) -> bool:
    if not bool(row.get("entry_hit")):
        return False

    family = str(variant.get("family") or "")
    params = dict(variant.get("parameters") or {})

    if family == "next_bar_close_confirmation":
        delay = int(params.get("confirmation_delay_bars") or 1)
        mfe = _as_float(row.get("max_favorable_excursion_r"))
        mae = _as_float(row.get("max_adverse_excursion_r"))
        bars = int(row.get("bars_evaluated") or 0)
        if mfe is None or mae is None:
            return False
        return (
            bars >= delay + 1
            and mfe >= float(params.get("minimum_mfe_r") or 0.0)
            and mae > -1.0
        )

    if family == "volatility_adjusted_confirmation":
        mfe = _as_float(row.get("max_favorable_excursion_r"))
        mae = _as_float(row.get("max_adverse_excursion_r"))
        if mfe is None or mae is None:
            return False
        return (
            mae >= float(params.get("max_adverse_excursion_r_allowed"))
            and mfe >= float(params.get("minimum_mfe_r") or 0.0)
        )

    if family == "volume_confirmed_breakout":
        entry_volume = _as_float(row.get("entry_volume"))
        avg_volume = _as_float(row.get("avg_volume_20"))
        if entry_volume is None or avg_volume is None or avg_volume <= 0:
            return False
        return entry_volume / avg_volume >= float(params.get("entry_volume_to_avg_volume_20_min"))

    return False


def _metrics(rows: list[dict[str, Any]], *, variant: dict[str, Any] | None = None) -> ExperimentMetrics:
    if variant is None:
        accepted = [row for row in rows if bool(row.get("entry_hit"))]
    else:
        accepted = [row for row in rows if _accepted_by_variant(row, variant)]

    r_values = [float(row.get("r_multiple") or 0.0) for row in accepted]
    total_accepted = len(accepted)

    return ExperimentMetrics(
        total_trades_considered=len(rows),
        accepted_trades=total_accepted,
        filtered_trades=len(rows) - total_accepted,
        false_breakout_rate=_rate(sum(bool(row.get("false_breakout")) for row in accepted), total_accepted),
        stop_hit_rate=_rate(sum(bool(row.get("stop_hit")) for row in accepted), total_accepted),
        target_1_hit_rate=_rate(sum(bool(row.get("target_1_hit")) for row in accepted), total_accepted),
        target_2_hit_rate=_rate(sum(bool(row.get("target_2_hit")) for row in accepted), total_accepted),
        average_r=_avg(r_values),
        expectancy_r=_avg(r_values),
    )


def _guard_reasons(baseline: ExperimentMetrics, experiment: ExperimentMetrics) -> list[str]:
    reasons: list[str] = []
    if experiment.accepted_trades < 2:
        reasons.append("candidate_variant_accepts_too_few_trades")
    if experiment.stop_hit_rate > baseline.stop_hit_rate:
        reasons.append("candidate_variant_worsens_stop_hit_rate")
    if experiment.false_breakout_rate > baseline.false_breakout_rate:
        reasons.append("candidate_variant_worsens_false_breakout_rate")
    if experiment.expectancy_r < baseline.expectancy_r:
        reasons.append("candidate_variant_expectancy_below_baseline")
    return reasons


def analyze(
    *,
    evidence_path: Path,
    variant_report_path: Path,
    candidate_variant_id: str = DEFAULT_VARIANT_ID,
) -> BT176Report:
    evidence = _load_json(evidence_path)
    rows = _require_evidence_contract(evidence)
    variant_report = _load_json(variant_report_path)
    variant = _select_variant(variant_report, candidate_variant_id)

    baseline = _metrics(rows)
    experiment = _metrics(rows, variant=variant)
    reasons = _guard_reasons(baseline, experiment)

    return BT176Report(
        report_version="bt176.v1",
        source_evidence=str(evidence_path),
        source_variant_report=str(variant_report_path),
        run_id=str(evidence.get("run_id")),
        candidate_variant_id=str(variant["variant_id"]),
        candidate_family=str(variant.get("family")),
        candidate_parameters=dict(variant.get("parameters") or {}),
        guard_status=STATUS_READY if not reasons else STATUS_BLOCKED,
        experiment_scope=EXPERIMENT_SCOPE,
        production_rule_change_allowed=False,
        live_trading_authorized=False,
        broker_execution_mode="paper_only",
        baseline_metrics=baseline,
        guarded_experiment_metrics=experiment,
        guard_reasons=reasons,
        acceptance_criteria=[
            "BT133 source recommendation remains PROMOTE_TO_GUARDED_EXPERIMENT.",
            "Candidate variant is evaluated, promoted and has no missing fields.",
            "Guarded experiment expectancy is not below baseline on the current evidence pack.",
            "Guarded experiment does not worsen false-breakout or stop-hit rate.",
            "At least two accepted trades remain after confirmation filtering.",
            "Experiment remains paper-observation shadow-only and cannot change production entry rules.",
        ],
        safety_notes=[
            "Research only. No production entry rule change.",
            "No live trading authorization.",
            "broker_execution_mode remains paper_only.",
            "Promotion to production requires a separate issue, fresh forward evidence and explicit approval.",
        ],
    )


def _markdown_table(headers: list[str], rows: list[list[Any]]) -> list[str]:
    lines = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    for row in rows:
        lines.append("| " + " | ".join(str(cell) for cell in row) + " |")
    return lines


def render_markdown(report: BT176Report) -> str:
    lines: list[str] = [
        "# BT176 Guarded Entry Confirmation Experiment",
        "",
        "## Evidence Contract",
        "",
        f"- Report version: {report.report_version}",
        f"- Source evidence: {report.source_evidence}",
        f"- Source variant report: {report.source_variant_report}",
        f"- Run ID: {report.run_id}",
        f"- Candidate variant: {report.candidate_variant_id}",
        f"- Candidate family: {report.candidate_family}",
        f"- Candidate parameters: `{json.dumps(report.candidate_parameters, sort_keys=True)}`",
        f"- Guard status: {report.guard_status}",
        f"- Experiment scope: {report.experiment_scope}",
        f"- Production rule change allowed: {report.production_rule_change_allowed}",
        f"- Live trading authorized: {report.live_trading_authorized}",
        f"- Broker execution mode: {report.broker_execution_mode}",
        "",
        "## Baseline vs Guarded Experiment",
        "",
    ]
    lines.extend(
        _markdown_table(
            [
                "Mode",
                "Considered",
                "Accepted",
                "Filtered",
                "False BO",
                "Stop",
                "T1",
                "T2",
                "Avg R",
                "Expectancy R",
            ],
            [
                [
                    "baseline",
                    report.baseline_metrics.total_trades_considered,
                    report.baseline_metrics.accepted_trades,
                    report.baseline_metrics.filtered_trades,
                    report.baseline_metrics.false_breakout_rate,
                    report.baseline_metrics.stop_hit_rate,
                    report.baseline_metrics.target_1_hit_rate,
                    report.baseline_metrics.target_2_hit_rate,
                    report.baseline_metrics.average_r,
                    report.baseline_metrics.expectancy_r,
                ],
                [
                    "guarded_experiment",
                    report.guarded_experiment_metrics.total_trades_considered,
                    report.guarded_experiment_metrics.accepted_trades,
                    report.guarded_experiment_metrics.filtered_trades,
                    report.guarded_experiment_metrics.false_breakout_rate,
                    report.guarded_experiment_metrics.stop_hit_rate,
                    report.guarded_experiment_metrics.target_1_hit_rate,
                    report.guarded_experiment_metrics.target_2_hit_rate,
                    report.guarded_experiment_metrics.average_r,
                    report.guarded_experiment_metrics.expectancy_r,
                ],
            ],
        )
    )

    lines.extend(["", "## Guard Reasons", ""])
    if report.guard_reasons:
        for reason in report.guard_reasons:
            lines.append(f"- {reason}")
    else:
        lines.append("- none")

    lines.extend(["", "## Acceptance Criteria", ""])
    for criterion in report.acceptance_criteria:
        lines.append(f"- {criterion}")

    lines.extend(["", "## Safety Notes", ""])
    for note in report.safety_notes:
        lines.append(f"- {note}")

    return "\n".join(lines).rstrip() + "\n"


def write_report(report: BT176Report, *, output_json: Path, output_md: Path) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(asdict(report), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    output_md.write_text(render_markdown(report), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--variant-report", type=Path, required=True)
    parser.add_argument("--candidate-variant-id", default=DEFAULT_VARIANT_ID)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = analyze(
        evidence_path=args.evidence,
        variant_report_path=args.variant_report,
        candidate_variant_id=args.candidate_variant_id,
    )
    write_report(report, output_json=args.output_json, output_md=args.output_md)
    print(json.dumps({"status": report.guard_status, "candidate_variant_id": report.candidate_variant_id}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
