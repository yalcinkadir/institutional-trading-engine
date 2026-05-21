# Entry / Stop / Exit Feedback

P14.5 adds deterministic feedback aggregation for Entry / Stop / Exit decision-quality models.

The goal is to measure whether the implemented entry, stop and exit models actually work historically.

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

Missing model fields are grouped under:

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

## Grouping

Feedback is grouped by:

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
```

---

## Design Rules

- Aggregation is deterministic.
- Empty inputs do not crash.
- Missing fields are grouped as `unknown`.
- Rates are rounded to four decimals.
- The module does not introduce new trading rules.
- The output is designed for later scoring/expectancy consumption.

---

## Next Steps

Future work:

```text
wire report helper into weekly feedback workflow
consume poor model statistics in adaptive scoring
store feedback reports under reports/feedback
add regime-aware grouping
add symbol/universe grouping
```
