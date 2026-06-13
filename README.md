# institutional-trading-engine

Institutional-grade trading decision engine with evidence-first gates, paper-observation discipline, real-data backtesting boundaries, and fail-closed governance.

## Current Validation Status

PO13: Monthly Paper Observation Review Pack implemented and CI-green
PO14: Forward Evidence Quality Gate implemented and CI-green
P120: Productive Paper Observation evidence remains gated until schema-valid durable observation artifacts are produced and CI-green.
P122: Paper Observation health gate blocks blind observation output when close/ATR/regime/scanner metrics indicate infrastructure failure.
P124: Silent-failure run health gate distinguishes valid no-trade, degraded data, fallback/demo and failed runs before reports, Paper Observation or backtests are treated as successful.
P166: Productive daily Paper Observation producer writes canonical reports/daily_evidence/<date>.json before PO11 validation and includes VIX/regime provenance.
#191: Scanner datafeed liveness gate classifies all-null close/missing-bar runs as DATAFEED_BLOCKED and writes repo-visible liveness evidence under reports/health/.
#192: Scheduled report liveness gate writes reports/scheduled_report_liveness/<date>-<type>-liveness.json, requires non-empty scheduled report/latest artifacts, requires signals and paper-health evidence for market reports, and blocks missing scheduled output from being counted as a productive report cycle.
#185: Report validation risk-tier gate requires structured decision/risk-tier evidence or an explicit no-active-risk state; prose-only Risk Tier mentions are blocked by tests/test_185_report_validation_risk_tier.py.
#186: Outcome tracking differentiates SUCCESS, BLOCKED_NO_VALID_SIGNALS, DEMO_NO_DATA and BLOCKED_MISSING_INPUTS; production outcome learning is not claimable when upstream signal files are empty, invalid or contain zero valid signals.
#177: Real-data backtest evidence requires runtime-pipeline-coupled trade plans; fake or non-runtime metadata is blocked by BT9 and scanner/signal/quality/validator exports require machine-checkable execution proof. CI run 27472676520 passed.
#194: Signal state consistency guard enforces action as the execution-readiness source of truth; exported NO_TRADE records cannot retain decision: approved, actionable risk tiers, non-zero position size or executable entry state. CI run 27472676520 passed.

Runtime Governance:
GOV1-GOV10: runtime / pre-live governance hardening implemented and CI-green
SR1-SR8: signal identity, ATR persistence, repo-write serialization, governance source enforcement, anomaly-state governance, threshold source of truth, completed-bar watcher semantics and dependency reproducibility implemented and CI-green
PSR1-PSR4: runtime evidence manifest, fill-quality evidence and drift/regime evidence linkage implemented and CI-green
RGP1: missing/invalid PortfolioState fail-closed proof implemented and CI-green
RGP2: runtime governance approval gate implemented and CI-green
RGP3: stale PortfolioState approval blocking implemented and CI-green
RGP4: actionable signal provider-fetch failure blocking implemented and CI-green
RGP5: critical STOP/EXIT alert ordering guard implemented and CI-green
RGP6: stale anomaly decision block implemented and CI-green
RGP7: no-fill fill-quality evidence guard implemented and CI-green
RGP8: position event idempotency guard implemented and CI-green
RGP9: deterministic execution ordering guard implemented and CI-green
RGP10: evidence-vs-state reconciliation guard implemented and CI-green

## Safety Boundary

- Paper-only by default.
- No live trading authorization unless explicitly proven by governance gates.
- Demo/public-safe evidence must not be promoted as real-data strategy evidence.
- CI-green is necessary but not sufficient for production-readiness claims.

## Repository Evidence Paths

- `reports/health/`
- `reports/signals/`
- `reports/daily_evidence/`
- `reports/backtests/`
- `data/historical/`
- `data/trade_plans/`

## Development Discipline

Every safety-relevant change must include:

1. a guard test,
2. a minimal implementation,
3. targeted tests,
4. full regression validation,
5. explicit documentation of the trust boundary.
