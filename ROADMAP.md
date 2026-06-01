# Institutional Trading Engine Roadmap

Status date: 2026-06-01  
Current state: EV1-EV12 evidence-integrity remediation is implemented, centrally documented and CI-green. CI runtime simplification is implemented and CI-green. B1.1 evidence operation discipline plus TG2/TG3 reporting integration is implemented and CI-wired. Phase B1.1 remains active as the 3-6 month observation-only evidence collection period. PO1 Paper Observation Timeline and Review Gate is implemented and CI-green. GOV1-GOV10 runtime/pre-live governance hardening is implemented and CI-green. SR1 stable signal identity, SR2 ATR persistence, SR3 repo-write serialization, SR4 trusted portfolio-governance source enforcement, SR5 persistent anomaly-state governance, SR6 governance-threshold single source of truth, SR7 completed-bar watcher semantics and SR8 dependency reproducibility contract are implemented and CI-green. PSR1 daily runtime evidence manifest, PSR2 runtime evidence manifest guard, PSR3 fill-quality evidence integration and PSR4 drift/regime-change evidence linkage are implemented and CI-green. Phase RGP Runtime Governance Proof Pack is complete through RGP12; RGP1 missing/invalid PortfolioState fail-closed proof, RGP2 runtime governance approval gate, RGP3 stale PortfolioState approval blocking, RGP4 actionable signal provider-fetch failure blocking, RGP5 critical STOP/EXIT alert ordering, RGP6 strict critical notification failure handling, RGP7 repo-write workflow governance guard, RGP8 artifact upload-on-failure guard, RGP9 signal lifecycle status source of truth, RGP10 latest-bar timestamp ordering guard, RGP11 signal identity float quantization and RGP12 partial-exit lifecycle persistence are implemented and CI-green. BT8 Backtesting Evidence Report generator is implemented and CI-green. Phase D expansion or any live-execution consideration remains blocked until forward evidence, drift monitoring, risk attribution, execution quality review, capacity/turnover realism and manual approval are in place. Real-money execution is not authorized by code.

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

## Phase PO — Paper Observation Evidence Process

Target window: active / CI-green  
Goal: formalize the 3-6 month paper-observation evidence period before any Phase D or live-execution consideration.

| ID | Task | Priority | Impact | Status |
|---|---|---:|---:|---|
| PO1 | Define Paper Observation start date, minimum duration, review dates, required evidence families and live-trading hard block | P0 | Critical | Done / CI-green |

PO1 establishes 2026-06-01 as the Paper Observation start date, 2026-07-01 as the first review date, 2026-09-01 as the major evidence review date and 2026-12-01 as the extended review date. It does not authorize live trading.

## Phase RGP — Runtime Governance Proof Pack

Target window: completed / CI-green  
Goal: prove that the runtime fails closed end-to-end when governance state, market data, alert delivery or persistence is degraded. This phase is not about adding scanner features. It is about proving the system cannot silently continue when runtime safety evidence is missing.

| ID | Task | Priority | Impact | Status |
|---|---|---:|---:|---|
| RGP1 | Prove missing or invalid `PortfolioState` forces kill-switch activation and prevents runtime approval paths from treating `0.0` drawdown as valid governance | P0 | Critical | Done / CI-green |
| RGP2 | Prove `governance_valid=False` blocks decision approval in the runtime integration path, not only in the portfolio-state data model | P0 | Critical | Done / CI-green |
| RGP3 | Treat stale `portfolio_state.updated_at` as governance-invalid or evidence-failing before observation-day acceptance | P0 | Critical | Done / CI-green |
| RGP4 | Escalate Polygon/data-provider fetch failure for actionable signals into explicit degraded/fail evidence instead of silently skipping lifecycle evaluation | P0 | Critical | Done / CI-green |
| RGP5 | Send or persist STOP/EXIT alerts before git commit/rebase/push so alert delivery cannot be blocked by repository persistence failures | P0 | Critical | Done / CI-green |
| RGP6 | Remove silent notification masking for critical alerts by using strict notification mode and eliminating `|| true` from critical alert paths | P1 | High | Done / CI-green |
| RGP7 | Verify all repo-writing workflows share the same repo-wide concurrency group or use a robust push retry strategy | P1 | High | Done / CI-green |
| RGP8 | Ensure alert/evidence artifacts are uploaded even when git persistence fails | P1 | High | Done / CI-green |
| RGP9 | Consolidate terminal signal-status definitions into one shared source of truth | P2 | Medium | Done / CI-green |
| RGP10 | Sort latest bars by timestamp before selecting the newest bar for watcher evaluation | P2 | Medium | Done / CI-green |
| RGP11 | Quantize signal identity float inputs before hashing to prevent deterministic-ID drift across platforms | P2 | Medium | Done / CI-green |
| RGP12 | Persist `PARTIAL_EXIT_FILLED` as a supplemental lifecycle event emitted by Target-1 runner management | P2 | Medium | Done / CI-green |

