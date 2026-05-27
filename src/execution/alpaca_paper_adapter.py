from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Protocol
from uuid import uuid4

from src.execution.broker_adapter import (
    BrokerAccountSnapshot,
    BrokerFill,
    BrokerMode,
    BrokerOrder,
    BrokerOrderRequest,
    BrokerPosition,
    BrokerReconciliationReport,
    OrderSide,
    OrderStatus,
    OrderType,
)


ALPACA_PAPER_ENDPOINT = "https://paper-api.alpaca.markets"


class AlpacaPaperTransport(Protocol):
    def post_order(self, payload: dict[str, object]) -> dict[str, Any]: ...

    def cancel_order(self, order_id: str) -> None: ...

    def get_order(self, order_id: str) -> dict[str, Any]: ...

    def list_orders(self) -> list[dict[str, Any]]: ...

    def list_positions(self) -> list[dict[str, Any]]: ...

    def list_fills(self) -> list[dict[str, Any]]: ...

    def get_account(self) -> dict[str, Any]: ...


@dataclass(frozen=True)
class AlpacaPaperAdapterConfig:
    endpoint: str = ALPACA_PAPER_ENDPOINT
    account_id: str = "alpaca-paper"
    time_in_force: str = "day"


class AlpacaPaperAdapter:
    mode = BrokerMode.PAPER

    def __init__(self, config: AlpacaPaperAdapterConfig, *, transport: AlpacaPaperTransport) -> None:
        _validate_config(config)
        self.config = config
        self.transport = transport

    def submit_order(self, request: BrokerOrderRequest) -> BrokerOrder:
        issues = _validate_order_request(request)
        if issues:
            return _rejected_order(request, "; ".join(issues))

        payload: dict[str, object] = {
            "symbol": request.symbol.strip().upper(),
            "side": request.side.value,
            "qty": request.quantity,
            "type": request.order_type.value,
            "time_in_force": self.config.time_in_force,
            "client_order_id": request.client_order_id or f"ite-{uuid4().hex}",
        }
        if request.limit_price is not None:
            payload["limit_price"] = request.limit_price
        if request.stop_price is not None:
            payload["stop_price"] = request.stop_price

        response = self.transport.post_order(payload)
        return _alpaca_order_to_broker_order(response, strategy_id=request.strategy_id, signal_id=request.signal_id)

    def cancel_order(self, order_id: str) -> BrokerOrder:
        if not order_id.strip():
            raise ValueError("order_id is required")
        self.transport.cancel_order(order_id)
        return self.get_order_status(order_id)

    def get_order_status(self, order_id: str) -> BrokerOrder:
        if not order_id.strip():
            raise ValueError("order_id is required")
        return _alpaca_order_to_broker_order(self.transport.get_order(order_id), strategy_id="unknown", signal_id="unknown")

    def list_positions(self) -> list[BrokerPosition]:
        return [_alpaca_position_to_broker_position(item) for item in self.transport.list_positions()]

    def list_fills(self) -> list[BrokerFill]:
        return [_alpaca_fill_to_broker_fill(item) for item in self.transport.list_fills()]

    def get_account_snapshot(self) -> BrokerAccountSnapshot:
        account = self.transport.get_account()
        return BrokerAccountSnapshot(
            account_id=str(account.get("id") or self.config.account_id),
            mode=self.mode,
            cash=_as_float(account.get("cash"), field="cash"),
            equity=_as_float(account.get("equity"), field="equity"),
            buying_power=_as_float(account.get("buying_power"), field="buying_power"),
            captured_at=_now_iso(),
        )

    def reconcile_orders(self) -> BrokerReconciliationReport:
        orders = [
            _alpaca_order_to_broker_order(item, strategy_id="unknown", signal_id="unknown")
            for item in self.transport.list_orders()
        ]
        fills = self.list_fills()
        positions = self.list_positions()
        issues: list[str] = []

        for order in orders:
            if order.status in {OrderStatus.ACCEPTED, OrderStatus.PARTIALLY_FILLED} and order.quantity <= 0:
                issues.append(f"active order has invalid quantity: {order.order_id}")
            if order.status == OrderStatus.FILLED and not any(fill.order_id == order.order_id for fill in fills):
                issues.append(f"filled order without fill activity: {order.order_id}")

        return BrokerReconciliationReport(
            passed=not issues,
            mode=self.mode,
            order_count=len(orders),
            fill_count=len(fills),
            position_count=len(positions),
            issues=issues,
        )


