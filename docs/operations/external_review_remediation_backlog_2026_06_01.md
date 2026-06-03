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
| ER12 | P2 | Sharpe evidence | Per-trade Sharpe uses population std and IID-style t-stat assumption | CLOSED_CI_GREEN | Guarded by `tests/test_er12_er13_evidence_accounting_precision_guard.py` |
| ER13 | P2 | Accounting precision | Money/PnL paths use float rather than Decimal | CLOSED_CI_GREEN | Guarded by `tests/test_er12_er13_evidence_accounting_precision_guard.py` |
| ER14 | P2 | Stop quality | Long-only stop logic lacks explicit short guard | CLOSED_CI_GREEN | Guarded by `tests/test_er14_er15_stop_loss_quality_guard.py` |
| ER15 | P2 | Stop quality | ATR fallback stops may lack max-distance cap comparable to swing stop cap | CLOSED_CI_GREEN | Guarded by `tests/test_er14_er15_stop_loss_quality_guard.py` |

---

## ER12 / ER13 — Evidence Caveats and Accounting Precision

External findings:

```text
ER12: Per-trade Sharpe uses population std and IID-style t-stat assumptions.
ER13: Money/PnL paths use float rather than Decimal.
```

Implemented remediation:

```text
Historical edge reports now expose explicit Sharpe caveats in JSON and Markdown.
The report states population_std, iid_assumption=not_verified, small_sample_warning and not_proof_of_edge.
Position-risk accounting uses Decimal at money boundaries with cent-stable outputs.
Public postmarket report example was restored to synthetic/public-safe content after the hygiene guard caught generated report leakage.
```

Files:

```text
src/validation/historical_edge_validation.py
src/trading/risk_engine.py
tests/test_er12_er13_evidence_accounting_precision_guard.py
reports/postmarket-report.md
```

Closure doc:

```text
docs/operations/er12_er13_evidence_accounting_precision_ci_green_closure_2026_06_02.md
```

Status:

```text
CLOSED_CI_GREEN
```

---

## Recommended Remediation Order

```text
1. External review remediation backlog is closed through ER15.
2. Continue with paper-observation hardening and forward-evidence review gates.
```

## Next Action

Continue with:

```text
Paper Observation / forward evidence quality gates
```
