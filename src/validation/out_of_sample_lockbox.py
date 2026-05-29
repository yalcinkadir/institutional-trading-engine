from __future__ import annotations

import hashlib
import json
import math
from dataclasses import asdict, dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import Any, Iterable

from src.config.thresholds import DEFAULT_THRESHOLDS
from src.validation.historical_edge_validation import (
    HistoricalEdgeValidationConfig,
    HistoricalEdgeValidationReport,
    calculate_profit_factor_degradation,
    validate_historical_edge,
)

DEFAULT_OOS_SPLIT_DATE = date(2024, 1, 1)
MAX_CORE_METRIC_DEGRADATION = 0.20
VALIDATION_METHOD = "fixed_date_holdout_degradation_check"
VALIDATION_SCOPE_NOTE = (
    "Fixed-date holdout degradation check only. This is not walk-forward optimization, "
    "not k-fold cross-validation, and not proof against overfitting."
)
THRESHOLD_VERSION_FIELDS = (
    "thresholds_version",
    "threshold_version",
    "decision_thresholds_version",
)


@dataclass(frozen=True)
class OutOfSampleLockboxConfig:
    split_date: date = DEFAULT_OOS_SPLIT_DATE
    max_core_metric_degradation: float = MAX_CORE_METRIC_DEGRADATION
    edge_config: HistoricalEdgeValidationConfig = HistoricalEdgeValidationConfig()
    threshold_version: str = DEFAULT_THRESHOLDS.version
    require_matching_record_threshold_version: bool = False


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
        return _json_safe(asdict(self))


