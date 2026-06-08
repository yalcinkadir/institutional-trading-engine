# Institutional Trading Engine Roadmap

Status date: 2026-06-07

Current state: TEST1 Evidence-Oriented TDD Policy is active. EV1-EV12 evidence-integrity remediation is implemented and CI-green. CI runtime simplification is implemented and CI-green. PO128 and PO129 silent-failure/dataflow guards are implemented and CI-green. W1 Entry/Exit Watcher Git-Write Decoupling is implemented and CI-green. P132 Scanner Runtime Boundary is implemented and CI-green. BT130 Real Historical Backtest Evidence Pack Gate is implemented and CI-pending. PortfolioState fail-closed fixture migration (#102) is validated and closed.

The system remains research / decision-support / paper-observation only. Real-money execution is not authorized by code.

## Hard Rules

No real-money execution before forward evidence, drift detection, regime-change monitoring, position-level risk attribution, capacity/turnover realism, runtime governance hardening and manual approval are in place.

Safety-relevant fixes and external review findings require a guard test first.

Committed public report examples must remain synthetic/public-safe.

No real-data backtest claim without a complete, validated evidence pack.

Scheduled runtime workflows must not mutate the main branch with generated artifacts. Runtime evidence belongs in CI artifacts, retention indexes or explicitly governed evidence stores.

Static Paper Observation watchlists must be labelled with `selection_mode=static_watchlist` and must not be represented as dynamic scanner evidence or trading-edge proof.

## Phase BT — Backtesting Evidence Gates

| ID | Task | Priority | Impact | Status |
|---|---|---:|---:|---|
| BT130 | Real Historical Backtest Evidence Pack Gate | P1 | High | Implemented / CI-pending |

BT130 requires real-data backtest evidence packs to include run identity, real-data source declaration, `is_demo=false`, symbol universe, date range, strategy version, input-pack gate status, coverage manifest path, survivorship universe path, trade-plan path, plan input/accepted/rejected counts, rejection reasons, metrics, results, and paper-only execution boundaries.

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

## Phase P132 — Scanner Runtime Boundary

| ID | Task | Priority | Impact | Status |
|---|---|---:|---:|---|
| P132 | Scanner Runtime Boundary: Static Watchlist vs Real Screener | P1 | High | Done / CI-green |

P132 requires runtime reports and Paper Observation evidence to expose `selection_mode`, selected symbols and selection reason. Static watchlists are allowed as research setup only and must not claim dynamic scanner breadth or trading-edge proof. Dynamic scanner claims require a documented scanner contract reference.

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
| W1 | Entry/Exit Watcher Git-Write Decoupling | P0 | Critical | Done / CI-green |
| RGP8 | Alert/evidence artifact upload-on-failure guard | P1 | High | Done / CI-green |
| RGP9 | Signal lifecycle status source of truth | P2 | Medium | Done / CI-green |
| RGP10 | Latest bar timestamp ordering guard | P2 | Medium | Done / CI-green |
| RGP11 | Signal identity float quantization | P2 | Medium | Done / CI-green |
| RGP12 | Partial-exit lifecycle persistence | P2 | Medium | Done / CI-green |
| RGP13 | Runtime Proof Pack Summary Builder | P1 | High | Done / CI-green |

W1 keeps scheduled watcher runtime output out of the repository. The Entry/Exit Watcher workflow uses read-only contents permission, non-persistent checkout credentials, isolated watcher concurrency and `actions/upload-artifact@v4` for runtime evidence.

## Phase FCM/RPW — Connectivity and Proof-Pack Retention

| ID | Task | Priority | Impact | Status |
|---|---|---:|---:|---|
| FCM1 | Feature Connectivity Matrix Guard | P1 | High | Done / CI-wired |
| RPW1 | Runtime Proof-Pack Artifact Writer / Retention Index | P1 | High | Done / CI-wired |

FCM1 requires implemented / CI-green features to declare runtime gates, guard tests, evidence artifacts, documentation references, upstream dependencies and downstream consumers. Unknown dependencies, missing guard tests, missing artifacts and unsafe live/non-paper boundaries block the matrix.

RPW1 writes deterministic runtime proof-pack JSON artifacts and maintains a retention index with artifact identity, SHA-256 hash, observation window, retention days and the paper-only safety boundary.

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

## Closed Remediation Items

- #102: PortfolioState fail-closed fixture migration validated and closed. Runtime remains fail-closed for missing or non-boolean `governance_valid`; test fixtures that need a valid state set `governance_valid=true`; committed default `data/portfolio_state.json` remains `governance_valid=false` until real paper/broker state exists.
- #132: Scanner Runtime Boundary validated and closed. Runtime reports and Paper Observation evidence must expose `selection_mode`; static watchlists remain research setup only and cannot claim dynamic scanner breadth or trading-edge proof.

## Recommended Next Remediation Order

1. Validate JWT fail-closed migration (#103)
2. Close FCM1/RPW1 CI-wired backlog status (#104)
3. Architecture reachability + runtime execution guard (#106)

## Safety Boundary

This roadmap does not authorize live trading, broker execution, capital allocation or production deployment.

The system remains research / decision-support / paper-observation only.
