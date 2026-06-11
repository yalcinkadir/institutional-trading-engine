# Institutional Trading Engine Roadmap

Status date: 2026-06-11

Current state: TEST1 Evidence-Oriented TDD Policy is active. EV1-EV12 evidence-integrity remediation is implemented and CI-green. CI runtime simplification is implemented and CI-green. PO128 and PO129 silent-failure/dataflow guards are implemented and CI-green. W1 Entry/Exit Watcher Git-Write Decoupling is implemented and CI-green. P132 Scanner Runtime Boundary is implemented and CI-green. P160 module classification baseline is completed. P161 Dataflow Contract Matrix is implemented and CI-green. P164 VIX/regime entitlement handling with volatility proxy fallback is implemented and CI-green. P166 productive daily Paper Observation evidence producer is implemented / CI-pending. #191 Scanner datafeed liveness gate is implemented / targeted guard tests documented. #192 Scheduled report liveness gate is implemented / targeted guard tests documented. BT130 Real Historical Backtest Evidence Pack Gate is implemented / CI-pending. #177 real-data backtest pipeline coupling is implemented / CI-green. #184 historical real-data input persistence is implemented / targeted guard tests documented. PortfolioState fail-closed fixture migration (#102), JWT fail-closed migration (#103), FCM1/RPW1 CI-wired backlog status (#104), runtime reachability guard (#178), Evidence Quality Gate (#188), and Logic Safety Governance (#189) are validated at documentation/test-guard level.

The system remains research / decision-support / paper-observation only. Real-money execution is not authorized by code.

## Hard Rules

No real-money execution before forward evidence, drift detection, regime-change monitoring, position-level risk attribution, capacity/turnover realism, runtime governance hardening and manual approval are in place.

Safety-relevant fixes and external review findings require a guard test first.

Committed public report examples must remain synthetic/public-safe.

No real-data backtest claim without a complete, validated evidence pack and persisted source inputs with checksums/manifests.

Scheduled runtime workflows must not mutate the main branch with generated artifacts unless an explicit evidence-persistence workflow owns that behavior and commits only reviewable, checksum-backed evidence inputs and reports.

Static Paper Observation watchlists must be labelled with `selection_mode=static_watchlist` and must not be represented as dynamic scanner evidence or trading-edge proof.

Unknown, degraded, blocked, failed, demo/stub/synthetic or missing-provenance states must not be promoted as full `PASS`, strategy validation, production-grade evidence or live-readiness.

Decision-critical modules must either be runtime-connected with an execution proof or explicitly classified as non-runtime research/quarantine/test/deprecated. Non-runtime modules must not be used for architecture maturity, strategy-validation or live-readiness claims.

Roadmap-stable, strategy-promotion, production-grade evidence, paper-confidence, backtesting-promotion, decision-stack-validation and live-readiness claims must pass the #188 Evidence Quality Gate first.

Paper Observation readiness requires fresh scheduled output and scanner datafeed liveness. A scheduled run with `DATAFEED_BLOCKED` is scheduled-but-blocked evidence, not productive observation.

Scheduled report readiness requires a non-empty dated report, non-empty latest report and, for market reports, non-empty signals plus paper-observation health evidence. Missing scheduled output is `BLOCKED` evidence, not a productive report cycle.

## Phase EV — Evidence Integrity Remediation

| ID | Task | Priority | Impact | Status |
|---|---|---:|---:|---|
| EV1 | Sharpe definition remediation | P0 | Critical | Done / CI-green |
| EV2 | Annualization consistency remediation | P0 | Critical | Done / CI-green |
| EV3 | Backtest execution timing fidelity | P0 | Critical | Done / CI-green |
| EV4 | Fees and slippage fidelity | P0 | Critical | Done / CI-green |
| EV5 | Split/dividend-adjusted price contract | P0 | Critical | Done / CI-green |
| EV6 | Survivorship and lookahead-bias guard | P0 | Critical | Done / CI-green |
| EV7 | Decision ranking determinism guard | P0 | Critical | Done / CI-green |
| EV8 | Fixed-date holdout semantics | P0 | Critical | Done / CI-green |
| EV9 | Full-suite flake review completion | P1 | High | Done / CI-green |
| EV10 | Profit-factor infinity handling | P0 | Critical | Done / CI-green |
| EV11 | Conservative setup scoring | P0 | Critical | Done / CI-green |
| EV12 | Drawdown magnitude semantics | P0 | Critical | Done / CI-green |

EV1-EV12 evidence-integrity remediation is tracked as completed only because the roadmap rows above are backed by targeted guard tests and the CI runtime simplification path. These rows are historical evidence-integrity status entries and do not authorize live trading, broker execution or capital allocation.

## Phase BT — Backtesting Evidence Gates

| ID | Task | Priority | Impact | Status |
|---|---|---:|---:|---|
| BT130 | Real Historical Backtest Evidence Pack Gate | P1 | High | Implemented / CI-pending |
| #184 | Persist historical real-data backtest inputs for auditability | P0 | Critical | Implemented / targeted guard tests documented |

BT130 requires real-data backtest evidence packs to include run identity, real-data source declaration, `is_demo=false`, symbol universe, date range, strategy version, input-pack gate status, coverage manifest path, survivorship universe path, trade-plan path, plan input/accepted/rejected counts, rejection reasons, metrics, results, and paper-only execution boundaries.

#184 requires successful real-data historical backtests to persist the source inputs needed to reproduce the run. Polygon bars must be stored as canonical CSV files under `data/historical/bars/1day/*.csv`; coverage manifests must include `symbols[].output_sha256`; BT9 must fail closed on missing or mismatched checksums; accepted evidence artifacts must include `input_checksums`; and the BT131 workflow must persist reports plus source inputs instead of relying only on transient GitHub Actions artifacts.

