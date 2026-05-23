from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import date, datetime
from pathlib import Path
from statistics import mean
from typing import Any, Iterable

MAX_ACCEPTABLE_SLIPPAGE_R = 0.25
MAX_ACCEPTABLE_FILL_DEVIATION_PCT = 0.0025


@dataclass(frozen=True)
class PaperTradingJournalConfig:
    max_acceptable_slippage_r: float = MAX_ACCEPTABLE_SLIPPAGE_R
    max_acceptable_fill_deviation_pct: float = MAX_ACCEPTABLE_FILL_DEVIATION_PCT


@dataclass(frozen=True)
class PaperTradingObservation:
    observation_id: str
    symbol: str
    observation_date: str
    theoretical_entry: float
    paper_fill_price: float | None
    stop_loss: float
    expected_result_r: float | None = None
    outcome_5d_r: float | None = None
    outcome_20d_r: float | None = None
    backtest_expectancy_r: float | None = None
    would_have_held: bool | None = None
    impulse_to_deviate: bool | None = None
    drawdown_stress_note: str | None = None
    notes: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PaperTradingObservationAnalysis:
    observation: PaperTradingObservation
    fill_available: bool
    fill_deviation_pct: float
    slippage_r: float
    model_deviation_5d_r: float | None
    model_deviation_20d_r: float | None
    has_execution_deviation: bool
    has_model_deviation: bool
    has_psychology_deviation: bool
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "observation": self.observation.to_dict(),
            "fill_available": self.fill_available,
            "fill_deviation_pct": self.fill_deviation_pct,
            "slippage_r": self.slippage_r,
            "model_deviation_5d_r": self.model_deviation_5d_r,
            "model_deviation_20d_r": self.model_deviation_20d_r,
            "has_execution_deviation": self.has_execution_deviation,
            "has_model_deviation": self.has_model_deviation,
            "has_psychology_deviation": self.has_psychology_deviation,
            "warnings": self.warnings,
        }


@dataclass(frozen=True)
class WeeklyPaperTradingSummary:
    week_start: str
    observation_count: int
    filled_count: int
    average_slippage_r: float
    average_fill_deviation_pct: float
    average_5d_r: float
    average_20d_r: float
    execution_deviation_count: int
    model_deviation_count: int
    psychology_deviation_count: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PaperTradingJournalReport:
    observation_count: int
    filled_count: int
    average_slippage_r: float
    average_5d_r: float
    average_20d_r: float
    execution_deviation_count: int
    model_deviation_count: int
    psychology_deviation_count: int
    observations: list[PaperTradingObservationAnalysis] = field(default_factory=list)
    weekly_summaries: list[WeeklyPaperTradingSummary] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "observation_count": self.observation_count,
            "filled_count": self.filled_count,
            "average_slippage_r": self.average_slippage_r,
            "average_5d_r": self.average_5d_r,
            "average_20d_r": self.average_20d_r,
            "execution_deviation_count": self.execution_deviation_count,
            "model_deviation_count": self.model_deviation_count,
            "psychology_deviation_count": self.psychology_deviation_count,
            "observations": [item.to_dict() for item in self.observations],
            "weekly_summaries": [item.to_dict() for item in self.weekly_summaries],
        }


def analyze_paper_trading_journal(
    records: Iterable[dict[str, Any] | PaperTradingObservation],
    *,
    config: PaperTradingJournalConfig = PaperTradingJournalConfig(),
) -> PaperTradingJournalReport:
    observations = [_coerce_observation(record) for record in records]
    analyses = [analyze_observation(item, config=config) for item in observations]
    weekly = build_weekly_summaries(analyses)

    filled = [item for item in analyses if item.fill_available]
    return PaperTradingJournalReport(
        observation_count=len(analyses),
        filled_count=len(filled),
        average_slippage_r=_avg([item.slippage_r for item in filled]),
        average_5d_r=_avg([item.observation.outcome_5d_r for item in analyses]),
        average_20d_r=_avg([item.observation.outcome_20d_r for item in analyses]),
        execution_deviation_count=sum(1 for item in analyses if item.has_execution_deviation),
        model_deviation_count=sum(1 for item in analyses if item.has_model_deviation),
        psychology_deviation_count=sum(1 for item in analyses if item.has_psychology_deviation),
        observations=analyses,
        weekly_summaries=weekly,
    )


