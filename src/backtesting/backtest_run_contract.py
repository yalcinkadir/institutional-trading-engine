from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

CONTRACT_SCHEMA_VERSION = "bt1.backtest_run_contract.v1"
_IDENTIFIER_PATTERN = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9_.:-]{1,127}$")
_DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")


class BacktestContractError(ValueError):
    """Raised when a backtest run contract is invalid."""


@dataclass(frozen=True)
class BacktestUniverse:
    universe_id: str
    symbols: tuple[str, ...] = field(default_factory=tuple)
    point_in_time: bool = False
    survivorship_bias_safe: bool = False
    notes: str | None = None

    def normalized(self) -> "BacktestUniverse":
        return BacktestUniverse(
            universe_id=self.universe_id.strip(),
            symbols=tuple(sorted({symbol.strip().upper() for symbol in self.symbols if symbol.strip()})),
            point_in_time=bool(self.point_in_time),
            survivorship_bias_safe=bool(self.survivorship_bias_safe),
            notes=self.notes.strip() if isinstance(self.notes, str) and self.notes.strip() else None,
        )


@dataclass(frozen=True)
class BacktestExecutionAssumptions:
    slippage_model: str
    commission_model: str
    fill_model: str = "next_bar_open"
    latency_model: str = "none"
    partial_fill_model: str = "none"
    market_impact_model: str = "none"

    def normalized(self) -> "BacktestExecutionAssumptions":
        return BacktestExecutionAssumptions(
            slippage_model=self.slippage_model.strip(),
            commission_model=self.commission_model.strip(),
            fill_model=self.fill_model.strip(),
            latency_model=self.latency_model.strip(),
            partial_fill_model=self.partial_fill_model.strip(),
            market_impact_model=self.market_impact_model.strip(),
        )


