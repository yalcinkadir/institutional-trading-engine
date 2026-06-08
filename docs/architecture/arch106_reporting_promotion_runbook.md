# ARCH106 Reporting Candidate Promotion Runbook

Status: operational handoff for Issue #106.

## Purpose

Promote the two CI-proven reporting runtime candidates from `unclassified_legacy` to `connected_runtime` without manually editing the generated inventory artifact.

Candidates:

- `src/reporting/cross_asset_report.py`
- `src/reporting/report_formatter.py`

## Preconditions

Before running the promotion workflow, confirm:

1. `ARCH106 Promotion Helper Guard` is green.
2. `ARCH106 Module Inventory Guard` is green.
3. `tests/test_architecture_runtime_execution_guard.py` contains runtime proof markers for both candidates:
   - `cross_asset_called`
   - `format_report_called`

## Manual promotion workflow

Run this workflow manually from GitHub Actions:

```text
Actions -> ARCH106 Promote Reporting Candidates -> Run workflow
```

Workflow file:

```text
.github/workflows/arch106-promote-reporting-candidates.yml
```

The workflow executes:

```bash
python scripts/promote_arch106_reporting_runtime_candidates.py
python scripts/generate_module_inventory.py --check
```

Then it verifies that both promoted modules are classified as `connected_runtime` in `docs/architecture/module_inventory.generated.json`.

If the promotion changes `docs/architecture/module_classification.json` or `docs/architecture/module_inventory.generated.json`, the workflow commits them with:

```text
Promote ARCH106 reporting runtime candidates
```

## Post-run verification

After the workflow completes, verify:

1. A commit named `Promote ARCH106 reporting runtime candidates` exists.
2. `docs/architecture/module_classification.json` contains both candidates under `classified_modules`.
3. `docs/architecture/module_inventory.generated.json` counters reflect:
   - `classified_modules` increased by 2
   - `connected_runtime` increased by 2
   - `unclassified_legacy_modules` decreased by 2
4. The focused ARCH106 workflows remain green.

## Issue #106 closure rule

Do not close #106 solely because these two candidates are promoted.

#106 can only close when the broader legacy module set has been systematically classified, quarantined, marked test-only, or marked delete-candidate according to the ARCH106 acceptance criteria.
