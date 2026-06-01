"""BT8 reproducible backtesting evidence report generation.

Builds an audit-friendly report from BT3 backtest run contracts. The report is
research/paper-only and does not authorize live execution.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

from src.validation.backtest_run_contract import (
    BacktestRunContract,
    BacktestRunContractReport,
    RESEARCH_ONLY_FOOTER,
    build_backtest_run_contract_report,
    load_backtest_run_contracts_json,
)

BT8_REPORT_VERSION = "BT8-v1"


@dataclass(frozen=True)
class BacktestingEvidenceReportSummary:
    run_count: int
    strategy_count: int
    dataset_count: int
    symbol_count: int
    trade_count: int
    average_return_pct: float | None
    average_win_rate_pct: float | None
    average_sharpe: float | None
    worst_max_drawdown_pct: float | None
    overall_status: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_count": self.run_count,
            "strategy_count": self.strategy_count,
            "dataset_count": self.dataset_count,
            "symbol_count": self.symbol_count,
            "trade_count": self.trade_count,
            "average_return_pct": _round_optional(self.average_return_pct),
            "average_win_rate_pct": _round_optional(self.average_win_rate_pct),
            "average_sharpe": _round_optional(self.average_sharpe),
            "worst_max_drawdown_pct": _round_optional(self.worst_max_drawdown_pct),
            "overall_status": self.overall_status,
        }


@dataclass(frozen=True)
class BacktestingEvidenceReport:
    version: str
    generated_at: str
    run_contract_report: BacktestRunContractReport
    summary: BacktestingEvidenceReportSummary
    limitations: tuple[str, ...]
    live_trading_authorized: bool = False
    footer: str = RESEARCH_ONLY_FOOTER

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "generated_at": self.generated_at,
            "overall_status": self.summary.overall_status,
            "live_trading_authorized": self.live_trading_authorized,
            "summary": self.summary.to_dict(),
            "gates": [gate.to_dict() for gate in self.run_contract_report.gates],
            "contracts": [contract.to_dict() for contract in self.run_contract_report.contracts],
            "limitations": list(self.limitations),
            "footer": self.footer,
        }


@dataclass(frozen=True)
class BacktestingEvidenceReportConfig:
    version: str = BT8_REPORT_VERSION
    limitations: tuple[str, ...] = field(
        default_factory=lambda: (
            "Backtesting evidence is historical/simulated and does not prove future performance.",
            "Forward paper observation remains required before any live-execution consideration.",
            "Execution quality, capacity, turnover and regime drift must be reviewed separately.",
        )
    )


def build_backtesting_evidence_report(
    contracts: Sequence[BacktestRunContract | Mapping[str, Any]],
    *,
    generated_at: str | None = None,
    config: BacktestingEvidenceReportConfig | None = None,
) -> BacktestingEvidenceReport:
    """Build a BT8 evidence report from BT3 backtest run contracts."""

    cfg = config or BacktestingEvidenceReportConfig()
    timestamp = generated_at or datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
    contract_report = build_backtest_run_contract_report(
        contracts,
        version="BT3-v1",
        generated_at=timestamp,
    )
    summary = _build_summary(contract_report)
    return BacktestingEvidenceReport(
        version=cfg.version,
        generated_at=timestamp,
        run_contract_report=contract_report,
        summary=summary,
        limitations=cfg.limitations,
        live_trading_authorized=False,
    )


def load_backtesting_evidence_report_from_contracts_json(
    path: str | Path,
    *,
    generated_at: str | None = None,
    config: BacktestingEvidenceReportConfig | None = None,
) -> BacktestingEvidenceReport:
    contracts = load_backtest_run_contracts_json(path)
    return build_backtesting_evidence_report(contracts, generated_at=generated_at, config=config)


def render_backtesting_evidence_report_markdown(report: BacktestingEvidenceReport) -> str:
    status = report.summary.overall_status
    lines = [
        "# BT8 Backtesting Evidence Report",
        "",
        f"Generated at: `{report.generated_at}`",
        f"Report version: `{report.version}`",
        f"Overall status: `{status}`",
        f"Live trading authorized: `{report.live_trading_authorized}`",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|---|---:|",
    ]
    for key, value in report.summary.to_dict().items():
        lines.append(f"| `{key}` | {value} |")

    lines.extend(["", "## Gate Results", "", "| Gate | Status | Message |", "|---|---|---|"])
    for gate in report.run_contract_report.gates:
        gate_status = "PASS" if gate.passed else "FAIL"
        message = gate.message if not gate.failures else f"{gate.message} Failures: {'; '.join(gate.failures)}"
        lines.append(f"| `{gate.name}` | `{gate_status}` | {message} |")

    lines.extend(
        [
            "",
            "## Runs",
            "",
            "| Run | Strategy | Version | Dataset | Symbols | Period | Trades | Return % | Max DD % | Sharpe | Win % |",
            "|---|---|---|---|---|---|---:|---:|---:|---:|---:|",
        ]
    )
    for contract in report.run_contract_report.contracts:
        metrics = contract.metrics
        lines.append(
            "| "
            f"`{contract.run_id}` | `{contract.strategy_id}` | `{contract.strategy_version}` | `{contract.dataset_id}` | "
            f"{', '.join(contract.symbols)} | {contract.start_date} to {contract.end_date} | "
            f"{_metric(metrics, 'trade_count')} | {_metric(metrics, 'total_return_pct')} | {_metric(metrics, 'max_drawdown_pct')} | "
            f"{_metric(metrics, 'sharpe')} | {_metric(metrics, 'win_rate_pct')} |"
        )

    lines.extend(["", "## Limitations", ""])
    for limitation in report.limitations:
        lines.append(f"- {limitation}")

    lines.extend(["", "---", "", report.footer, ""])
    return "\n".join(lines)


def write_backtesting_evidence_report(
    report: BacktestingEvidenceReport,
    *,
    output_json: str | Path,
    output_md: str | Path,
) -> None:
    json_path = Path(output_json)
    md_path = Path(output_md)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(render_backtesting_evidence_report_markdown(report), encoding="utf-8")


def _build_summary(contract_report: BacktestRunContractReport) -> BacktestingEvidenceReportSummary:
    contracts = contract_report.contracts
    trade_count = int(sum(float(contract.metrics.get("trade_count", 0)) for contract in contracts))
    overall_status = "PASS" if contract_report.passed else "FAIL"
    return BacktestingEvidenceReportSummary(
        run_count=contract_report.metrics.run_count,
        strategy_count=contract_report.metrics.strategy_count,
        dataset_count=contract_report.metrics.dataset_count,
        symbol_count=contract_report.metrics.symbol_count,
        trade_count=trade_count,
        average_return_pct=_average_metric(contracts, "total_return_pct"),
        average_win_rate_pct=_average_metric(contracts, "win_rate_pct"),
        average_sharpe=_average_metric(contracts, "sharpe"),
        worst_max_drawdown_pct=_min_metric(contracts, "max_drawdown_pct"),
        overall_status=overall_status,
    )


def _average_metric(contracts: Sequence[BacktestRunContract], key: str) -> float | None:
    values = [float(contract.metrics[key]) for contract in contracts if isinstance(contract.metrics.get(key), (int, float))]
    return sum(values) / len(values) if values else None


def _min_metric(contracts: Sequence[BacktestRunContract], key: str) -> float | None:
    values = [float(contract.metrics[key]) for contract in contracts if isinstance(contract.metrics.get(key), (int, float))]
    return min(values) if values else None


def _round_optional(value: float | None) -> float | None:
    return None if value is None else round(value, 4)


def _metric(metrics: Mapping[str, Any], key: str) -> Any:
    return metrics.get(key, "n/a")
