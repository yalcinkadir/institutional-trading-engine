# Historical Trade Plan Generation

## Purpose

Generate historical `BUY_WATCH` trade plans for backtesting while keeping a hard boundary between baseline/demo testing and real strategy-evidence claims.

This document now defines three different paths:

1. baseline/demo historical plan generation from OHLCV bars
2. validated Paper Observation export for research/audit continuity
3. #177 scanner-coupled real-data plan export through the active Scanner → Signal Generator → Quality Engines → Trade Plan Validator path

Only the third path is acceptable for real-data strategy evidence.

## Evidence boundary

### 1. Baseline / demo historical plan generation

Uses:

```text
scripts/generate_historical_trade_plans.py
```

Status:

```text
research_only / baseline / not pipeline-coupled
```

This path can support operational stability, fill-model smoke tests and deterministic regression tests, but it is **not** real strategy evidence.

It must **not** be used to claim that the live Scanner → Signal Generator → Quality/Fusion → Trade Plan Validator pipeline has been validated.

### 2. Validated Paper Observation export

Uses:

```text
scripts/export_historical_trade_plans.py
```

Input shape:

```text
observations[] / signals[] / records[]
```

Status:

```text
research_only / paper-observation continuity / not accepted as real-data strategy evidence by BT9
```

This path may export already validated Paper Observation records when they contain non-demo provenance and runtime-gate annotations. It exists to preserve audit continuity and to support research-only replay checks.

Important #177 rule:

```text
validated_paper_observation_export != scanner_signal_quality_validator
```

A validated observation export must not be promoted into real-data strategy evidence merely because records contain `pipeline_coupled: true` or `runtime_gates_applied` metadata. The BT9 real historical input pack gate rejects this path for real-data strategy evidence.

### 3. Pipeline-coupled real-data evidence

Uses:

```text
scripts/export_historical_trade_plans.py
```

The exporter accepts a #177 pipeline payload containing:

```text
decision_report
scanner_metrics_map / scanner_metrics
market_regime
```

For #177 payloads, the exporter calls:

```text
src.signals.signal_generator.build_signals()
```

That means historical trade plans are not created by a separate simplified generator. They are derived through:

```text
Scanner metrics
  -> Signal Generator
  -> Entry Quality
  -> Stop-Loss Quality
  -> Exit Target Quality
  -> Trade Plan Validator
  -> Historical Trade Plan Export
```

A pipeline-coupled export must include:

```text
pipeline_coupled: true
pipeline_generation_source: scanner_signal_quality_validator
runtime_gates_applied:
  - scanner
  - signal_generator
  - quality_fusion
  - trade_plan_validator
generated_signal_count
validated_trade_plan_count
blocked_signal_count
```

If scanner fields, ATR, source provenance, data status, entry/stop/target validation, or demo-provenance checks fail, the exporter writes a manifest with failures and does not write a trade-plan output file.

## Input

### Baseline input

A directory of daily bar CSV files:

```text
data/historical_bars/*.csv
```

Required CSV columns:

```text
date,open,high,low,close,volume
```

### #177 pipeline input

A JSON file with this shape:

```json
{
  "market_regime": "Bullish",
  "decision_report": {
    "decisions": [
      {
        "symbol": "SPY",
        "decision": "approved",
        "setup_type": "momentum_breakout",
        "risk_tier": "tier_1",
        "position_size_multiplier": 1.0,
        "setup_score": 82.0,
        "regime_alignment": 0.9,
        "score_source": "scanner_runtime",
        "data_source": "polygon",
        "thresholds_version": "v1_real_runtime"
      }
    ]
  },
  "scanner_metrics_map": {
    "SPY": {
      "close": 100.0,
      "high": 100.5,
      "low": 98.5,
      "atr14": 1.0,
      "rvol": 1.2,
      "vwap": 99.5,
      "swing_low_3bar": 99.0,
      "data_status": "OK",
      "source": "polygon",
      "source_timestamp": "2026-06-01T21:00:00Z",
      "fallback_level": "none"
    }
  }
}
```

## Output

```text
data/trade_plans/historical_trade_plans.json
```

The JSON contains:

