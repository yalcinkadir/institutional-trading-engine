# External Review Remediation Backlog — 2026-06-01

Status: intake captured / remediation backlog active  
Source: external code review of the Institutional Trading Engine core trading, risk, backtesting, evidence and persistence paths.

## Purpose

This document preserves all relevant findings from the external review so they cannot slip through the cracks.

Each finding must be reconciled against the current codebase before being marked done.

Status vocabulary:

```text
OPEN
IN_PROGRESS
IMPLEMENTED_PENDING_CI
LIKELY_CLOSED_BY_EXISTING_WORK_NEEDS_VERIFICATION
CLOSED_CI_GREEN
WONT_FIX_DOCUMENTED
```

Severity vocabulary:

```text
P0 Critical
P1 High
P2 Medium
```

Safety boundary:

```text
Live trading authorization: not granted by code
Broker execution: paper_only unless explicitly stated otherwise
This backlog does not authorize live trading, broker execution or capital allocation
```

---

## Summary table

| ID | Severity | Area | Finding | Status | Notes |
|---|---:|---|---|---|---|
| ER1 | P0 | Backtest realism | Optimistic T1 expiry booking in `t1_t2` model books full T1 even when trade expires after T1 without T2 | OPEN | Verify current `src/backtesting/historical_entry_exit_backtest.py`; fix if still present |
| ER2 | P0 | Backtest realism | Entry fills ignore gap-through-entry while stop fills model gaps pessimistically | OPEN | Add entry gap fill realism and breakeven gap handling if still open |
| ER3 | P0 | Position sizing | Position sizing lacked notional / buying-power cap | IMPLEMENTED_PENDING_CI | Fixed in `src/trading/risk_engine.py`; guarded by `tests/test_risk_engine_notional_cap.py` |
| ER4 | P0 | Persistence / audit integrity | State and evidence writes are not consistently atomic | OPEN | Verify `portfolio_state.py`, `adjustment_history.py`, `manual_portfolio_sync.py`, `outcomes/*`; standardize tmp + `os.replace` |
| ER5 | P1 | Outcome metrics | Falsy-zero bug can replace true `0.0` result with alternate metric | OPEN | Check `src/scoring/expectancy_adjuster.py` and related outcome consumers |
| ER6 | P1 | Evidence quality | Missing result keys may be silently counted as `0.0` breakeven trades | OPEN | Check `edge_evidence_backtest.py` and any `record.get(... ) or 0.0` evidence paths |
| ER7 | P1 | Sizing governance | `MIN_SAMPLES = 5` for automatic size adjustment is statistically weak | OPEN | Raise threshold or gate with confidence / bootstrap evidence before real sizing impact |
| ER8 | P1 | Expectancy logic | Isolated win-rate gate can block positive-asymmetry profiles despite positive expectancy | OPEN | Reconcile with asymmetry philosophy; prefer expectancy + profit factor / distribution evidence |
| ER9 | P1 | Portfolio risk | Portfolio-risk warnings reduce all tradable symbols globally instead of targeted pair/sector reduction | OPEN | Verify current `src/portfolio_risk.py`; improve targeted reduction and expose multiplier |
| ER10 | P1 | OOS methodology | No purge/embargo around OOS split while trades can overlap boundary | OPEN | Add purge/embargo semantics to `src/backtesting/out_of_sample_validation.py` if not already handled elsewhere |
| ER11 | P2 | Metric semantics | Two different expectancy definitions use similar naming but different units / denominators | OPEN | Standardize names such as `expectancy_r` and `expectancy_pct` |
| ER12 | P2 | Sharpe evidence | Per-trade Sharpe uses population std and IID-style t-stat assumption | LIKELY_CLOSED_BY_EXISTING_WORK_NEEDS_VERIFICATION | EV1/EV2 addressed Sharpe unit issue; verify small-sample/std/IID caveats remain documented and gated |
| ER13 | P2 | Accounting precision | Money/PnL paths use float rather than Decimal | OPEN | Consider Decimal at ledger/equity aggregation boundaries |
| ER14 | P2 | Stop quality | Long-only stop logic lacks explicit short guard | OPEN | Add reject/assert for short setups if shorts remain unsupported |
| ER15 | P2 | Stop quality | ATR fallback stops may lack max-distance cap comparable to swing stop cap | OPEN | Verify `src/signals/stop_loss_quality.py`; add cap if missing |

---

## ER1 — Optimistic T1 expiry booking in backtest

External finding:

```text
In `src/backtesting/historical_entry_exit_backtest.py`, the `t1_t2` model books a trade that touched T1 but never hit T2 or stop as a full T1 winner at expiry.
```

Risk:

```text
Systematically inflated win rate and expectancy.
```

Expected remediation:

```text
If T1 was touched but T2 was not hit and no stop occurred before expiry, close remaining exposure at the final available close, not at target_1.
```

Status:

```text
OPEN
```

---

## ER2 — Entry fills ignore gap-through-entry

External finding:

```text
Entry fill uses `entry_trigger` even when the bar opens above the trigger. Stop gaps are modeled pessimistically, entry gaps are not.
```

Risk:

```text
Understates entry price and risk for gap-up entries; makes R-multiple evidence too optimistic.
```

Expected remediation:

```text
When open gaps through entry, fill at worse open price for long entries. For breakeven-after-T1 gap below entry, avoid filling at exact breakeven if open is worse.
```

Status:

```text
OPEN
```

---

## ER3 — Position sizing lacked notional / buying-power cap

External finding:

```text
`calculate_position_risk` capped risk amount but not notional exposure. Tight stops could create oversized notional exposure.
```

Implemented remediation:

```text
Added optional `buying_power` and `max_notional` caps.
Shares are now min(risk_based_shares, notional_capped_shares).
Returned fields now include `notional` and `notional_cap`.
```

