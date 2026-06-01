# PO1 Paper Observation Timeline and Review Gate

Status date: 2026-06-01
Status: implemented / CI-wired

## Purpose

PO1 formalizes the Paper Observation period as an evidence process. It defines the start date, minimum observation duration, target duration, review milestones and live-trading block.

This is an operational evidence gate, not a live-trading authorization.

## Timeline

```text
Paper Observation start date: 2026-06-01
Minimum duration: 3 months
Target duration: 3-6 months
First review date: 2026-07-01
Major evidence review date: 2026-09-01
Target extended review date: 2026-12-01
```

## Review gates

```text
30-day review: verify daily evidence completeness, missing-data incidents, drift flags, fill-quality evidence and report generation health.
90-day review: verify forward paper evidence quality, drawdown behavior, capacity/turnover realism, execution-quality evidence, risk attribution and regime/drift behavior.
3-6 month observation window: continue evidence collection until evidence is stable enough for a manual research review.
```

## Required evidence families

```text
- Daily Evidence reports
- Runtime Evidence manifests
- Drift and regime evidence
- Fill-quality evidence
- Backtesting Evidence reports
- Capacity / turnover realism evidence
- Runtime governance proof status
- Manual review notes
```

## Hard block

```text
Live trading authorization: not granted by code
Broker execution: paper-only infrastructure
Real-money execution: blocked until manual approval after sufficient forward evidence
```

## Acceptance rule

A Paper Observation day is not accepted as evidence unless required reports and manifests are present, generated successfully and remain research/paper-only.

## Test command

```bash
pytest tests/test_po1_paper_observation_timeline.py -q
```
