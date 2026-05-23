# Report Archive

P29 adds persistent local archive support for important validation and operations reports.

It copies selected report files into a timestamped archive folder and writes a JSON/Markdown manifest.

It does not use external storage yet.

---

## Local Command

```bash
python scripts/archive_reports.py
```

With explicit archive id:

```bash
python scripts/archive_reports.py \
  --archive-root reports/archive \
  --archive-id manual-review-001
```

With selected files:

```bash
python scripts/archive_reports.py \
  --report-paths reports/readiness/operational-readiness-review.json,reports/scheduled-runs/scheduled-decision-support-dry-run.json
```

---

## Default Files

The default archive chain includes:

```text
reports/backtests/historical-entry-exit-backtest.json
reports/backtests/historical-entry-exit-backtest.md
reports/backtests/out-of-sample-validation.json
reports/backtests/out-of-sample-validation.md
reports/paper-live/paper-live-observation.json
reports/paper-live/paper-live-observation.md
reports/readiness/operational-readiness-review.json
reports/readiness/operational-readiness-review.md
reports/scheduled-runs/scheduled-decision-support-dry-run.json
reports/scheduled-runs/scheduled-decision-support-dry-run.md
data/portfolio_state.json
```

Missing files are not fatal. They are recorded in the manifest.

---

## Output

Example:

```text
reports/archive/archive-20260523T204500Z/
  manifest.json
  manifest.md
  reports/backtests/...
  reports/paper-live/...
  reports/readiness/...
  reports/scheduled-runs/...
  data/portfolio_state.json
```

---

## GitHub Actions Workflow

```text
Actions → Archive Reports → Run workflow
```

Inputs:

```text
archive_id: optional
archive_root: reports/archive
report_paths: optional comma-separated paths
```

Artifact:

```text
report-archive-artifacts
```

---

## Manifest Fields

```text
archive_id
generated_at_utc
archive_dir
copied_files
missing_files
notes
```

---

## Interpretation

The archive is useful for review and audit history.

```text
copied_files
```

shows what was persisted into the archive folder.

```text
missing_files
```

shows which expected reports were not available in the workflow workspace.

---

## Guardrail

```text
No external storage integration yet.
No broker call.
No order execution.
No trading authorization.
No database persistence.
```

---

## Next Step

Later versions may add:

```text
S3 / R2 / Supabase Storage
Postgres report index
static HTML dashboard
long-term analytics history
```
