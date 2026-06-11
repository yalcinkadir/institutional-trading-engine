# CHANGELOG

## Watcher Lifecycle Evidence #193 — 2026-06-11

### Added
- Added `scripts/watcher_lifecycle_summary.py` to build deterministic, lightweight watcher lifecycle summaries without growing the ARCH106 `src/` module baseline.
- Added dated and latest lifecycle summary outputs:
  - `reports/watchers/lifecycle/YYYY-MM-DD.json`
  - `reports/watchers/lifecycle/latest.json`
- Added `tests/test_193_watcher_lifecycle_summary.py` to prove lifecycle summaries are written for zero-actionable/no-trade watcher runs.
- Added `docs/operations/watcher_lifecycle_evidence.md` as the authoritative lifecycle evidence contract.

### Changed
- Updated `scripts/run_entry_exit_watcher.py` so every successful watcher cycle writes lifecycle summary evidence, including cycles with zero actionable open signals.
- Moved watcher lifecycle summary writing out of `src/` and into the runner/script evidence layer to keep ARCH106 production-module ratchet stable.
- Updated `README.md` and `ROADMAP.md` with the #193 watcher lifecycle evidence boundary.

### Guardrails
- A watcher cycle with zero actionable open signals is explicitly marked `NO_ACTIONABLE_SIGNALS`.
- Silent watcher success is not accepted as signal-level forward evidence.
- Lifecycle summaries include the original signal file path and SHA256 checksum reference.
- `data/signal_lifecycle.jsonl` remains a mutable event log; the repo-visible authoritative summary is under `reports/watchers/lifecycle/`.

### Boundary
- This is watcher evidence/auditability hardening.
- No strategy rule, scoring threshold, entry/exit rule or broker execution capability is changed.
- Live trading authorization: unchanged; not granted by code.
- Repository-wide full-regression green is not claimed by this changelog entry.

---

## Backtest Runtime Pipeline Coupling #177 — 2026-06-11

### Changed
- Hardened `scripts/validate_bt9_real_historical_input_pack.py` so BT9 real-data input validation now requires canonical #177 pipeline metadata before a backtest input pack can pass as strategy evidence.
- Updated `tests/test_htp1_historical_trade_plan_export.py` with a guard proving fixture-declared pipeline metadata from validated observation exports is rejected by BT9.
- Updated `docs/operations/historical_trade_plan_generation.md` to separate baseline/demo generation, Paper Observation research export and canonical Scanner → Signal → Quality → Validator real-data evidence.
- Updated `README.md` to clarify that real-data strategy evidence requires `pipeline_generation_source=scanner_signal_quality_validator`.

### Guardrails
- Trade plans without metadata are blocked from real-data strategy evidence.
- Trade plans with `pipeline_generation_source=validated_paper_observation_export` are blocked from real-data strategy evidence even when records contain `pipeline_coupled: true` metadata.
- BT9 requires `pipeline_coupled == true`, `pipeline_generation_source == scanner_signal_quality_validator`, all required runtime gates and a positive `validated_trade_plan_count`.
- Validated Paper Observation exports remain available for research/audit continuity but cannot be promoted into real-data strategy evidence.

### Boundary
- This is evidence-boundary and backtest-input hardening.
- No strategy rule, scoring threshold, entry/exit rule or broker execution capability is changed.
- Live trading authorization: unchanged; not granted by code.
- Repository-wide full-regression green is not claimed by this changelog entry.

---

## Signal State Consistency #194 — 2026-06-11

### Added
- Added `tests/test_194_signal_state_consistency.py` to guard the signal action/decision/risk-tier execution-state invariant.
- Added #194 signal execution-state rules to `docs/architecture/dataflow_contract_matrix.md`.

### Changed
- Updated `README.md` with #194 signal state consistency status.
- Documented `action` as the execution-readiness source of truth for downstream watcher, outcome, backtest and future adapter consumers.

