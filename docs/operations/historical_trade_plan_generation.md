# Historical Trade Plan Generation

## Purpose

Generate deterministic historical `BUY_WATCH` trade plans from Polygon daily OHLCV bars.

The output feeds the gated edge-evidence backtest.

## Input

A directory of daily bar CSV files:

```text
data/historical_bars/*.csv
```

Required CSV columns:

```text
date,open,high,low,close,volume
```

## Output

```text
data/trade_plans/historical_trade_plans.json
```

The JSON contains:

```text
metadata
plans[]
```

Each plan includes:

```text
signal_id
symbol
signal_date
action
entry_trigger
stop_loss
target_1
target_2
valid_until
entry_type
setup_type
stop_model
exit_model
```

## Local command

```bash
python scripts/generate_historical_trade_plans.py \
  --bars-root data/historical_bars \
  --output data/trade_plans/historical_trade_plans.json \
  --max-plans 5000 \
  --max-plans-per-symbol 3 \
  --min-history 60 \
  --lookahead-days 20
```

## Workflow integration

The workflow below can generate plans automatically before the backtest:

```text
Edge Evidence From Polygon Artifact
```

Relevant inputs:

```text
generate_plans: true
max_generated_plans: 5000
max_plans_per_symbol: 3
plans_path: data/trade_plans/historical_trade_plans.json
```

Generated plans are uploaded as:

```text
generated-historical-trade-plans
```

## Strategy rule

The generator uses a simple deterministic pullback-continuation rule:

```text
close > SMA50
recent 10-day low touches/pulls below SMA20
minimum dollar volume passes
entry = close * 1.01
risk = max(ATR14 * 1.25, close * 0.02)
stop = entry - risk
target_1 = entry + 2R
target_2 = entry + 3R
```

This is a testable baseline, not a claim of edge.

## Tests

```bash
pytest tests/test_generate_historical_trade_plans.py -q
pytest tests/test_edge_evidence_from_polygon_artifact_workflow.py -q
```
