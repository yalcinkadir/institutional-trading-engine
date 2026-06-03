from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from src.validation.capacity_turnover_realism_gate import CapacityTurnoverRealismReport

CAPACITY_EXECUTION_REVIEW_READY = "REVIEW_READY"
CAPACITY_EXECUTION_REVIEW_BLOCKED = "BLOCKED"


@dataclass(frozen=True)
class CapacityExecutionRealismReviewResult:
    valid: bool
    errors: tuple[str, ...]
    summary: dict[str, Any]


def _metric(report: CapacityTurnoverRealismReport, name: str) -> float:
    value = report.snapshot.metrics.get(name, 0.0)
    return float(value)


def build_capacity_execution_realism_review(
    report: CapacityTurnoverRealismReport,
    *,
    live_trading_authorized: bool = False,
    broker_execution_mode: str = "paper_only",
) -> CapacityExecutionRealismReviewResult:
    """Summarize BT7 capacity/turnover evidence for execution-realism review.

    CER1 is a review layer over existing BT7 evidence. It does not authorize
    live trading, broker execution, capital allocation or production deployment.
    """

    errors: list[str] = []
    failed_gates = [gate.name for gate in report.gates if not gate.passed]

    if not report.passed:
        errors.append("bt7_report_failed")

    if live_trading_authorized is not False:
        errors.append("live_trading_must_remain_false")

    if broker_execution_mode != "paper_only":
        errors.append("broker_execution_mode_must_be_paper_only")

    status = CAPACITY_EXECUTION_REVIEW_BLOCKED if errors else CAPACITY_EXECUTION_REVIEW_READY
    summary = {
        "capacity_execution_review_status": status,
        "approved_for_execution_review": not errors,
        "bt7_version": report.version,
        "bt7_generated_at": report.generated_at,
        "bt7_passed": report.passed,
        "failed_gates": failed_gates,
        "run_identity": {
            "run_id": report.snapshot.run_id,
            "strategy_id": report.snapshot.strategy_id,
            "dataset_id": report.snapshot.dataset_id,
            "parameter_version": report.snapshot.parameter_version,
            "evidence_type": report.snapshot.evidence_type,
        },
        "scale_profile": {
            "proposed_capital_usd": report.snapshot.proposed_capital_usd,
            "symbol_count": report.snapshot.symbol_count,
            "median_adv_usd": _metric(report, "median_adv_usd"),
        },
        "liquidity_profile": {
            "max_position_adv_pct": _metric(report, "max_position_adv_pct"),
            "portfolio_adv_pct": _metric(report, "portfolio_adv_pct"),
        },
        "turnover_profile": {
            "average_daily_turnover_pct": _metric(report, "average_daily_turnover_pct"),
            "annual_turnover_pct": _metric(report, "annual_turnover_pct"),
            "average_holding_days": _metric(report, "average_holding_days"),
            "trade_count": _metric(report, "trade_count"),
        },
        "cost_profile": {
            "round_trip_cost_bps": _metric(report, "round_trip_cost_bps"),
            "gross_expectancy_bps": _metric(report, "gross_expectancy_bps"),
            "net_expectancy_bps": _metric(report, "net_expectancy_bps"),
            "slippage_model_coverage_pct": _metric(report, "slippage_model_coverage_pct"),
        },
        "artifact_hashes": dict(report.snapshot.artifact_hashes),
        "tags": list(report.snapshot.tags),
        "errors": tuple(errors),
        "live_trading_authorized": False,
        "broker_execution_mode": "paper_only",
    }

    return CapacityExecutionRealismReviewResult(valid=not errors, errors=tuple(errors), summary=summary)
