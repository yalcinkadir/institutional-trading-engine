# Trade Plan Validator

The Trade Plan Validator is the first concrete implementation step of the Entry / Stop / Exit Decision Quality roadmap.

A high setup score is not enough. A `BUY_WATCH` signal must pass a complete executable trade-plan validation.

---

## Component

```text
src/signals/trade_plan_validator.py
```

Integrated into:

```text
src/signals/signal_generator.py
```

Tests:

```text
tests/test_trade_plan_validator.py
tests/test_signal_generator_identity.py
```

---

## Validation Result

The validator returns a structured result:

```text
TradePlanValidationResult
```

Fields:

```text
is_valid
reasons
risk_reward
risk_per_share
reward_per_share
stop_distance_atr
```

---

## Long Trade Plan Rules

For long-side `BUY_WATCH` signals, the validator checks:

```text
entry_trigger exists
stop_loss exists
target_1 exists
stop_loss < entry_trigger
target_1 > entry_trigger
target_2 > target_1 when target_2 exists
risk_reward >= configured minimum
stop distance is not too tight when ATR is available
stop distance is not too wide when ATR is available
```

---

## Failure Behavior

If validation fails during signal generation:

```text
BUY_WATCH → NO_TRADE
position_size → 0.0
notes include validation reasons
```

This prevents incomplete or invalid trade plans from reaching the watcher as fake actionable signals.

---

## Current Defaults

```text
minimum risk/reward: 1.2
minimum stop distance: 0.25 ATR
maximum stop distance: 4.0 ATR
```

These are conservative defaults and can later be moved into configuration.

---

## Example Failure Reasons

```text
missing_entry_trigger
missing_stop_loss
missing_target_1
stop_loss_not_below_entry
target_1_not_above_entry
target_2_not_above_target_1
invalid_risk_per_share
invalid_reward_per_share
risk_reward_below_minimum
stop_distance_too_tight
stop_distance_too_wide
```

---

## Design Rules

- `BUY_WATCH` only survives if the validator passes.
- Invalid plans must be downgraded, not silently emitted.
- Failure reasons must be persisted in signal notes.
- The watcher should receive only executable actionable signals.
- Tests must cover both valid and invalid trade-plan cases.

---

## Next Steps

The validator is the foundation. The next roadmap components should improve how levels are derived:

```text
P14.2 Entry Quality Engine
P14.3 Stop-Loss Quality Engine
P14.4 Exit / Target Quality Engine
P14.5 Entry/Stop/Exit Backtest Feedback
```
