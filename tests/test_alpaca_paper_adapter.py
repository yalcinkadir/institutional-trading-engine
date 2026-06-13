import pytest

from src.execution.alpaca_paper_adapter import (
    ALPACA_PAPER_ENDPOINT,
    AlpacaPaperAdapter,
    AlpacaPaperAdapterConfig,
    InMemoryAlpacaPaperTransport,
)
from src.execution.broker_adapter import (
    BrokerMode,
    BrokerOrderRequest,
    ExecutionAuthorization,
    OrderSide,
    OrderStatus,
    OrderType,
)


def _authorization() -> ExecutionAuthorization:
    return ExecutionAuthorization.paper_observation()


def _valid_request() -> BrokerOrderRequest:
    return BrokerOrderRequest(
        symbol="aapl",
        side=OrderSide.BUY,
        quantity=3,
        order_type=OrderType.MARKET,
        strategy_id="rule_based_core_v1",
        signal_id="sig-001",
    )


def _adapter(*, transport: InMemoryAlpacaPaperTransport | None = None) -> AlpacaPaperAdapter:
    return AlpacaPaperAdapter(
        AlpacaPaperAdapterConfig(),
        transport=transport or InMemoryAlpacaPaperTransport(cash=75_000),
    )


def test_alpaca_paper_adapter_blocks_missing_execution_authorization_fail_closed():
    adapter = _adapter()

    order = adapter.submit_order(_valid_request())

    assert order.status == OrderStatus.REJECTED
    assert "execution authorization is required" in (order.reason or "")


def test_alpaca_paper_adapter_blocks_live_authorization_flag_fail_closed():
    adapter = _adapter()
    authorization = ExecutionAuthorization(
        authorization_id="live-not-allowed",
        broker_execution_mode="paper_only",
        live_trading_authorized=True,
        paper_trading_authorized=True,
        approved_by="unit-test",
        reason="negative test",
    )

    order = adapter.submit_order(_valid_request(), authorization=authorization)

    assert order.status == OrderStatus.REJECTED
    assert "live_trading_authorized must be false" in (order.reason or "")


def test_alpaca_paper_adapter_blocks_non_paper_execution_mode_fail_closed():
    adapter = _adapter()
    authorization = ExecutionAuthorization(
        authorization_id="live-mode-not-allowed",
        broker_execution_mode="live",
        live_trading_authorized=False,
        paper_trading_authorized=True,
        approved_by="unit-test",
        reason="negative test",
    )

    order = adapter.submit_order(_valid_request(), authorization=authorization)

    assert order.status == OrderStatus.REJECTED
    assert "broker_execution_mode must be paper_only" in (order.reason or "")


def test_alpaca_paper_adapter_accepts_market_order_with_authorization():
    transport = InMemoryAlpacaPaperTransport(cash=75_000)
    adapter = _adapter(transport=transport)

    order = adapter.submit_order(_valid_request(), authorization=_authorization())

    assert adapter.mode == BrokerMode.PAPER
    assert order.status == OrderStatus.ACCEPTED
    assert order.symbol == "AAPL"
    assert order.quantity == 3
    assert adapter.get_order_status(order.order_id).status == OrderStatus.ACCEPTED
    raw_order = transport.get_order(order.order_id)
    assert raw_order["execution_authorization_id"] == "paper-observation-runtime-authorization"
    assert raw_order["broker_execution_mode"] == "paper_only"
    assert raw_order["live_trading_authorized"] is False


def test_alpaca_paper_adapter_rejects_invalid_order_fail_closed():
    adapter = _adapter()

    order = adapter.submit_order(
        BrokerOrderRequest(
            symbol="",
            side=OrderSide.BUY,
            quantity=0,
            order_type=OrderType.MARKET,
            strategy_id="",
            signal_id="",
        ),
        authorization=_authorization(),
    )

    assert order.status == OrderStatus.REJECTED
    assert "symbol is required" in (order.reason or "")
    assert "quantity must be positive" in (order.reason or "")


def test_alpaca_paper_adapter_blocks_non_paper_endpoint():
    with pytest.raises(ValueError, match="paper endpoint"):
        AlpacaPaperAdapter(
            AlpacaPaperAdapterConfig(endpoint="https://api.alpaca.markets"),
            transport=InMemoryAlpacaPaperTransport(),
        )


def test_alpaca_paper_adapter_keeps_official_paper_endpoint():
    adapter = AlpacaPaperAdapter(
        AlpacaPaperAdapterConfig(endpoint=ALPACA_PAPER_ENDPOINT),
        transport=InMemoryAlpacaPaperTransport(),
    )

    assert adapter.config.endpoint == ALPACA_PAPER_ENDPOINT
    assert adapter.mode == BrokerMode.PAPER


def test_alpaca_paper_adapter_cancel_order():
    adapter = _adapter()
    order = adapter.submit_order(
        BrokerOrderRequest(
            symbol="MSFT",
            side=OrderSide.BUY,
            quantity=1,
            order_type=OrderType.MARKET,
            strategy_id="strategy",
            signal_id="signal",
        ),
        authorization=_authorization(),
    )

    cancelled = adapter.cancel_order(order.order_id)

    assert cancelled.status == OrderStatus.CANCELLED
    assert adapter.get_order_status(order.order_id).status == OrderStatus.CANCELLED


def test_alpaca_paper_adapter_account_snapshot_and_reconciliation():
    adapter = _adapter()
    adapter.submit_order(
        BrokerOrderRequest(
            symbol="NVDA",
            side=OrderSide.BUY,
            quantity=2,
            order_type=OrderType.LIMIT,
            limit_price=900.0,
            strategy_id="strategy",
            signal_id="signal",
        ),
        authorization=_authorization(),
    )

    snapshot = adapter.get_account_snapshot()
    report = adapter.reconcile_orders()

    assert snapshot.mode == BrokerMode.PAPER
    assert snapshot.cash == 75_000
    assert report.mode == BrokerMode.PAPER
    assert report.order_count == 1
    assert report.passed is True


def test_alpaca_position_and_fill_mapping():
    transport = InMemoryAlpacaPaperTransport()
    transport.positions.append(
        {
            "symbol": "AAPL",
            "qty": "5",
            "market_value": "1000.5",
            "avg_entry_price": "190.1",
            "unrealized_pl": "50.2",
        }
    )
    transport.fills.append(
        {
            "id": "fill-1",
            "order_id": "order-1",
            "symbol": "AAPL",
            "side": "buy",
            "qty": "5",
            "price": "190.1",
            "transaction_time": "2026-05-27T10:00:00+00:00",
            "commission": "0",
        }
    )
    adapter = AlpacaPaperAdapter(AlpacaPaperAdapterConfig(), transport=transport)

    position = adapter.list_positions()[0]
    fill = adapter.list_fills()[0]

    assert position.symbol == "AAPL"
    assert position.quantity == 5
    assert position.market_value == 1000.5
    assert fill.fill_id == "fill-1"
    assert fill.fill_price == 190.1
