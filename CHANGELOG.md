# CHANGELOG

## ER7 / ER8 Expectancy Statistical Discipline — 2026-06-02

### Added
- Added `tests/test_er7_er8_expectancy_statistical_discipline.py`.
- Added `docs/operations/er7_er8_expectancy_statistical_discipline_ci_green_closure_2026_06_02.md`.

### Changed
- Separated score evidence from size evidence in `src/scoring/expectancy_adjuster.py`.
- Added a stronger sample floor for size multipliers.
- Updated `tests/test_expectancy_adjuster.py` so small evidence sets may affect score while keeping multiplier neutral.
- Restored `reports/premarket-report.md` to a synthetic public-safe example after artifact hygiene caught generated report content.

### Validated
- Positive profiles below the stronger size-evidence floor can score while multiplier remains neutral.
- Negative profiles below the stronger size-evidence floor can reduce score while multiplier remains neutral.
- Positive asymmetric expectancy is not blocked only because win rate is low.
- Existing expectancy tests prove both 6-sample and 20-sample behavior.
- Public committed premarket report content is synthetic/public-safe again.

### Status
- ER7: CLOSED_CI_GREEN.
- ER8: CLOSED_CI_GREEN.
- Live trading authorization: unchanged; not granted by code.

---

## ER4 Atomic Persistence Remediation — 2026-06-02

### Added
- Added `src/persistence/atomic_write.py`.
- Added `tests/test_er4_atomic_persistence_guard.py`.
- Added `docs/operations/er4_atomic_persistence_ci_green_closure_2026_06_02.md`.

### Changed
- Updated `PortfolioStateStore.save(...)` to use the central atomic JSON writer.
- Preserved fail-closed portfolio-state warning semantics required by runtime governance tests.

### Validated
- Atomic JSON writes replace the destination via temporary sibling file and `os.replace`.
- Failed replacement preserves the existing destination file.
- Temporary files are cleaned up after failed replacement.
- `PortfolioStateStore` routes writes through `write_json_atomic(...)`.

### Status
- ER4: CLOSED_CI_GREEN.
- Live trading authorization: unchanged; not granted by code.

---

## ER1 / ER2 Backtest Realism Remediation — 2026-06-02

### Added
- Added `tests/test_er1_er2_backtest_realism_guard.py`.
- Added `docs/operations/er1_er2_backtest_realism_ci_green_closure_2026_06_02.md`.

### Validated
- ER1: `t1_t2` trades that touch Target 1 but never reach Target 2 expire at the final available close, not optimistically at Target 1.
- ER2: gap-through-entry fills at the worse open price and recalculates R-multiple from the actual entry fill.
- ER2: breakeven-after-T1 gap-down fills at the worse open, not artificially at exact breakeven.

### Status
- ER1: CLOSED_CI_GREEN.
- ER2: CLOSED_CI_GREEN.
- Live trading authorization: unchanged; not granted by code.

---

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

## IP9/IP10 Public Repository Governance — 2026-06-01

### Added
- Added PR public-edge review governance for newly introduced edge constants.
- Added license and usage disclaimer documentation for the public decision-support research framework.
- Added `docs/operations/ip9_ip10_public_repo_governance.md`.
- Added `tests/test_ip9_ip10_public_repo_governance.py`.

### Stabilization Result
- IP9/IP10 implementation status: Done / CI-wired.
- Live trading authorization: unchanged; not granted by code.
