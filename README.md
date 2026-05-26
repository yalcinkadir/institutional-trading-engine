# Institutional Trading Engine

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![CI](https://img.shields.io/badge/CI-pytest-brightgreen.svg)
![Status](https://img.shields.io/badge/status-research--evidence--platform-orange.svg)

Institutional Trading Engine is a production-oriented market intelligence, screening, reporting, runtime orchestration, observability, historical validation and decision-support platform.

The system is designed for research and decision support. It does not place live trades.

## Current Validation Status

```text
P36-P47 validation roadmap: implemented
Phase A Evidence Hygiene A3-A10: implemented
Phase A CI stabilization: green
Full regression suite: green
Phase B1-B11 evidence pipeline: implemented, CI-green and workflow-green
Phase B1.1: active 3-6 month observation-only evidence collection
Live trading authorization: not granted by code
Broker execution: not implemented
```

Code quality is not trading edge. The system is promising enough to test seriously, but real capital still requires forward evidence, drift detection, regime-change monitoring, position-level risk attribution and manual review.

## Phase B Daily Evidence Pipeline

The Daily Evidence workflow now runs as a fail-closed evidence chain. It no longer builds green reports from placeholder component JSONs.

```text
Observation-only source bootstrap when explicitly requested
→ Daily evidence input builder
→ Daily evidence input validator
→ B1-B6 component report generation
→ Daily evidence report generation
→ Artifact upload
```

Manual workflow path:

```text
Actions → Daily Evidence Report → Run workflow
bootstrap_observation_only_sources=true
```

The bootstrap mode is only a Day-0 observation-only seed. Records are marked as `observation_only_bootstrap` and are not statistically meaningful 3-6 month forward evidence.

Operational documentation:

```text
docs/operations/generated_daily_evidence_components.md
docs/operations/daily_evidence_input_pipeline.md
docs/operations/daily_evidence_input_builder.md
docs/operations/daily_evidence_source_bootstrap.md
```

Core CLI commands:

```bash
python scripts/bootstrap_daily_evidence_sources.py \
  --output-dir reports/daily_evidence_sources \
  --report-dir reports/daily_evidence_source_bootstrap \
  --report-date 2026-05-26

python scripts/build_daily_evidence_inputs.py \
  --source-dir reports/daily_evidence_sources \
  --output-dir reports/daily_evidence_inputs \
  --report-dir reports/daily_evidence_input_build

python scripts/validate_daily_evidence_inputs.py \
  --input-dir reports/daily_evidence_inputs \
  --output-dir reports/daily_evidence_input_validation

python scripts/generate_daily_evidence_components.py \
  --input-dir reports/daily_evidence_inputs \
  --output-dir reports/daily_evidence_components \
  --report-date 2026-05-26

python scripts/run_daily_evidence_report.py \
  --input-dir reports/daily_evidence_components \
  --output-dir reports/daily_evidence \
  --report-date 2026-05-26
```

## Phase A Evidence Hygiene

Phase A strengthened the foundation before Phase B forward observation. It added evidence governance, statistical robustness, execution realism, observability and operational hygiene.

Implemented Phase A items:

```text
A3 Versioned decision thresholds
A4 Threshold-aware evidence / lockbox invalidation
A5 Square-root regime-aware slippage model
A6 Deflated Sharpe + Bootstrap Confidence Intervals
A7 Polygon structured logging
A8 Polygon cache locking
A9 CHANGELOG / SETUP_NOTES refresh
A10 Quarterly secrets rotation policy
```

Phase A stabilization gate:

```text
Phase A tests added to CI: done
CI test run executed: done
Regression failures fixed: done
Full regression suite green: done
README finalized: done
```

Operational documentation:

```text
docs/operations/threshold_evidence_contract.md
docs/operations/slippage_model.md
docs/operations/statistical_robustness.md
docs/operations/polygon_structured_logging.md
docs/operations/polygon_cache_locking.md
docs/operations/secrets_rotation_policy.md
docs/operations/phase_a_ci_stabilization.md
```

## Core Capabilities

- market regime analysis
- decision confidence scoring
- probabilistic decision normalization
- weighted regime similarity scoring
- adaptive feedback decay weighting
- multi-factor fusion recalibration
- historical edge validation
- Deflated Sharpe probability and bootstrap confidence intervals
- regime-phase backtest matrix
- walk-forward validation
- execution realism adjustment with square-root regime-aware slippage
- out-of-sample validation lockbox with threshold-aware evidence invalidation
- paper trading journal / live observation v2
- Phase B daily evidence input pipeline and report artifacts
- final live readiness gate
- cross-asset market-data coverage
- Polygon active universe runtime builder
- Polygon all-assets data workflow
- Polygon structured JSON logging
- Polygon cache locking and atomic writes
- Polygon daily OHLCV bars downloader
- Polygon artifact consolidation workflow
- historical trade plan generation from Polygon bars
- configurable survivorship audit mode for runtime Polygon artifacts
- edge-evidence diagnostics for failed validation gates
- edge-evidence diagnostics snapshot in workflow logs
- edge-evidence execution from combined Polygon artifacts
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
→ Liquidity filter
→ Signal generation
→ Entry / Stop / Exit quality engines
→ Trade plan validation
→ Decision confidence scoring
→ Probabilistic decision normalization
→ Weighted regime similarity scoring
→ Adaptive feedback decay weighting
→ Multi-factor fusion recalibration
→ Survivorship universe audit
→ 500+ universe coverage gate
→ Historical edge validation
→ Statistical robustness checks
→ Regime-phase backtest matrix
→ Walk-forward validation
→ Execution realism adjustment
→ Out-of-sample validation lockbox
→ Edge-evidence diagnostics
→ Edge-evidence workflow log snapshot
→ Paper trading journal / live observation v2
→ Daily evidence input pipeline
→ Daily evidence report artifact
→ Final live readiness gate
→ Human review
```

## Main Test Commands

Full suite:

```bash
pytest -q
```

Phase A stabilization tests:

```bash
pytest tests/test_decision_engine.py -q
pytest tests/test_out_of_sample_lockbox.py -q
pytest tests/test_slippage_model.py -q
pytest tests/test_execution_realism.py -q
pytest tests/test_statistical_robustness.py -q
pytest tests/test_historical_edge_validation.py -q
pytest tests/test_polygon_structured_logging.py -q
pytest tests/test_polygon_data_pipeline.py -q
pytest tests/test_polygon_cache.py -q
```

Phase B daily evidence tests:

```bash
pytest tests/test_paper_observation_reconciliation.py -q
pytest tests/test_performance_drift_detection.py -q
pytest tests/test_sequential_edge_decay.py -q
pytest tests/test_regime_change_detection.py -q
pytest tests/test_position_risk_attribution.py -q
pytest tests/test_monte_carlo_robustness.py -q
pytest tests/test_daily_evidence_report.py -q
pytest tests/test_run_daily_evidence_report_cli.py -q
pytest tests/test_generate_daily_evidence_components_cli.py -q
pytest tests/test_daily_evidence_input_validation.py -q
pytest tests/test_daily_evidence_input_builder.py -q
pytest tests/test_daily_evidence_source_bootstrap.py -q
```

Representative validation tests:

```bash
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
pytest tests/test_survivorship_universe.py
pytest tests/test_liquidity_filter.py
pytest tests/test_forward_outcome_tracker.py
pytest tests/test_vix_adapter.py
pytest tests/test_edge_evidence_backtest.py
pytest tests/test_generate_historical_trade_plans.py
pytest tests/test_edge_evidence_from_polygon_artifact_workflow.py
pytest tests/test_polygon_data_pipeline.py
pytest tests/test_polygon_edge_data_workflow.py
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

## Edge-Evidence Backtesting

Backtesting is activated through a gated evidence pipeline, not as a loose script.

Manual run:

```bash
python scripts/run_edge_evidence_backtest.py \
  --universe data/universe/survivorship_universe.csv \
  --plans data/trade_plans/historical_trade_plans.json \
  --bars-root data/historical_bars \
  --as-of 2026-05-24 \
  --minimum-assets 500 \
  --oos-split-date 2024-01-01 \
  --survivorship-mode strict
```

Generate historical trade plans from Polygon bars before the backtest:

```bash
python scripts/generate_historical_trade_plans.py \
  --bars-root data/historical_bars \
  --output data/trade_plans/historical_trade_plans.json \
  --min-history 60 \
  --lookahead-days 20
```

GitHub Actions:

```text
Actions → Edge Evidence From Polygon Artifact → Run workflow
```

Use the successful Polygon artifact-consolidation run ID as `run_id`.

The workflow can generate historical trade plans automatically when `generate_plans` is set to `true`.

For combined Polygon runtime artifacts, the workflow uses:

```text
survivorship_mode: runtime_active_universe
```

Use `strict` only when the universe file contains vetted point-in-time ticker lifecycles.

The pipeline writes reports under:

```text
reports/edge_evidence/
```

Expected report files include:

```text
historical-entry-exit-backtest.json
historical-entry-exit-backtest.md
walk-forward-validation.json
walk-forward-validation.md
out-of-sample-lockbox.json
out-of-sample-lockbox.md
edge-evidence-diagnostics.json
edge-evidence-diagnostics.md
edge-evidence-summary.json
edge-evidence-summary.md
```

The diagnostics report explains gate failures with:

```text
historical result distribution
average R and cumulative R
top result reasons
walk-forward failing cycle samples
failed OOS gates
failed degradation checks
```

The GitHub Actions workflow also prints a compact diagnostics snapshot directly into the job log when diagnostics are available:

```text
Historical results
Wins / losses / breakeven
Win rate
Average R
Cumulative R
Walk-forward passing / failing cycles
OOS count
Failed OOS gates
Failed degradation checks
Failing walk-forward cycle samples
```

The historical report writer, diagnostics artifacts and workflow log snapshot are covered by:

```bash
pytest tests/test_edge_evidence_backtest.py -q
pytest tests/test_edge_evidence_from_polygon_artifact_workflow.py -q
```

It fails closed when:

```text
universe_coverage_below_minimum
survivorship_audit_failed
no_trade_plans_loaded
walk_forward_failed
out_of_sample_lockbox_failed
```

Detailed documentation:

```text
docs/operations/historical_trade_plan_generation.md
docs/operations/edge_evidence_from_polygon_artifact.md
docs/operations/runtime_active_universe_mode.md
```

## 500+ Starter Universe

Build a current active starter universe from S&P 500 constituents plus curated sector, industry, factor, international, credit, commodity and volatility ETFs:

```bash
python scripts/build_sp500_plus_universe.py \
  --output data/universe/survivorship_universe.csv
```

Then validate coverage:

```bash
python scripts/validate_universe_coverage.py \
  --universe data/universe/survivorship_universe.csv \
  --as-of 2026-05-24 \
  --minimum 500
```

Important limitation:

```text
This starter universe is useful for current scans and forward paper observation.
It is not a survivorship-safe 10+ year historical dataset.
For serious historical backtesting, enrich it with point-in-time membership and delisted ticker lifecycles from Norgate, CRSP, Sharadar or an equivalent vetted source.
```

## Polygon Edge Data Pipeline

Build the full active Polygon runtime universe. By default this walks all active symbols returned by Polygon for the selected market; 500 is only the minimum acceptance gate, not the target size.

```bash
POLYGON_API_KEY=... python scripts/build_polygon_universe.py \
  --output data/universe/survivorship_universe.csv \
  --active-from 2026-05-24
```

Download daily OHLCV bars for all symbols in that universe:

```bash
POLYGON_API_KEY=... python scripts/download_polygon_daily_bars.py \
  --universe data/universe/survivorship_universe.csv \
  --output-dir data/historical_bars \
  --from-date 2016-01-01 \
  --to-date 2026-05-24 \
  --min-bars 120
```

Use `--max-symbols` only for smoke tests, rate-limit control, or cost-controlled trial runs:

```bash
POLYGON_API_KEY=... python scripts/build_polygon_universe.py --max-symbols 25
POLYGON_API_KEY=... python scripts/download_polygon_daily_bars.py --max-symbols 25
```

For large all-assets historical bar pulls, prefer batching:

```bash
POLYGON_API_KEY=... python scripts/download_polygon_daily_bars.py \
  --universe data/universe/survivorship_universe.csv \
  --output-dir data/historical_bars \
  --from-date 2016-01-01 \
  --to-date 2026-05-24 \
  --min-bars 120 \
  --batch-size 500 \
  --batch-index 0
```

### GitHub Actions all-assets data workflow

After adding the repository secret `POLYGON_API_KEY`, run:

```text
Actions → Polygon Edge Data Pipeline → Run workflow
```

Recommended controlled batch inputs:

```text
from_date: 2016-01-01
to_date: 2026-05-24
min_bars: 120
max_symbols: 0
batch_size: 500
batch_index: 0
sleep_seconds: 0.0
```

`max_symbols: 0` means all available active Polygon symbols. `batch_size: 500` and `batch_index: 0` mean: download the first 500-symbol bar batch. Increase `batch_index` to `1`, `2`, `3`, and so on for later batches.

The workflow does not commit generated market data. It uploads a runtime artifact named:

```text
polygon-edge-runtime-dataset
```

The artifact contains:

```text
data/universe/survivorship_universe.csv
data/historical_bars/
reports/edge_evidence_data/
```

The downloader writes a manifest to:

```text
reports/edge_evidence_data/polygon-bars-manifest.md
```

Important limitation:

```text
Polygon active tickers plus OHLCV bars are enough to start broad runtime evidence collection.
They are not enough for final survivorship-safe 10+ year evidence without delisted ticker lifecycles and point-in-time membership.
Generated market datasets should be stored as workflow artifacts or external data, not committed as large Git blobs.
```

Detailed documentation:

```text
docs/operations/polygon_edge_data_pipeline.md
docs/operations/polygon_artifact_consolidation.md
docs/operations/polygon_structured_logging.md
docs/operations/polygon_cache_locking.md
```

## Historical Data Requirement

For serious 3-6 month edge-evidence work, historical bars must cover:

```text
10+ years
500+ symbols
S&P 500 current and historical constituents
sector ETFs
industry ETFs such as SMH, IGV, XLF, XLV, XBI, KRE, SOXX
second-source delisted ticker lifecycle data
```

Historical Polygon bars can provide OHLCV history, but delisted ticker lifecycle and point-in-time index membership must be validated from a second source before the result is treated as survivorship-safe evidence.

## VIX Activation Policy

VIX is active through:

```text
src/macro/vix_adapter.py
src/decision_engine.py::apply_vix_snapshot_to_context
```

Quality policy:

| Quality | Meaning | Decision Engine Use |
|---|---|---|
| DIRECT | VIX + VIX9D available | trusted |
| PARTIAL | VIX + VIX3M or partial implied-vol data | trusted with lower confidence |
| REALIZED_PROXY | SPY realized volatility proxy | ignored unless explicitly allowed |
| UNAVAILABLE | no usable data | ignored |

The Decision Engine does not fabricate VIX inversion when data is unavailable.

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
Months 4-6:  max 75% only if observed metrics remain >=85% of expectation
Month 7+:    max 100% only if cumulatively profitable and drawdown remains below kill switch
```

## Decision Quality and Validation Roadmap

Detailed roadmap:

```text
docs/roadmap/decision_quality_p36_p40.md
ROADMAP.md
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
| Statistical Robustness | Implemented |
| Regime-Phase Backtest Matrix | Implemented |
| Walk-Forward Validation | Implemented |
| Execution Realism Layer | Implemented |
| Square-Root Slippage Model | Implemented |
| Out-of-Sample Validation Lockbox | Implemented |
| Threshold-Aware Evidence Invalidation | Implemented |
| Paper Trading Journal / Live Observation v2 | Implemented |
| Phase B Daily Evidence Pipeline | Implemented |
| Final Live Readiness Gate | Implemented |
| Survivorship Universe Loader | Implemented |
| 500+ Universe Coverage Gate | Implemented |
| S&P 500 + ETF Universe Builder | Implemented |
| Polygon Active Universe Builder | Implemented |
| Polygon Structured Logging | Implemented |
| Polygon Cache Locking | Implemented |
| Polygon All-Assets Data Workflow | Implemented |
| Polygon Daily Bars Downloader | Implemented |
| Polygon Artifact Consolidation Workflow | Implemented |
| Historical Trade Plan Generator | Implemented |
| Runtime Active Universe Audit Mode | Implemented |
| Edge Evidence Diagnostics | Implemented |
| Edge Evidence Workflow Log Snapshot | Implemented |
| Edge Evidence From Polygon Artifact Workflow | Implemented |
| Liquidity Filter | Implemented |
| Forward Outcome Tracker | Implemented |
| VIX Adapter | Implemented |
| Gated Edge-Evidence Backtest Orchestrator | Implemented |
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

- Phase B11 daily evidence source/input/validation/bootstrap pipeline
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
- Polygon artifact consolidation workflow
- Edge evidence workflow from combined Polygon artifact
- Historical trade plan generation from Polygon bars
- Runtime active universe audit mode for exploratory Polygon artifacts
- Edge evidence diagnostics summary
- Edge evidence workflow log snapshot
- Phase A Evidence Hygiene A3-A10
- Phase A CI stabilization gate

### Phase B: 3-6 months observation-only evidence collection

- replace observation-only bootstrap seed with real persisted daily observation source feed
- run 3-6 months of paper observation with daily reconciliation
- maintain 500+ active scan universe
- ingest 10+ years of historical bars
- generate deterministic historical trade plans from runtime bars
- run exploratory runtime-active-universe evidence on Polygon artifacts
- use diagnostics reports and workflow log snapshots to tune setup filters and validation thresholds transparently
- enrich universe with second-source delisted lifecycle data
- run strict walk-forward validation across full history once point-in-time lifecycles are available
- evaluate which setups pass in which regimes
- open the out-of-sample lockbox once, record result, then keep it locked
- append forward live/paper outcomes for every generated signal
- monitor paper-vs-backtest drift, sequential edge decay, regime change, risk attribution and Monte Carlo robustness daily

### Planned Next

Phase B11 is implemented, CI-green and workflow-green. Future work should replace the Day-0 observation-only bootstrap with a real persisted observation source feed, while continuing the 3-6 month observation-only evidence period.

## Disclaimer

This project is intended for research, education, systematic market screening and decision-support experiments. It is not financial advice and does not execute trades.
