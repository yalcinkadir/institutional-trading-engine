# Institutional Trading Engine Roadmap

Status date: 2026-06-11

Current state: TEST1 Evidence-Oriented TDD Policy is active. EV1-EV12 evidence-integrity remediation is implemented and CI-green. CI runtime simplification is implemented and CI-green. PO128 and PO129 silent-failure/dataflow guards are implemented and CI-green. W1 Entry/Exit Watcher Git-Write Decoupling is implemented and CI-green. P132 Scanner Runtime Boundary is implemented and CI-green. P160 module classification baseline is completed. P161 Dataflow Contract Matrix is implemented and CI-green. P164 VIX/regime entitlement handling with volatility proxy fallback is implemented and CI-green. P166 productive daily Paper Observation evidence producer is implemented / CI-pending. #191 Scanner datafeed liveness gate is implemented / targeted guard tests documented. BT130 Real Historical Backtest Evidence Pack Gate is implemented / CI-pending. #177 real-data backtest pipeline coupling is implemented / CI-green. #184 historical real-data input persistence is implemented / targeted guard tests documented. PortfolioState fail-closed fixture migration (#102), JWT fail-closed migration (#103), FCM1/RPW1 CI-wired backlog status (#104), runtime reachability guard (#178), Evidence Quality Gate (#188), and Logic Safety Governance (#189) are validated at documentation/test-guard level.

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

P166 makes the scheduled PO11 workflow produce `reports/daily_evidence/<observation_date>.json` before PO11 validates it. The producer embeds selection mode, selected symbols, run-health status, data-quality status, paper-only safety boundary and VIX/regime provenance. Runtime evidence is uploaded as Actions artifacts and is not committed back to `main`.

#191 makes scanner datafeed liveness an explicit Paper Observation readiness gate. If all tracked symbols have missing/non-numeric `close` values, missing required bars, provider failures or unusable scanner metrics, the run is `DATAFEED_BLOCKED`. The active report path writes `reports/health/<date>-datafeed-liveness.json` and `reports/health/datafeed-liveness-latest.json`, propagates `datafeed_status` and `provider_failure_reason` into signal artifacts, and prevents blocked datafeed runs from being counted as productive observation cycles.

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

P164 requires regime evidence to first attempt true Polygon `I:VIX`. If unavailable because of provider entitlement, the report path falls back to the configured volatility proxy `VOLATILITY_PROXY_SYMBOL` defaulting to `VIXY`, stamps `source=polygon_proxy`, `status=PROXY_DEGRADED`, `validation_status=DEGRADED`, and does not authorize live/paper confidence claims. If both true VIX and proxy evidence are unavailable, regime output is `UNVALIDATED_REGIME`.

Contract document: `docs/architecture/dataflow_contract_matrix.md`.

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
| FCM1 | Feature Connectivity Matrix Guard | P1 | High | Closed / targeted CI-wired |
| RPW1 | Runtime Proof-Pack Artifact Writer / Retention Index | P1 | High | Closed / targeted CI-wired |

FCM1 requires implemented / CI-green features to declare runtime gates, guard tests, evidence artifacts, documentation references, upstream dependencies and downstream consumers. Unknown dependencies, missing guard tests, missing artifacts and unsafe live/non-paper boundaries block the matrix.

RPW1 writes deterministic runtime proof-pack JSON artifacts and maintains a retention index with artifact identity, SHA-256 hash, observation window, retention days and the paper-only safety boundary.

Closure evidence: `docs/operations/fcm1_rpw1_connectivity_proof_pack_retention_closure_2026_06_03.md`. This is a targeted feature closure and does not claim repository-wide full-regression green.

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
- #103: JWT fail-closed migration validated and closed. Missing or blank `INSTITUTIONAL_JWT_SECRET` blocks token creation and validation; protected API routes return explicit authentication/configuration failures instead of accepting requests; closure evidence is documented in `docs/operations/jwt_fail_closed_migration_103.md`.
- #104: FCM1/RPW1 CI-wired backlog status validated and closed. Feature connectivity and runtime proof-pack retention have guard tests, dedicated targeted CI wiring, closure evidence and a paper-only safety boundary; no repository-wide full-regression green is claimed.
- #132: Scanner Runtime Boundary validated and closed. Runtime reports and Paper Observation evidence must expose `selection_mode`; static watchlists remain research setup only and cannot claim dynamic scanner breadth or trading-edge proof.
- #160: Module classification baseline validated and closed. Pipeline-relevant modules have explicit classification, and the architecture inventory is regenerated under guard.
- #164: VIX/regime entitlement handling validated and closed. The Paper Observation/report regime path attempts true `I:VIX`, falls back to `VOLATILITY_PROXY_SYMBOL`/`VIXY` with degraded proxy provenance, and fails visible as `UNVALIDATED_REGIME` if neither true VIX nor proxy evidence is available.
- #177: Real-data backtest pipeline coupling phase 1 implemented and CI-green. Historical trade plans can be exported through the Scanner → Signal → Quality → Validator path; non-pipeline-coupled plans remain blocked from real-data evidence claims.
- #178: Runtime reachability guard implemented at documentation/test-guard level. Decision-critical modules are registered in `docs/architecture/decision_critical_runtime_reachability.json`; active modules require runtime entrypoint plus guard proof, while non-runtime helpers have explicit forbidden architecture/evidence claims.
- #184: Historical real-data input persistence implemented at checksum/auditability guard level. BT9 verifies coverage-manifest SHA256 checksums against persisted bars, accepted evidence exposes `input_checksums`, and BT131 persists source inputs plus reports.
- #188: Evidence Quality Gate implemented at documentation/test-guard level. The gate is documented in `docs/operations/evidence-quality-gate.md`, evaluated by `src/evidence_quality_gate.py` / `scripts/evaluate_evidence_quality_gate.py`, and guarded by `tests/test_evidence_quality_gate_188.py`.

## Recommended Next Remediation Order

1. Continue unresolved evidence-critical blockers referenced by #188, especially #181, #185, #186 and #187.
2. Continue Phase B data-integrity foundation: survivorship-safe universe, second-provider cross-validation and real persisted daily observation source feed.
3. Validate remaining CI-pending evidence workflows before upgrading status language.

## Safety Boundary

This roadmap does not authorize live trading, broker execution, capital allocation or production deployment.

The system remains research / decision-support / paper-observation only.
