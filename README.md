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
RGP3: stale PortfolioState approval blocking implemented / awaiting CI
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
tests/test_runtime_governance_proof_pack.py
```

Implemented safeguards:

- RGP1: missing or invalid `PortfolioState` forces kill-switch activation and prevents harmless-looking `0.0` drawdown from being treated as valid governance.
- RGP2: `evaluate_runtime_governance_approval()` blocks runtime approval when portfolio governance is invalid or the kill switch is active.
- RGP3: stale, future-dated or invalid `portfolio_state.updated_at` blocks runtime approval with `stale_portfolio_state`.
- Runtime approval is explicit: `approved=True` is only possible when governance is valid, portfolio state is recent and the kill switch is inactive.
- Tests inject deterministic timestamps so CI remains reproducible.
- No broker execution, no live trading authorization and no private edge parameters are introduced.

RGP test command:

```bash
pytest tests/test_runtime_governance_proof_pack.py -q
```

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