RGP is an audit/proof phase. It does not authorize live trading, production execution or new strategy complexity. Phase D remains blocked until forward evidence, risk attribution, execution-quality review and manual approval requirements are satisfied.

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

EV1-EV12 are implemented, CI-green and consolidated in `docs/operations/ev_evidence_consolidation_full_suite_review.md`.

## Phase GOV — Runtime Governance Hardening

Target window: completed / CI-green  
Goal: close runtime-governance gaps found during Paper Observation before adding strategy complexity or moving closer to live consideration.

| ID | Task | Priority | Impact | Status |
|---|---|---:|---:|---|
| GOV1 | Feed `severe_anomaly_count` from runtime state into `evaluate_kill_switch` instead of passing a hardcoded `0` | P0 | Critical | Done / CI-green |
| GOV2 | Make missing portfolio state fail closed: `conservative_default` must not silently return `drawdown_percent=0.0` and `daily_loss_percent=0.0` as if governance state were valid | P0 | Critical | Done / CI-green |
| GOV3 | Reject all computed non-positive entries and stops after calculation, not only explicitly supplied entry values | P0 | Critical | Done / CI-green |
| GOV4 | Treat `VIX=None` consistently in `negative_override` instead of silently defaulting missing VIX to `0` | P1 | High | Done / CI-green |
| GOV5 | Bound `RuntimeState.history` with a ring buffer or documented max length to avoid unbounded memory growth during multi-day observation | P1 | Medium | Done / CI-green |
| GOV6 | Add runtime-loop exception handling with logging and a max-consecutive-error limit so one provider/network exception cannot kill the loop silently | P1 | Medium | Done / CI-green |
| GOV7 | Fix adaptive-weighting rounding so normalized public weights sum to exactly `1.0` after rounding | P2 | Medium | Done / CI-green |
| GOV8 | Document or encode VIX term-structure inversion mode so PARTIAL and DIRECT modes are not treated as the same boolean semantics | P2 | Medium | Done / CI-green |
| GOV9 | Add deprecation markers or consolidation plan for duplicate modules with overlapping responsibilities | P2 | Medium | Done / CI-green |
| GOV10 | Add cumulative drift gate for Paper Observation so small persistent daily drift cannot avoid detection by only checking max absolute daily drift | P2 | Medium | Done / CI-green |

## Phase IP — Public Framework / Private Edge Separation

Target window: completed / CI-wired  
Goal: keep the repository useful as a public framework while protecting proprietary strategy edge.

| ID | Task | Priority | Impact | Status |
|---|---|---:|---:|---|
| IP1 | Define the public/private boundary for framework code, strategy configuration, thresholds, setup mappings, exit profiles, scoring weights and evidence artifacts | P0 | Critical | Done |
| IP2 | Add an operational policy document for public repository hygiene and private edge handling | P0 | Critical | Done |
| IP3 | Replace public production-like thresholds and strategy constants with clearly marked demo defaults or external configurable interfaces | P0 | Critical | Done / CI-green |
| IP4 | Add a private-edge adapter/import boundary so local/private modules can provide real thresholds, regime maps, scoring weights and exit profiles without being committed to the public repo | P0 | Critical | Done / CI-green |
| IP5 | Move real reports, ranked opportunities, raw evidence outputs and non-synthetic artifacts out of public version control or replace them with synthetic examples | P0 | Critical | Done / CI-wired |
| IP6 | Expand `.gitignore` for private configs, generated reports, databases, caches, logs, coverage output and local artifacts | P0 | High | Done / CI-wired |
| IP7 | Update README to state that the public repo contains framework/demo defaults only, not proprietary production edge configuration | P1 | High | Done |
| IP8 | Add tests proving the public fallback path works without private modules and that private modules are optional imports only | P1 | High | Done / CI-green |
| IP9 | Review open PRs for newly introduced edge constants before merge, especially setup-specific target profiles and scoring changes | P0 | Critical | Done / CI-wired |
| IP10 | Add license and usage disclaimer appropriate for a public decision-support research framework | P1 | Medium | Done / CI-wired |
| IP11 | Add fail-closed Report Output Boundary Guard so generated runtime reports cannot overwrite committed public report examples | P0 | Critical | Done / CI-green |

IP9/IP10 implemented artifacts:

```text
.github/pull_request_template.md
.github/workflows/ip9_ip10.yml
LICENSE
DISCLAIMER.md
docs/operations/ip9_ip10_public_repo_governance.md
tests/test_ip9_ip10_public_repo_governance.py
```