@dataclass(frozen=True)
class BacktestRunContract:
    strategy_id: str
    strategy_version: str
    universe: BacktestUniverse
    start_date: str
    end_date: str
    data_source: str
    data_source_version: str
    threshold_version: str
    setup_config_version: str
    execution_assumptions: BacktestExecutionAssumptions
    benchmark_id: str = "SPY"
    run_purpose: str = "research"
    schema_version: str = CONTRACT_SCHEMA_VERSION
    created_at_utc: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def normalized(self) -> "BacktestRunContract":
        return BacktestRunContract(
            strategy_id=self.strategy_id.strip(),
            strategy_version=self.strategy_version.strip(),
            universe=self.universe.normalized(),
            start_date=self.start_date.strip(),
            end_date=self.end_date.strip(),
            data_source=self.data_source.strip(),
            data_source_version=self.data_source_version.strip(),
            threshold_version=self.threshold_version.strip(),
            setup_config_version=self.setup_config_version.strip(),
            execution_assumptions=self.execution_assumptions.normalized(),
            benchmark_id=self.benchmark_id.strip().upper(),
            run_purpose=self.run_purpose.strip(),
            schema_version=self.schema_version.strip(),
            created_at_utc=self.created_at_utc,
            metadata={key: self.metadata[key] for key in sorted(self.metadata)},
        )

    def to_public_dict(self, *, include_created_at: bool = False) -> dict[str, Any]:
        payload = asdict(self.normalized())
        if not include_created_at:
            payload["created_at_utc"] = None
        return payload

    def contract_id(self) -> str:
        payload = json.dumps(self.to_public_dict(include_created_at=False), sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:24]

    def with_created_at(self) -> "BacktestRunContract":
        return BacktestRunContract(
            **{**asdict(self), "created_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat()}
        )


def _validate_identifier(name: str, value: str) -> None:
    if not value or not _IDENTIFIER_PATTERN.match(value):
        raise BacktestContractError(f"{name} must be a stable identifier")


def _validate_date(name: str, value: str) -> None:
    if not _DATE_PATTERN.match(value):
        raise BacktestContractError(f"{name} must use YYYY-MM-DD format")


def validate_backtest_run_contract(contract: BacktestRunContract) -> BacktestRunContract:
    normalized = contract.normalized()
    if normalized.schema_version != CONTRACT_SCHEMA_VERSION:
        raise BacktestContractError(f"schema_version must be {CONTRACT_SCHEMA_VERSION}")

    for field_name in (
        "strategy_id",
        "strategy_version",
        "data_source",
        "data_source_version",
        "threshold_version",
        "setup_config_version",
        "benchmark_id",
        "run_purpose",
    ):
        _validate_identifier(field_name, getattr(normalized, field_name))

    _validate_identifier("universe_id", normalized.universe.universe_id)
    _validate_date("start_date", normalized.start_date)
    _validate_date("end_date", normalized.end_date)
    if normalized.start_date >= normalized.end_date:
        raise BacktestContractError("start_date must be before end_date")

    if not normalized.universe.symbols:
        raise BacktestContractError("universe.symbols must contain at least one symbol")

    for symbol in normalized.universe.symbols:
        _validate_identifier("symbol", symbol)

    for field_name in (
        "slippage_model",
        "commission_model",
        "fill_model",
        "latency_model",
        "partial_fill_model",
        "market_impact_model",
    ):
        _validate_identifier(field_name, getattr(normalized.execution_assumptions, field_name))

    return normalized

def with_created_at(self) -> "BacktestRunContract":
    return BacktestRunContract(
        strategy_id=self.strategy_id,
        strategy_version=self.strategy_version,
        universe=self.universe,
        start_date=self.start_date,
        end_date=self.end_date,
        data_source=self.data_source,
        data_source_version=self.data_source_version,
        threshold_version=self.threshold_version,
        setup_config_version=self.setup_config_version,
        execution_assumptions=self.execution_assumptions,
        benchmark_id=self.benchmark_id,
        run_purpose=self.run_purpose,
        schema_version=self.schema_version,
        created_at_utc=datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        metadata=dict(self.metadata),
    )

def backtest_run_contract_from_dict(payload: dict[str, Any]) -> BacktestRunContract:
    universe_payload = payload.get("universe") or {}
    execution_payload = payload.get("execution_assumptions") or {}
    metadata = payload.get("metadata") or {}
    if not isinstance(metadata, dict):
        raise BacktestContractError("metadata must be an object")
    return BacktestRunContract(
        strategy_id=str(payload.get("strategy_id", "")),
        strategy_version=str(payload.get("strategy_version", "")),
        universe=BacktestUniverse(
            universe_id=str(universe_payload.get("universe_id", "")),
            symbols=tuple(universe_payload.get("symbols", ()) or ()),
            point_in_time=bool(universe_payload.get("point_in_time", False)),
            survivorship_bias_safe=bool(universe_payload.get("survivorship_bias_safe", False)),
            notes=universe_payload.get("notes"),
        ),
        start_date=str(payload.get("start_date", "")),
        end_date=str(payload.get("end_date", "")),
        data_source=str(payload.get("data_source", "")),
        data_source_version=str(payload.get("data_source_version", "")),
        threshold_version=str(payload.get("threshold_version", "")),
        setup_config_version=str(payload.get("setup_config_version", "")),
        execution_assumptions=BacktestExecutionAssumptions(
            slippage_model=str(execution_payload.get("slippage_model", "")),
            commission_model=str(execution_payload.get("commission_model", "")),
            fill_model=str(execution_payload.get("fill_model", "next_bar_open")),
            latency_model=str(execution_payload.get("latency_model", "none")),
            partial_fill_model=str(execution_payload.get("partial_fill_model", "none")),
            market_impact_model=str(execution_payload.get("market_impact_model", "none")),
        ),
        benchmark_id=str(payload.get("benchmark_id", "SPY")),
        run_purpose=str(payload.get("run_purpose", "research")),
        schema_version=str(payload.get("schema_version", CONTRACT_SCHEMA_VERSION)),
        created_at_utc=payload.get("created_at_utc"),
        metadata=metadata,
    )


def load_backtest_run_contract(path: str | Path) -> BacktestRunContract:
    return backtest_run_contract_from_dict(json.loads(Path(path).read_text(encoding="utf-8")))


def write_backtest_run_contract(contract: BacktestRunContract, path: str | Path) -> dict[str, Any]:
    normalized = validate_backtest_run_contract(contract)
    payload = normalized.to_public_dict(include_created_at=True)
    payload["contract_id"] = normalized.contract_id()
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return payload
