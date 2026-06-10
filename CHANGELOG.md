# CHANGELOG

## Logic Safety Governance #189 — 2026-06-11

### Added
- Added `docs/architecture/system-invariants.md`.
- Added `docs/operations/logic-safety-governance.md`.
- Added `tests/test_system_invariants.py`.
- Added `tests/test_logic_safety_state_matrix.py`.
- Added `tests/test_evidence_traceability_contract.py`.

### Changed
- Updated `.github/pull_request_template.md` with a Logic Safety Governance section.
- Updated `README.md` to document #189, System Invariants and the targeted guard test command.
- Updated `ROADMAP.md` to add #189 as a P0 machine-checkable logic-safety governance layer.

### Guardrails
- System invariants now define severity classes `P0_BLOCKER`, `P1_DEGRADED` and `P2_WARNING`.
- The logic-safety state matrix blocks promotion of `UNKNOWN`, `DEGRADED`, `BLOCKED`, demo/stub/synthetic or missing-provenance output as full `PASS` evidence.
- Evidence traceability now requires run identity, data mode, source/provenance, checksum or artifact hash, pipeline/generator version and runtime trace where applicable.
- PRs touching decision/evidence logic must map changes to affected invariants and link a concrete evidence or test command.

### Boundary
- This is a governance and guard-test layer.
- No strategy rule, scoring threshold, entry/exit rule or broker execution capability is changed.
- Live trading authorization: unchanged; not granted by code.
- Repository-wide full-regression green is not claimed by this changelog entry.

---

## FCM1 / RPW1 CI-wired Backlog Closure #104 — 2026-06-11

### Verified
- #104 was already closed/completed on GitHub.
- FCM1 has implementation, guard tests and dedicated targeted CI workflow wiring.
- RPW1 has implementation, guard tests and dedicated targeted CI workflow wiring.
- Closure evidence is documented in `docs/operations/fcm1_rpw1_connectivity_proof_pack_retention_closure_2026_06_03.md`.

### Changed
- Updated FCM1/RPW1 closure evidence from `implemented / CI-wired` to `closed / targeted CI-wired evidence verified`.
- Updated `ROADMAP.md` so #104 is no longer listed as the next open remediation item.
- Updated `README.md` so FCM1/RPW1 are represented as targeted feature closures, not stale open CI-wired backlog items.
- Recommended next remediation order now starts with #106.

### Boundary
- This is a targeted feature closure.
- Repository-wide full-regression green is not claimed by this changelog entry.
- Live trading authorization: unchanged; not granted by code.
- Broker execution: unchanged; remains paper-only infrastructure.

---

## JWT Fail-Closed Migration #103 — 2026-06-11

### Added
- Added `docs/operations/jwt_fail_closed_migration_103.md` as closure evidence for the JWT authentication safety boundary.

### Verified
- Existing JWT implementation refuses missing or blank `INSTITUTIONAL_JWT_SECRET`.
- Token creation and validation both fail closed when the JWT secret is not configured.
- Protected API routes return explicit authentication/configuration failures instead of accepting requests.
- Existing guard coverage is documented for `tests/test_jwt_auth.py` and `tests/test_security_layer.py`.

### Changed
- Updated `ROADMAP.md` so #103 is no longer listed as the next open remediation item.
- Recommended next remediation order now starts with #104, then #106.

### Boundary
- Live trading authorization: unchanged; not granted by code.
- Broker execution: unchanged; not authorized by this closure.
- Repository-wide full-regression green is not claimed by this changelog entry.

---

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
