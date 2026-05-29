# Institutional Trading Engine Roadmap

Status date: 2026-05-29  
Current state: IP3 public-demo threshold defaults are implemented and CI-green. IP4 optional external edge provider boundary is implemented and CI-green. IP5/IP6 artifact hygiene and `.gitignore` hardening are implemented and CI-wired. IP8 fallback/private-edge absence test coverage is implemented and CI-green. CL1 core decision logic remediation for asymmetry, portfolio-risk tier handling and breakeven expectancy is implemented and CI-wired. CL2 scoring-system audit and report-vs-decision separation are implemented and CI-wired. CL3 kill-switch drawdown-source validation is implemented and CI-wired. CL4 ATR calculation governance, Wilder ATR evaluation and threshold-version bump are implemented and CI-wired. BT7 Capacity / Turnover / Realism Gate is implemented and CI-green. BT6 Evidence Baseline Regression Gate is implemented and CI-green. BT5 Walk-Forward / Out-of-Sample Robustness Gate is implemented and CI-green. Phase B1.1 remains the active 3-6 month observation-only evidence collection period. Real-money execution is not authorized by code.

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
9. multi-strategy expansion only after the base edge is proven

Hard rule: no real-money execution before real forward evidence, drift detection, regime-change monitoring, position-level risk attribution, capacity/turnover realism and manual approval are in place.

Hard IP rule: the public repository may demonstrate architecture, evidence discipline and deterministic framework behavior, but proprietary edge configuration must not be developed further in public by default.

Hard logic rule: decision-critical math must be regression-tested before it is trusted by reports, ranking or paper execution workflows.

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
| IP9 | Review open PRs for newly introduced edge constants before merge, especially setup-specific target profiles and scoring changes | P0 | Critical | Planned |
| IP10 | Add license and usage disclaimer appropriate for a public decision-support research framework | P1 | Medium | Planned |

## Phase CL — Core Logic Remediation

| ID | Task | Priority | Impact | Status |
|---|---|---:|---:|---|
| CL1 | Fix inflated downside asymmetry below SMA50, all-tier portfolio-risk reduction and breakeven expectancy classification | P0/P1 | Critical/High | Done / CI-wired |
| CL2 | Document and reconcile dual setup-scoring systems so report scores and decision scores are clearly separated or unified | P1 | High | Done / CI-wired |
| CL3 | Add explicit drawdown-source validation before kill-switch drawdown governance can be considered active | P1 | High | Done / CI-wired |
| CL4 | Evaluate Wilder-style ATR migration behind regression tests and threshold-version bump | P2 | Medium | Done / CI-wired |
| CL5 | Review whether `regime_alignment` should remain a derived score or become an independent regime signal | P2 | Medium | Planned |

CL1-CL4 are remediation and audit gates only. CL1 fixes decision-critical math and measurement issues. CL2 separates report-only scores from decision-authoritative gates. CL3 prevents drawdown kill-switch governance from being considered active unless the drawdown source is real, reconciled and internally consistent. CL4 prevents ATR semantics from changing silently by making ATR method, version and evidence invalidation explicit. None of these prove edge and none authorize live trading.

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
| TG2 | Integrate Telegram summaries into daily evidence/report workflows after CI workflow permissions are confirmed | P2 | Medium | Planned |
| TG3 | Add report templates for Daily Evidence, Fill Quality, Kill Switch and Backtest Summary | P2 | Medium | Planned |

## Phase A — Foundation Repair and Evidence Hygiene

| ID | Task | Priority | Impact | Status |
|---|---|---:|---:|---|
| A1 | Add a survivorship-safe data source, for example Norgate, Sharadar or equivalent point-in-time universe coverage | P0 | Critical | Planned |
| A2 | Add a second data provider abstraction for cross-validation against Polygon | P0 | Critical | Planned |
| A3 | Centralize decision thresholds in `src/config/thresholds.py` with explicit versioning | P1 | High | Done |
| A4 | Invalidate backtest/lockbox evidence when threshold versions change | P1 | High | Done |
| A5 | Replace linear slippage heuristic with square-root impact plus regime multipliers | P1 | High | Done |
| A6 | Add Deflated Sharpe Ratio and bootstrap confidence intervals to edge validation | P1 | High | Done |
| A7 | Convert Polygon client retry/rate-limit output to structured logging | P2 | Medium | Done |
| A8 | Add cache locking for `.cache/polygon` writes | P2 | Medium | Done |
| A9 | Update `CHANGELOG.md` and `SETUP_NOTES.md` for P47 readiness state | P2 | Medium | Done |
| A10 | Document quarterly secrets rotation policy | P2 | Medium | Done |

