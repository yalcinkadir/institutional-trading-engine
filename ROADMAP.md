# Institutional Trading Engine Roadmap

Status date: 2026-06-02

Current state: TEST1 Evidence-Oriented TDD Policy is active as the default workflow for safety-relevant fixes and external review findings. EV1-EV12 evidence-integrity remediation is implemented, centrally documented and CI-green. CI runtime simplification is implemented and CI-green. Paper Observation evidence collection is active. Runtime governance proofing, evidence integrity, report boundaries, public-repository governance and external-review remediation are being handled through guard-test-first development. ER1/ER2 backtest-realism guards are implemented and CI-green. ER4 atomic persistence guard is implemented and CI-green.

The system remains research / decision-support / paper-observation only. Real-money execution is not authorized by code.

## Strategic Direction

The next stage is not more scanner features. The next stage is institutional evidence, realistic execution assumptions, controlled public/private edge separation and mathematically correct decision hygiene.

Priorities:

```text
1. public framework / private edge separation
2. survivorship-safe data
3. statistically defensible edge validation
4. forward paper evidence
5. execution realism
6. capacity / turnover realism
7. portfolio-level risk attribution
8. core decision-logic regression gates
9. runtime governance hardening before any live consideration
10. public repository governance before new strategy complexity
11. multi-strategy expansion only after the base edge is proven
12. end-to-end runtime governance proof before expansion
13. deterministic daily observation acceptance records
14. deterministic review gates before Phase D or live-execution discussion
15. scheduled paper-observation automation
16. indexed artifact retention
17. monthly paper-observation review packs
18. test-first guard coverage for safety-relevant fixes
```

## Hard Rules

```text
Hard live-execution rule:
No real-money execution before forward evidence, drift detection, regime-change monitoring, position-level risk attribution, capacity/turnover realism, runtime governance hardening and manual approval are in place.

Hard IP rule:
The public repository may demonstrate architecture, evidence discipline and deterministic framework behavior, but proprietary edge configuration must not be developed further in public by default.

Hard logic rule:
Decision-critical math must be regression-tested before it is trusted by reports, ranking or paper execution workflows.

Hard artifact rule:
Committed public report examples must remain synthetic/public-safe. Generated runtime reports must be written only to non-committed output locations.

Hard evidence-integrity rule:
Metrics must use explicit units. Sharpe-like metrics, expectancy metrics, t-statistics and return percentages must not be mixed.

Hard TEST1 rule:
Safety-relevant fixes and external review findings require a guard test first. A green suite is not sufficient unless the dangerous path is explicitly covered.
```

## Phase TEST — Evidence-Oriented Test Discipline

| ID | Task | Priority | Impact | Status |
|---|---|---:|---:|---|
| TEST1 | Adopt Evidence-Oriented TDD Policy: guard test first, minimal fix second, targeted test, module tests, full suite, documentation last | P0 | Critical | Active |

TEST1 is mandatory for external-review findings and safety-relevant fixes.

## Phase IP — Public Repository Governance

| ID | Task | Priority | Impact | Status |
|---|---|---:|---:|---|
| IP1 | Define public/private edge separation boundary | P0 | Critical | Done / CI-green |
| IP2 | Add public repository hygiene policy | P0 | Critical | Done / CI-green |
| IP3 | Add public-demo defaults | P1 | High | Done / CI-green |
| IP4 | Add optional external edge provider boundary | P1 | High | Done / CI-green |
| IP5 | Add artifact hygiene controls | P1 | High | Done / CI-wired |
| IP6 | Harden `.gitignore` for generated evidence artifacts | P1 | High | Done / CI-wired |
| IP9 | Add PR public-edge review governance checklist | P1 | High | Done / CI-wired |
| IP10 | Add license and research-only usage disclaimer | P1 | High | Done / CI-wired |

IP9/IP10 preserve public-repository safety. They do not authorize live trading.

## Phase PO — Paper Observation Evidence Process

