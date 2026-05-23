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

MIN_PASSING_PHASES = 3


@dataclass(frozen=True)
class RegimePhase:
    name: str
    start_date: date
    end_date: date
    description: str

    def contains(self, value: date) -> bool:
        return self.start_date <= value <= self.end_date

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "description": self.description,
        }


@dataclass(frozen=True)
class RegimePhaseResult:
    phase: RegimePhase
    total_records: int
    validation_report: HistoricalEdgeValidationReport

    @property
    def passed(self) -> bool:
        return self.validation_report.passed

    def to_dict(self) -> dict[str, Any]:
        return {
            "phase": self.phase.to_dict(),
            "total_records": self.total_records,
            "passed": self.passed,
            "validation_report": self.validation_report.to_dict(),
        }


@dataclass(frozen=True)
class RegimePhaseBacktestMatrixReport:
    passed: bool
    passing_phases: int
    required_passing_phases: int
    total_phases: int
    unassigned_records: int
    phase_results: list[RegimePhaseResult] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "passing_phases": self.passing_phases,
            "required_passing_phases": self.required_passing_phases,
            "total_phases": self.total_phases,
            "unassigned_records": self.unassigned_records,
            "phase_results": [result.to_dict() for result in self.phase_results],
        }


def default_regime_phases() -> list[RegimePhase]:
    return [
        RegimePhase(
            name="Low-Vol Bull",
            start_date=date(2019, 1, 1),
            end_date=date(2020, 2, 29),
            description="Reference bull market before COVID dislocation.",
        ),
        RegimePhase(
            name="Panic/Dislocation",
            start_date=date(2020, 3, 1),
            end_date=date(2020, 4, 30),
            description="COVID crash and market dislocation.",
        ),
        RegimePhase(
            name="Recovery",
            start_date=date(2020, 5, 1),
            end_date=date(2021, 12, 31),
            description="Post-crash recovery and momentum regime.",
        ),
        RegimePhase(
            name="High-Vol Regime",
            start_date=date(2022, 1, 1),
            end_date=date(2022, 12, 31),
            description="Rate-hike and bear-market environment.",
        ),
        RegimePhase(
            name="Neutral/Transition",
            start_date=date(2023, 1, 1),
            end_date=date(2024, 6, 30),
            description="Mixed transition regime.",
        ),
    ]


def build_regime_phase_backtest_matrix(
    records: Iterable[dict[str, Any]],
    *,
    phases: Iterable[RegimePhase] | None = None,
    config: HistoricalEdgeValidationConfig = HistoricalEdgeValidationConfig(),
    date_field: str = "exit_date",
    fallback_date_fields: tuple[str, ...] = ("closed_at", "signal_date", "date"),
    result_field: str = "result_r",
    required_passing_phases: int = MIN_PASSING_PHASES,
) -> RegimePhaseBacktestMatrixReport:
    phase_list = list(phases) if phases is not None else default_regime_phases()
    buckets: dict[str, list[dict[str, Any]]] = {phase.name: [] for phase in phase_list}
    unassigned_records = 0

    for record in records:
        if not isinstance(record, dict):
            continue
        record_date = _extract_record_date(
            record,
            primary_field=date_field,
            fallback_fields=fallback_date_fields,
        )
        if record_date is None:
            unassigned_records += 1
            continue

        matched_phase = next((phase for phase in phase_list if phase.contains(record_date)), None)
        if matched_phase is None:
            unassigned_records += 1
            continue

        buckets[matched_phase.name].append(dict(record))

    phase_results = [
        RegimePhaseResult(
            phase=phase,
            total_records=len(buckets[phase.name]),
            validation_report=validate_historical_edge(
                buckets[phase.name],
                config=config,
                result_field=result_field,
            ),
        )
        for phase in phase_list
    ]
    passing_phases = sum(1 for result in phase_results if result.passed)

    return RegimePhaseBacktestMatrixReport(
        passed=passing_phases >= required_passing_phases,
        passing_phases=passing_phases,
        required_passing_phases=required_passing_phases,
        total_phases=len(phase_results),
        unassigned_records=unassigned_records,
        phase_results=phase_results,
    )


def render_regime_phase_matrix_markdown(report: RegimePhaseBacktestMatrixReport) -> str:
    lines = [
        "# Regime-Phase Backtest Matrix",
        "",
        f"Status: **{'PASS' if report.passed else 'FAIL'}**",
        f"Passing phases: **{report.passing_phases}/{report.total_phases}**",
        f"Required passing phases: **{report.required_passing_phases}**",
        f"Unassigned records: **{report.unassigned_records}**",
        "",
        "| Phase | Date Range | Status | Trades | Win Rate | Expectancy R | Profit Factor | Max DD R | Sharpe |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|",
    ]

    for result in report.phase_results:
        metrics = result.validation_report.metrics
        lines.append(
            f"| {result.phase.name} | "
            f"{result.phase.start_date.isoformat()} to {result.phase.end_date.isoformat()} | "
            f"{'PASS' if result.passed else 'FAIL'} | "
            f"{metrics.total_trades} | "
            f"{metrics.win_rate:.2%} | "
            f"{metrics.expectancy_r:.4f} | "
            f"{_format_number(metrics.profit_factor)} | "
            f"{metrics.max_drawdown:.4f} | "
            f"{metrics.sharpe_ratio:.4f} |"
        )

    return "\n".join(lines).rstrip() + "\n"


def write_regime_phase_matrix_report(
    report: RegimePhaseBacktestMatrixReport,
    *,
    json_path: Path,
    markdown_path: Path,
) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report.to_dict(), indent=2), encoding="utf-8")
    markdown_path.write_text(render_regime_phase_matrix_markdown(report), encoding="utf-8")


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
