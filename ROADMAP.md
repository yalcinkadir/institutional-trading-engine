# Institutional Trading Engine Roadmap

Status date: 2026-05-28

Current state: TG1 Telegram research-only report dispatcher is implemented. IP1 public/private edge boundary guardrail is implemented. IP2 public repository hygiene and private-edge handling policy is implemented. Phase C3-C7 paper execution control and audit infrastructure is implemented. BT1 deterministic backtest run contract is now the active backtesting foundation. Real-money execution is not authorized by code.

## Strategic direction

The project is already a strong research and decision-support framework. The next stage is institutional evidence discipline:

1. public framework / private edge separation
2. deterministic backtest contracts
3. strategy scenario matrix
4. walk-forward and out-of-sample validation
5. paper-observation comparison
6. report delivery and audit trail
7. portfolio-level risk attribution

Hard rule: no real-money execution before forward evidence, drift monitoring, regime monitoring and risk attribution are mature.

Hard IP rule: the public repository may demonstrate framework behavior and reproducibility, but proprietary production edge configuration must stay outside public source control.

## Phase IP — Public Framework / Private Edge Separation

| ID | Task | Priority | Impact | Status |
|---|---|---:|---:|---|
| IP1 | Public/private edge boundary scanner and policy | P0 | Critical | Done |
| IP2 | Public repository hygiene and private-edge handling policy | P0 | Critical | Done |
| IP3 | Replace production-like constants with demo defaults or external config interfaces | P0 | Critical | Planned |
| IP4 | Optional private-edge adapter/import boundary | P0 | Critical | Planned |
| IP5 | Move real reports and non-synthetic artifacts out of public version control | P0 | Critical | Planned |
| IP6 | Expand artifact and private-config ignore rules | P0 | High | Planned |

## Phase TG — Report Delivery

| ID | Task | Priority | Impact | Status |
|---|---|---:|---:|---|
| TG1 | Telegram report dispatcher with research-only guardrails | P1 | High | Done |
| TG2 | Integrate Telegram summaries into evidence/report workflows | P2 | Medium | Planned |
| TG3 | Add report templates for Daily Evidence, Fill Quality, Kill Switch and Backtest Summary | P2 | Medium | Planned |

## Phase BT — Backtesting Foundation

Goal: make strategy testing reproducible before scenario expansion or optimization.

| ID | Task | Priority | Impact | Status |
|---|---|---:|---:|---|
| BT1 | Deterministic Backtest Run Contract with stable contract id, validation, JSON export and CLI | P0 | Critical | In Review |
| BT2 | Strategy Scenario Test Matrix for user-provided hypotheses | P0 | Critical | Planned |
| BT3 | Walk-forward and out-of-sample runner | P0 | Critical | Planned |
| BT4 | Backtest vs paper-observation comparison | P1 | High | Planned |
| BT5 | Backtest summary report and Telegram-safe summary | P1 | High | Planned |

## Phase B — Real Forward Evidence

B1.1 remains the long-running observation-only evidence collection period.

| ID | Task | Priority | Impact | Status |
|---|---|---:|---:|---|
| B1-B17 | Daily evidence, observation cadence, paper observation source and validation pipeline | P0 | Critical | Done |
| B1.1 | 3-6 month observation-only evidence collection | P0 | Critical | In Progress |

## Phase C — Execution Reality

Paper-execution and audit infrastructure only. No real-money execution authorization.

| ID | Task | Priority | Impact | Status |
|---|---|---:|---:|---|
| C1 | Paper broker adapter interface | P0 | High | Done |
| C2 | Alpaca paper adapter | P1 | High | Done |
| C3 | VWAP/TWAP paper order slicing | P1 | High | Done |
| C4 | Order reconciliation engine | P1 | High | Done |
| C5 | Daily execution reconciliation workflow | P1 | High | Done |
| C6 | Fill-quality report | P2 | Medium | Done |
| C7 | Execution kill switch governance | P1 | High | Done |

## Phase D — Strategy Expansion

Start only after private-edge boundary and BT foundation are stable.

| ID | Task | Priority | Impact | Status |
|---|---|---:|---:|---|
| D1 | Mean-reversion strategy sleeve behind private-edge boundary or demo-only public constants | P1 | High | Planned |
| D2 | Multi-strategy risk-parity allocator | P1 | High | Planned |
| D3 | Factor, sector and style exposure caps | P1 | High | Planned |
| D4 | Correlation-aware position sizing | P1 | High | Planned |

## Phase E — Continuous Institutionalization

| ID | Task | Priority | Impact | Status |
|---|---|---:|---:|---|
| E1 | Continuous backtesting in CI | P1 | Medium | Planned |
| E2 | PR gates against evidence baselines | P1 | Medium | Planned |
| E3 | Automated daily backtest vs observation reconciliation | P1 | High | Planned |
| E4 | Capacity and portfolio risk modelling | P2 | High | Planned |
| E5 | Evidence, drift, risk and execution dashboard | P2 | Medium | Planned |

## Current execution focus

BT1 is the current implementation focus. After BT1 is green and merged, the next step is BT2: strategy scenario matrix for user-provided hypotheses.

## Do not do yet

- Do not enable real-money execution.
- Do not add auto-execution.
- Do not add new asset classes before evidence discipline is stable.
- Do not add ML before rule-based evidence is statistically defensible.
- Do not skip forward paper observation.
- Do not commit real private thresholds, setup maps, scoring weights, reports or private experiment results.
- Do not send Telegram messages that imply live trading authorization or contain private edge parameters.
