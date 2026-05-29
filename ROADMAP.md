# Institutional Trading Engine Roadmap

Status date: 2026-05-29  
Current state: B1.1 evidence operation discipline plus TG2/TG3 reporting integration is implemented and CI-wired. Phase B1.1 remains active as the 3-6 month observation-only evidence collection period. GOV1-GOV10 runtime/pre-live governance hardening is implemented and CI-green. Real-money execution is not authorized by code.

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

Hard rule: no real-money execution before real forward evidence, drift detection, regime-change monitoring, position-level risk attribution, capacity/turnover realism, runtime governance hardening and manual approval are in place.

Hard IP rule: the public repository may demonstrate architecture, evidence discipline and deterministic framework behavior, but proprietary edge configuration must not be developed further in public by default.

Hard logic rule: decision-critical math must be regression-tested before it is trusted by reports, ranking or paper execution workflows.

Hard runtime-governance rule: missing state, missing anomaly data, non-positive computed price levels and runtime-loop exceptions must fail closed or be explicitly surfaced before any result can be trusted.

Hard report-artifact rule: committed public report examples must remain synthetic/public-safe and generated runtime reports must be written only to non-committed output locations.

## Phase GOV — Runtime Governance Hardening

Target window: active  
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

GOV1-GOV10 are implemented and CI-green. They add runtime governance, runtime stability and pre-live hygiene for anomaly handling, missing portfolio state, non-positive prices, VIX handling, runtime-loop resilience, rounded public weights, VIX term-structure semantics, duplicate-module remediation markers and cumulative Paper Observation drift detection.

## Phase IP — Public Framework / Private Edge Separation

Target window: immediate  
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

BT5 is a robustness gate only. BT6 is a baseline-regression gate only. BT7 is a capacity/turnover realism gate only. None of them prove production edge and none authorize live trading.

## Phase TG — Report Delivery

| ID | Task | Priority | Impact | Status |
|---|---|---:|---:|---|
| TG1 | Add Telegram report dispatcher with research-only guardrails, dry-run mode and injectable transport | P1 | High | Done |
| TG2 | Integrate Telegram summaries into daily evidence/report workflows after CI workflow permissions are confirmed | P2 | Medium | Done / CI-wired |
| TG3 | Add report templates for Daily Evidence, Fill Quality, Kill Switch and Backtest Summary | P2 | Medium | Done / CI-wired |

## Phase A — Foundation Repair and Evidence Hygiene

| ID | Task | Priority | Impact | Status |
|---|---|---:|---:|---|
| A1 | Add a survivorship-safe data source, for example Norgate, Sharadar or equivalent point-in-time universe coverage | P0 | Critical | Planned |
| A2 | Add a second data provider abstraction for cross-validation against Polygon | P0 | Critical | Planned |
| A3-A10 | Threshold versioning, evidence invalidation, slippage realism, statistical robustness, structured logging, cache locking, documentation and secrets rotation policy | P1/P2 | High/Medium | Done / CI-green |

## Phase B — Real Forward Evidence

Target window: 3-6 months  
Goal: prove whether the rule-based system has live-observable edge before adding complexity.

| ID | Task | Priority | Impact | Status |
|---|---|---:|---:|---|
| B1 | Prepare paper observation daily reconciliation gate and report model | P0 | Critical | Done |
| B1.1 | Run 3-6 months of observation-only paper evidence with daily reconciliation | P0 | Critical | In Progress / operation gate CI-wired |
| B1.2 | Keep visible asset-treatment timeline artifacts for each Paper Observation run | P1 | Medium | Done / CI-wired |
| B2-B17 | Drift detection, sequential edge decay, regime-change detection, risk attribution, Monte Carlo robustness and daily evidence pipeline | P0/P1 | Critical/High | Done |

## Phase C — Execution Reality

| ID | Task | Priority | Impact | Status |
|---|---|---:|---:|---|
| C1-C7 | Paper broker adapter, Alpaca paper adapter, order slicing, reconciliation, live-vs-backtest reconciliation, fill quality and execution kill switch | P0/P2 | High/Medium | Done |

## Phase D — Strategy Expansion

Start only after Phase B and C produce credible evidence, after the private-edge boundary exists and after GOV1-GOV10 runtime/pre-live hygiene is implemented and CI-green.

| ID | Task | Priority | Impact | Status |
|---|---|---:|---:|---|
| D1 | Add mean-reversion strategy sleeve with separate validation behind the private-edge boundary or with demo-only public constants | P1 | High | Planned / Blocked by B1.1 + GOV |
| D2 | Add multi-strategy risk-parity allocator | P1 | High | Planned / Blocked by B1.1 + GOV |
| D3 | Add factor, sector and style exposure caps | P1 | High | Planned / Blocked by B1.1 + GOV |
| D4 | Add correlation-aware position sizing | P1 | High | Planned / Blocked by B1.1 + GOV |
| D5 | Pilot options-flow features such as GEX, skew and put/call signals | P2 | Medium | Planned / Blocked by B1.1 + GOV |
| D6 | Pilot LLM-based news sentiment pipeline | P2 | Medium | Planned / Blocked by B1.1 + GOV |
| D7 | Evaluate event-driven earnings module with separate edge validation | P2 | Medium | Planned / Blocked by B1.1 + GOV |

