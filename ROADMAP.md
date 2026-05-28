# Institutional Trading Engine Roadmap

Status date: 2026-05-28  
Current state: Phase C5 daily expected-vs-observed execution reconciliation is implemented as paper/live observation infrastructure. Phase C4 order reconciliation is implemented as paper-only infrastructure. Phase C3 VWAP/TWAP paper order slicing is implemented and CI-green. Phase C2 Alpaca paper adapter is implemented and CI-green. Phase C1 paper broker adapter interface is implemented and CI-green. Phase B17 daily real paper observation runbook discipline is implemented and CI-green. Phase B16 real paper observation raw data contract is implemented and CI-green. Phase B15 observation cadence review is implemented and CI-green. Phase B14 Daily Evidence workflow dispatch integration is implemented, CI-green and workflow-green with uploaded artifact. Phase B13 real daily paper observation source builder is implemented and CI-green. Phase B12 persisted daily observation source feed and observation-only component mode are implemented. Phase A Evidence Hygiene implemented and CI-green. P36-P47 validation stack implemented. Real-money execution is not authorized by code. New P0 governance focus: public framework / private edge separation before further proprietary strategy development.

## Strategic direction

The next stage is not more scanner features. The next stage is institutional evidence and controlled intellectual-property separation.

The project is already a strong research and decision-support system. To become top-tier, the roadmap now prioritizes:

1. public framework / private edge separation
2. survivorship-safe data
3. statistically defensible edge validation
4. forward paper evidence
5. execution realism
6. portfolio-level risk attribution
7. multi-strategy expansion only after the base edge is proven

Hard rule: no real-money execution before real forward evidence, drift detection, regime-change monitoring and position-level risk attribution are in place.

Hard IP rule: the public repository may demonstrate architecture, evidence discipline and deterministic framework behavior, but proprietary edge configuration must not be developed further in public by default.

## Phase IP — Public Framework / Private Edge Separation

Target window: immediate  
Goal: keep the repository useful as a public framework while protecting proprietary strategy edge.

| ID | Task | Priority | Impact | Status |
|---|---|---:|---:|---|
| IP1 | Define the public/private boundary for framework code, strategy configuration, thresholds, setup mappings, exit profiles, scoring weights and evidence artifacts | P0 | Critical | Next |
| IP2 | Add an operational policy document for public repository hygiene and private edge handling | P0 | Critical | Planned |
| IP3 | Replace public production-like thresholds and strategy constants with clearly marked demo defaults or external configurable interfaces | P0 | Critical | Planned |
| IP4 | Add a private-edge adapter/import boundary so local/private modules can provide real thresholds, regime maps, scoring weights and exit profiles without being committed to the public repo | P0 | Critical | Planned |
| IP5 | Move real reports, ranked opportunities, raw evidence outputs and non-synthetic artifacts out of public version control or replace them with synthetic examples | P0 | Critical | Planned |
| IP6 | Expand `.gitignore` for private configs, generated reports, databases, caches, logs, coverage output and local artifacts | P0 | High | Planned |
| IP7 | Update README to state that the public repo contains framework/demo defaults only, not proprietary production edge configuration | P1 | High | Planned |
| IP8 | Add tests proving the public fallback path works without private modules and that private modules are optional imports only | P1 | High | Planned |
| IP9 | Review open PRs for newly introduced edge constants before merge, especially setup-specific target profiles and scoring changes | P0 | Critical | Planned |
| IP10 | Add license and usage disclaimer appropriate for a public decision-support research framework | P1 | Medium | Planned |

## Phase IP Implementation Order

The immediate execution order is:

```text
1. Roadmap and policy update
2. Public/private boundary interfaces
3. Demo defaults and optional private imports
4. Tests for fallback and private-edge absence
5. Public artifact hygiene and .gitignore hardening
6. README and operational documentation update
7. CI / regression run
8. Fixes until green
```

C3, C4 and C5 are implemented as public paper-execution/evidence infrastructure only. They do not add proprietary strategy edge and do not authorize live trading.

## Public vs Private Boundary

Public repository may contain:

```text
framework orchestration
interfaces and protocols
demo thresholds
demo setup maps
synthetic example reports
test fixtures
paper-observation infrastructure
evidence validation machinery
broker adapter interfaces
security and operations documentation
```

Private edge should contain:

```text
real decision thresholds
real regime-to-setup mappings
proprietary scoring weights
non-public entry/exit profiles
real ranked opportunity reports
private evidence artifacts
private experiment results
provider-specific operational settings
```

Secrets remain outside both public and private source control. API keys, tokens, database URLs and broker credentials must stay in GitHub Actions secrets, local environment variables or a dedicated secret manager.

## Phase A — Foundation Repair and Evidence Hygiene

Target window: 4-8 weeks  
Goal: make the research foundation harder to fool.

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

## Phase A Stabilization Gate

Phase A is implementation-complete and CI-validated.

