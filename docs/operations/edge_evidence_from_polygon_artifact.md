# Edge Evidence From Polygon Artifact

## Purpose

Run the gated edge-evidence backtest against a previously consolidated Polygon runtime dataset artifact.

## Required prior step

Create a combined artifact with:

```text
Polygon Artifact Consolidation
```

Expected artifact name:

```text
polygon-edge-runtime-dataset-combined
```

## Run workflow

Open GitHub Actions and start:

```text
Edge Evidence From Polygon Artifact
```

Inputs:

```text
run_id: workflow run ID that contains the combined Polygon artifact
artifact_pattern: polygon-edge-runtime-dataset-combined*
plans_path: data/trade_plans/historical_trade_plans.json
as_of: 2026-05-24
minimum_assets: 500
oos_split_date: 2024-01-01
max_bars_per_plan: 20
```

Use the numeric run ID from the consolidation workflow URL:

```text
/actions/runs/<run_id>
```

## Output

The workflow uploads:

```text
edge-evidence-from-polygon-artifact
```

Report directory:

```text
reports/edge_evidence/
```

Expected summary files:

```text
edge-evidence-summary.json
edge-evidence-summary.md
```

## Fail-closed behavior

The workflow uploads reports even when the backtest gates fail. It then fails the workflow if the edge-evidence script exits with failure.

Common fail reasons:

```text
no_trade_plans_loaded
universe_coverage_below_minimum
survivorship_audit_failed
walk_forward_failed
out_of_sample_lockbox_failed
```

## Tests

```bash
pytest tests/test_edge_evidence_backtest.py -q
pytest tests/test_edge_evidence_from_polygon_artifact_workflow.py -q
```
