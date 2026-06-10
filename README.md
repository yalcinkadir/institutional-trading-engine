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
#189: System Invariants and Logic Safety Governance implemented as machine-checkable documentation/test guards; `DEGRADED`, `BLOCKED`, `UNKNOWN`, demo/stub and missing-provenance states must not be promoted as full `PASS` evidence.

Backtesting / Evidence:
BT2: Strategy Test Matrix implemented
BT3: Backtest reproducibility contract implemented
BT5: Walk-Forward / Out-of-Sample Robustness Gate implemented and CI-green
BT6: Evidence Baseline Regression Gate implemented and CI-green
BT7: Capacity / Turnover / Realism Gate implemented and CI-green
BT130: Real Historical Backtest Evidence Pack Gate implemented / CI-pending
BT131: Real-data backtest evidence workflow implemented / CI-pending; valid output requires BT9 and P121/BT130 gates, otherwise a BLOCKED artifact is uploaded.
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

## Logic Safety Governance

#189 adds machine-checkable System Invariants and Logic Safety Governance.

Policy documents:

- `docs/architecture/system-invariants.md`
- `docs/operations/logic-safety-governance.md`

The core rule is simple: unknown, degraded, blocked, demo/stub or missing-provenance states must never be promoted as full `PASS` evidence.

Initial core invariants:

- `SI-001 No silent success`
- `SI-002 No uncoupled strategy evidence`
- `SI-003 No unknown regime promotion`
- `SI-004 No placeholder scoring in confidence/readiness`
- `SI-005 No missing provenance for production-grade evidence`
- `SI-006 No decision-critical module without runtime reachability`
- `SI-007 DEGRADED must not behave like PASS`

Relevant guard tests:

```bash
pytest tests/test_system_invariants.py tests/test_logic_safety_state_matrix.py tests/test_evidence_traceability_contract.py -q
```

## Paper Observation Evidence Process

Paper Observation is a 3-6 month evidence collection process.

Start date: 2026-06-01
Minimum duration: 3 months
Target duration: 3-6 months
First review date: 2026-07-01
Major evidence review date: 2026-09-01
Extended review date: 2026-12-01
Live trading authorization: not granted by code
Productive Paper Observation evidence is produced by `scripts/produce_daily_observation_evidence_p166.py` and written to `reports/daily_evidence/<observation_date>.json` before PO11 validation.

The scheduled PO11 workflow runs the P166 producer, validates the generated evidence through the existing daily observation record path, uploads `reports/daily_evidence/*.json`, and then uploads the PO11 automation artifact. Runtime evidence is not committed back to `main`.

PO14 adds a forward-evidence quality gate for monthly Paper Observation packs.
CER1 adds capacity/execution realism review.
PFA1 adds position-level forward-evidence attribution by joining risk attribution with 1D, 5D, 20D, MFE and MAE outcome evidence.
FCM1 adds a feature connectivity matrix guard so implemented / CI-green features must declare runtime gates, guard tests, evidence artifacts, documentation references and upstream/downstream links.
RPW1 adds a deterministic runtime proof-pack artifact writer and retention index for review-ready runtime proof evidence.

## Backtesting Evidence Process

BT131 provides a manual GitHub Actions workflow for real-data backtest evidence generation:

```bash
gh workflow run bt131_real_data_backtest_evidence.yml \
  -f symbols=MSFT,NVDA,META,AAPL,MU,QQQ,GLD,SLV \
  -f start_date=2024-01-01 \
  -f end_date=2026-06-09 \
  -f run_id=bt131-real-data-manual \
  -f strategy_version=historical-entry-exit-v1 \
  -f plans_file=data/trade_plans/historical_trade_plans.json
```

The workflow ingests Polygon historical bars when `POLYGON_API_KEY` is available, validates the BT9 real historical input pack, runs the real-data historical entry/exit backtest, validates accepted evidence through the P121/BT130 gate, and uploads JSON/Markdown artifacts.

If required real inputs are missing, invalid, demo, synthetic, placeholder or public-safe, the workflow must write and upload a `BLOCKED` real-data evidence artifact instead of claiming productive historical evidence.

## Architecture Contracts

The active pipeline contract is documented in `docs/architecture/dataflow_contract_matrix.md`.

The matrix defines required fields across Scanner → Signals → Quality → Validator → Watcher → Evidence, including `signal_id`, `action`, `decision`, `entry_trigger`, `stop_loss`, `target_1`, `run_health_status`, and the canonical `atr14` naming rule.

Missing critical downstream fields must fail closed as `BLOCKED_MISSING_INPUTS`; they must not be silently interpreted as valid `NO_TRADE_VALID` days.

## Regime / VIX Data Quality Policy

The regime path first attempts the true Polygon VIX index ticker `I:VIX`. If that ticker is unavailable because the configured provider tier lacks entitlement, the system uses a configured volatility proxy from `VOLATILITY_PROXY_SYMBOL`, defaulting to `VIXY`.

Proxy evidence is useful for Paper Observation continuity, but it is not full VIX validation. Proxy-backed regime evidence is stamped with `source=polygon_proxy`, `status=PROXY_DEGRADED`, `validation_status=DEGRADED`, `reason=VIX_PROXY_FALLBACK`, and `live_or_paper_confidence_authorized=false`.

If neither true VIX nor proxy evidence is available, the system stamps `UNVALIDATED_REGIME` with `VIX_UNAVAILABLE_ENTITLEMENT` or `VIX_UNAVAILABLE`. Such runs may proceed for research visibility but do not authorize live trading, paper-confidence claims, or evidence-quality claims.
