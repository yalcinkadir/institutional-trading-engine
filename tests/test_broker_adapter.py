import pytest

from src.execution.broker_adapter import (
    BrokerMode,
    BrokerOrderRequest,
    MockPaperBrokerAdapter,
    OrderSide,
    OrderStatus,
    OrderType,
)


def test_mock_paper_adapter_accepts_valid_market_order():
    adapter = MockPaperBrokerAdapter()
    order = adapter.submit_order(
        BrokerOrderRequest(
            symbol="aapl",
            side=OrderSide.BUY,
            quantity=10,
            order_type=OrderType.MARKET,
            strategy_id="rule_based_core_v1",
            signal_id="sig-001",
        )
    )

    assert adapter.mode == BrokerMode.PAPER
    assert order.status == OrderStatus.ACCEPTED
    assert order.symbol == "AAPL"
    assert adapter.get_order_status(order.order_id) == order


def test_mock_paper_adapter_rejects_invalid_order_fail_closed():
    adapter = MockPaperBrokerAdapter()
    order = adapter.submit_order(
        BrokerOrderRequest(
            symbol="",
            side=OrderSide.BUY,
            quantity=0,
            order_type=OrderType.MARKET,
            strategy_id="",
            signal_id="",
        )
    )

    assert order.status == OrderStatus.REJECTED
    assert "symbol is required" in (order.reason or "")
    assert "quantity must be positive" in (order.reason or "")


def test_limit_and_stop_orders_require_prices():
    adapter = MockPaperBrokerAdapter()
    limit_order = adapter.submit_order(
        BrokerOrderRequest(
            symbol="MSFT",
            side=OrderSide.BUY,
            quantity=1,
            order_type=OrderType.LIMIT,
            strategy_id="strategy",
            signal_id="signal",
        )
    )
    stop_order = adapter.submit_order(
        BrokerOrderRequest(
            symbol="MSFT",
            side=OrderSide.SELL,
            quantity=1,
            order_type=OrderType.STOP,
            strategy_id="strategy",
            signal_id="signal",
        )
    )

    assert limit_order.status == OrderStatus.REJECTED
    assert "limit_price is required" in (limit_order.reason or "")
    assert stop_order.status == OrderStatus.REJECTED
    assert "stop_price is required" in (stop_order.reason or "")


def test_cancel_order_updates_status():
    adapter = MockPaperBrokerAdapter()
    order = adapter.submit_order(
        BrokerOrderRequest(
            symbol="NVDA",
            side=OrderSide.BUY,
            quantity=2,
            order_type=OrderType.MARKET,
            strategy_id="strategy",
            signal_id="signal",
        )
    )

    cancelled = adapter.cancel_order(order.order_id)

    assert cancelled.status == OrderStatus.CANCELLED
    assert adapter.get_order_status(order.order_id).status == OrderStatus.CANCELLED


def test_unknown_order_status_raises_key_error():
    adapter = MockPaperBrokerAdapter()

    with pytest.raises(KeyError):
        adapter.get_order_status("unknown")


def test_account_snapshot_and_reconciliation_are_paper_only():
    adapter = MockPaperBrokerAdapter(cash=50_000)
    snapshot = adapter.get_account_snapshot()
    report = adapter.reconcile_orders()

    assert snapshot.mode == BrokerMode.PAPER
    assert snapshot.cash == 50_000
    assert report.mode == BrokerMode.PAPER
    assert report.passed is True
