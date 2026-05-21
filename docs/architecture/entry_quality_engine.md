# Entry Quality Engine

The Entry Quality Engine is the second concrete implementation step of the Entry / Stop / Exit Decision Quality roadmap.

The system should not only store an `entry_trigger`; it should explain why that entry exists and reject invalid or late entries.

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

Initial deterministic support:

```text
breakout
pullback
retest
gap_fill
at_market only when explicitly allowed
```

---

## Default Rules

### Momentum Breakout

```text
entry_type: breakout
entry_trigger: close + 0.5 ATR
entry_reason: breakout entry above current close using 0.5 ATR buffer
```

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

This prevents late or impossible entries from becoming actionable watcher signals.

---

## Design Rules

- Every actionable signal must have `entry_trigger`, `entry_type` and `entry_reason`.
- Entry derivation must be deterministic.
- At-market entries are blocked unless explicitly allowed.
- Late breakout entries must be rejected.
- Entry failure reasons must be visible in signal notes.
- Trade Plan Validator remains the final executable gate.

---

## Next Steps

The Entry Quality Engine is intentionally deterministic first. Next improvements should add richer structure awareness:

```text
recent resistance / breakout level
recent support / pullback level
retest of prior breakout
gap boundary detection
late-entry blocking by current price vs entry trigger
```
