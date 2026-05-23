from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Iterable

DEFAULT_SPREAD_COST_PCT = 0.0005
DEFAULT_NORMAL_SLIPPAGE_PCT = 0.0010
DEFAULT_VOLATILE_SLIPPAGE_PCT = 0.0030
VOLATILE_REGIME_LABELS = {
    "volatile",
    "high_vol",
    "high-vol",
    "high volatility",
    "panic",
    "dislocation",
    "risk_off",
    "risk-off",
}


@dataclass(frozen=True)
class ExecutionRealismConfig:
    spread_cost_pct: float = DEFAULT_SPREAD_COST_PCT
    normal_slippage_pct: float = DEFAULT_NORMAL_SLIPPAGE_PCT
    volatile_slippage_pct: float = DEFAULT_VOLATILE_SLIPPAGE_PCT
    volatile_regime_labels: frozenset[str] = frozenset(VOLATILE_REGIME_LABELS)


@dataclass(frozen=True)
class ExecutionAdjustedRecord:
    original_record: dict[str, Any]
    adjusted_record: dict[str, Any]
    original_r: float
    adjusted_r: float
    execution_cost_r: float
    spread_cost_pct: float
    slippage_pct: float
    total_cost_pct: float
    regime_label: str
    valid: bool
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ExecutionRealismSummary:
    total_records: int
    adjusted_records: int
    invalid_records: int
    total_original_r: float
    total_adjusted_r: float
    total_execution_cost_r: float
    average_execution_cost_r: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ExecutionRealismReport:
    summary: ExecutionRealismSummary
    records: list[ExecutionAdjustedRecord] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "summary": self.summary.to_dict(),
            "records": [record.to_dict() for record in self.records],
        }


def apply_execution_realism(
    records: Iterable[dict[str, Any]],
    *,
    config: ExecutionRealismConfig = ExecutionRealismConfig(),
    result_field: str = "result_r",
    entry_field: str = "entry_price",
    stop_field: str = "stop_loss",
    regime_field: str = "volatility_regime",
) -> ExecutionRealismReport:
    adjusted: list[ExecutionAdjustedRecord] = []
    for record in records:
        if not isinstance(record, dict):
            continue
        adjusted.append(
            adjust_execution_record(
                record,
                config=config,
                result_field=result_field,
                entry_field=entry_field,
                stop_field=stop_field,
                regime_field=regime_field,
            )
        )

    valid_records = [record for record in adjusted if record.valid]
    total_original_r = sum(record.original_r for record in valid_records)
    total_adjusted_r = sum(record.adjusted_r for record in valid_records)
    total_cost_r = sum(record.execution_cost_r for record in valid_records)
    average_cost_r = total_cost_r / len(valid_records) if valid_records else 0.0

    return ExecutionRealismReport(
        summary=ExecutionRealismSummary(
            total_records=len(adjusted),
            adjusted_records=len(valid_records),
            invalid_records=len(adjusted) - len(valid_records),
            total_original_r=round(total_original_r, 6),
            total_adjusted_r=round(total_adjusted_r, 6),
            total_execution_cost_r=round(total_cost_r, 6),
            average_execution_cost_r=round(average_cost_r, 6),
        ),
        records=adjusted,
    )


