# Daily Evidence CLI and Artifact Workflow

Phase B8 turns the daily evidence report generator into an operational process.

## CLI

Run the report builder with:

```bash
python scripts/run_daily_evidence_report.py \
  --input-dir reports/daily_evidence_components \
  --output-dir reports/daily_evidence \
  --report-date 2026-05-25
```

The CLI reads component JSON reports and writes:

```text
reports/daily_evidence/daily_evidence_report_YYYY-MM-DD.json
reports/daily_evidence/daily_evidence_report_YYYY-MM-DD.md
```

Exit code behavior:

```text
0 = daily evidence report passed
1 = daily evidence report failed
```

Optional flags:

```text
--allow-missing-risk-attribution
--allow-missing-monte-carlo
--max-failed-components N
```

## Expected Input Files

```text
paper_observation_reconciliation.json
performance_drift_detection.json
sequential_edge_decay.json
regime_change_detection.json
position_risk_attribution.json
monte_carlo_robustness.json
```

## GitHub Actions

Workflow:

```text
.github/workflows/daily-evidence-report.yml
```

It supports:

```text
workflow_dispatch
scheduled weekday run
artifact upload
```

The uploaded artifact is named:

```text
daily-evidence-report-YYYY-MM-DD
```

## Operational Rule

This workflow is for observation-only evidence collection. A green workflow or daily PASS report does not approve live capital. It only confirms that the daily evidence package was generated and passed its configured validation gates.
