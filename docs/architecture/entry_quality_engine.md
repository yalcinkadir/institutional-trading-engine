# Entry Quality Engine

The Entry Quality Engine is the second concrete implementation step of the Entry / Stop / Exit Decision Quality roadmap.

The system should not only store an `entry_trigger`; it should explain why that entry exists and reject invalid, late or weak-context entries.

---

## Component

```text
src/signals/entry_quality.py
```

Integrated into:

```text
src/signals/signal_generator.py
```

Tests:

```text
tests/test_entry_quality.py
tests/test_signal_generator_identity.py
```

---

## Entry Result

The engine returns:

```text
EntryQualityResult
```

Fields:

```text
is_valid
entry_trigger
entry_type
entry_reason
reasons
```

---

## Supported Entry Types

```text
breakout
pullback
retest
gap_fill
at_market only when explicitly allowed
```

---

## Breakout Context Rules

Momentum breakout entries now prefer a scanner-provided high trigger when available.

### Preferred Breakout Trigger

```text
entry_type: breakout
entry_trigger: high * 1.001
entry_reason: breakout above scanner high with 0.1 percent buffer
```

### Fallback Breakout Trigger

If `high` is unavailable:

```text
entry_type: breakout
entry_trigger: close + 0.5 ATR
entry_reason: breakout entry above current close using 0.5 ATR buffer
```

### Relative Volume Confirmation

When `rvol` is available, weak breakout volume is rejected.

Default threshold:

```text
min_breakout_rvol = 0.8
```

Failure reason:

```text
insufficient_volume_for_breakout
```

### Optional VWAP Filter

When `vwap` is available, breakout entries below VWAP are rejected.

Failure reason:

```text
breakout_entry_below_vwap
```

Missing VWAP is currently non-fatal. Full intraday VWAP calculation is planned separately.

---

## Other Default Rules

### Pullback Continuation

```text
entry_type: pullback
entry_trigger: close - 1.0 ATR
entry_reason: pullback entry near 1 ATR below current close
```

### Retest Continuation

```text
entry_type: retest
entry_trigger: close - 0.5 ATR
entry_reason: retest entry near 0.5 ATR below current close
```

### Gap Fill

```text
entry_type: gap_fill
entry_trigger: close - 0.75 ATR
entry_reason: gap-fill entry near 0.75 ATR below current close
```

---

## Late Entry Rejection

Scanner-provided breakout entries are rejected when the current price is too far beyond the trigger.

Default threshold:

```text
max_breakout_extension_atr = 1.5
```

Failure reason:

```text
late_entry_price_extended_beyond_trigger
```

---

## Failure Behavior

If entry quality fails during signal generation:

```text
BUY_WATCH -> NO_TRADE
notes include entry_quality reasons
trade plan validation also records missing levels when applicable
```

This prevents late, weak-volume, below-VWAP or otherwise invalid entries from becoming actionable watcher signals.

---

## Design Rules

- Every actionable signal must have `entry_trigger`, `entry_type` and `entry_reason`.
- Momentum breakouts prefer scanner `high * 1.001` over ATR fallback.
- Low RVOL breakouts are rejected when RVOL exists.
- Breakouts below VWAP are rejected when VWAP exists.
- Missing VWAP is non-fatal until intraday VWAP support is added.
- At-market entries are blocked unless explicitly allowed.
- Late breakout entries must be rejected.
- Entry failure reasons must be visible in signal notes.
- Trade Plan Validator remains the final executable gate.

---

## Next Steps

The next entry improvements should add richer intraday structure and confirmation:

```text
intraday VWAP calculation
close-above-VWAP confirmation
breakout confirmation fields
support/resistance breakout level
false-breakout feedback
```
