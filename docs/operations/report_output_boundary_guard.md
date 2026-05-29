# Report Output Boundary Guard

The Report Output Boundary Guard protects committed public report examples from accidental runtime overwrites.

## Protected public artifacts

The following files are comitted synthetic examples only:

```text
reports/premarket-report.md
reports/postmarket-report.md
reports/weekly-report.md
```

Runtime generators must not write generated report content to these paths.

## Guard implementation

```text
src/report_output_boundary.py
scripts/generate_report.py
tests/test_report_output_boundary.py
tests/test_generate_report_output_boundary.py
```

The guard is fail-closed. If a generator targets a protected public artifact, it raises `ReportOutputBoundaryError` before any write occurs.

## Allowed output locations

Generated reports should be written to non-committed locations, for example:

```text
reports/generated/
reports/live/
reports/private/
outputs/
```

Those locations remain governed by repository hygiene rules.

## Test command

```bash
pytest tests/test_report_output_boundary.py -q
pytest tests/test_generate_report_output_boundary.py -q
```

## Boundary rule

This guard is repository hygiene infrastructure only. It does not validate market data, does not prove edge and does not authorize live trading.
