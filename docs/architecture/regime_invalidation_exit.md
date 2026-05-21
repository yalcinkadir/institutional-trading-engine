# Regime Invalidation Exit

P20 adds deterministic regime invalidation for long-side signals.

P20B extends this behavior to pending actionable signals. If the broader market regime deteriorates into a defensive or risk-off state before entry, still-pending `BUY_WATCH` signals are cancelled instead of remaining watchable.

This does not execute broker orders. It updates signal state and emits lifecycle-compatible events.

---

## Components

```text
src/watchers/regime_invalidation.py
src/watchers/entry_exit_watcher.py
```

Tests:

```text
tests/test_regime_invalidation.py
tests/test_entry_exit_watcher.py
```

---

## Event

Regime invalidation emits:

```text
REGIME_INVALIDATION_EXIT
```

The terminal signal status becomes:

```text
CANCELLED_BY_REGIME_CHANGE
```

---

## Eligible Signals

Open long-side actionable signals are eligible:

```text
action = BUY_WATCH
status in {PENDING, TRIGGERED, TARGET_1_HIT}
```

Meaning:

```text
PENDING      -> setup is no longer watchable under risk-off regime
TRIGGERED    -> active signal is cancelled by regime deterioration
TARGET_1_HIT -> active runner is cancelled by regime deterioration
```

Ignored signals:

```text
NO_TRADE
STOP_HIT
TARGET_2_HIT
EXPIRED
CANCELLED_BY_REGIME_CHANGE
```

---

## Risk-Off / Defensive Labels

The helper recognizes defensive labels such as:

```text
risk_off
risk-off
risk off
bearish
defensive
capital_protection
capital protection
avoid_longs
avoid longs
```

Dictionary-style regime payloads are also supported:

```json
{"risk_state": "Risk-Off"}
{"regime": "Bearish"}
{"market_regime": "Defensive"}
```

---

## Signal State Update

When invalidated, the signal receives:

```text
status = CANCELLED_BY_REGIME_CHANGE
last_event_at = <timestamp>
regime_invalidation_at = <timestamp>
regime_invalidation_reason = <normalized regime label>
```

Example:

```json
{
  "status": "CANCELLED_BY_REGIME_CHANGE",
  "regime_invalidation_at": "2026-05-21T20:00:00Z",
  "regime_invalidation_reason": "risk off"
}
```

---

## Lifecycle Integration

`evaluate_regime_invalidation()` returns the same object types as other watcher events:

```text
WatcherAlert
SignalLifecycleUpdate
```

`evaluate_regime_invalidations()` evaluates a whole signal list and returns:

```text
alerts
lifecycle_updates
updated_signals
```

Lifecycle deduplication still uses:

```text
signal_id + event_type
```

---

## Design Rules

- No broker execution.
- No real order placement.
- Open actionable signals are invalidated.
- Pending actionable signals are cancelled before entry.
- Terminal signals are ignored.
- Non-actionable signals are ignored.
- Non-risk-off regimes do nothing.
- Regime invalidation is terminal.
- Duplicate lifecycle records are prevented by the existing lifecycle deduplication logic.

---

## Next Steps

Future improvements:

```text
wire regime invalidation into scheduled watcher/runtime run
add short-side invalidation rules
add notification-specific message templates
```
