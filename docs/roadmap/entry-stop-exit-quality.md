# Entry / Stop / Exit Decision Quality Roadmap

Decision logic must work excellently. The system must not only produce signals; it must produce executable, explainable and falsifiable trade plans.

The most important rule:

```text
No BUY_WATCH without a complete and valid trade plan.
```

A complete trade plan requires:

```text
entry_trigger + entry_reason
stop_loss + stop_reason
target_1 + exit_reason
risk_reward validation
quality gate passed
```

---

## Current Implemented Baseline

Implemented and CI-green:

- native `signal_id` generation
- watcher fallback identity for older signals
- lifecycle deduplication by `signal_id + event_type`
- central notification CLI
- structured runtime logs
- executable-level quality gate
- Entry Quality Engine
- Stop-Loss Quality Engine
- Exit / Target Quality Engine
- Trade Plan Validator
- Scanner-to-Signal Metrics Pipeline normalizer
- native scanner `swing_low_3bar`
- Intraday VWAP support when intraday bars are available
- Trailing Stop and Partial Exit Management
- Regime Invalidation Exit
- Pending Signal Regime Invalidation
- Entry / Stop / Exit Backtest Feedback
- Regime-aware feedback grouping
- initial file-backed portfolio state
- End-to-End Dry Run validator

The executable-level quality gate means:

```text
BUY_WATCH requires entry_trigger, stop_loss, target_1 and a valid quality gate result.
```

If those fields or quality gates are incomplete, the signal is downgraded to:

```text
NO_TRADE
```

---

## Go-Live Operating Gates

Before scheduled live Decision-Support is enabled:

```text
1. CI green
2. POLYGON_API_KEY set
3. Telegram/notification secrets verified when alerts are enabled
4. data/portfolio_state.json present and intentionally initialized
5. generate_report produces latest-signals.json
6. E2E dry-run returns PASS
7. manual watcher run completes successfully
8. 5 consecutive entry-exit-watcher runs are green
```

Live mode remains:

```text
Decision-Support only
```

Non-goal:

```text
No broker execution. No automatic live orders.
```

---

## Historical Data / Strategy Training Roadmap

This is the next major quality phase after operational live-readiness.

The goal is not to blindly “train a strategy”. The goal is to create a falsifiable historical research loop:

```text
Historical data ingestion
→ Historical feature generation
→ Entry/Stop/Exit backtest
→ Regime-aware validation
→ Out-of-sample testing
→ Scoring/expectancy feedback
→ Paper-live observation
→ trading decision
```

Training is only allowed after out-of-sample validation.

---

## P23 — Historical Polygon Data Ingestion

### Goal

Build a reliable historical data foundation from Polygon data.

After the Stock Developer/Advanced-style Polygon subscription is enabled, the system should be able to ingest long-range historical OHLCV data for the configured universe.

### Requirements

- Add historical Polygon aggregate downloader.
- Support daily bars first.
- Support intraday bars later where plan/rate limits allow.
- Store historical bars locally in a backtest-friendly format.
- Prefer Parquet for compact analytics storage.
- Avoid duplicate bars.
- Add retry and rate-limit handling.
- Add symbol-level ingestion status.
- Add metadata file with ingestion range, symbol, timespan and last update.
- Keep ingestion deterministic and resumable.

### Initial Storage Layout

```text
data/historical/bars/1d/NVDA.parquet
data/historical/bars/1d/AAPL.parquet
data/historical/bars/1d/SPY.parquet
data/historical/metadata/ingestion_status.json
```

### Acceptance Criteria

- Historical downloader can fetch a configured symbol and date range.
- Saved data contains date/time, open, high, low, close, volume.
- Duplicate bars are removed.
- Missing/empty Polygon responses are visible.
- Tests use mocked Polygon responses, not live API calls.
- README and architecture docs explain how to run ingestion.

### Status

Planned for tomorrow.

---

## P24 — Historical Entry / Stop / Exit Backtest Runner

### Goal

Use historical bars to evaluate whether generated trade plans would have worked.

This is not yet ML training. This is deterministic strategy falsification.

### Requirements

- Load historical bars from P23 storage.
- Generate historical scanner metrics per symbol/date.
- Reconstruct Entry / Stop / Exit trade plans.
- Simulate future bars after signal date.
- Measure whether entry was hit, stop was hit, target_1 was hit, target_2 was hit or signal expired.
- Use conservative event ordering when one bar touches both stop and target.
- Group results by entry_type, setup_type, stop_model, exit_model, market_regime, risk_state and volatility_regime.

### Required Metrics

```text
entry_hit_rate
expired_without_entry_rate
stop_hit_rate
target_1_hit_rate
target_2_hit_rate
false_breakout_rate
average_R
expectancy_R
max_adverse_excursion
max_favorable_excursion
```

### Acceptance Criteria

