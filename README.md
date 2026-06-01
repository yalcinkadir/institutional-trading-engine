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
RGP1: missing/invalid PortfolioState fail-closed proof implemented and CI-green
RGP2: runtime governance approval gate implemented and CI-green
RGP3: stale PortfolioState approval blocking implemented and CI-green
RGP4: actionable signal provider-fetch failure blocking implemented and CI-wired
RGP5: critical STOP/EXIT alert ordering guard implemented and CI-green
RGP6: strict critical notification failure handling implemented and CI-green
RGP7: repo-writing workflow serialization/retry guard implemented and CI-green
RGP8: alert/evidence artifact upload-on-failure guard implemented and CI-green
Live trading authorization: not granted by code
Broker execution: paper-only infrastructure; live execution is not implemented
```

Code quality is not trading edge. The system is promising enough to test seriously, but real capital still requires long-running forward evidence, drift detection, regime-change monitoring, position-level risk attribution, execution-quality review, capacity/turnover realism and manual approval.

## RGP Runtime Governance Proof Pack

RGP proves that runtime governance fails closed when safety evidence is missing, invalid or stale. It is an audit/proof phase, not a strategy-expansion phase.

```text
src/governance/kill_switch.py
src/runtime/governance_approval_gate.py
src/runtime/portfolio_state.py
src/notifications/critical_runtime_alert.py
tests/test_runtime_governance_proof_pack.py
tests/test_critical_runtime_alert.py
tests/test_rgp7_repo_write_workflow_governance.py
tests/test_rgp8_artifact_upload_on_git_failure.py
```

Implemented safeguards:

- RGP1: missing or invalid `PortfolioState` forces kill-switch activation and prevents harmless-looking `0.0` drawdown from being treated as valid governance.
- RGP2: `evaluate_runtime_governance_approval()` blocks runtime approval when portfolio governance is invalid or the kill switch is active.
- RGP3: stale, future-dated or invalid `portfolio_state.updated_at` blocks runtime approval with `stale_portfolio_state`.
- RGP4: actionable signals with provider/data-fetch failures block runtime approval with `data_provider_fetch_failure` instead of being silently skipped.
- RGP5: critical STOP/EXIT runtime alerts are dispatched and persisted before repository commit/rebase/push style persistence can fail.
- RGP6: critical notification transport failures and guardrail blocks are not masked; failure evidence is persisted and repository persistence is not attempted.
- RGP7: repo-writing GitHub Actions are guarded so future commit/push/rebase workflows require repo-wide concurrency or robust push retry.
- RGP8: repo-writing GitHub Actions are guarded so alert/evidence/runtime artifacts must be uploaded with `if: always()` even when git persistence fails.
- Runtime approval is explicit: `approved=True` is only possible when governance is valid, portfolio state is recent, provider evidence is usable for actionable signals and the kill switch is inactive.
- Critical lifecycle alerts are research/paper-only, persisted as audit evidence and do not authorize live trading.
- Tests inject deterministic timestamps so CI remains reproducible.
- No broker execution, no live trading authorization and no private edge parameters are introduced.

RGP test commands:

```bash
pytest tests/test_runtime_governance_proof_pack.py -q
pytest tests/test_critical_runtime_alert.py -q
pytest tests/test_rgp7_repo_write_workflow_governance.py -q
pytest tests/test_rgp8_artifact_upload_on_git_failure.py -q
```

## PSR4 Drift and Regime Evidence

PSR4 adds structured drift and regime-change evidence. Observation days can now document score/decision drift, cumulative drift and market-regime transitions as daily audit artifacts.

```text
src/operations/drift_regime_evidence.py
```
