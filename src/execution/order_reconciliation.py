from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from math import isclose

from src.execution.broker_adapter import BrokerFill, BrokerOrder, OrderSide, OrderStatus


QUANTITY_PRECISION = 6
PRICE_PRECISION = 6
CASH_PRECISION = 2
_EPSILON = 10 ** -QUANTITY_PRECISION


class ReconciliationSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


@dataclass(frozen=True)
class ReconciliationIssue:
    severity: ReconciliationSeverity
    code: str
    message: str
    order_id: str | None = None

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["severity"] = self.severity.value
        return payload


@dataclass(frozen=True)
class OrderLifecycleState:
    order_id: str
    symbol: str
    side: OrderSide
    status: OrderStatus
    requested_quantity: float
    filled_quantity: float
    remaining_quantity: float
    average_fill_price: float | None
    fill_count: int
    strategy_id: str
    signal_id: str
    client_order_id: str | None = None
    issues: list[ReconciliationIssue] = field(default_factory=list)

    @property
    def is_consistent(self) -> bool:
        return not any(issue.severity == ReconciliationSeverity.ERROR for issue in self.issues)

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["side"] = self.side.value
        payload["status"] = self.status.value
        payload["issues"] = [issue.to_dict() for issue in self.issues]
        return payload


@dataclass(frozen=True)
class PortfolioPositionState:
    symbol: str
    quantity: float
    average_price: float
    realized_pnl: float = 0.0
    commissions: float = 0.0

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class PortfolioState:
    cash: float
    realized_pnl: float
    total_commissions: float
    positions: list[PortfolioPositionState]

    @property
    def position_count(self) -> int:
        return len([position for position in self.positions if not isclose(position.quantity, 0.0, abs_tol=_EPSILON)])

    def get_position(self, symbol: str) -> PortfolioPositionState | None:
        normalized = symbol.strip().upper()
        for position in self.positions:
            if position.symbol == normalized:
                return position
        return None

    def to_dict(self) -> dict[str, object]:
        return {
            "cash": self.cash,
            "realized_pnl": self.realized_pnl,
            "total_commissions": self.total_commissions,
            "position_count": self.position_count,
            "positions": [position.to_dict() for position in self.positions],
        }


@dataclass(frozen=True)
class OrderReconciliationSnapshot:
    passed: bool
    order_count: int
    fill_count: int
    position_count: int
    orders: list[OrderLifecycleState]
    portfolio: PortfolioState
    issues: list[ReconciliationIssue] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return {
            "passed": self.passed,
            "order_count": self.order_count,
            "fill_count": self.fill_count,
            "position_count": self.position_count,
            "orders": [order.to_dict() for order in self.orders],
            "portfolio": self.portfolio.to_dict(),
            "issues": [issue.to_dict() for issue in self.issues],
            "notes": list(self.notes),
        }


def reconcile_orders_and_fills(
    *,
    orders: list[BrokerOrder],
    fills: list[BrokerFill],
    starting_cash: float = 0.0,
) -> OrderReconciliationSnapshot:
    """Reconcile broker orders and fills into an auditable portfolio state.

    The engine is intentionally pure and paper-safe. It does not submit orders,
    cancel orders, fetch market data or approve live trading. It only validates
    an observed broker/order/fill snapshot and derives deterministic state.
    """

    issue_log: list[ReconciliationIssue] = []
    order_map = _index_orders(orders, issue_log)
    fills_by_order = _group_fills(fills, order_map, issue_log)

    order_states: list[OrderLifecycleState] = []
    portfolio_builder = _PortfolioBuilder(starting_cash=starting_cash)

    for order in orders:
        related_fills = fills_by_order.get(order.order_id, [])
        order_issues = _validate_order_lifecycle(order, related_fills)
        issue_log.extend(order_issues)
        for fill in related_fills:
            if _is_valid_fill(fill, order):
                portfolio_builder.apply_fill(fill)
        order_states.append(_build_order_state(order, related_fills, order_issues))

    portfolio = portfolio_builder.snapshot()
    passed = not any(issue.severity == ReconciliationSeverity.ERROR for issue in issue_log)

    return OrderReconciliationSnapshot(
        passed=passed,
        order_count=len(orders),
        fill_count=len(fills),
        position_count=portfolio.position_count,
        orders=order_states,
        portfolio=portfolio,
        issues=issue_log,
        notes=[
            "paper_execution_reconciliation_only",
            "no_live_order_submission_performed",
            "fail_closed_on_inconsistent_order_fill_state",
        ],
    )


def _index_orders(orders: list[BrokerOrder], issue_log: list[ReconciliationIssue]) -> dict[str, BrokerOrder]:
    indexed: dict[str, BrokerOrder] = {}
    for order in orders:
        if order.order_id in indexed:
            issue_log.append(
                ReconciliationIssue(
                    severity=ReconciliationSeverity.ERROR,
                    code="duplicate_order_id",
                    message=f"duplicate order id observed: {order.order_id}",
                    order_id=order.order_id,
                )
            )
        indexed[order.order_id] = order
    return indexed


