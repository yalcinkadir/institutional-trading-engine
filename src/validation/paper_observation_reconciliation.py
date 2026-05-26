from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import Any, Iterable


@dataclass(frozen=True)
class PaperObservationConfig:
    min_observation_days: int = 63
    target_observation_days: int = 126
    max_action_mismatch_rate: float = 0.05
    max_abs_daily_drift_r: float = 1.0
    max_unresolved_records: int = 0
    require_observation_only: bool = True


@dataclass(frozen=True)
class DailyReconciliationSummary:
    observation_date: str
    records: int
    action_matches: int
    action_mismatches: int
    unresolved_records: int
    expected_total_r: float
    paper_total_r: float
    drift_r: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PaperObservationMetrics:
    observation_days: int
    target_observation_days: int
    first_observation_date: str | None
    last_observation_date: str | None
    total_records: int
    resolved_records: int
    unresolved_records: int
    action_matches: int
    action_mismatches: int
    action_mismatch_rate: float
    expected_total_r: float
    paper_total_r: float
    total_drift_r: float
    mean_daily_drift_r: float
    max_abs_daily_drift_r: float
    daily_summaries: list[DailyReconciliationSummary] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["daily_summaries"] = [summary.to_dict() for summary in self.daily_summaries]
        return data


@dataclass(frozen=True)
class PaperObservationGate:
    name: str
    passed: bool
    value: float | int | str | bool | None
    threshold: float | int | str | bool | None
    message: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PaperObservationReport:
    passed: bool
    observation_only: bool
    metrics: PaperObservationMetrics
    gates: list[PaperObservationGate] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "observation_only": self.observation_only,
            "metrics": self.metrics.to_dict(),
            "gates": [gate.to_dict() for gate in self.gates],
        }


def reconcile_paper_observation(
    records: Iterable[dict[str, Any]],
    *,
    config: PaperObservationConfig = PaperObservationConfig(),
    observation_only: bool = True,
) -> PaperObservationReport:
    normalized_records = [_normalize_record(record) for record in records if isinstance(record, dict)]
    daily_summaries = _build_daily_summaries(normalized_records)
    metrics = _calculate_metrics(daily_summaries, config=config)
    gates = _build_gates(metrics, config=config, observation_only=observation_only)
    return PaperObservationReport(
        passed=all(gate.passed for gate in gates),
        observation_only=observation_only,
        metrics=metrics,
        gates=gates,
    )


def render_paper_observation_markdown(report: PaperObservationReport) -> str:
    metrics = report.metrics
    lines = [
        "# Paper Observation Daily Reconciliation",
        "",
        f"Status: **{'PASS' if report.passed else 'FAIL'}**",
        f"Observation-only mode: **{str(report.observation_only).lower()}**",
        "",
        "## Metrics",
        "",
        f"- Observation days: {metrics.observation_days} / {metrics.target_observation_days}",
        f"- First observation date: {metrics.first_observation_date or 'n/a'}",
        f"- Last observation date: {metrics.last_observation_date or 'n/a'}",
        f"- Total records: {metrics.total_records}",
        f"- Resolved records: {metrics.resolved_records}",
        f"- Unresolved records: {metrics.unresolved_records}",
        f"- Action matches: {metrics.action_matches}",
        f"- Action mismatches: {metrics.action_mismatches}",
        f"- Action mismatch rate: {metrics.action_mismatch_rate:.2%}",
        f"- Expected total R: {metrics.expected_total_r:.4f}",
        f"- Paper total R: {metrics.paper_total_r:.4f}",
        f"- Total drift R: {metrics.total_drift_r:.4f}",
        f"- Mean daily drift R: {metrics.mean_daily_drift_r:.4f}",
        f"- Max absolute daily drift R: {metrics.max_abs_daily_drift_r:.4f}",
        "",
        "## Gates",
        "",
        "| Gate | Status | Value | Threshold |",
        "|---|---:|---:|---:|",
    ]
    for gate in report.gates:
        lines.append(
            f"| {gate.name} | {'PASS' if gate.passed else 'FAIL'} | "
            f"{_format_value(gate.value)} | {_format_value(gate.threshold)} |"
        )
    return "\n".join(lines).rstrip() + "\n"


def write_paper_observation_report(
    report: PaperObservationReport,
    *,
    json_path: Path,
    markdown_path: Path,
) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report.to_dict(), indent=2), encoding="utf-8")
    markdown_path.write_text(render_paper_observation_markdown(report), encoding="utf-8")


def _build_gates(
    metrics: PaperObservationMetrics,
    *,
    config: PaperObservationConfig,
    observation_only: bool,
) -> list[PaperObservationGate]:
    return [
        PaperObservationGate(
            name="observation_only_mode",
            passed=(not config.require_observation_only) or observation_only,
            value=observation_only,
            threshold=True,
            message="Phase B1 must remain observation-only.",
        ),
        PaperObservationGate(
            name="minimum_observation_days",
            passed=metrics.observation_days >= config.min_observation_days,
            value=metrics.observation_days,
            threshold=config.min_observation_days,
            message="Forward paper observation must run long enough before evidence is trusted.",
        ),
        PaperObservationGate(
            name="unresolved_records",
            passed=metrics.unresolved_records <= config.max_unresolved_records,
            value=metrics.unresolved_records,
            threshold=config.max_unresolved_records,
            message="Every expected/paper record should be reconciled daily.",
        ),
        PaperObservationGate(
            name="action_mismatch_rate",
            passed=metrics.action_mismatch_rate <= config.max_action_mismatch_rate,
            value=metrics.action_mismatch_rate,
            threshold=config.max_action_mismatch_rate,
            message="Paper action stream should match the expected stream within tolerance.",
        ),
        PaperObservationGate(
            name="max_abs_daily_drift_r",
            passed=metrics.max_abs_daily_drift_r <= config.max_abs_daily_drift_r,
            value=metrics.max_abs_daily_drift_r,
            threshold=config.max_abs_daily_drift_r,
            message="Daily paper-vs-expected R drift should remain within tolerance.",
        ),
    ]