### Guardrails
- Exported `NO_TRADE` records cannot retain `decision: approved`.
- Exported `NO_TRADE` records cannot retain actionable risk tiers such as `tier_1`, `tier_2` or `tier_3`.
- Exported `NO_TRADE` records must carry `position_size: 0.0` and no executable `entry_trigger`.
- Downstream consumers must require `action == "BUY_WATCH"` before treating a signal as executable paper-observation input.

### Boundary
- This is signal-boundary and downstream-consumer safety hardening.
- No strategy rule, scoring threshold, entry/exit rule or broker execution capability is changed.
- Live trading authorization: unchanged; not granted by code.
- Repository-wide full-regression green is not claimed by this changelog entry.

---

## Report Validation Risk Tier #185 — 2026-06-11

### Added
- Added `tests/test_185_report_validation_risk_tier.py` with positive and negative guard coverage for report risk-tier validation.
- Added machine-readable `risk_tier_evidence` to `ReportQualityResult` so report validation can expose #185 status, matched decision/risk-tier rows and explicit no-active-risk handling.

### Changed
- Updated `src/reporting/report_quality.py` so market-report validation no longer accepts a loose prose-only `Risk Tier` mention as sufficient evidence.
- Updated `scripts/validate_report_quality.py` to print the exact report file path, canonical decision/risk-tier pattern, validation status, row count and explicit no-active-risk state.
- Updated `README.md` with #185 report validation risk-tier gate status.

### Guardrails
- Canonical rows such as `- Decision: **approved** | Risk Tier: tier_1`, `tier_2` or `tier_3` are accepted.
- Reports with only prose-level `Risk Tier` mentions are blocked.
- Explicit no-active-risk reports are accepted when the report clearly states no ranked opportunities qualified for active risk and remains in No-Trade / watch mode.
- Actionable decisions cannot carry `no_trade` risk tier.
- Non-actionable decisions must carry `no_trade` risk tier.
- Invalid risk-tier values are blocked.

### Boundary
- This is report-validation and evidence-governance hardening.
- No strategy rule, scoring threshold, entry/exit rule or broker execution capability is changed.
- Live trading authorization: unchanged; not granted by code.
- Repository-wide full-regression green is not claimed by this changelog entry.

---

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
- Added `docs/operations/bt184_historical_input_auditability.md` as the durable audit source-of-truth contract for accepted BT131 real-data evidence.
- Added guard coverage proving BT131 repository persistence happens before temporary Actions artifact upload.

### Changed
- Updated Polygon historical ingestion so each successful CSV output records `output_sha256` in ingestion metadata and coverage manifests.
- Updated `scripts/validate_bt9_real_historical_input_pack.py` so real historical input packs fail closed when coverage manifests are missing, missing `symbols[].output_sha256`, or checksum-mismatched against the actual bars file.
- Updated `scripts/run_historical_entry_exit_backtest.py` and `src/backtesting/historical_entry_exit_backtest.py` so BT9 input checksums are propagated into real-data backtest evidence.
- Updated `scripts/validate_real_data_backtest_evidence_gate.py` so accepted real-data evidence requires non-empty valid SHA256 `input_checksums`.
- Updated BT131 workflow persistence so successful real-data runs commit reports plus source inputs: historical CSV bars, coverage manifest, ingestion metadata, runtime universe, historical trade plans and trade-plan manifest.
- Updated BT9, HIST1, HTP1 and BT131 workflow tests for checksum-backed input persistence.
- Updated `README.md` and `ROADMAP.md` with the #184 auditability rule and repository-as-source-of-truth boundary.

### Guardrails
- A real-data backtest result is not claimable if the bars file cannot be tied to a coverage manifest checksum.
- GitHub Actions artifacts alone are not treated as the audit source of truth for successful real-data backtests.
- Missing, empty or malformed `input_checksums` blocks accepted real-data evidence.
- Checksum mismatches produce explicit BT9 failures rather than degraded success.
- Accepted BT131 evidence must persist source CSVs, metadata, trade plans and evidence indexes to repository paths; temporary Actions artifacts are review aids only.

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
