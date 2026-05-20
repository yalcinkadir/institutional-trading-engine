# Institutional Trading Engine

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![CI](https://img.shields.io/badge/CI-enabled-brightgreen.svg)
![Status](https://img.shields.io/badge/status-production--oriented-orange.svg)

Institutional Trading Engine is a production-oriented market intelligence, screening, reporting, runtime orchestration and outcome-learning platform.

The long-term goal is to become a high-quality institutional market screener that does more than generate reports:

```text
Market analysis
→ Signal generation
→ Entry / Exit monitoring
→ Lifecycle tracking
→ Outcome evaluation
→ Expectancy learning
→ Better future scoring
```

The system is NOT a black-box trading bot and does NOT place live trades.

It is designed as an institutional decision-support and research platform that:

- analyzes market regimes
- evaluates risk conditions
- ranks opportunities
- generates premarket, intraday, postmarket and weekly reports
- produces machine-readable signal files
- stores signal history in the repository
- monitors entries, stops and targets
- records signal lifecycle events
- evaluates triggered vs expired vs pending signals separately
- tracks real outcomes from market data
- builds adaptive expectancy profiles
- prepares future scoring improvements
- persists runtime and decision history for auditability

---

# Core Principles

The project is designed to be:

- modular
- auditable
- deterministic
- reproducible
- explainable
- risk-first
- testable
- production-oriented

The most important design rule:

```text
A signal is not a trade until its entry trigger is hit.
```

Therefore:

- untriggered signals are not counted as losses
- expired signals are tracked separately
- triggered signals are evaluated with real outcomes
- stop/target events are stored as lifecycle data
- historical learning is based on lifecycle-aware outcomes

---

# Current High-Level Pipeline

```text
Market Data
    ↓
Market Regime / Screener / Decision Engine
    ↓
Institutional Report
    ↓
Machine-Readable Signal JSON
    ↓
Entry / Exit Watcher
    ↓
Alerts + Signal Lifecycle JSONL
    ↓
Lifecycle-Aware Outcome Tracking
    ↓
Adaptive Expectancy Profiles
    ↓
Future Scoring Adjustments
```

The current implementation already supports the full structural flow:

```text
Reports → Signals → Watcher → Alerts → Lifecycle → Outcomes → Expectancy
```

The next major future step is to feed expectancy results back into scoring.

---

# Quick Start

## Requirements

- Python 3.11+
- Git
- Polygon.io API key
- GitHub Actions enabled

Optional:

- Telegram bot token
- Telegram chat ID
- webhook endpoint for external notifications

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

Create `.env` locally or configure GitHub Secrets:

```env
POLYGON_API_KEY=your_polygon_api_key
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id
REPORT_WEBHOOK_URL=optional_webhook_url
```

---

# Main Commands

## Generate a Premarket Report

```bash
python scripts/generate_report.py \
  --type premarket \
  --output reports/premarket/test-report.md
```

## Generate an Intraday Report

```bash
python scripts/generate_report.py \
  --type intraday \
  --output reports/intraday/test-report.md
```

## Generate a Postmarket Report

```bash
python scripts/generate_report.py \
  --type postmarket \
  --output reports/postmarket/test-report.md
```

## Generate a Weekly Report

```bash
python scripts/generate_report.py \
  --type weekly \
  --output reports/weekly/test-report.md
```

## Run the Entry / Exit Watcher

```bash
python scripts/run_entry_exit_watcher.py \
  --signals-file reports/signals/latest-signals.json
```

## Generate Lifecycle-Aware Outcomes

```bash
python scripts/generate_outcomes.py --days 7
```

## Update Expectancy Report

```bash
python scripts/update_outcomes.py \
  --decision-log data/decision_log.csv \
  --output reports/expectancy-report.md
```

JSONL decision logs are also supported by the reader layer.

## Run Tests

```bash
pytest
```

---

# Repository Structure

```text
institutional-trading-engine/
├── .github/
│   └── workflows/
│       ├── institutional-reports.yml
│       ├── entry-exit-watcher.yml
│       ├── outcome-tracking.yml
│       └── daily-backup.yml
│
├── data/
│   ├── decision_log.csv              # CSV decision history when produced
│   ├── decision_log.jsonl            # JSONL runtime/audit history when produced
│   └── signal_lifecycle.jsonl        # Entry/exit lifecycle events
│
├── docs/
│   └── architecture/
│
├── reports/
│   ├── premarket/
│   ├── intraday/
│   ├── postmarket/
│   ├── weekly/
│   ├── signals/
│   │   ├── YYYY-MM-DD-signals.json
│   │   ├── YYYY-MM-DD-signals.md
│   │   └── latest-signals.json
│   ├── alerts/
│   │   ├── YYYY-MM-DD-alerts.json
│   │   └── latest-alerts.json
│   ├── outcomes/
│   │   ├── YYYY-MM-DD-outcomes.json
│   │   ├── YYYY-MM-DD-outcomes.md
│   │   ├── latest-outcomes.md
│   │   └── outcome-history.json
│   └── expectancy-report.md
│
├── scripts/
│   ├── generate_report.py
│   ├── run_entry_exit_watcher.py
│   ├── generate_outcomes.py
│   └── update_outcomes.py
│
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
│   ├── signals/
│   ├── simulation/
│   ├── storage/
│   ├── strategy/
│   └── watchers/
│
└── tests/
```

---

# Architecture Reality Check

The repository contains many institutional intelligence modules.

Not all modules are fully integrated into a single live, continuously running production pipeline yet.

Current state:

| Layer | Status |
|---|---|
| Report Automation | Implemented |
| Premarket / Intraday / Postmarket / Weekly Reports | Implemented |
| Machine-Readable Signals | Implemented |
| Entry / Exit Watcher | Implemented as testable V1 |
| Alerts Persistence | Implemented |
| Signal Lifecycle JSONL | Implemented |
| Lifecycle-Aware Outcomes | Implemented |
| Entry-Type Expectancy Profiles | Implemented |
| Runtime Loop | Implemented |
| Decision Persistence | Implemented |
| End-to-End Institutional Flow | Partially implemented |
| Fully Unified Continuous Runtime | In progress |
| Live Portfolio Tracking | Not yet implemented |
| Broker Execution | Not implemented |
| Streaming Intraday Data | Not implemented |
| Dashboard UI | Not implemented |

---

# Reporting System

Reports are generated through:

```text
scripts/generate_report.py
```

Supported report types:

```text
premarket
intraday
postmarket
weekly
```

Market reports generate both:

```text
Markdown report
Signal JSON / Markdown files
```

Weekly reports are strategic-only and do not generate signals.

---

## Premarket Report

Purpose:
Prepare before the US market opens.

Contains:

- market regime
- market health score
- SPY / QQQ trend context
- VIX-aware risk context where available
- breadth analysis
- cross-asset regime
- decision engine summary
- actionable setups
- blocked / no-trade names
- Entry / Stop / Target levels when available

---

## Intraday Report

Purpose:
Capture market conditions during the session without overwriting postmarket reports.

Stored separately:

```text
reports/intraday/YYYY-MM-DD-intraday.md
reports/intraday-report.md
```

The intraday workflow currently uses the same reporting engine but stores output separately.

This prevents the mid-session run from overwriting the real postmarket report.

---

## Postmarket Report

Purpose:
Analyze the completed market session and generate next-session candidates.

Contains:

- regime confirmation
- decision engine output
- watchlist candidates
- leaders / weak names where available
- risk warnings
- signal candidates for future monitoring

---

## Weekly Report

Purpose:
Strategic institutional review.

Contains:

- regime evolution
- strongest setups
- weak setups
- performance attribution
- strategic observations
- adaptive intelligence preparation
- outcome review

---

# Signal Generation

Signals are generated by:

```text
src/signals/signal_generator.py
```

and saved by:

```text
scripts/generate_report.py
```

Generated files:

```text
reports/signals/YYYY-MM-DD-signals.json
reports/signals/YYYY-MM-DD-signals.md
reports/signals/latest-signals.json
```

A signal is machine-readable and contains:

```json
{
  "symbol": "NVDA",
  "action": "BUY_WATCH",
  "setup_type": "momentum_breakout",
  "decision": "approved",
  "risk_tier": "tier_1",
  "position_size": 1.0,
  "close": 226.12,
  "entry_trigger": 228.4,
  "entry_type": "break_above",
  "stop_loss": 219.8,
  "target_1": 240.0,
  "target_2": 252.0,
  "risk_reward": 1.35,
  "atr_pct": 2.1,
  "setup_score": 82,
  "regime_alignment": 0.82,
  "valid_until": "2026-05-23",
  "market_regime": "bullish",
  "generated_at": "2026-05-20T21:00:00Z",
  "notes": "regime-aligned setup"
}
```

Signal levels are also merged back into the main report before rendering, so the Markdown report can show:

```text
Entry | Stop | Target 1 | Target 2 | R:R
```

---

# Signal Lifecycle Model

Signals move through lifecycle states.

Current supported statuses:

```text
PENDING
TRIGGERED
TARGET_1_HIT
TARGET_2_HIT
STOP_HIT
EXPIRED
UNTRIGGERED
CANCELLED_BY_REGIME_CHANGE
```

Meaning:

| Status | Meaning |
|---|---|
| PENDING | Signal exists, entry not hit yet |
| TRIGGERED | Entry trigger was hit |
| TARGET_1_HIT | First target was reached |
| TARGET_2_HIT | Second target was reached |
| STOP_HIT | Stop level was reached |
| EXPIRED | Signal expired before triggering |
| UNTRIGGERED | Signal remained inactive during evaluation window |
| CANCELLED_BY_REGIME_CHANGE | Future state for cancelled signals |

Critical rule:

```text
PENDING / EXPIRED / UNTRIGGERED signals are not counted as losing trades.
```

They are signal-quality information, not executed trade outcomes.

---

# Entry / Exit Watcher

The watcher is implemented in:

```text
src/watchers/entry_exit_watcher.py
scripts/run_entry_exit_watcher.py
```

It evaluates signal files against injected price bars.

The core watcher logic is pure and testable. It does not fetch market data directly.

The CLI runner is responsible for:

```text
latest-signals.json
→ Polygon daily bars
→ watcher evaluation
→ alerts
→ lifecycle JSONL
→ updated latest-signals.json
```

Current watcher events:

```text
ENTRY_TRIGGERED
STOP_HIT
TARGET_1_HIT
TARGET_2_HIT
EXPIRED
```

Conservative backtest rule:

```text
If a single price bar touches both stop and target, STOP_HIT is evaluated first.
```

This avoids optimistic backtest bias.

Generated files:

```text
reports/alerts/YYYY-MM-DD-alerts.json
reports/alerts/latest-alerts.json
data/signal_lifecycle.jsonl
```

Example alert:

```json
{
  "alert_type": "ENTRY_TRIGGERED",
  "symbol": "NVDA",
  "timestamp": "2026-05-21T15:00:00Z",
  "signal_date": "2026-05-20",
  "price": 228.4,
  "trigger_price": 228.4,
  "stop_loss": 219.8,
  "target_1": 240.0,
  "target_2": 252.0,
  "previous_status": "PENDING",
  "new_status": "TRIGGERED"
}
```

---

# Outcome Tracking

Outcome generation is handled by:

```text
scripts/generate_outcomes.py
```

Generated files:

```text
reports/outcomes/YYYY-MM-DD-outcomes.json
reports/outcomes/YYYY-MM-DD-outcomes.md
reports/outcomes/latest-outcomes.md
reports/outcomes/outcome-history.json
```

The outcome system is now lifecycle-aware.

It separates:

```text
TRIGGERED
TARGET_1_HIT
TARGET_2_HIT
STOP_HIT
PENDING
EXPIRED
UNTRIGGERED
```

Only triggered signals are evaluated as trade-like outcomes.

Non-triggered states are tracked but not treated as losses.

Outcome report examples:

```text
NVDA [WIN / TRIGGERED]
AAPL [EXPIRED / EXPIRED]
MSFT [PENDING / PENDING]
```

The primary performance horizon is currently:

```text
5 trading days
```

Also tracked:

```text
1d result
5d result
20d result
performance_percent
classification
lifecycle_status
```

Classifications:

```text
WIN
LOSS
NEUTRAL
PENDING
EXPIRED
UNTRIGGERED
```

---

# Adaptive Expectancy Learning

Expectancy reporting is handled by:

```text
scripts/update_outcomes.py
src/adaptive_expectancy.py
src/outcome_pipeline.py
```

Generated file:

```text
reports/expectancy-report.md
```

The system now builds expectancy profiles by:

```text
setup_type
market_regime / market_state
entry_type
setup_type + regime
setup_type + regime + entry_type
```

Examples of future learning targets:

```text
bullish::momentum_breakout::break_above
neutral::pullback_continuation::pullback_to
risk_off::defensive_rotation::at_market
```

The goal is to learn patterns such as:

```text
Momentum breakout + bullish regime + break_above
→ positive expectancy
→ future score can be increased
```

or:

```text
Momentum breakout + neutral regime + break_above
→ negative expectancy
→ future score should be reduced
```

Current adaptive recommendations:

```text
increase_risk_selectively
maintain_exposure
reduce_size
avoid_or_block
insufficient_data
```

The next major future step is:

```text
Feed expectancy profiles back into the scoring engine.
```

---

# Runtime Architecture

Runtime modules include:

```text
src/runtime/runtime_loop.py
src/runtime/runtime_state.py
src/runtime/in_memory_state_cache.py
src/runtime/runtime_market_snapshot.py
src/runtime/live_runtime_cycle.py
```

The runtime system is designed around deterministic institutional cycles.

Runtime flow:

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

# Persistence Strategy

The project currently uses repository-based persistence.

Important persisted outputs:

```text
reports/
data/
```

Key persisted files:

```text
reports/signals/*.json
reports/alerts/*.json
reports/outcomes/*.json
reports/expectancy-report.md
data/decision_log.csv
data/decision_log.jsonl
data/signal_lifecycle.jsonl
```

Current persistence style:

```text
Git repository + JSON / JSONL / CSV files
```

Future production target:

```text
Postgres-backed institutional persistence
```

The current Git-based approach is useful because it provides:

- audit trail
- versioned signal history
- reproducibility
- easy inspection
- simple GitHub Actions integration

But it is not the final production-grade storage layer.

---

# GitHub Actions Workflows

Main workflows:

```text
.github/workflows/institutional-reports.yml
.github/workflows/entry-exit-watcher.yml
.github/workflows/outcome-tracking.yml
.github/workflows/daily-backup.yml
```

---

## Institutional Reports Workflow

File:

```text
.github/workflows/institutional-reports.yml
```

Schedule:

```text
12:30 UTC  Premarket
15:00 UTC  Intraday
21:00 UTC  Postmarket
Saturday   Weekly
```

Responsibilities:

- generate reports
- generate signals
- validate report quality
- commit reports and data
- upload artifacts
- send Telegram summaries if configured

Important:

```text
Intraday output is stored separately and does not overwrite postmarket output.
```

---

## Entry / Exit Watcher Workflow

File:

```text
.github/workflows/entry-exit-watcher.yml
```

Schedule:

```text
15:00 UTC   First intraday check
17:30 UTC   Mid-session check
21:00 UTC   Postmarket lifecycle check
```

Responsibilities:

- load latest signals
- check entry/stop/target events
- update signal statuses
- write alerts
- append lifecycle events
- commit reports/signals, reports/alerts and data
- send Telegram alert summary if configured

---

## Outcome Tracking Workflow

File:

```text
.github/workflows/outcome-tracking.yml
```

Schedule:

```text
02:00 UTC daily
```

Responsibilities:

- generate lifecycle-aware outcomes
- update expectancy report
- commit outcome files and data
- upload artifacts

The workflow is robust against missing decision logs.

It prefers:

```text
data/decision_log.csv
```

and can fall back to:

```text
data/decision_log.jsonl
```

---

# Decision Safety Architecture

One of the most important architectural principles:

```text
High scores alone are NOT enough.
```

The platform includes risk and override logic.

Purpose:
Prevent dangerous recommendations even when setup scores are high.

Example:

```text
NVDA
Score: 90
Conviction: High

BUT:
- VIX elevated
- market breadth weak
- event risk high

→ Final recommendation can be downgraded or blocked
```

Important recent fix:

```text
Data quality degradation is not treated as liquidity stress.
```

Previously, partial data could cause permanent blocking. Now degraded data reduces confidence/sizing instead of automatically blocking all signals.

---

# VIX Handling

VIX is used as a risk context input.

Current scanner implementation attempts to fetch:

```text
I:VIX
```

If VIX is unavailable, the system should not crash.

Rules:

- scanner can continue with `vix_data = None`
- bridge uses conservative fallback assumptions
- governance does not treat missing VIX as falsely calm
- missing VIX should reduce confidence, not automatically block every signal
- degraded-data warnings are preserved for auditability

---

# Current Limitations

The system is stronger than a simple report generator, but it is not yet a fully institutional production platform.

Current limitations:

- no live broker execution
- no real portfolio position tracking
- no real-time websocket watcher
- no streaming intraday bars in the core implementation
- Git-based persistence is not final production storage
- no dashboard UI yet
- no Postgres persistence yet
- expectancy results are not yet automatically fed back into scoring
- no regime similarity memory yet
- no ML inference layer yet
- no full observability dashboard yet

Important:

```text
This project currently supports research, screening, alerting and lifecycle analysis.
It does not execute trades.
```

---

# Testing

Run all tests:

```bash
pytest
```

Useful targeted tests:

```bash
pytest tests/test_runtime_loop.py
pytest tests/test_decision_log_store.py
pytest tests/test_in_memory_state_cache.py
pytest tests/test_scanner_to_orchestrator_bridge.py
pytest tests/test_runtime_market_snapshot.py
pytest tests/test_live_runtime_cycle.py
pytest tests/test_scanner_market_snapshot_builder.py
pytest tests/test_end_to_end_institutional_flow.py
pytest tests/test_entry_exit_watcher.py
```

Test coverage includes:

- governance
- reporting
- signal generation
- entry/exit watcher logic
- lifecycle persistence
- outcome tracking
- adaptive expectancy
- runtime state handling
- decision persistence
- scanner-to-runtime bridge logic
- end-to-end institutional flow

Watcher tests specifically cover:

- entry trigger detection
- stop hit detection
- target 1 detection
- target 2 detection
- expiry detection
- terminal status protection
- symbol-specific updates
- alert persistence
- lifecycle JSONL persistence
- updated signal file persistence

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

For market intelligence features, also require:

```text
- machine-readable output
- lifecycle-aware state handling
- non-fatal failure mode
- clear audit trail
```

---

# Roadmap

## Implemented Foundation

- report automation
- signal generation
- signal persistence
- Entry / Exit Watcher V1
- alerts persistence
- lifecycle JSONL
- lifecycle-aware outcomes
- entry-type expectancy profiles
- runtime loop
- decision persistence
- VIX-aware runtime context
- governance-first runtime cycle

## Next High-Value Steps

1. Feed expectancy profiles back into the scoring engine.
2. Add explicit `signal_id` to every generated signal.
3. Prevent duplicate lifecycle events for the same signal/event pair.
4. Improve intraday data support with higher-frequency bars if Polygon plan allows.
5. Add stronger portfolio state tracking.
6. Add dashboard or static HTML reporting.
7. Move long-term persistence from Git files to Postgres.
8. Add structured JSON logging.
9. Add regime similarity memory.
10. Add scoring adjustment history.

---

# Example End-to-End Day

```text
12:30 UTC — Premarket report
  → reports/premarket/YYYY-MM-DD-premarket.md
  → reports/signals/YYYY-MM-DD-signals.json

15:00 UTC — Intraday report + watcher
  → reports/intraday/YYYY-MM-DD-intraday.md
  → watcher checks entries and exits
  → reports/alerts/YYYY-MM-DD-alerts.json
  → data/signal_lifecycle.jsonl

17:30 UTC — Watcher check
  → additional entry/stop/target alerts if triggered

21:00 UTC — Postmarket report + watcher
  → reports/postmarket/YYYY-MM-DD-postmarket.md
  → updated signals
  → updated lifecycle

02:00 UTC — Outcome tracking
  → reports/outcomes/YYYY-MM-DD-outcomes.md/json
  → reports/expectancy-report.md
```

---

# License

Currently:

```text
All Rights Reserved
```

Until an open-source license is explicitly added.

---

# Disclaimer

This project is intended for:

- research
- education
- institutional analysis experiments
- systematic market screening
- signal lifecycle analysis

It is not financial advice.

It does not place trades.

Any trading or investment decision remains the responsibility of the user.