| ID | Task | Priority | Impact | Status |
|---|---|---:|---:|---|
| PO1 | Paper Observation timeline and review gate | P0 | Critical | Done / CI-green |
| PO2 | Daily Observation Acceptance Gate | P0 | Critical | Done / CI-green |
| PO3 | Daily Observation Run Record | P0 | Critical | Done / CI-green |
| PO4 | Daily Observation Record Validator | P0 | Critical | Done / CI-green |
| PO5 | Daily Observation Record Writer | P0 | Critical | Done / CI-green |
| PO6 | Daily Observation Record Artifact Contract | P0 | Critical | Done / CI-green |
| PO7 | Daily Observation Record Index | P0 | Critical | Done / CI-green |
| PO8 | Daily Observation Review Summary | P0 | Critical | Done / CI-green |
| PO9 | Paper Observation Review Gate | P0 | Critical | Done / CI-green |
| PO10 | Daily Observation Automation Runner | P0 | Critical | Done / CI-green |
| PO11 | Scheduled Daily Observation Workflow | P0 | Critical | Done / CI-green |
| PO12 | Daily Observation Artifact Retention & Review Index | P0 | Critical | Done / CI-green |
| PO13 | Monthly Paper Observation Review Pack | P0 | Critical | Done / CI-green |

PO status does not authorize live trading. It structures paper-observation evidence for future human review only.

## Phase RGP — Runtime Governance Proof Pack

| ID | Task | Priority | Impact | Status |
|---|---|---:|---:|---|
| RGP1 | Missing/invalid PortfolioState fail-closed proof | P0 | Critical | Done / CI-green |
| RGP2 | Runtime governance approval gate | P0 | Critical | Done / CI-green |
| RGP3 | Stale PortfolioState approval blocking | P0 | Critical | Done / CI-green |
| RGP4 | Actionable signal provider-fetch failure blocking | P0 | Critical | Done / CI-green |
| RGP5 | Critical STOP/EXIT alert ordering guard | P0 | Critical | Done / CI-green |
| RGP6 | Strict critical notification failure handling | P1 | High | Done / CI-green |
| RGP7 | Repo-writing workflow serialization/retry guard | P1 | High | Done / CI-green |
| RGP8 | Alert/evidence artifact upload-on-failure guard | P1 | High | Done / CI-green |
| RGP9 | Signal lifecycle status source of truth | P2 | Medium | Done / CI-green |
| RGP10 | Latest bar timestamp ordering guard | P2 | Medium | Done / CI-green |
| RGP11 | Signal identity float quantization | P2 | Medium | Done / CI-green |
| RGP12 | Partial-exit lifecycle persistence | P2 | Medium | Done / CI-green |

RGP is an audit/proof phase. It does not authorize live execution.

## Phase EV — Evidence Integrity Fixes

EV1-EV12 evidence-integrity remediation is complete and CI-green.

| ID | Task | Priority | Impact | Status |
|---|---|---:|---:|---|
| EV1 | Fix `calculate_sharpe_ratio` so it returns per-trade Sharpe instead of a sample-size-scaled t-statistic | P0 | Critical | Done / CI-green |
| EV2 | Ensure Deflated Sharpe receives per-trade Sharpe and not the t-statistic | P0 | Critical | Done / CI-green |
| EV3 | Make historical backtest actually simulate declared `stop_model` / `exit_model` or fail closed | P0 | Critical | Done / CI-green |
| EV4 | Prevent full `-1R` booking after Target 1 when the declared stop model implies breakeven or partial management | P0 | High | Done / CI-green |
| EV5 | Model gap-through-stop fills pessimistically instead of always filling exactly at stop | P0 | High | Done / CI-green |
| EV6 | Fix Target-1-only `exit_date` so fixed-date holdout segmentation uses the actual hit date | P1 | High | Done / CI-green |
| EV7 | Prevent `tier_3` and other weak-evidence tiers from being treated as fully institutional evidence without appropriate guardrails | P1 | High | Done / CI-green |
| EV8 | Add evidence consolidation guard so generated evidence artifacts remain internally consistent and public-safe | P1 | High | Done / CI-green |
| EV9 | Add historical-edge validation guardrails for minimum evidence quality and fail-closed reporting | P1 | High | Done / CI-green |
| EV10 | Add report-output boundary guard so committed examples remain synthetic/public-safe and generated runtime reports stay outside committed output | P1 | High | Done / CI-green |
| EV11 | Add full-suite flake review policy so ignored or unstable tests are tracked instead of silently accepted | P2 | Medium | Done / CI-green |
| EV12 | Add drawdown-magnitude evidence guard so drawdown reporting is explicit and not confused with unrelated risk measures | P2 | Medium | Done / CI-green |

## External Review Remediation Backlog

