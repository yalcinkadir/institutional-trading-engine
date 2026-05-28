from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable

from src.execution.broker_adapter import BrokerFill, BrokerOrder, OrderSide, OrderStatus


class ReconciliationStatus(str, Enum):
    OPEN = "open"
    PARTIALLY_FILLED = "partially_filled"
    FILLED = "filled"
    CANCELLED = "cancelled"
    REJECTED = "rejected"
    OVERFILLED = "overfilled"


class ReconciliationSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


@dataclass(frozen=True)
class ReconciliationIssue:
    severity: ReconciliationSeverity
    code: str
    message: str
    order_id: str | None = None
    symbol: str | None = None


@dataclass(frozen=True)
class ReconciledOrder:
    order_id: str
    symbol: str
    side: OrderSide
    requested_quantity: float
    filled_quantity: float
    remaining_quantity: float
    average_fill_price: float | None
    status: ReconciliationStatus
    source_status: OrderStatus
    signal_id: str
    strategy_id: str
    fill_ids: tuple[str, ...] = ()


@dataclass(frozen=True)
class ReconciledPosition:
    symbol: str
    net_quantity: float
    average_price: float | None


@dataclass(frozen=True)
class ReconciliationReport:
    orders: list[ReconciledOrder]
    positions: list[ReconciledPosition]
    issues: list[ReconciliationIssue] = field(default_factory=list)

    @property
    def has_critical_issues(self) -> bool:
        return any(issue.severity == ReconciliationSeverity.CRITICAL for issue in self.issues)

    def order_by_id(self, order_id: str) -> ReconciledOrder:
        for order in self.orders:
            if order.order_id == order_id:
                return order
        raise KeyError(order_id)

    def position_by_symbol(self, symbol: str) -> ReconciledPosition:
        normalized_symbol = symbol.strip().upper()
        for position in self.positions:
            if position.symbol == normalized_symbol:
                return position
        raise KeyError(normalized_symbol)


def reconcile_orders(
    orders: Iterable[BrokerOrder],
    fills: Iterable[BrokerFill],
) -> ReconciliationReport:
    """Reconcile paper orders and fills into an auditable snapshot.

    C4 is intentionally side-effect free. It does not contact a broker, does not
    mutate adapter state and does not enable live execution. It only derives a
    deterministic order/fill/position view from already captured paper objects.
    """

    order_list = list(orders)
    fill_list = list(fills)
    fills_by_order_id = _group_fills_by_order_id(fill_list)
    known_order_ids = {order.order_id for order in order_list}

    reconciled_orders: list[ReconciledOrder] = []
    issues: list[ReconciliationIssue] = []

    for order in sorted(order_list, key=lambda item: item.order_id):
        order_fills = fills_by_order_id.get(order.order_id, [])
        filled_quantity = round(sum(fill.quantity for fill in order_fills), 6)
        remaining_quantity = round(order.quantity - filled_quantity, 6)
        average_price = _weighted_average_price(order_fills)
        reconciliation_status = _derive_reconciliation_status(order, filled_quantity)

        if reconciliation_status == ReconciliationStatus.OVERFILLED:
            issues.append(
                ReconciliationIssue(
                    severity=ReconciliationSeverity.CRITICAL,
                    code="order_overfilled",
                    message="Filled quantity exceeds requested order quantity.",
                    order_id=order.order_id,
                    symbol=order.symbol,
                )
            )
        elif filled_quantity > 0 and order.status == OrderStatus.REJECTED:
            issues.append(
                ReconciliationIssue(
                    severity=ReconciliationSeverity.CRITICAL,
                    code="rejected_order_has_fills",
                    message="Rejected order has one or more fills.",
                    order_id=order.order_id,
                    symbol=order.symbol,
                )
            )
        elif order.status == OrderStatus.CANCELLED and filled_quantity == 0:
            issues.append(
                ReconciliationIssue(
                    severity=ReconciliationSeverity.INFO,
                    code="cancelled_without_fills",
                    message="Cancelled order has no fills.",
                    order_id=order.order_id,
                    symbol=order.symbol,
                )
            )

        reconciled_orders.append(
            ReconciledOrder(
                order_id=order.order_id,
                symbol=order.symbol.strip().upper(),
                side=order.side,
                requested_quantity=round(order.quantity, 6),
                filled_quantity=filled_quantity,
                remaining_quantity=remaining_quantity,
                average_fill_price=average_price,
                status=reconciliation_status,
                source_status=order.status,
                signal_id=order.signal_id,
                strategy_id=order.strategy_id,
                fill_ids=tuple(fill.fill_id for fill in order_fills),
            )
        )

    for fill in fill_list:
        if fill.order_id not in known_order_ids:
            issues.append(
                ReconciliationIssue(
                    severity=ReconciliationSeverity.CRITICAL,
                    code="orphan_fill",
                    message="Fill references an unknown order id.",
                    order_id=fill.order_id,
                    symbol=fill.symbol,
                )
            )

    return ReconciliationReport(
        orders=reconciled_orders,
        positions=_build_positions(reconciled_orders),
        issues=issues,
    )


def _group_fills_by_order_id(fills: list[BrokerFill]) -> dict[str, list[BrokerFill]]:
    grouped: dict[str, list[BrokerFill]] = {}
    for fill in sorted(fills, key=lambda item: item.fill_id):
        grouped.setdefault(fill.order_id, []).append(fill)
    return grouped


def _weighted_average_price(fills: list[BrokerFill]) -> float | None:
    total_quantity = sum(fill.quantity for fill in fills)
    if total_quantity <= 0:
        return None
    total_notional = sum(fill.quantity * fill.fill_price for fill in fills)
    return round(total_notional / total_quantity, 6)


def _derive_reconciliation_status(
    order: BrokerOrder,
    filled_quantity: float,
) -> ReconciliationStatus:
    if filled_quantity > order.quantity:
        return ReconciliationStatus.OVERFILLED
    if order.status == OrderStatus.REJECTED:
        return ReconciliationStatus.REJECTED
    if order.status == OrderStatus.CANCELLED:
        return ReconciliationStatus.CANCELLED
    if filled_quantity == order.quantity:
        return ReconciliationStatus.FILLED
    if filled_quantity > 0:
        return ReconciliationStatus.PARTIALLY_FILLED
    return ReconciliationStatus.OPEN


def _build_positions(orders: list[ReconciledOrder]) -> list[ReconciledPosition]:
    positions: dict[str, dict[str, float]] = {}
    for order in orders:
        if order.filled_quantity <= 0 or order.average_fill_price is None:
            continue

        state = positions.setdefault(order.symbol, {"quantity": 0.0, "notional": 0.0})
        signed_quantity = order.filled_quantity
        if order.side == OrderSide.SELL:
            signed_quantity = -signed_quantity

        state["quantity"] = round(state["quantity"] + signed_quantity, 6)
        state["notional"] = round(
            state["notional"] + signed_quantity * order.average_fill_price,
            6,
        )

    reconciled_positions: list[ReconciledPosition] = []
    for symbol, state in sorted(positions.items()):
        net_quantity = round(state["quantity"], 6)
        average_price = None
        if net_quantity != 0:
            average_price = round(abs(state["notional"] / net_quantity), 6)
        reconciled_positions.append(
            ReconciledPosition(
                symbol=symbol,
                net_quantity=net_quantity,
                average_price=average_price,
            )
        )
    return reconciled_positions