def analyze_observation(
    observation: PaperTradingObservation,
    *,
    config: PaperTradingJournalConfig = PaperTradingJournalConfig(),
) -> PaperTradingObservationAnalysis:
    warnings: list[str] = []
    fill_available = observation.paper_fill_price is not None
    initial_risk = abs(observation.theoretical_entry - observation.stop_loss)
    if initial_risk <= 0:
        warnings.append("invalid_initial_risk")
        initial_risk = 1e-9

    if fill_available:
        fill_deviation = float(observation.paper_fill_price) - observation.theoretical_entry
        fill_deviation_pct = fill_deviation / observation.theoretical_entry if observation.theoretical_entry else 0.0
        slippage_r = fill_deviation / initial_risk
    else:
        warnings.append("missing_paper_fill_price")
        fill_deviation_pct = 0.0
        slippage_r = 0.0

    model_deviation_5d = _model_deviation(observation.outcome_5d_r, observation.expected_result_r)
    model_deviation_20d = _model_deviation(observation.outcome_20d_r, observation.expected_result_r)
    has_execution_deviation = abs(slippage_r) > config.max_acceptable_slippage_r or abs(fill_deviation_pct) > config.max_acceptable_fill_deviation_pct
    has_model_deviation = _is_model_deviation(model_deviation_5d) or _is_model_deviation(model_deviation_20d)
    has_psychology_deviation = observation.would_have_held is False or observation.impulse_to_deviate is True

    return PaperTradingObservationAnalysis(
        observation=observation,
        fill_available=fill_available,
        fill_deviation_pct=round(fill_deviation_pct, 6),
        slippage_r=round(slippage_r, 6),
        model_deviation_5d_r=None if model_deviation_5d is None else round(model_deviation_5d, 6),
        model_deviation_20d_r=None if model_deviation_20d is None else round(model_deviation_20d, 6),
        has_execution_deviation=has_execution_deviation,
        has_model_deviation=has_model_deviation,
        has_psychology_deviation=has_psychology_deviation,
        warnings=warnings,
    )


def build_weekly_summaries(analyses: Iterable[PaperTradingObservationAnalysis]) -> list[WeeklyPaperTradingSummary]:
    buckets: dict[str, list[PaperTradingObservationAnalysis]] = {}
    for item in analyses:
        parsed = _parse_date(item.observation.observation_date)
        if parsed is None:
            week_key = "unknown"
        else:
            week_start = parsed.fromordinal(parsed.toordinal() - parsed.weekday())
            week_key = week_start.isoformat()
        buckets.setdefault(week_key, []).append(item)

    summaries: list[WeeklyPaperTradingSummary] = []
    for week, items in sorted(buckets.items()):
        filled = [item for item in items if item.fill_available]
        summaries.append(
            WeeklyPaperTradingSummary(
                week_start=week,
                observation_count=len(items),
                filled_count=len(filled),
                average_slippage_r=_avg([item.slippage_r for item in filled]),
                average_fill_deviation_pct=_avg([item.fill_deviation_pct for item in filled]),
                average_5d_r=_avg([item.observation.outcome_5d_r for item in items]),
                average_20d_r=_avg([item.observation.outcome_20d_r for item in items]),
                execution_deviation_count=sum(1 for item in items if item.has_execution_deviation),
                model_deviation_count=sum(1 for item in items if item.has_model_deviation),
                psychology_deviation_count=sum(1 for item in items if item.has_psychology_deviation),
            )
        )
    return summaries


