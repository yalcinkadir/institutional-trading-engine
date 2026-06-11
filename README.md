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
P120: Productive Paper Observation evidence remains gated until schema-valid durable observation artifacts are produced and CI-green.
P122: Paper Observation health gate blocks blind observation output when close/ATR/regime/scanner metrics indicate infrastructure failure.
P124: Silent-failure run health gate distinguishes valid no-trade, degraded data, fallback/demo and failed runs before reports, Paper Observation or backtests are treated as successful.
P166: Productive daily Paper Observation producer writes canonical `reports/daily_evidence/<date>.json` before PO11 validation and includes VIX/regime provenance.
#191: Scanner datafeed liveness gate classifies all-null close/missing-bar runs as `DATAFEED_BLOCKED` and writes repo-visible liveness evidence under `reports/health/`.
#192: Scheduled report liveness gate writes `reports/scheduled_report_liveness/<date>-<type>-liveness.json`, requires non-empty scheduled report/latest artifacts, requires signals and paper-health evidence for market reports, and blocks missing scheduled output from being counted as a productive report cycle.
#185: Report validation risk-tier gate requires structured decision/risk-tier evidence or an explicit no-active-risk state; prose-only `Risk Tier` mentions are blocked by `tests/test_185_report_validation_risk_tier.py`.

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
FCM1: Feature Connectivity Matrix Guard closed / targeted CI-wired; no repository-wide full-regression green claimed
RPW1: Runtime Proof-Pack Artifact Writer / Retention Index closed / targeted CI-wired; no repository-wide full-regression green claimed
DATA1: Market data quality contract blocks missing close/ATR, stale timestamps and missing source metadata before signals or reports consume them.
P161: Dataflow Contract Matrix defines Scanner → Signals → Quality → Validator → Watcher → Evidence required fields, canonical ATR naming and fail-closed missing-field behavior.
P164: VIX/regime evidence first uses Polygon `I:VIX`; if unavailable because of provider entitlement, it falls back to configured volatility proxy `VOLATILITY_PROXY_SYMBOL` defaulting to `VIXY` and stamps `PROXY_DEGRADED` provenance.
#178: Runtime reachability guard adds `docs/architecture/decision_critical_runtime_reachability.json` and `tests/test_runtime_reachability_guard_178.py` so decision-critical modules are either runtime-connected with proof or explicitly classified as non-runtime research/quarantine/test/deprecated.
#188: Evidence Quality Gate adds `docs/operations/evidence-quality-gate.md`, `src/evidence_quality_gate.py`, `scripts/evaluate_evidence_quality_gate.py` and `tests/test_evidence_quality_gate_188.py` so roadmap, strategy, paper-confidence, production-grade evidence and live-readiness claims are blocked unless evidence quality is proven.
#189: System Invariants and Logic Safety Governance implemented as machine-checkable documentation/test guards; `DEGRADED`, `BLOCKED`, `UNKNOWN`, demo/stub and missing-provenance states must not be promoted as full `PASS` evidence.

Backtesting / Evidence:
BT2: Strategy Test Matrix implemented
BT3: Backtest reproducibility contract implemented
BT5: Walk-Forward / Out-of-Sample Robustness Gate implemented and CI-green
BT6: Evidence Baseline Regression Gate implemented and CI-green
BT7: Capacity / Turnover / Realism Gate implemented and CI-green
BT130: Real Historical Backtest Evidence Pack Gate implemented / CI-pending
BT131: Real-data backtest evidence workflow implemented / CI-pending; valid output requires BT9 and P121/BT130 gates, otherwise a BLOCKED artifact is uploaded.
#177: Real-data historical trade plans can now be exported through the actual Scanner → Signal Generator → Entry/Stop/Exit Quality → Trade Plan Validator path using `scripts/export_historical_trade_plans.py`; non-pipeline-coupled plans remain blocked from real-data evidence claims.
#184: Historical real-data backtest inputs must be durable and auditable. Polygon CSV bars are persisted under `data/historical/bars/1day/*.csv`, coverage manifests include SHA256 checksums, BT9 fails on missing/mismatched input checksums, and accepted real-data evidence must include `input_checksums`.
CER1: Capacity / Execution Realism Evidence Review Summary implemented and CI-green
PFA1: Position-level Forward Evidence Attribution implemented and CI-green
BT8: Backtesting Evidence Report generator implemented and CI-green
BT9: Real historical backtesting remains fail-closed unless the input pack gate passes universe, bars, trade-plan, demo-data and coverage-manifest checksum checks.
UNI1: Initial survivorship universe contract defines point-in-time symbol lifecycle validation for real backtesting.
HIST1: Polygon historical bars ingestion writes canonical CSV bars plus coverage manifest with `output_sha256` for BT9 compatibility.
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

## Logic Safety Governance

#189 adds machine-checkable System Invariants and Logic Safety Governance.

Policy documents:

- `docs/architecture/system-invariants.md`
- `docs/operations/logic-safety-governance.md`
