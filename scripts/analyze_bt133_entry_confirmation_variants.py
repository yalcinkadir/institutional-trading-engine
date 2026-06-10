#!/usr/bin/env python3
"""Analyze BT131 evidence for BT133 entry-confirmation variant research.

BT133 is research-only. It compares stricter entry-confirmation variants against
validated BT131 real-data evidence without changing production entry rules.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path
from statistics import mean
from typing import Any


RECOMMEND_KEEP_BASELINE = "KEEP_BASELINE"
RECOMMEND_PROMOTE = "PROMOTE_TO_GUARDED_EXPERIMENT"
RECOMMEND_REJECT = "REJECT_VARIANT"
RECOMMEND_NEEDS_MORE_DATA = "NEEDS_MORE_DATA"
RECOMMEND_OVERFIT_RISK = "OVERFIT_RISK"

STATUS_EVALUATED = "EVALUATED"
STATUS_SKIPPED = "SKIPPED_INSUFFICIENT_FIELDS"
PERIOD_NAMES = ("training", "walk_forward", "out_of_sample")


@dataclass(frozen=True)
class VariantSpec:
    variant_id: str
    family: str
    description: str
    parameters: dict[str, Any]
    required_fields: tuple[str, ...]


@dataclass(frozen=True)
class PeriodMetrics:
    period: str
    start_date: str | None
    end_date: str | None
    total_trades_considered: int
    accepted_trades: int
    skipped_trades: int
    false_breakout_rate: float
    stop_hit_rate: float
    target_1_hit_rate: float
    target_2_hit_rate: float
    average_r: float
    expectancy_r: float


@dataclass(frozen=True)
class VariantResult:
    variant_id: str
    family: str
    description: str
    parameters: dict[str, Any]
    status: str
    missing_fields: list[str]
    limitations: list[str]
    recommendation: str
    overfit_warning: str | None
    periods: list[PeriodMetrics]


@dataclass(frozen=True)
class BT133Report:
    report_version: str
    source_evidence: str
    run_id: str
    data_source: str
    is_demo: bool
    input_pack_gate_status: str
    input_completeness_status: str
    run_health_status: str
    live_trading_authorized: bool
    broker_execution_mode: str
    total_source_trades: int
    walk_forward_periods: dict[str, dict[str, str | None]]
    variant_results: list[VariantResult]
    final_recommendation: str
    safety_notes: list[str]


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


def _load_evidence(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise SystemExit("BT133 source evidence must be a JSON object")
    if payload.get("data_source") != "real_data":
        raise SystemExit("BT133 requires data_source=real_data")
    if payload.get("is_demo") is not False:
        raise SystemExit("BT133 refuses demo evidence")
    if payload.get("input_pack_gate_status") != "PASSED":
        raise SystemExit("BT133 requires input_pack_gate_status=PASSED")
    if payload.get("run_health_status") != "OK":
        raise SystemExit("BT133 requires run_health_status=OK")
    if payload.get("live_trading_authorized") is not False:
        raise SystemExit("BT133 requires live_trading_authorized=false")
    if payload.get("broker_execution_mode") != "paper_only":
        raise SystemExit("BT133 requires broker_execution_mode=paper_only")
    if not isinstance(payload.get("results"), list) or not payload["results"]:
        raise SystemExit("BT133 requires non-empty BT131 results")
    return payload


def _parse_signal_date(row: dict[str, Any]) -> date:
    raw = str(row.get("signal_date") or "")
    try:
        return date.fromisoformat(raw[:10])
    except ValueError:
        return date.min


def _period_for_index(index: int, total: int) -> str:
    if total <= 2:
        return PERIOD_NAMES[min(index, len(PERIOD_NAMES) - 1)]
    first_cut = max(1, total // 3)
    second_cut = max(first_cut + 1, (2 * total) // 3)
    if index < first_cut:
        return "training"
    if index < second_cut:
        return "walk_forward"
    return "out_of_sample"


def _assign_periods(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sorted_rows = sorted(
        results,
        key=lambda row: (_parse_signal_date(row), str(row.get("signal_id") or "")),
    )
    assigned: list[dict[str, Any]] = []
    total = len(sorted_rows)
    for index, row in enumerate(sorted_rows):
        copied = dict(row)
        copied["bt133_period"] = _period_for_index(index, total)
        assigned.append(copied)
    return assigned


def _period_bounds(rows: list[dict[str, Any]]) -> dict[str, dict[str, str | None]]:
    bounds: dict[str, dict[str, str | None]] = {}
    for period in PERIOD_NAMES:
        dates = sorted(
            str(row.get("signal_date"))
            for row in rows
            if row.get("bt133_period") == period and row.get("signal_date")
        )
        bounds[period] = {
            "start_date": dates[0] if dates else None,
            "end_date": dates[-1] if dates else None,
        }
    return bounds


def _variant_grid() -> list[VariantSpec]:
    specs = [
        VariantSpec(
            variant_id="baseline_breakout_trigger",
            family="baseline",
            description="Current BT131 breakout trigger baseline.",
            parameters={"entry_rule": "breakout_trigger"},
            required_fields=("entry_hit", "r_multiple"),
        )
    ]

    for delay in (1, 2, 3):
        specs.append(
            VariantSpec(
                variant_id=f"next_bar_close_confirmation_{delay}bar",
                family="next_bar_close_confirmation",
                description="Proxy for next-bar close confirmation using BT136 MFE/MAE path summary.",
                parameters={
                    "confirmation_delay_bars": delay,
                    "minimum_mfe_r": round(0.25 * delay, 2),
                },
                required_fields=(
                    "entry_hit",
                    "bars_evaluated",
                    "max_favorable_excursion_r",
                    "max_adverse_excursion_r",
                    "r_multiple",
                ),
            )
        )

    for threshold in (1.1, 1.25, 1.5):
        specs.append(
            VariantSpec(
                variant_id=f"volume_confirmed_breakout_{str(threshold).replace('.', '_')}x",
                family="volume_confirmed_breakout",
                description="Volume-confirmed breakout requiring entry volume versus average volume.",
                parameters={"entry_volume_to_avg_volume_20_min": threshold},
                required_fields=("entry_volume", "avg_volume_20", "entry_hit", "r_multiple"),
            )
        )

    for name, max_adverse_r, min_favorable_r in (
        ("conservative", -0.95, 0.25),
        ("medium", -0.75, 0.5),
        ("strict", -0.5, 0.75),
    ):
        specs.append(
            VariantSpec(
                variant_id=f"volatility_adjusted_confirmation_{name}",
                family="volatility_adjusted_confirmation",
                description="Volatility-adjusted confirmation proxy using BT136 MAE/MFE in R.",
                parameters={
                    "max_adverse_excursion_r_allowed": max_adverse_r,
                    "minimum_mfe_r": min_favorable_r,
                },
                required_fields=(
                    "entry_hit",
                    "max_favorable_excursion_r",
                    "max_adverse_excursion_r",
                    "r_multiple",
                ),
            )
        )

    return specs


def _missing_fields(rows: list[dict[str, Any]], fields: tuple[str, ...]) -> list[str]:
    return sorted(
        field
        for field in fields
        if not any(row.get(field) is not None for row in rows)
    )


def _accepted_by_variant(row: dict[str, Any], spec: VariantSpec) -> bool:
    if spec.family == "baseline":
        return bool(row.get("entry_hit"))

    if not bool(row.get("entry_hit")):
        return False

    if spec.family == "next_bar_close_confirmation":
        mfe = _as_float(row.get("max_favorable_excursion_r"))
        mae = _as_float(row.get("max_adverse_excursion_r"))
        bars = int(row.get("bars_evaluated") or 0)
        return (
            mfe is not None
            and mae is not None
            and bars >= int(spec.parameters["confirmation_delay_bars"]) + 1
            and mfe >= float(spec.parameters["minimum_mfe_r"])
            and mae > -1.0
        )

    if spec.family == "volume_confirmed_breakout":
        entry_volume = _as_float(row.get("entry_volume"))
        avg_volume = _as_float(row.get("avg_volume_20"))
        return (
            entry_volume is not None
            and avg_volume is not None
            and avg_volume > 0
            and entry_volume / avg_volume
            >= float(spec.parameters["entry_volume_to_avg_volume_20_min"])
        )

    if spec.family == "volatility_adjusted_confirmation":
        mfe = _as_float(row.get("max_favorable_excursion_r"))
        mae = _as_float(row.get("max_adverse_excursion_r"))
        return (
            mfe is not None
            and mae is not None
            and mae >= float(spec.parameters["max_adverse_excursion_r_allowed"])
            and mfe >= float(spec.parameters["minimum_mfe_r"])
        )

    return False


def _metrics_for_period(
    rows: list[dict[str, Any]],
    period: str,
    spec: VariantSpec,
    status: str,
) -> PeriodMetrics:
    period_rows = [row for row in rows if row.get("bt133_period") == period]

    if status != STATUS_EVALUATED:
        return PeriodMetrics(
            period,
            None,
            None,
            len(period_rows),
            0,
            len(period_rows),
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        )

    accepted = [row for row in period_rows if _accepted_by_variant(row, spec)]
    r_values = [float(row.get("r_multiple") or 0.0) for row in accepted]
    dates = sorted(str(row.get("signal_date")) for row in period_rows if row.get("signal_date"))
    total_accepted = len(accepted)

    return PeriodMetrics(
        period=period,
        start_date=dates[0] if dates else None,
        end_date=dates[-1] if dates else None,
        total_trades_considered=len(period_rows),
        accepted_trades=total_accepted,
        skipped_trades=len(period_rows) - total_accepted,
        false_breakout_rate=_rate(
            sum(bool(row.get("false_breakout")) for row in accepted),
            total_accepted,
        ),
        stop_hit_rate=_rate(
            sum(bool(row.get("stop_hit")) for row in accepted),
            total_accepted,
        ),
        target_1_hit_rate=_rate(
            sum(bool(row.get("target_1_hit")) for row in accepted),
            total_accepted,
        ),
        target_2_hit_rate=_rate(
            sum(bool(row.get("target_2_hit")) for row in accepted),
            total_accepted,
        ),
        average_r=_avg(r_values),
        expectancy_r=_avg(r_values),
    )


def _period_metric(periods: list[PeriodMetrics], period: str, field: str) -> float:
    for item in periods:
        if item.period == period:
            return float(getattr(item, field))
    return 0.0


def _recommend(
    spec: VariantSpec,
    periods: list[PeriodMetrics],
    baseline_periods: list[PeriodMetrics] | None,
) -> tuple[str, str | None]:
    if spec.family == "baseline" or baseline_periods is None:
        return RECOMMEND_KEEP_BASELINE, None

    train_delta = _period_metric(periods, "training", "expectancy_r") - _period_metric(
        baseline_periods,
        "training",
        "expectancy_r",
    )
    oos_delta = _period_metric(periods, "out_of_sample", "expectancy_r") - _period_metric(
        baseline_periods,
        "out_of_sample",
        "expectancy_r",
    )
    oos_expectancy = _period_metric(periods, "out_of_sample", "expectancy_r")
    oos_accepted = next(
        (item.accepted_trades for item in periods if item.period == "out_of_sample"),
        0,
    )

    if train_delta > 0 and oos_delta < 0:
        return (
            RECOMMEND_OVERFIT_RISK,
            "In-sample improves while out-of-sample degrades versus baseline.",
        )

    if train_delta > 0 and oos_accepted >= 2 and oos_expectancy < 0:
        return (
            RECOMMEND_OVERFIT_RISK,
            "In-sample improves but out-of-sample expectancy remains negative.",
        )

    if oos_accepted < 2:
        return RECOMMEND_NEEDS_MORE_DATA, None

    if oos_delta >= 0.15:
        return RECOMMEND_PROMOTE, None

    if oos_delta < -0.25:
        return RECOMMEND_REJECT, None

    return RECOMMEND_KEEP_BASELINE, None


def _final_recommendation(results: list[VariantResult]) -> str:
    if any(item.recommendation == RECOMMEND_PROMOTE for item in results):
        return RECOMMEND_PROMOTE
    if any(item.recommendation == RECOMMEND_OVERFIT_RISK for item in results):
        return RECOMMEND_OVERFIT_RISK
    if any(item.recommendation == RECOMMEND_NEEDS_MORE_DATA for item in results):
        return RECOMMEND_NEEDS_MORE_DATA
    return RECOMMEND_KEEP_BASELINE


def analyze(evidence_path: Path) -> BT133Report:
    evidence = _load_evidence(evidence_path)
    rows = _assign_periods(list(evidence["results"]))
    bounds = _period_bounds(rows)
    variant_results: list[VariantResult] = []
    baseline_periods: list[PeriodMetrics] | None = None

    for spec in _variant_grid():
        missing = _missing_fields(rows, spec.required_fields)
        status = STATUS_EVALUATED if not missing else STATUS_SKIPPED
        limitations: list[str] = []

        if spec.family in {"next_bar_close_confirmation", "volatility_adjusted_confirmation"}:
            limitations.append(
                "BT131/BT136 evidence has MAE/MFE summaries, not exact intrabar path ordering; "
                "result is research proxy only."
            )

        if missing:
            limitations.append(
                "Variant skipped because required evidence fields are missing from all source rows."
            )

        periods = [_metrics_for_period(rows, period, spec, status) for period in PERIOD_NAMES]

        if spec.family == "baseline":
            recommendation, overfit = RECOMMEND_KEEP_BASELINE, None
            baseline_periods = periods
        else:
            recommendation, overfit = _recommend(spec, periods, baseline_periods)
            if status != STATUS_EVALUATED:
                recommendation, overfit = RECOMMEND_NEEDS_MORE_DATA, None

        variant_results.append(
            VariantResult(
                spec.variant_id,
                spec.family,
                spec.description,
                spec.parameters,
                status,
                missing,
                limitations,
                recommendation,
                overfit,
                periods,
            )
        )

    return BT133Report(
        report_version="bt133.v1",
        source_evidence=str(evidence_path),
        run_id=str(evidence.get("run_id")),
        data_source=str(evidence.get("data_source")),
        is_demo=bool(evidence.get("is_demo")),
        input_pack_gate_status=str(evidence.get("input_pack_gate_status")),
        input_completeness_status=str(evidence.get("input_completeness_status")),
        run_health_status=str(evidence.get("run_health_status")),
        live_trading_authorized=bool(evidence.get("live_trading_authorized")),
        broker_execution_mode=str(evidence.get("broker_execution_mode")),
        total_source_trades=len(rows),
        walk_forward_periods=bounds,
        variant_results=variant_results,
        final_recommendation=_final_recommendation(variant_results),
        safety_notes=[
            "Research only. No production entry rule change.",
            "No live trading authorization.",
            "broker_execution_mode remains paper_only.",
            "Promotion requires a separate guarded issue with before/after evidence.",
        ],
    )


def _markdown_table(headers: list[str], rows: list[list[Any]]) -> list[str]:
    lines = [
        "| " + " | ".join(headers) + " |",
        "|" + "|".join("---" for _ in headers) + "|",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(cell) for cell in row) + " |")
    return lines


def render_markdown(report: BT133Report) -> str:
    lines = [
        "# BT133 Entry Confirmation Variant Report",
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
        f"- Live trading authorized: {report.live_trading_authorized}",
        f"- Broker execution mode: {report.broker_execution_mode}",
        f"- Total source trades: {report.total_source_trades}",
        f"- Final recommendation: {report.final_recommendation}",
        "",
        "## Walk-forward Periods",
        "",
    ]

    lines.extend(
        _markdown_table(
            ["Period", "Start", "End"],
            [
                [period, bounds.get("start_date"), bounds.get("end_date")]
                for period, bounds in report.walk_forward_periods.items()
            ],
        )
    )

    lines.extend(["", "## Variant Results", ""])

    for result in report.variant_results:
        lines.extend(
            [
                f"### {result.variant_id}",
                "",
                f"- Family: {result.family}",
                f"- Status: {result.status}",
                f"- Recommendation: {result.recommendation}",
                f"- Parameters: `{json.dumps(result.parameters, sort_keys=True)}`",
                "- Missing fields: "
                + (", ".join(result.missing_fields) if result.missing_fields else "none"),
            ]
        )

        if result.overfit_warning:
            lines.append(f"- Overfit warning: {result.overfit_warning}")

        for limitation in result.limitations:
            lines.append(f"- Limitation: {limitation}")

        lines.append("")
        lines.extend(
            _markdown_table(
                [
                    "Period",
                    "Considered",
                    "Accepted",
                    "Skipped",
                    "False BO",
                    "Stop",
                    "T1",
                    "T2",
                    "Avg R",
                    "Expectancy R",
                ],
                [
                    [
                        p.period,
                        p.total_trades_considered,
                        p.accepted_trades,
                        p.skipped_trades,
                        p.false_breakout_rate,
                        p.stop_hit_rate,
                        p.target_1_hit_rate,
                        p.target_2_hit_rate,
                        p.average_r,
                        p.expectancy_r,
                    ]
                    for p in result.periods
                ],
            )
        )
        lines.append("")

    lines.extend(["## Safety Notes", ""])

    for note in report.safety_notes:
        lines.append(f"- {note}")

    return "\n".join(lines).rstrip() + "\n"


def write_report(report: BT133Report, *, output_json: Path, output_md: Path) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(
        json.dumps(asdict(report), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    output_md.write_text(render_markdown(report), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyze BT131/BT136 evidence into BT133 entry-confirmation variant reports"
    )
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = analyze(args.evidence)
    write_report(report, output_json=args.output_json, output_md=args.output_md)
    print(json.dumps({"status": report.final_recommendation, "variants": len(report.variant_results)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())