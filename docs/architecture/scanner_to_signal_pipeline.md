# Scanner-to-Signal Metrics Pipeline

P15 repairs and hardens the scanner-to-signal data path. P18A extends the path with breakout context metrics.

Entry / Stop / Exit quality engines require live scanner metrics. If `close` and `atr14` do not reach signal generation, candidates are correctly downgraded to `NO_TRADE`, but the system is not operationally useful.

---

## Components

```text
src/scanner.py
src/signals/scanner_metrics_pipeline.py
src/signals/signal_generator.py
scripts/generate_report.py
```

Tests:

```text
tests/test_scanner_metrics_pipeline.py
tests/test_generate_report_scanner_metrics_pipeline.py
tests/test_entry_quality.py
tests/test_signal_generator_identity.py
```

---

## Required Signal Metrics

The signal generation path requires:

```text
close
atr14
```

Optional but preserved when available:

```text
atr_pct
entry
entry_type
stop_loss
exit_1
exit_2
high
low
volume
rvol
vwap
```

Breakout context metrics:

```text
high  -> preferred breakout trigger source
rvol  -> relative volume confirmation
vwap  -> optional breakout context filter
```

---

## Normalization

Raw scanner output is normalized before it reaches `build_signals()`.

Rules:

- numeric values are converted to `float`
- `NaN`, `inf`, invalid values and missing values become `None`
- `entry_type` is preserved as a string label
- `warnings` are preserved as a list
- missing symbols are tracked separately from incomplete symbols

---

## Diagnostics

The pipeline returns:

```text
ScannerMetricsDiagnostics
```

Fields:

```text
total_symbols
valid_symbols
missing_symbols
missing_required_fields
```

Warning line examples:

```text
scanner_metrics_missing:NVDA
scanner_metrics_incomplete:MSFT:atr14
```

These warnings are printed during report generation. This prevents data pipeline failures from being silently hidden inside `NO_TRADE` signal notes.

---

## Report Path

Report generation now follows:

```text
build_decision_report()
_load_scanner_metrics()
normalize_scanner_metrics_map()
build_signals(scanner_metrics_map=normalized)
_merge_signal_levels_into_decisions()
format_report()
save_signals()
```

The regression tests verify that valid scanner metrics produce non-null:

```text
close
entry_trigger
stop_loss
target_1
```

both in generated signals and merged decision report items.

---

## Breakout Context Behavior

When `high` exists, momentum breakout entry uses:

```text
entry_trigger = high * 1.001
```

When `rvol` exists and is below the configured threshold, momentum breakout is rejected:

```text
insufficient_volume_for_breakout
```

When `vwap` exists and `close < vwap`, momentum breakout is rejected:

```text
breakout_entry_below_vwap
```

Missing VWAP is non-fatal until intraday VWAP generation is implemented.

---

## Failure Behavior

Missing scanner metrics are non-fatal.

Expected behavior:

```text
missing metrics -> diagnostics warning
missing close/atr14 -> signal downgraded to NO_TRADE
report generation continues
```

This is intentional. Operational visibility improves without making report generation brittle.

---

## Design Rules

- Never silently swallow scanner metric failures.
- Normalize scanner metrics before signal generation.
- Preserve scanner-provided entry, stop and target levels when available.
- Preserve breakout context metrics when available.
- Missing live data should be visible as pipeline diagnostics.
- Quality engines remain defensive and downgrade incomplete trade plans.

---

## Next Steps

After P18A, the next operational layer is:

```text
P16 Trailing Stop and Partial Exit Management
```

This should manage lifecycle behavior after `TARGET_1_HIT`:

```text
partial exit
stop to breakeven
ATR trailing stop for runner
```
