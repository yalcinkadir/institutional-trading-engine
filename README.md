# Institutional Trading Engine

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![CI](https://img.shields.io/badge/CI-pytest-brightgreen.svg)
![Status](https://img.shields.io/badge/status-research--evidence--platform-orange.svg)

Institutional Trading Engine is a research, market-intelligence, screening, reporting, backtesting, evidence-validation and decision-support platform.

The system is designed for research and paper-observation evidence collection. It does **not** place live trades and does **not** authorize real-money execution.

## Current Validation Status

```text
TEST1: Evidence-Oriented TDD Policy active

Paper Observation:
PO1: Paper Observation timeline and review gate implemented and CI-green
PO2: Daily Observation Acceptance Gate implemented and CI-green
PO3: Daily Observation Run Record implemented and CI-green
PO4: Daily Observation Record Validator implemented and CI-green
PO5: Daily Observation Record Writer implemented and CI-green
PO6: Daily Observation Record Artifact Contract implemented and CI-green
PO7: Daily Observation Record Index implemented and CI-green
PO8: Daily Observation Review Summary implemented and CI-green
PO9: Paper Observation Review Gate implemented and CI-green
PO10: Daily Observation Automation Runner implemented and CI-green
PO11: Scheduled Daily Observation Workflow implemented and CI-green
PO12: Daily Observation Artifact Retention & Review Index implemented and CI-green
PO13: Monthly Paper Observation Review Pack implemented and CI-green

Runtime Governance:
GOV1-GOV10: runtime / pre-live governance hardening implemented and CI-green
SR1-SR8: signal identity, ATR persistence, repo-write serialization, governance source enforcement, anomaly-state governance, threshold source of truth, completed-bar watcher semantics and dependency reproducibility implemented and CI-green
PSR1-PSR4: runtime evidence manifest, fill-quality evidence and drift/regime evidence linkage implemented and CI-green
RGP1-RGP12: runtime governance proof pack implemented and CI-green

Backtesting / Evidence:
BT2: Strategy Test Matrix implemented
BT3: Backtest reproducibility contract implemented
BT5: Walk-Forward / Out-of-Sample Robustness Gate implemented and CI-green
BT6: Evidence Baseline Regression Gate implemented and CI-green
BT7: Capacity / Turnover / Realism Gate implemented and CI-green
BT8: Backtesting Evidence Report generator implemented and CI-green
EV1-EV12: evidence-integrity remediation implemented and CI-green

External Review Remediation:
ER1: T1/T2 expiry realism guard implemented and CI-green
ER2: gap-through-entry and breakeven-gap realism guards implemented and CI-green
ER3: notional / buying-power capped position sizing implemented and CI-green
ER4: atomic persistence utility and PortfolioStateStore atomic save implemented and CI-green
ER5: falsy-zero outcome substitution guard implemented and CI-green
ER6: missing result evidence is surfaced instead of counted as breakeven and CI-green
ER7: expectancy-based adjustment sample discipline implemented and CI-green
ER8: positive asymmetric expectancy handling implemented and CI-green
ER9: targeted portfolio-risk reduction evidence implemented and CI-green
ER10: OOS purge / embargo lockbox guard implemented and CI-green
ER11: explicit expectancy_r unit naming implemented and CI-green
ER12: Sharpe caveats and small-sample/IID assumption disclosure implemented and CI-green
ER13: Decimal/cent-stable position-risk accounting implemented and CI-green
ER14: unsupported short-side stop guard implemented and CI-green
ER15: ATR max-distance stop quality guard implemented and CI-green

Repository / Public Safety:
IP1/IP2: public/private edge boundary and public repository hygiene policy implemented
IP3/IP4: public-demo defaults and optional external edge provider boundary implemented and CI-green
IP5/IP6: artifact hygiene and .gitignore hardening implemented / CI-wired
IP9/IP10: PR public-edge review governance, license and usage disclaimer implemented / CI-wired
Report Output Boundary Guard: protected public report artifacts implemented and CI-green

Live trading authorization: not granted by code
Broker execution: paper-only infrastructure; live execution is not implemented
```

Code quality is not trading edge. The system is promising enough to test seriously, but real capital still requires long-running forward evidence, drift detection, regime-change monitoring, position-level risk attribution, execution-quality review, capacity/turnover realism and manual approval.

## TEST1 Evidence-Oriented TDD Policy

TEST1 makes test-first development mandatory for safety-relevant fixes, external review findings and trading-risk logic.

```text
1. Guard test first
2. Minimal fix second
3. Targeted test third
4. Relevant module tests fourth
5. Full suite fifth
6. Documentation last
```

A fix is not complete unless a guard test captures the dangerous path, boundary case or fail-closed invariant.

Policy document:

```text
docs/operations/test1_evidence_oriented_tdd_policy.md
```

## External Review Remediation Status

### ER1 — T1/T2 Expiry Realism Guard

A `t1_t2` trade that touches Target 1 but never reaches Target 2 now expires at the final available close, not optimistically at Target 1.

Guard:

```text
tests/test_er1_er2_backtest_realism_guard.py
```

Status:

```text
CLOSED_CI_GREEN
```

### ER2 — Gap-Through-Entry and Breakeven Gap Guard

Gap-through-entry fills at the worse open price and recalculates R-multiple from the actual entry fill. Breakeven-after-T1 gap-down stops fill at the worse open, not artificially at exact breakeven.

Guard:

```text
tests/test_er1_er2_backtest_realism_guard.py
```

Status:

```text
CLOSED_CI_GREEN
```

### ER3 — Notional-Capped Position Sizing

`calculate_position_risk` supports optional `buying_power` and `max_notional` caps.

Status:

```text
CLOSED_CI_GREEN
```

### ER4 — Atomic Persistence Guard

A central atomic persistence helper protects governance/evidence writes from direct destination truncation and failed replacement scenarios.

Files:

```text
src/persistence/atomic_write.py
src/runtime/portfolio_state.py
tests/test_er4_atomic_persistence_guard.py
```

Status:

```text
CLOSED_CI_GREEN
```

### ER5 / ER6 / ER11 — Outcome and Expectancy Evidence Hygiene

True `0.0` outcomes are preserved, missing result evidence is surfaced instead of counted as breakeven, and ambiguous expectancy outputs are explicit as `expectancy_r`.

Guards:

```text
tests/test_er5_expectancy_zero_result_guard.py
tests/test_er6_edge_evidence_missing_result_guard.py
tests/test_er11_expectancy_units_guard.py
```

Status:

```text
CLOSED_CI_GREEN
```

### ER7 / ER8 — Expectancy Statistical Discipline

The expectancy adjuster separates score evidence from size evidence. Smaller samples may affect score, but the multiplier remains neutral until the stronger sample floor is met. Positive asymmetric expectancy is no longer blocked solely by low win rate.

Guard:

```text
tests/test_er7_er8_expectancy_statistical_discipline.py
```

Related tests:

```text
tests/test_expectancy_adjuster.py
```

Status:

```text
CLOSED_CI_GREEN
```

### ER9 — Targeted Portfolio-Risk Reduction Evidence

Portfolio-risk warnings now produce targeted evidence instead of reducing every tradable candidate by default.

The result exposes:

```text
symbol_risk_multipliers
```

Guard:

```text
tests/test_er9_targeted_portfolio_risk_reduction.py
```

Related tests:

```text
tests/test_portfolio_risk.py
```

Status:

```text
CLOSED_CI_GREEN
```

### ER10 — OOS Purge / Embargo Guard

The fixed-date holdout lockbox prevents train/test-boundary contamination from trades that overlap the OOS split or start inside the embargo window.

The report exposes:

```text
purge_days
embargo_days
purged_records
embargoed_records
```

Guard:

```text
tests/test_er10_oos_purge_embargo_guard.py
```

Related tests:

```text
tests/test_out_of_sample_lockbox.py
```

Status:

```text
CLOSED_CI_GREEN
```

### ER12 / ER13 — Evidence Caveats and Accounting Precision

Historical edge validation now exposes Sharpe caveats in JSON and Markdown, including population standard deviation, unverified IID assumptions, small-sample warnings and `not_proof_of_edge`. Position-risk accounting now uses Decimal at money boundaries and returns cent-stable outputs.

The report exposes:

```text
caveats.sharpe_std_method = population_std
caveats.iid_assumption = not_verified
caveats.small_sample_warning
caveats.not_proof_of_edge
```

Guard:

```text
tests/test_er12_er13_evidence_accounting_precision_guard.py
```

Related tests:

```text
tests/test_historical_edge_validation.py
tests/test_artifact_hygiene.py
```

Status:

```text
CLOSED_CI_GREEN
```

### ER14 / ER15 — Stop-Loss Quality Guards

The stop-loss quality engine explicitly rejects unsupported short-side stop derivation and enforces max ATR-distance quality checks for scanner-provided and ATR fallback stops.

The engine exposes:

```text
SUPPORTED_SIDE = "long"
MAX_ATR_STOP_DISTANCE = 2.0
```

Guard:

```text
tests/test_er14_er15_stop_loss_quality_guard.py
```

Related tests:

```text
tests/test_stop_loss_quality.py
```

Status:

```text
CLOSED_CI_GREEN
```

## Paper Observation Evidence Process

Paper Observation is a 3-6 month evidence collection process.

```text
Start date: 2026-06-01
Minimum duration: 3 months
Target duration: 3-6 months
First review date: 2026-07-01
Major evidence review date: 2026-09-01
Extended review date: 2026-12-01
Live trading authorization: not granted by code
```

Daily observation evidence is accepted only when required evidence families, generated reports, artifact references, research-only status and paper-only execution boundaries are valid.

Daily status vocabulary:

```text
ACCEPTED
REJECTED
NEEDS_REVIEW
```

## Core Commands

Targeted remediation tests:

```bash
pytest tests/test_er12_er13_evidence_accounting_precision_guard.py -q
pytest tests/test_historical_edge_validation.py -q
pytest tests/test_artifact_hygiene.py -q
pytest tests/test_er14_er15_stop_loss_quality_guard.py -q
pytest tests/test_stop_loss_quality.py -q
pytest tests/test_er10_oos_purge_embargo_guard.py -q
pytest tests/test_out_of_sample_lockbox.py -q
pytest tests/test_er9_targeted_portfolio_risk_reduction.py -q
pytest tests/test_portfolio_risk.py -q
pytest tests/test_er7_er8_expectancy_statistical_discipline.py -q
pytest tests/test_expectancy_adjuster.py -q
pytest tests/test_er4_atomic_persistence_guard.py -q
pytest tests/test_portfolio_state.py -q
pytest tests/test_er1_er2_backtest_realism_guard.py -q
pytest tests/test_historical_entry_exit_backtest.py -q
pytest tests/test_er5_expectancy_zero_result_guard.py -q
pytest tests/test_er6_edge_evidence_missing_result_guard.py -q
pytest tests/test_er11_expectancy_units_guard.py -q
pytest tests/test_edge_evidence_backtest.py -q
pytest tests/test_decision_report.py -q
```

Documentation/status guards:

```bash
pytest tests/test_ip9_ip10_public_repo_governance.py -q
pytest tests/test_post_rgp_status_consistency.py -q
pytest tests/test_roadmap_ev_completion_guard.py -q
```

Full test suite:

```bash
pytest -q
```

## Safety Boundary

This repository is a research and paper-observation framework.

It does not authorize:

```text
live trading
broker execution
capital allocation
production deployment
real-money execution
```

Any future live-execution discussion remains blocked until forward evidence, drift monitoring, risk attribution, execution-quality review, capacity/turnover realism, runtime governance hardening and manual approval are in place.
