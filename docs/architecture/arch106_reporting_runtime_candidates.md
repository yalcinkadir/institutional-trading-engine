# ARCH106 Reporting Runtime Classification Candidates

Status: candidate evidence only. This document does not replace `module_classification.json` or `module_inventory.generated.json`.

## Principle

Reachability is necessary but not sufficient.

A module may be promoted from `unclassified_legacy` to `connected_runtime` only when both conditions are true:

1. The module is reachable from a real runtime entry point.
2. The relevant runtime path is exercised by an explicit runtime-execution proof.

## Current runtime entry point

- `scripts/generate_report.py`

## Candidate: `src/reporting/cross_asset_report.py`

Proposed classification: `connected_runtime`

Evidence:

- Runtime entry point imports `build_cross_asset_report` from `src.reporting.cross_asset_report`.
- Market report payload executes `build_cross_asset_report()` inside `_build_market_payload(...)`.
- ARCH106 runtime proof now records `cross_asset_called` in `tests/test_architecture_runtime_execution_guard.py`.
- Runtime-order assertion verifies `cross_asset_called` occurs before `scanner_metrics_normalized`.

Required follow-up before promotion:

- Add this module to `docs/architecture/module_classification.json`.
- Regenerate or update `docs/architecture/module_inventory.generated.json` consistently.
- Verify `python scripts/generate_module_inventory.py --check` passes in CI.

## Candidate: `src/reporting/report_formatter.py`

Proposed classification: `connected_runtime`

Evidence:

- Runtime entry point imports `format_report` from `src.reporting.report_formatter`.
- `build_report(...)` returns `format_report(payload)` for market reports.
- ARCH106 runtime proof now records `format_report_called` in `tests/test_architecture_runtime_execution_guard.py`.
- Runtime-order assertion verifies `signals_built` occurs before `format_report_called` and `format_report_called` before `signals_saved`.
- The patched proof validates that the formatter receives a payload containing `report_type`, `cross_asset`, and `decision_report` data.

Required follow-up before promotion:

- Add this module to `docs/architecture/module_classification.json`.
- Regenerate or update `docs/architecture/module_inventory.generated.json` consistently.
- Verify `python scripts/generate_module_inventory.py --check` passes in CI.

## Not promoted yet

These modules remain unclassified until their runtime role is proven or they are explicitly marked as non-runtime/test-only/quarantine/delete-candidate:

- `src/reporting/report_quality.py`
- `src/reporting/tg2_tg3_report_templates.py`
- `src/reporting/trade_summary.py`
- `src/reporting/weekly_summary.py`
- `src/reporting/cross_asset_report.py`
- `src/reporting/report_formatter.py`

The last two are classification-ready candidates, but they should only be promoted together with a consistent inventory artifact update.
