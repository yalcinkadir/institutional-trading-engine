# Static Dashboard HTML Reporting

P35 builds a static dashboard from existing local report files.

The dashboard is static reporting only. It does not connect to brokers and does not execute orders.

## Files

```text
src/operations/static_dashboard.py
scripts/build_static_dashboard.py
tests/test_static_dashboard.py
.github/workflows/static-dashboard.yml
```

## Outputs

```text
reports/dashboard/index.html
reports/dashboard/dashboard.json
```

## Default Inputs

```text
reports/signals/latest-signals.json
data/portfolio_state.json
reports/paper-live/paper-live-observation.json
reports/operations/operational-readiness-review.json
reports/operations/scheduled-decision-support-dry-run.json
reports/portfolio/manual-portfolio-sync.json
reports/archive/latest/manifest.json
```

Missing files do not fail the dashboard build. They are shown as missing inputs.

## Status Values

```text
PASS     all configured inputs are available
PARTIAL  at least one input is missing
WARN     at least one input has invalid JSON
EMPTY    all configured inputs are missing
```

## Local Command

```bash
python scripts/build_static_dashboard.py \
  --output-html reports/dashboard/index.html \
  --output-json reports/dashboard/dashboard.json \
  --json
```

## Tests

```bash
pytest tests/test_static_dashboard.py
```

## GitHub Actions

```text
Actions → Static Dashboard → Run workflow
```

Artifact:

```text
static-dashboard-artifacts
```

## Boundary

P35 is a reporting layer only. It reads existing local files and writes static HTML/JSON output.