def _group_fills(
    fills: list[BrokerFill],
    orders_by_id: dict[str, BrokerOrder],
    issue_log: list[ReconciliationIssue],
) -> dict[str, list[BrokerFill]]:
    grouped: dict[str, list[BrokerFill]] = {}
    for fill in fills:
        fill_issues = _validate_fill_shape(fill)
        issue_log.extend(fill_issues)
        if fill.order_id not in orders_by_id:
            issue_log.append(
                ReconciliationIssue(
                    severity=ReconciliationSeverity.ERROR,
                    code="orphan_fill",
                    message=f"fill references unknown order id: {fill.order_id}",
                    order_id=fill.order_id,
                )
            )
            continue
        grouped.setdefault(fill.order_id, []).append(fill)
    return grouped


def _validate_fill_shape(fill: BrokerFill) -> list[ReconciliationIssue]:
    issues: list[ReconciliationIssue] = []
    if fill.quantity <= 0:
        issues.append(
            ReconciliationIssue(
                severity=ReconciliationSeverity.ERROR,
                code="invalid_fill_quantity",
                message="fill quantity must be positive",
                order_id=fill.order_id,
            )
        )
    if fill.fill_price <= 0:
        issues.append(
            ReconciliationIssue(
                severity=ReconciliationSeverity.ERROR,
                code="invalid_fill_price",
                message="fill price must be positive",
                order_id=fill.order_id,
            )
        )
    if fill.commission < 0:
        issues.append(
            ReconciliationIssue(
                severity=ReconciliationSeverity.ERROR,
                code="invalid_commission",
                message="fill commission must not be negative",
                order_id=fill.order_id,
            )
        )
    return issues


def _validate_order_lifecycle(order: BrokerOrder, fills: list[BrokerFill]) -> list[ReconciliationIssue]:
    issues: list[ReconciliationIssue] = []
    valid_fills = [fill for fill in fills if _is_valid_fill(fill, order)]
    filled_quantity = _sum_quantity(valid_fills)

    for fill in fills:
        if fill.symbol.strip().upper() != order.symbol.strip().upper():
            issues.append(
                ReconciliationIssue(
                    severity=ReconciliationSeverity.ERROR,
                    code="fill_symbol_mismatch",
                    message=f"fill symbol {fill.symbol} does not match order symbol {order.symbol}",
                    order_id=order.order_id,
                )
            )
        if fill.side != order.side:
            issues.append(
                ReconciliationIssue(
                    severity=ReconciliationSeverity.ERROR,
                    code="fill_side_mismatch",
                    message=f"fill side {fill.side.value} does not match order side {order.side.value}",
                    order_id=order.order_id,
                )
            )

    if filled_quantity - order.quantity > _EPSILON:
        issues.append(
            ReconciliationIssue(
                severity=ReconciliationSeverity.ERROR,
                code="overfilled_order",
                message=f"filled quantity {filled_quantity} exceeds requested quantity {order.quantity}",
                order_id=order.order_id,
            )
        )

    if order.status == OrderStatus.FILLED and not isclose(filled_quantity, order.quantity, abs_tol=_EPSILON):
        issues.append(
            ReconciliationIssue(
                severity=ReconciliationSeverity.ERROR,
                code="filled_status_quantity_mismatch",
                message="FILLED order status requires filled quantity to equal requested quantity",
                order_id=order.order_id,
            )
        )

    if order.status == OrderStatus.PARTIALLY_FILLED and not (0 < filled_quantity < order.quantity):
        issues.append(
            ReconciliationIssue(
                severity=ReconciliationSeverity.ERROR,
                code="partial_status_quantity_mismatch",
                message="PARTIALLY_FILLED order status requires 0 < filled quantity < requested quantity",
                order_id=order.order_id,
            )
        )

    if order.status in {OrderStatus.REJECTED, OrderStatus.CANCELLED} and filled_quantity > _EPSILON:
        issues.append(
            ReconciliationIssue(
                severity=ReconciliationSeverity.ERROR,
                code="terminal_order_has_fills",
                message=f"{order.status.value} order must not have fills",
                order_id=order.order_id,
            )
        )

    if order.status in {OrderStatus.NEW, OrderStatus.ACCEPTED} and filled_quantity > _EPSILON:
        issues.append(
            ReconciliationIssue(
                severity=ReconciliationSeverity.WARNING,
                code="open_order_has_fills",
                message=f"{order.status.value} order has fills but status was not updated to partial or filled",
                order_id=order.order_id,
            )
        )

    return issues


