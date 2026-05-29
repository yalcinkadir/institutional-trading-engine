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
IP5/IP6: artifact hygiene and .gitignore hardening implemented / CI-wired
IP9/IP10: PR public-edge review governance, license and usage disclaimer implemented / CI-wired
Report Output Boundary Guard: protected public report artifacts implemented and CI-green
CL1: core decision logic remediation for asymmetry, portfolio-risk tier handling and breakeven expectancy implemented / CI-wired
CL2: scoring-system audit registry and report-vs-decision separation implemented / CI-wired
CL3: kill-switch drawdown-source validation implemented / CI-wired
CL4: ATR calculation governance, Wilder ATR evaluation and threshold-version bump implemented / CI-wired
CL5: regime_alignment independent gate implemented / CI-wired
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

## IP9/IP10 Public Repository Governance

IP9/IP10 closes the immediate public-repository governance gap before new strategy complexity is added.

Implemented files:

```text
.github/pull_request_template.md
.github/workflows/ip9_ip10.yml
LICENSE
DISCLAIMER.md
docs/operations/ip9_ip10_public_repo_governance.md
tests/test_ip9_ip10_public_repo_governance.py
```

Implemented safeguards:

- Future PRs that touch strategy, scoring, thresholds, setup maps, exit profiles, ranking, reports, evidence, execution, sizing or CI gates must pass an explicit public-edge review checklist.
- Strategy-like public values must remain clearly marked as public-demo defaults or synthetic fixtures.
- Research/private configuration belongs behind an external/private boundary, not in the public repository.
- Generated reports, raw evidence, provider extracts, ranked opportunity output and local artifacts must not be committed.
- The public repository now includes a license and a separate research/usage disclaimer.
- The disclaimer states that the project is research and decision-support only, does not provide financial advice, does not guarantee performance and does not grant live trading permission.
- Dedicated IP9/IP10 governance workflow runs PR-template, license/disclaimer and public-boundary checks.

IP9/IP10 test commands:

```bash
pytest tests/test_ip9_ip10_public_repo_governance.py -q
python scripts/check_ip_boundary.py --root . --no-write
pytest tests/test_ip_boundary.py -q
python scripts/validate_public_repo_policy.py --no-write
```

Operational documentation:

```text
docs/operations/ip9_ip10_public_repo_governance.md
```

## Report Output Boundary Guard

The Report Output Boundary Guard prevents generated runtime reports from overwriting committed public report examples:

```text
src/report_output_boundary.py
scripts/generate_report.py
tests/test_report_output_boundary.py
tests/test_generate_report_output_boundary.py
docs/operations/report_output_boundary_guard.md
```

Protected public artifacts:

```text
reports/premarket-report.md
reports/postmarket-report.md
reports/weekly-report.md
```

Implemented safeguards:

- Generated report writes to protected public report paths fail closed with `ReportOutputBoundaryError`.
- Relative traversal attempts such as `reports/generated/../premarket-report.md` are normalized and blocked.
- Allowed runtime outputs stay in non-committed locations such as `reports/generated/`, `reports/live/`, `reports/private/` and `outputs/`.
- The main CI workflow runs the boundary tests before BT7 and the full regression suite.

## CL5 Regime Alignment Governance

CL5 makes `regime_alignment` an explicit independent decision gate before risk-tier scoring can approve or watch a setup:

```text
src/decision_engine.py
tests/test_decision_engine.py
docs/operations/cl5_regime_alignment_governance.md
```

Implemented safeguards:

- `regime_alignment` is checked after hard risk overrides and setup-regime mapping, but before asymmetry, data-confidence and risk-tier scoring.
- A candidate below the independent regime floor returns `NO_TRADE` with `poor_regime_alignment`.
- The decision notes include `regime_alignment_independent_gate` for auditability.
- The public-demo Tier 3 regime-alignment cutoff is reused as the fail-closed floor to avoid adding new proprietary public constants.
- Custom threshold objects can tighten the regime-alignment floor without code changes.
- Ranking regression coverage proves that a high setup score cannot outrank an approved candidate when regime alignment fails.

## CL4 ATR Governance

CL4 makes ATR semantics explicit, versioned and regression-tested before ATR-dependent evidence can be trusted across reports, ranking, backtests, paper execution or validation gates:

