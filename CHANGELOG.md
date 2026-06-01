# CHANGELOG

## PO11 Scheduled Daily Observation Workflow — 2026-06-01

### Added
- Added `.github/workflows/po11_daily_observation.yml` to schedule PO10 Daily Observation Automation through GitHub Actions.
- Added `tests/test_po11_scheduled_daily_observation_workflow.py` to guard schedule configuration, workflow dispatch inputs, PO10 invocation, artifact upload, read-only permissions and paper-only safety boundaries.
- Added `docs/operations/po11_scheduled_daily_observation_workflow.md` to document PO11 and CI-green status.

### Workflow Contract
- Runs Monday to Friday at 22:15 UTC via cron `15 22 * * 1-5`.
- Supports manual `workflow_dispatch` with `observation_date` and `minimum_records` inputs.
- Runs PO10 Daily Observation Automation Runner.
- Uploads `po11-daily-observation-artifact` from `reports/daily_observation_automation/*.json`.
- Uses read-only repository permissions with `contents: read`.
- Preserves the paper-only boundary with `live_trading_authorized=false` and `broker_execution_mode=paper_only`.

### Stabilization Result
- PO11 implementation status: Done / CI-green.
- CI status: green; guarded by `tests/test_po11_scheduled_daily_observation_workflow.py`.
- Live trading authorization: unchanged; not granted by code.

---

## PO10 Daily Observation Automation Runner — 2026-06-01

### Added
- Added `src/operations/daily_observation_automation_runner.py` to connect PO5 Daily Observation Record creation, PO7 indexing, PO8 review summary generation and PO9 review-gate evaluation into one deterministic daily automation artifact.
- Added `tests/test_po10_daily_observation_automation_runner.py` to guard passed/blocked automation status, minimum-record blocking, rejected/needs-review observation days, existing-record inclusion, duplicate-date error surfacing and canonical artifact writing.
- Added `docs/operations/po10_daily_observation_automation_runner.md` to document PO10 and CI-green status.

### Automation Contract
- Produces canonical daily automation artifacts under `reports/daily_observation_automation/YYYY-MM-DD.json`.
- Produces `PASSED` or `BLOCKED` automation status.
- Includes the generated observation record path, PO7 index path, PO8 summary, PO9 gate output and deterministic errors.
- Preserves the paper-only boundary with `live_trading_authorized=false` and `broker_execution_mode=paper_only`.

### Stabilization Result
- PO10 implementation status: Done / CI-green.
- CI status: green; guarded by `tests/test_po10_daily_observation_automation_runner.py`.
- Live trading authorization: unchanged; not granted by code.

---

## PO9 Paper Observation Review Gate — 2026-06-01

### Added
- Added `src/operations/paper_observation_review_gate.py` to evaluate PO8 review summaries as a deterministic Paper Observation review gate.
- Added `tests/test_po9_paper_observation_review_gate.py` to guard passed/blocked gate status, minimum-record enforcement, rejected/needs-review blockers and paper-only boundary enforcement.
- Added `docs/operations/po9_paper_observation_review_gate.md` to document PO9 and CI-green status.

### Review Gate Contract
- Produces `PASSED` or `BLOCKED`.
- Requires `review_ready=true`, sufficient observation records, all records accepted, no rejected days, no needs-review days and no manual-review dates.
- Preserves the paper-only boundary with `live_trading_authorized=false` and `broker_execution_mode=paper_only`.

### Stabilization Result
- PO9 implementation status: Done / CI-green.
- CI status: green; guarded by `tests/test_po9_paper_observation_review_gate.py`.
- Live trading authorization: unchanged; not granted by code.

---

## PO8 Daily Observation Review Summary — 2026-06-01

### Added
- Added `src/operations/daily_observation_review_summary.py` to build a deterministic review summary from the PO7 Daily Observation Record Index.
- Added `tests/test_po8_daily_observation_review_summary.py` to guard review-ready state, rejected/needs-review date extraction, count consistency and paper-only boundary enforcement.
- Added `docs/operations/po8_daily_observation_review_summary.md` to document PO8 and CI-green status.

### Review Summary Contract
- Includes `total_records`, `accepted_count`, `rejected_count`, `needs_review_count`, `review_required_dates`, `rejected_dates`, `needs_review_dates` and `review_ready`.
- `review_ready` requires at least one record, zero rejected records, zero needs-review records, no review-required records and no consistency errors.
- Preserves the paper-only boundary with `live_trading_authorized=false` and `broker_execution_mode=paper_only`.

### Stabilization Result
- PO8 implementation status: Done / CI-green.
- CI status: green.
- Live trading authorization: unchanged; not granted by code.

---

## PO7 Daily Observation Record Index — 2026-06-01

### Added
- Added `src/operations/daily_observation_record_index.py` to build a deterministic index for PO3/PO5 daily observation records.
- Added `tests/test_po7_daily_observation_record_index.py` to guard sorting, status counts, duplicate-date rejection, invalid-record rejection, canonical writing and fail-closed output-path handling.
- Added `docs/operations/po7_daily_observation_record_index.md` to document PO7 and CI-green status.

### Index Contract
- Canonical index path: `reports/daily_observation_records/index.json`.
- Includes `total_records`, `status_counts` and one record entry per observation day.
- Preserves the paper-only boundary with `live_trading_authorized=false` and `broker_execution_mode=paper_only`.

