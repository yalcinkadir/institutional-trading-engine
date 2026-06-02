# CHANGELOG

## ER5 / ER6 / ER11 External Review Remediation — 2026-06-02

### Fixed
- Preserved true `0.0` outcome results in expectancy adjustment instead of falling back to alternate metrics.
- Treated flat `0.0R` expectancy as neutral rather than negative/blocking.
- Excluded missing result records from edge-evidence win/loss/breakeven metrics.
- Surfaced missing result evidence as `missing_result_count`.
- Renamed ambiguous expectancy outputs to explicit `expectancy_r` in the expectancy adjuster and decision-report payloads.

### Added
- Added `tests/test_er5_expectancy_zero_result_guard.py`.
- Added `tests/test_er6_edge_evidence_missing_result_guard.py`.
- Added `tests/test_er11_expectancy_units_guard.py`.
- Added `docs/operations/er5_er6_ci_green_closure_2026_06_02.md`.
- Added `docs/operations/er11_ci_green_closure_2026_06_02.md`.
- Added `docs/operations/er5_er6_er11_documentation_update_2026_06_02.md`.

### Status
- ER5: CLOSED_CI_GREEN.
- ER6: CLOSED_CI_GREEN.
- ER11: CLOSED_CI_GREEN.
- Live trading authorization: unchanged; not granted by code.

---

## TEST1 Evidence-Oriented TDD Policy — 2026-06-01

### Added
- Added `docs/operations/test1_evidence_oriented_tdd_policy.md` as the active project policy for safety-relevant fixes and external review findings.
- Documented the test-first workflow: guard test first, minimal fix second, targeted test, relevant module tests, full suite, documentation last.
- Added README and ROADMAP visibility for TEST1.

### Policy Contract
- A fix is not complete without a guard test.
- A happy-path-only test is not sufficient for safety-critical logic.
- Dangerous paths, boundary cases and fail-closed invariants must be explicitly covered.
- External review findings should receive explicit guard tests.

### Safety Boundary
- TEST1 does not authorize live trading, broker execution, capital allocation or production deployment.

---

## PO13 Monthly Paper Observation Review Pack — 2026-06-01

### Added
- Added `src/operations/monthly_paper_observation_review_pack.py` to build deterministic monthly Paper Observation review packs from the PO12 review index.
- Added `tests/test_po13_monthly_paper_observation_review_pack.py`.
- Added `docs/operations/po13_monthly_paper_observation_review_pack.md`.

### Monthly Review Contract
- Produces `reports/monthly_paper_observation_review/YYYY-MM.json`.
- Produces `REVIEW_READY` or `BLOCKED` monthly review status.
- Preserves `live_trading_authorized=false` and `broker_execution_mode=paper_only`.

### Stabilization Result
- PO13 implementation status: Done / CI-green.
- Live trading authorization: unchanged; not granted by code.

---

## PO12 Daily Observation Artifact Retention & Review Index — 2026-06-01

### Added
- Added `src/operations/daily_observation_artifact_review_index.py`.
- Added `tests/test_po12_daily_observation_artifact_review_index.py`.
- Added `docs/operations/po12_daily_observation_artifact_review_index.md`.

### Stabilization Result
- PO12 implementation status: Done / CI-green.
- Live trading authorization: unchanged; not granted by code.

---

## PO11 Scheduled Daily Observation Workflow — 2026-06-01

### Added
- Added `.github/workflows/po11_daily_observation.yml`.
- Added `tests/test_po11_scheduled_daily_observation_workflow.py`.
- Added `docs/operations/po11_scheduled_daily_observation_workflow.md`.

### Workflow Contract
- Runs Monday to Friday at 22:15 UTC via cron `15 22 * * 1-5`.
- Supports manual dispatch with `observation_date` and `minimum_records`.
- Uploads `po11-daily-observation-artifact`.
- Uses read-only repository permissions.
- Does not authorize live trading.

---

## PO10 Daily Observation Automation Runner — 2026-06-01

### Added
- Added `src/operations/daily_observation_automation_runner.py`.
- Added `tests/test_po10_daily_observation_automation_runner.py`.
- Added `docs/operations/po10_daily_observation_automation_runner.md`.

