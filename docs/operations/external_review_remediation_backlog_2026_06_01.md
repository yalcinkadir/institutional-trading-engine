# External Review Remediation Backlog — 2026-06-01

Status: remediation backlog active  
Last updated: 2026-06-02  
Source: external code review of the Institutional Trading Engine core trading, risk, backtesting, evidence and persistence paths.

## Purpose

This document preserves all relevant findings from the external review so they cannot slip through the cracks.

Each finding must be reconciled against the current codebase before being marked done.

## Status Vocabulary

```text
OPEN
IN_PROGRESS
IMPLEMENTED_PENDING_CI
LIKELY_CLOSED_BY_EXISTING_WORK_NEEDS_VERIFICATION
CLOSED_CI_GREEN
WONT_FIX_DOCUMENTED
```

## Severity Vocabulary

```text
P0 Critical
P1 High
P2 Medium
```

## Safety Boundary

```text
Live trading authorization: not granted by code
Broker execution: paper_only unless explicitly stated otherwise
This backlog does not authorize live trading, broker execution or capital allocation
```

## Summary Table

| ID | Severity | Area | Finding | Status | Notes |
|---|---:|---|---|---|---|
| ER1 | P0 | Backtest realism | Optimistic T1 expiry booking in `t1_t2` model books full T1 even when trade expires after T1 without T2 | CLOSED_CI_GREEN | Guarded by `tests/test_er1_er2_backtest_realism_guard.py` |
| ER2 | P0 | Backtest realism | Entry fills ignore gap-through-entry while stop fills model gaps pessimistically | CLOSED_CI_GREEN | Guarded by `tests/test_er1_er2_backtest_realism_guard.py` |
| ER3 | P0 | Position sizing | Position sizing lacked notional / buying-power cap | CLOSED_CI_GREEN | Fixed in `src/trading/risk_engine.py` |
| ER4 | P0 | Persistence / audit integrity | State and evidence writes are not consistently atomic | CLOSED_CI_GREEN | Guarded by `tests/test_er4_atomic_persistence_guard.py` |
| ER5 | P1 | Outcome metrics | Falsy-zero bug can replace true `0.0` result with alternate metric | CLOSED_CI_GREEN | Guarded by `tests/test_er5_expectancy_zero_result_guard.py` |
| ER6 | P1 | Evidence quality | Missing result keys may be silently counted as `0.0` breakeven trades | CLOSED_CI_GREEN | Guarded by `tests/test_er6_edge_evidence_missing_result_guard.py` |
| ER7 | P1 | Sizing governance | `MIN_SAMPLES = 5` for automatic size adjustment is statistically weak | CLOSED_CI_GREEN | Guarded by `tests/test_er7_er8_expectancy_statistical_discipline.py` |
| ER8 | P1 | Expectancy logic | Isolated win-rate gate can block positive-asymmetry profiles despite positive expectancy | CLOSED_CI_GREEN | Guarded by `tests/test_er7_er8_expectancy_statistical_discipline.py` |
| ER9 | P1 | Portfolio risk | Portfolio-risk warnings reduce all tradable symbols globally instead of targeted pair/sector reduction | CLOSED_CI_GREEN | Guarded by `tests/test_er9_targeted_portfolio_risk_reduction.py` |
| ER10 | P1 | OOS methodology | No purge/embargo around OOS split while trades can overlap boundary | CLOSED_CI_GREEN | Guarded by `tests/test_er10_oos_purge_embargo_guard.py` |
| ER11 | P2 | Metric semantics | Two different expectancy definitions use similar naming but different units / denominators | CLOSED_CI_GREEN | Standardized to `expectancy_r` |
| ER12 | P2 | Sharpe evidence | Per-trade Sharpe uses population std and IID-style t-stat assumption | LIKELY_CLOSED_BY_EXISTING_WORK_NEEDS_VERIFICATION | EV1/EV2 addressed unit issue; verify caveats |
| ER13 | P2 | Accounting precision | Money/PnL paths use float rather than Decimal | OPEN | Consider Decimal/integer cents at ledger boundaries |
| ER14 | P2 | Stop quality | Long-only stop logic lacks explicit short guard | CLOSED_CI_GREEN | Guarded by `tests/test_er14_er15_stop_loss_quality_guard.py` |
| ER15 | P2 | Stop quality | ATR fallback stops may lack max-distance cap comparable to swing stop cap | CLOSED_CI_GREEN | Guarded by `tests/test_er14_er15_stop_loss_quality_guard.py` |

---

## ER14 / ER15 — Stop-Loss Quality Guards

External findings:

```text
ER14: Long-only stop logic lacks explicit short guard.
ER15: ATR fallback stops may lack max-distance cap comparable to swing stop cap.
```

Implemented remediation:

```text
Unsupported short-side stop derivation fails closed with unsupported_side:<side>.
Scanner-provided stops exceeding MAX_ATR_STOP_DISTANCE fail closed.
ATR fallback stops use MAX_ATR_STOP_DISTANCE = 2.0.
Valid scanner-provided stop reason remains backward compatible.
```

Files:

```text
src/signals/stop_loss_quality.py
tests/test_er14_er15_stop_loss_quality_guard.py
tests/test_stop_loss_quality.py
```

Closure doc:

```text
docs/operations/er14_er15_stop_loss_quality_ci_green_closure_2026_06_02.md
```

Status:

```text
CLOSED_CI_GREEN
```

---

## Recommended Remediation Order

```text
1. ER12 / ER13 — evidence caveats and accounting precision review
```

## Next Action

Continue with:

```text
ER12 / ER13 — evidence caveats and accounting precision review
```