Files:

```text
src/trading/risk_engine.py
tests/test_risk_engine_notional_cap.py
```

Status:

```text
IMPLEMENTED_PENDING_CI
```

Required validation:

```bash
pytest tests/test_risk_engine_notional_cap.py -q
pytest -q
```

---

## ER4 — Non-atomic state and evidence writes

External finding:

```text
Several state/evidence files use direct `write_text` / file writes instead of tmp + atomic replace.
```

Risk:

```text
Crash or concurrent write can corrupt JSON state used as governance evidence.
```

Expected remediation:

```text
Create shared atomic JSON write utility with tmp file, fsync where appropriate, and `os.replace`.
Use it for portfolio state, adjustment history, manual portfolio sync, outcome records and evidence files.
Consider backup-before-overwrite for critical single-source-of-truth files.
```

Status:

```text
OPEN
```

---

## ER5 — Falsy-zero result bug

External finding:

```text
`outcome.get("result_5d") or outcome.get("performance_percent")` treats a true `0.0` as missing and swaps metric source.
```

Risk:

```text
Silent metric substitution and distorted expectancy profiles.
```

Expected remediation:

```text
Use explicit None checks. Preserve valid zero values.
```

Status:

```text
OPEN
```

---

## ER6 — Missing result keys counted as breakeven

External finding:

```text
Patterns like `record.get("result_r") or 0.0` can convert missing data into breakeven trades.
```

Risk:

```text
Data gaps become evidence, hiding missingness and distorting expectancy toward zero.
```

Expected remediation:

```text
Differentiate missing key, invalid value and true 0.0 result. Surface missing data as evidence error or excluded record with explicit count.
```

Status:

```text
OPEN
```

---

## ER7 — Automatic sizing with too few samples

External finding:

```text
`MIN_SAMPLES = 5` is too low for automatic size adjustment.
```

Risk:

```text
Noise-driven size increases or reductions.
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

## ER8 — Win-rate gate conflicts with asymmetry

External finding:

```text
An isolated low win-rate gate can block high-payoff positive expectancy profiles.
```

Risk:

```text
Contradicts asymmetry-focused strategy logic and may reject desirable profiles.
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

## ER9 — Global portfolio-risk reduction

External finding:

```text
One correlation or sector warning reduces all tradable symbols globally and returns only symbols, not actual reduced multipliers.
```

Risk:

```text
Over-broad risk response; unclear whether actual sizing is reduced downstream.
```

Expected remediation:

```text
Make reduction targeted to the causing pair/sector or return per-symbol risk multiplier evidence.
```

Status:

```text
OPEN
```

---

## ER10 — No purge/embargo around OOS split

External finding:

```text
In-sample signals close to split date can resolve into OOS period when max holding period is multiple bars.
```

Risk:

```text
Boundary leakage in OOS evidence.
```

Expected remediation:

```text
Add purge/embargo window around split date, parameterized by max holding bars or explicit embargo days.
```

Status:

```text
OPEN
```

---

## ER11 — Mixed expectancy units

External finding:

```text
Backtest expectancy and adjustment expectancy use different units and denominators while sharing similar naming.
```

Risk:

```text
Audit confusion and possible misuse across modules.
```

Expected remediation:

```text
Use explicit field names: `expectancy_r`, `expectancy_pct`, `mean_return_pct`, etc.
```

Status:

```text
OPEN
```

---

## ER12 — Sharpe assumptions and small-sample handling

External finding:

```text
Sharpe evidence uses per-trade std and IID-style significance assumptions.
```

Existing context:

```text
EV1/EV2 already addressed the per-trade Sharpe vs t-stat / Deflated Sharpe unit issue.
```

Expected verification:

```text
Confirm remaining std/IID/small-sample caveats are documented and not overstated by gates.
```

Status:

```text
LIKELY_CLOSED_BY_EXISTING_WORK_NEEDS_VERIFICATION
```

---

## ER13 — Float money accounting

External finding:

```text
PnL/equity paths use float broadly.
```

Risk:

```text
Rounding drift in audit / aggregation paths.
```

Expected remediation:

```text
Consider Decimal or integer cents at ledger/equity aggregation boundaries.
```

Status:

```text
OPEN
```

---

## ER14 — Long-only stop logic lacks short guard

External finding:

```text
Stop-loss quality logic is long-side but may not explicitly reject short setups.
```

Risk:

```text
Future short support could silently get invalid stop placement.
```

Expected remediation:

```text
Add explicit guard/reject for unsupported short direction.
```

Status:

```text
OPEN
```

---

## ER15 — ATR fallback stop max-distance cap

External finding:

```text
ATR fallback stops may not have the same max-distance cap as swing stop logic.
```

Risk:

```text
Unexpectedly wide stops can distort sizing and risk acceptance.
```

Expected remediation:

```text
Add or verify max ATR-distance cap for fallback stops.
```

Status:

```text
OPEN
```

---

## Recommended remediation order

```text
1. ER3 — notional-capped position sizing: confirm CI green, then document as RISK1.
2. ER1/ER2 — backtest fill realism and T1 expiry logic.
3. ER4 — atomic persistence for governance state and evidence files.
4. ER5/ER6/ER11 — outcome/evidence metric correctness and explicit units.
5. ER7/ER8 — expectancy adjuster statistical discipline.
6. ER9 — targeted portfolio-risk reduction evidence.
7. ER10 — OOS purge/embargo.
8. ER14/ER15 — stop-loss quality guards.
9. ER12/ER13 — evidence caveats and accounting precision review.
```

## Next action

After CI confirms ER3, document it as:

```text
RISK1 — Notional-Capped Position Sizing
```

Then continue with ER1/ER2 as the next P0 backtest-realism remediation.
