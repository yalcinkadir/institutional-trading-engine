# CHANGELOG

## Scheduled Report Liveness #192 — 2026-06-11

### Added
- Added workflow-facing scheduled report liveness validation logic inside `scripts/validate_scheduled_report_liveness.py` to build canonical scheduled report liveness evidence without expanding the `src/` runtime-module inventory.
- Added `scripts/validate_scheduled_report_liveness.py` as the workflow-facing #192 validation CLI.
- Added `tests/test_192_scheduled_report_liveness.py` to guard missing, empty and complete scheduled report evidence paths.

### Changed
- Updated `.github/workflows/institutional-reports.yml` so scheduled reports run #192 liveness validation after report quality and paper-observation health validation.
- Updated the report workflow to archive `reports/scheduled_report_liveness/*.json` and persist bounded liveness evidence paths with report/signals/validation outputs.
- Updated `tests/test_po11_scheduled_daily_observation_workflow.py` with workflow-level guards proving #192 is wired into the scheduled report path.
- Updated `README.md` and `ROADMAP.md` with the #192 scheduled report liveness rule.

### Guardrails
- A scheduled market report is not a productive report cycle unless the dated report, latest report, latest signals payload and latest paper-observation health artifact exist and are non-empty.
- Missing or empty scheduled output is `BLOCKED` evidence, not an invisible green scheduled cycle.
- Weekly reports are not forced to produce signals or paper-observation health evidence.

### Boundary
- This is report-liveness and evidence-governance hardening.
- No strategy rule, scoring threshold, entry/exit rule or broker execution capability is changed.
- Live trading authorization: unchanged; not granted by code.
- Repository-wide full-regression green is not claimed by this changelog entry.

---

## IP9/IP10 Public Repository Governance — 2026-06-11

### Added
- Added IP9 public-edge review governance to the PR review process.
- Added IP10 license and research-only usage disclaimer status coverage.

### Guardrails
- Public repository changes must preserve public-demo defaults and must not expose proprietary thresholds, setup maps, scoring weights, exit profiles or production-like parameters.
- Research/paper-only and no-live-trading language must remain intact in public-facing project files.

### Boundary
- This is public repository governance and disclosure-safety documentation.
- No strategy rule, scoring threshold, entry/exit rule or broker execution capability is changed.
- Live trading authorization: unchanged; not granted by code.

---

## System Invariants and Logic Safety Governance #189 — 2026-06-11

### Added
- Added machine-checkable System Invariants and Logic Safety Governance coverage for #189.
- Added status coverage for forbidden state conversions, logic-safety severity classes and evidence-traceability requirements.

### Guardrails
- `DEGRADED`, `BLOCKED`, `UNKNOWN`, demo/stub and missing-provenance states must not be promoted as full `PASS` evidence.
- Logic-safety mappings require evidence commands, guard tests, contract tests, validation scripts, CI workflow results or evidence artifacts.

### Boundary
- This is logic-safety governance and evidence-traceability hardening.
- No strategy rule, scoring threshold, entry/exit rule or broker execution capability is changed.
- Live trading authorization: unchanged; not granted by code.
- Repository-wide full-regression green is not claimed by this changelog entry.

---

## Historical Real-Data Input Persistence #184 — 2026-06-11

### Added
- Added `tests/test_184_historical_input_persistence.py` to guard historical real-data input auditability.
- Added BT9 checksum validation for persisted historical bars through `coverage_manifest.json`.
- Added `input_checksums` to accepted and blocked real-data backtest evidence artifacts.

