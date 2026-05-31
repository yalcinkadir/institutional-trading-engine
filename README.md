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
SR5: persistent anomaly-state governance implemented and CI-green
SR6: governance thresholds single source of truth implemented and CI-green
SR7: completed-bar watcher semantics implemented and CI-green
SR8: dependency reproducibility contract implemented and CI-green
PSR1: daily runtime evidence manifest implemented and CI-green
PSR2: runtime evidence manifest guard implemented and CI-green
PSR3: fill-quality evidence artifact implemented and CI-green
PSR4: drift and regime evidence artifact implemented and CI-green
Live trading authorization: not granted by code
Broker execution: paper-only infrastructure; live execution is not implemented
```

Code quality is not trading edge. The system is promising enough to test seriously, but real capital still requires long-running forward evidence, drift detection, regime-change monitoring, position-level risk attribution, execution-quality review, capacity/turnover realism and manual approval.

## PSR4 Drift and Regime Evidence

PSR4 adds structured drift and regime-change evidence. Observation days can now document score/decision drift, cumulative drift and market-regime transitions as daily audit artifacts.

```text
src/operations/drift_regime_evidence.py
scripts/generate_drift_regime_evidence.py
tests/test_psr4_drift_regime_evidence.py
```

Implemented safeguards:

- Drift metrics compare observed and expected values and classify drift as `PASS`, `WARN` or `FAIL`.
- Cumulative drift is tracked separately with warn/fail thresholds.
- Regime transitions classify stable, minor, major and unknown transitions.
- Daily evidence summarizes metric, cumulative and regime statuses into one final status.
- Evidence JSON supports deterministic write/load round trips.
- Evidence validation rejects inconsistent metric drift, status mismatches, schema drift and `live_trading_authorized=True`.
- No broker execution, no live trading authorization and no private edge parameters are introduced.

PSR4 test commands:

```bash
pytest tests/test_psr4_drift_regime_evidence.py -q
python scripts/generate_drift_regime_evidence.py --trading-date 2026-05-31 --input path/to/drift-regime.json
```

## PSR3 Fill-Quality Evidence

PSR3 adds structured paper-execution quality evidence. Slippage, fill status and reconciliation state can now be persisted as a daily audit artifact and included in the runtime evidence manifest chain.

```text
src/operations/fill_quality_evidence.py
scripts/generate_fill_quality_evidence.py
tests/test_psr3_fill_quality_evidence.py
```

Implemented safeguards:

- Fill-quality records normalize order ID, signal ID, symbol, side, quantity, expected price, actual price, fill status and reconciliation status.
- Buy and sell slippage are calculated in absolute units and basis points.
- Failed, rejected, cancelled, expired or unknown fills fail the record.
- Unreconciled, missing or mismatched reconciliation status fails the record.
- High but not catastrophic slippage produces `WARN`; severe slippage produces `FAIL`.
- Daily evidence summarizes filled, partial-fill, failed and unreconciled counts.
- Evidence validation rejects inconsistent counts, schema drift and `live_trading_authorized=True`.
- No broker execution, no live trading authorization and no private edge parameters are introduced.

PSR3 test commands:

```bash
pytest tests/test_psr3_fill_quality_evidence.py -q
python scripts/generate_fill_quality_evidence.py --trading-date 2026-05-31 --input path/to/paper-fills.json
```

## PSR2 Runtime Evidence Manifest Guard

PSR2 turns the PSR1 manifest into an enforceable observation-day gate. A paper/observation day is not accepted when the manifest is missing, invalid or not `PASS`.

```text
src/operations/runtime_evidence_manifest_guard.py
scripts/guard_runtime_evidence_manifest.py
tests/test_psr2_runtime_evidence_manifest_guard.py
```

Implemented safeguards:

- Missing daily manifests fail closed with `manifest_missing`.
- Invalid manifest JSON or schema fails closed.
- Manifest status other than `PASS` blocks observation-day acceptance.
- Missing required artifacts are surfaced as guard errors.
- `live_trading_authorized=True` is rejected by the guard.
- A CLI script can evaluate a manifest by explicit path or trading date and optionally write a JSON guard report.
- No broker execution, no live trading authorization and no private edge parameters are introduced.

PSR2 test commands:

```bash
pytest tests/test_psr1_runtime_evidence_manifest.py tests/test_psr2_runtime_evidence_manifest_guard.py -q
python scripts/guard_runtime_evidence_manifest.py --trading-date 2026-05-31
```

## PSR1 Daily Runtime Evidence Manifest

PSR1 starts the post-SR runtime evidence hardening block. It adds a daily manifest for paper/observation evidence integrity.

```text
src/operations/runtime_evidence_manifest.py
scripts/generate_runtime_evidence_manifest.py
tests/test_psr1_runtime_evidence_manifest.py
```

Implemented safeguards:

- Daily runtime evidence manifests include required input, output and governance-state artifact metadata.
- Existing artifacts are recorded with SHA256 hashes and file sizes.
- Missing required artifacts produce manifest status `FAIL`.
- Missing optional artifacts do not fail the manifest.
- Manifest validation enforces schema consistency and keeps `live_trading_authorized=False`.
- A CLI script can generate daily manifests into `reports/evidence/manifests/`.
- No broker execution, no live trading authorization and no private edge parameters are introduced.

PSR1 test commands:

```bash
pytest tests/test_psr1_runtime_evidence_manifest.py -q
python scripts/generate_runtime_evidence_manifest.py --trading-date 2026-05-31 --required-input requirements.txt --required-output requirements.lock --required-governance-state requirements.lock
```

## SR8 Dependency Reproducibility Contract

SR8 closes a reproducibility gap. Runtime and test dependencies are now installed through a locked dependency contract instead of freely drifting package names.

```text
requirements.txt
requirements.lock
tests/test_sr8_dependency_reproducibility.py
```

Implemented safeguards:

- `requirements.txt` delegates to `requirements.lock`.
- `requirements.lock` pins the current top-level runtime/test dependencies exactly.
- A regression guard verifies that the root requirements entry point delegates to the lockfile.
- A regression guard verifies every meaningful lockfile dependency uses exact `==` pinning.
- Workflow-local requirements files are prevented from becoming a second dependency source of truth.
- No broker execution, no live trading authorization and no private edge parameters are introduced.

SR8 test commands:

```bash
pytest tests/test_sr8_dependency_reproducibility.py -q
pip install -r requirements.txt
pytest -q
```

## SR7 Completed-Bar Watcher Semantics

SR7 closes a watcher timing gap. Entry, stop and target lifecycle events are no longer emitted from explicitly incomplete bars.

```text
src/watchers/entry_exit_watcher.py
tests/test_sr7_completed_bar_semantics.py
```

Implemented safeguards:

- `PriceBar` now carries `is_complete`, `completed_at` and `completion_source` metadata.
- `evaluate_signal_against_bar()` returns no lifecycle update when the supplied bar is incomplete.
- Pending entries, stops and targets are all protected from intrabar high/low noise.
- Polygon aggregate conversion respects explicit provider completion flags when available.
- Daily aggregate bars without provider flags receive completion metadata from the bar timestamp.
- Regression tests prove incomplete bars preserve signal state while completed bars preserve existing watcher behavior.
- No broker execution, no live trading authorization and no private edge parameters are introduced.

SR7 test commands:

```bash
pytest tests/test_entry_exit_watcher.py tests/test_sr7_completed_bar_semantics.py -q
```

## SR6 Governance Thresholds Single Source of Truth

SR6 closes a governance configuration-drift gap. Runtime kill-switch and risk-limit thresholds are now centralized instead of being spread across runtime modules as local magic numbers.

```text
src/governance/governance_thresholds.py
src/governance/kill_switch.py
src/runtime/live_runtime_cycle.py
tests/test_governance_thresholds.py
```

Implemented safeguards:

- `GovernanceThresholds` centralizes VIX kill level, portfolio drawdown kill level, severe anomaly kill count, max drawdown and max daily loss thresholds.
- `DEFAULT_GOVERNANCE_THRESHOLDS` preserves the existing public/demo defaults.
- `evaluate_kill_switch()` receives thresholds explicitly instead of owning hardcoded governance constants.
- `LiveRuntimeCycle` accepts injectable `governance_thresholds` and uses them for kill-switch and risk-limit checks.
- Decision payloads and governance-block payloads include `governance_thresholds` for auditability.
- Regression tests prove custom thresholds affect behavior and the runtime cycle no longer defines local governance threshold constants.
- No broker execution, no live trading authorization and no private edge parameters are introduced.

SR6 test commands:

```bash
pytest tests/test_governance_thresholds.py -q
pytest tests/test_live_runtime_cycle.py -q
pytest tests/test_portfolio_state.py -q
```

## SR5 Persistent Anomaly-State Governance

SR5 closes a runtime governance persistence gap. The anomaly kill-switch no longer depends primarily on process-local in-memory cache during GitHub Actions runs.

```text
src/runtime/anomaly_state.py
src/runtime/live_runtime_cycle.py
tests/test_anomaly_state.py
tests/test_live_runtime_cycle.py
tests/test_live_runtime_cycle_portfolio_state.py
```

Implemented safeguards:

- `AnomalyStateStore` loads severe anomaly evidence from persistent `data/anomaly_state.json`.
- Missing or invalid anomaly state remains auditable through `anomaly_state_missing` / `anomaly_state_invalid` warnings.
- `LiveRuntimeCycle` persists `anomaly_state` in the decision payload and runtime state update.
- Process-local cache is retained only as a fallback when persistent anomaly state is unavailable.
- Regression tests cover missing, invalid, negative, legacy alias and persistent severe anomaly counts.
- No broker execution, no live trading authorization and no private edge parameters are introduced.

SR5 test commands:

```bash
pytest tests/test_anomaly_state.py -q
pytest tests/test_live_runtime_cycle.py -q
pytest tests/test_live_runtime_cycle_portfolio_state.py -q
```

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

- `regime_alignment` is now normalized before risk-tier scoring.
- Missing or invalid alignment is treated conservatively.
- Candidates with insufficient regime alignment cannot be promoted by score alone.
- Regression tests prove the gate blocks weak alignment and allows valid alignment.
