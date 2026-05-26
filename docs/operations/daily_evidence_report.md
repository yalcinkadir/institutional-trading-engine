# Daily Evidence Report

Phase B7 adds a daily evidence report generator for observation-only evidence review.

The goal is to combine the Phase B evidence components into one daily PASS/FAIL report so that paper observation is not reviewed manually across scattered artifacts.

## Included Components

The report summarizes:

```text
B1 reconciliation
B2 performance drift
B3 sequential edge decay
B4 regime change
B5 position risk attribution
B6 Monte Carlo robustness
```

## Inputs

The generator accepts component report dictionaries or JSON files. Known file names are mapped automatically:

```text
paper_observation_reconciliation.json -> reconciliation
performance_drift_detection.json -> performance_drift
sequential_edge_decay.json -> edge_decay
regime_change_detection.json -> regime_change
position_risk_attribution.json -> risk_attribution
monte_carlo_robustness.json -> monte_carlo
```

## Gates

Default gates:

```text
required_components_present
failed_components <= 0
```

By default all six components are required and any failed component fails the daily report.

## Outputs

The module can write:

```text
daily_evidence_report.json
daily_evidence_report.md
```

## Operational Rule

This report is an evidence-quality dashboard. A pass does not approve live capital. A failure means the daily paper evidence package is incomplete or contains a failed validation component and must be reviewed before escalation.