| Gate | Status |
|---|---|
| Add Phase A tests to CI workflow | Done |
| Execute CI test run | Done |
| Fix failures if any | Done |
| Full regression suite green | Done |
| Final README update | Done |
| Approve Phase B start | Done |

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
| B7 | Emit a daily evidence report for paper/live observation | P2 | Medium | Done |
| B8 | Add daily evidence CLI and scheduled artifact workflow | P2 | Medium | Done |
| B9 | Run daily scheduled observation workflow and review artifacts | P2 | Medium | Done |
| B10 | Replace placeholder component reports with real generated B1-B6 component artifacts | P1 | High | Done |
| B11 | Replace smoke-fixture workflow mode with daily evidence source, input, validation and bootstrap pipeline | P1 | High | Done |
| B12 | Add persisted daily observation source feed and observation-only bootstrap workflow mode | P0 | Critical | Done |
| B13 | Replace bootstrap incoming records with real persisted daily paper observation source records | P0 | Critical | Done |
| B14 | Integrate real paper observation source path into Daily Evidence workflow dispatch | P0 | Critical | Done |
| B15 | Start real daily paper observation data capture and artifact review cadence | P0 | Critical | Done |
| B16 | Define real paper observation raw data contract and daily capture template | P0 | Critical | Done |
| B17 | Begin daily real paper observation runbook and evidence review discipline | P0 | Critical | Done |

## Phase C — Execution Reality

Target window: starts after B16 foundation; runs in parallel with B1.1 observation period  
Goal: ensure simulated edge survives realistic execution assumptions without enabling real-money execution.

| ID | Task | Priority | Impact | Status |
|---|---|---:|---:|---|
| C1 | Define broker adapter interface for paper execution first | P0 | High | Done |
| C2 | Add Alpaca paper adapter as first broker implementation | P1 | High | Done |
| C3 | Add VWAP/TWAP order slicing using public demo profiles only until private-edge boundary exists | P1 | High | Done |
| C4 | Add order reconciliation engine for signal, order, fill and portfolio state | P1 | High | Done |
| C5 | Add live vs. backtest daily reconciliation workflow | P1 | High | Done |
| C6 | Add fill-quality report for slippage, spread, delay and partial fills | P2 | Medium | Planned |
| C7 | Add execution kill switch when execution drift exceeds limits | P1 | High | Planned |

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
| E5 | Add capacity modeling to estimate how much capital the strategy can absorb | P2 | High | Planned |
| E6 | Add hierarchical risk parity allocation | P2 | Medium | Planned |
| E7 | Build an audit dashboard for evidence, drift, risk and execution quality | P2 | Medium | Planned |

## Recently completed evidence-visibility work

- Edge-evidence diagnostics summary artifacts: done.
- Edge-evidence workflow log snapshot: done.
- Versioned decision thresholds: done.
- Threshold-aware lockbox invalidation: done.
- Square-root regime-aware slippage model: done.
- Deflated Sharpe probability and bootstrap confidence intervals: done.
- Polygon structured logging: done.
- Polygon cache locking: done.
- Phase A changelog and setup notes refresh: done.
- Quarterly secrets rotation policy: done.
- Phase A CI stabilization plan: done.
- Phase A tests in CI: done.
- Full regression suite green after stabilization fixes: done.
- Paper observation daily reconciliation gate and report model: done.
- Performance drift detection engine: done and CI-green.
- Sequential edge-decay test: done and CI-green.
- Regime-change detection gate: done and CI-green.
- Position-level risk attribution: done and CI-green.
- Monte Carlo robustness suite: done and CI-green.
- Daily evidence report generator: done and CI-green.
- Daily evidence CLI and scheduled artifact workflow: done and CI-green.
- Daily evidence artifact workflow verified with uploaded PASS artifact: done.
- Generated B1-B6 daily evidence component CLI: done and CI-green.
- Daily evidence input validator, input builder and observation-only source bootstrap: done, CI-green and workflow-green.
- Persisted daily observation source feed, observation-only component mode and Daily Evidence workflow green: done.
- Real daily paper observation source builder with bootstrap rejection: done and CI-green.
- Daily Evidence workflow dispatch integration with fail-safe artifact upload: done, CI-green and workflow-green.
- Real paper observation cadence review: done and CI-green.
- Real paper observation raw data contract and capture template: done and CI-green.
- Daily real paper observation runbook discipline: done and CI-green.
- Paper broker adapter interface and mock paper execution adapter: done and CI-green.
- Alpaca paper adapter with deterministic in-memory transport: done and CI-green.
- VWAP/TWAP paper order slicing: done and CI-green.
- Order reconciliation engine for signal, order, fill and portfolio state: done.
- Daily expected-vs-observed execution reconciliation workflow: done.

## Current execution focus

B1.1 remains the long-running evidence collection period. Phase C is active for paper execution only. Immediate focus remains Phase IP: public framework / private edge separation, while C6 can proceed as paper-only execution-quality reporting on top of C3-C5.

## Do not do yet

- Do not enable real-money execution.
- Do not add new asset classes.
- Do not add ML before rule-based edge is statistically significant.
- Do not open or reuse lockbox evidence casually.
- Do not skip forward paper observation.
- Do not add new proprietary thresholds, setup maps, scoring weights or exit profiles directly to the public repo unless they are explicitly demo-only.
- Do not commit real ranked opportunity reports, raw evidence outputs, provider credentials or private strategy experiments to the public repo.
