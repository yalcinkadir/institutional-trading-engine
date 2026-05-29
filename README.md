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
BT7: Capacity / Turnover / Realism Gate implemented and CI-green
Live trading authorization: not granted by code
Broker execution: paper-only infrastructure; live execution is not implemented
```

Code quality is not trading edge. The system is promising enough to test seriously, but real capital still requires long-running forward evidence, drift detection, regime-change monitoring, position-level risk attribution, execution-quality review, capacity/turnover realism and manual approval.

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

## Main Test Commands

Full suite:

```bash
pytest -q
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
