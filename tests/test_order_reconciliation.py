from src.execution.broker_adapter import BrokerFill, BrokerOrder, OrderSide, OrderStatus, OrderType
from src.execution.reconciliation import (
    ReconciliationSeverity,
    ReconciliationStatus,
    reconcile_orders,
)


def _order(
    *,
    order_id: str,
    symbol: str = "AAPL",
    side: OrderSide = OrderSide.BUY,
    quantity: float = 10,
    status: OrderStatus = OrderStatus.ACCEPTED,
) -> BrokerOrder:
    return BrokerOrder(
        order_id=order_id,
        symbol=symbol,
        side=side,
        quantity=quantity,
        order_type=OrderType.MARKET,
        status=status,
        strategy_id="strategy-1",
        signal_id="signal-1",
        submitted_at="2026-05-28T09:30:00+00:00",
    )


def _fill(
    *,
    fill_id: str,
    order_id: str,
    symbol: str = "AAPL",
    side: OrderSide = OrderSide.BUY,
    quantity: float = 10,
    fill_price: float = 100,
) -> BrokerFill:
    return BrokerFill(
        fill_id=fill_id,
        order_id=order_id,
        symbol=symbol,
        side=side,
        quantity=quantity,
        fill_price=fill_price,
        filled_at="2026-05-28T09:31:00+00:00",
    )


def test_reconcile_filled_order_and_position_snapshot():
    order = _order(order_id="order-1", quantity=10)
    fills = [
        _fill(fill_id="fill-1", order_id="order-1", quantity=4, fill_price=100),
        _fill(fill_id="fill-2", order_id="order-1", quantity=6, fill_price=110),
    ]

    report = reconcile_orders([order], fills)

    reconciled_order = report.order_by_id("order-1")
    assert reconciled_order.status == ReconciliationStatus.FILLED
    assert reconciled_order.filled_quantity == 10
    assert reconciled_order.remaining_quantity == 0
    assert reconciled_order.average_fill_price == 106
    assert reconciled_order.fill_ids == ("fill-1", "fill-2")

    position = report.position_by_symbol("AAPL")
    assert position.net_quantity == 10
    assert position.average_price == 106
    assert not report.has_critical_issues


def test_reconcile_partially_filled_order():
    order = _order(order_id="order-1", quantity=10)
    fill = _fill(fill_id="fill-1", order_id="order-1", quantity=4, fill_price=100)

    report = reconcile_orders([order], [fill])

    reconciled_order = report.order_by_id("order-1")
    assert reconciled_order.status == ReconciliationStatus.PARTIALLY_FILLED
    assert reconciled_order.filled_quantity == 4
    assert reconciled_order.remaining_quantity == 6
    assert reconciled_order.average_fill_price == 100
    assert report.position_by_symbol("AAPL").net_quantity == 4


def test_reconcile_sell_fill_reduces_net_position():
    buy_order = _order(order_id="buy-1", quantity=10, side=OrderSide.BUY)
    sell_order = _order(order_id="sell-1", quantity=3, side=OrderSide.SELL)
    fills = [
        _fill(fill_id="fill-1", order_id="buy-1", quantity=10, fill_price=100, side=OrderSide.BUY),
        _fill(fill_id="fill-2", order_id="sell-1", quantity=3, fill_price=120, side=OrderSide.SELL),
    ]

    report = reconcile_orders([buy_order, sell_order], fills)

    position = report.position_by_symbol("AAPL")
    assert position.net_quantity == 7
    assert position.average_price == 91.428571


def test_reconcile_detects_overfilled_order_as_critical():
    order = _order(order_id="order-1", quantity=5)
    fill = _fill(fill_id="fill-1", order_id="order-1", quantity=6, fill_price=100)

    report = reconcile_orders([order], [fill])

    reconciled_order = report.order_by_id("order-1")
    assert reconciled_order.status == ReconciliationStatus.OVERFILLED
    assert report.has_critical_issues
    assert report.issues[0].severity == ReconciliationSeverity.CRITICAL
    assert report.issues[0].code == "order_overfilled"


def test_reconcile_detects_orphan_fill_as_critical():
    fill = _fill(fill_id="fill-1", order_id="missing-order", quantity=1, fill_price=100)

    report = reconcile_orders([], [fill])

    assert report.orders == []
    assert report.positions == []
    assert report.has_critical_issues
    assert report.issues[0].code == "orphan_fill"


def test_reconcile_cancelled_without_fills_is_informational():
    order = _order(order_id="order-1", status=OrderStatus.CANCELLED)

    report = reconcile_orders([order], [])

    reconciled_order = report.order_by_id("order-1")
    assert reconciled_order.status == ReconciliationStatus.CANCELLED
    assert not report.has_critical_issues
    assert report.issues[0].severity == ReconciliationSeverity.INFO
    assert report.issues[0].code == "cancelled_without_fills"


def test_reconcile_rejected_order_with_fill_is_critical():
    order = _order(order_id="order-1", status=OrderStatus.REJECTED)
    fill = _fill(fill_id="fill-1", order_id="order-1", quantity=1, fill_price=100)

    report = reconcile_orders([order], [fill])

    assert report.order_by_id("order-1").status == ReconciliationStatus.REJECTED
    assert report.has_critical_issues
    assert report.issues[0].code == "rejected_order_has_fills"
