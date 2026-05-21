# Stop-Loss Quality Engine

The Stop-Loss Quality Engine is the third concrete implementation step of the Entry / Stop / Exit Decision Quality roadmap.

The system should not only store `stop_loss`; it should explain why the stop exists and reject invalid or inverted stops before they reach the watcher.

P17 adds structure-aware long-side stops using confirmed 3-bar swing lows.

---

## Component

```text
src/signals/stop_loss_quality.py
src/signals/structure_levels.py
```

Integrated into:

```text
src/signals/signal_generator.py
scripts/generate_report.py
```

Tests:

```text
tests/test_stop_loss_quality.py
tests/test_structure_levels.py
tests/test_signal_generator_identity.py
tests/test_generate_report_structure_enrichment.py
```

---

## Stop Result

The engine returns:

```text
StopLossQualityResult
```

Fields:

```text
is_valid
stop_loss
stop_model
stop_reason
reasons
```

---

## Supported Stop Models

Current deterministic support:

```text
swing_low_structure_stop
atr_stop
pullback_structure_stop
retest_structure_stop
gap_fill_stop
scanner_provided_stop
```

---

## Structure-Aware Stop Rule

When `swing_low_3bar` is available and valid, it is preferred before ATR/setup fallback stops.

```text
stop_model: swing_low_structure_stop
stop_loss: swing_low_3bar * 0.998
stop_reason: swing-low structure stop with 0.2 percent buffer
```

Validation:

```text
swing_low_3bar < entry_trigger
(entry_trigger - stop_loss) / atr <= 3.0
```

If the swing low is missing, above entry, invalid or too far away, the engine falls back to the existing ATR/setup stop models.

---

## Structure Level Detection

3-bar swing-low detection lives in:

```text
src/signals/structure_levels.py
```

A confirmed 3-bar swing low means:

```text
previous_low > pivot_low < next_low
```

The latest bar cannot confirm itself, so the helper returns the latest historical confirmed pivot low.

Report generation enriches scanner metrics with:

```text
swing_low_3bar
```

before metrics are normalized and passed into signal generation.

---

## Default Rules

### Breakout / Default ATR Stop

```text
stop_model: atr_stop
stop_loss: entry_trigger - 2.0 ATR
stop_reason: ATR stop 2 ATR below entry
```

### Pullback Structure Stop

```text
stop_model: pullback_structure_stop
stop_loss: entry_trigger - 1.5 ATR
stop_reason: pullback structure stop 1.5 ATR below entry
```

### Retest Structure Stop

```text
stop_model: retest_structure_stop
stop_loss: entry_trigger - 1.25 ATR
stop_reason: retest structure stop 1.25 ATR below entry
```

### Gap-Fill Stop

```text
stop_model: gap_fill_stop
stop_loss: entry_trigger - 1.5 ATR
stop_reason: gap-fill stop 1.5 ATR below entry
```

### Scanner-Provided Stop

```text
stop_model: scanner_provided_stop
stop_reason: scanner provided stop below entry
```

Scanner-provided stops are only accepted when below entry for long signals and take precedence over structure stops.

---

## Failure Behavior

If stop quality fails during signal generation:

```text
BUY_WATCH -> NO_TRADE
notes include stop_quality reasons
trade plan validation also records invalid or missing levels when applicable
```

This prevents inverted or invalid stops from becoming actionable watcher signals.

---

## Example Failure Reasons

```text
missing_entry_trigger
missing_close
missing_or_invalid_atr
invalid_scanner_stop
scanner_stop_not_below_entry
```

Invalid or too-wide swing lows do not fail the signal by themselves. They are ignored and the engine falls back to ATR/setup stop logic.

---

## Design Rules

- Every actionable signal must have `stop_loss`, `stop_model` and `stop_reason`.
- Stops for long signals must be below entry.
- Stop derivation must be deterministic.
- Scanner-provided stops must be validated before use.
- Valid swing-low stops are preferred before ATR fallback.
- Too-wide structure stops are ignored to avoid poor risk/reward.
- Stop failure reasons must be visible in signal notes.
- Trade Plan Validator remains the final executable gate.

---

## Next Steps

Future improvements:

```text
support-zone clustering
invalidation-level stops
short-side swing-high stops
volatility regime stop adjustment
stop-quality feedback from historical outcomes
```