class InMemoryAlpacaPaperTransport:
    def __init__(self, *, account_id: str = "alpaca-paper-test", cash: float = 100_000.0) -> None:
        self.account_id = account_id
        self.cash = cash
        self.orders: dict[str, dict[str, Any]] = {}
        self.fills: list[dict[str, Any]] = []
        self.positions: list[dict[str, Any]] = []

    def post_order(self, payload: dict[str, object]) -> dict[str, Any]:
        order_id = f"alpaca-paper-{uuid4().hex}"
        order = {
            "id": order_id,
            "client_order_id": payload.get("client_order_id"),
            "symbol": payload["symbol"],
            "side": payload["side"],
            "qty": payload["qty"],
            "type": payload["type"],
            "status": "accepted",
            "limit_price": payload.get("limit_price"),
            "stop_price": payload.get("stop_price"),
            "submitted_at": _now_iso(),
        }
        self.orders[order_id] = order
        return order

    def cancel_order(self, order_id: str) -> None:
        if order_id not in self.orders:
            raise KeyError(f"unknown alpaca paper order id: {order_id}")
        self.orders[order_id]["status"] = "canceled"

    def get_order(self, order_id: str) -> dict[str, Any]:
        if order_id not in self.orders:
            raise KeyError(f"unknown alpaca paper order id: {order_id}")
        return dict(self.orders[order_id])

    def list_orders(self) -> list[dict[str, Any]]:
        return [dict(order) for order in self.orders.values()]

    def list_positions(self) -> list[dict[str, Any]]:
        return [dict(position) for position in self.positions]

    def list_fills(self) -> list[dict[str, Any]]:
        return [dict(fill) for fill in self.fills]

    def get_account(self) -> dict[str, Any]:
        return {
            "id": self.account_id,
            "cash": str(self.cash),
            "equity": str(self.cash),
            "buying_power": str(self.cash),
        }


def _validate_config(config: AlpacaPaperAdapterConfig) -> None:
    if config.endpoint.rstrip("/") != ALPACA_PAPER_ENDPOINT:
        raise ValueError("AlpacaPaperAdapter only allows the official paper endpoint")
    if config.time_in_force not in {"day", "gtc", "opg", "cls", "ioc", "fok"}:
        raise ValueError("unsupported Alpaca time_in_force")


def _validate_order_request(request: BrokerOrderRequest) -> list[str]:
    issues: list[str] = []
    if not request.symbol.strip():
        issues.append("symbol is required")
    if request.quantity <= 0:
        issues.append("quantity must be positive")
    if not request.strategy_id.strip():
        issues.append("strategy_id is required")
    if not request.signal_id.strip():
        issues.append("signal_id is required")
    if request.order_type == OrderType.LIMIT and request.limit_price is None:
        issues.append("limit_price is required for limit orders")
    if request.order_type == OrderType.STOP and request.stop_price is None:
        issues.append("stop_price is required for stop orders")
    return issues


def _rejected_order(request: BrokerOrderRequest, reason: str) -> BrokerOrder:
    return BrokerOrder(
        order_id=request.client_order_id or f"alpaca-paper-rejected-{uuid4().hex}",
        symbol=request.symbol.strip().upper(),
        side=request.side,
        quantity=request.quantity,
        order_type=request.order_type,
        status=OrderStatus.REJECTED,
        strategy_id=request.strategy_id,
        signal_id=request.signal_id,
        submitted_at=_now_iso(),
        client_order_id=request.client_order_id,
        limit_price=request.limit_price,
        stop_price=request.stop_price,
        reason=reason,
    )


