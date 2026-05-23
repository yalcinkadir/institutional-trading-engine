from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import Any, Iterable

from src.validation.historical_edge_validation import (
    HistoricalEdgeValidationConfig,
    HistoricalEdgeValidationReport,
    validate_historical_edge,
)

DEFAULT_OOS_SPLIT_DATE = date(2024, 1, 1)
MAX_CORE_METRIC_DEGRADATION = 0.20


@dataclass(frozen=True)
class OutOfSampleLockboxConfig:
    split_date: date = DEFAULT_OOS_SPLIT_DATE
    max_core_metric_degradation: float = MAX_CORE_METRIC_DEGRADATION
    edge_config: HistoricalEdgeValidationConfig = HistoricalEdgeValidationConfig()


@dataclass(frozen=True)
class MetricDegradation:
    metric: str
    in_sample_value: float
    out_of_sample_value: float
    degradation: float
    max_allowed_degradation: float
    passed: bool
    higher_is_better: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class OutOfSampleLockboxReport:
    passed: bool
    split_date: str
    in_sample_count: int
    out_of_sample_count: int
    unassigned_records: int
    in_sample_report: HistoricalEdgeValidationReport
    out_of_sample_report: HistoricalEdgeValidationReport
    degradation_checks: list[MetricDegradation] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "split_date": self.split_date,
            "in_sample_count": self.in_sample_count,
            "out_of_sample_count": self.out_of_sample_count,
            "unassigned_records": self.unassigned_records,
            "in_sample_report": self.in_sample_report.to_dict(),
            "out_of_sample_report": self.out_of_sample_report.to_dict(),
            "degradation_checks": [check.to_dict() for check in self.degradation_checks],
        }


def build_out_of_sample_lockbox(
    records: Iterable[dict[str, Any]],
    *,
    config: OutOfSampleLockboxConfig = OutOfSampleLockboxConfig(),
    date_field: str = "exit_date",
    fallback_date_fields: tuple[str, ...] = ("closed_at", "signal_date", "date"),
    result_field: str = "result_r",
) -> OutOfSampleLockboxReport:
    in_sample_records: list[dict[str, Any]] = []
    out_of_sample_records: list[dict[str, Any]] = []
    unassigned_records = 0

    for record in records:
        if not isinstance(record, dict):
            unassigned_records += 1
            continue
        record_date = _extract_record_date(record, primary_field=date_field, fallback_fields=fallback_date_fields)
        if record_date is None:
            unassigned_records += 1
            continue
        if record_date < config.split_date:
            in_sample_records.append(dict(record))
        else:
            out_of_sample_records.append(dict(record))

    in_sample_report = validate_historical_edge(
        in_sample_records,
        config=config.edge_config,
        result_field=result_field,
    )
    out_of_sample_report = validate_historical_edge(
        out_of_sample_records,
        config=config.edge_config,
        result_field=result_field,
    )
    degradation_checks = build_degradation_checks(
        in_sample_report,
        out_of_sample_report,
        max_allowed_degradation=config.max_core_metric_degradation,
    )
    passed = (
        in_sample_report.passed
        and out_of_sample_report.passed
        and all(check.passed for check in degradation_checks)
    )

    return OutOfSampleLockboxReport(
        passed=passed,
        split_date=config.split_date.isoformat(),
        in_sample_count=len(in_sample_records),
        out_of_sample_count=len(out_of_sample_records),
        unassigned_records=unassigned_records,
        in_sample_report=in_sample_report,
        out_of_sample_report=out_of_sample_report,
        degradation_checks=degradation_checks,
    )


def build_degradation_checks(
    in_sample_report: HistoricalEdgeValidationReport,
    out_of_sample_report: HistoricalEdgeValidationReport,
    *,
    max_allowed_degradation: float = MAX_CORE_METRIC_DEGRADATION,
) -> list[MetricDegradation]:
    in_metrics = in_sample_report.metrics
    oos_metrics = out_of_sample_report.metrics
    return [
        _higher_is_better_check(
            "expectancy_r",
            in_metrics.expectancy_r,
            oos_metrics.expectancy_r,
            max_allowed_degradation,
        ),
        _higher_is_better_check(
            "profit_factor",
            in_metrics.profit_factor,
            oos_metrics.profit_factor,
            max_allowed_degradation,
        ),
        _higher_is_better_check(
            "sharpe_ratio",
            in_metrics.sharpe_ratio,
            oos_metrics.sharpe_ratio,
            max_allowed_degradation,
        ),
        _lower_is_better_check(
            "max_drawdown",
            in_metrics.max_drawdown,
            oos_metrics.max_drawdown,
            max_allowed_degradation,
        ),
    ]


