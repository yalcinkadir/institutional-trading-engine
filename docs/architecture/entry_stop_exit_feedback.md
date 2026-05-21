# Entry / Stop / Exit Feedback

P14.5 adds deterministic feedback aggregation for Entry / Stop / Exit decision-quality models.

P21 adds regime-aware grouping so model quality can be evaluated in market-context dimensions such as bullish, risk-off, low-volatility or high-volatility regimes.

The goal is to measure whether the implemented entry, stop and exit models actually work historically, and whether they work differently across regimes.

---

## Components

```text
src/feedback/entry_stop_exit_feedback.py
src/feedback/entry_stop_exit_report.py
```

Tests:

```text
tests/test_entry_stop_exit_feedback.py
tests/test_entry_stop_exit_report.py
```

---

## Input Records

The feedback aggregator is source-agnostic. Records can come from:

```text
historical validation
signal lifecycle outcomes
JSONL exports
future database rows
weekly report artifacts
```

Supported status fields:

```text
outcome
final_status
status
event_type
```

Supported boolean fields:

```text
entry_hit
stop_hit
target_1_hit
target_2_hit
expired_without_entry
false_breakout
```

Supported model dimensions:

```text
entry_type
setup_type
stop_model
exit_model
```

Supported regime dimensions:

```text
market_regime
risk_state
volatility_regime
```

Missing model or regime fields are grouped under:

```text
unknown
```

---

## Measurements

The report calculates:

```text
total
entry_hits
stop_hits
target_1_hits
target_2_hits
expired_without_entry
false_breakouts
entry_hit_rate
stop_hit_rate
target_1_hit_rate
target_2_hit_rate
expired_without_entry_rate
false_breakout_rate
```

---

## Default Grouping

Default feedback remains backwards-compatible and groups by:

```text
entry_type
setup_type
stop_model
exit_model
```

Examples:

```text
entry_type = breakout
stop_model = swing_low_structure_stop
exit_model = momentum_targets
setup_type = momentum_breakout
```

---

## Regime-Aware Grouping

Regime-aware grouping is available through:

```text
REGIME_AWARE_GROUP_FIELDS
aggregate_regime_aware_entry_stop_exit_feedback()
```

It groups by:

```text
entry_type
setup_type
stop_model
exit_model
market_regime
risk_state
volatility_regime
```

Examples:

```text
market_regime = bullish
market_regime = risk_off
risk_state = risk_on
risk_state = defensive
volatility_regime = low_vol
volatility_regime = high_vol
```

This allows questions such as:

```text
Does breakout work in bullish regimes?
Does ATR stop fail more often in high-volatility regimes?
Does swing_low_structure_stop behave better in risk-on regimes?
Do pullback entries expire more often in defensive regimes?
```

---

## Custom Grouping

Consumers can request only selected dimensions:

```python
aggregate_entry_stop_exit_feedback(
    records,
    group_fields=("market_regime", "risk_state"),
)
```

The default behavior is unchanged unless regime fields are explicitly requested.

---

## False Breakout Classification

A false breakout is counted when:

```text
false_breakout = true
```

or when:

```text
entry_hit = true
stop_hit = true
target_1_hit = false
```

This lets explicit outcome records and lifecycle-derived records both contribute to the same metric.

---

## Report Output

The report helper can persist:

```text
entry-stop-exit-feedback.json
entry-stop-exit-feedback.md
```

Markdown format includes:

```text
overall statistics
grouped statistics by entry_type
grouped statistics by setup_type
grouped statistics by stop_model
grouped statistics by exit_model
optional grouped statistics by market_regime
optional grouped statistics by risk_state
optional grouped statistics by volatility_regime
```

---

## Design Rules

- Aggregation is deterministic.
- Empty inputs do not crash.
- Missing fields are grouped as `unknown`.
- Default grouping remains backwards-compatible.
- Regime grouping is opt-in through regime-aware group fields.
- Rates are rounded to four decimals.
- The module does not introduce new trading rules.
- The output is designed for later scoring/expectancy consumption.

---

## Next Steps

Future work:

```text
wire regime-aware report helper into weekly feedback workflow
consume poor model statistics in adaptive scoring
store feedback reports under reports/feedback
add symbol/universe grouping
add cross-field grouping such as entry_type x market_regime
```
