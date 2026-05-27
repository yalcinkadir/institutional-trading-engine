# C4 Order Reconciliation Engine

## Purpose

C4 adds a deterministic reconciliation layer for paper-execution state.

It connects the execution-observation chain:

```text
Signal
→ BrokerOrderRequest
→ BrokerOrder
→ BrokerFill
→ OrderLifecycleState
→ PortfolioState
```

The engine is intentionally pure and paper-safe. It does not submit orders, cancel orders, fetch market data, place live trades or authorize live execution.

## Implemented module

```text
src/execution/order_reconciliation.py
```

Primary API:

```python
reconcile_orders_and_fills(
    orders=[...],
    fills=[...],
    starting_cash=100_000,
)
```

## Output

The engine returns an `OrderReconciliationSnapshot` with:

```text
passed
order_count
fill_count
position_count
orders[]
portfolio
issues[]
notes[]
```

Each order is converted into an auditable lifecycle state:

```text
requested_quantity
filled_quantity
remaining_quantity
average_fill_price
fill_count
status
issues
```

Portfolio state includes:

```text
cash
realized_pnl
total_commissions
positions[]
```

## Fail-closed rules

The snapshot fails when hard inconsistencies are found:

```text
duplicate_order_id
orphan_fill
invalid_fill_quantity
invalid_fill_price
invalid_commission
fill_symbol_mismatch
fill_side_mismatch
overfilled_order
filled_status_quantity_mismatch
partial_status_quantity_mismatch
terminal_order_has_fills
```

Warnings are allowed but visible, for example an accepted order with fills where the broker status has not yet moved to partial or filled.

## Portfolio handling

The portfolio builder derives state from valid fills only.

Buy fills:

```text
increase long exposure or reduce short exposure
cash decreases by gross notional + commission
```

Sell fills:

```text
reduce long exposure or increase short exposure
cash increases by gross notional - commission
```

Realized PnL is calculated only when an existing position is reduced or closed. Commissions are included in realized PnL as costs.

## Safety boundary

C4 is still decision-support infrastructure only.

```text
paper_execution_reconciliation_only
no_live_order_submission_performed
fail_closed_on_inconsistent_order_fill_state
```

Real-money execution remains disabled by design.

## Test coverage

```text
tests/test_order_reconciliation.py
```

Covered scenarios:

```text
filled buy order → portfolio state
partial fill → remaining quantity
buy then sell → realized PnL and cash
orphan fill → fail closed
overfilled order → fail closed
rejected/cancelled order with fills → fail closed
symbol/side mismatch → fail closed
duplicate order id → fail closed
```
