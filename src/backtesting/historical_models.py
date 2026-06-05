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

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "data_source": self.data_source,
            "is_demo": self.is_demo,
            "symbol_universe": self.symbol_universe,
            "date_range": self.date_range,
            "strategy_version": self.strategy_version,
            "tags": self.tags,
            "metrics": self.metrics.to_dict(),
            "results": [result.to_dict() for result in self.results],
        }