def render_out_of_sample_lockbox_markdown(report: OutOfSampleLockboxReport) -> str:
    lines = [
        "# Out-of-Sample Validation Lockbox",
        "",
        f"Status: **{'PASS' if report.passed else 'FAIL'}**",
        f"Split date: `{report.split_date}`",
        f"In-sample records: **{report.in_sample_count}**",
        f"Out-of-sample records: **{report.out_of_sample_count}**",
        f"Unassigned records: **{report.unassigned_records}**",
        "",
        "## Core Metrics",
        "",
        "| Segment | Trades | Expectancy R | Profit Factor | Max DD R | Sharpe |",
        "|---|---:|---:|---:|---:|---:|",
        _metrics_row("in_sample", report.in_sample_report),
        _metrics_row("out_of_sample", report.out_of_sample_report),
        "",
        "## Degradation Checks",
        "",
        "| Metric | Status | In-Sample | OOS | Degradation | Max Allowed |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for check in report.degradation_checks:
        lines.append(
            f"| {check.metric} | {'PASS' if check.passed else 'FAIL'} | "
            f"{_format_number(check.in_sample_value)} | {_format_number(check.out_of_sample_value)} | "
            f"{check.degradation:.2%} | {check.max_allowed_degradation:.2%} |"
        )
    return "\n".join(lines).rstrip() + "\n"


def write_out_of_sample_lockbox_report(
    report: OutOfSampleLockboxReport,
    *,
    json_path: Path,
    markdown_path: Path,
) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report.to_dict(), indent=2), encoding="utf-8")
    markdown_path.write_text(render_out_of_sample_lockbox_markdown(report), encoding="utf-8")


def _higher_is_better_check(
    metric: str,
    in_sample_value: float,
    out_of_sample_value: float,
    max_allowed_degradation: float,
) -> MetricDegradation:
    baseline = max(abs(in_sample_value), 1e-9)
    degradation = max(0.0, (in_sample_value - out_of_sample_value) / baseline)
    return MetricDegradation(
        metric=metric,
        in_sample_value=round(float(in_sample_value), 6),
        out_of_sample_value=round(float(out_of_sample_value), 6),
        degradation=round(degradation, 6),
        max_allowed_degradation=max_allowed_degradation,
        passed=degradation <= max_allowed_degradation,
        higher_is_better=True,
    )


def _lower_is_better_check(
    metric: str,
    in_sample_value: float,
    out_of_sample_value: float,
    max_allowed_degradation: float,
) -> MetricDegradation:
    baseline = max(abs(in_sample_value), 1e-9)
    degradation = max(0.0, (out_of_sample_value - in_sample_value) / baseline)
    return MetricDegradation(
        metric=metric,
        in_sample_value=round(float(in_sample_value), 6),
        out_of_sample_value=round(float(out_of_sample_value), 6),
        degradation=round(degradation, 6),
        max_allowed_degradation=max_allowed_degradation,
        passed=degradation <= max_allowed_degradation,
        higher_is_better=False,
    )


def _metrics_row(label: str, report: HistoricalEdgeValidationReport) -> str:
    metrics = report.metrics
    return (
        f"| {label} | {metrics.total_trades} | {metrics.expectancy_r:.4f} | "
        f"{_format_number(metrics.profit_factor)} | {metrics.max_drawdown:.4f} | "
        f"{metrics.sharpe_ratio:.4f} |"
    )


def _extract_record_date(
    record: dict[str, Any],
    *,
    primary_field: str,
    fallback_fields: tuple[str, ...],
) -> date | None:
    for field in (primary_field, *fallback_fields):
        parsed = _parse_date(record.get(field))
        if parsed is not None:
            return parsed
    return None


def _parse_date(value: Any) -> date | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return None
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"
        try:
            return datetime.fromisoformat(text).date()
        except ValueError:
            try:
                return date.fromisoformat(text[:10])
            except ValueError:
                return None
    return None


def _format_number(value: float | int) -> str:
    if isinstance(value, float) and value == float("inf"):
        return "inf"
    if isinstance(value, int):
        return str(value)
    return f"{float(value):.4f}"
