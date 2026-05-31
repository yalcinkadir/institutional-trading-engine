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
Phase B1.1: evidence operation discipline implemented / CI-wired; 3-6 month observation-only evidence collection remains active
Phase C paper execution infrastructure: implemented for planning, reconciliation, drift, fill-quality and kill-switch governance
Phase EV1-EV2: Sharpe/Deflated-Sharpe evidence-unit correction implemented / CI-wired
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
GOV1-GOV3: critical runtime governance hardening implemented and CI-green
GOV4-GOV6: runtime stability hardening implemented and CI-green
GOV7-GOV10: pre-live hygiene validators implemented and CI-green
TG1: Telegram research-only report dispatcher implemented
TG2/TG3: research-only Telegram summary integration and report templates implemented / CI-wired
BT2: Strategy Test Matrix model, demo matrix, CLI, docs and tests implemented
BT3: Backtest reproducibility contract implemented
BT5: Walk-Forward / Out-of-Sample Robustness Gate implemented and CI-green
BT6: Evidence Baseline Regression Gate implemented and CI-green
BT7: Capacity / Turnover / Realism Gate implemented and CI-green
SR1-SR3: signal identity, ATR persistence and repo-write serialization implemented and CI-green
SR4: trusted portfolio-governance source enforcement implemented and CI-green
Live trading authorization: not granted by code
Broker execution: paper-only infrastructure; live execution is not implemented
```

Code quality is not trading edge. The system is promising enough to test seriously, but real capital still requires long-running forward evidence, drift detection, regime-change monitoring, position-level risk attribution, execution-quality review, capacity/turnover realism and manual approval.

## SR4 Trusted Portfolio Governance Source

SR4 closes a runtime governance source-integrity gap. Runtime portfolio override arguments are no longer accepted as trusted governance state.

```text
src/runtime/live_runtime_cycle.py
tests/test_live_runtime_cycle.py
tests/test_live_runtime_cycle_portfolio_state.py
```

Implemented safeguards:

- `portfolio_drawdown_percent` and `daily_loss_percent` passed directly to `LiveRuntimeCycle.run()` now fail closed.
- Runtime argument overrides are persisted as `runtime_argument_override_rejected` with `governance_valid=False`.
- Successful runtime-cycle tests use an injected trusted `PortfolioStateStore` path instead of overriding governance by arguments.
- Missing or untrusted portfolio state blocks the cycle before kill-switch and risk-limit evaluation.
- No broker execution, no live trading authorization and no private edge parameters are introduced.

SR4 test commands:

```bash
pytest tests/test_live_runtime_cycle.py -q
pytest tests/test_live_runtime_cycle_portfolio_state.py -q
pytest tests/test_portfolio_state.py -q
```

## EV1-EV2 Sharpe / Deflated-Sharpe Evidence Fix

EV1-EV2 corrects the most important evidence-unit issue from the static code review:

```text
src/validation/historical_edge_validation.py
src/config/thresholds.py
tests/test_sharpe_definition_regression.py
```

Implemented safeguards:

- `calculate_sharpe_ratio` now returns sample-size-independent per-trade Sharpe: `mean(R) / std(R)`.
- `calculate_sharpe_tstat` exposes the sample-size-scaled significance proxy separately.
- Deflated Sharpe now receives the per-trade Sharpe unit expected by the robustness formula.
- Historical edge metrics now include `sharpe_tstat` and `sharpe_definition_version` for auditability.
- `MIN_SHARPE_RATIO` was recalibrated from `0.8` to `0.10` for the corrected per-trade Sharpe semantics.
- `THRESHOLDS_VERSION` was bumped to invalidate older public-demo evidence artifacts using the prior Sharpe definition.
- The drawdown gate now reports the effective absolute R threshold instead of only the raw multiplier.
- No broker execution, no live trading authorization and no private edge parameters are introduced.

EV1-EV2 test command:

```bash
pytest tests/test_sharpe_definition_regression.py -q
```

## GOV7-GOV10 Pre-Live Hygiene

GOV7-GOV10 closes the next pre-live hygiene layer before any new strategy complexity is added:

```text
src/validation/gov7_gov10_pre_live_hygiene.py
tests/test_gov7_gov10_pre_live_hygiene.py
```

Implemented safeguards:

- GOV7: public/demo adaptive weights can be rounded while still summing exactly to `1.0`.
- GOV8: VIX term-structure inversion has explicit `DIRECT`, `PARTIAL`, `NONE` and `UNKNOWN` modes.
- GOV9: duplicate/overlapping module remediation can be tracked with owner, replacement and rationale markers.
- GOV10: cumulative Paper Observation drift can detect small persistent drift that may evade daily max-drift gates.
- No broker execution, no live trading authorization and no private edge parameters are introduced.

GOV7-GOV10 test command:

```bash
pytest tests/test_gov7_gov10_pre_live_hygiene.py -q
```

## GOV4-GOV6 Runtime Stability Hardening

GOV4-GOV6 closes the next runtime-stability gaps found during Paper Observation:

```text
src/core/negative_override.py
src/runtime/runtime_state.py
src/runtime/runtime_loop.py
tests/test_negative_override.py
tests/test_runtime_state.py
tests/test_runtime_loop.py
```

Implemented safeguards:

- VIX `None` or invalid VIX values are no longer silently treated as `0` market stress.
- A visible `vix_unavailable` minor override is emitted when a VIX key is present but unavailable or invalid.
- `RuntimeState.history` is bounded by a ring buffer instead of growing without limit during multi-day observation.
- `RuntimeLoop` catches transient provider exceptions, logs them and continues until a max-consecutive-error limit is reached.
- Persistent provider failures raise `RuntimeLoopError` instead of killing the loop silently.
- No broker execution, no live trading authorization and no private edge parameters are introduced.

GOV4-GOV6 test commands:

```bash
pytest tests/test_negative_override.py -q
pytest tests/test_runtime_state.py -q
pytest tests/test_runtime_loop.py -q
```

## B1.1 Evidence Operation Discipline + TG2/TG3 Reporting Integration

B1.1 converts the active 3-6 month observation period into an explicit operating gate. It does not add strategy complexity, broker execution or live-trading authorization.

Implemented files:

```text
src/operations/evidence_operation_discipline.py
src/reporting/tg2_tg3_report_templates.py
docs/operations/b11_evidence_operation_discipline.md
tests/test_b11_evidence_operation_discipline.py
```

Implemented safeguards:

- Observation mode must remain research-only, observation-only or paper-only.
- Daily evidence report must exist and pass.
- Daily reconciliation component must pass before the observation day is considered clean.
- TG3 renders public-safe Daily Evidence, Fill Quality, Kill Switch and Backtest Summary templates.
- TG2 Telegram dispatch records must remain inside the existing TG1 research-only boundary.
- Telegram messages must include the research-only/no-live-trading footer.
- No broker execution, no live trading authorization and no private edge parameters are introduced.

B1.1 test command:

```bash
pytest tests/test_b11_evidence_operation_discipline.py -q
```

Operational documentation:

```text
docs/operations/b11_evidence_operation_discipline.md
```

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
