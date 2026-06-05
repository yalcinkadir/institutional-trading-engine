# Institutional Trading Engine

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![CI](https://img.shields.io/badge/CI-pytest-brightgreen.svg)
![Status](https://img.shields.io/badge/status-research--evidence--platform-orange.svg)

Institutional Trading Engine is a research, market-intelligence, screening, reporting, backtesting, evidence-validation and decision-support platform.

The system is designed for research and paper-observation evidence collection. It does not place live trades and does not authorize real-money execution.

## Current Validation Status

TEST1: Evidence-Oriented TDD Policy active

Paper Observation:
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
PO13: Monthly Paper Observation Review Pack implemented and CI-green
PO14: Forward Evidence Quality Gate implemented and CI-green
P120: Productive Paper Observation evidence remains gated until schema-valid observation artifacts are produced and CI-green.

Runtime Governance:
GOV1-GOV10: runtime / pre-live governance hardening implemented and CI-green
SR1-SR8: signal identity, ATR persistence, repo-write serialization, governance source enforcement, anomaly-state governance, threshold source of truth, completed-bar watcher semantics and dependency reproducibility implemented and CI-green
PSR1-PSR4: runtime evidence manifest, fill-quality evidence and drift/regime evidence linkage implemented and CI-green
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
RGP13: Runtime Proof Pack Summary Builder implemented and CI-green
FCM1: Feature Connectivity Matrix Guard implemented and CI-wired
RPW1: Runtime Proof-Pack Artifact Writer / Retention Index implemented and CI-wired

Backtesting / Evidence:
BT2: Strategy Test Matrix implemented
BT3: Backtest reproducibility contract implemented
BT5: Walk-Forward / Out-of-Sample Robustness Gate implemented and CI-green
BT6: Evidence Baseline Regression Gate implemented and CI-green
BT7: Capacity / Turnover / Realism Gate implemented and CI-green
CER1: Capacity / Execution Realism Evidence Review Summary implemented and CI-green
PFA1: Position-level Forward Evidence Attribution implemented and CI-green
BT8: Backtesting Evidence Report generator implemented and CI-green
BT9: Real historical backtesting remains fail-closed unless the input pack gate passes universe, bars, trade-plan and demo-data checks.
HIST1: Polygon historical bars ingestion writes canonical CSV bars plus coverage manifest for BT9 compatibility.
P121: Real historical-data backtest evidence is only claimable after a valid `real_data` evidence artifact passes the P121 schema gate.
EV1-EV12: evidence-integrity remediation implemented and CI-green

External Review Remediation:
ER1-ER15: external review remediation implemented and CI-green

Repository / Public Safety:
IP1/IP2: public/private edge boundary and public repository hygiene policy implemented
IP3/IP4: public-demo defaults and optional external edge provider boundary implemented and CI-green
IP5/IP6: artifact hygiene and .gitignore hardening implemented / CI-wired
IP9/IP10: PR public-edge review governance, license and usage disclaimer implemented / CI-wired
Report Output Boundary Guard: protected public report artifacts implemented and CI-green

Live trading authorization: not granted by code
Broker execution: paper-only infrastructure; live execution is not implemented

## TEST1 Evidence-Oriented TDD Policy

TEST1 makes test-first development mandatory for safety-relevant fixes, external review findings and trading-risk logic.

1. Guard test first
2. Minimal fix second
3. Targeted test third
4. Relevant module tests fourth
5. Full suite fifth
6. Documentation last

A fix is not complete unless a guard test captures the dangerous path, boundary case or fail-closed invariant.

Policy document:
docs/operations/test1_evidence_oriented_tdd_policy.md

## Paper Observation Evidence Process

Paper Observation is a 3-6 month evidence collection process.

Start date: 2026-06-01
Minimum duration: 3 months
Target duration: 3-6 months
First review date: 2026-07-01
Major evidence review date: 2026-09-01
Extended review date: 2026-12-01
Live trading authorization: not granted by code
Productive Paper Observation evidence is not claimed until P120 validates schema-valid durable observation artifacts in CI.

PO14 adds a forward-evidence quality gate for monthly Paper Observation packs.
CER1 adds capacity/execution realism review.
PFA1 adds position-level forward-evidence attribution by joining risk attribution with 1D, 5D, 20D, MFE and MAE outcome evidence.
FCM1 adds a feature connectivity matrix guard so implemented / CI-green features must declare runtime gates, guard tests, evidence artifacts, documentation references and upstream/downstream links.
RPW1 adds a deterministic runtime proof-pack artifact writer and retention index for review-ready runtime proof evidence.

## Historical Bars Ingestion Boundary

HIST1 uses Polygon daily aggregate bars and writes generated data under ignored local paths:

- data/historical/bars/1day/<SYMBOL>.csv
- data/historical/metadata/ingestion_status.json
- data/historical/metadata/coverage_manifest.json

Manual ingestion example:

python scripts/ingest_historical_polygon.py --symbols NVDA,AAPL,SPY --start-date 2024-01-01 --end-date 2026-01-01 --coverage-manifest-path data/historical/metadata/coverage_manifest.json

The Polygon API key must be supplied through POLYGON_API_KEY. Generated historical datasets and metadata are evidence artifacts and must not be committed to the public repository.

## Core Commands

Targeted remediation tests:
pytest tests/test_pfa1_position_forward_evidence_attribution.py -q
pytest tests/test_position_risk_attribution.py -q
pytest tests/test_outcome_tracking.py -q
pytest tests/test_cer1_capacity_execution_realism_review.py -q
pytest tests/test_bt7_capacity_turnover_realism_gate.py -q
pytest tests/test_rgp13_runtime_proof_pack_summary.py -q
pytest tests/test_po14_forward_evidence_quality_gate.py -q
pytest tests/test_fcm1_feature_connectivity_matrix_guard.py -q
pytest tests/test_rpw1_runtime_proof_pack_artifact_writer.py -q
pytest tests/test_p120_paper_observation_evidence_gate.py -q
pytest tests/test_p121_real_data_backtest_evidence_gate.py -q
pytest tests/test_bt9_real_historical_input_pack_gate.py -q
pytest tests/test_polygon_historical_ingestion.py -q

Architecture inventory:
python scripts/generate_module_inventory.py
python scripts/generate_module_inventory.py --check

after regeneration:
git add docs/architecture/module_inventory.generated.json

Documentation/status guards:
pytest tests/test_ip9_ip10_public_repo_governance.py -q
pytest tests/test_post_rgp_status_consistency.py -q
pytest tests/test_roadmap_ev_completion_guard.py -q

Full test suite:
pytest -q

## Safety Boundary

This repository is a research and paper-observation framework.

It does not authorize:
live trading
broker execution
capital allocation
production deployment
real-money execution

Any future live-execution discussion remains blocked until forward evidence, drift monitoring, risk attribution, execution-quality review, capacity/turnover realism, runtime governance hardening and manual approval are in place.
