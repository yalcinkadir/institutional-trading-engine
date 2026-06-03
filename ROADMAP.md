# Institutional Trading Engine Roadmap

Status date: 2026-06-03

Current state: TEST1 Evidence-Oriented TDD Policy is active. EV1-EV12 evidence-integrity remediation is implemented and CI-green. CI runtime simplification is implemented and CI-green. ER1-ER15, PO14, RGP13, CER1 and PFA1 are implemented and CI-green.

The system remains research / decision-support / paper-observation only. Real-money execution is not authorized by code.

## Hard Rules

No real-money execution before forward evidence, drift detection, regime-change monitoring, position-level risk attribution, capacity/turnover realism, runtime governance hardening and manual approval are in place.

Safety-relevant fixes and external review findings require a guard test first.

Committed public report examples must remain synthetic/public-safe.

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

## Phase TEST — Evidence-Oriented Test Discipline

| ID | Task | Priority | Impact | Status |
|---|---|---:|---:|---|
| TEST1 | Evidence-Oriented TDD Policy | P0 | Critical | Active |

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
| PO14 | Forward Evidence Quality Gate | P0 | Critical | Done / CI-green |

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
| RGP13 | Runtime Proof Pack Summary Builder | P1 | High | Done / CI-green |

## Phase EV — Evidence Integrity Fixes

EV1-EV12 evidence-integrity remediation is complete and CI-green.

| ID | Task | Priority | Impact | Status |
|---|---|---:|---:|---|
| EV1 | Fix per-trade Sharpe semantics | P0 | Critical | Done / CI-green |
| EV2 | Ensure Deflated Sharpe receives per-trade Sharpe | P0 | Critical | Done / CI-green |
| EV3 | Enforce declared stop/exit model or fail closed | P0 | Critical | Done / CI-green |
| EV4 | Correct Target-1 partial-management outcome booking | P0 | High | Done / CI-green |
| EV5 | Model gap-through-stop fills pessimistically | P0 | High | Done / CI-green |
| EV6 | Fix Target-1-only exit date semantics | P1 | High | Done / CI-green |
| EV7 | Guard weak-evidence tiers | P1 | High | Done / CI-green |
| EV8 | Add evidence consolidation guard | P1 | High | Done / CI-green |
| EV9 | Add historical-edge validation guardrails | P1 | High | Done / CI-green |
| EV10 | Add report-output boundary guard | P1 | High | Done / CI-green |
| EV11 | Add full-suite flake review policy | P2 | Medium | Done / CI-green |
| EV12 | Add drawdown-magnitude evidence guard | P2 | Medium | Done / CI-green |

## Phase CER — Capacity / Execution Realism Evidence Review

| ID | Task | Priority | Impact | Status |
|---|---|---:|---:|---|
| CER1 | Capacity / Execution Realism Evidence Review Summary | P1 | High | Done / CI-green |

## Phase PFA — Position-level Forward Evidence Attribution

| ID | Task | Priority | Impact | Status |
|---|---|---:|---:|---|
| PFA1 | Position-level Forward Evidence Attribution | P1 | High | Done / CI-green |

PFA joins position-level risk attribution with forward outcome evidence. It does not authorize live trading.

## PFA1 Closure Summary

PFA1 Position-level Forward Evidence Attribution is implemented and CI-green.

Implemented behavior:
position risk attribution is joined with forward outcome records by symbol
risk contribution is exposed per position
1D, 5D, 20D, MFE and MAE forward outcomes are exposed per position
portfolio-level 1D, 5D and 20D forward outcome totals are summarized
missing outcome records block forward review
failed position-risk attribution reports block forward review
missing observation window blocks forward review
missing evidence manifest path blocks forward review
live_trading_authorized must remain false
broker_execution_mode must remain paper_only

Guard test:
tests/test_pfa1_position_forward_evidence_attribution.py

Closure doc:
docs/operations/pfa1_position_forward_evidence_attribution_ci_green_closure_2026_06_03.md

## Recommended Next Remediation Order

1. Runtime proof-pack artifact writer / retention index
2. Capacity / execution realism monthly aggregation
3. Position-level attribution trend review

## Safety Boundary

This roadmap does not authorize live trading, broker execution, capital allocation or production deployment.

The system remains research / decision-support / paper-observation only.
