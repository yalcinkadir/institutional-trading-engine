# Institutional Trading Engine

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![CI](https://img.shields.io/badge/CI-enabled-brightgreen.svg)
![Status](https://img.shields.io/badge/status-production--oriented-orange.svg)

Institutional-grade market analysis, reporting, screening, governance, runtime orchestration and outcome-tracking platform.

The project is designed as:

- modular
- auditable
- deterministic
- reproducible
- explainable
- risk-first
- production-oriented

The system is NOT intended to be a black-box trading bot.

Instead, it acts as an institutional intelligence platform that:

- analyzes markets
- evaluates regimes
- ranks opportunities
- generates reports
- validates report quality
- stores historical reports
- tracks outcomes
- measures signal quality
- prepares adaptive intelligence
- applies institutional risk overrides
- connects scanner-derived market data into runtime decisions
- persists decision snapshots for auditability

---

# Quick Start

## Requirements

- Python 3.11+
- Git
- Polygon.io API Key
- GitHub Actions enabled

---

## Installation

Clone repository:

```bash
git clone https://github.com/yalcinkadir/institutional-trading-engine.git
cd institutional-trading-engine
```

Create virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Environment Setup

Create:

```text
.env
```

Example:

```env
POLYGON_API_KEY=your_api_key
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

---

## Generate Premarket Report

```bash
python scripts/generate_report.py \
  --type premarket \
  --output reports/premarket/test-report.md
```

---

## Generate Outcome Reports

```bash
python scripts/generate_outcomes.py
```

---

## Run Tests

```bash
pytest
```

---

# Repository Structure

```text
institutional-trading-engine/
├── .github/workflows/
├── docs/
│   └── architecture/
├── reports/
├── scripts/
├── src/
│   ├── bridge/
│   ├── core/
│   ├── data/
│   ├── governance/
│   ├── monitoring/
│   ├── network/
│   ├── optimization/
│   ├── orchestration/
│   ├── outcomes/
│   ├── reporting/
│   ├── runtime/
│   ├── simulation/
│   ├── storage/
│   └── strategy/
├── tests/
├── data/
└── README.md
```

---

# Architecture Reality Check

A critical architectural clarification:

The repository now contains many institutional intelligence modules.

However, not all modules are fully integrated into a single live runtime pipeline yet.

Current state:

| Layer | Status |
|---|---|
| Individual Engines | Implemented |
| Unit Tests | Mostly implemented |
| Architecture Docs | Partially implemented |
| Report Automation | Implemented |
| Outcome Tracking | Implemented |
| Scanner → Runtime Integration | Phase 1 implemented |
| End-to-End Orchestration | Partially implemented |
| Fully Unified Runtime Pipeline | In progress |

---

# How The System Works

```text
Market Data
    ↓
Scanner / Metrics Map
    ↓
VIX Context
    ↓
Scanner → Orchestrator Bridge
    ↓
Institutional Decision Inputs
    ↓
Market Regime / Cross Asset / Tail Risk / Liquidity / Portfolio Layers
    ↓
Decision Fusion
    ↓
Negative Override Layer
    ↓
Governance Controls
    ↓
Runtime Snapshot
    ↓
Decision Log Persistence
    ↓
Runtime State / In-Memory Cache
    ↓
Report Generation
    ↓
Telegram Delivery
    ↓
Historical Storage
    ↓
Outcome Tracking
    ↓
Adaptive Intelligence
```

---

# Runtime Evolution Status

The platform is transitioning from:

```text
collection of institutional intelligence engines
```

into:

```text
continuous institutional runtime system
```

The current implementation intentionally prioritizes:

- explainability
- auditability
- runtime simplicity
- deterministic execution

before introducing:

- distributed runtime systems
- event buses
- async infrastructure
- Redis pub/sub

---

# Phase 1 — Runtime Loop

Implemented:

```text
src/runtime/runtime_loop.py
src/runtime/runtime_state.py
```

Capabilities:

- continuous runtime cycles
- deterministic orchestration
- runtime state tracking
- cycle history
- state snapshots

Validation:

```text
tests/test_runtime_loop.py
```

Architecture documentation:

```text
docs/architecture/runtime_loop.md
```

---

# Phase 2 — Persistence Layer

Implemented:

```text
src/storage/decision_log_store.py
```

Capabilities:

- append-only decision persistence
- runtime audit trail
- historical replay foundation
- institutional memory foundation

Validation:

```text
tests/test_decision_log_store.py
```

Architecture documentation:

```text
docs/architecture/decision_log_store.md
```

Current implementation:

```text
JSONL persistence
```

Future target:

```text
Postgres-backed institutional persistence
```

---

# Phase 3 — Runtime State Layer

Implemented:

```text
src/runtime/in_memory_state_cache.py
```

Capabilities:

- runtime state caching
- shared runtime memory
- temporary orchestration state
- deterministic state access

Validation:

```text
tests/test_in_memory_state_cache.py
```

Important:

Redis was intentionally NOT added yet.

Reason:

```text
Deterministic runtime architecture
is currently more important than distributed infrastructure complexity.
```

---

# Phase 4 — Live Data Integration Layer

Implemented:

```text
src/bridge/scanner_to_orchestrator.py
src/bridge/scanner_market_snapshot_builder.py
src/runtime/runtime_market_snapshot.py
src/runtime/live_runtime_cycle.py
src/scanner.py
```

Capabilities:

- scanner-derived institutional decision inputs
- VIX-aware risk context
- conservative fallback handling for degraded data
- governance-first runtime execution
- immutable runtime market snapshots
- decision log persistence
- runtime state updates
- in-memory latest-state cache updates
- non-fatal runtime cycle handling after report generation

Validation:

```text
tests/test_scanner_to_orchestrator_bridge.py
tests/test_runtime_market_snapshot.py
tests/test_live_runtime_cycle.py
tests/test_scanner_market_snapshot_builder.py
```

Architecture documentation:

```text
docs/architecture/live_runtime_integration.md
```

Important design rule:

```text
The scanner report must never be blocked by runtime-cycle failure.
```

Therefore, `src/scanner.py` writes the markdown report first and runs the institutional runtime cycle afterwards.

---

# Live Runtime Decision Flow

```text
scanner.py
  ↓ metrics_map + vix_data
scanner_to_orchestrator.translate()
  ↓ InstitutionalDecisionInputs
institutional_decision_orchestrator.evaluate()
  ↓ InstitutionalDecisionResult
RuntimeMarketSnapshot.create()
  ↓ immutable audit record
decision_log_store.append()
  ↓ JSONL persistence
runtime_state.update()
  ↓ cycle state
in_memory_state_cache.set()
  ↓ latest runtime access
```

Governance always runs before institutional decision creation.

If governance blocks a cycle:

```text
- no decision snapshot is produced
- no exposure decision is persisted
- a governance block event is persisted for auditability
```

---

# Connected Runtime Decision Flow

The following engines are now connected through:

```text
src/orchestration/institutional_decision_orchestrator.py
```

Connected layers:

```text
Cross Asset Intelligence
→ Tail Risk Engine
→ Liquidity Intelligence
→ Portfolio Intelligence
→ Macro Regime Fusion
→ Slippage Intelligence
→ Multi-Factor Fusion
→ Probabilistic Decision Engine
→ Confidence Weighted Execution
→ Runtime Loop
→ Runtime State
→ Decision Log Persistence
```

This represents the first continuously executable institutional runtime architecture inside the repository.

---

# End-to-End Integration Validation

The repository contains a real integration test:

```text
tests/test_end_to_end_institutional_flow.py
```

This validates that the major intelligence engines:

- communicate together
- exchange outputs
- produce a unified institutional decision
- generate final exposure sizing
- create explainable reasoning

This is one of the most important architectural milestones.

---

# Current Architectural Reality

Currently:

```text
Some modules are fully connected.
Some modules are still standalone intelligence layers.
```

Examples of connected systems:

- Scanner runtime
- VIX-aware market context
- Scanner → Orchestrator bridge
- Macro Regime Fusion
- Cross Asset Intelligence
- Tail Risk Intelligence
- Liquidity Intelligence
- Portfolio Intelligence
- Multi-Factor Fusion
- Probabilistic Decisions
- Confidence-Weighted Execution
- Runtime Loop
- Runtime State
- Decision Persistence

Examples of partially isolated systems:

- Event Bus
- Background Workers
- Redis Runtime
- Postgres Runtime
- Regime Similarity Memory
- Feature Attribution Learning
- Adaptive Weighting Persistence
- Real portfolio position tracking
- Earnings calendar integration
- Structured JSON logging

These exist partly or are planned/tested individually, but are not yet fully integrated into one continuous runtime orchestration layer.

---

# Decision Safety Architecture

One of the most important architectural principles:

```text
High scores alone are NOT enough.
```

The platform includes:

```text
Negative Override Logic
```

Purpose:
Prevent dangerous recommendations even when setup scores are high.

Example:

```text
NVDA
Score: 90
Conviction: High

BUT:
- Earnings tomorrow
- VIX elevated
- Event risk high

→ Final recommendation downgraded automatically
```

---

# Reporting System

Location:

```text
scripts/generate_report.py
src/reporting/
src/scanner.py
```

The platform automatically generates institutional reports.

## Premarket Report

Purpose:
Prepare before the US market opens.

Schedule:
Sunday-Friday before market open.

Contains:

- SPY / QQQ trend analysis
- VIX analysis
- Market Health Score
- breadth analysis
- setup readiness
- watchlists
- risk warnings
- institutional recommendation logic

---

## Postmarket Report

Purpose:
Analyze the completed market session.

Schedule:
Monday-Friday after market close.

Contains:

- leaders
- weak names
- volatility expansion
- signal validation
- relative strength review
- market regime confirmation
- risk override validation

---

## Weekly Report

Purpose:
Strategic institutional review.

Schedule:
Saturday.

Contains:

- regime evolution
- strongest setups
- weak setups
- performance attribution
- strategic observations
- adaptive intelligence preparation
- outcome review

---

# Report Storage

Reports are automatically committed into the repository.

Structure:

```text
reports/
├── premarket/
├── postmarket/
├── weekly/
├── outcomes/
├── premarket-report.md
├── postmarket-report.md
└── weekly-report.md
```

---

# Outcome Tracking System

Location:

```text
scripts/generate_outcomes.py
src/outcomes/
reports/outcomes/
```

Generated files:

```text
reports/outcomes/
├── YYYY-MM-DD-outcomes.md
├── latest-outcomes.md
├── outcome-history.json
└── signal-performance.json
```

Capabilities:

- WIN / LOSS / NEUTRAL classification
- signal extraction
- winrate analysis
- average performance tracking
- signal persistence
- structured JSON output

---

# Telegram Integration

Reports are automatically delivered to Telegram.

Required GitHub Secrets:

```env
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
```

---

# Market Regime Engine

Location:

```text
src/reporting/market_regime.py
```

Data states:

```text
LIVE
PARTIAL
FALLBACK
```

The platform supports:

```text
Graceful Degradation
```

Single feed failures no longer destroy the entire report.

---

# VIX Handling

VIX is used as a risk context input.

Current scanner implementation attempts to fetch:

```text
I:VIX
```

If VIX is unavailable, the runtime does not crash.

Rules:

- scanner can continue with `vix_data = None`
- bridge uses conservative fallback assumptions
- governance does not treat missing VIX as falsely calm
- degraded-data warnings are preserved for auditability

---

# Testing

Run all tests:

```bash
pytest
```

Run specific test file:

```bash
pytest tests/test_negative_override.py
```

Runtime-specific tests:

```bash
pytest tests/test_runtime_loop.py
pytest tests/test_decision_log_store.py
pytest tests/test_in_memory_state_cache.py
pytest tests/test_scanner_to_orchestrator_bridge.py
pytest tests/test_runtime_market_snapshot.py
pytest tests/test_live_runtime_cycle.py
pytest tests/test_scanner_market_snapshot_builder.py
pytest tests/test_end_to_end_institutional_flow.py
```

Test coverage includes:

- governance
- reporting
- optimization
- outcome tracking
- monitoring
- simulation
- probabilistic infrastructure
- negative override logic
- scanner-to-runtime bridge logic
- runtime state handling
- decision persistence
- end-to-end institutional flow

---

# GitHub Actions

Main workflows:

```text
.github/workflows/institutional-reports.yml
.github/workflows/outcome-tracking.yml
.github/workflows/daily-backup.yml
```

Responsible for:

- scheduled reports
- outcome generation
- Telegram delivery
- report archival
- quality validation
- backups
- artifact uploads

---

# Development Standard

No new feature should be added without:

```text
- tests
- architecture documentation
- explainability
- operational notes
- deterministic behavior
```

This is considered an institutional development requirement.

---

# Contributing

Contributions are welcome.

Recommended workflow:

```text
1. Create feature branch
2. Add implementation
3. Add tests
4. Add or update architecture documentation
5. Run pytest
6. Open pull request
```

---

# License

Currently:

```text
All Rights Reserved
```

Until an open-source license is explicitly added.

---

# Current Platform Status

Current maturity:

```text
Production-Oriented Institutional Intelligence Platform
```

Implemented:

- report automation
- historical report storage
- Telegram integration
- governance controls
- optimization layer
- intelligence network
- monitoring
- backups
- probabilistic infrastructure
- outcome tracking automation
- negative override layer
- graceful degradation
- quality validation
- runtime loop
- decision log persistence
- runtime state cache
- scanner-derived live runtime integration
- VIX-aware runtime context
- governance-first runtime cycle

Still missing for full production maturity:

- streaming pipelines
- dashboard UI
- Redis cache
- async workers
- Postgres migration
- feature importance
- regime similarity engine
- ML inference
- observability dashboards
- real market outcome evaluation
- real portfolio position tracking
- earnings calendar integration
- structured JSON logging

---

# Disclaimer

This project is intended for:

- research
- education
- institutional analysis experiments

It is not financial advice.
