# Generated Daily Evidence Components

B10 replaces hand-written placeholder component reports with generated B1-B6 evidence component reports.

## Purpose

The daily evidence report should be built from outputs produced by the validation modules, not from static placeholder JSON.

## CLI

```bash
python scripts/generate_daily_evidence_components.py \
  --input-dir reports/daily_evidence_inputs \
  --output-dir reports/daily_evidence_components \
  --report-date 2026-05-25
```

For deterministic workflow smoke runs before real daily observation inputs exist:

```bash
python scripts/generate_daily_evidence_components.py \
  --output-dir reports/daily_evidence_components \
  --report-date 2026-05-25 \
  --use-smoke-fixture \
  --min-observation-days 1
```

## Expected real input files

Place these files in the input directory:

- `paper_observation_records.json`
- `backtest_records.json`
- `forward_records.json`
- `regime_records.json`
- `position_records.json`

## Generated component files

The CLI writes JSON and Markdown for:

- `paper_observation_reconciliation`
- `performance_drift_detection`
- `sequential_edge_decay`
- `regime_change_detection`
- `position_risk_attribution`
- `monte_carlo_robustness`

## Operational rule

Smoke fixtures are only for workflow plumbing. Real B1.1 evidence must come from actual observation records. Live capital remains unauthorized.
