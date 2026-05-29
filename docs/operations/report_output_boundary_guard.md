# Report Output Boundary Guard

The report output boundary guard protects committed public report examples from accidental runtime overwrites.

## Protected public artifacts

The following files are committed synthetic examples only:

```text
reports/premarket-report.md
reports/postmarket-report.md
reports/weekly-report.md
```

Runtime generators must not write live, provider-backed, private or raw report content to these paths.

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

Those locations remain covered by repository hygiene rules and should not be used for committed live or private artifacts.

## CLI examples

Blocked:

```bash
python scripts/generate_report.py --type premarket --output reports/premarket-report.md
python scripts/generate_report.py --type postmarket --output reports/postmarket-report.md
python scripts/generate_report.py --type weekly --output reports/weekly-report.md
```

Allowed:

```bash
python scripts/generate_report.py --type premarket --output reports/generated/premarket-report.md
python scripts/generate_report.py --type postmarket --output reports/generated/postmarket-report.md
python scripts/generate_report.py --type weekly --output reports/generated/weekly-report.md
```

## Test command

```bash
pytest tests/test_report_output_boundary.py -q
pytest tests/test_generate_report_output_boundary.py -q
```

## Boundary rule

This guard is repository hygiene infrastructure only. It does not validate market data, does not prove edge and does not authorize live trading.