def _build_order_state(
    order: BrokerOrder,
    fills: list[BrokerFill],
    issues: list[ReconciliationIssue],
) -> OrderLifecycleState:
    valid_fills = [fill for fill in fills if _is_valid_fill(fill, order)]
    filled_quantity = _sum_quantity(valid_fills)
    average_fill_price = _average_fill_price(valid_fills)
    remaining_quantity = max(round(order.quantity - filled_quantity, QUANTITY_PRECISION), 0.0)
    return OrderLifecycleState(
        order_id=order.order_id,
        symbol=order.symbol.strip().upper(),
        side=order.side,
        status=order.status,
        requested_quantity=round(order.quantity, QUANTITY_PRECISION),
        filled_quantity=filled_quantity,
        remaining_quantity=remaining_quantity,
        average_fill_price=average_fill_price,
        fill_count=len(valid_fills),
        strategy_id=order.strategy_id,
        signal_id=order.signal_id,
        client_order_id=order.client_order_id,
        issues=issues,
    )


def _is_valid_fill(fill: BrokerFill, order: BrokerOrder) -> bool:
    return (
        fill.quantity > 0
        and fill.fill_price > 0
        and fill.commission >= 0
        and fill.symbol.strip().upper() == order.symbol.strip().upper()
        and fill.side == order.side
    )


def _sum_quantity(fills: list[BrokerFill]) -> float:
    return round(sum(fill.quantity for fill in fills), QUANTITY_PRECISION)


def _average_fill_price(fills: list[BrokerFill]) -> float | None:
    if not fills:
        return None
    quantity = sum(fill.quantity for fill in fills)
    if quantity <= 0:
        return None
    return round(sum(fill.quantity * fill.fill_price for fill in fills) / quantity, PRICE_PRECISION)


@dataclass
class _MutablePosition:
    symbol: str
    quantity: float = 0.0
    average_price: float = 0.0
    realized_pnl: float = 0.0
    commissions: float = 0.0


class _PortfolioBuilder:
    def __init__(self, *, starting_cash: float) -> None:
        self._cash = starting_cash
        self._positions: dict[str, _MutablePosition] = {}
        self._total_commissions = 0.0

    def apply_fill(self, fill: BrokerFill) -> None:
        symbol = fill.symbol.strip().upper()
        position = self._positions.setdefault(symbol, _MutablePosition(symbol=symbol))
        signed_quantity = fill.quantity if fill.side == OrderSide.BUY else -fill.quantity
        gross = fill.quantity * fill.fill_price
        self._cash += -gross - fill.commission if fill.side == OrderSide.BUY else gross - fill.commission
        self._total_commissions += fill.commission
        position.commissions += fill.commission
        position.realized_pnl -= fill.commission

        if isclose(position.quantity, 0.0, abs_tol=_EPSILON) or _same_direction(position.quantity, signed_quantity):
            self._increase_position(position, signed_quantity, fill.fill_price)
            return

        self._reduce_or_flip_position(position, signed_quantity, fill.fill_price)

    def snapshot(self) -> PortfolioState:
        positions = [
            PortfolioPositionState(
                symbol=position.symbol,
                quantity=round(position.quantity, QUANTITY_PRECISION),
                average_price=round(position.average_price, PRICE_PRECISION),
                realized_pnl=round(position.realized_pnl, CASH_PRECISION),
                commissions=round(position.commissions, CASH_PRECISION),
            )
            for position in sorted(self._positions.values(), key=lambda item: item.symbol)
        ]
        return PortfolioState(
            cash=round(self._cash, CASH_PRECISION),
            realized_pnl=round(sum(position.realized_pnl for position in self._positions.values()), CASH_PRECISION),
            total_commissions=round(self._total_commissions, CASH_PRECISION),
            positions=positions,
        )

    @staticmethod
    def _increase_position(position: _MutablePosition, signed_quantity: float, price: float) -> None:
        new_quantity = position.quantity + signed_quantity
        if isclose(new_quantity, 0.0, abs_tol=_EPSILON):
            position.quantity = 0.0
            position.average_price = 0.0
            return
        position.average_price = (
            abs(position.quantity) * position.average_price + abs(signed_quantity) * price
        ) / abs(new_quantity)
        position.quantity = new_quantity

    @staticmethod
    def _reduce_or_flip_position(position: _MutablePosition, signed_quantity: float, price: float) -> None:
        closing_quantity = min(abs(position.quantity), abs(signed_quantity))
        if position.quantity > 0:
            position.realized_pnl += (price - position.average_price) * closing_quantity
        else:
            position.realized_pnl += (position.average_price - price) * closing_quantity

        new_quantity = position.quantity + signed_quantity
        if isclose(new_quantity, 0.0, abs_tol=_EPSILON):
            position.quantity = 0.0
            position.average_price = 0.0
            return

        flipped = (position.quantity > 0 > new_quantity) or (position.quantity < 0 < new_quantity)
        position.quantity = new_quantity
        if flipped:
            position.average_price = price


def _same_direction(left: float, right: float) -> bool:
    return (left >= 0 and right >= 0) or (left <= 0 and right <= 0)
