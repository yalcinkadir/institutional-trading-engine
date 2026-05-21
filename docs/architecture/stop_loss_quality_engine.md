# Stop-Loss Quality Engine

The Stop-Loss Quality Engine is the third concrete implementation step of the Entry / Stop / Exit Decision Quality roadmap.

The system should not only store `stop_loss`; it should explain why the stop exists and reject invalid or inverted stops before they reach the watcher.

---

## Component

```text
src/signals/stop_loss_quality.py
```

Integrated into:

```text
src/signals/signal_generator.py
```

Tests:

```text
tests/test_stop_loss_quality.py
tests/test_signal_generator_identity.py
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

Initial deterministic support:

```text
atr_stop
pullback_structure_stop
retest_structure_stop
gap_fill_stop
scanner_provided_stop
```

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

Scanner-provided stops are only accepted when below entry for long signals.

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

---

## Design Rules

- Every actionable signal must have `stop_loss`, `stop_model` and `stop_reason`.
- Stops for long signals must be below entry.
- Stop derivation must be deterministic.
- Scanner-provided stops must be validated before use.
- Stop failure reasons must be visible in signal notes.
- Trade Plan Validator remains the final executable gate.

---

## Next Steps

The Stop-Loss Quality Engine is deterministic first. Next improvements should add richer structure awareness:

```text
recent swing low / high based stops
support/resistance invalidation stops
volatility regime stop adjustment
stop-quality feedback from historical outcomes
```
