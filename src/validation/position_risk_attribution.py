from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Iterable


@dataclass(frozen=True)
class PositionRiskAttributionConfig:
    min_positions: int = 1
    max_single_name_contribution_r: float = 1.0
    max_sector_contribution_r: float = 2.0
    max_factor_contribution_r: float = 2.0
    max_abs_unattributed_r: float = 1.0
    require_known_sector: bool = True


@dataclass(frozen=True)
class PositionAttribution:
    symbol: str
    sector: str
    weight: float
    result_r: float
    beta: float
    market_return_r: float
    total_contribution_r: float
    beta_contribution_r: float
    factor_contribution_r: float
    specific_contribution_r: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PositionRiskAttributionMetrics:
    positions: int
    portfolio_r: float
    beta_contribution_r: float
    factor_contribution_r: float
    specific_contribution_r: float
    unattributed_r: float
    max_single_name_contribution_r: float
    max_sector_contribution_r: float
    max_factor_contribution_r: float
    unknown_sector_count: int
    sector_contributions: dict[str, float] = field(default_factory=dict)
    factor_contributions: dict[str, float] = field(default_factory=dict)
    position_attributions: list[PositionAttribution] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "positions": self.positions,
            "portfolio_r": self.portfolio_r,
            "beta_contribution_r": self.beta_contribution_r,
            "factor_contribution_r": self.factor_contribution_r,
            "specific_contribution_r": self.specific_contribution_r,
            "unattributed_r": self.unattributed_r,
            "max_single_name_contribution_r": self.max_single_name_contribution_r,
            "max_sector_contribution_r": self.max_sector_contribution_r,
            "max_factor_contribution_r": self.max_factor_contribution_r,
            "unknown_sector_count": self.unknown_sector_count,
            "sector_contributions": self.sector_contributions,
            "factor_contributions": self.factor_contributions,
            "position_attributions": [item.to_dict() for item in self.position_attributions],
        }


@dataclass(frozen=True)
class PositionRiskAttributionGate:
    name: str
    passed: bool
    value: float | int | str | bool
    threshold: float | int | str | bool
    message: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PositionRiskAttributionReport:
    passed: bool
    metrics: PositionRiskAttributionMetrics
    gates: list[PositionRiskAttributionGate] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "metrics": self.metrics.to_dict(),
            "gates": [gate.to_dict() for gate in self.gates],
        }


def attribute_position_risk(
    records: Iterable[dict[str, Any]],
    *,
    config: PositionRiskAttributionConfig = PositionRiskAttributionConfig(),
) -> PositionRiskAttributionReport:
    normalized = [_normalize_record(record) for record in records if isinstance(record, dict)]
    metrics = _calculate_metrics(normalized)
    gates = _build_gates(metrics, config=config)
    return PositionRiskAttributionReport(
        passed=all(gate.passed for gate in gates),
        metrics=metrics,
        gates=gates,
    )


def render_position_risk_attribution_markdown(report: PositionRiskAttributionReport) -> str:
    metrics = report.metrics
    lines = [
        "# Position-Level Risk Attribution",
        "",
        f"Status: **{'PASS' if report.passed else 'FAIL'}**",
        "",
        "## Metrics",
        "",
        f"- Positions: {metrics.positions}",
        f"- Portfolio R: {metrics.portfolio_r:.4f}",
        f"- Beta contribution R: {metrics.beta_contribution_r:.4f}",
        f"- Factor contribution R: {metrics.factor_contribution_r:.4f}",
        f"- Specific contribution R: {metrics.specific_contribution_r:.4f}",
        f"- Unattributed R: {metrics.unattributed_r:.4f}",
        f"- Max single-name contribution R: {metrics.max_single_name_contribution_r:.4f}",
        f"- Max sector contribution R: {metrics.max_sector_contribution_r:.4f}",
        f"- Max factor contribution R: {metrics.max_factor_contribution_r:.4f}",
        f"- Unknown sector count: {metrics.unknown_sector_count}",
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
    lines.extend(["", "## Sector Contributions", "", "| Sector | Contribution R |", "|---|---:|"])
    for sector, contribution in sorted(metrics.sector_contributions.items()):
        lines.append(f"| {sector} | {contribution:.4f} |")
    lines.extend(["", "## Factor Contributions", "", "| Factor | Contribution R |", "|---|---:|"])
    for factor, contribution in sorted(metrics.factor_contributions.items()):
        lines.append(f"| {factor} | {contribution:.4f} |")
    return "\n".join(lines).rstrip() + "\n"


def write_position_risk_attribution_report(
    report: PositionRiskAttributionReport,
    *,
    json_path: Path,
    markdown_path: Path,
) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report.to_dict(), indent=2), encoding="utf-8")
    markdown_path.write_text(render_position_risk_attribution_markdown(report), encoding="utf-8")


