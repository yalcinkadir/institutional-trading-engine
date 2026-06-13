import pytest

from src.execution.broker_adapter import (
    ExecutionAuthorization,
    MockPaperBrokerAdapter,
    OrderSide,
    OrderStatus,
    OrderType,
)
from src.execution.order_slicing import (
    MAX_SLICE_COUNT,
    SliceAlgorithm,
    SlicingPlanRequest,
    build_slicing_plan,
    build_twap_plan,
    build_vwap_plan,
)


def test_twap_plan_splits_quantity_equally_and_preserves_total():
    plan = build_twap_plan(
        symbol="aapl",
        side=OrderSide.BUY,
        total_quantity=10,
        slice_count=4,
        strategy_id="rule_based_core_v1",
        signal_id="sig-001",
        start_at="2026-05-27T13:30:00+00:00",
        interval_seconds=60,
        client_order_id_prefix="twap-test",
    )

    assert plan.algorithm == SliceAlgorithm.TWAP
    assert plan.symbol == "AAPL"
    assert plan.total_sliced_quantity() == 10
    assert [item.quantity for item in plan.slices] == [2.5, 2.5, 2.5, 2.5]
    assert [item.scheduled_at for item in plan.slices] == [
        "2026-05-27T13:30:00+00:00",
        "2026-05-27T13:31:00+00:00",
        "2026-05-27T13:32:00+00:00",
        "2026-05-27T13:33:00+00:00",
    ]
    assert plan.slices[0].order_request.client_order_id == "twap-test-001"
    assert plan.slices[-1].order_request.client_order_id == "twap-test-004"


def test_twap_rounding_reconciles_remainder_on_last_slice():
    plan = build_twap_plan(
        symbol="MSFT",
        side=OrderSide.BUY,
        total_quantity=10,
        slice_count=3,
        strategy_id="strategy",
        signal_id="signal",
        start_at="2026-05-27T13:30:00+00:00",
    )

    assert plan.total_sliced_quantity() == 10
    assert [item.quantity for item in plan.slices] == [3.333333, 3.333333, 3.333334]


def test_vwap_plan_allocates_by_volume_weights():
    plan = build_vwap_plan(
        symbol="NVDA",
        side=OrderSide.BUY,
        total_quantity=100,
        volume_weights=[10, 20, 70],
        strategy_id="strategy",
        signal_id="signal",
        start_at="2026-05-27T13:30:00Z",
        interval_seconds=120,
        client_order_id_prefix="vwap-test",
    )

    assert plan.algorithm == SliceAlgorithm.VWAP
    assert plan.total_sliced_quantity() == 100
    assert [item.quantity for item in plan.slices] == [10, 20, 70]
    assert [item.participation_weight for item in plan.slices] == [0.1, 0.2, 0.7]
    assert plan.slices[2].scheduled_at == "2026-05-27T13:34:00+00:00"


def test_slicing_plan_creates_broker_order_requests_compatible_with_paper_adapter():
    plan = build_twap_plan(
        symbol="QQQ",
        side=OrderSide.SELL,
        total_quantity=6,
        slice_count=3,
        strategy_id="strategy",
        signal_id="signal",
        order_type=OrderType.LIMIT,
        limit_price=500.25,
        start_at="2026-05-27T13:30:00+00:00",
    )
    adapter = MockPaperBrokerAdapter()
    authorization = ExecutionAuthorization.paper_observation(
        authorization_id="order-slicing-paper-authorization",
        reason="order slicing compatibility test uses paper broker only",
    )

    orders = [
        adapter.submit_order(slice_order.order_request, authorization=authorization)
        for slice_order in plan.slices
    ]

    assert [order.status for order in orders] == [OrderStatus.ACCEPTED] * 3
    assert [order.quantity for order in orders] == [2, 2, 2]
    assert all(order.order_type == OrderType.LIMIT for order in orders)
    assert all(order.limit_price == 500.25 for order in orders)


def test_generic_slicing_request_supports_market_twap():
    plan = build_slicing_plan(
        SlicingPlanRequest(
            symbol="SPY",
            side=OrderSide.BUY,
            total_quantity=5,
            strategy_id="strategy",
            signal_id="signal",
            slice_count=5,
            algorithm=SliceAlgorithm.TWAP,
            start_at="2026-05-27T13:30:00+00:00",
        )
    )

    assert len(plan.slices) == 5
    assert plan.total_sliced_quantity() == 5
    assert all(item.order_request.order_type == OrderType.MARKET for item in plan.slices)


@pytest.mark.parametrize(
    "slicing_request, expected_message",
    [
        (
            SlicingPlanRequest(
                symbol="",
                side=OrderSide.BUY,
                total_quantity=1,
                strategy_id="strategy",
                signal_id="signal",
                slice_count=1,
                algorithm=SliceAlgorithm.TWAP,
            ),
            "symbol is required",
        ),
        (
            SlicingPlanRequest(
                symbol="AAPL",
                side=OrderSide.BUY,
                total_quantity=0,
                strategy_id="strategy",
                signal_id="signal",
                slice_count=1,
                algorithm=SliceAlgorithm.TWAP,
            ),
            "total_quantity must be positive",
        ),
        (
            SlicingPlanRequest(
                symbol="AAPL",
                side=OrderSide.BUY,
                total_quantity=1,
                strategy_id="strategy",
                signal_id="signal",
                slice_count=MAX_SLICE_COUNT + 1,
                algorithm=SliceAlgorithm.TWAP,
            ),
            "slice_count exceeds maximum",
        ),
        (
            SlicingPlanRequest(
                symbol="AAPL",
                side=OrderSide.BUY,
                total_quantity=1,
                strategy_id="strategy",
                signal_id="signal",
                slice_count=1,
                algorithm=SliceAlgorithm.VWAP,
            ),
            "volume_weights are required for VWAP slicing",
        ),
    ],
)
def test_invalid_slicing_requests_fail_closed(slicing_request, expected_message):
    with pytest.raises(ValueError, match=expected_message):
        build_slicing_plan(slicing_request)
