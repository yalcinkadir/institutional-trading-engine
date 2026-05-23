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

## P37 Probabilistic Softmax Normalization

Implemented in:

```text
src/decision/probabilistic_decision_engine.py
docs/operations/probabilistic_softmax.md
tests/test_probabilistic_decisions.py
```

P37 converts bullish, bearish and neutral outputs into a normalized probability distribution.

Logits:

```text
raw_bullish = signal_score * 0.5 + regime_confidence * 0.3 - risk_score * 0.1
raw_bearish = risk_score * 0.6 + max(0, 50 - regime_confidence) * 0.2
raw_neutral = 50 - abs(raw_bullish - raw_bearish) * 0.3
```

Softmax invariant:

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

P38 replaces unweighted regime similarity with weighted normalized distance plus cosine similarity.

Distance weights:

```text
volatility 0.40
health     0.25
breadth    0.20
momentum   0.15
```

Final score:

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

P39 weights recent trade feedback more strongly than older observations.

Constants:

```text
DECAY_HALF_LIFE_STABLE = 30
DECAY_HALF_LIFE_REGIME_SHIFT = 10
REGIME_SHIFT_RECOVERY_DAYS = 5
MIN_WEIGHT_FLOOR = 0.05
```

Formula:

```text
weight_i = decay_factor ^ (age_in_days_i / half_life_days)
adjusted_performance = sum(result_i * weight_i) / sum(weight_i)
```

## P40 MultiFactorFusion Recalibration

Implemented in:

```text
src/fusion/multi_factor_fusion_engine.py
docs/operations/multi_factor_fusion.md
tests/test_multi_factor_fusion.py
```

P40 separates opportunity from risk.

Opportunity weights:

```text
regime_score          0.30
feature_alpha_score   0.30
execution_confidence  0.20
liquidity_score       0.20
```

Risk penalty:

```text
tail_risk_score      0.20
portfolio_risk_score 0.10
```

Final score:

```text
fusion_score = clamp(opportunity_points - risk_penalty, 0, 100)
```

Regime gate:

```text
if regime_score < 20:
    fusion_score = min(fusion_score, 40)
```

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

## SQLite Runtime Persistence

Implemented in:

```text
src/operations/sqlite_persistence.py
scripts/check_sqlite_persistence.py
docs/operations/sqlite_persistence.md
tests/test_sqlite_persistence.py
.github/workflows/sqlite-persistence.yml
```

## Event Risk Placeholder Metadata

Implemented in:

```text
src/event_risk_engine.py
docs/operations/event_risk_placeholder.md
tests/test_event_risk_engine.py
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

1. P41 Historical Edge Validation Framework
2. P42 Regime-Phase Backtest Matrix
3. P43 Walk-Forward Validation
4. P44 Execution Realism Layer
5. P45 Out-of-Sample Validation Lockbox
6. P46 Paper Trading Journal / Live Observation v2
7. P47 Final Live Readiness Gate

## Disclaimer

This project is intended for research, education, systematic market screening and decision-support experiments. It is not financial advice and does not execute trades.