### Stabilization Result
- PO10 implementation status: Done / CI-green.
- Live trading authorization: unchanged; not granted by code.

---

## PO9 Paper Observation Review Gate — 2026-06-01

### Added
- Added `src/operations/paper_observation_review_gate.py`.
- Added `tests/test_po9_paper_observation_review_gate.py`.
- Added `docs/operations/po9_paper_observation_review_gate.md`.

### Stabilization Result
- PO9 implementation status: Done / CI-green.
- Live trading authorization: unchanged; not granted by code.

---

## PO8 Daily Observation Review Summary — 2026-06-01

### Added
- Added `src/operations/daily_observation_review_summary.py`.
- Added `tests/test_po8_daily_observation_review_summary.py`.
- Added `docs/operations/po8_daily_observation_review_summary.md`.

### Stabilization Result
- PO8 implementation status: Done / CI-green.
- Live trading authorization: unchanged; not granted by code.

---

## PO7 Daily Observation Record Index — 2026-06-01

### Added
- Added `src/operations/daily_observation_record_index.py`.
- Added `tests/test_po7_daily_observation_record_index.py`.
- Added `docs/operations/po7_daily_observation_record_index.md`.

### Stabilization Result
- PO7 implementation status: Done / CI-green.
- Live trading authorization: unchanged; not granted by code.

---

## PO6 Daily Observation Record Artifact Contract — 2026-06-01

### Added
- Added `src/operations/daily_observation_record_artifact_contract.py`.
- Added `tests/test_po6_artifact_contract.py`.
- Added `docs/operations/po6_daily_observation_record_artifact_contract.md`.

### Stabilization Result
- PO6 implementation status: Done / CI-green.
- Live trading authorization: unchanged; not granted by code.

---

## PO5 Daily Observation Record Writer — 2026-06-01

### Added
- Added `src/operations/daily_observation_record_writer.py`.
- Added `tests/test_po5_daily_observation_record_writer.py`.
- Added PO5 documentation.

### Stabilization Result
- PO5 implementation status: Done / CI-green.
- Live trading authorization: unchanged; not granted by code.

---

## PO4 Daily Observation Record Validator — 2026-06-01

### Added
- Added `src/operations/daily_observation_record_validator.py`.
- Added `tests/test_po4_daily_observation_record_validator.py`.
- Added PO4 documentation.

### Stabilization Result
- PO4 implementation status: Done / CI-green.
- Live trading authorization: unchanged; not granted by code.

---

## PO3 Daily Observation Run Record — 2026-06-01

### Added
- Added `docs/operations/po3_daily_observation_run_record.md`.
- Added `tests/test_po3_daily_observation_run_record.py`.

### Stabilization Result
- PO3 implementation status: Done / CI-green.
- Live trading authorization: unchanged; not granted by code.

---

## PO2 Daily Observation Acceptance Gate — 2026-06-01

### Added
- Added `docs/operations/po2_daily_observation_acceptance_gate.md`.
- Added `tests/test_po2_daily_observation_acceptance_gate.py`.

### Stabilization Result
- PO2 implementation status: Done / CI-green.
- Live trading authorization: unchanged; not granted by code.

---

## PO1 Paper Observation Timeline — 2026-06-01

### Added
- Added `docs/operations/po1_paper_observation_timeline.md`.
- Added `tests/test_po1_paper_observation_timeline.py`.

### Paper Observation Timeline
- Start date: 2026-06-01.
- Minimum duration: 3 months.
- Target duration: 3-6 months.
- First review date: 2026-07-01.
- Major evidence review date: 2026-09-01.
- Extended review date: 2026-12-01.

### Stabilization Result
- PO1 implementation status: Done / CI-green.
- Live trading authorization: unchanged; not granted by code.

---

## IP9/IP10 Public Repository Governance — 2026-06-01

### Added
- Added public-edge pull request review governance for newly introduced edge constants.
- Added license and usage disclaimer documentation for the public decision-support research framework.
- Added `docs/operations/ip9_ip10_public_repo_governance.md`.
- Added `tests/test_ip9_ip10_public_repo_governance.py`.

### Stabilization Result
- IP9/IP10 implementation status: Done / CI-wired.
- Live trading authorization: unchanged; not granted by code.
