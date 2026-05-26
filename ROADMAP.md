# Institutional Trading Engine Roadmap

Status date: 2026-05-26  
Current state: Phase B12 persisted daily observation source feed, observation-only component mode, CI-green and Daily Evidence workflow-green are implemented. Phase A Evidence Hygiene implemented and CI-green. P36-P47 validation stack implemented. Live trading is not authorized by code.

## Strategic direction

The next stage is not more scanner features. The next stage is institutional evidence.

The project is already a strong research and decision-support system. To become top-tier, the roadmap now prioritizes:

1. survivorship-safe data
2. statistically defensible edge validation
3. forward paper evidence
4. execution realism
5. portfolio-level risk attribution
6. multi-strategy expansion only after the base edge is proven

Hard rule: no live capital before real forward evidence, drift detection, regime-change monitoring and position-level risk attribution are in place.

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
| B13 | Replace bootstrap incoming records with real persisted daily paper observation source records | P0 | Critical | Next |

## Phase C — Execution Reality

Target window: parallel with Phase B  
Goal: ensure simulated edge survives realistic execution assumptions.

| ID | Task | Priority | Impact | Status |
|---|---|---:|---:|---|
| C1 | Define broker adapter interface for paper execution first | P0 | High | Planned |
| C2 | Add Alpaca paper adapter as first broker implementation | P1 | High | Planned |
| C3 | Add VWAP/TWAP order slicing | P1 | High | Planned |
| C4 | Add order reconciliation engine for signal, order, fill and portfolio state | P1 | High | Planned |
| C5 | Add live vs. backtest daily reconciliation workflow | P1 | High | Planned |
| C6 | Add fill-quality report for slippage, spread, delay and partial fills | P2 | Medium | Planned |
| C7 | Add execution kill switch when execution drift exceeds limits | P1 | High | Planned |

## Phase D — Strategy Expansion

Start only after Phase B and C produce credible evidence.

| ID | Task | Priority | Impact | Status |
|---|---|---:|---:|---|
| D1 | Add mean-reversion strategy sleeve with separate validation | P1 | High | Planned |
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
| E4 | Add meta-labeling layer for trade/no-trade decision after primary signal | P2 | Medium | Planned |
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

## Current execution focus

B1.1 remains the long-running evidence collection period. The next step is B13: replace bootstrap incoming records with real persisted daily paper observation source records. Phase B must remain observation-only until enough forward evidence exists.

## Do not do yet

- Do not enable live capital.
- Do not add crypto or forex.
- Do not add ML before rule-based edge is statistically significant.
- Do not open or reuse lockbox evidence casually.
- Do not skip forward paper observation.
