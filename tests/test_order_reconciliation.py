from src.execution.broker_adapter import BrokerFill, BrokerOrder, OrderSide, OrderStatus, OrderType
from src.execution.order_reconciliation import reconcile_orders_and_fills


def _order(
    *,
    order_id: str = "ord-1",
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
        submitted_at="2026-05-27T10:00:00+00:00",
        client_order_id=f"client-{order_id}",
    )


def _fill(
    *,
    fill_id: str = "fill-1",
    order_id: str = "ord-1",
    symbol: str = "AAPL",
    side: OrderSide = OrderSide.BUY,
    quantity: float = 10,
    fill_price: float = 100,
    commission: float = 1.0,
) -> BrokerFill:
    return BrokerFill(
        fill_id=fill_id,
        order_id=order_id,
        symbol=symbol,
        side=side,
        quantity=quantity,
        fill_price=fill_price,
        filled_at="2026-05-27T10:01:00+00:00",
        commission=commission,
    )


def test_reconciles_filled_buy_order_into_portfolio_state():
    snapshot = reconcile_orders_and_fills(
        orders=[_order(quantity=10, status=OrderStatus.FILLED)],
        fills=[_fill(quantity=4, fill_price=100), _fill(fill_id="fill-2", quantity=6, fill_price=110)],
        starting_cash=10_000,
    )

    assert snapshot.passed is True
    assert snapshot.order_count == 1
    assert snapshot.fill_count == 2
    assert snapshot.position_count == 1
    order_state = snapshot.orders[0]
    assert order_state.filled_quantity == 10
    assert order_state.remaining_quantity == 0
    assert order_state.average_fill_price == 106

    position = snapshot.portfolio.get_position("AAPL")
    assert position is not None
    assert position.quantity == 10
    assert position.average_price == 106
    assert snapshot.portfolio.cash == 8938
    assert snapshot.portfolio.total_commissions == 2


def test_partial_fill_state_tracks_remaining_quantity():
    snapshot = reconcile_orders_and_fills(
        orders=[_order(quantity=10, status=OrderStatus.PARTIALLY_FILLED)],
        fills=[_fill(quantity=3, fill_price=50, commission=0.5)],
        starting_cash=1_000,
    )

    assert snapshot.passed is True
    order_state = snapshot.orders[0]
    assert order_state.filled_quantity == 3
    assert order_state.remaining_quantity == 7
    assert order_state.fill_count == 1
    assert snapshot.portfolio.get_position("AAPL").quantity == 3
    assert snapshot.portfolio.cash == 849.5


def test_overfilled_order_fails_closed():
    snapshot = reconcile_orders_and_fills(
        orders=[_order(quantity=10, status=OrderStatus.FILLED)],
        fills=[_fill(quantity=12, fill_price=100)],
    )

    assert snapshot.passed is False
    assert any(issue.code == "overfilled_order" for issue in snapshot.issues)


def test_orphan_fill_fails_closed_and_does_not_create_position():
    snapshot = reconcile_orders_and_fills(
        orders=[],
        fills=[_fill(order_id="missing-order", quantity=1, fill_price=100)],
        starting_cash=1_000,
    )

    assert snapshot.passed is False
    assert any(issue.code == "orphan_fill" for issue in snapshot.issues)
    assert snapshot.portfolio.position_count == 0
    assert snapshot.portfolio.cash == 1_000


def test_rejected_order_with_fill_fails_closed():
    snapshot = reconcile_orders_and_fills(
        orders=[_order(quantity=5, status=OrderStatus.REJECTED)],
        fills=[_fill(quantity=5, fill_price=100)],
    )

    assert snapshot.passed is False
    assert any(issue.code == "terminal_order_has_fills" for issue in snapshot.issues)


def test_fill_symbol_and_side_mismatch_fail_closed():
    snapshot = reconcile_orders_and_fills(
        orders=[_order(symbol="AAPL", side=OrderSide.BUY, quantity=5, status=OrderStatus.FILLED)],
        fills=[_fill(symbol="MSFT", side=OrderSide.SELL, quantity=5, fill_price=100)],
    )

    assert snapshot.passed is False
    assert any(issue.code == "fill_symbol_mismatch" for issue in snapshot.issues)
    assert any(issue.code == "fill_side_mismatch" for issue in snapshot.issues)
    assert snapshot.portfolio.position_count == 0


def test_buy_then_sell_updates_realized_pnl_and_cash():
    buy_order = _order(order_id="buy-1", side=OrderSide.BUY, quantity=10, status=OrderStatus.FILLED)
    sell_order = _order(order_id="sell-1", side=OrderSide.SELL, quantity=4, status=OrderStatus.FILLED)
    snapshot = reconcile_orders_and_fills(
        orders=[buy_order, sell_order],
        fills=[
            _fill(fill_id="buy-fill", order_id="buy-1", side=OrderSide.BUY, quantity=10, fill_price=100, commission=1),
            _fill(fill_id="sell-fill", order_id="sell-1", side=OrderSide.SELL, quantity=4, fill_price=120, commission=1),
        ],
        starting_cash=2_000,
    )

    assert snapshot.passed is True
    position = snapshot.portfolio.get_position("AAPL")
    assert position is not None
    assert position.quantity == 6
    assert position.average_price == 100
    assert position.realized_pnl == 78
    assert snapshot.portfolio.realized_pnl == 78
    assert snapshot.portfolio.cash == 1478


def test_duplicate_order_id_fails_closed():
    snapshot = reconcile_orders_and_fills(
        orders=[_order(order_id="dup"), _order(order_id="dup")],
        fills=[],
    )

    assert snapshot.passed is False
    assert any(issue.code == "duplicate_order_id" for issue in snapshot.issues)
