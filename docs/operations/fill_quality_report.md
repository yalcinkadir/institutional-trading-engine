# C6 Fill Quality Report

Status date: 2026-05-28

C6 adds an execution-quality audit layer for observed paper/live fill records.

## Purpose

The fill-quality report measures whether observed fills behave within acceptable execution-quality tolerances.

It compares each observed fill against reference execution context:

```text
arrival/reference price
average fill price
requested quantity
filled quantity
bid/ask spread
submitted timestamp
first fill timestamp
```

It does not:

```text
place live trades
connect to a broker
change orders
approve live trading
claim execution edge
```

It does:

```text
measure directional slippage in basis points
measure spread width in basis points
measure fill delay
measure partial-fill and full-fill rates
fail closed on malformed or dangerous records
write JSON and Markdown audit reports
```

## Core Module

```text
src/validation/fill_quality_report.py
```

Main entry points:

```text
analyze_fill_quality(...)
load_fill_quality_records(...)
write_fill_quality_report(...)
render_fill_quality_markdown(...)
```

## CLI

```bash
python scripts/generate_fill_quality_report.py \
  --input-file reports/fill_quality_input/fills.json \
  --output-dir reports/fill_quality
```

Input format:

```json
{
  "records": [
    {
      "order_id": "order-1",
      "symbol": "AAPL",
      "side": "buy",
      "requested_quantity": 100,
      "filled_quantity": 100,
      "arrival_price": 100,
      "average_fill_price": 100.05,
      "submitted_at": "2026-05-28T13:30:00+00:00",
      "first_fill_at": "2026-05-28T13:30:10+00:00",
      "bid_price": 99.99,
      "ask_price": 100.01,
      "strategy_id": "strategy-1",
      "signal_id": "signal-1"
    }
  ]
}
```

## Gates

Default thresholds:

```text
max_abs_slippage_bps = 25.0
max_avg_abs_slippage_bps = 15.0
max_spread_bps = 20.0
max_avg_delay_seconds = 300.0
min_fill_rate = 0.95
min_full_fill_rate = 0.80
fail_on_missing_reference_price = true
```

Record-level fail-closed cases:

```text
missing order_id
missing symbol
invalid side
requested_quantity <= 0
filled_quantity < 0
overfilled order
missing arrival/reference price
invalid average fill price
crossed spread
negative fill delay
duplicate order_id
```

Aggregate gates:

```text
fill rate below minimum
full-fill rate below minimum
average absolute slippage above tolerance
average delay above tolerance
```

## Directional Slippage

For buys:

```text
average_fill_price > arrival_price => adverse slippage
```

For sells:

```text
average_fill_price < arrival_price => adverse slippage
```

This keeps slippage positive when execution is worse than the arrival/reference price.

## Test Coverage

```text
tests/test_fill_quality_report.py
```

Covered scenarios:

```text
good fill pass
bad buy slippage
sell-side directional slippage
partial fill and aggregate fill-rate gates
wide spread warning
slow average delay warning
missing reference price error / warning mode
duplicate order id
overfill
crossed spread
negative fill delay
JSON input and report output
```

## Execution Status

C6 is an audit layer only.

It does not authorize live execution and does not call any broker adapter.
