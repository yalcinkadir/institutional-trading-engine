from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any, Iterable

from src.validation.historical_edge_validation import (
    HistoricalEdgeValidationConfig,
    HistoricalEdgeValidationReport,
    validate_historical_edge,
)

DEFAULT_TRAINING_MONTHS = 18
DEFAULT_TEST_MONTHS = 6
DEFAULT_STEP_MONTHS = 3
MIN_WALK_FORWARD_CYCLES = 6


@dataclass(frozen=True)
class WalkForwardConfig:
    training_months: int = DEFAULT_TRAINING_MONTHS
    test_months: int = DEFAULT_TEST_MONTHS
    step_months: int = DEFAULT_STEP_MONTHS
    min_cycles: int = MIN_WALK_FORWARD_CYCLES
    edge_config: HistoricalEdgeValidationConfig = HistoricalEdgeValidationConfig()


@dataclass(frozen=True)
class WalkForwardCycle:
    cycle_number: int
    training_start: date
    training_end: date
    test_start: date
    test_end: date

    def to_dict(self) -> dict[str, Any]:
        return {
            "cycle_number": self.cycle_number,
            "training_start": self.training_start.isoformat(),
            "training_end": self.training_end.isoformat(),
            "test_start": self.test_start.isoformat(),
            "test_end": self.test_end.isoformat(),
        }


@dataclass(frozen=True)
class WalkForwardCycleResult:
    cycle: WalkForwardCycle
    training_records: int
    test_records: int
    validation_report: HistoricalEdgeValidationReport

    @property
    def passed(self) -> bool:
        return self.validation_report.passed

    def to_dict(self) -> dict[str, Any]:
        return {
            "cycle": self.cycle.to_dict(),
            "training_records": self.training_records,
            "test_records": self.test_records,
            "passed": self.passed,
            "validation_report": self.validation_report.to_dict(),
        }


@dataclass(frozen=True)
class WalkForwardValidationReport:
    passed: bool
    generated_cycles: int
    passing_cycles: int
    min_required_cycles: int
    min_required_passing_cycles: int
    unassigned_records: int
    cycle_results: list[WalkForwardCycleResult] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "generated_cycles": self.generated_cycles,
            "passing_cycles": self.passing_cycles,
            "min_required_cycles": self.min_required_cycles,
            "min_required_passing_cycles": self.min_required_passing_cycles,
            "unassigned_records": self.unassigned_records,
            "cycle_results": [result.to_dict() for result in self.cycle_results],
        }


def build_walk_forward_validation(
    records: Iterable[dict[str, Any]],
    *,
    config: WalkForwardConfig = WalkForwardConfig(),
    start_date: date | str | None = None,
    end_date: date | str | None = None,
    date_field: str = "exit_date",
    fallback_date_fields: tuple[str, ...] = ("closed_at", "signal_date", "date"),
    result_field: str = "result_r",
    min_required_passing_cycles: int | None = None,
) -> WalkForwardValidationReport:
    dated_records, unassigned_records = _extract_dated_records(
        records,
        primary_field=date_field,
        fallback_fields=fallback_date_fields,
    )

    if not dated_records:
        return WalkForwardValidationReport(
            passed=False,
            generated_cycles=0,
            passing_cycles=0,
            min_required_cycles=config.min_cycles,
            min_required_passing_cycles=min_required_passing_cycles or config.min_cycles,
            unassigned_records=unassigned_records,
            cycle_results=[],
        )

    first_date = _parse_date(start_date) or min(item[0] for item in dated_records)
    last_date = _parse_date(end_date) or max(item[0] for item in dated_records)
    cycles = generate_walk_forward_cycles(
        start_date=first_date,
        end_date=last_date,
        training_months=config.training_months,
        test_months=config.test_months,
        step_months=config.step_months,
    )

    cycle_results: list[WalkForwardCycleResult] = []
    for cycle in cycles:
        training_records = [
            record
            for record_date, record in dated_records
            if cycle.training_start <= record_date <= cycle.training_end
        ]
        test_records = [
            record
            for record_date, record in dated_records
            if cycle.test_start <= record_date <= cycle.test_end
        ]
        validation_report = validate_historical_edge(
            test_records,
            config=config.edge_config,
            result_field=result_field,
        )
        cycle_results.append(
            WalkForwardCycleResult(
                cycle=cycle,
                training_records=len(training_records),
                test_records=len(test_records),
                validation_report=validation_report,
            )
        )

    passing_cycles = sum(1 for result in cycle_results if result.passed)
    required_passing = min_required_passing_cycles or config.min_cycles
    passed = len(cycle_results) >= config.min_cycles and passing_cycles >= required_passing

    return WalkForwardValidationReport(
        passed=passed,
        generated_cycles=len(cycle_results),
        passing_cycles=passing_cycles,
        min_required_cycles=config.min_cycles,
        min_required_passing_cycles=required_passing,
        unassigned_records=unassigned_records,
        cycle_results=cycle_results,
    )


