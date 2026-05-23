# P41: Historical Edge Validation Framework

## Purpose

P41 adds a validation layer that checks whether completed historical trades show evidence of a positive edge.

This is the first step after the decision-quality fixes P36-P40. It does not approve live trading. It only measures whether the historical results are strong enough to justify deeper validation.

## Inputs

The validator accepts completed trade records with either:

```text
result_r
```

or fallback:

```text
r_multiple
```

Each value is interpreted as R-multiple per trade.

## Core Metrics

The framework calculates:

```text
total_trades
wins
losses
breakeven
win_rate
expectancy_r
profit_factor
max_drawdown
sharpe_ratio
max_consecutive_losses
recovery_time_trades
cumulative_r
```

## Default Validation Gates

```text
MIN_TOTAL_TRADES     = 300
MIN_PROFIT_FACTOR    = 1.4
MIN_EXPECTANCY_R     = 0.5
MAX_DRAWDOWN_LIMIT   = 0.25
MIN_SHARPE_RATIO     = 0.8
```

## Important Interpretation

A passing P41 report does not mean the system is ready for live capital.

It only means:

```text
historical edge metrics are strong enough to continue to P42-P47 validation
```

The next required stages are:

```text
P42 Regime-Phase Backtest Matrix
P43 Walk-Forward Validation
P44 Execution Realism Layer
P45 Out-of-Sample Validation Lockbox
P46 Paper Trading Journal / Live Observation v2
P47 Final Live Readiness Gate
```

## Example

```python
from src.validation.historical_edge_validation import validate_historical_edge

records = [
    {"result_r": 1.0},
    {"result_r": -0.5},
]

report = validate_historical_edge(records)
```

## Report Helpers

```python
from pathlib import Path
from src.validation.historical_edge_validation import write_historical_edge_report

write_historical_edge_report(
    report,
    json_path=Path("reports/validation/historical-edge.json"),
    markdown_path=Path("reports/validation/historical-edge.md"),
)
```

## Test

```bash
pytest tests/test_historical_edge_validation.py
```

## Guardrails

This framework is decision-support only.

It does not:

- place orders
- connect to a broker
- authorize live trading
- prove forward profitability
- replace out-of-sample validation
