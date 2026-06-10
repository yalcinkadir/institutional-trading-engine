# Historical Trade Plan Generation

## Purpose

Generate deterministic historical `BUY_WATCH` trade plans from daily OHLCV bars.

This generator is a **research/demo baseline utility**, not the canonical real-data strategy-evidence path.

It remains useful for:

- simulator smoke tests
- fill-model regression tests
- deterministic local experimentation
- public-safe examples where no strategy-evidence claim is made

It must **not** be used to claim that the live Scanner → Signal Generator → Quality/Fusion → Trade Plan Validator pipeline has been validated.

## Evidence boundary

There are now two distinct paths:

### 1. Baseline / demo historical plan generation

Uses:

```text
scripts/generate_historical_trade_plans.py
```

Status:

```text
research_only / baseline / not pipeline-coupled
```

This path can support operational stability and regression testing, but it is **not** real strategy evidence.

### 2. Pipeline-coupled real-data evidence

Uses:

```text
scripts/export_historical_trade_plans.py
```

with validated Paper Observation records that already prove:

```text
pipeline_coupled: true
runtime_gates_applied:
  - scanner
  - signal_generator
  - quality_fusion
  - trade_plan_validator
```

Only this path may produce trade-plan files for BT131 real-data evidence.

If validated observations are missing, BT131 should remain operationally stable by writing a reviewable `BLOCKED` artifact, not by silently falling back to this deterministic generator.

## Input

A directory of daily bar CSV files:

```text
data/historical_bars/*.csv
```

Required CSV columns:

```text
date,open,high,low,close,volume
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

For baseline generation, metadata describes the generator summary. For pipeline-coupled real-data evidence, metadata must include:

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
action
entry_trigger
stop_loss
target_1
target_2
valid_until
entry_type
setup_type
stop_model
exit_model
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

## Pipeline-coupled export command

```bash
python scripts/export_historical_trade_plans.py \
  --source reports/paper_observation/validated_observations.json \
  --output data/trade_plans/historical_trade_plans.json \
  --manifest data/trade_plans/historical_trade_plans_manifest.json
```

The source observations must be validated, non-demo, and runtime-gate annotated. Missing runtime-gate proof should fail export rather than producing ambiguous evidence.

## Workflow integration

The workflow below may still use the deterministic generator for baseline edge-evidence experiments:

```text
Edge Evidence From Polygon Artifact
```

The workflow below must use validated observations for real-data strategy evidence:

```text
BT131 Real Data Backtest Evidence
```

BT131 behavior:

```text
source_observations present and valid -> export pipeline-coupled plans -> run BT9 -> run backtest
source_observations missing          -> write BLOCKED_MISSING_VALIDATED_OBSERVATIONS artifact
source_observations invalid          -> export fails -> downstream evidence remains BLOCKED
```

This keeps Backtesting operationally stable while preventing false strategy-evidence claims.

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

This is a testable baseline, not a claim of edge.

## Tests

```bash
pytest tests/test_generate_historical_trade_plans.py -q
pytest tests/test_htp1_historical_trade_plan_export.py -q
pytest tests/test_edge_evidence_from_polygon_artifact_workflow.py -q
pytest tests/test_bt131_real_data_backtest_evidence_workflow.py -q
```
