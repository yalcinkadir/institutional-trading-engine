# Institutional Trading Engine

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![CI](https://img.shields.io/badge/CI-pytest-brightgreen.svg)
![Status](https://img.shields.io/badge/status-research--evidence--platform-orange.svg)

Institutional Trading Engine is a production-oriented market intelligence, screening, reporting, runtime orchestration, observability, historical validation and decision-support platform.

The system is designed for research and decision support. It does not place live trades.

## Current Validation Status

```text
P36-P47 validation roadmap: implemented
Phase A Evidence Hygiene A3-A10: implemented and CI-green
Phase B evidence pipeline: implemented, CI-green and workflow-green
Phase B1.1: active 3-6 month observation-only evidence collection
Phase C paper execution infrastructure: implemented for planning, reconciliation, drift, fill-quality and kill-switch governance
Phase IP1/IP2: public/private edge boundary and public repository hygiene policy implemented
TG1: Telegram research-only report dispatcher implemented
BT2: Strategy Test Matrix model, demo matrix, CLI, docs and tests implemented
BT3: Backtest reproducibility contract implemented
BT5: Walk-Forward / Out-of-Sample Robustness Gate implemented and CI-green
BT6: Evidence Baseline Regression Gate implemented and CI-green
BT7: Capacity / Turnover / Realism Gate implemented with tests, CLI, docs and dedicated workflow
Live trading authorization: not granted by code
Broker execution: paper-only infrastructure; live execution is not implemented
```

Code quality is not trading edge. The system is promising enough to test seriously, but real capital still requires long-running forward evidence, drift detection, regime-change monitoring, position-level risk attribution, execution-quality review and manual approval.

## Public / Private Edge Boundary

The public repository exposes framework discipline, validation machinery, paper-execution controls, auditability, tests and documentation. It is not intended to expose proprietary production edge configuration.

Public-safe content may include architecture, interfaces, demo defaults, synthetic examples, tests, documentation and paper-observation infrastructure. Private edge must stay outside the public repository, including real thresholds, real scoring weights, proprietary setup rankings, non-public entry/exit profiles and private evidence artifacts.

Core checks:

```bash
python scripts/check_ip_boundary.py --root . --no-write
python scripts/validate_public_repo_policy.py --no-write
```

Operational documentation:

```text
docs/operations/ip_boundary.md
docs/operations/public_repo_hygiene_policy.md
```

## BT2 Strategy Test Matrix

BT2 adds a public-safe strategy coverage matrix for validating whether strategy sleeves are covered across regimes, setup families, validation stages and data modes.

```bash
python scripts/generate_strategy_test_matrix.py --demo
pytest tests/test_strategy_test_matrix.py -q
```

Operational documentation:

```text
docs/operations/strategy_test_matrix.md
```

## BT3 Backtest Reproducibility Contract

BT3 validates whether historical validation results are tied to pinned run identity, code commit, strategy version, parameter version, dataset fingerprint, symbol set, date window, deterministic seed, metrics and artifact hashes.

```bash
python scripts/generate_bt3_contract_report.py --demo
pytest tests/test_bt3_backtest_run_contract.py -q
```

Operational documentation:

```text
docs/operations/bt3_reproducibility_contract.md
```

## BT5 Walk-Forward / Out-of-Sample Robustness Gate

BT5 adds a deterministic gate for walk-forward and out-of-sample robustness evidence. It blocks weak historical evidence from passing simply because in-sample results look good.

BT5 validates:

```text
minimum fold count
complete fold identity and dataset metadata
chronological train and OOS windows
non-overlapping OOS folds
required train and OOS metrics
minimum OOS trade count
maximum OOS drawdown
minimum OOS pass rate
positive primary OOS metric rate
train-to-OOS degradation limit
public-safe demo tags
research-only footer
```

Demo command:

```bash
python scripts/generate_bt5_walk_forward_report.py --demo
```

File-based command:

```bash
python scripts/generate_bt5_walk_forward_report.py \
  --input-json data/demo_bt5_walk_forward_folds.json \
  --output-json reports/bt5_walk_forward/robustness_report.json \
  --output-md reports/bt5_walk_forward/robustness_report.md
```

BT5 test command:

```bash
pytest tests/test_bt5_walk_forward_robustness_gate.py -q
```

Operational documentation:

```text
docs/operations/bt5_walk_forward_robustness_gate.md
```

Every generated BT5 report remains compatible with:

```text
Research / Paper Observation Only. Execution is not authorized by this report.
```

## BT6 Evidence Baseline Regression Gate

BT6 compares a new evidence snapshot against a previously accepted baseline snapshot. It blocks silent regression after strategy, parameter, dataset or validation-code changes.

BT6 validates:

```text
baseline and current run identity
strategy comparability
dataset comparability
required metric presence and numeric validity
artifact hash references
expectancy degradation
Sharpe degradation
OOS pass-rate degradation
drawdown increase
trade-count collapse
public-safe demo tags
research-only footer
```

Demo command:

```bash
python scripts/generate_bt6_baseline_regression_report.py --demo
```

File-based command:

```bash
python scripts/generate_bt6_baseline_regression_report.py \
  --input-json data/demo_bt6_evidence_baseline.json \
  --output-json reports/bt6_baseline_regression/report.json \
  --output-md reports/bt6_baseline_regression/report.md
```

BT6 test command:

```bash
pytest tests/test_bt6_evidence_baseline_regression_gate.py -q
```

Operational documentation:

```text
docs/operations/bt6_evidence_baseline_regression_gate.md
```

Every generated BT6 report remains compatible with:

```text
Research / Paper Observation Only. Execution is not authorized by this report.
```

## BT7 Capacity / Turnover / Realism Gate

BT7 adds a deterministic capacity, turnover and transaction-cost realism gate before any private production sizing work. It blocks historically attractive validation evidence from being treated as credible when proposed scale, liquidity usage, turnover, cost drag or slippage coverage are not realistic.

BT7 validates:

```text
complete run identity
required numeric capacity and turnover metrics
positive proposed capital and symbol count
single-position ADV usage
portfolio ADV usage
average daily turnover
annual turnover
transaction-cost drag versus gross expectancy
net expectancy after costs
average holding-period realism
minimum trade count
slippage-model coverage
artifact hash references
public-safe demo tags
research-only footer
```

Demo command:

```bash
python scripts/generate_bt7_capacity_turnover_report.py --demo
```

File-based command:

```bash
python scripts/generate_bt7_capacity_turnover_report.py \
  --input-json data/demo_bt7_capacity_turnover.json \
  --output-json reports/bt7_capacity_turnover/report.json \
  --output-md reports/bt7_capacity_turnover/report.md
```

BT7 test command:

```bash
pytest tests/test_bt7_capacity_turnover_realism_gate.py -q
```

Operational documentation:

```text
docs/operations/bt7_capacity_turnover_realism_gate.md
```

Every generated BT7 report remains compatible with:

```text
Research / Paper Observation Only. Execution is not authorized by this report.
```

## Telegram Research-Only Reports

TG1 can dispatch Telegram reports in research-only mode. It blocks live-trading language, order-action phrases and private-edge terms before sending.

Dry-run mode:

```bash
python scripts/send_telegram_report.py \
  --report-file reports/daily_evidence/latest.md \
  --title "Daily Evidence" \
  --dry-run
```

Actual Telegram delivery requires explicit `--send` plus secrets in the environment.

Operational documentation:

```text
docs/operations/telegram_report_dispatcher.md
```

## Phase B Daily Evidence Pipeline

The Daily Evidence workflow runs as an auditable evidence chain:

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
- BT5 walk-forward / out-of-sample robustness gate
- BT6 evidence baseline regression gate
- BT7 capacity / turnover / realism gate
- execution realism adjustment with square-root regime-aware slippage
- out-of-sample validation lockbox with threshold-aware evidence invalidation
- paper trading journal / live observation v2
- persisted daily observation source feed
- real paper observation source builder
- daily observation cadence review
- Phase B daily evidence input pipeline and report artifacts
- paper broker adapter interface
- VWAP/TWAP paper order slicing
- paper order reconciliation and portfolio-state derivation
- daily expected-vs-observed execution reconciliation
- fill-quality reporting for slippage, spread, delay and partial fills
- execution kill-switch governance for failed evidence and execution-quality drift
- public/private edge boundary guardrail
- public repository hygiene policy validation
- Telegram research-only report dispatching
- BT2 Strategy Test Matrix coverage validation
- BT3 backtest reproducibility contract
- final live readiness gate
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
→ BT5 walk-forward / out-of-sample robustness gate
→ BT6 evidence baseline regression gate
→ BT7 capacity / turnover / realism gate
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
→ Telegram report dispatch guardrails
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

Telegram report tests:

```bash
pytest tests/test_telegram_report_dispatcher.py -q
```

Backtest validation gates:

```bash
pytest tests/test_strategy_test_matrix.py -q
pytest tests/test_bt3_backtest_run_contract.py -q
pytest tests/test_bt5_walk_forward_robustness_gate.py -q
pytest tests/test_bt6_evidence_baseline_regression_gate.py -q
pytest tests/test_bt7_capacity_turnover_realism_gate.py -q
```

## Hard Safety Rule

This repository is a research and decision-support framework. No generated report, backtest, walk-forward result, evidence baseline comparison, capacity/turnover realism report, paper execution artifact, Telegram dispatch or CI-green state authorizes live trading.