## Phase CL — Core Logic Remediation

| ID | Task | Priority | Impact | Status |
|---|---|---:|---:|---|
| CL1 | Fix inflated downside asymmetry below SMA50, all-tier portfolio-risk reduction and breakeven expectancy classification | P0/P1 | Critical/High | Done / CI-wired |
| CL2 | Document and reconcile dual setup-scoring systems so report scores and decision scores are clearly separated or unified | P1 | High | Done / CI-wired |
| CL3 | Add explicit drawdown-source validation before kill-switch drawdown governance can be considered active | P1 | High | Done / CI-wired |
| CL4 | Evaluate Wilder-style ATR migration behind regression tests and threshold-version bump | P2 | Medium | Done / CI-wired |
| CL5 | Make `regime_alignment` an independent fail-closed gate before risk-tier scoring can approve or watch a setup | P2 | Medium | Done / CI-wired |

CL1-CL5 are remediation and audit gates only. None of these prove edge and none authorize live trading.

## Phase BT — Backtest Evidence Hardening

| ID | Task | Priority | Impact | Status |
|---|---|---:|---:|---|
| BT2 | Add public-safe Strategy Test Matrix coverage validation | P1 | High | Done |
| BT3 | Add reproducible backtest run contract with pinned inputs, dataset fingerprints, metrics and artifact hashes | P1 | High | Done |
| BT5 | Add Walk-Forward / Out-of-Sample Robustness Gate with OOS pass rate, degradation, drawdown, trade-count and chronology checks | P0 | Critical | Done / CI-green |
| BT6 | Add previous-run evidence baseline comparison for regression gates | P1 | High | Done / CI-green |
| BT7 | Add capacity and turnover realism gates before any private production sizing work | P1 | High | Done / CI-green |
| BT8 | Add reproducible Backtesting Evidence Report generator with JSON/Markdown outputs from BT3 run contracts | P1 | High | Done / CI-green |

## Phase TG — Report Delivery

| ID | Task | Priority | Impact | Status |
|---|---|---:|---:|---|
| TG1 | Add Telegram report dispatcher with research-only guardrails, dry-run mode and injectable transport | P1 | High | Done |
| TG2 | Integrate Telegram summaries into daily evidence/report workflows after CI workflow permissions are confirmed | P2 | Medium | Done / CI-wired |
| TG3 | Add report templates for Daily Evidence, Fill Quality and Kill Switch | P2 | Medium | Done / CI-wired |

## Phase SR — Signal Runtime Audit Stabilization

| ID | Task | Priority | Impact | Status |
|---|---|---:|---:|---|
| SR1 | Make `signal_id` stable across regenerations by excluding volatile `generated_at` from identity fields and proving same-day logical signal stability with regression tests | P0 | Critical | Done / CI-green |
| SR2 | Persist `atr14` or reconstruct ATR deterministically so Target-1 runner management can activate the declared ATR trailing-stop path | P0 | Critical | Done / CI-green |
| SR3 | Serialize all repo-writing GitHub Actions with a shared repo-wide write concurrency group or robust pull-rebase-push retry loop | P0 | Critical | Done / CI-green |
| SR4 | Remove or evidence-gate override arguments that mark portfolio governance valid without a trusted portfolio-state source | P1 | High | Done / CI-green |
| SR5 | Feed anomaly kill-switch logic from persistent anomaly state instead of process-local in-memory cache during GitHub Actions runs | P1 | High | Done / CI-green |
| SR6 | Consolidate governance thresholds into a single source of truth so tuning constants cannot be changed in dead code | P1 | Medium | Done / CI-green |
| SR7 | Align watcher cadence with completed-bar semantics or migrate watcher evaluation to true intraday bars | P1 | High | Done / CI-green |
| SR8 | Pin runtime/test dependencies and introduce a lockfile or equivalent reproducibility contract | P1 | Medium | Done / CI-green |

## Phase PSR — Post-SR Runtime Evidence Hardening

| ID | Task | Priority | Impact | Status |
|---|---|---:|---:|---|
| PSR1 | Add daily runtime evidence manifest with required input/output/governance artifact hashes and PASS/FAIL status | P0 | Critical | Done / CI-green |
| PSR2 | Add daily manifest CI/report guard so missing evidence blocks observation-day acceptance | P0 | Critical | Done / CI-green |
| PSR3 | Add fill-quality evidence manifest integration for paper execution outcomes | P1 | High | Done / CI-green |
| PSR4 | Add drift and regime-change evidence linkage into the daily manifest | P1 | High | Done / CI-green |

PSR1-PSR4 are implemented and CI-green. The Post-SR Runtime Evidence Hardening block is closed. None of these authorize live trading.
