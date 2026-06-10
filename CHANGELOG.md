# CHANGELOG

## BT176 Guarded Entry Confirmation Experiment — 2026-06-10

### Added
- Added `scripts/analyze_bt176_guarded_entry_confirmation_experiment.py`.
- Added `tests/test_bt176_guarded_entry_confirmation_experiment.py`.
- Added `docs/operations/bt176_guarded_entry_confirmation_experiment.md`.

### Changed
- Wired BT176 into `.github/workflows/bt131_real_data_backtest_evidence.yml` after BT133 report generation.
- The BT131 evidence workflow now persists BT176 JSON and Markdown artifacts into run-specific and latest real-data report folders.
- The real-data backtest index now records `bt176_guard_status`, `bt176_candidate_variant_id`, `bt176_experiment_scope` and `bt176_production_rule_change_allowed`.
- BT133 recommendation logic now checks explicit overfit risk before insufficient-sample classification.
- Updated workflow guard tests to cover BT132, BT133 and BT176 persistence together.

### Boundary
- BT176 is research-only and paper-observation shadow-only.
- No production entry rule is changed.
- `broker_execution_mode=paper_only` remains explicit.
- Promotion to production requires a separate issue with fresh forward evidence and explicit approval.

### Status
- #176: Implemented / BT176 evidence workflow green on run `27267495405` for commit `121f6e7b999a32eac0c3340596062c765285fa15`.
- Full repository regression is not claimed here; this status is scoped to the real-data BT131/BT132/BT133/BT176 evidence workflow.

---

## P148 CI-Truthful Status Claims Guard — 2026-06-08

### Added
- Added `docs/operations/ci_truthful_status_claims_policy.md`.
- Added `scripts/validate_ci_truthful_status_claims.py`.
- Added `tests/test_ci_truthful_status_claims.py`.

### Changed
- Documentation status claims now distinguish scoped feature-level `CI-green` labels from repository-wide health claims.
- Repository-wide green claims must be accompanied by concrete evidence such as a successful run/job URL, commit SHA, or evidence artifact.
- Single targeted-test success is explicitly not treated as full-regression success.
- Removed optimistic unscoped `CI is green` wording from the changelog history.

### Validated
- Unsupported repository-wide green claims are blocked by tests.
- Repository-wide claims with run/job or commit evidence are allowed.
- Feature-level historical labels such as `Done / CI-green` remain allowed as scoped status labels.
- The guard validates README, ROADMAP and CHANGELOG through test coverage.

### Status
- P148: Implemented / CI-pending.
- Live trading authorization: unchanged; not granted by code.

---

## P149 Governance/Kill-Switch Runtime-Proof — 2026-06-08

### Status
- #149: Closed / completed.
- Runtime governance is executed in the active report path.
- Kill-switch and governance denial block actionable output.
- Signal and report artifacts expose governance state.
- Live trading authorization: unchanged; not granted by code.

---

## P152 Paper Observation Health Evidence — 2026-06-08

### Status
- #152: Implemented / CI-green; runtime artifact closure remains dependent on a real scheduled Institutional Reports artifact.
- Paper Observation health artifacts include run metadata, commit SHA, workflow name, provenance, degradation reasons and governance state.
- Live trading authorization: unchanged; not granted by code.

---

## P146 VIX/Regime Data Failure Provenance — 2026-06-08

### Status
- #146: Closed / completed.
- VIX/regime data no longer fails silently on unavailable index data.
- Volatility proxy provenance and degraded health state are reported explicitly.
- Live trading authorization: unchanged; not granted by code.

---

## P153 Report Output Boundary — 2026-06-08

### Status
- #153: Closed / completed.
- Report-quality workflow writes generated report artifacts under allowed generated-report paths.
- Protected public report paths remain guarded.

---

## IP9/IP10 Public Repository Governance — 2026-06-01

### Status
- IP9: Done / CI-wired.
- IP10: Done / CI-wired.
- Historical anchor retained for public repository governance tests.
- Live trading authorization: unchanged; not granted by code.

---

## Historical changelog note

Earlier detailed entries remain available in git history. Current and future changelog status language follows `docs/operations/ci_truthful_status_claims_policy.md`.
