# README Note: Edge Evidence From Polygon Artifact

Use this after the combined Polygon dataset artifact has been created.

Workflow:

```text
Actions -> Edge Evidence From Polygon Artifact -> Run workflow
```

Input:

```text
run_id: the workflow run ID that contains polygon-edge-runtime-dataset-combined
artifact_pattern: polygon-edge-runtime-dataset-combined*
plans_path: data/trade_plans/historical_trade_plans.json
minimum_assets: 500
```

The workflow downloads the combined Polygon artifact, resolves `survivorship_universe.csv` and `historical_bars/`, runs the gated edge-evidence backtest, uploads `reports/edge_evidence/`, and fails closed if evidence gates fail.

Detailed operations guide:

```text
docs/operations/edge_evidence_from_polygon_artifact.md
```