- Backtest runner produces deterministic JSON/Markdown report.
- Backtest uses historical bars, not synthetic data.
- Results can feed existing Entry / Stop / Exit feedback aggregation.
- Tests cover entry hit, stop hit, T1 hit, T2 hit, expiry and same-bar stop/target ordering.

### Status

Planned after P23.

---

## P25 — Out-of-Sample Validation and Adaptive Feedback Integration

### Goal

Prevent overfitting before using historical results for scoring changes.

### Required Dataset Split

```text
Training period:   older historical data
Validation period: middle historical data
Out-of-sample:     most recent untouched historical data
```

Example split for long history:

```text
2012–2020 training
2021–2023 validation
2024–2026 out-of-sample test
```

### Requirements

- Add configurable date split definition.
- Produce separate metrics for training, validation and out-of-sample windows.
- Only allow scoring adjustments when validation and out-of-sample results agree directionally.
- Add guardrails against over-optimization.
- Persist model feedback history.
- Feed validated adjustments into existing expectancy/scoring system.

### Acceptance Criteria

- Backtest report clearly separates training, validation and out-of-sample periods.
- No scoring adjustment is accepted based only on training-period performance.
- Poor models can reduce future scores only after validation.
- Documentation warns against overfitting.

### Status

Planned after P24.

---

## P26 — Paper-Live Observation Before Trading

### Goal

Observe the system in live Decision-Support mode before any real trading decision.

### Requirements

- Run scheduled Decision-Support for a defined observation window.
- Compare live signals with actual outcomes.
- Verify Telegram/alerts, lifecycle updates and feedback reports.
- Review false breakout rate, stop rate and expectancy.
- Keep manual portfolio_state.json accurate if no broker sync exists.

### Suggested Gate

```text
Minimum 2–4 weeks paper-live observation
No real broker automation
Manual review of every actionable signal
```

### Acceptance Criteria

- Observation report exists.
- Alerts are reliable.
- Watcher is stable.
- Feedback is usable.
- No critical data-pipeline warnings remain.

### Status

Planned after P25 and live dry-run validation.

---

## Completed Decision-Quality Items

### P15 — Scanner-to-Signal Data Pipeline Repair

Status: implemented and CI-green.

### P14.1 — Trade Plan Validator

Status: implemented and CI-green.

### P14.2 — Entry Quality Engine

Status: implemented and CI-green.

### P14.3 — Stop-Loss Quality Engine

Status: implemented and CI-green.

### P14.4 — Exit / Target Quality Engine

Status: implemented and CI-green.

### P18A — Breakout Entry Context Upgrade

Status: implemented and CI-green.

### P16 — Trailing Stop and Partial Exit Management

Status: implemented and CI-green.

### P17 — Structure-Aware Stops

Status: implemented and CI-green.

### P17B — Native Scanner Structure Metric

Status: implemented and CI-green.

### P18B — VWAP / Intraday Entry Timing Upgrade

Status: implemented and CI-green.

### P20 — Regime Invalidation Exit

Status: implemented and CI-green.

### P20B — Pending Signal Regime Invalidation

Status: implemented and CI-green.

### P14.5 — Entry / Stop / Exit Backtest Feedback

Status: implemented and CI-green.

### P21 — Regime-Aware Feedback Grouping

Status: implemented and CI-green.

### P22 — End-to-End Dry Run Support

Status: implemented and CI-green.

---

## Future Module — P19 Short-Side Decision Path

### Problem

The current system is long-only. That limits hedge, downside and market-neutral use cases.

### Requirements

- Add short entry quality derivation.
- Add short stop quality derivation using stop above entry.
- Add short target quality derivation using targets below entry.
- Add validator support for short trade plans.

### Acceptance Criteria

- `SELL_WATCH` or equivalent short action can be generated.
- Short plan validates entry > target and stop > entry.
- Long and short validation paths are tested separately.

### Status

Planned after historical validation foundation.

---

## Updated Implementation Order

```text
0. Complete operational go-live checks for Decision-Support mode
1. Enable Polygon Stock subscription with required historical range
2. P23 Historical Polygon Data Ingestion
3. P24 Historical Entry / Stop / Exit Backtest Runner
4. P25 Out-of-Sample Validation and Adaptive Feedback Integration
5. P26 Paper-Live Observation Before Trading
6. Fix missing points discovered by historical tests and paper-live observation
7. Only then decide about real trading
8. P19 Short-Side Decision Path later
9. README + architecture documentation after every patch
```

---

## Non-Goals

- broker execution
- live order placement
- blind ML prediction engine
- dashboard UI
- real trading without validation

---

## Operating Rule

From this point forward, a signal is not good because it has a high score.

A signal is only actionable when:

```text
score + regime + live data + executable trade plan + risk validation + lifecycle management + historical validation
```

all pass together.

Trading decision rule:

```text
No historical validation → no training.
No out-of-sample validation → no adaptive scoring change.
No paper-live observation → no trading decision.
```
