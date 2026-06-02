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
| ER7 | P1 | Sizing governance | `MIN_SAMPLES = 5` for automatic size adjustment is statistically weak | OPEN | Raise threshold or add confidence gate |
| ER8 | P1 | Expectancy logic | Isolated win-rate gate can block positive-asymmetry profiles despite positive expectancy | OPEN | Prefer expectancy + distribution evidence |
| ER9 | P1 | Portfolio risk | Portfolio-risk warnings reduce all tradable symbols globally instead of targeted pair/sector reduction | OPEN | Return per-symbol/sector multipliers |
| ER10 | P1 | OOS methodology | No purge/embargo around OOS split while trades can overlap boundary | OPEN | Add purge/embargo semantics |
| ER11 | P2 | Metric semantics | Two different expectancy definitions use similar naming but different units / denominators | CLOSED_CI_GREEN | Standardized to `expectancy_r` |
| ER12 | P2 | Sharpe evidence | Per-trade Sharpe uses population std and IID-style t-stat assumption | LIKELY_CLOSED_BY_EXISTING_WORK_NEEDS_VERIFICATION | EV1/EV2 addressed unit issue; verify caveats |
| ER13 | P2 | Accounting precision | Money/PnL paths use float rather than Decimal | OPEN | Consider Decimal/integer cents at ledger boundaries |
| ER14 | P2 | Stop quality | Long-only stop logic lacks explicit short guard | OPEN | Add reject/assert for unsupported short setups |
| ER15 | P2 | Stop quality | ATR fallback stops may lack max-distance cap comparable to swing stop cap | OPEN | Verify and cap if missing |

---

## ER1 — Optimistic T1 Expiry Booking in Backtest

External finding:

```text
In src/backtesting/historical_entry_exit_backtest.py, the t1_t2 model may book a trade that touched T1 but never hit T2 or stop as a full T1 winner at expiry.
```

Risk:

```text
Systematically inflated win rate and expectancy.
```

Validated remediation:

```text
If T1 was touched but T2 was not hit and no stop occurred before expiry, remaining exposure closes at the final available close, not at target_1.
```

Files:

```text
src/backtesting/historical_entry_exit_backtest.py
tests/test_er1_er2_backtest_realism_guard.py
```

Closure doc:

```text
docs/operations/er1_er2_backtest_realism_ci_green_closure_2026_06_02.md
```

Status:

```text
CLOSED_CI_GREEN
```

---

## ER2 — Entry Fills Ignore Gap-Through-Entry

External finding:

```text
Entry fill uses entry_trigger even when the bar opens above the trigger. Stop gaps are modeled pessimistically, entry gaps are not.
```

Risk:

```text
Understates entry price and risk for gap-up entries; makes R-multiple evidence too optimistic.
```

Validated remediation:

```text
When open gaps through entry, fill at worse open price for long entries.
For breakeven-after-T1 gap below entry, fill at the worse open rather than exact breakeven.
R-multiple is recalculated from the actual entry fill.
```

Files:

```text
src/backtesting/historical_entry_exit_backtest.py
tests/test_er1_er2_backtest_realism_guard.py
```

Closure doc:

```text
docs/operations/er1_er2_backtest_realism_ci_green_closure_2026_06_02.md
```

Status:

```text
CLOSED_CI_GREEN
```

---

## ER3 — Position Sizing Lacked Notional / Buying-Power Cap

External finding:

```text
calculate_position_risk capped risk amount but not notional exposure. Tight stops could create oversized notional exposure.
```

Implemented remediation:

```text
Added optional buying_power and max_notional caps.
Shares are now min(risk_based_shares, notional_capped_shares).
Returned fields now include notional and notional_cap.
```

Files:

```text
src/trading/risk_engine.py
tests/test_risk_engine_notional_cap.py
```

Status:

```text
CLOSED_CI_GREEN
```

---

## ER4 — Non-Atomic State and Evidence Writes

External finding:

```text
Several state/evidence files use direct write_text / file writes instead of tmp + atomic replace.
```

Risk:

```text
Crash or concurrent write can corrupt JSON state used as governance evidence.
```

Implemented remediation:

```text
Created central atomic persistence helper for text and JSON files.
Atomic writes use temporary sibling files and os.replace.
Existing destination files remain unchanged when replacement fails.
PortfolioStateStore.save uses the central atomic JSON writer.
```

Files:

```text
src/persistence/atomic_write.py
src/runtime/portfolio_state.py
tests/test_er4_atomic_persistence_guard.py
```

Closure doc:

```text
docs/operations/er4_atomic_persistence_ci_green_closure_2026_06_02.md
```

Status:

```text
CLOSED_CI_GREEN
```

---

## ER5 — Falsy-Zero Result Bug

External finding:

```text
outcome.get("result_5d") or outcome.get("performance_percent") treats a true 0.0 as missing and swaps metric source.
```

Implemented remediation:

```text
Use explicit field-presence checks.
Preserve valid zero values.
Treat flat 0.0R expectancy as neutral, not negative/blocking.
```

Files:

```text
src/scoring/expectancy_adjuster.py
tests/test_er5_expectancy_zero_result_guard.py
```

Status:

```text
CLOSED_CI_GREEN
```

---

## ER6 — Missing Result Keys Counted as Breakeven

External finding:

```text
Patterns like record.get("result_r") or 0.0 can convert missing data into breakeven trades.
```

Implemented remediation:

```text
Differentiate missing key, invalid value and true 0.0 result.
Missing result records are excluded from win/loss/breakeven metrics.
Missing result records are surfaced as missing_result_count.
True 0.0 values remain valid breakeven evidence.
```

Files:

```text
src/backtesting/edge_evidence_backtest.py
tests/test_er6_edge_evidence_missing_result_guard.py
```

Status:

```text
CLOSED_CI_GREEN
```

---

## ER7 — Automatic Sizing With Too Few Samples

External finding:

```text
MIN_SAMPLES = 5 is too low for automatic size adjustment.
```

Expected remediation:

```text
Raise minimum sample threshold or add confidence / bootstrap / recency-weighted gate before any real sizing impact.
```

Status:

```text
OPEN
```

---

## ER8 — Win-Rate Gate Conflicts With Asymmetry

External finding:

```text
An isolated low win-rate gate can block high-payoff positive expectancy profiles.
```

Expected remediation:

```text
Base blocking primarily on expectancy, profit factor, drawdown and distribution evidence rather than win rate alone.
```

Status:

```text
OPEN
```

---

## Recommended Remediation Order

```text
1. ER7 / ER8 — expectancy adjuster statistical discipline
2. ER9 — targeted portfolio-risk reduction evidence
3. ER10 — OOS purge/embargo
4. ER14 / ER15 — stop-loss quality guards
5. ER12 / ER13 — evidence caveats and accounting precision review
```

## Next Action

Continue with:

```text
ER7 / ER8 — expectancy adjuster statistical discipline
```

Rationale:

```text
ER7 and ER8 both affect score/risk adjustment quality and should be handled together because both live in expectancy-adjustment governance.
```
