# Institutional Trading Engine

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![CI](https://img.shields.io/badge/CI-pytest-brightgreen.svg)
![Status](https://img.shields.io/badge/status-production--oriented-orange.svg)

Institutional Trading Engine is a production-oriented market intelligence, screening, reporting, runtime orchestration, observability, historical validation and decision-support platform.

The system is designed for research and decision support. It does not place live trades.

## Core Capabilities

- market regime analysis
- decision confidence scoring
- cross-asset market-data coverage
- event-risk placeholder metadata
- optional SQLite runtime persistence
- static dashboard HTML reporting
- signal generation with entry, stop and target planning
- watcher-based lifecycle tracking
- manual portfolio synchronization
- historical Polygon data ingestion
- historical Entry / Stop / Exit backtesting
- out-of-sample validation
- paper-live observation
- operational readiness review
- scheduled decision-support dry runs
- persistent report archive
- feedback and expectancy analysis

## Core Flow

```text
Market analysis
→ Expanded universe scan
→ Event-risk metadata check
→ Scanner metrics normalization
→ Signal generation
→ Entry / Stop / Exit quality engines
→ Trade plan validation
→ Decision confidence scoring
→ Watcher lifecycle tracking
→ Manual portfolio sync
→ Optional SQLite persistence
→ Static dashboard reporting
→ Historical validation
→ Feedback aggregation
→ Human review
```

## Main Test Commands

```bash
pytest
pytest tests/test_decision_confidence.py
pytest tests/test_static_dashboard.py
pytest tests/test_sqlite_persistence.py
pytest tests/test_event_risk_engine.py
pytest tests/test_symbol_universe.py
pytest tests/test_historical_entry_exit_backtest.py
pytest tests/test_out_of_sample_validation.py
pytest tests/test_paper_live_observation.py
pytest tests/test_operational_readiness_review.py
pytest tests/test_scheduled_decision_support_dry_run.py
pytest tests/test_report_archive.py
pytest tests/test_entry_exit_watcher_health.py
pytest tests/test_manual_portfolio_sync.py
```

## P36 Decision Confidence Scoring

Implemented in:

```text
src/decision_confidence.py
docs/operations/confidence_scoring.md
tests/test_decision_confidence.py
```

P36 separates confidence into three independent layers:

```text
asset setup score      weight 0.45
market health score   weight 0.35
regime alignment      weight 0.20
```

Formula:

```text
confidence = setup_score * 0.45 + market_health_score * 0.35 + regime_alignment_score * 0.20
```

Regime alignment mapping:

```text
Tier 1   100
Tier 2    65
Tier 3    35
No Trade   0
```

This avoids counting market-health factors again inside confidence scoring.

## Static Dashboard HTML Reporting

Implemented in:

```text
src/operations/static_dashboard.py
scripts/build_static_dashboard.py
docs/operations/static_dashboard.md
tests/test_static_dashboard.py
.github/workflows/static-dashboard.yml
```

Build locally:

```bash
python scripts/build_static_dashboard.py \
  --output-html reports/dashboard/index.html \
  --output-json reports/dashboard/dashboard.json \
  --json
```

Outputs:

```text
reports/dashboard/index.html
reports/dashboard/dashboard.json
```

Dashboard status values:

```text
PASS
PARTIAL
WARN
EMPTY
```

## SQLite Runtime Persistence

Implemented in:

```text
src/operations/sqlite_persistence.py
scripts/check_sqlite_persistence.py
docs/operations/sqlite_persistence.md
tests/test_sqlite_persistence.py
.github/workflows/sqlite-persistence.yml
```

Smoke check:

```bash
python scripts/check_sqlite_persistence.py \
  --db data/runtime/runtime.sqlite \
  --write-smoke-record \
  --json
```

## Event Risk Placeholder Metadata

Implemented in:

```text
src/event_risk_engine.py
docs/operations/event_risk_placeholder.md
tests/test_event_risk_engine.py
```

Default metadata:

```text
event_risk_available=false
event_risk_source=static_placeholder
event_risk_confidence=low
event_risk_is_placeholder=true
```

## Market Data Coverage

Configured in:

```text
src/config.py
docs/operations/market_data_coverage.md
tests/test_symbol_universe.py
```

Default groups:

```text
core_indices: SPY, QQQ, IWM, DIA
rates_bonds: TLT, IEF, SHY
dollar_proxy: UUP
sectors: XLK, XLF, XLE, XLV, XLY, XLP, XLI, XLU, XLB, XLRE
mega_caps: AAPL, MSFT, NVDA, AMZN, GOOGL, META, TSLA
semiconductors: SMH, MU, AMD, AVGO
commodities: GLD, SLV, USO
legacy_quality: CSCO
```

## Key Local Commands

```bash
python scripts/sync_manual_portfolio_state.py \
  --snapshot data/manual_portfolio_snapshot.example.json \
  --portfolio-state-out data/portfolio_state.json \
  --report-json-out reports/portfolio/manual-portfolio-sync.json \
  --report-md-out reports/portfolio/manual-portfolio-sync.md
```

```bash
python scripts/run_out_of_sample_validation.py \
  --symbols SPY,QQQ,IWM,DIA,TLT,IEF,SHY,UUP,XLK,XLF,XLE,XLV,XLY,XLP,XLI,XLU,XLB,XLRE,GLD,SLV,USO \
  --bars-root data/historical/bars/1day \
  --split-date 2023-01-01 \
  --lookback-bars 20 \
  --every-nth-signal 20 \
  --max-bars 20
```

```bash
python scripts/archive_reports.py
```

## GitHub Actions

```text
Actions → Static Dashboard → Run workflow
Actions → SQLite Persistence → Run workflow
Actions → Manual Portfolio Sync → Run workflow
Actions → Historical Entry Exit Backtest → Run workflow
Actions → Out-of-Sample Historical Validation → Run workflow
Actions → Paper Live Observation → Run workflow
Actions → Entry Exit Watcher Health → Run workflow
Actions → Operational Readiness Review → Run workflow
Actions → Scheduled Decision-Support Dry Run → Run workflow
Actions → Archive Reports → Run workflow
```

## Decision Quality Roadmap

Detailed roadmap:

```text
docs/roadmap/decision_quality_p36_p40.md
```

Sequence:

```text
P36 Confidence Score Double Counting Fix
P37 Probabilistic Engine Softmax Normalization
P38 Regime Similarity Weighted Distance + Cosine Similarity
P39 Adaptive Feedback Decay
P40 MultiFactorFusion Recalibration
```

## Implemented Components

| Layer | Status |
|---|---|
| Decision Confidence Scoring | Implemented |
| Static Dashboard HTML Reporting | Implemented |
| SQLite Runtime Persistence | Implemented |
| Event Risk Placeholder Metadata | Implemented |
| Expanded Market Data Coverage | Implemented |
| Scanner-to-Signal Metrics Pipeline | Implemented |
| Entry / Stop / Exit Quality Engines | Implemented |
| Trade Plan Validator | Implemented |
| Entry / Exit Watcher | Implemented |
| Entry / Exit Watcher Health Diagnostics | Implemented |
| Manual Portfolio Sync | Implemented |
| Polygon Live Readiness | Implemented |
| Historical Polygon Data Ingestion | Implemented |
| Historical Backtesting | Implemented |
| Out-of-Sample Historical Validation | Implemented |
| Paper-Live Observation | Implemented |
| Operational Readiness Review | Implemented |
| Scheduled Decision-Support Dry Runs | Implemented |
| Persistent Report Archive | Implemented |
| Feedback Aggregation | Implemented |
| Broker Execution | Not implemented |

## Roadmap

### Done

- P36 confidence score double counting fix
- P35 static dashboard HTML reporting
- P34 optional SQLite runtime persistence
- P33 event-risk placeholder metadata
- P32 expanded market-data coverage
- P31 manual portfolio-state calculation

### Planned Next

1. P37 Probabilistic Engine Softmax Normalization
2. P38 Regime Similarity Weighted Distance + Cosine Similarity
3. P39 Adaptive Feedback Decay
4. P40 MultiFactorFusion Recalibration
5. External artifact storage readiness

## Disclaimer

This project is intended for research, education, systematic market screening and decision-support experiments. It is not financial advice.
