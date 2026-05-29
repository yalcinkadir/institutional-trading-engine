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
IP3/IP4: public-demo defaults and optional external edge provider boundary implemented and CI-green
Report Output Boundary Guard: protected public report outputs implemented and CI-wired
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

## IP3/IP4 Public Demo Defaults and Private Edge Boundary

Public thresholds are now explicitly marked as demo defaults only:

```text
src/config/thresholds.py
```

The optional external edge provider boundary lives in:

```text
src/config/external_edge_provider.py
```

Without configuration, the public repository uses public-demo defaults and CI stays self-contained. A local/private module can be supplied outside the public repository with:

```bash
export ITE_EXTERNAL_EDGE_PROVIDER="your_local_module.path"
```

The private module must expose:

```python
def get_decision_thresholds() -> DecisionThresholds:
    ...
```

IP3/IP4 test command:

```bash
pytest tests/test_external_edge_provider.py -q
```

Operational documentation:

```text
docs/operations/ip3_ip4_public_demo_and_private_edge_boundary.md
```

## Report Output Boundary Guard

The committed public report files are synthetic examples only:

```text
reports/premarket-report.md
reports/postmarket-report.md
reports/weekly-report.md
```

Runtime report generation now fails closed if `scripts/generate_report.py` is asked to write to one of those protected paths. Generated reports should use non-committed output locations such as:

```text
reports/generated/
reports/live/
reports/private/
outputs/
```

Protected by:

```text
src/report_output_boundary.py
tests/test_report_output_boundary.py
tests/test_generate_report_output_boundary.py
docs/operations/report_output_boundary_guard.md
```

Report Output Boundary Guard test command:

```bash
pytest tests/test_report_output_boundary.py -q
pytest tests/test_generate_report_output_boundary.py -q
```

## BT7 Capacity / Turnover / Realism Gate

BT7 adds a deterministic capacity, turnover and transaction-cost realism gate before any private production sizing work. It blocks historically attractive validation evidence from being treated as credible when proposed scale, liquidity usage, turnover, cost drag or slippage coverage are not realistic.

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

Backtest, report-boundary and IP validation gates:

```bash
pytest tests/test_strategy_test_matrix.py -q
pytest tests/test_bt3_backtest_run_contract.py -q
pytest tests/test_bt5_walk_forward_robustness_gate.py -q
pytest tests/test_bt6_evidence_baseline_regression_gate.py -q
pytest tests/test_bt7_capacity_turnover_realism_gate.py -q
pytest tests/test_report_output_boundary.py -q
pytest tests/test_generate_report_output_boundary.py -q
pytest tests/test_external_edge_provider.py -q
```

## Hard Safety Rule

This repository is a research and decision-support framework. No generated report, report output boundary guard, backtest, walk-forward result, evidence baseline comparison, capacity/turnover realism report, paper execution artifact, Telegram dispatch, external edge provider or CI-green state authorizes live trading.
