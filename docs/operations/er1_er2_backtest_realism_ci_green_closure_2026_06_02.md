# ER1 / ER2 Backtest Realism CI-Green Closure — 2026-06-02

Status: closed / CI-green by user confirmation

## Scope

This closure records validated completion of:

```text
ER1 — Optimistic T1 expiry booking in backtest
ER2 — Entry fills ignore gap-through-entry
```

## TEST1 workflow evidence

The remediation followed TEST1 Evidence-Oriented TDD Policy:

```text
1. Guard test first
2. Minimal implementation or existing-behavior validation second
3. Targeted tests
4. Relevant module tests
5. CI confirmation
6. Documentation after green validation
```

## ER1 Finding

The external review identified that a `t1_t2` trade that touched Target 1 but never reached Target 2 could be booked too optimistically if expiry were recorded at Target 1 instead of the final available close.

## ER1 Validated behavior

The guard proves:

```text
If T1 is touched, T2 is not touched, no stop occurs and the trade expires,
the remaining exposure is closed at the final available close.
```

Expected outcome:

```text
outcome: EXPIRED
target_1_hit: true
target_2_hit: false
exit_price: final close
reason: expired_after_target_1_without_target_2
```

## ER2 Finding

The external review identified that entry fills could be too optimistic if a bar opened above the entry trigger and the backtest still filled at the trigger.

It also identified that a breakeven-after-T1 stop could be too optimistic if a gap-down after T1 were filled exactly at breakeven instead of the worse open.

## ER2 Validated behavior

The guard proves:

```text
Gap-through-entry fills at the worse open price.
R-multiple is recalculated from the actual entry fill.
Breakeven-after-T1 gap-down fills at the worse open, not at exact breakeven.
```

## Files

```text
src/backtesting/historical_entry_exit_backtest.py
tests/test_er1_er2_backtest_realism_guard.py
```

## Relevant commit

```text
c9db5bcea333323e7e2de7ae686eade07f319a4f
```

## CI confirmation

The user confirmed CI is green after the ER1/ER2 guard tests were added.

Recommended verification commands:

```bash
pytest tests/test_er1_er2_backtest_realism_guard.py -q
pytest tests/test_historical_entry_exit_backtest.py -q
pytest -q
```

## Safety boundary

This closure does not authorize live trading, broker execution, capital allocation or production deployment.

The system remains research / decision-support / paper-observation only.