#184 guard tests:

- `tests/test_184_historical_input_persistence.py`
- `tests/test_bt9_real_historical_input_pack_gate.py`
- `tests/test_polygon_historical_ingestion.py`
- `tests/test_bt131_real_data_backtest_evidence_workflow.py`

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
| #178 | Decision-critical Runtime Reachability Guard | P0 | Critical | Implemented / targeted guard tests documented |
| #188 | Evidence Quality Gate before roadmap or strategy promotion | P0 | Critical | Implemented / targeted guard tests documented |
| #189 | Machine-checkable System Invariants and Logic Safety Governance | P0 | Critical | Implemented / targeted guard tests documented |

#178 defines a decision-critical runtime reachability registry at `docs/architecture/decision_critical_runtime_reachability.json`. It prevents decision-quality modules from being counted as active runtime architecture unless they have a runtime entry point and guard-test proof. `src/decision_confidence.py`, `src/data_quality_engine.py`, `src/event_risk_engine.py` and `src/liquidity_volatility_engine.py` are explicitly non-runtime research helpers until promoted with execution proof.

#178 guard test:

- `tests/test_runtime_reachability_guard_178.py`

#188 defines a cross-cutting Evidence Quality Gate at `docs/operations/evidence-quality-gate.md`. It blocks roadmap-stable, strategy-promotion, production-grade evidence, paper-confidence, backtesting-promotion, decision-stack-validation and live-readiness claims unless evidence quality, durability, runtime reachability, historical input reproducibility, report validation, empty/no-signal classification and VIX/regime provenance are proven.

#188 implementation and guard tests:

- `src/evidence_quality_gate.py`
- `scripts/evaluate_evidence_quality_gate.py`
- `tests/test_evidence_quality_gate_188.py`

#189 defines machine-checkable system invariants, logic-safety severity classes, forbidden state conversions, evidence-traceability minimums and PR checklist linkage. It complements #188 Evidence Quality Gate by preventing `DEGRADED`, `UNKNOWN`, `BLOCKED`, demo/stub or missing-provenance output from being promoted as full `PASS` evidence.

Governance documents:

- `docs/architecture/system-invariants.md`
- `docs/operations/logic-safety-governance.md`

Guard tests:

- `tests/test_system_invariants.py`
- `tests/test_logic_safety_state_matrix.py`
- `tests/test_evidence_traceability_contract.py`

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
| P166 | Productive daily Paper Observation evidence producer with VIX/regime provenance | P0 | Critical | Implemented / CI-pending |
| #191 | Restore Scanner datafeed liveness for Paper Observation | P0 | Critical | Implemented / targeted guard tests documented |
| #192 | Scheduled Report Liveness | P0 | Critical | Implemented / targeted guard tests documented |

P166 makes the scheduled PO11 workflow produce `reports/daily_evidence/<observation_date>.json` before PO11 validates it. The producer embeds selection mode, selected symbols, run-health status, data-quality status, paper-only safety boundary and VIX/regime provenance. Runtime evidence is uploaded as Actions artifacts and is not committed back to `main`.

#191 makes scanner datafeed liveness an explicit Paper Observation readiness gate. If all tracked symbols have missing/non-numeric `close` values, missing required bars, provider failures or unusable scanner metrics, the run is `DATAFEED_BLOCKED`. The active report path writes `reports/health/<date>-datafeed-liveness.json` and `reports/health/datafeed-liveness-latest.json`, propagates `datafeed_status` and `provider_failure_reason` into signal artifacts, and prevents blocked datafeed runs from being counted as productive observation cycles.

#192 makes scheduled report liveness explicit. The institutional reports workflow now writes `reports/scheduled_report_liveness/<date>-<type>-liveness.json` and `reports/scheduled_report_liveness/latest-scheduled-report-liveness.json`. Market reports are `PASSED` only when the dated report, latest report, latest signals payload and latest paper-observation health evidence are present and non-empty. Missing or empty scheduled output becomes `BLOCKED` evidence instead of an invisible green scheduled cycle.

#192 guard tests:

- `tests/test_192_scheduled_report_liveness.py`
- `tests/test_po11_scheduled_daily_observation_workflow.py`

## Phase P132 — Scanner Runtime Boundary

| ID | Task | Priority | Impact | Status |
|---|---|---:|---:|---|
| P132 | Scanner Runtime Boundary: Static Watchlist vs Real Screener | P1 | High | Done / CI-green |

P132 requires runtime reports and Paper Observation evidence to expose `selection_mode`, selected symbols and selection reason. Static watchlists are allowed as research setup only and must not claim dynamic scanner breadth or trading-edge proof. Dynamic scanner claims require a documented scanner contract reference.

## Phase P160/P161/P164 — Architecture, Dataflow & Regime Contracts

| ID | Task | Priority | Impact | Status |
|---|---|---:|---:|---|
| P160 | Classify unclassified legacy modules before expanding runtime scope | P1 | High | Done / CI-green |
| P161 | Dataflow Contract Matrix: Scanner → Signals → Quality → Validator → Watcher → Evidence | P1 | High | Done / CI-green |
| P164 | VIX/regime entitlement handling with volatility proxy fallback | P1 | High | Done / CI-green |

P161 defines required pipeline fields, canonical `atr14` naming, allowed `atr` boundary aliasing, runtime producer/consumer ownership and fail-closed behavior. Missing critical fields must become `BLOCKED_MISSING_INPUTS`, not silent `NO_TRADE_VALID` output.
