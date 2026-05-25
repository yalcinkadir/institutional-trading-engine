# Runtime Active Universe Mode

## Purpose

`runtime_active_universe` is an exploratory audit mode for the Polygon artifact workflow.

It is intended for this dataset shape:

```text
current active Polygon universe
historical Polygon bars
generated historical trade plans
```

## Why this mode exists

The current Polygon runtime universe can contain broad active ticker coverage, but it is not a final point-in-time lifecycle dataset.

For final lifecycle-safe evidence, use:

```text
strict
```

For exploratory runtime evidence from the combined Polygon artifact, use:

```text
runtime_active_universe
```

## Behavior

```text
strict:
  validates every trade plan against ticker active_from / active_to

runtime_active_universe:
  validates that trade-plan symbols exist in the downloaded runtime universe
  allows generated historical plans to continue to walk-forward and OOS gates
```

The summary report includes the selected mode:

```text
survivorship_mode
```

## Report outputs

When the universe, plan and survivorship gates allow the backtest to continue, the edge-evidence pipeline writes:

```text
reports/edge_evidence/historical-entry-exit-backtest.json
reports/edge_evidence/historical-entry-exit-backtest.md
reports/edge_evidence/walk-forward-validation.json
reports/edge_evidence/walk-forward-validation.md
reports/edge_evidence/out-of-sample-lockbox.json
reports/edge_evidence/out-of-sample-lockbox.md
reports/edge_evidence/edge-evidence-summary.json
reports/edge_evidence/edge-evidence-summary.md
```

The historical report writer import is covered by:

```bash
pytest tests/test_edge_evidence_backtest.py -q
```

## Workflow default

The Polygon artifact workflow defaults to:

```text
survivorship_mode: runtime_active_universe
```

## CLI usage

```bash
python scripts/run_edge_evidence_backtest.py \
  --universe data/universe/survivorship_universe.csv \
  --plans data/trade_plans/historical_trade_plans.json \
  --bars-root data/historical_bars \
  --survivorship-mode runtime_active_universe
```

## Test command

```bash
pytest tests/test_edge_evidence_backtest.py -q
pytest tests/test_edge_evidence_from_polygon_artifact_workflow.py -q
```