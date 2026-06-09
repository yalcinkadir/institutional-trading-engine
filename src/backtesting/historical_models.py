"""Data models for historical backtesting."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

OUTCOME_ENTRY_NOT_HIT = "ENTRY_NOT_HIT"
OUTCOME_EXPIRED = "EXPIRED"
OUTCOME_STOP_HIT = "STOP_HIT"
OUTCOME_TARGET_1_HIT = "TARGET_1_HIT"
OUTCOME_TARGET_2_HIT = "TARGET_2_HIT"


@dataclass(frozen=True)
class HistoricalTradePlan:
    signal_id: str
    symbol: str
    signal_date: str
    entry_trigger: float
    stop_loss: float
    target_1: float
    target_2: float | None = None
    valid_until: str | None = None
    entry_type: str | None = None
    setup_type: str | None = None
    stop_model: str | None = None
    exit_model: str | None = None

    @property
    def initial_risk(self) -> float:
        return float(self.entry_trigger) - float(self.stop_loss)


@dataclass(frozen=True)
class HistoricalTradePlanRejection:
    plan_index: int
    signal_id: str | None
    symbol: str | None
    reasons: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class HistoricalTradePlanLoadReport:
    input_plan_count: int
    accepted_plan_count: int
    rejected_plan_count: int
    rejection_reasons: list[HistoricalTradePlanRejection] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "input_plan_count": self.input_plan_count,
            "accepted_plan_count": self.accepted_plan_count,
            "rejected_plan_count": self.rejected_plan_count,
            "rejection_reasons": [rejection.to_dict() for rejection in self.rejection_reasons],
        }


@dataclass(frozen=True)
class HistoricalTradePlanLoadResult:
    plans: list[HistoricalTradePlan]
    report: HistoricalTradePlanLoadReport


@dataclass(frozen=True)
class HistoricalBacktestResult:
    signal_id: str
    symbol: str
    signal_date: str
    outcome: str
    entry_hit: bool
    target_1_hit: bool
    target_2_hit: bool
    stop_hit: bool
    false_breakout: bool
    entry_date: str | None = None
    exit_date: str | None = None
    exit_price: float | None = None
    r_multiple: float = 0.0
    bars_evaluated: int = 0
    reason: str = ""
    entry_type: str | None = None
    setup_type: str | None = None
    stop_model: str | None = None
    exit_model: str | None = None
    entry_price: float | None = None
    entry_trigger: float | None = None
    initial_stop_loss: float | None = None
    target_1: float | None = None
    target_2: float | None = None
    max_favorable_excursion_r: float | None = None
    max_adverse_excursion_r: float | None = None
    same_bar_ambiguous: bool = False
    missing_field_reasons: dict[str, str] = field(default_factory=dict)
    signal_day_cluster_size: int | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class HistoricalBacktestMetrics:
    total: int
    entry_hit_rate: float
    expired_without_entry_rate: float
    stop_hit_rate: float
    target_1_hit_rate: float
    target_2_hit_rate: float
    false_breakout_rate: float
    average_r: float
    expectancy_r: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class HistoricalBacktestReport:
    metrics: HistoricalBacktestMetrics
    results: list[HistoricalBacktestResult] = field(default_factory=list)
    run_id: str = "historical-demo-run"
    data_source: str = "historical_demo"
    is_demo: bool = True
    symbol_universe: list[str] = field(default_factory=list)
    date_range: dict[str, str] = field(default_factory=dict)
    strategy_version: str = "historical-entry-exit-v1"
    tags: list[str] = field(default_factory=lambda: ["demo", "public_safe", "research_only"])
    input_pack_gate_status: str = "NOT_RUN"
    input_completeness_status: str = "UNKNOWN"
    run_health_status: str = "UNKNOWN"
    coverage_manifest_path: str = ""
    survivorship_universe_path: str = ""
    trade_plans_path: str = ""
    input_plan_count: int = 0
    accepted_plan_count: int = 0
    rejected_plan_count: int = 0
    rejection_reasons: list[dict[str, Any]] = field(default_factory=list)
    live_trading_authorized: bool = False
    broker_execution_mode: str = "paper_only"

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "data_source": self.data_source,
            "is_demo": self.is_demo,
            "symbol_universe": self.symbol_universe,
            "date_range": self.date_range,
            "strategy_version": self.strategy_version,
            "tags": self.tags,
            "input_pack_gate_status": self.input_pack_gate_status,
            "input_completeness_status": self.input_completeness_status,
            "run_health_status": self.run_health_status,
            "coverage_manifest_path": self.coverage_manifest_path,
            "survivorship_universe_path": self.survivorship_universe_path,
            "trade_plans_path": self.trade_plans_path,
            "input_plan_count": self.input_plan_count,
            "accepted_plan_count": self.accepted_plan_count,
            "rejected_plan_count": self.rejected_plan_count,
            "rejection_reasons": self.rejection_reasons,
            "metrics": self.metrics.to_dict(),
            "results": [result.to_dict() for result in self.results],
            "live_trading_authorized": self.live_trading_authorized,
            "broker_execution_mode": self.broker_execution_mode,
        }
