# Institutional Trading Engine

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![CI](https://img.shields.io/badge/CI-pytest-brightgreen.svg)
![Status](https://img.shields.io/badge/status-production--oriented-orange.svg)

Institutional Trading Engine is a production-oriented market intelligence, screening, reporting, runtime orchestration, observability, historical validation and decision-support platform.

The system is designed for research and decision support. It does not place live trades.

## Core Capabilities

- market regime analysis
- decision confidence scoring
- probabilistic decision normalization
- weighted regime similarity scoring
- adaptive feedback decay weighting
- multi-factor fusion recalibration
- historical edge validation
- regime-phase backtest matrix
- walk-forward validation
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
→ Probabilistic decision normalization
→ Weighted regime similarity scoring
→ Adaptive feedback decay weighting
→ Multi-factor fusion recalibration
→ Historical edge validation
→ Regime-phase backtest matrix
→ Walk-forward validation
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
pytest tests/test_probabilistic_decisions.py
pytest tests/test_regime_similarity_engine.py
pytest tests/test_adaptive_feedback_decay.py
pytest tests/test_multi_factor_fusion.py
pytest tests/test_historical_edge_validation.py
pytest tests/test_regime_phase_backtest_matrix.py
pytest tests/test_walk_forward_validation.py
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

```text
confidence = setup_score * 0.45 + market_health_score * 0.35 + regime_alignment_score * 0.20
```

## P37 Probabilistic Softmax Normalization

Implemented in:

```text
src/decision/probabilistic_decision_engine.py
docs/operations/probabilistic_softmax.md
tests/test_probabilistic_decisions.py
```

```text
bullish_probability + bearish_probability + neutral_probability = 100
```

## P38 Weighted Regime Similarity

Implemented in:

```text
src/regime/regime_similarity_engine.py
docs/operations/regime_similarity.md
tests/test_regime_similarity_engine.py
```

```text
similarity_score = distance_similarity * 0.70 + cosine_similarity * 0.30
```

## P39 Adaptive Feedback Decay

Implemented in:

```text
src/feedback/adaptive_feedback_decay.py
docs/operations/adaptive_feedback_decay.md
tests/test_adaptive_feedback_decay.py
```

```text
weight_i = decay_factor ^ (age_in_days_i / half_life_days)
```

## P40 MultiFactorFusion Recalibration

Implemented in:

```text
src/fusion/multi_factor_fusion_engine.py
docs/operations/multi_factor_fusion.md
tests/test_multi_factor_fusion.py
```

```text
fusion_score = clamp(opportunity_points - risk_penalty, 0, 100)
```

## P41 Historical Edge Validation

Implemented in:

```text
src/validation/historical_edge_validation.py
docs/operations/historical_edge_validation.md
tests/test_historical_edge_validation.py
```

Default gates:

```text
MIN_TOTAL_TRADES     = 300
MIN_PROFIT_FACTOR    = 1.4
MIN_EXPECTANCY_R     = 0.5
MAX_DRAWDOWN_LIMIT   = 0.25
MIN_SHARPE_RATIO     = 0.8
```

## P42 Regime-Phase Backtest Matrix

Implemented in:

```text
src/validation/regime_phase_backtest_matrix.py
docs/operations/regime_phase_backtest_matrix.md
tests/test_regime_phase_backtest_matrix.py
```

```text
at least 3 of 5 phases must pass
```

## P43 Walk-Forward Validation

Implemented in:

```text
src/validation/walk_forward_validation.py
docs/operations/walk_forward_validation.md
tests/test_walk_forward_validation.py
```

P43 separates training windows from forward test windows.

```text
training window 18 months
test window      6 months
step size        3 months
minimum cycles   6
```

Each forward test window is validated independently with P41 historical edge metrics.

## Static Dashboard HTML Reporting

Implemented in:

```text
src/operations/static_dashboard.py
scripts/build_static_dashboard.py
docs/operations/static_dashboard.md
tests/test_static_dashboard.py
.github/workflows/static-dashboard.yml
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

## Decision Quality and Validation Roadmap

Detailed roadmap:

```text
docs/roadmap/decision_quality_p36_p40.md
```

Decision-quality sequence:

```text
P36 Confidence Score Double Counting Fix
P37 Probabilistic Engine Softmax Normalization
P38 Regime Similarity Weighted Distance + Cosine Similarity
P39 Adaptive Feedback Decay
P40 MultiFactorFusion Recalibration
```

Validation sequence after P40:

```text
P41 Historical Edge Validation Framework
P42 Regime-Phase Backtest Matrix
P43 Walk-Forward Validation
P44 Execution Realism Layer
P45 Out-of-Sample Validation Lockbox
P46 Paper Trading Journal / Live Observation v2
P47 Final Live Readiness Gate
```

## Implemented Components

| Layer | Status |
|---|---|
| Decision Confidence Scoring | Implemented |
| Probabilistic Decision Softmax Normalization | Implemented |
| Weighted Regime Similarity Scoring | Implemented |
| Adaptive Feedback Decay Weighting | Implemented |
| MultiFactorFusion Recalibration | Implemented |
| Historical Edge Validation | Implemented |
| Regime-Phase Backtest Matrix | Implemented |
| Walk-Forward Validation | Implemented |
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

- P43 walk-forward validation
- P42 regime-phase backtest matrix
- P41 historical edge validation framework
- P40 multi-factor fusion recalibration
- P39 adaptive feedback decay
- P38 regime similarity weighted distance and cosine similarity
- P37 probabilistic engine softmax normalization
- P36 confidence score double counting fix
- P35 static dashboard HTML reporting
- P34 optional SQLite runtime persistence
- P33 event-risk placeholder metadata
- P32 expanded market-data coverage
- P31 manual portfolio-state calculation

### Planned Next

1. P44 Execution Realism Layer
2. P45 Out-of-Sample Validation Lockbox
3. P46 Paper Trading Journal / Live Observation v2
4. P47 Final Live Readiness Gate

## Disclaimer

This project is intended for research, education, systematic market screening and decision-support experiments. It is not financial advice and does not execute trades.