| ID | Severity | Area | Finding | Status |
|---|---:|---|---|---|
| ER1 | P0 | Backtest realism | Optimistic T1 expiry booking in `t1_t2` model | CLOSED_CI_GREEN |
| ER2 | P0 | Backtest realism | Entry fills ignore gap-through-entry | CLOSED_CI_GREEN |
| ER3 | P0 | Position sizing | Position sizing lacked notional / buying-power cap | CLOSED_CI_GREEN |
| ER4 | P0 | Persistence / audit integrity | State/evidence writes not consistently atomic | CLOSED_CI_GREEN |
| ER5 | P1 | Outcome metrics | Falsy-zero bug can replace true `0.0` result | CLOSED_CI_GREEN |
| ER6 | P1 | Evidence quality | Missing result keys counted as `0.0` breakeven evidence | CLOSED_CI_GREEN |
| ER7 | P1 | Sizing governance | `MIN_SAMPLES = 5` too weak for automatic size adjustment | OPEN |
| ER8 | P1 | Expectancy logic | Isolated win-rate gate can block positive-asymmetry profiles | OPEN |
| ER9 | P1 | Portfolio risk | Portfolio-risk reduction too global | OPEN |
| ER10 | P1 | OOS methodology | No purge/embargo around OOS split | OPEN |
| ER11 | P2 | Metric semantics | Mixed expectancy naming / units | CLOSED_CI_GREEN |
| ER12 | P2 | Sharpe evidence | Small-sample / IID assumptions need verification | LIKELY_CLOSED_BY_EXISTING_WORK_NEEDS_VERIFICATION |
| ER13 | P2 | Accounting precision | Float money/PnL accounting | OPEN |
| ER14 | P2 | Stop quality | Long-only stop logic lacks explicit short guard | OPEN |
| ER15 | P2 | Stop quality | ATR fallback stop may lack max-distance cap | OPEN |

## ER1 / ER2 Closure Summary

ER1/ER2 backtest-realism remediation is implemented and CI-green.

Implemented behavior:

```text
T1/T2 expiry after Target 1 closes remaining exposure at final close
Gap-through-entry fills at worse open price
R-multiple is recalculated from actual entry fill
Breakeven-after-T1 gap-down fills at worse open, not exact breakeven
```

Guard test:

```text
tests/test_er1_er2_backtest_realism_guard.py
```

Closure doc:

```text
docs/operations/er1_er2_backtest_realism_ci_green_closure_2026_06_02.md
```

## ER4 Closure Summary

ER4 atomic persistence remediation is implemented and CI-green.

Implemented behavior:

```text
central write_text_atomic and write_json_atomic helpers introduced
atomic writes use temporary sibling files and os.replace
failed replace attempts preserve existing destination content
PortfolioStateStore.save uses the central atomic JSON writer
```

Guard test:

```text
tests/test_er4_atomic_persistence_guard.py
```

Closure doc:

```text
docs/operations/er4_atomic_persistence_ci_green_closure_2026_06_02.md
```

## ER5 / ER6 / ER11 Closure Summary

ER5/ER6/ER11 outcome/evidence metric remediation is implemented and CI-green.

Implemented behavior:

```text
true 0.0 outcome results are preserved
missing result evidence is surfaced explicitly as missing_result_count
missing results are excluded from win/loss/breakeven metrics
expectancy units are explicit as expectancy_r
decision report payloads expose expectancy.expectancy_r
```

Guard tests:

```text
tests/test_er5_expectancy_zero_result_guard.py
tests/test_er6_edge_evidence_missing_result_guard.py
tests/test_er11_expectancy_units_guard.py
```

Closure docs:

```text
docs/operations/er5_er6_ci_green_closure_2026_06_02.md
docs/operations/er11_ci_green_closure_2026_06_02.md
docs/operations/er5_er6_er11_documentation_update_2026_06_02.md
```

## Recommended Next Remediation Order

```text
1. ER7 / ER8 — expectancy adjuster statistical discipline
2. ER9 — targeted portfolio-risk reduction evidence
3. ER10 — OOS purge / embargo
4. ER14 / ER15 — stop-loss quality guards
5. ER12 / ER13 — evidence caveats and accounting precision review
```

## Safety Boundary

This roadmap does not authorize live trading, broker execution, capital allocation or production deployment.

The system remains research / decision-support / paper-observation only.
