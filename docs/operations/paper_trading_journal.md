# P46: Paper Trading Journal / Live Observation v2

## Purpose

P46 adds a structured paper trading journal for live observation before any real-capital decision.

It tracks theoretical model signals against observed paper/live-like outcomes:

```text
theoretical entry
paper fill price
slippage
5-day outcome in R
20-day outcome in R
model deviation
manual psychology/protocol deviation
```

This is validation evidence only. It does not authorize live trading.

## Input Fields

Primary fields:

```text
observation_id
symbol
observation_date
theoretical_entry
paper_fill_price
stop_loss
expected_result_r
outcome_5d_r
outcome_20d_r
would_have_held
impulse_to_deviate
drawdown_stress_note
notes
```

Fallback fields:

```text
signal_id          -> observation_id
date               -> observation_date
signal_date        -> observation_date
entry_trigger      -> theoretical_entry
entry_price        -> theoretical_entry
actual_fill_price  -> paper_fill_price
backtest_expectancy_r -> expected_result_r
```

## Execution Metrics

```text
fill_deviation_pct = (paper_fill_price - theoretical_entry) / theoretical_entry
slippage_r = (paper_fill_price - theoretical_entry) / abs(theoretical_entry - stop_loss)
```

Default execution deviation thresholds:

```text
max_acceptable_slippage_r = 0.25
max_acceptable_fill_deviation_pct = 0.25%
```

## Model Deviation

The journal compares expected R against observed forward outcomes:

```text
model_deviation_5d_r  = outcome_5d_r  - expected_result_r
model_deviation_20d_r = outcome_20d_r - expected_result_r
```

A model deviation is flagged when absolute deviation is at least 1.0R.

## Psychology / Protocol Fields

Manual review fields:

```text
would_have_held
impulse_to_deviate
drawdown_stress_note
notes
```

A psychology deviation is flagged if:

```text
would_have_held == False
or impulse_to_deviate == True
```

## Weekly Summary

Observations are grouped by ISO week start.

Weekly metrics:

```text
observation_count
filled_count
average_slippage_r
average_fill_deviation_pct
average_5d_r
average_20d_r
execution_deviation_count
model_deviation_count
psychology_deviation_count
```

## Example

```python
from src.validation.paper_trading_journal import analyze_paper_trading_journal

records = [
    {
        "observation_id": "obs-1",
        "symbol": "SPY",
        "observation_date": "2024-01-08",
        "theoretical_entry": 100.0,
        "paper_fill_price": 100.2,
        "stop_loss": 98.0,
        "expected_result_r": 1.0,
        "outcome_5d_r": 0.8,
        "outcome_20d_r": 1.4,
        "would_have_held": True,
        "impulse_to_deviate": False,
    }
]

report = analyze_paper_trading_journal(records)
```

## Report Helpers

```python
from pathlib import Path
from src.validation.paper_trading_journal import write_paper_trading_journal_report

write_paper_trading_journal_report(
    report,
    json_path=Path("reports/validation/paper-trading-journal.json"),
    markdown_path=Path("reports/validation/paper-trading-journal.md"),
)
```

## Tests

```bash
pytest tests/test_paper_trading_journal.py
```

## Guardrails

This journal is decision-support only.

It does not:

- place orders
- connect to a broker
- authorize live trading
- replace out-of-sample validation
- prove forward profitability