### Stabilization Result
- PO7 implementation status: Done / CI-green.
- CI status: green.
- Live trading authorization: unchanged; not granted by code.

---

## PO6 Daily Observation Record Artifact Contract — 2026-06-01

### Added
- Added `src/operations/daily_observation_record_artifact_contract.py` to define the canonical artifact path contract for PO3/PO5 daily observation records.
- Added `tests/test_po6_artifact_contract.py` to guard the canonical daily observation record path.
- Added `docs/operations/po6_daily_observation_record_artifact_contract.md` to document PO6 and CI-green status.

### Artifact Contract
- Canonical root: `reports/daily_observation_records/`.
- Canonical filename: `YYYY-MM-DD.json`.
- Example: `reports/daily_observation_records/2026-06-01.json`.

### Stabilization Result
- PO6 implementation status: Done / CI-green.
- CI status: green.
- Live trading authorization: unchanged; not granted by code.

---

## PO5 Daily Observation Record Writer — 2026-06-01

### Added
- Added `src/operations/daily_observation_record_writer.py` to generate PO3 Daily Observation Run Records.
- Added `tests/test_po5_daily_observation_record_writer.py` to guard status mapping, JSON writing, PO4 validation integration and fail-closed behavior for invalid records.
- Added `docs/operations/po5_daily_observation_record_writer.md` to document PO5 and CI-green status.

### Writer Rules
- Clean day maps to ACCEPTED.
- Missing evidence maps to REJECTED.
- Incidents map to NEEDS_REVIEW.
- live_trading_authorized is always false.
- broker_execution_mode is always paper_only.
- Invalid records are not written.

### Stabilization Result
- PO5 implementation status: Done / CI-green.
- CI status: green.
- Live trading authorization: unchanged; not granted by code.

---

## PO4 Daily Observation Record Validator — 2026-06-01

### Added
- Added `src/operations/daily_observation_record_validator.py` to validate PO3 daily observation run records.
- Added `tests/test_po4_daily_observation_record_validator.py` to guard required fields, status consistency, ISO date handling, list typing and the paper-only safety boundary.
- Added `docs/operations/po4_daily_observation_record_validator.md` to document the PO4 validator and CI-green status.

### Validation Rules
- Required fields must be present.
- Status must be ACCEPTED, REJECTED or NEEDS_REVIEW.
- ACCEPTED records cannot contain missing evidence or unresolved incidents.
- REJECTED records require missing evidence.
- NEEDS_REVIEW records require incidents and review_required=true.
- live_trading_authorized must remain false.
- broker_execution_mode must remain paper_only.

### Stabilization Result
- PO4 implementation status: Done / CI-green.
- CI status: green.
- Live trading authorization: unchanged; not granted by code.

---

## PO3 Daily Observation Run Record — 2026-06-01

### Added
- Added `docs/operations/po3_daily_observation_run_record.md` to define the daily Paper Observation run-record contract.
- Added `tests/test_po3_daily_observation_run_record.py` to guard required fields, status vocabulary, acceptance mapping and the paper-only safety boundary.

### Record Vocabulary
- ACCEPTED.
- REJECTED.
- NEEDS_REVIEW.

### Stabilization Result
- PO3 implementation status: Done / CI-green.
- CI status: green.
- Live trading authorization: unchanged; not granted by code.

---

## PO2 Daily Observation Acceptance Gate — 2026-06-01

### Added
- Added `docs/operations/po2_daily_observation_acceptance_gate.md` to define when a Paper Observation day is accepted as valid evidence.
- Added `tests/test_po2_daily_observation_acceptance_gate.py` to guard required evidence families, rejection reasons, status vocabulary and the research-only safety boundary.

### Acceptance Vocabulary
- ACCEPTED.
- REJECTED.
- NEEDS_REVIEW.

### Stabilization Result
- PO2 implementation status: Done / CI-green.
- CI status: green.
- Live trading authorization: unchanged; not granted by code.

---

## PO1 Paper Observation Timeline — 2026-06-01

### Added
- Added `docs/operations/po1_paper_observation_timeline.md` to formalize the Paper Observation evidence period.
- Added `tests/test_po1_paper_observation_timeline.py` to guard the observation start date, review dates, required evidence families and live-trading block.

### Paper Observation Timeline
- Start date: 2026-06-01.
- Minimum duration: 3 months.
- Target duration: 3-6 months.
- First review date: 2026-07-01.
- Major evidence review date: 2026-09-01.
- Extended review date: 2026-12-01.

### Stabilization Result
- PO1 implementation status: Done / CI-green.
- CI status: green.
- Live trading authorization: unchanged; not granted by code.

---

## IP9/IP10 Public Repository Governance — 2026-06-01

### Added
- Added public-edge pull request review governance for newly introduced edge constants.
- Added license and usage disclaimer documentation for the public decision-support research framework.
- Added `docs/operations/ip9_ip10_public_repo_governance.md` and `tests/test_ip9_ip10_public_repo_governance.py`.

### Stabilization Result
- IP9/IP10 implementation status: Done / CI-wired.
- CI status: guarded by `tests/test_ip9_ip10_public_repo_governance.py`.
- Live trading authorization: unchanged; not granted by code.
