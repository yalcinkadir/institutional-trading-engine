# Exit / Target Quality Engine

The Exit / Target Quality Engine is the fourth concrete implementation step of the Entry / Stop / Exit Decision Quality roadmap.

The system should not only store `target_1` and `target_2`; it should explain why exit levels exist and reject invalid targets before they reach the watcher.

---

## Component

```text
src/signals/exit_target_quality.py
```

Integrated into:

```text
src/signals/signal_generator.py
```

Tests:

```text
tests/test_exit_target_quality.py
tests/test_signal_generator_identity.py
```

---

## Exit Result

The engine returns:

```text
ExitTargetQualityResult
```

Fields:

```text
is_valid
target_1
target_2
exit_model
exit_reason
reasons
```

---

## Supported Exit Models

Initial deterministic support:

```text
momentum_targets
pullback_targets
retest_targets
gap_fill_targets
scanner_provided_targets
default_risk_targets
```

---

## Default Rules

### Momentum Targets

```text
exit_model: momentum_targets
target_1: entry + 1.5R
target_2: entry + 2.5R
exit_reason: momentum targets at 1.5R and 2.5R
```

### Pullback Targets

```text
exit_model: pullback_targets
target_1: entry + 1.35R
target_2: entry + 2.25R
exit_reason: pullback continuation targets at 1.35R and 2.25R
```

### Retest Targets

```text
exit_model: retest_targets
target_1: entry + 1.4R
target_2: entry + 2.3R
exit_reason: retest continuation targets at 1.4R and 2.3R
```

### Gap-Fill Targets

```text
exit_model: gap_fill_targets
target_1: entry + 1.35R
target_2: entry + 2.0R
exit_reason: gap-fill targets at 1.35R and 2.0R
```

### Scanner-Provided Targets

```text
exit_model: scanner_provided_targets
exit_reason: scanner provided target levels validated above entry
```

Scanner-provided targets are only accepted when:

```text
target_1 > entry_trigger
target_2 > target_1 when target_2 exists
```

---

## Failure Behavior

If exit/target quality fails during signal generation:

```text
BUY_WATCH -> NO_TRADE
notes include exit_quality reasons
trade plan validation also records invalid or missing levels when applicable
```

This prevents inverted or invalid targets from becoming actionable watcher signals.

---

## Example Failure Reasons

```text
missing_entry_trigger
missing_stop_loss
stop_loss_not_below_entry
invalid_risk_per_share
target_1_not_above_entry
target_2_not_above_target_1
```

---

## Design Rules

- Every actionable signal must have `target_1`, `exit_model` and `exit_reason`.
- `target_2` is optional but must be above `target_1` when present.
- Targets for long signals must be above entry.
- Target derivation must be deterministic.
- Scanner-provided targets must be validated before use.
- Exit failure reasons must be visible in signal notes.
- Trade Plan Validator remains the final executable gate.

---

## Next Steps

The Exit / Target Quality Engine is deterministic first. Next improvements should add richer exit management:

```text
partial exit policy after target_1
runner policy after target_2
trailing-stop logic after target_1
time-stop / expiry outcome analysis
exit-quality feedback from historical outcomes
```
