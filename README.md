# Institutional Trading Engine

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![CI](https://img.shields.io/badge/CI-pytest-brightgreen.svg)
![Status](https://img.shields.io/badge/status-production--oriented-orange.svg)

Institutional Trading Engine is a production-oriented market intelligence, screening, reporting, runtime orchestration, observability, historical validation and decision-support platform.

The system is designed for research and decision support. It does not place live trades.

## Current Validation Status

```text
P36-P47 validation roadmap: implemented
P47 final live readiness gate: completed
CI status: green
Live trading authorization: not granted by code
Broker execution: not implemented
```

Code quality is not trading edge. The system is promising enough to test seriously, but real capital still requires evidence from the validation gates, paper observation and manual review.

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
- execution realism adjustment
- out-of-sample validation lockbox
- paper trading journal / live observation v2
- final live readiness gate
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
→ Execution realism adjustment
→ Out-of-sample validation lockbox
→ Paper trading journal / live observation v2
→ Final live readiness gate
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
pytest tests/test_execution_realism.py
pytest tests/test_out_of_sample_lockbox.py
pytest tests/test_paper_trading_journal.py
pytest tests/test_final_live_readiness_gate.py
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

## P36-P47 Validation Stack

Implemented and CI-green layers:

```text
P36 Confidence Score Double Counting Fix
P37 Probabilistic Engine Softmax Normalization
P38 Regime Similarity Weighted Distance + Cosine Similarity
P39 Adaptive Feedback Decay
P40 MultiFactorFusion Recalibration
P41 Historical Edge Validation Framework
P42 Regime-Phase Backtest Matrix
P43 Walk-Forward Validation
P44 Execution Realism Layer
P45 Out-of-Sample Validation Lockbox
P46 Paper Trading Journal / Live Observation v2
P47 Final Live Readiness Gate
```

## P47 Final Live Readiness Gate

Implemented in:

```text
src/validation/final_live_readiness_gate.py
docs/operations/final_live_readiness_gate.md
tests/test_final_live_readiness_gate.py
```

P47 consolidates P41-P46 evidence into a final fail-closed readiness report.

Readiness levels:

```text
NOT_READY
OBSERVATION_ONLY
REVIEW_READY
```

Required evidence:

```text
historical edge validation
regime-phase robustness
walk-forward stability
execution realism
out-of-sample robustness
paper observation quality
manual review
risk limits
kill-switch definition
```

Staged capital-risk guidance:

```text
Months 1-3:  max 50% size after all gates pass and manual review is complete
Months 4-6:  max 75% size only if observed metrics remain >=85% of expectation
Month 7+:    max 100% only if cumulatively profitable and drawdown remains below kill switch
```

## Decision Quality and Validation Roadmap

Detailed roadmap:

```text
docs/roadmap/decision_quality_p36_p40.md
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
| Execution Realism Layer | Implemented |
| Out-of-Sample Validation Lockbox | Implemented |
| Paper Trading Journal / Live Observation v2 | Implemented |
| Final Live Readiness Gate | Implemented |
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

- P47 final live readiness gate
- P46 paper trading journal / live observation v2
- P45 out-of-sample validation lockbox
- P44 execution realism layer
- P43 walk-forward validation
- P42 regime-phase backtest matrix
- P41 historical edge validation framework
- P40 multi-factor fusion recalibration
- P39 adaptive feedback decay
- P38 regime similarity weighted distance and cosine similarity
- P37 probabilistic engine softmax normalization
- P36 confidence score double counting fix

### Planned Next

Validation roadmap P36-P47 is implemented. Future work should focus on real evidence collection, report review and paper-observation quality, not feature expansion.

## Disclaimer

This project is intended for research, education, systematic market screening and decision-support experiments. It is not financial advice and does not execute trades.
