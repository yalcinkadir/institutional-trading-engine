from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Iterable

from src.execution.broker_adapter import BrokerOrderRequest, OrderSide, OrderType


class SliceAlgorithm(str, Enum):
    TWAP = "twap"
    VWAP = "vwap"


MAX_SLICE_COUNT = 100
QUANTITY_PRECISION = 6


@dataclass(frozen=True)
class SlicingPlanRequest:
    symbol: str
    side: OrderSide
    total_quantity: float
    strategy_id: str
    signal_id: str
    slice_count: int
    algorithm: SliceAlgorithm
    order_type: OrderType = OrderType.MARKET
    limit_price: float | None = None
    stop_price: float | None = None
    start_at: str | None = None
    interval_seconds: int = 300
    volume_weights: tuple[float, ...] | None = None
    client_order_id_prefix: str | None = None


@dataclass(frozen=True)
class SlicedOrder:
    slice_id: str
    sequence: int
    total_slices: int
    scheduled_at: str
    quantity: float
    participation_weight: float
    order_request: BrokerOrderRequest


@dataclass(frozen=True)
class SlicingPlan:
    algorithm: SliceAlgorithm
    symbol: str
    side: OrderSide
    total_quantity: float
    total_slices: int
    slices: list[SlicedOrder]
    notes: list[str] = field(default_factory=list)

    def total_sliced_quantity(self) -> float:
        return round(sum(item.quantity for item in self.slices), QUANTITY_PRECISION)


def build_slicing_plan(request: SlicingPlanRequest) -> SlicingPlan:
    """Build a deterministic paper-execution slicing plan.

    The function is intentionally pure. It does not submit orders and it does not
    fetch market data. It only turns a parent execution intent into child
    BrokerOrderRequest objects that can be submitted to a paper broker adapter.
    """

    _validate_request(request)
    start_at = _parse_start_at(request.start_at)
    quantity_weights = _build_quantity_weights(request)
    display_weights = _round_weights(quantity_weights)
    quantities = _allocate_quantities(request.total_quantity, quantity_weights)
    prefix = _client_order_id_prefix(request)

    slices: list[SlicedOrder] = []
    for index, quantity in enumerate(quantities, start=1):
        scheduled_at = (start_at + timedelta(seconds=request.interval_seconds * (index - 1))).isoformat()
        slice_id = f"{prefix}-{index:03d}"
        broker_request = BrokerOrderRequest(
            symbol=request.symbol.strip().upper(),
            side=request.side,
            quantity=quantity,
            order_type=request.order_type,
            strategy_id=request.strategy_id.strip(),
            signal_id=request.signal_id.strip(),
            limit_price=request.limit_price,
            stop_price=request.stop_price,
            client_order_id=slice_id,
        )
        slices.append(
            SlicedOrder(
                slice_id=slice_id,
                sequence=index,
                total_slices=request.slice_count,
                scheduled_at=scheduled_at,
                quantity=quantity,
                participation_weight=display_weights[index - 1],
                order_request=broker_request,
            )
        )

    return SlicingPlan(
        algorithm=request.algorithm,
        symbol=request.symbol.strip().upper(),
        side=request.side,
        total_quantity=round(request.total_quantity, QUANTITY_PRECISION),
        total_slices=request.slice_count,
        slices=slices,
        notes=[
            "paper_execution_only",
            "deterministic_child_order_plan",
            "no_live_broker_execution_performed",
        ],
    )


def build_twap_plan(
    *,
    symbol: str,
    side: OrderSide,
    total_quantity: float,
    slice_count: int,
    strategy_id: str,
    signal_id: str,
    order_type: OrderType = OrderType.MARKET,
    limit_price: float | None = None,
    start_at: str | None = None,
    interval_seconds: int = 300,
    client_order_id_prefix: str | None = None,
) -> SlicingPlan:
    return build_slicing_plan(
        SlicingPlanRequest(
            symbol=symbol,
            side=side,
            total_quantity=total_quantity,
            strategy_id=strategy_id,
            signal_id=signal_id,
            slice_count=slice_count,
            algorithm=SliceAlgorithm.TWAP,
            order_type=order_type,
            limit_price=limit_price,
            start_at=start_at,
            interval_seconds=interval_seconds,
            client_order_id_prefix=client_order_id_prefix,
        )
    )


