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
PO1: Paper Observation timeline and review gate implemented and CI-green
PO2: Daily Observation Acceptance Gate implemented and CI-green
PO3: Daily Observation Run Record implemented and CI-green
PO4: Daily Observation Record Validator implemented and CI-green
PO5: Daily Observation Record Writer implemented and CI-green
PO6: Daily Observation Record Artifact Contract implemented and CI-green
PO7: Daily Observation Record Index implemented and CI-green
PO8: Daily Observation Review Summary implemented and CI-green
PO9: Paper Observation Review Gate implemented and CI-green
PO10: Daily Observation Automation Runner implemented and CI-green
PO11: Scheduled Daily Observation Workflow implemented and CI-green
PO12: Daily Observation Artifact Retention & Review Index implemented and CI-green
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
BT8: Backtesting Evidence Report generator implemented and CI-green
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
RGP4: actionable signal provider-fetch failure blocking implemented and CI-green
RGP5: critical STOP/EXIT alert ordering guard implemented and CI-green
RGP6: strict critical notification failure handling implemented and CI-green
RGP7: repo-writing workflow serialization/retry guard implemented and CI-green
RGP8: alert/evidence artifact upload-on-failure guard implemented and CI-green
RGP9: signal lifecycle status source of truth implemented and CI-green
RGP10: latest bar timestamp ordering guard implemented and CI-green
RGP11: signal identity float quantization implemented and CI-green
RGP12: partial-exit lifecycle persistence implemented and CI-green
Live trading authorization: not granted by code
Broker execution: paper-only infrastructure; live execution is not implemented
```

Code quality is not trading edge. The system is promising enough to test seriously, but real capital still requires long-running forward evidence, drift detection, regime-change monitoring, position-level risk attribution, execution-quality review, capacity/turnover realism and manual approval.

## PO1 Paper Observation Timeline

PO1 formalizes Paper Observation as a 3-6 month evidence process.

```text
Paper Observation start date: 2026-06-01
Minimum duration: 3 months
Target duration: 3-6 months
First review date: 2026-07-01
Major evidence review date: 2026-09-01
Target extended review date: 2026-12-01
Live trading authorization: not granted by code
```

```bash
pytest tests/test_po1_paper_observation_timeline.py -q
```

## PO2 Daily Observation Acceptance Gate

PO2 defines when a Paper Observation day is accepted as valid evidence. A day must have required evidence families, generated reports, artifact references, research-only status and no live-trading authorization.

```text
ACCEPTED
REJECTED
NEEDS_REVIEW
```

```bash
pytest tests/test_po2_daily_observation_acceptance_gate.py -q
```

## PO3 Daily Observation Run Record

PO3 defines the machine-readable daily Paper Observation run record. Each observation day records status, missing evidence, incidents, artifact paths, review requirement and the hard paper-only execution boundary.

```text
date
status: ACCEPTED / REJECTED / NEEDS_REVIEW
missing_evidence
incidents
artifact_paths
review_required
review_notes
live_trading_authorized: false
broker_execution_mode: paper_only
created_at
```

```bash
pytest tests/test_po3_daily_observation_run_record.py -q
```

## PO4 Daily Observation Record Validator

PO4 adds executable validation for the PO3 Daily Observation Run Record. It checks required fields, status consistency, ISO date fields, list typing and the paper-only execution boundary.

Test command:

    pytest tests/test_po4_daily_observation_record_validator.py -q

PO4 does not authorize live trading.

## PO5 Daily Observation Record Writer

PO5 generates machine-readable PO3 Daily Observation Run Records and validates them with the PO4 validator before writing JSON output.

Test command:

    pytest tests/test_po5_daily_observation_record_writer.py -q

PO5 maps clean days to ACCEPTED, missing evidence to REJECTED and documented incidents to NEEDS_REVIEW. Invalid records are not written. PO5 does not authorize live trading.

## PO6 Daily Observation Record Artifact Contract

PO6 defines the canonical artifact path contract for PO3 Daily Observation Run Records generated by PO5.

Root:

    reports/daily_observation_records/

Filename format:

    YYYY-MM-DD.json

Example:

    reports/daily_observation_records/2026-06-01.json

Test command:

    pytest tests/test_po6_artifact_contract.py -q

PO6 does not authorize live trading.

## PO7 Daily Observation Record Index

PO7 adds a deterministic index for PO3 Daily Observation Run Records generated by PO5 and stored according to the PO6 artifact contract.

Index path:

    reports/daily_observation_records/index.json

Index includes:

    total_records
    status_counts
    records[]
    records[].date
    records[].status
    records[].path
    records[].review_required
    records[].missing_evidence_count
    records[].incident_count
    live_trading_authorized: false
    broker_execution_mode: paper_only

Test command:

    pytest tests/test_po7_daily_observation_record_index.py -q

PO7 does not authorize live trading.

## PO8 Daily Observation Review Summary

PO8 builds a deterministic review summary from the PO7 Daily Observation Record Index.

Summary includes:

    total_records
    accepted_count
    rejected_count
    needs_review_count
    review_required_dates
    rejected_dates
    needs_review_dates
    review_ready
    live_trading_authorized: false
    broker_execution_mode: paper_only

Review readiness requires at least one observation record, zero rejected records, zero needs-review records, no review-required records and no consistency errors.

Test command:

    pytest tests/test_po8_daily_observation_review_summary.py -q

PO8 does not authorize live trading.

## PO9 Paper Observation Review Gate

PO9 evaluates the PO8 Daily Observation Review Summary and decides whether Paper Observation evidence is ready for human review.

Gate status:

    PASSED
    BLOCKED

PO9 passes only when the PO8 summary is review-ready, the minimum observation-record requirement is met, all records are accepted, no rejected or needs-review days exist, no manual-review dates remain and the paper-only boundary is preserved.

Test command:

    pytest tests/test_po9_paper_observation_review_gate.py -q

PO9 does not authorize live trading. A passed PO9 gate means review-ready paper-observation evidence only.

## PO10 Daily Observation Automation Runner

PO10 automates the daily Paper Observation evidence chain by connecting PO5, PO7, PO8 and PO9 into one deterministic runner.

Automation flow:

    Daily Observation input
    -> PO5 Daily Observation Record
    -> PO7 Daily Observation Record Index
    -> PO8 Daily Observation Review Summary
    -> PO9 Paper Observation Review Gate
    -> PO10 Automation Artifact

Canonical automation artifact root:

    reports/daily_observation_automation/

Artifact filename format:

    YYYY-MM-DD.json

Automation status:

    PASSED
    BLOCKED

Test command:

    pytest tests/test_po10_daily_observation_automation_runner.py -q

PO10 does not authorize live trading. A passed PO10 artifact means the daily Paper Observation automation chain completed and the resulting evidence package is review-ready according to PO9.

## PO11 Scheduled Daily Observation Workflow

PO11 schedules the PO10 Daily Observation Automation Runner through GitHub Actions.

Workflow file:

    .github/workflows/po11_daily_observation.yml

Scheduled run:

    15 22 * * 1-5

This runs Monday to Friday at 22:15 UTC. Manual dispatch supports `observation_date` and `minimum_records` inputs.

PO11 uploads the generated PO10 automation artifact:

    po11-daily-observation-artifact

Artifact path:

    reports/daily_observation_automation/*.json

Test command:

    pytest tests/test_po11_scheduled_daily_observation_workflow.py -q

PO11 uses read-only repository permissions and does not authorize live trading. It preserves `live_trading_authorized=false` and `broker_execution_mode=paper_only`.

## PO12 Daily Observation Artifact Retention & Review Index

PO12 builds a deterministic review index over generated PO10/PO11 daily observation automation artifacts.

Review index path:

    reports/daily_observation_automation/review_index.json

Default retention metadata:

    retention_days: 180

The review index includes:

    total_artifacts
    status_counts
    passed_count
    blocked_count
    review_ready_count
    artifacts[]
    artifacts[].observation_date
    artifacts[].artifact_path
    artifacts[].automation_status
    artifacts[].review_ready
    artifacts[].gate_status
    artifacts[].approved_for_review
    artifacts[].blocker_count
    artifacts[].error_count
    live_trading_authorized: false
    broker_execution_mode: paper_only

Test command:

    pytest tests/test_po12_daily_observation_artifact_review_index.py -q

PO12 does not authorize live trading. A valid PO12 index means generated observation artifacts are structured for review only.

## BT8 Backtesting Evidence Report

BT8 turns reproducible BT3 backtest run contracts into audit-friendly JSON and Markdown evidence reports. The report summarizes run count, strategy count, datasets, symbols, trades, average return, average win rate, average Sharpe, worst max drawdown, BT3 gate results, run-level metrics and research-only limitations.

```bash
python scripts/generate_backtesting_evidence_report.py \
  --contracts-json reports/backtest_run_contract/contracts.json \
  --output-json reports/backtesting_evidence/bt8_report.json \
  --output-md reports/backtesting_evidence/bt8_report.md
```

```bash
pytest tests/test_bt8_backtesting_evidence_report.py -q
```

BT8 does not authorize live trading. It is a research / paper-observation evidence report.

## RGP Runtime Governance Proof Pack

RGP proves that runtime governance fails closed when safety evidence is missing, invalid or stale. It is an audit/proof phase, not a strategy-expansion phase.
