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
Phase B1-B14 evidence pipeline: implemented, CI-green and workflow-green
Phase B15 observation cadence review: implemented and CI-green
Phase B1.1: active 3-6 month observation-only evidence collection
Phase C3/C4/C5/C6/C7: paper-only execution planning, reconciliation, drift, fill-quality and kill-switch governance infrastructure
Phase IP1: public/private edge boundary guardrail implemented
Phase IP2: public repository hygiene policy implemented
Live trading authorization: not granted by code
Broker execution: paper-only infrastructure; live execution is not implemented
```

Code quality is not trading edge. The system is promising enough to test seriously, but real capital still requires forward evidence, drift detection, regime-change monitoring, position-level risk attribution and manual review.

## Public / Private Edge Boundary

The public repository is intended to expose the framework, validation discipline, paper-execution controls, auditability, tests and documentation. It is not intended to expose proprietary production edge configuration.

IP1 adds a conservative repository hygiene scanner:

```bash
python scripts/check_ip_boundary.py --root . --no-write
```

IP2 adds the operational public repository hygiene policy:

```bash
python scripts/validate_public_repo_policy.py --no-write
```

Policy files:

```text
.ip-boundary.yml
docs/operations/public_repo_hygiene_policy.md
```

Operational documentation:

```text
docs/operations/ip_boundary.md
docs/operations/public_repo_hygiene_policy.md
```

Public-safe content may include architecture, interfaces, demo defaults, synthetic examples, tests, documentation and paper-observation infrastructure. Private edge should stay outside the public repository, including real thresholds, real scoring weights, proprietary setup rankings, non-public entry/exit profiles and private evidence artifacts.

## Phase B Daily Evidence Pipeline

The Daily Evidence workflow now runs as an auditable evidence chain. It no longer builds green reports from placeholder component JSONs.

```text
Observation source selection
→ optional real paper observation source builder
→ optional Day-0 observation-only bootstrap
→ persisted daily observation feed
→ daily evidence input builder
→ daily evidence input validator
→ B1-B6 component report generation
→ daily evidence report generation
→ optional real paper observation cadence review
→ artifact upload
```

Manual bootstrap workflow path:

```text
Actions → Daily Evidence Report → Run workflow
bootstrap_observation_only_sources=true
use_real_paper_observation_source=false
```

Manual real paper observation workflow path:

```text
Actions → Daily Evidence Report → Run workflow
bootstrap_observation_only_sources=false
use_real_paper_observation_source=true
real_paper_observation_source_dir=reports/daily_paper_observation_raw
```

The bootstrap mode is only a Day-0 observation-only seed. Records are marked as `observation_only_bootstrap` and are not statistically meaningful 3-6 month forward evidence.

The real paper observation mode is still observation-only. It proves capture discipline and artifact completeness, not live trading readiness.

Operational documentation:

```text
docs/operations/generated_daily_evidence_components.md
docs/operations/daily_evidence_input_pipeline.md
docs/operations/daily_evidence_input_builder.md
docs/operations/daily_evidence_source_bootstrap.md
docs/operations/daily_paper_observation_source.md
docs/operations/daily_observation_cadence.md
docs/operations/vwap_twap_slicing.md
docs/operations/order_reconciliation.md
docs/operations/daily_execution_reconciliation.md
docs/operations/fill_quality_report.md
docs/operations/execution_kill_switch.md
docs/operations/ip_boundary.md
docs/operations/public_repo_hygiene_policy.md
```

Core CLI commands:

```bash
python scripts/bootstrap_daily_evidence_sources.py \
  --output-dir reports/daily_observation_incoming \
  --report-dir reports/daily_evidence_source_bootstrap \
  --report-date 2026-05-26

python scripts/build_daily_paper_observation_sources.py \
  --source-dir reports/daily_paper_observation_raw \
  --output-dir reports/daily_observation_incoming \
  --report-dir reports/daily_paper_observation_source

python scripts/persist_daily_observation_sources.py \
  --incoming-dir reports/daily_observation_incoming \
  --feed-dir reports/daily_observation_feed \
  --report-dir reports/daily_observation_source_feed \
  --report-date 2026-05-26

python scripts/build_daily_evidence_inputs.py \
  --source-dir reports/daily_observation_feed \
  --output-dir reports/daily_evidence_inputs \
  --report-dir reports/daily_evidence_input_build

python scripts/validate_daily_evidence_inputs.py \
  --input-dir reports/daily_evidence_inputs \
  --output-dir reports/daily_evidence_input_validation

python scripts/generate_daily_evidence_components.py \
  --input-dir reports/daily_evidence_inputs \
  --output-dir reports/daily_evidence_components \
  --report-date 2026-05-26 \
  --observation-only

python scripts/run_daily_evidence_report.py \
  --input-dir reports/daily_evidence_components \
  --output-dir reports/daily_evidence \
  --report-date 2026-05-26 \
  --max-failed-components 3

python scripts/review_daily_observation_cadence.py \
  --report-date 2026-05-26 \
  --raw-source-dir reports/daily_paper_observation_raw \
  --artifact-root reports \
  --output-dir reports/daily_observation_cadence

python scripts/reconcile_daily_execution.py \
  --expected-file reports/daily_expected_execution/expected.json \
  --observed-file reports/daily_observed_execution/observed.json \
  --output-dir reports/daily_execution_reconciliation

python scripts/generate_fill_quality_report.py \
  --input-file reports/fill_quality_input/fills.json \
  --output-dir reports/fill_quality

python scripts/evaluate_execution_kill_switch.py \
  --input-file reports/execution_kill_switch_input/input.json \
  --output-dir reports/execution_kill_switch

python scripts/check_ip_boundary.py \
  --root . \
  --no-write

python scripts/validate_public_repo_policy.py \
  --no-write
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
- persisted daily observation source feed
- real paper observation source builder
- daily observation cadence review
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
- paper broker adapter interface
- VWAP/TWAP paper order slicing
- paper order reconciliation and portfolio-state derivation
- daily expected-vs-observed execution reconciliation
- fill-quality reporting for slippage, spread, delay and partial fills
- execution kill-switch governance for failed evidence and execution-quality drift
- public/private edge boundary guardrail
- public repository hygiene policy validation
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
→ Daily observation cadence review
→ Paper execution planning
→ Order / Fill reconciliation
→ Portfolio-state snapshot
→ Daily expected-vs-observed execution reconciliation
→ Fill-quality reporting
→ Execution kill-switch decision
→ Public/private edge boundary scan
→ Public repository policy validation
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

Phase C paper execution tests:

```bash
pytest tests/test_order_slicing.py -q
pytest tests/test_order_reconciliation.py -q
pytest tests/test_daily_execution_reconciliation.py -q
pytest tests/test_fill_quality_report.py -q
pytest tests/test_execution_kill_switch.py -q
```

IP boundary and policy tests:

```bash
pytest tests/test_ip_boundary.py -q
pytest tests/test_public_repo_policy.py -q
```