def build_vwap_plan(
    *,
    symbol: str,
    side: OrderSide,
    total_quantity: float,
    volume_weights: Iterable[float],
    strategy_id: str,
    signal_id: str,
    order_type: OrderType = OrderType.MARKET,
    limit_price: float | None = None,
    start_at: str | None = None,
    interval_seconds: int = 300,
    client_order_id_prefix: str | None = None,
) -> SlicingPlan:
    weights = tuple(volume_weights)
    return build_slicing_plan(
        SlicingPlanRequest(
            symbol=symbol,
            side=side,
            total_quantity=total_quantity,
            strategy_id=strategy_id,
            signal_id=signal_id,
            slice_count=len(weights),
            algorithm=SliceAlgorithm.VWAP,
            order_type=order_type,
            limit_price=limit_price,
            start_at=start_at,
            interval_seconds=interval_seconds,
            volume_weights=weights,
            client_order_id_prefix=client_order_id_prefix,
        )
    )


def _validate_request(request: SlicingPlanRequest) -> None:
    if not request.symbol.strip():
        raise ValueError("symbol is required")
    if request.total_quantity <= 0:
        raise ValueError("total_quantity must be positive")
    if request.slice_count <= 0:
        raise ValueError("slice_count must be positive")
    if request.slice_count > MAX_SLICE_COUNT:
        raise ValueError(f"slice_count must not exceed {MAX_SLICE_COUNT}")
    if not request.strategy_id.strip():
        raise ValueError("strategy_id is required")
    if not request.signal_id.strip():
        raise ValueError("signal_id is required")
    if request.interval_seconds <= 0:
        raise ValueError("interval_seconds must be positive")
    if request.order_type == OrderType.LIMIT and request.limit_price is None:
        raise ValueError("limit_price is required for sliced limit orders")
    if request.order_type == OrderType.STOP:
        raise ValueError("stop orders are not supported for VWAP/TWAP slicing")
    if request.algorithm == SliceAlgorithm.VWAP:
        if request.volume_weights is None:
            raise ValueError("volume_weights are required for VWAP slicing")
        if len(request.volume_weights) != request.slice_count:
            raise ValueError("volume_weights length must equal slice_count")
        if any(weight <= 0 for weight in request.volume_weights):
            raise ValueError("volume_weights must be positive")


def _build_quantity_weights(request: SlicingPlanRequest) -> list[float]:
    if request.algorithm == SliceAlgorithm.TWAP:
        return [1.0 / request.slice_count] * request.slice_count

    assert request.volume_weights is not None
    total_weight = sum(request.volume_weights)
    if total_weight <= 0:
        raise ValueError("volume_weights must sum to a positive number")
    return [weight / total_weight for weight in request.volume_weights]


def _round_weights(weights: list[float]) -> list[float]:
    return [round(weight, QUANTITY_PRECISION) for weight in weights]


def _allocate_quantities(total_quantity: float, weights: list[float]) -> list[float]:
    quantities: list[float] = []
    allocated = 0.0
    for index, weight in enumerate(weights, start=1):
        if index == len(weights):
            quantity = round(total_quantity - allocated, QUANTITY_PRECISION)
        else:
            quantity = round(total_quantity * weight, QUANTITY_PRECISION)
            allocated = round(allocated + quantity, QUANTITY_PRECISION)
        if quantity <= 0:
            raise ValueError("slice quantity must be positive after allocation")
        quantities.append(quantity)
    return quantities


def _parse_start_at(value: str | None) -> datetime:
    if value is None:
        return datetime.now(timezone.utc).replace(microsecond=0)
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.replace(microsecond=0)


def _client_order_id_prefix(request: SlicingPlanRequest) -> str:
    if request.client_order_id_prefix:
        return request.client_order_id_prefix.strip()
    return f"{request.algorithm.value}-{request.signal_id.strip()}-{request.symbol.strip().upper()}"