```text
metadata
plans[]
```

For pipeline-coupled real-data evidence, metadata must include:

```text
pipeline_coupled
pipeline_generation_source
generated_signal_count
validated_trade_plan_count
blocked_signal_count
runtime_gates_applied
```

Each plan includes:

```text
signal_id
symbol
signal_date
entry_trigger
stop_loss
target_1
target_2
valid_until
entry_type
setup_type
stop_model
exit_model
provenance
```

## Local baseline command

```bash
python scripts/generate_historical_trade_plans.py \
  --bars-root data/historical_bars \
  --output data/trade_plans/historical_trade_plans.json \
  --max-plans 5000 \
  --max-plans-per-symbol 3 \
  --min-history 60 \
  --lookahead-days 20
```

Use this command for deterministic baseline testing only.

## Research-only Paper Observation export command

```bash
python scripts/export_historical_trade_plans.py \
  --source reports/paper_observation/validated_observations.json \
  --output data/trade_plans/historical_trade_plans.json \
  --manifest data/trade_plans/historical_trade_plans_manifest.json
```

The source observations must be validated, non-demo, and runtime-gate annotated. Missing runtime-gate proof fails export rather than producing ambiguous evidence. Even when this export succeeds, BT9 must not accept it as real-data strategy evidence because it is not generated from the canonical `scanner_signal_quality_validator` adapter.

## Pipeline-coupled export command

```bash
python scripts/export_historical_trade_plans.py \
  --source reports/backtests/scanner_signal_quality_validator_input.json \
  --output data/trade_plans/historical_trade_plans.json \
  --manifest data/trade_plans/historical_trade_plans_manifest.json
```

This is the canonical adapter for real-data backtest coupling. It executes `build_signals()` and exports only validated `BUY_WATCH` signals.

## BT9 real-data gate rule

The BT9 real historical input pack gate accepts real-data strategy evidence only when trade-plan metadata satisfies all of the following:

```text
pipeline_coupled == true
pipeline_generation_source == scanner_signal_quality_validator
runtime_gates_applied includes scanner, signal_generator, quality_fusion, trade_plan_validator
validated_trade_plan_count > 0
```

Lists without metadata, baseline generator output, and validated Paper Observation exports are blocked from real-data strategy-evidence claims.

## Workflow integration

The workflow below may still use the deterministic generator for baseline edge-evidence experiments:

```text
Edge Evidence From Polygon Artifact
```

The workflow below must use a #177 pipeline payload for real-data strategy evidence:

```text
BT131 Real Data Backtest Evidence
```

BT131 behavior:

```text
#177 pipeline payload present and valid -> export scanner_signal_quality_validator plans -> run BT9 -> run backtest
#177 pipeline payload missing            -> write BLOCKED_MISSING_PIPELINE_PAYLOAD artifact
#177 pipeline payload invalid            -> export fails -> downstream evidence remains BLOCKED
```

This keeps backtesting operationally stable while preventing false strategy-evidence claims.

## Strategy rule for baseline generator

The baseline generator uses a simple deterministic pullback-continuation rule:

```text
close > SMA50
recent 10-day low touches/pulls below SMA20
minimum dollar volume passes
entry = close * 1.01
risk = max(ATR14 * 1.25, close * 0.02)
stop = entry - risk
target_1 = entry + 2R
target_2 = entry + 3R
```

This rule is deterministic and reproducible. It is not a claim that the runtime strategy stack has been validated.

## Guard tests

The current guard coverage lives in:

```text
tests/test_htp1_historical_trade_plan_export.py
tests/test_bt131_real_data_backtest_evidence_workflow.py
tests/test_bt130_real_historical_backtest_evidence_pack.py
```

Required #177 guard behavior:

```text
non-pipeline trade plans cannot be used for real-data evidence
fixture-declared pipeline metadata from observation exports is rejected by BT9
missing runtime gates fail closed
missing ATR/source/provenance fails closed
pipeline-coupled export remains BT9-compatible
```

## Current boundary

This system still does not authorize live trading.

All generated backtest evidence remains:

```text
research_only
paper_only
not investment advice
live_trading_authorized: false
```
