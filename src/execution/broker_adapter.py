from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Protocol
from uuid import uuid4


class BrokerMode(str, Enum):
    PAPER = "paper"


class OrderSide(str, Enum):
    BUY = "buy"
    SELL = "sell"


class OrderType(str, Enum):
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"


class OrderStatus(str, Enum):
    NEW = "new"
    ACCEPTED = "accepted"
    CANCELLED = "cancelled"
    REJECTED = "rejected"
    FILLED = "filled"
    PARTIALLY_FILLED = "partially_filled"


@dataclass(frozen=True)
class BrokerOrderRequest:
    symbol: str
    side: OrderSide
    quantity: float
    order_type: OrderType
    strategy_id: str
    signal_id: str
    limit_price: float | None = None
    stop_price: float | None = None
    client_order_id: str | None = None


@dataclass(frozen=True)
class BrokerOrder:
    order_id: str
    symbol: str
    side: OrderSide
    quantity: float
    order_type: OrderType
    status: OrderStatus
    strategy_id: str
    signal_id: str
    submitted_at: str
    client_order_id: str | None = None
    limit_price: float | None = None
    stop_price: float | None = None
    reason: str | None = None

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["side"] = self.side.value
        payload["order_type"] = self.order_type.value
        payload["status"] = self.status.value
        return payload


@dataclass(frozen=True)
class BrokerFill:
    fill_id: str
    order_id: str
    symbol: str
    side: OrderSide
    quantity: float
    fill_price: float
    filled_at: str
    commission: float = 0.0

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["side"] = self.side.value
        return payload


@dataclass(frozen=True)
class BrokerPosition:
    symbol: str
    quantity: float
    market_value: float
    average_price: float
    unrealized_pnl: float = 0.0

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class BrokerAccountSnapshot:
    account_id: str
    mode: BrokerMode
    cash: float
    equity: float
    buying_power: float
    captured_at: str

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["mode"] = self.mode.value
        return payload


@dataclass(frozen=True)
class BrokerReconciliationReport:
    passed: bool
    mode: BrokerMode
    order_count: int
    fill_count: int
    position_count: int
    issues: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["mode"] = self.mode.value
        return payload


class PaperBrokerAdapter(Protocol):
    mode: BrokerMode

    def submit_order(self, request: BrokerOrderRequest) -> BrokerOrder: ...

    def cancel_order(self, order_id: str) -> BrokerOrder: ...

    def get_order_status(self, order_id: str) -> BrokerOrder: ...

    def list_positions(self) -> list[BrokerPosition]: ...

    def list_fills(self) -> list[BrokerFill]: ...

    def get_account_snapshot(self) -> BrokerAccountSnapshot: ...

    def reconcile_orders(self) -> BrokerReconciliationReport: ...


class MockPaperBrokerAdapter:
    mode = BrokerMode.PAPER

    def __init__(self, *, account_id: str = "paper-mock", cash: float = 100_000.0) -> None:
        self._account_id = account_id
        self._cash = cash
        self._orders: dict[str, BrokerOrder] = {}
        self._fills: list[BrokerFill] = []
        self._positions: dict[str, BrokerPosition] = {}

    def submit_order(self, request: BrokerOrderRequest) -> BrokerOrder:
        issues = _validate_order_request(request)
        order_id = request.client_order_id or f"paper-{uuid4().hex}"
        status = OrderStatus.REJECTED if issues else OrderStatus.ACCEPTED
        order = BrokerOrder(
            order_id=order_id,
            symbol=request.symbol.strip().upper(),
            side=request.side,
            quantity=request.quantity,
            order_type=request.order_type,
            status=status,
            strategy_id=request.strategy_id,
            signal_id=request.signal_id,
            submitted_at=_now_iso(),
            client_order_id=request.client_order_id,
            limit_price=request.limit_price,
            stop_price=request.stop_price,
            reason="; ".join(issues) if issues else None,
        )
        self._orders[order_id] = order
        return order

    def cancel_order(self, order_id: str) -> BrokerOrder:
        order = self.get_order_status(order_id)
        if order.status in {OrderStatus.FILLED, OrderStatus.CANCELLED, OrderStatus.REJECTED}:
            return order
        cancelled = BrokerOrder(
            order_id=order.order_id,
            symbol=order.symbol,
            side=order.side,
            quantity=order.quantity,
            order_type=order.order_type,
            status=OrderStatus.CANCELLED,
            strategy_id=order.strategy_id,
            signal_id=order.signal_id,
            submitted_at=order.submitted_at,
            client_order_id=order.client_order_id,
            limit_price=order.limit_price,
            stop_price=order.stop_price,
            reason="cancelled by paper adapter",
        )
        self._orders[order_id] = cancelled
        return cancelled

    def get_order_status(self, order_id: str) -> BrokerOrder:
        if order_id not in self._orders:
            raise KeyError(f"unknown paper order id: {order_id}")
        return self._orders[order_id]

    def list_positions(self) -> list[BrokerPosition]:
        return list(self._positions.values())

    def list_fills(self) -> list[BrokerFill]:
        return list(self._fills)

    def get_account_snapshot(self) -> BrokerAccountSnapshot:
        return BrokerAccountSnapshot(
            account_id=self._account_id,
            mode=self.mode,
            cash=self._cash,
            equity=self._cash + sum(position.unrealized_pnl for position in self._positions.values()),
            buying_power=self._cash,
            captured_at=_now_iso(),
        )

    def reconcile_orders(self) -> BrokerReconciliationReport:
        issues: list[str] = []
        for order in self._orders.values():
            if order.status == OrderStatus.ACCEPTED and order.quantity <= 0:
                issues.append(f"accepted order has invalid quantity: {order.order_id}")
        return BrokerReconciliationReport(
            passed=not issues,
            mode=self.mode,
            order_count=len(self._orders),
            fill_count=len(self._fills),
            position_count=len(self._positions),
            issues=issues,
        )


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


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()