def _calculate_metrics(
    daily_summaries: list[DailyReconciliationSummary],
    *,
    config: PaperObservationConfig,
) -> PaperObservationMetrics:
    observation_days = len(daily_summaries)
    total_records = sum(summary.records for summary in daily_summaries)
    unresolved_records = sum(summary.unresolved_records for summary in daily_summaries)
    resolved_records = max(0, total_records - unresolved_records)
    action_matches = sum(summary.action_matches for summary in daily_summaries)
    action_mismatches = sum(summary.action_mismatches for summary in daily_summaries)
    compared_actions = action_matches + action_mismatches
    action_mismatch_rate = action_mismatches / compared_actions if compared_actions else 0.0
    expected_total_r = sum(summary.expected_total_r for summary in daily_summaries)
    paper_total_r = sum(summary.paper_total_r for summary in daily_summaries)
    total_drift_r = paper_total_r - expected_total_r
    mean_daily_drift_r = total_drift_r / observation_days if observation_days else 0.0
    max_abs_daily_drift_r = max((abs(summary.drift_r) for summary in daily_summaries), default=0.0)
    first_date = daily_summaries[0].observation_date if daily_summaries else None
    last_date = daily_summaries[-1].observation_date if daily_summaries else None
    return PaperObservationMetrics(
        observation_days=observation_days,
        target_observation_days=config.target_observation_days,
        first_observation_date=first_date,
        last_observation_date=last_date,
        total_records=total_records,
        resolved_records=resolved_records,
        unresolved_records=unresolved_records,
        action_matches=action_matches,
        action_mismatches=action_mismatches,
        action_mismatch_rate=round(action_mismatch_rate, 6),
        expected_total_r=round(expected_total_r, 6),
        paper_total_r=round(paper_total_r, 6),
        total_drift_r=round(total_drift_r, 6),
        mean_daily_drift_r=round(mean_daily_drift_r, 6),
        max_abs_daily_drift_r=round(max_abs_daily_drift_r, 6),
        daily_summaries=daily_summaries,
    )


def _build_daily_summaries(records: list[dict[str, Any]]) -> list[DailyReconciliationSummary]:
    by_date: dict[str, list[dict[str, Any]]] = {}
    for record in records:
        by_date.setdefault(record["observation_date"], []).append(record)
    summaries: list[DailyReconciliationSummary] = []
    for observation_date in sorted(by_date):
        date_records = by_date[observation_date]
        unresolved_records = sum(1 for record in date_records if record["unresolved"])
        action_matches = sum(1 for record in date_records if record["action_compared"] and record["action_match"])
        action_mismatches = sum(1 for record in date_records if record["action_compared"] and not record["action_match"])
        expected_total_r = sum(record["expected_r"] for record in date_records if not record["unresolved"])
        paper_total_r = sum(record["paper_r"] for record in date_records if not record["unresolved"])
        summaries.append(
            DailyReconciliationSummary(
                observation_date=observation_date,
                records=len(date_records),
                action_matches=action_matches,
                action_mismatches=action_mismatches,
                unresolved_records=unresolved_records,
                expected_total_r=round(expected_total_r, 6),
                paper_total_r=round(paper_total_r, 6),
                drift_r=round(paper_total_r - expected_total_r, 6),
            )
        )
    return summaries


def _normalize_record(record: dict[str, Any]) -> dict[str, Any]:
    observation_date = _normalize_date(record.get("observation_date") or record.get("date"))
    expected_action = _normalize_action(record.get("expected_action") or record.get("backtest_action"))
    paper_action = _normalize_action(record.get("paper_action") or record.get("observed_action"))
    expected_r = _safe_float(record.get("expected_r", record.get("backtest_r")))
    paper_r = _safe_float(record.get("paper_r", record.get("observed_r")))
    unresolved = expected_action is None or paper_action is None or expected_r is None or paper_r is None
    action_compared = expected_action is not None and paper_action is not None
    return {
        "observation_date": observation_date,
        "expected_action": expected_action,
        "paper_action": paper_action,
        "expected_r": expected_r if expected_r is not None else 0.0,
        "paper_r": paper_r if paper_r is not None else 0.0,
        "unresolved": unresolved,
        "action_compared": action_compared,
        "action_match": bool(action_compared and expected_action == paper_action),
    }


def _normalize_date(value: Any) -> str:
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return "unknown"
        try:
            return datetime.fromisoformat(text.replace("Z", "+00:00")).date().isoformat()
        except ValueError:
            return text[:10]
    return "unknown"


def _normalize_action(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip().lower().replace(" ", "_").replace("-", "_")
    if not text:
        return None
    aliases = {
        "buy": "enter_long",
        "long": "enter_long",
        "entry": "enter_long",
        "enter": "enter_long",
        "enter_long": "enter_long",
        "skip": "skip",
        "no_action": "skip",
        "hold": "hold",
        "exit": "exit",
    }
    return aliases.get(text, text)


def _safe_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _format_value(value: Any) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, float):
        return f"{value:.4f}"
    if value is None:
        return "n/a"
    return str(value)