def generate_walk_forward_cycles(
    *,
    start_date: date,
    end_date: date,
    training_months: int = DEFAULT_TRAINING_MONTHS,
    test_months: int = DEFAULT_TEST_MONTHS,
    step_months: int = DEFAULT_STEP_MONTHS,
) -> list[WalkForwardCycle]:
    if training_months <= 0 or test_months <= 0 or step_months <= 0:
        raise ValueError("training_months, test_months and step_months must be greater than 0")

    cycles: list[WalkForwardCycle] = []
    cycle_number = 1
    training_start = start_date

    while True:
        test_start = _add_months(training_start, training_months)
        training_end = test_start - timedelta(days=1)
        test_end = _add_months(test_start, test_months) - timedelta(days=1)

        if test_end > end_date:
            break

        cycles.append(
            WalkForwardCycle(
                cycle_number=cycle_number,
                training_start=training_start,
                training_end=training_end,
                test_start=test_start,
                test_end=test_end,
            )
        )
        cycle_number += 1
        training_start = _add_months(training_start, step_months)

    return cycles


def render_walk_forward_markdown(report: WalkForwardValidationReport) -> str:
    lines = [
        "# Walk-Forward Validation",
        "",
        f"Status: **{'PASS' if report.passed else 'FAIL'}**",
        f"Generated cycles: **{report.generated_cycles}**",
        f"Passing cycles: **{report.passing_cycles}**",
        f"Minimum required cycles: **{report.min_required_cycles}**",
        f"Minimum required passing cycles: **{report.min_required_passing_cycles}**",
        f"Unassigned records: **{report.unassigned_records}**",
        "",
        "| Cycle | Train Window | Test Window | Train Records | Test Records | Status | Expectancy R | Profit Factor | Max DD R | Sharpe |",
        "|---:|---|---|---:|---:|---:|---:|---:|---:|---:|",
    ]

    for result in report.cycle_results:
        metrics = result.validation_report.metrics
        lines.append(
            f"| {result.cycle.cycle_number} | "
            f"{result.cycle.training_start.isoformat()} to {result.cycle.training_end.isoformat()} | "
            f"{result.cycle.test_start.isoformat()} to {result.cycle.test_end.isoformat()} | "
            f"{result.training_records} | "
            f"{result.test_records} | "
            f"{'PASS' if result.passed else 'FAIL'} | "
            f"{metrics.expectancy_r:.4f} | "
            f"{_format_number(metrics.profit_factor)} | "
            f"{metrics.max_drawdown:.4f} | "
            f"{metrics.sharpe_ratio:.4f} |"
        )

    return "\n".join(lines).rstrip() + "\n"


def write_walk_forward_report(
    report: WalkForwardValidationReport,
    *,
    json_path: Path,
    markdown_path: Path,
) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report.to_dict(), indent=2), encoding="utf-8")
    markdown_path.write_text(render_walk_forward_markdown(report), encoding="utf-8")


def _extract_dated_records(
    records: Iterable[dict[str, Any]],
    *,
    primary_field: str,
    fallback_fields: tuple[str, ...],
) -> tuple[list[tuple[date, dict[str, Any]]], int]:
    dated_records: list[tuple[date, dict[str, Any]]] = []
    unassigned = 0
    for record in records:
        if not isinstance(record, dict):
            continue
        record_date = _extract_record_date(record, primary_field=primary_field, fallback_fields=fallback_fields)
        if record_date is None:
            unassigned += 1
            continue
        dated_records.append((record_date, dict(record)))
    return dated_records, unassigned


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


def _add_months(value: date, months: int) -> date:
    month = value.month - 1 + months
    year = value.year + month // 12
    month = month % 12 + 1
    day = min(value.day, _days_in_month(year, month))
    return date(year, month, day)


def _days_in_month(year: int, month: int) -> int:
    if month == 12:
        next_month = date(year + 1, 1, 1)
    else:
        next_month = date(year, month + 1, 1)
    return (next_month - timedelta(days=1)).day


def _format_number(value: float | int) -> str:
    if isinstance(value, float) and value == float("inf"):
        return "inf"
    if isinstance(value, int):
        return str(value)
    return f"{float(value):.4f}"
