# Institutional Trading Engine README

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
P120: Productive Paper Observation evidence remains gated until schema-valid durable observation artifacts are produced and CI-green.
P122: Paper Observation health gate blocks blind observation output when close/ATR/regime/scanner metrics indicate infrastructure failure.
P124: Silent-failure run health gate distinguishes valid no-trade, degraded data, fallback/demo and failed runs before reports, Paper Observation or backtests are treated as successful.

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
W1: Entry/Exit Watcher Git-Write Decoupling implemented and CI-green
RGP8: alert/evidence artifact upload-on-failure guard implemented and CI-green
RGP9: signal lifecycle status source of truth implemented and CI-green
RGP10: latest bar timestamp ordering guard implemented and CI-green
RGP11: signal identity float quantization implemented and CI-green
RGP12: partial-exit lifecycle persistence implemented and CI-green
RGP13: Runtime Proof Pack Summary Builder implemented and CI-green
FCM1: Feature Connectivity Matrix Guard implemented and CI-wired
RPW1: Runtime Proof-Pack Artifact Writer / Retention Index implemented and CI-wired
DATA1: Market data quality contract blocks missing close/ATR, stale timestamps and missing source metadata before signals or reports consume them.

Backtesting / Evidence:
BT2: Strategy Test Matrix implemented
BT3: Backtest reproducibility contract implemented
BT5: Walk-Forward / Out-of-Sample Robustness Gate implemented and CI-green
BT6: Evidence Baseline Regression Gate implemented and CI-green
BT7: Capacity / Turnover / Realism Gate implemented and CI-green
BT130: Real Historical Backtest Evidence Pack Gate implemented / CI-pending
CER1: Capacity / Execution Realism Evidence Review Summary implemented and CI-green
PFA1: Position-level Forward Evidence Attribution implemented and CI-green
BT8: Backtesting Evidence Report generator implemented and CI-green
BT9: Real historical backtesting remains fail-closed unless the input pack gate passes universe, bars, trade-plan and demo-data checks.
UNI1: Initial survivorship universe contract defines point-in-time symbol lifecycle validation for real backtesting.
HIST1: Polygon historical bars ingestion writes canonical CSV bars plus coverage manifest for BT9 compatibility.
HTP1: Validated Paper Observation records can be exported into deterministic historical trade plans plus manifest for BT9 compatibility.
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

## Paper Observation Health Gate

P122 prevents silent blind Paper Observation output after DATA1 and CLOSE1 are restored.

A Paper Observation report is unhealthy when:

- all or most symbol close values are missing
- all or most ATR values are missing
- market_regime remains Unknown despite available close/ATR data
- scanner metrics are missing for core symbols
- actionable_count is zero because required market-data fields are missing

A zero-actionable day is still allowed when close values, ATR values, market regime and scanner metrics are present. P122 does not loosen signal thresholds and does not create trades artificially.

## Silent-Failure Run Health Gate

P124 introduces an explicit run-health classification so empty or degraded outputs cannot be mistaken for successful no-trade days.

Market reports and signal generation expose:

- run_health_status
- success_status
- signal_generation_status
- scanner_data_quality
- reasons

Supported health outcomes include:

- OK
- NO_TRADE_VALID
- DEGRADED_DATA
- EMPTY_INPUT
- FALLBACK_ACTIVE
- FAILED

Reports render a dedicated Run Health / Silent-Failure Gate block. Real-data backtest evidence also includes input_completeness_status and run_health_status.

## Entry/Exit Watcher Runtime Output Boundary

W1 keeps the scheduled Entry/Exit Watcher read-only against the repository. Runtime outputs are uploaded as GitHub Actions artifacts instead of being committed back to the schedule branch.

The watcher workflow must keep:

- repository contents permission at read-only scope
- checkout credentials non-persistent
- no scheduled `git add`, `git commit`, `git pull --rebase` or `git push`
- runtime output upload through `actions/upload-artifact@v4`
- isolated watcher concurrency instead of the shared repo-write group

This protects main from scheduled runtime artifact mutation while preserving reviewable watcher evidence.

## Market Data Quality Boundary

DATA1 defines the central market-data quality contract used before report, signal, paper-observation or decision paths consume symbol metrics.

Required per-symbol fields:

- close
- ATR
- source / vendor
- source timestamp
- fallback level
- fallback status

The DATA1 contract returns one of three statuses:

- ok: all required data is present, fresh and provenance-aware
- degraded: non-blocking provenance gaps are recorded explicitly, such as missing fallback metadata
- blocked: missing close, missing ATR, missing source, invalid timestamp or stale source timestamp blocks downstream use

Signals consuming DATA1 receive the same data_status, provenance and structured data_quality_events as report paths. This prevents missing close/ATR from becoming a silent zero-actionable no-op.

## Survivorship Universe Boundary

UNI1 defines the first controlled survivorship-aware universe contract for real historical backtesting.

Required canonical file:

data/universe/survivorship_universe.csv

Required columns:

symbol, effective_from, effective_to, active, asset_class, exchange, source, status, reason

The initial universe is intentionally small and auditable. It is not a full institutional survivorship database. It is the first point-in-time lifecycle source that blocks real backtests when a requested symbol is missing, malformed or inactive for the tested date range.

