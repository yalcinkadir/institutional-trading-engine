# Daily Evidence Input Pipeline

B11.1 adds a fail-closed preflight layer for the Daily Evidence workflow.

## Goal

The Daily Evidence workflow must not produce a green report from missing or malformed inputs. It should fail before B1-B6 component generation when the observation input contract is broken.

## Required input directory

```text
reports/daily_evidence_inputs/
```

## Required files

```text
paper_observation_records.json
backtest_records.json
forward_records.json
regime_records.json
position_records.json
```

Each file must contain a non-empty JSON list.

## Validation CLI

```bash
python scripts/validate_daily_evidence_inputs.py \
  --input-dir reports/daily_evidence_inputs \
  --output-dir reports/daily_evidence_input_validation
```

Exit codes:

```text
0 = input contract valid
1 = input contract invalid
```

## Output artifacts

```text
reports/daily_evidence_input_validation/daily_evidence_input_validation.json
reports/daily_evidence_input_validation/daily_evidence_input_validation.md
```

## Workflow behavior

The Daily Evidence workflow now runs the input validator before component generation.

```text
Validate daily evidence inputs
→ Generate B1-B6 evidence component reports
→ Build daily evidence report
→ Upload validation, component and daily report artifacts
```

If inputs are missing, malformed or schema-invalid, the workflow stops before report generation. This is intentional.

## Operational rule

A green Daily Evidence workflow must mean real daily observation inputs were present and valid. Smoke fixtures and placeholders are not acceptable as operational evidence.

Live capital remains unauthorized until the forward evidence period is complete and all required gates are satisfied.
