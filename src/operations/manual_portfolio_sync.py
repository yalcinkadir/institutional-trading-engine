"""Manual portfolio synchronization without broker integration.

This module converts a manually maintained portfolio snapshot into the
runtime/governance-compatible portfolio_state.json structure.

It intentionally does not connect to a broker and does not place orders.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping


class ManualPortfolioSyncError(ValueError):
    """Raised when a manual portfolio snapshot cannot be converted."""


@dataclass(frozen=True)
class ManualPortfolioPosition:
    symbol: str
    quantity: float
    market_value: float
    unrealized_pnl: float = 0.0
    side: str = "long"

    def to_dict(self) -> dict[str, Any]:
        return {
            "symbol": self.symbol,
            "quantity": self.quantity,
            "market_value": self.market_value,
            "unrealized_pnl": self.unrealized_pnl,
            "side": self.side,
        }


@dataclass(frozen=True)
class ManualPortfolioSnapshot:
    equity_start: float
    equity_peak: float
    equity_previous_close: float
    equity_current: float
    cash: float | None = None
    positions: tuple[ManualPortfolioPosition, ...] = ()
    source: str = "manual_portfolio_snapshot"
    snapshot_time: str | None = None


@dataclass(frozen=True)
class ManualPortfolioSyncResult:
    portfolio_state: dict[str, Any]
    report: dict[str, Any]
    warnings: tuple[str, ...] = field(default_factory=tuple)


def _as_float(payload: Mapping[str, Any], key: str) -> float:
    if key not in payload:
        raise ManualPortfolioSyncError(f"missing_required_field:{key}")
    value = payload[key]
    try:
        numeric = float(value)
    except (TypeError, ValueError) as exc:
        raise ManualPortfolioSyncError(f"invalid_numeric_field:{key}") from exc
    if numeric != numeric or numeric in (float("inf"), float("-inf")):
        raise ManualPortfolioSyncError(f"non_finite_numeric_field:{key}")
    return numeric


def _optional_float(payload: Mapping[str, Any], key: str) -> float | None:
    if key not in payload or payload[key] is None:
        return None
    try:
        numeric = float(payload[key])
    except (TypeError, ValueError) as exc:
        raise ManualPortfolioSyncError(f"invalid_numeric_field:{key}") from exc
    if numeric != numeric or numeric in (float("inf"), float("-inf")):
        raise ManualPortfolioSyncError(f"non_finite_numeric_field:{key}")
    return numeric


def _parse_position(payload: Mapping[str, Any], index: int) -> ManualPortfolioPosition:
    symbol = str(payload.get("symbol", "")).strip().upper()
    if not symbol:
        raise ManualPortfolioSyncError(f"position_{index}:missing_symbol")

    quantity = _as_float(payload, "quantity")
    market_value = _as_float(payload, "market_value")
    unrealized_pnl = _optional_float(payload, "unrealized_pnl") or 0.0
    side = str(payload.get("side", "long")).strip().lower() or "long"
    if side not in {"long", "short", "cash", "hedge"}:
        raise ManualPortfolioSyncError(f"position_{index}:invalid_side")

    return ManualPortfolioPosition(
        symbol=symbol,
        quantity=quantity,
        market_value=market_value,
        unrealized_pnl=unrealized_pnl,
        side=side,
    )


def load_manual_portfolio_snapshot(path: str | Path) -> ManualPortfolioSnapshot:
    snapshot_path = Path(path)
    try:
        payload = json.loads(snapshot_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ManualPortfolioSyncError(f"snapshot_file_missing:{snapshot_path}") from exc
    except json.JSONDecodeError as exc:
        raise ManualPortfolioSyncError(f"snapshot_file_invalid_json:{snapshot_path}") from exc

    if not isinstance(payload, dict):
        raise ManualPortfolioSyncError("snapshot_must_be_json_object")

    positions_payload = payload.get("positions", [])
    if positions_payload is None:
        positions_payload = []
    if not isinstance(positions_payload, list):
        raise ManualPortfolioSyncError("positions_must_be_list")

    positions = tuple(
        _parse_position(position, index)
        for index, position in enumerate(positions_payload)
        if isinstance(position, Mapping)
    )
    if len(positions) != len(positions_payload):
        raise ManualPortfolioSyncError("positions_must_contain_objects")

    return ManualPortfolioSnapshot(
        equity_start=_as_float(payload, "equity_start"),
        equity_peak=_as_float(payload, "equity_peak"),
        equity_previous_close=_as_float(payload, "equity_previous_close"),
        equity_current=_as_float(payload, "equity_current"),
        cash=_optional_float(payload, "cash"),
        positions=positions,
        source=str(payload.get("source", "manual_portfolio_snapshot")),
        snapshot_time=str(payload.get("snapshot_time")) if payload.get("snapshot_time") else None,
    )


def _percent_loss(reference: float, current: float) -> float:
    if reference <= 0:
        raise ManualPortfolioSyncError("reference_equity_must_be_positive")
    return round(max(0.0, ((reference - current) / reference) * 100.0), 4)


def build_manual_portfolio_state(snapshot: ManualPortfolioSnapshot) -> ManualPortfolioSyncResult:
    warnings: list[str] = []

    if snapshot.equity_start <= 0:
        raise ManualPortfolioSyncError("equity_start_must_be_positive")
    if snapshot.equity_peak <= 0:
        raise ManualPortfolioSyncError("equity_peak_must_be_positive")
    if snapshot.equity_previous_close <= 0:
        raise ManualPortfolioSyncError("equity_previous_close_must_be_positive")
    if snapshot.equity_current < 0:
        raise ManualPortfolioSyncError("equity_current_must_not_be_negative")
    if snapshot.equity_peak < snapshot.equity_current:
        warnings.append("equity_peak_below_current_equity_adjusted_for_drawdown_reference")

    drawdown_reference = max(snapshot.equity_peak, snapshot.equity_current)
    drawdown_percent = _percent_loss(drawdown_reference, snapshot.equity_current)
    daily_loss_percent = _percent_loss(snapshot.equity_previous_close, snapshot.equity_current)

    total_position_value = round(sum(position.market_value for position in snapshot.positions), 4)
    total_unrealized_pnl = round(sum(position.unrealized_pnl for position in snapshot.positions), 4)

    generated_at = datetime.now(timezone.utc).isoformat()
    open_positions = [position.to_dict() for position in snapshot.positions]

    portfolio_state = {
        "equity_start": snapshot.equity_start,
        "equity_current": snapshot.equity_current,
        "drawdown_percent": drawdown_percent,
        "daily_loss_percent": daily_loss_percent,
        "open_positions": open_positions,
        "source": "manual_portfolio_sync",
        "warnings": warnings,
        "metadata": {
            "generated_at": generated_at,
            "snapshot_time": snapshot.snapshot_time,
            "snapshot_source": snapshot.source,
            "equity_peak": snapshot.equity_peak,
            "equity_previous_close": snapshot.equity_previous_close,
            "cash": snapshot.cash,
            "total_position_value": total_position_value,
            "total_unrealized_pnl": total_unrealized_pnl,
            "broker_api_used": False,
        },
    }

    report = {
        "generated_at": generated_at,
        "status": "PASS",
        "broker_api_used": False,
        "calculated_fields": {
            "drawdown_percent": drawdown_percent,
            "daily_loss_percent": daily_loss_percent,
            "total_position_value": total_position_value,
            "total_unrealized_pnl": total_unrealized_pnl,
            "open_position_count": len(open_positions),
        },
        "warnings": warnings,
        "portfolio_state": portfolio_state,
    }

    return ManualPortfolioSyncResult(
        portfolio_state=portfolio_state,
        report=report,
        warnings=tuple(warnings),
    )


def write_manual_portfolio_sync_outputs(
    result: ManualPortfolioSyncResult,
    portfolio_state_path: str | Path,
    report_json_path: str | Path,
    report_md_path: str | Path,
) -> None:
    state_path = Path(portfolio_state_path)
    json_path = Path(report_json_path)
    md_path = Path(report_md_path)

    state_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)

    state_path.write_text(json.dumps(result.portfolio_state, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    json_path.write_text(json.dumps(result.report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    calculated = result.report["calculated_fields"]
    md_lines = [
        "# Manual Portfolio Sync Report",
        "",
        f"Generated at: `{result.report['generated_at']}`",
        "",
        "## Scope",
        "",
        "- Broker API used: `false`",
        "- Order execution: `false`",
        "- Purpose: governance-compatible manual portfolio state",
        "",
        "## Calculated Fields",
        "",
        f"- Drawdown percent: `{calculated['drawdown_percent']}`",
        f"- Daily loss percent: `{calculated['daily_loss_percent']}`",
        f"- Total position value: `{calculated['total_position_value']}`",
        f"- Total unrealized PnL: `{calculated['total_unrealized_pnl']}`",
        f"- Open positions: `{calculated['open_position_count']}`",
        "",
        "## Warnings",
        "",
    ]
    if result.warnings:
        md_lines.extend(f"- `{warning}`" for warning in result.warnings)
    else:
        md_lines.append("- none")
    md_lines.append("")
    md_path.write_text("\n".join(md_lines), encoding="utf-8")