def render_paper_trading_journal_markdown(report: PaperTradingJournalReport) -> str:
    lines = [
        "# Paper Trading Journal / Live Observation v2",
        "",
        f"Observation count: **{report.observation_count}**",
        f"Filled count: **{report.filled_count}**",
        f"Average slippage R: **{report.average_slippage_r:.4f}**",
        f"Average 5d R: **{report.average_5d_r:.4f}**",
        f"Average 20d R: **{report.average_20d_r:.4f}**",
        f"Execution deviations: **{report.execution_deviation_count}**",
        f"Model deviations: **{report.model_deviation_count}**",
        f"Psychology deviations: **{report.psychology_deviation_count}**",
        "",
        "## Weekly Summary",
        "",
        "| Week | Observations | Filled | Avg Slip R | Avg 5d R | Avg 20d R | Exec Dev | Model Dev | Psych Dev |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for item in report.weekly_summaries:
        lines.append(
            f"| {item.week_start} | {item.observation_count} | {item.filled_count} | "
            f"{item.average_slippage_r:.4f} | {item.average_5d_r:.4f} | {item.average_20d_r:.4f} | "
            f"{item.execution_deviation_count} | {item.model_deviation_count} | {item.psychology_deviation_count} |"
        )
    lines.extend(["", "## Observation Details", "", "| ID | Symbol | Date | Slip R | 5d R | 20d R | Warnings |", "|---|---|---|---:|---:|---:|---|"])
    for item in report.observations:
        warnings = ", ".join(item.warnings) if item.warnings else "-"
        lines.append(
            f"| {item.observation.observation_id} | {item.observation.symbol} | {item.observation.observation_date} | "
            f"{item.slippage_r:.4f} | {_fmt(item.observation.outcome_5d_r)} | {_fmt(item.observation.outcome_20d_r)} | {warnings} |"
        )
    return "\n".join(lines).rstrip() + "\n"


def write_paper_trading_journal_report(
    report: PaperTradingJournalReport,
    *,
    json_path: Path,
    markdown_path: Path,
) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report.to_dict(), indent=2), encoding="utf-8")
    markdown_path.write_text(render_paper_trading_journal_markdown(report), encoding="utf-8")


def _coerce_observation(record: dict[str, Any] | PaperTradingObservation) -> PaperTradingObservation:
    if isinstance(record, PaperTradingObservation):
        return record
    return PaperTradingObservation(
        observation_id=str(record.get("observation_id") or record.get("signal_id") or "unknown"),
        symbol=str(record.get("symbol") or "unknown"),
        observation_date=str(record.get("observation_date") or record.get("date") or record.get("signal_date") or "unknown"),
        theoretical_entry=float(record.get("theoretical_entry") or record.get("entry_trigger") or record.get("entry_price") or 0.0),
        paper_fill_price=_optional_float(record.get("paper_fill_price") or record.get("actual_fill_price")),
        stop_loss=float(record.get("stop_loss") or 0.0),
        expected_result_r=_optional_float(record.get("expected_result_r") or record.get("backtest_expectancy_r")),
        outcome_5d_r=_optional_float(record.get("outcome_5d_r")),
        outcome_20d_r=_optional_float(record.get("outcome_20d_r")),
        backtest_expectancy_r=_optional_float(record.get("backtest_expectancy_r")),
        would_have_held=record.get("would_have_held"),
        impulse_to_deviate=record.get("impulse_to_deviate"),
        drawdown_stress_note=record.get("drawdown_stress_note"),
        notes=record.get("notes"),
    )


def _model_deviation(actual: float | None, expected: float | None) -> float | None:
    if actual is None or expected is None:
        return None
    return actual - expected


def _is_model_deviation(value: float | None) -> bool:
    return value is not None and abs(value) >= 1.0


def _avg(values: Iterable[float | None]) -> float:
    cleaned = [float(value) for value in values if value is not None]
    return round(mean(cleaned), 6) if cleaned else 0.0


def _optional_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _parse_date(value: str) -> date | None:
    if value == "unknown":
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).date()
    except ValueError:
        return None


def _fmt(value: float | None) -> str:
    return "-" if value is None else f"{value:.4f}"
