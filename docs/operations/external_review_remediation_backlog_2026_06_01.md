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
| ER1 | P0 | Backtest realism | Optimistic T1 expiry booking in `t1_t2` model books full T1 even when trade expires after T1 without T2 | OPEN | Verify and fix if still present |
| ER2 | P0 | Backtest realism | Entry fills ignore gap-through-entry while stop fills model gaps pessimistically | OPEN | Add entry gap fill realism and breakeven gap handling |
| ER3 | P0 | Position sizing | Position sizing lacked notional / buying-power cap | CLOSED_CI_GREEN | Fixed in `src/trading/risk_engine.py` |
| ER4 | P0 | Persistence / audit integrity | State and evidence writes are not consistently atomic | OPEN | Standardize tmp + `os.replace` |
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

Expected remediation:

```text
If T1 was touched but T2 was not hit and no stop occurred before expiry, close remaining exposure at the final available close, not at target_1.
```

Status:

```text
OPEN
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

Expected remediation:

```text
When open gaps through entry, fill at worse open price for long entries. For breakeven-after-T1 gap below entry, avoid filling at exact breakeven if open is worse.
```

Status:

```text
OPEN
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

Expected remediation:

```text
Create shared atomic JSON write utility with tmp file, fsync where appropriate, and os.replace.
Use it for portfolio state, adjustment history, manual portfolio sync, outcome records and evidence files.
Consider backup-before-overwrite for critical single-source-of-truth files.
```

Status:

```text
OPEN
```

---

## ER5 — Falsy-Zero Result Bug

External finding:

```text
outcome.get("result_5d") or outcome.get("performance_percent") treats a true 0.0 as missing and swaps metric source.
```

Risk:

```text
Silent metric substitution and distorted expectancy profiles.
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

Relevant commits:

```text
419878b8a31b7de8cbac3c3afa085030d99fa59d
a7ad248b17d42cce4101503948f12cd1bb3b493e
8660b752e736513cd67d230364f7d6ec0358ba13
f5257df6485d3c835293b45e9a0a42c484186109
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

Risk:

```text
Data gaps become evidence, hiding missingness and distorting expectancy toward zero.
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

Relevant commits:

```text
5a931bda3edaec511f587c112d869bbe1cc3b9e8
0dfe9e8f13e9cf71856c6d07dfb9d87c44f60e7d
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

## ER8 — Win-Rate Gate Conflicts With Asymmetry

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

## ER9 — Global Portfolio-Risk Reduction

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

## ER10 — No Purge/Embargo Around OOS Split

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

## ER11 — Mixed Expectancy Units

External finding:

```text
Backtest expectancy and adjustment expectancy use different units and denominators while sharing similar naming.
```

Risk:

```text
Audit confusion and possible misuse across modules.
```

Implemented remediation:

```text
Renamed ambiguous expectancy adjustment fields to expectancy_r.
Decision report payloads now expose expectancy.expectancy_r.
expectancy_r means average R-multiple per evaluated trade/outcome profile.
```

Files:

```text
src/scoring/expectancy_adjuster.py
src/reporting/decision_report.py
tests/test_er11_expectancy_units_guard.py
tests/test_er5_expectancy_zero_result_guard.py
```

Relevant commits:

```text
bfad22fc357803c462b68f9e4dcf954242356e97
8a45637191913530f8ad4d78b6e6b1ca92b95b27
458e78a7b67c24450e90c8855eb04b6f302e485b
f5257df6485d3c835293b45e9a0a42c484186109
90951ccf1551da074ebe5e8fb42c19181e40907b
```

Status:

```text
CLOSED_CI_GREEN
```

---

## ER12 — Sharpe Assumptions and Small-Sample Handling

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

## ER13 — Float Money Accounting

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

## ER14 — Long-Only Stop Logic Lacks Short Guard

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

## ER15 — ATR Fallback Stop Max-Distance Cap

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

## Recommended Remediation Order

```text
1. ER1 / ER2 — backtest fill realism and T1 expiry logic
2. ER4 — atomic persistence for governance state and evidence files
3. ER7 / ER8 — expectancy adjuster statistical discipline
4. ER9 — targeted portfolio-risk reduction evidence
5. ER10 — OOS purge/embargo
6. ER14 / ER15 — stop-loss quality guards
7. ER12 / ER13 — evidence caveats and accounting precision review
```

## Next Action

Continue with:

```text
ER1 / ER2 — backtest realism
```

Rationale:

```text
These are P0 evidence-realism issues and directly affect historical expectancy, win-rate and R-multiple quality.
```
