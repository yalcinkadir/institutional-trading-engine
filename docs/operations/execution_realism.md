# P44: Execution Realism Layer

## Purpose

P44 applies realistic execution assumptions before edge validation.

Raw historical R-multiples can look better than executable results because they often ignore spread and slippage. This layer adjusts historical trade records before they are passed into downstream validation.

## Default Assumptions

```text
spread cost          0.05% per trade
normal slippage      0.10%
volatile slippage    0.30%
```

Volatile regimes include labels such as:

```text
volatile
high_vol
high-vol
high volatility
panic
dislocation
risk_off
risk-off
```

## Cost Conversion

Execution cost is converted into R-multiple impact:

```text
total_cost_pct = spread_cost_pct + slippage_pct
cost_price = entry_price * total_cost_pct
execution_cost_r = cost_price / abs(entry_price - stop_loss)
adjusted_r = original_r - execution_cost_r
```

## Required Record Fields

Primary fields:

```text
result_r
entry_price
stop_loss
volatility_regime
```

Fallback fields:

```text
r_multiple      -> result_r
entry_trigger   -> entry_price
market_regime   -> volatility_regime
```

## Output Metadata

Adjusted records include:

```text
execution_realism_applied
execution_cost_r
spread_cost_pct
slippage_pct
no_lookahead_execution_adjustment
```

Invalid records are not adjusted and are marked with warnings such as:

```text
missing_result_r
missing_entry_price
missing_stop_loss
invalid_initial_risk
```

## Report Helpers

```python
from pathlib import Path
from src.validation.execution_realism import apply_execution_realism, write_execution_realism_report

report = apply_execution_realism(records)
write_execution_realism_report(
    report,
    json_path=Path("reports/validation/execution-realism.json"),
    markdown_path=Path("reports/validation/execution-realism.md"),
)
```

## Tests

```bash
pytest tests/test_execution_realism.py
```

## Guardrails

This layer is decision-support only.

It does not:

- place orders
- connect to a broker
- authorize live trading
- model market impact perfectly
- replace out-of-sample validation