```text
src/validation/atr_governance.py
tests/test_atr_governance.py
src/config/thresholds.py
docs/operations/cl4_atr_governance.md
```

Implemented safeguards:

- True range explicitly includes previous-close gap risk.
- Supported ATR methods are explicit: simple rolling ATR and Wilder-smoothed ATR.
- Wilder ATR is seeded by the first simple average and then recursively smoothed.
- `ATR_CALCULATION_VERSION` records the public-demo ATR semantics.
- `THRESHOLDS_VERSION` was bumped because ATR migration is evidence-affecting.
- ATR method changes require evidence invalidation instead of silently reusing older ATR-dependent artifacts.

## CL2/CL3 Scoring and Drawdown-Source Governance

CL2 makes scoring systems auditable instead of implicit:

```text
src/validation/scoring_audit.py
tests/test_scoring_audit.py
```

CL3 makes kill-switch drawdown governance fail closed until the drawdown source is valid:

```text
src/validation/execution_kill_switch.py
tests/test_execution_kill_switch.py
scripts/evaluate_execution_kill_switch.py
```

Implemented safeguards:

- Report-only ranking scores are explicitly separated from decision-authoritative scores.
- Decision Engine tier gating is documented as the authoritative downstream gate.
- Non-authoritative scores are blocked from feeding paper/execution gates.
- A validated drawdown source is required by default.
- Backtest-only, unknown, unreconciled or internally inconsistent drawdown sources are rejected.

## CL1 Core Decision Logic Remediation

CL1 fixes and regression-tests three decision-critical logic issues:

```text
src/setup_scoring.py
src/portfolio_risk.py
src/outcome_tracking.py
```

Implemented safeguards:

- Asymmetry downside risk now uses absolute distance to the SMA50 invalidation reference, preventing below-SMA50 assets from receiving inflated reward/risk scores.
- Portfolio risk elevation now reduces all tradable tiers instead of only Tier 1 candidates.
- Breakeven outcomes are treated as neutral in basic expectancy instead of being classified as losses.

## IP3/IP4 Public Demo Defaults and Private Edge Boundary

Public thresholds are explicitly marked as demo defaults only:

```text
src/config/thresholds.py
src/config/external_edge_provider.py
docs/operations/ip3_ip4_public_demo_and_private_edge_boundary.md
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

## BT7 Capacity / Turnover / Realism Gate

BT7 adds a deterministic capacity, turnover and transaction-cost realism gate before any private production sizing work. It blocks historically attractive validation evidence from being treated as credible when proposed scale, liquidity usage, turnover, cost drag or slippage coverage are not realistic.

```text
src/validation/capacity_turnover_realism_gate.py
tests/test_bt7_capacity_turnover_realism_gate.py
docs/operations/bt7_capacity_turnover_realism_gate.md
```

## Main Test Commands

Full suite:

```bash
pytest -q
```

Backtest, IP, report-boundary and core-logic validation gates:

```bash
pytest tests/test_strategy_test_matrix.py -q
pytest tests/test_bt3_backtest_run_contract.py -q
pytest tests/test_bt5_walk_forward_robustness_gate.py -q
pytest tests/test_bt6_evidence_baseline_regression_gate.py -q
pytest tests/test_bt7_capacity_turnover_realism_gate.py -q
pytest tests/test_external_edge_provider.py -q
pytest tests/test_artifact_hygiene.py -q
pytest tests/test_ip9_ip10_public_repo_governance.py -q
pytest tests/test_report_output_boundary.py -q
pytest tests/test_generate_report_output_boundary.py -q
pytest tests/test_setup_scoring.py -q
pytest tests/test_portfolio_risk.py -q
pytest tests/test_outcome_tracking.py -q
pytest tests/test_scoring_audit.py -q
pytest tests/test_execution_kill_switch.py -q
pytest tests/test_atr_governance.py -q
pytest tests/test_decision_engine.py -q
```

## Hard Safety Rule

This repository is a research and decision-support framework. No generated report, protected public report example, backtest, walk-forward result, evidence baseline comparison, capacity/turnover realism report, paper execution artifact, Telegram dispatch, external edge provider, core-logic remediation, scoring audit, kill-switch drawdown-source validation, ATR governance change, threshold-version bump, regime-alignment governance change, report output boundary guard, IP9/IP10 governance check or CI-green state authorizes live trading.
