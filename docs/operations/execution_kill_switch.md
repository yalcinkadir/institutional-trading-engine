# C7 Execution Kill Switch

Status date: 2026-05-28

C7 adds a fail-closed execution governance layer on top of C5 daily execution reconciliation and C6 fill-quality reporting.

## Purpose

The execution kill switch decides whether downstream paper/execution workflow steps may continue.

It produces one of three states:

```text
ALLOW  -> all required evidence is clean
WATCH  -> degraded but not blocked
BLOCK  -> execution must stop fail-closed
```

It does not:

```text
place live trades
connect to a broker
cancel broker orders
approve live trading
override human risk review
```

It does:

```text
consume C5 daily execution reconciliation reports
consume C6 fill-quality reports
consume manual risk flags
fail closed when required evidence is missing
block on failed reconciliation/fill-quality reports
watch or block on drift/slippage/fill-rate thresholds
write JSON and Markdown decisions
```

## Core Module

```text
src/validation/execution_kill_switch.py
```

Main entry points:

```text
evaluate_execution_kill_switch(...)
load_kill_switch_input(...)
write_execution_kill_switch_decision(...)
render_execution_kill_switch_markdown(...)
```

## CLI

```bash
python scripts/evaluate_execution_kill_switch.py \
  --input-file reports/execution_kill_switch_input/input.json \
  --output-dir reports/execution_kill_switch
```

Input format:

```json
{
  "daily_reconciliation_report": {
    "passed": true,
    "status": "PASS",
    "metrics": {
      "total_r_drift": 0.0,
      "matched_count": 1
    },
    "issues": []
  },
  "fill_quality_report": {
    "passed": true,
    "status": "PASS",
    "metrics": {
      "avg_abs_slippage_bps": 5.0,
      "fill_rate": 1.0
    },
    "issues": []
  },
  "manual_risk_flags": []
}
```

## Default Gates

```text
block_on_failed_daily_reconciliation = true
block_on_failed_fill_quality = true
block_on_manual_risk_flag = true
max_total_r_drift = 0.5
max_avg_abs_slippage_bps = 25.0
max_fill_quality_issue_errors = 0
watch_total_r_drift = 0.25
watch_avg_abs_slippage_bps = 15.0
watch_fill_rate = 0.98
require_daily_reconciliation_report = true
require_fill_quality_report = true
```

## BLOCK Conditions

```text
missing required daily reconciliation report
missing required fill-quality report
failed daily reconciliation report
failed fill-quality report
total R drift above block threshold
average absolute slippage above block threshold
fill-quality error count above maximum
manual risk flag with ERROR severity
```

## WATCH Conditions

```text
daily reconciliation warning state
fill-quality warning state
total R drift above watch threshold
average absolute slippage above watch threshold
fill rate below watch threshold
manual risk flag with WARNING severity
```

## Safety Model

C7 is intentionally conservative:

```text
missing required evidence => BLOCK
failed required evidence => BLOCK
warning evidence => WATCH
clean required evidence => ALLOW
```

The module is a governance/audit layer only. It does not call a broker adapter and does not authorize real-money execution.

## Test Coverage

```text
tests/test_execution_kill_switch.py
```

Covered scenarios:

```text
clean reports allow execution workflow continuation
missing required reports block fail-closed
failed C5 daily reconciliation blocks
failed C6 fill-quality blocks
total R drift block and watch thresholds
average absolute slippage block and watch thresholds
fill-rate watch threshold
manual error and warning risk flags
optional-report mode
JSON input and report output
```