def adjust_execution_record(
    record: dict[str, Any],
    *,
    config: ExecutionRealismConfig = ExecutionRealismConfig(),
    result_field: str = "result_r",
    entry_field: str = "entry_price",
    stop_field: str = "stop_loss",
    regime_field: str = "volatility_regime",
) -> ExecutionAdjustedRecord:
    warnings: list[str] = []
    original_r = _safe_float(record.get(result_field, record.get("r_multiple")))
    entry_price = _safe_float(record.get(entry_field, record.get("entry_trigger")))
    stop_loss = _safe_float(record.get(stop_field))
    regime_label = str(record.get(regime_field, record.get("market_regime", "normal"))).strip().lower()

    if original_r is None:
        warnings.append("missing_result_r")
    if entry_price is None:
        warnings.append("missing_entry_price")
    if stop_loss is None:
        warnings.append("missing_stop_loss")

    valid = not warnings
    spread_cost_pct = max(config.spread_cost_pct, DEFAULT_SPREAD_COST_PCT)
    slippage_pct = _slippage_for_regime(regime_label, config=config)
    total_cost_pct = spread_cost_pct + slippage_pct

    if not valid:
        return ExecutionAdjustedRecord(
            original_record=dict(record),
            adjusted_record=dict(record),
            original_r=0.0,
            adjusted_r=0.0,
            execution_cost_r=0.0,
            spread_cost_pct=spread_cost_pct,
            slippage_pct=slippage_pct,
            total_cost_pct=total_cost_pct,
            regime_label=regime_label or "normal",
            valid=False,
            warnings=warnings,
        )

    initial_risk = abs(float(entry_price) - float(stop_loss))
    if initial_risk <= 0:
        warnings.append("invalid_initial_risk")
        return ExecutionAdjustedRecord(
            original_record=dict(record),
            adjusted_record=dict(record),
            original_r=float(original_r),
            adjusted_r=float(original_r),
            execution_cost_r=0.0,
            spread_cost_pct=spread_cost_pct,
            slippage_pct=slippage_pct,
            total_cost_pct=total_cost_pct,
            regime_label=regime_label or "normal",
            valid=False,
            warnings=warnings,
        )

    cost_price = float(entry_price) * total_cost_pct
    execution_cost_r = cost_price / initial_risk
    adjusted_r = float(original_r) - execution_cost_r
    adjusted_record = dict(record)
    adjusted_record[result_field] = round(adjusted_r, 6)
    adjusted_record["execution_realism_applied"] = True
    adjusted_record["execution_cost_r"] = round(execution_cost_r, 6)
    adjusted_record["spread_cost_pct"] = spread_cost_pct
    adjusted_record["slippage_pct"] = slippage_pct
    adjusted_record["no_lookahead_execution_adjustment"] = True

    return ExecutionAdjustedRecord(
        original_record=dict(record),
        adjusted_record=adjusted_record,
        original_r=round(float(original_r), 6),
        adjusted_r=round(adjusted_r, 6),
        execution_cost_r=round(execution_cost_r, 6),
        spread_cost_pct=spread_cost_pct,
        slippage_pct=slippage_pct,
        total_cost_pct=total_cost_pct,
        regime_label=regime_label or "normal",
        valid=True,
        warnings=warnings,
    )


def render_execution_realism_markdown(report: ExecutionRealismReport) -> str:
    summary = report.summary
    lines = [
        "# Execution Realism Report",
        "",
        "## Summary",
        "",
        f"- Total records: {summary.total_records}",
        f"- Adjusted records: {summary.adjusted_records}",
        f"- Invalid records: {summary.invalid_records}",
        f"- Total original R: {summary.total_original_r:.4f}",
        f"- Total adjusted R: {summary.total_adjusted_r:.4f}",
        f"- Total execution cost R: {summary.total_execution_cost_r:.4f}",
        f"- Average execution cost R: {summary.average_execution_cost_r:.4f}",
        "",
        "## Records",
        "",
        "| Symbol | Regime | Valid | Original R | Cost R | Adjusted R | Warnings |",
        "|---|---|---:|---:|---:|---:|---|",
    ]
    for item in report.records:
        symbol = item.original_record.get("symbol", "unknown")
        warnings = ", ".join(item.warnings) if item.warnings else "-"
        lines.append(
            f"| {symbol} | {item.regime_label} | {'yes' if item.valid else 'no'} | "
            f"{item.original_r:.4f} | {item.execution_cost_r:.4f} | {item.adjusted_r:.4f} | {warnings} |"
        )
    return "\n".join(lines).rstrip() + "\n"


def write_execution_realism_report(
    report: ExecutionRealismReport,
    *,
    json_path: Path,
    markdown_path: Path,
) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report.to_dict(), indent=2), encoding="utf-8")
    markdown_path.write_text(render_execution_realism_markdown(report), encoding="utf-8")


def _slippage_for_regime(regime_label: str, *, config: ExecutionRealismConfig) -> float:
    normalized = regime_label.strip().lower()
    if normalized in config.volatile_regime_labels:
        return max(config.volatile_slippage_pct, DEFAULT_VOLATILE_SLIPPAGE_PCT)
    return max(config.normal_slippage_pct, DEFAULT_NORMAL_SLIPPAGE_PCT)


def _safe_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None
