"""Portfolio state model and JSON persistence."""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from src.persistence.atomic_write import write_json_atomic


DEFAULT_PORTFOLIO_STATE_PATH = Path("data/portfolio_state.json")


class PortfolioStateError(RuntimeError):
    """Raised when a portfolio state file exists but cannot be trusted."""


@dataclass(frozen=True)
class PortfolioPosition:
    """Minimal open-position snapshot used for auditability."""

    symbol: str
    side: str
    entry: float | None = None
    current: float | None = None
    risk_amount: float | None = None
    unrealized_pnl: float | None = None

    @classmethod
    def from_mapping(cls, payload: dict[str, Any]) -> "PortfolioPosition":
        return cls(
            symbol=str(payload.get("symbol", "")),
            side=str(payload.get("side", "")),
            entry=_optional_safe_float(payload.get("entry")),
            current=_optional_safe_float(payload.get("current")),
            risk_amount=_optional_safe_float(payload.get("risk_amount")),
            unrealized_pnl=_optional_safe_float(payload.get("unrealized_pnl")),
        )


@dataclass(frozen=True)
class PortfolioState:
    """Portfolio-level risk state consumed by runtime governance."""

    equity_start: float
    equity_current: float
    drawdown_percent: float
    daily_loss_percent: float
    open_positions: list[PortfolioPosition] = field(default_factory=list)
    updated_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    source: str = "portfolio_state_json"
    warnings: list[str] = field(default_factory=list)
    governance_valid: bool = True

    @classmethod
    def from_mapping(cls, payload: dict[str, Any]) -> "PortfolioState":
        open_positions_payload = payload.get("open_positions", [])
        if not isinstance(open_positions_payload, list):
            raise PortfolioStateError("open_positions must be a list")
        if "governance_valid" not in payload:
            raise PortfolioStateError("Missing required portfolio state field: governance_valid")
        if not isinstance(payload.get("governance_valid"), bool):
            raise PortfolioStateError("governance_valid must be a boolean")

        return cls(
            equity_start=_required_safe_float(payload, "equity_start"),
            equity_current=_required_safe_float(payload, "equity_current"),
            drawdown_percent=_required_safe_float(payload, "drawdown_percent"),
            daily_loss_percent=_required_safe_float(payload, "daily_loss_percent"),
            open_positions=[
                PortfolioPosition.from_mapping(item)
                for item in open_positions_payload
                if isinstance(item, dict)
            ],
            updated_at=str(payload.get("updated_at") or datetime.now(UTC).isoformat()),
            source=str(payload.get("source") or "portfolio_state_json"),
            warnings=[str(item) for item in payload.get("warnings", []) if item],
            governance_valid=payload["governance_valid"],
        )

    @classmethod
    def conservative_default(cls, warning: str, *, source: str = "missing_portfolio_state_fail_closed") -> "PortfolioState":
        """Return a non-crashing fallback that is visibly degraded and fail-closed."""

        return cls(
            equity_start=0.0,
            equity_current=0.0,
            drawdown_percent=0.0,
            daily_loss_percent=0.0,
            open_positions=[],
            updated_at=datetime.now(UTC).isoformat(),
            source=source,
            warnings=[
                warning,
                "Portfolio state is missing, invalid or unavailable. Runtime governance must fail closed until real state is provided.",
            ],
            governance_valid=False,
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class PortfolioStateStore:
    """Read/write portfolio state from a deterministic JSON file."""

    def __init__(self, path: Path | str = DEFAULT_PORTFOLIO_STATE_PATH) -> None:
        self.path = Path(path)

    def load(self) -> PortfolioState:
        if not self.path.exists():
            return PortfolioState.conservative_default(
                f"Portfolio state file missing: {self.path}. Governance is invalid until real portfolio state exists."
            )

        try:
            payload = json.loads(self.path.read_text(encoding="utf-8"))
            if not isinstance(payload, dict):
                raise PortfolioStateError(f"Portfolio state must be a JSON object: {self.path}")
            return PortfolioState.from_mapping(payload)
        except (json.JSONDecodeError, PortfolioStateError) as exc:
            return PortfolioState.conservative_default(
                f"Invalid portfolio state JSON: {self.path}: {exc}",
                source="invalid_portfolio_state_fail_closed",
            )

    def save(self, state: PortfolioState) -> Path:
        return write_json_atomic(self.path, state.to_dict())


def _required_safe_float(payload: dict[str, Any], key: str) -> float:
    if key not in payload:
        raise PortfolioStateError(f"Missing required portfolio state field: {key}")
    return _safe_float(payload[key], field_name=key)


def _optional_safe_float(value: Any) -> float | None:
    if value is None:
        return None
    return _safe_float(value, field_name="optional_position_value")


def _safe_float(value: Any, field_name: str) -> float:
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise PortfolioStateError(f"Invalid numeric portfolio state field {field_name}: {value!r}") from exc

    if not math.isfinite(result):
        raise PortfolioStateError(f"Non-finite portfolio state field {field_name}: {value!r}")

    return result