def _calculate_metrics(records: list[dict[str, Any]]) -> PositionRiskAttributionMetrics:
    position_attributions: list[PositionAttribution] = []
    sector_contributions: dict[str, float] = {}
    factor_contributions: dict[str, float] = {}

    for record in records:
        weight = record["weight"]
        result_r = record["result_r"]
        total_contribution = weight * result_r
        beta_contribution = weight * record["beta"] * record["market_return_r"]
        factor_contribution = 0.0
        for factor, exposure in record["factor_exposures"].items():
            factor_return = record["factor_returns"].get(factor, 0.0)
            contribution = weight * exposure * factor_return
            factor_contribution += contribution
            factor_contributions[factor] = factor_contributions.get(factor, 0.0) + contribution
        specific_contribution = total_contribution - beta_contribution - factor_contribution
        sector = record["sector"]
        sector_contributions[sector] = sector_contributions.get(sector, 0.0) + total_contribution
        position_attributions.append(
            PositionAttribution(
                symbol=record["symbol"],
                sector=sector,
                weight=round(weight, 6),
                result_r=round(result_r, 6),
                beta=round(record["beta"], 6),
                market_return_r=round(record["market_return_r"], 6),
                total_contribution_r=round(total_contribution, 6),
                beta_contribution_r=round(beta_contribution, 6),
                factor_contribution_r=round(factor_contribution, 6),
                specific_contribution_r=round(specific_contribution, 6),
            )
        )

    portfolio_r = sum(item.total_contribution_r for item in position_attributions)
    beta_contribution_r = sum(item.beta_contribution_r for item in position_attributions)
    factor_contribution_r = sum(item.factor_contribution_r for item in position_attributions)
    specific_contribution_r = sum(item.specific_contribution_r for item in position_attributions)
    unattributed_r = portfolio_r - beta_contribution_r - factor_contribution_r - specific_contribution_r
    unknown_sector_count = sum(1 for item in position_attributions if item.sector == "unknown")

    sector_contributions = {key: round(value, 6) for key, value in sector_contributions.items()}
    factor_contributions = {key: round(value, 6) for key, value in factor_contributions.items()}

    return PositionRiskAttributionMetrics(
        positions=len(position_attributions),
        portfolio_r=round(portfolio_r, 6),
        beta_contribution_r=round(beta_contribution_r, 6),
        factor_contribution_r=round(factor_contribution_r, 6),
        specific_contribution_r=round(specific_contribution_r, 6),
        unattributed_r=round(unattributed_r, 6),
        max_single_name_contribution_r=round(max((abs(item.total_contribution_r) for item in position_attributions), default=0.0), 6),
        max_sector_contribution_r=round(max((abs(value) for value in sector_contributions.values()), default=0.0), 6),
        max_factor_contribution_r=round(max((abs(value) for value in factor_contributions.values()), default=0.0), 6),
        unknown_sector_count=unknown_sector_count,
        sector_contributions=sector_contributions,
        factor_contributions=factor_contributions,
        position_attributions=position_attributions,
    )


def _build_gates(
    metrics: PositionRiskAttributionMetrics,
    *,
    config: PositionRiskAttributionConfig,
) -> list[PositionRiskAttributionGate]:
    return [
        PositionRiskAttributionGate(
            name="minimum_positions",
            passed=metrics.positions >= config.min_positions,
            value=metrics.positions,
            threshold=config.min_positions,
            message="At least one position is required for risk attribution.",
        ),
        PositionRiskAttributionGate(
            name="known_sector_coverage",
            passed=(not config.require_known_sector) or metrics.unknown_sector_count == 0,
            value=metrics.unknown_sector_count,
            threshold=0,
            message="All attributed positions should have known sector labels.",
        ),
        PositionRiskAttributionGate(
            name="single_name_concentration",
            passed=metrics.max_single_name_contribution_r <= config.max_single_name_contribution_r,
            value=metrics.max_single_name_contribution_r,
            threshold=config.max_single_name_contribution_r,
            message="No single position should dominate portfolio R attribution.",
        ),
        PositionRiskAttributionGate(
            name="sector_concentration",
            passed=metrics.max_sector_contribution_r <= config.max_sector_contribution_r,
            value=metrics.max_sector_contribution_r,
            threshold=config.max_sector_contribution_r,
            message="No sector should dominate portfolio R attribution.",
        ),
        PositionRiskAttributionGate(
            name="factor_concentration",
            passed=metrics.max_factor_contribution_r <= config.max_factor_contribution_r,
            value=metrics.max_factor_contribution_r,
            threshold=config.max_factor_contribution_r,
            message="No factor should dominate portfolio R attribution.",
        ),
        PositionRiskAttributionGate(
            name="unattributed_r",
            passed=abs(metrics.unattributed_r) <= config.max_abs_unattributed_r,
            value=abs(metrics.unattributed_r),
            threshold=config.max_abs_unattributed_r,
            message="Attribution residual should remain within tolerance.",
        ),
    ]


def _normalize_record(record: dict[str, Any]) -> dict[str, Any]:
    symbol = str(record.get("symbol") or record.get("ticker") or "unknown").upper()
    sector = _normalize_label(record.get("sector") or record.get("gics_sector"))
    factor_exposures = _normalize_float_map(record.get("factor_exposures") or record.get("factors"))
    factor_returns = _normalize_float_map(record.get("factor_returns"))
    return {
        "symbol": symbol,
        "sector": sector,
        "weight": _safe_float(record.get("weight", record.get("position_weight", record.get("size", 1.0)))) or 0.0,
        "result_r": _safe_float(record.get("result_r", record.get("r_multiple", record.get("paper_r")))) or 0.0,
        "beta": _safe_float(record.get("beta", record.get("market_beta"))) or 0.0,
        "market_return_r": _safe_float(record.get("market_return_r", record.get("benchmark_r"))) or 0.0,
        "factor_exposures": factor_exposures,
        "factor_returns": factor_returns,
    }


def _normalize_float_map(value: Any) -> dict[str, float]:
    if not isinstance(value, dict):
        return {}
    normalized: dict[str, float] = {}
    for key, raw in value.items():
        parsed = _safe_float(raw)
        if parsed is not None:
            normalized[_normalize_label(key)] = parsed
    return normalized


def _normalize_label(value: Any) -> str:
    if value is None:
        return "unknown"
    text = str(value).strip().lower().replace(" ", "_").replace("-", "_")
    return text if text else "unknown"


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
    return str(value)