### Changed
- Updated Polygon historical ingestion so each successful CSV output records `output_sha256` in ingestion metadata and coverage manifests.
- Updated `scripts/validate_bt9_real_historical_input_pack.py` so real historical input packs fail closed when coverage manifests are missing, missing `symbols[].output_sha256`, or checksum-mismatched against the actual bars file.
- Updated `scripts/run_historical_entry_exit_backtest.py` and `src/backtesting/historical_entry_exit_backtest.py` so BT9 input checksums are propagated into real-data backtest evidence.
- Updated `scripts/validate_real_data_backtest_evidence_gate.py` so accepted real-data evidence requires non-empty valid SHA256 `input_checksums`.
- Updated BT131 workflow persistence so successful real-data runs commit reports plus source inputs: historical CSV bars, coverage manifest, ingestion metadata, runtime universe, historical trade plans and trade-plan manifest.
- Updated BT9, HIST1, HTP1 and BT131 workflow tests for checksum-backed input persistence.
- Updated `README.md` and `ROADMAP.md` with the #184 auditability rule.

### Guardrails
- A real-data backtest result is not claimable if the bars file cannot be tied to a coverage manifest checksum.
- GitHub Actions artifacts alone are not treated as the audit source of truth for successful real-data backtests.
- Missing, empty or malformed `input_checksums` blocks accepted real-data evidence.
- Checksum mismatches produce explicit BT9 failures rather than degraded success.

### Boundary
- This is an evidence-auditability and reproducibility layer.
- No strategy rule, scoring threshold, entry/exit rule or broker execution capability is changed.
- Live trading authorization: unchanged; not granted by code.
- Repository-wide full-regression green is not claimed by this changelog entry.

---

## CI Gate Fixes — 2026-06-11

### Fixed
- Fixed `scripts/evaluate_evidence_quality_gate.py` so direct subprocess execution can import `src.evidence_quality_gate` by adding the repository root to `sys.path`.
- Aligned `docs/operations/evidence-quality-gate.md` with the machine-readable #188 claim tokens checked by `tests/test_evidence_quality_gate_188.py`.
- Updated `scripts/generate_module_inventory.py` so #188 evidence-governance helper modules are excluded from ARCH106 trading-runtime inventory checks instead of increasing the unclassified legacy baseline.

### Boundary
- These are CI/governance consistency fixes.
- No strategy rule, scoring threshold, entry/exit rule or broker execution capability is changed.
- Live trading authorization: unchanged; not granted by code.
- Repository-wide full-regression green is not claimed by this changelog entry.

---

## Evidence Quality Gate #188 — 2026-06-11

### Added
- Added `docs/operations/evidence-quality-gate.md`.
- Added `src/evidence_quality_gate.py`.
- Added `scripts/evaluate_evidence_quality_gate.py`.
- Added `tests/test_evidence_quality_gate_188.py`.

### Changed
- Updated `README.md` with #188 Evidence Quality Gate status, policy links, machine-readable CLI example and targeted guard command.
- Updated `ROADMAP.md` to add #188 as implemented / targeted guard tests documented and remove #188/#190 from the next remediation order.
- Closed #190 as duplicate of #188.

### Guardrails
- Roadmap-stable, strategy-promotion, production-grade evidence, paper-confidence, backtesting-promotion, decision-stack-validation and live-readiness claims must pass the Evidence Quality Gate first.
- Demo, stub, synthetic, placeholder or degraded evidence cannot support promotion claims.
- Required promotion evidence includes `run_id`, `data_mode`, `provenance`, `checksum_or_manifest`, `runtime_trace` and `promotion_claim`.
- The gate tracks evidence-critical blockers #177, #178, #181, #184, #185, #186 and #187.
- The gate returns machine-readable `PASS`, `DEGRADED` or `BLOCKED` output with exact blocker reasons and issue references.

### Boundary
- This is an evidence-governance and guard-test layer.
- It does not claim that all evidence-critical blockers are solved.
- It does not claim repository-wide full-regression green.
- It does not authorize live trading, broker execution or capital allocation.

---

## Runtime Reachability Guard #178 — 2026-06-11

### Added
- Added `docs/architecture/decision_critical_runtime_reachability.json`.
- Added `tests/test_runtime_reachability_guard_178.py`.
