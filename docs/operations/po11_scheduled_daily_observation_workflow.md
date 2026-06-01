# PO11 Scheduled Daily Observation Workflow

Status date: 2026-06-01  
Status: Done / CI-green

## Purpose

PO11 schedules the PO10 Daily Observation Automation Runner through GitHub Actions.

It creates a repeatable daily Paper Observation workflow that runs without live-trading permission, without broker secrets and without repository write access.

## Workflow file

```text
.github/workflows/po11_daily_observation.yml
```

## Test file

```text
tests/test_po11_scheduled_daily_observation_workflow.py
```

## Workflow triggers

```text
schedule
workflow_dispatch
```

Scheduled run:

```text
15 22 * * 1-5
```

This runs Monday to Friday at 22:15 UTC.

Manual dispatch inputs:

```text
observation_date
minimum_records
```

## Workflow behavior

The workflow performs the following steps:

```text
checkout repository
setup Python 3.11
install requirements
run PO10 daily observation automation
write canonical PO10 automation artifact
validate paper-only safety boundary
upload PO11 automation artifact
```

## Artifact output

Uploaded artifact name:

```text
po11-daily-observation-artifact
```

Artifact path:

```text
reports/daily_observation_automation/*.json
```

## Safety boundary

PO11 uses read-only repository permissions:

```text
permissions:
  contents: read
```

PO11 must preserve:

```text
live_trading_authorized: false
broker_execution_mode: paper_only
```

PO11 must not use:

```text
contents: write
broker secrets
live-trading secrets
live broker execution
capital allocation logic
```

## CI guard

PO11 is guarded by:

```bash
pytest tests/test_po11_scheduled_daily_observation_workflow.py -q
```

The guard verifies:

```text
workflow file exists
schedule exists
workflow_dispatch exists
PO10 runner is invoked
artifact upload exists
paper-only boundary is checked
permissions remain read-only
live broker/secrets are not referenced
```

## Operational meaning

A successful PO11 workflow means the daily Paper Observation automation chain produced and uploaded a review artifact.

It does not mean:

```text
live trading is approved
broker execution is approved
production deployment is approved
capital allocation is approved
```

Live trading remains blocked until long-running forward evidence, drift monitoring, regime-change monitoring, execution-quality review, capacity/turnover realism, risk attribution and explicit manual approval exist.
