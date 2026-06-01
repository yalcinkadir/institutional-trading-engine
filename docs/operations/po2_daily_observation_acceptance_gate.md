# PO2 Daily Observation Acceptance Gate

Status date: 2026-06-01
Status: Done / CI-green

## Purpose

PO2 defines when a Paper Observation day is accepted as valid evidence. The goal is to prevent incomplete, missing, non-reproducible or execution-implying daily artifacts from being treated as usable forward evidence.

This gate is research / paper-observation only. It does not authorize live trading.

## Daily acceptance rule

A Paper Observation day is accepted only when every required evidence family is present, generated successfully, internally consistent and explicitly research-only.

```text
accepted_day = required_evidence_present
             AND reports_generated_successfully
             AND manifests_reference_required_artifacts
             AND no_live_trading_authorization
             AND no_real_money_execution
             AND manual_notes_present_when_incidents_exist
```

## Required evidence families

```text
- Daily Evidence report
- Runtime Evidence manifest
- Drift and regime evidence
- Fill-quality evidence when paper fills exist
- Backtesting Evidence reference when strategy/backtest comparison is used
- Capacity / turnover realism reference when sizing or turnover is discussed
- Runtime governance status
- Incident notes when missing data, provider degradation or runtime anomalies occur
```

## Rejection reasons

A day is rejected as evidence if any of the following are true:

```text
- required report missing
- required manifest missing
- report generation failed
- artifact hash/reference mismatch
- missing data is not documented
- provider degradation is not documented
- drift/regime event is not documented
- fill-quality evidence is missing for paper fills
- live trading is implied or authorized
- real-money execution is implied or authorized
```

## Output status vocabulary

```text
ACCEPTED
REJECTED
NEEDS_REVIEW
```

`NEEDS_REVIEW` is used for days that have all core artifacts but contain incidents requiring manual review before they can be promoted to accepted evidence.

## CI result

```text
PO2 Daily Observation Acceptance Gate: Done / CI-green
```

## Test command

```bash
pytest tests/test_po2_daily_observation_acceptance_gate.py -q
```
