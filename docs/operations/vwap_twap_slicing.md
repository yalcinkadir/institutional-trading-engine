# VWAP / TWAP Paper Slicing

Status date: 2026-05-27

C3 adds deterministic VWAP/TWAP child-order planning for paper execution.

## Purpose

The slicing engine converts a parent execution intent into a set of scheduled child `BrokerOrderRequest` objects.

It does not:

```text
place live trades
connect to a broker
fetch market data
claim execution edge
```

It does:

```text
split parent quantity deterministically
preserve total quantity after rounding
create stable child client_order_id values
support paper broker adapter submission
fail closed on invalid slicing requests
```

## Supported Algorithms

### TWAP

TWAP splits total quantity equally across a fixed number of time slices.

```text
total_quantity = 10
slice_count = 4
→ 2.5, 2.5, 2.5, 2.5
```

### VWAP

VWAP splits total quantity according to explicit volume weights.

```text
total_quantity = 100
volume_weights = [10, 20, 70]
→ 10, 20, 70
```

The engine normalizes weights internally, so `[1, 2, 7]` and `[10, 20, 70]` produce the same allocation.

## Safety Rules

The engine fails closed when:

```text
symbol is empty
total_quantity <= 0
slice_count <= 0
slice_count > 100
strategy_id is empty
signal_id is empty
interval_seconds <= 0
limit order has no limit_price
stop orders are requested
VWAP weights are missing, non-positive, or length-mismatched
```

Stop orders are intentionally excluded from C3 slicing. Stop-loss handling remains a separate risk lifecycle concern.

## Integration Contract

Core module:

```text
src/execution/order_slicing.py
```

Primary functions:

```text
build_twap_plan(...)
build_vwap_plan(...)
build_slicing_plan(...)
```

Output object:

```text
SlicingPlan
  slices: list[SlicedOrder]
    order_request: BrokerOrderRequest
```

The generated child requests can be submitted to paper adapters such as:

```text
MockPaperBrokerAdapter
AlpacaPaperAdapter
```

## Test Coverage

Core tests:

```text
tests/test_order_slicing.py
```

Covered scenarios:

```text
TWAP equal split
TWAP rounding remainder on last slice
VWAP volume-weighted split
scheduled timestamps by interval
client_order_id generation
paper broker adapter compatibility
invalid request fail-closed behavior
```

## Execution Status

C3 remains paper-execution infrastructure only.

Real-money execution stays explicitly unauthorized.