# Institutional Trading Engine Roadmap

Status date: 2026-05-31  
Current state: EV1-EV12 evidence-integrity remediation is implemented, centrally documented and CI-green. CI runtime simplification is implemented and CI-green. B1.1 evidence operation discipline plus TG2/TG3 reporting integration is implemented and CI-wired. Phase B1.1 remains active as the 3-6 month observation-only evidence collection period. GOV1-GOV10 runtime/pre-live governance hardening is implemented and CI-green. SR1 stable signal identity, SR2 ATR persistence, SR3 repo-write serialization, SR4 trusted portfolio-governance source enforcement, SR5 persistent anomaly-state governance, SR6 governance-threshold single source of truth, SR7 completed-bar watcher semantics and SR8 dependency reproducibility contract are implemented and CI-green. PSR1 daily runtime evidence manifest, PSR2 runtime evidence manifest guard, PSR3 fill-quality evidence integration and PSR4 drift/regime-change evidence linkage are implemented and CI-green. Phase RGP Runtime Governance Proof Pack is active; RGP1 missing/invalid PortfolioState fail-closed proof and RGP2 runtime governance approval gate are implemented and CI-green. RGP3 stale PortfolioState approval blocking is implemented and awaiting CI. Phase D expansion or any live-execution consideration remains blocked until forward evidence, drift monitoring, risk attribution, execution quality review, capacity/turnover realism and manual approval are in place. Real-money execution is not authorized by code.

## Strategic direction

The next stage is not more scanner features. The next stage is institutional evidence, realistic execution assumptions, controlled intellectual-property separation and mathematically correct decision hygiene.

The project now prioritizes:

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
12. end-to-end runtime governance proof before any additional expansion

Hard rule: no real-money execution before real forward evidence, drift detection, regime-change monitoring, position-level risk attribution, capacity/turnover realism, runtime governance hardening and manual approval are in place.

Hard IP rule: the public repository may demonstrate architecture, evidence discipline and deterministic framework behavior, but proprietary edge configuration must not be developed further in public by default.

Hard logic rule: decision-critical math must be regression-tested before it is trusted by reports, ranking or paper execution workflows.

Hard runtime-governance rule: missing state, missing anomaly data, non-positive computed price levels and runtime-loop exceptions must fail closed or be explicitly surfaced before any result can be trusted.

Hard report-artifact rule: committed public report examples must remain synthetic/public-safe and generated runtime reports must be written only to non-committed output locations.

Hard evidence-integrity rule: Sharpe-like metrics must use explicit units. Per-trade Sharpe, t-statistic and Deflated Sharpe inputs must not be mixed.

## Phase RGP — Runtime Governance Proof Pack

Target window: active  
Goal: prove that the runtime fails closed end-to-end when governance state, market data, alert delivery or persistence is degraded. This phase is not about adding scanner features. It is about proving the system cannot silently continue when runtime safety evidence is missing.

| ID | Task | Priority | Impact | Status |
|---|---|---:|---:|---|
| RGP1 | Prove missing or invalid `PortfolioState` forces kill-switch activation and prevents runtime approval paths from treating `0.0` drawdown as valid governance | P0 | Critical | Done / CI-green |
| RGP2 | Prove `governance_valid=False` blocks decision approval in the runtime integration path, not only in the portfolio-state data model | P0 | Critical | Done / CI-green |
| RGP3 | Treat stale `portfolio_state.updated_at` as governance-invalid or evidence-failing before observation-day acceptance | P0 | Critical | Implemented / awaiting CI |
| RGP4 | Escalate Polygon/data-provider fetch failure for actionable signals into explicit degraded/fail evidence instead of silently skipping lifecycle evaluation | P0 | Critical | Pending |
| RGP5 | Send or persist STOP/EXIT alerts before git commit/rebase/push so alert delivery cannot be blocked by repository persistence failures | P0 | Critical | Pending |
| RGP6 | Remove silent notification masking for critical alerts by using strict notification mode and eliminating `|| true` from critical alert paths | P1 | High | Pending |
| RGP7 | Verify all repo-writing workflows share the same repo-wide concurrency group or use a robust push retry strategy | P1 | High | Pending |
| RGP8 | Ensure alert/evidence artifacts are uploaded even when git persistence fails | P1 | High | Pending |
| RGP9 | Consolidate terminal signal-status definitions into one shared source of truth | P2 | Medium | Pending |
| RGP10 | Sort latest bars by timestamp before selecting the newest bar for watcher evaluation | P2 | Medium | Pending |
| RGP11 | Quantize signal identity float inputs before hashing to prevent deterministic-ID drift across platforms | P2 | Medium | Pending |
| RGP12 | Either persist `PARTIAL_EXIT_FILLED` as a lifecycle event or remove the dead event path from runner management | P2 | Medium | Pending |

RGP is an audit/proof phase. It does not authorize live trading, production execution or new strategy complexity. It must be CI-backed before Phase D expansion resumes.

## Phase EV — Evidence Integrity Fixes

Target window: completed / CI-green  
Goal: repair evidence-math and backtest-fidelity issues found by static code review before building new strategy complexity.

| ID | Task | Priority | Impact | Status |
|---|---|---:|---:|---|
| EV1 | Fix `calculate_sharpe_ratio` so it returns per-trade Sharpe instead of a sample-size-scaled t-statistic | P0 | Critical | Done / CI-green |
| EV2 | Ensure Deflated Sharpe receives per-trade Sharpe and not the t-statistic | P0 | Critical | Done / CI-green |
| EV3 | Make historical backtest actually simulate declared `stop_model` / `exit_model` or fail closed | P0 | Critical | Done / CI-green |
| EV4 | Prevent full `-1R` booking after Target 1 when the declared stop model implies breakeven or partial management | P0 | High | Done / CI-green |
| EV5 | Model gap-through-stop fills pessimistically instead of always filling exactly at stop | P0 | High | Done / CI-green |
| EV6 | Fix Target-1-only `exit_date` so fixed-date holdout segmentation uses the actual hit date | P1 | High | Done / CI-green |
| EV7 | Prevent `tier_3` + size reduction from ranking above clean `tier_3` WATCH candidates | P1 | Medium | Done / CI-green |
| EV8 | Clarify fixed-date holdout semantics so the report does not overstate overfitting protection | P2 | Medium | Done / CI-green |
| EV9 | Report effective drawdown threshold instead of raw multiplier | P1 | Medium | Done / CI-green |
| EV10 | Handle `profit_factor=inf` degradation without `nan` audit output | P1 | Medium | Done / CI-green |
| EV11 | Make setup scoring fallbacks conservative for missing RSI / ATR / RVOL instead of ideal-zone defaults | P1 | Medium | Done / CI-green |
| EV12 | Add drawdown magnitude thresholds to kill-switch governance | P1 | Medium | Done / CI-green |
