# Polygon Artifact Consolidation

## Run

Open GitHub Actions and start:

```text
Polygon Artifact Consolidation
```

Required input:

```text
run_ids
```

Use the workflow run IDs from completed Polygon batch runs. The value can be comma, space or newline separated.

Example:

```text
26374949328, 26375000000, 26375100000
```

Optional inputs:

```text
artifact_pattern: polygon-edge-runtime-dataset*
output_name: polygon-edge-runtime-dataset-combined
minimum_bar_files: 500
```

## Output

The workflow uploads a combined artifact:

```text
polygon-edge-runtime-dataset-combined
```

It also writes:

```text
reports/edge_evidence_data/combined-polygon-bars-manifest.md
```

## Local command

```bash
python scripts/consolidate_polygon_artifacts.py \
  --artifacts-root runtime_artifacts/polygon_batches \
  --output-root runtime_artifacts/polygon_combined \
  --combined-manifest reports/edge_evidence_data/combined-polygon-bars-manifest.md
```

## Tests

```bash
pytest tests/test_consolidate_polygon_artifacts.py -q
pytest tests/test_polygon_artifact_consolidation_workflow.py -q
```
