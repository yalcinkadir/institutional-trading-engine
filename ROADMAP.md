# Institutional Trading Engine Roadmap

Status date: 2026-05-25  
Current state: P36-P47 implemented, CI green, live trading is not authorized by code.

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
| A5 | Replace linear slippage heuristic with square-root impact plus regime multipliers | P1 | High | Next |
| A6 | Add Deflated Sharpe Ratio and bootstrap confidence intervals to edge validation | P1 | High | Planned |
| A7 | Convert Polygon client retry/rate-limit output to structured logging | P2 | Medium | Planned |
| A8 | Add cache locking for `.cache/polygon` writes | P2 | Medium | Planned |
| A9 | Update `CHANGELOG.md` and `SETUP_NOTES.md` for P47 readiness state | P2 | Medium | Planned |
| A10 | Document quarterly secrets rotation policy | P2 | Medium | Planned |

## Phase B — Real Forward Evidence

Target window: 3-6 months  
Goal: prove whether the rule-based system has live-observable edge before adding complexity.

| ID | Task | Priority | Impact | Status |
|---|---|---:|---:|---|
| B1 | Run 3-6 months of paper observation with daily reconciliation | P0 | Critical | Planned |
| B2 | Add live/paper vs. backtest drift detection | P0 | High | Planned |
| B3 | Add SPRT or equivalent sequential test for edge decay | P1 | High | Planned |
| B4 | Add regime-change detection using HMM or BOCPD-style logic | P1 | High | Planned |
| B5 | Add position-level risk attribution by beta, sector, factor and single-name contribution | P1 | High | Planned |
| B6 | Add Monte Carlo robustness suite with bootstrap and permutation tests | P1 | Medium | Planned |
| B7 | Emit a daily evidence report for paper/live observation | P2 | Medium | Planned |

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

## Current execution focus

A3 and A4 are complete. Edge-evidence diagnostics are visible in artifacts and workflow logs. The next implementation step is A5: replace the current linear slippage heuristic with a square-root impact model plus regime multipliers. That is the correct next move because execution cost realism directly affects whether simulated edge survives contact with the market.

## Do not do yet

- Do not enable live capital.
- Do not add crypto or forex.
- Do not add ML before rule-based edge is statistically significant.
- Do not open or reuse lockbox evidence casually.
- Do not add more features on top of a non-survivorship-safe data foundation.