## Phase E — Continuous Institutionalization

| ID | Task | Priority | Impact | Status |
|---|---|---:|---:|---|
| E1 | Add continuous backtesting in CI | P1 | Medium | Planned |
| E2 | Add statistically significant PR gates against previous evidence baselines | P1 | Medium | Planned |
| E3 | Automate daily live vs. backtest reconciliation | P1 | High | Planned |
| E4 | Add meta-labeling layer for trade/no-trade decision after primary signal behind private-edge boundary or demo-only public constants | P2 | Medium | Planned |
| E5 | Add capacity modeling to estimate how much capital the strategy can absorb | P2 | High | Superseded by BT7 baseline gate / future expansion |
| E6 | Add hierarchical risk parity allocation | P2 | Medium | Planned |
| E7 | Build an audit dashboard for evidence, drift, risk and execution quality | P2 | Medium | Planned |

## Recently completed evidence-visibility, IP and logic-safety work

- GOV1-GOV10 runtime/pre-live governance hardening: implemented and CI-green.
- B1.1 evidence operation discipline plus TG2/TG3 reporting integration: implemented and CI-wired.
- B1.2 visible Paper Observation asset-treatment timeline artifacts: implemented and CI-wired.
- Paper Observation Telegram notification workflow: implemented and active when repository secrets are configured.
- IP9/IP10 public repository governance: done and CI-wired.
- Report Output Boundary Guard: done and CI-green.
- CL5 regime-alignment independent gate: done and CI-wired.
- CL4 ATR calculation governance and threshold-version bump: done and CI-wired.
- CL3 kill-switch drawdown-source validation: done and CI-wired.
- CL2 scoring-system audit and report-vs-decision separation: done and CI-wired.
- CL1 core decision logic remediation: done and CI-wired.
- IP5/IP6 artifact hygiene and `.gitignore` hardening: done and CI-wired.
- IP3 public-demo threshold defaults: done and CI-green.
- IP4 optional external edge provider boundary: done and CI-green.
- IP8 fallback/private-edge absence tests: done and CI-green.
- BT7 Capacity / Turnover / Realism Gate: done and CI-green.
- BT6 Evidence Baseline Regression Gate: done and CI-green.
- BT5 Walk-Forward / Out-of-Sample Robustness Gate: done and CI-green.
- TG1 Telegram research-only report dispatcher: done.
- Phase C paper execution and audit infrastructure: done.
- Phase B daily evidence pipeline and paper observation discipline: done.
- Phase A evidence hygiene: done and CI-green.

## Current execution focus

B1.1 remains the long-running evidence collection period. GOV1-GOV10 are implemented and CI-green. Phase C is active for paper execution only. Telegram delivery is allowed for research/paper-observation reports only. Immediate focus: keep observation discipline running, inspect daily reconciliation cleanliness and avoid new strategy complexity until enough forward evidence exists.

## Recommended next block

Continue B1.1 Paper Observation discipline. Only consider lower-priority pre-live work or additional evidence/audit dashboard items after the observation cadence remains clean. Do not add strategy complexity until enough forward paper evidence exists.

## Do not do yet

- Do not enable real-money execution.
- Do not add new asset classes.
- Do not add ML before rule-based edge is statistically significant.
- Do not add Phase D strategy expansion before B1.1 observation evidence and GOV1-GOV10 runtime/pre-live hygiene are complete and CI-green.
- Do not ignore missing portfolio state or treat it as a healthy zero-drawdown state.
- Do not allow computed non-positive entries or stops to pass validation.
- Do not treat hardcoded `severe_anomaly_count=0` as acceptable runtime governance.
- Do not treat missing or invalid VIX as zero market stress.
- Do not let runtime history grow without bounds during multi-day observation.
- Do not let a single runtime provider exception silently kill the loop.
- Do not publish rounded public/demo weights that do not sum to exactly 1.0.
- Do not treat partial VIX curve compression as the same as direct VIX inversion.
- Do not leave duplicate or overlapping modules without ownership/deprecation markers.
- Do not rely only on max daily drift when cumulative small drift can accumulate across Paper Observation days.
- Do not open or reuse lockbox evidence casually.
- Do not skip forward paper observation.
- Do not add new proprietary thresholds, setup maps, scoring weights or exit profiles directly to the public repo unless they are explicitly demo-only.
- Do not commit real ranked opportunity reports, raw evidence outputs, provider credentials or private strategy experiments to the public repo.
- Do not overwrite committed public report examples with generated runtime reports.
- Do not treat report-only scores as decision-authoritative despite the CL2 audit boundary.
- Do not treat drawdown kill-switch governance as active unless CL3 drawdown-source validation is present and clean.
- Do not change ATR semantics or compare ATR-dependent artifacts across threshold versions without explicit CL4 evidence-invalidation handling.
- Do not let high setup score, asymmetry score or data confidence rescue poor regime alignment after CL5.
- Do not send Telegram messages that imply live trading authorization or contain private edge parameters.