## Phase B — Real Forward Evidence

Target window: 3-6 months  
Goal: prove whether the rule-based system has live-observable edge before adding complexity.

| ID | Task | Priority | Impact | Status |
|---|---|---:|---:|---|
| B1 | Prepare paper observation daily reconciliation gate and report model | P0 | Critical | Done |
| B1.1 | Run 3-6 months of observation-only paper evidence with daily reconciliation | P0 | Critical | In Progress |
| B2 | Add paper vs. backtest performance drift detection | P0 | High | Done |
| B3 | Add SPRT-style sequential test for edge decay | P1 | High | Done |
| B4 | Add deterministic regime-change detection gate | P1 | High | Done |
| B5 | Add position-level risk attribution by beta, sector, factor and single-name contribution | P1 | High | Done |
| B6 | Add Monte Carlo robustness suite with bootstrap and permutation tests | P1 | Medium | Done |
| B7-B17 | Daily evidence pipeline, persisted observation feed, raw contract and real paper observation runbook discipline | P0/P1 | Critical/High | Done |

## Phase C — Execution Reality

| ID | Task | Priority | Impact | Status |
|---|---|---:|---:|---|
| C1 | Define broker adapter interface for paper execution first | P0 | High | Done |
| C2 | Add Alpaca paper adapter as first broker implementation | P1 | High | Done |
| C3 | Add VWAP/TWAP order slicing using public demo profiles only until private-edge boundary exists | P1 | High | Done |
| C4 | Add order reconciliation engine for signal, order, fill and portfolio state | P1 | High | Done |
| C5 | Add live vs. backtest daily reconciliation workflow | P1 | High | Done |
| C6 | Add fill-quality report for slippage, spread, delay and partial fills | P2 | Medium | Done |
| C7 | Add execution kill switch when execution drift exceeds limits | P1 | High | Done |

## Phase D — Strategy Expansion

Start only after Phase B and C produce credible evidence and after the private-edge boundary exists.

| ID | Task | Priority | Impact | Status |
|---|---|---:|---:|---|
| D1 | Add mean-reversion strategy sleeve with separate validation behind the private-edge boundary or with demo-only public constants | P1 | High | Planned |
| D2 | Add multi-strategy risk-parity allocator | P1 | High | Planned |
| D3 | Add factor, sector and style exposure caps | P1 | High | Planned |
| D4 | Add correlation-aware position sizing | P1 | High | Planned |
| D5 | Pilot options-flow features such as GEX, skew and put/call signals | P2 | Medium | Planned |
| D6 | Pilot LLM-based news sentiment pipeline | P2 | Medium | Planned |
| D7 | Evaluate event-driven earnings module with separate edge validation | P2 | Medium | Planned |

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

## Recently completed evidence-visibility and logic-safety work

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
- IP1 public/private edge boundary guardrail: done.
- IP2 public repository hygiene and private-edge handling policy: done.
- Phase C paper execution and audit infrastructure: done.
- Phase B daily evidence pipeline and paper observation discipline: done.
- Phase A evidence hygiene: done and CI-green.

## Current execution focus

B1.1 remains the long-running evidence collection period. Phase C is active for paper execution only. Telegram delivery is allowed for research/paper-observation reports only. IP3/IP4 is complete and CI-green. IP5/IP6 and CL1-CL4 are implemented and CI-wired. Immediate focus: confirm CI green, then execute CL5 before adding new strategy complexity.

## Recommended next block

The next rational block is **CL5**: review whether `regime_alignment` remains a derived score or becomes an independent regime signal.

## Do not do yet

- Do not enable real-money execution.
- Do not add new asset classes.
- Do not add ML before rule-based edge is statistically significant.
- Do not open or reuse lockbox evidence casually.
- Do not skip forward paper observation.
- Do not add new proprietary thresholds, setup maps, scoring weights or exit profiles directly to the public repo unless they are explicitly demo-only.
- Do not commit real ranked opportunity reports, raw evidence outputs, provider credentials or private strategy experiments to the public repo.
- Do not treat report-only scores as decision-authoritative despite the CL2 audit boundary.
- Do not treat drawdown kill-switch governance as active unless CL3 drawdown-source validation is present and clean.
- Do not change ATR semantics or compare ATR-dependent artifacts across threshold versions without explicit CL4 evidence-invalidation handling.
- Do not send Telegram messages that imply live trading authorization or contain private edge parameters.