@dataclass(frozen=True)
class OutOfSampleLockboxReport:
    passed: bool
    split_date: str
    threshold_version: str
    evidence_contract_hash: str
    in_sample_count: int
    out_of_sample_count: int
    unassigned_records: int
    in_sample_report: HistoricalEdgeValidationReport
    out_of_sample_report: HistoricalEdgeValidationReport
    validation_method: str = VALIDATION_METHOD
    validation_scope_note: str = VALIDATION_SCOPE_NOTE
    degradation_checks: list[MetricDegradation] = field(default_factory=list)
    invalidation_reasons: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "validation_method": self.validation_method,
            "validation_scope_note": self.validation_scope_note,
            "split_date": self.split_date,
            "threshold_version": self.threshold_version,
            "evidence_contract_hash": self.evidence_contract_hash,
            "in_sample_count": self.in_sample_count,
            "out_of_sample_count": self.out_of_sample_count,
            "unassigned_records": self.unassigned_records,
            "in_sample_report": self.in_sample_report.to_dict(),
            "out_of_sample_report": self.out_of_sample_report.to_dict(),
            "degradation_checks": [check.to_dict() for check in self.degradation_checks],
            "invalidation_reasons": list(self.invalidation_reasons),
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
    invalidation_reasons = build_invalidation_reasons(
        [*in_sample_records, *out_of_sample_records],
        config=config,
    )
    passed = (
        not invalidation_reasons
        and in_sample_report.passed
        and out_of_sample_report.passed
        and all(check.passed for check in degradation_checks)
    )

    return OutOfSampleLockboxReport(
        passed=passed,
        split_date=config.split_date.isoformat(),
        threshold_version=config.threshold_version,
        evidence_contract_hash=build_evidence_contract_hash(config),
        in_sample_count=len(in_sample_records),
        out_of_sample_count=len(out_of_sample_records),
        unassigned_records=unassigned_records,
        in_sample_report=in_sample_report,
        out_of_sample_report=out_of_sample_report,
        degradation_checks=degradation_checks,
        invalidation_reasons=tuple(invalidation_reasons),
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
        _profit_factor_check(
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


def build_invalidation_reasons(
    assigned_records: Iterable[dict[str, Any]],
    *,
    config: OutOfSampleLockboxConfig,
) -> list[str]:
    reasons: list[str] = []

    if config.threshold_version != DEFAULT_THRESHOLDS.version:
        reasons.append(
            f"stale_threshold_version:{config.threshold_version}!={DEFAULT_THRESHOLDS.version}"
        )

    if not config.require_matching_record_threshold_version:
        return reasons

    observed_versions = _collect_record_threshold_versions(assigned_records)
    if not observed_versions:
        reasons.append("missing_record_threshold_versions")
        return reasons

    mismatched_versions = sorted(version for version in observed_versions if version != config.threshold_version)
    if mismatched_versions:
        reasons.append(
            "record_threshold_version_mismatch:"
            + ",".join(mismatched_versions)
            + f"!={config.threshold_version}"
        )

    return reasons


def build_evidence_contract_hash(config: OutOfSampleLockboxConfig) -> str:
    payload = {
        "split_date": config.split_date.isoformat(),
        "max_core_metric_degradation": config.max_core_metric_degradation,
        "edge_config": asdict(config.edge_config),
        "threshold_version": config.threshold_version,
        "require_matching_record_threshold_version": config.require_matching_record_threshold_version,
        "validation_method": VALIDATION_METHOD,
        "validation_scope_note": VALIDATION_SCOPE_NOTE,
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def render_out_of_sample_lockbox_markdown(report: OutOfSampleLockboxReport) -> str:
    lines = [
        "# Fixed-Date Holdout Validation Lockbox",
        "",
        f"Status: **{'PASS' if report.passed else 'FAIL'}**",
        f"Validation method: `{report.validation_method}`",
        f"Validation scope: {report.validation_scope_note}",
        f"Split date: `{report.split_date}`",
        f"Threshold version: `{report.threshold_version}`",
        f"Evidence contract hash: `{report.evidence_contract_hash}`",
        f"In-sample records: **{report.in_sample_count}**",
        f"Holdout records: **{report.out_of_sample_count}**",
        f"Unassigned records: **{report.unassigned_records}**",
        "",
    ]
    if report.invalidation_reasons:
        lines.extend(
            [
                "## Invalidation Reasons",
                "",
                *[f"- `{reason}`" for reason in report.invalidation_reasons],
                "",
            ]
        )
    lines.extend(
        [
            "## Core Metrics",
            "",
            "| Segment | Trades | Expectancy R | Profit Factor | Max DD R | Sharpe |",
            "|---|---:|---:|---:|---:|---:|",
            _metrics_row("in_sample", report.in_sample_report),
            _metrics_row("fixed_date_holdout", report.out_of_sample_report),
            "",
            "## Degradation Checks",
            "",
            "| Metric | Status | In-Sample | Holdout | Degradation | Max Allowed |",
            "|---|---:|---:|---:|---:|---:|",
        ]
    )
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
    json_path.write_text(json.dumps(report.to_dict(), indent=2, allow_nan=False), encoding="utf-8")
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


def _profit_factor_check(
    in_sample_value: float,
    out_of_sample_value: float,
    max_allowed_degradation: float,
) -> MetricDegradation:
    degradation = calculate_profit_factor_degradation(out_of_sample_value, in_sample_value)
    return MetricDegradation(
        metric="profit_factor",
        in_sample_value=round(float(in_sample_value), 6),
        out_of_sample_value=round(float(out_of_sample_value), 6),
        degradation=degradation,
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


def _collect_record_threshold_versions(records: Iterable[dict[str, Any]]) -> set[str]:
    versions: set[str] = set()
    for record in records:
        for field in THRESHOLD_VERSION_FIELDS:
            value = record.get(field)
            if isinstance(value, str) and value.strip():
                versions.add(value.strip())
                break
    return versions


def _format_number(value: float | int) -> str:
    if isinstance(value, float) and math.isinf(value):
        return "inf" if value > 0 else "-inf"
    if isinstance(value, int):
        return str(value)
    return f"{float(value):.4f}"


def _json_safe(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: _json_safe(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_json_safe(item) for item in value]
    if isinstance(value, tuple):
        return [_json_safe(item) for item in value]
    if isinstance(value, float):
        if math.isinf(value):
            return "inf" if value > 0 else "-inf"
        if math.isnan(value):
            return "nan"
    return value