def _alpaca_order_to_broker_order(payload: dict[str, Any], *, strategy_id: str, signal_id: str) -> BrokerOrder:
    return BrokerOrder(
        order_id=str(payload.get("id") or payload.get("client_order_id") or f"alpaca-paper-{uuid4().hex}"),
        symbol=str(payload.get("symbol", "")).upper(),
        side=OrderSide(str(payload.get("side", OrderSide.BUY.value)).lower()),
        quantity=_as_float(payload.get("qty"), field="qty"),
        order_type=OrderType(str(payload.get("type", OrderType.MARKET.value)).lower()),
        status=_map_alpaca_status(str(payload.get("status", "new"))),
        strategy_id=str(payload.get("strategy_id") or strategy_id),
        signal_id=str(payload.get("signal_id") or signal_id),
        submitted_at=str(payload.get("submitted_at") or payload.get("created_at") or _now_iso()),
        client_order_id=payload.get("client_order_id"),
        limit_price=_optional_float(payload.get("limit_price"), field="limit_price"),
        stop_price=_optional_float(payload.get("stop_price"), field="stop_price"),
        reason=payload.get("failed_at") or payload.get("rejected_at"),
    )


def _alpaca_position_to_broker_position(payload: dict[str, Any]) -> BrokerPosition:
    return BrokerPosition(
        symbol=str(payload.get("symbol", "")).upper(),
        quantity=_as_float(payload.get("qty"), field="qty"),
        market_value=_as_float(payload.get("market_value"), field="market_value"),
        average_price=_as_float(payload.get("avg_entry_price"), field="avg_entry_price"),
        unrealized_pnl=_as_float(payload.get("unrealized_pl"), field="unrealized_pl", default=0.0),
    )


def _alpaca_fill_to_broker_fill(payload: dict[str, Any]) -> BrokerFill:
    return BrokerFill(
        fill_id=str(payload.get("id") or f"fill-{uuid4().hex}"),
        order_id=str(payload.get("order_id", "")),
        symbol=str(payload.get("symbol", "")).upper(),
        side=OrderSide(str(payload.get("side", OrderSide.BUY.value)).lower()),
        quantity=_as_float(payload.get("qty"), field="qty"),
        fill_price=_as_float(payload.get("price"), field="price"),
        filled_at=str(payload.get("transaction_time") or _now_iso()),
        commission=_as_float(payload.get("commission"), field="commission", default=0.0),
    )


def _map_alpaca_status(status: str) -> OrderStatus:
    mapping = {
        "new": OrderStatus.NEW,
        "accepted": OrderStatus.ACCEPTED,
        "accepted_for_bidding": OrderStatus.ACCEPTED,
        "pending_new": OrderStatus.NEW,
        "partially_filled": OrderStatus.PARTIALLY_FILLED,
        "filled": OrderStatus.FILLED,
        "done_for_day": OrderStatus.ACCEPTED,
        "canceled": OrderStatus.CANCELLED,
        "cancelled": OrderStatus.CANCELLED,
        "expired": OrderStatus.CANCELLED,
        "replaced": OrderStatus.ACCEPTED,
        "pending_cancel": OrderStatus.ACCEPTED,
        "pending_replace": OrderStatus.ACCEPTED,
        "rejected": OrderStatus.REJECTED,
        "stopped": OrderStatus.REJECTED,
        "suspended": OrderStatus.REJECTED,
        "calculated": OrderStatus.ACCEPTED,
    }
    return mapping.get(status.lower(), OrderStatus.REJECTED)


def _as_float(value: Any, *, field: str, default: float | None = None) -> float:
    if value is None:
        if default is not None:
            return default
        raise ValueError(f"missing numeric Alpaca field: {field}")
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"invalid numeric Alpaca field {field}: {value!r}") from exc


def _optional_float(value: Any, *, field: str) -> float | None:
    if value in {None, ""}:
        return None
    return _as_float(value, field=field)


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()