Manual validation example:

python scripts/validate_survivorship_universe.py --universe data/universe/survivorship_universe.csv --symbols SPY,QQQ,AAPL,MSFT,NVDA,GOOGL,META,GLD --start-date 2021-01-01 --end-date 2021-01-02

## Historical Bars Ingestion Boundary

HIST1 uses Polygon daily aggregate bars and writes generated data under ignored local paths:

- data/historical/bars/1day/<SYMBOL>.csv
- data/historical/metadata/ingestion_status.json
- data/historical/metadata/coverage_manifest.json

Manual ingestion example:

python scripts/ingest_historical_polygon.py --symbols NVDA,AAPL,SPY --start-date 2024-01-01 --end-date 2026-01-01 --coverage-manifest-path data/historical/metadata/coverage_manifest.json

The Polygon API key must be supplied through POLYGON_API_KEY. Generated historical datasets and metadata are evidence artifacts and must not be committed to the public repository.

## Historical Trade Plans Export Boundary

HTP1 converts validated Paper Observation records into deterministic historical trade plans.

Required canonical outputs:

- data/trade_plans/historical_trade_plans.json
- data/trade_plans/historical_trade_plans_manifest.json

The exporter accepts JSON or CSV observation records. It fails closed when a record is missing close, entry, stop, target, timestamp, symbol, data status or provenance. It also rejects demo, synthetic, placeholder and public-safe markers for real historical trade-plan evidence.

Manual export example:

python scripts/export_historical_trade_plans.py --source artifacts/evidence/paper-observation/latest-observations.json --output data/trade_plans/historical_trade_plans.json --manifest data/trade_plans/historical_trade_plans_manifest.json

The exported plans remain paper-only / research-only evidence. They are inputs for historical backtesting and do not authorize live trading.

## Real Historical Backtest Evidence Pack Gate

BT130 requires any real-data backtest claim to write a complete evidence pack. The JSON artifact must include run identity, `data_source=real_data`, `is_demo=false`, symbol universe, date range, strategy version, BT9 input-pack gate status, input completeness status, run health status, coverage manifest path, survivorship universe path, trade-plan path, input/accepted/rejected plan counts, rejection reasons, metrics, results, and paper-only execution boundaries.

Real-data backtests fail closed when the coverage manifest is missing or when all trade plans are rejected. Invalid trade plans are counted with explicit rejection reasons instead of being silently skipped.

Demo, synthetic, placeholder and public-safe backtests are never trading-edge evidence. They may be used only for parser, workflow and guard validation.

P151 adds an orchestrated real-data evidence-pack builder that either writes a `BLOCKED` package with explicit reasons or a `VALID` package after the real-data BT130 gate passes.

Manual real-data evidence example:

python scripts/run_historical_entry_exit_backtest.py --plans-file data/trade_plans/historical_trade_plans.json --bars-root data/historical/bars/1day --universe data/universe/survivorship_universe.csv --coverage-manifest data/historical/metadata/coverage_manifest.json --run-id real-bt-manual-001 --real-data --json-output reports/backtests/real-data-backtest-evidence.json --markdown-output reports/backtests/real-data-backtest-evidence.md

P151 evidence package example:

python scripts/build_real_data_backtest_evidence_pack.py --symbols SPY,QQQ,AAPL --start-date 2024-01-01 --end-date 2026-01-01 --run-id real-bt-manual-001 --plans-file data/trade_plans/historical_trade_plans.json --bars-root data/historical/bars/1day --universe data/universe/survivorship_universe.csv --coverage-manifest data/historical/metadata/coverage_manifest.json --output-dir reports/backtests/real-data-evidence-pack

Validation example:

python scripts/validate_real_data_backtest_evidence_gate.py --artifact reports/backtests/real-data-backtest-evidence.json

## Core Commands

Targeted remediation tests:
pytest tests/test_p124_silent_failure_health_gate.py -q
pytest tests/test_pfa1_position_forward_evidence_attribution.py -q
pytest tests/test_position_risk_attribution.py -q
pytest tests/test_outcome_tracking.py -q
pytest tests/test_cer1_capacity_execution_realism_review.py -q
pytest tests/test_bt7_capacity_turnover_realism_gate.py -q
pytest tests/test_rgp13_runtime_proof_pack_summary.py -q
pytest tests/test_po14_forward_evidence_quality_gate.py -q
pytest tests/test_w1_entry_exit_watcher_git_write_decoupling.py -q
pytest tests/test_fcm1_feature_connectivity_matrix_guard.py -q
pytest tests/test_rpw1_runtime_proof_pack_artifact_writer.py -q
pytest tests/test_p120_paper_observation_evidence_gate.py -q
pytest tests/test_p121_real_data_backtest_evidence_gate.py -q
pytest tests/test_bt130_real_historical_evidence_pack_gate.py -q
pytest tests/test_bt9_real_historical_input_pack_gate.py -q
pytest tests/test_p151_real_data_backtest_evidence_pack.py -q
pytest tests/test_uni1_survivorship_universe_contract.py -q
pytest tests/test_polygon_historical_ingestion.py -q
pytest tests/test_htp1_historical_trade_plan_export.py -q
pytest tests/test_data1_market_data_quality_contract.py -q

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
