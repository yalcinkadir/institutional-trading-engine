from src.execution.broker_adapter import BrokerFill, BrokerOrder, OrderSide, OrderStatus, OrderType
from src.execution.order_reconciliation import (
    ReconciliationSeverity,
    reconcile_orders_and_fills,
)


def _order(
    *,
    order_id: str,
    symbol: str = "AAPL",
    side: OrderSide = OrderSide.BUY,
    quantity: float = 10,
    status: OrderStatus = OrderStatus.FILLED,
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
    commission: float = 0.0,
) -> BrokerFill:
    return BrokerFill(
        fill_id=fill_id,
        order_id=order_id,
        symbol=symbol,
        side=side,
        quantity=quantity,
        fill_price=fill_price,
        filled_at="2026-05-28T09:31:00+00:00",
        commission=commission,
    )


def test_reconcile_filled_order_and_portfolio_snapshot():
    order = _order(order_id="order-1", quantity=10, status=OrderStatus.FILLED)
    fills = [
        _fill(fill_id="fill-1", order_id="order-1", quantity=4, fill_price=100, commission=1),
        _fill(fill_id="fill-2", order_id="order-1", quantity=6, fill_price=110, commission=1),
    ]

    snapshot = reconcile_orders_and_fills(orders=[order], fills=fills, starting_cash=10_000)

    assert snapshot.passed
    assert snapshot.order_count == 1
    assert snapshot.fill_count == 2
    assert snapshot.position_count == 1
    assert snapshot.orders[0].filled_quantity == 10
    assert snapshot.orders[0].remaining_quantity == 0
    assert snapshot.orders[0].average_fill_price == 106
    assert snapshot.portfolio.cash == 8938
    assert snapshot.portfolio.total_commissions == 2

    position = snapshot.portfolio.get_position("AAPL")
    assert position is not None
    assert position.quantity == 10
    assert position.average_price == 106
    assert position.commissions == 2


def test_reconcile_partially_filled_order_is_consistent():
    order = _order(order_id="order-1", quantity=10, status=OrderStatus.PARTIALLY_FILLED)
    fill = _fill(fill_id="fill-1", order_id="order-1", quantity=4, fill_price=100)

    snapshot = reconcile_orders_and_fills(orders=[order], fills=[fill], starting_cash=5_000)

    assert snapshot.passed
    assert snapshot.orders[0].filled_quantity == 4
    assert snapshot.orders[0].remaining_quantity == 6
    assert snapshot.orders[0].average_fill_price == 100
    assert snapshot.portfolio.get_position("AAPL") is not None
    assert snapshot.portfolio.get_position("AAPL").quantity == 4


def test_reconcile_sell_fill_reduces_position_and_realizes_pnl():
    buy_order = _order(order_id="buy-1", quantity=10, side=OrderSide.BUY, status=OrderStatus.FILLED)
    sell_order = _order(order_id="sell-1", quantity=3, side=OrderSide.SELL, status=OrderStatus.FILLED)
    fills = [
        _fill(fill_id="fill-1", order_id="buy-1", quantity=10, fill_price=100, side=OrderSide.BUY),
        _fill(fill_id="fill-2", order_id="sell-1", quantity=3, fill_price=120, side=OrderSide.SELL),
    ]

    snapshot = reconcile_orders_and_fills(orders=[buy_order, sell_order], fills=fills, starting_cash=10_000)

    position = snapshot.portfolio.get_position("AAPL")
    assert position is not None
    assert position.quantity == 7
    assert position.average_price == 100
    assert position.realized_pnl == 60
    assert snapshot.portfolio.realized_pnl == 60
    assert snapshot.portfolio.cash == 9360


def test_reconcile_detects_overfilled_order_as_error():
    order = _order(order_id="order-1", quantity=5, status=OrderStatus.FILLED)
    fill = _fill(fill_id="fill-1", order_id="order-1", quantity=6, fill_price=100)

    snapshot = reconcile_orders_and_fills(orders=[order], fills=[fill])

    assert not snapshot.passed
    assert snapshot.issues[0].severity == ReconciliationSeverity.ERROR
    assert snapshot.issues[0].code == "overfilled_order"
    assert snapshot.orders[0].issues[0].code == "overfilled_order"


def test_reconcile_detects_orphan_fill_as_error():
    fill = _fill(fill_id="fill-1", order_id="missing-order", quantity=1, fill_price=100)

    snapshot = reconcile_orders_and_fills(orders=[], fills=[fill])

    assert not snapshot.passed
    assert snapshot.order_count == 0
    assert snapshot.position_count == 0
    assert snapshot.issues[0].code == "orphan_fill"


def test_reconcile_terminal_order_with_fill_is_error():
    order = _order(order_id="order-1", status=OrderStatus.REJECTED)
    fill = _fill(fill_id="fill-1", order_id="order-1", quantity=1, fill_price=100)

    snapshot = reconcile_orders_and_fills(orders=[order], fills=[fill])

    assert not snapshot.passed
    assert snapshot.issues[0].code == "terminal_order_has_fills"


def test_reconcile_open_order_with_fill_is_warning_but_not_failed():
    order = _order(order_id="order-1", status=OrderStatus.ACCEPTED)
    fill = _fill(fill_id="fill-1", order_id="order-1", quantity=1, fill_price=100)

    snapshot = reconcile_orders_and_fills(orders=[order], fills=[fill])

    assert snapshot.passed
    assert snapshot.issues[0].severity == ReconciliationSeverity.WARNING
    assert snapshot.issues[0].code == "open_order_has_fills"


def test_reconcile_duplicate_order_id_fails_closed():
    first = _order(order_id="order-1", quantity=1)
    second = _order(order_id="order-1", quantity=1)

    snapshot = reconcile_orders_and_fills(orders=[first, second], fills=[])

    assert not snapshot.passed
    assert snapshot.issues[0].severity == ReconciliationSeverity.ERROR
    assert snapshot.issues[0].code == "duplicate_order_id"


def test_reconcile_fill_symbol_mismatch_fails_closed():
    order = _order(order_id="order-1", symbol="AAPL", quantity=1)
    fill = _fill(fill_id="fill-1", order_id="order-1", symbol="MSFT", quantity=1)

    snapshot = reconcile_orders_and_fills(orders=[order], fills=[fill])

    assert not snapshot.passed
    assert snapshot.issues[0].code == "fill_symbol_mismatch"
    assert snapshot.position_count == 0


def test_reconcile_fill_side_mismatch_fails_closed():
    order = _order(order_id="order-1", side=OrderSide.BUY, quantity=1)
    fill = _fill(fill_id="fill-1", order_id="order-1", side=OrderSide.SELL, quantity=1)

    snapshot = reconcile_orders_and_fills(orders=[order], fills=[fill])

    assert not snapshot.passed
    assert snapshot.issues[0].code == "fill_side_mismatch"
    assert snapshot.position_count == 0
