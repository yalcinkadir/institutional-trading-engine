# CHANGELOG

## Runtime Reachability Guard #178 — 2026-06-11

### Added
- Added `docs/architecture/decision_critical_runtime_reachability.json`.
- Added `tests/test_runtime_reachability_guard_178.py`.

### Changed
- Updated `README.md` with #178 runtime reachability governance, targeted guard command and current module boundary.
- Updated `ROADMAP.md` to add #178 as implemented / targeted guard tests documented and remove #178 from the next remediation order.

### Guardrails
- Decision-critical modules must either be `runtime_connected` with a runtime entry point plus guard-test proof, or explicitly classified as `experimental`, `quarantine`, `test_only` or `deprecated`.
- Non-runtime decision helpers must not support claims such as `decision_stack_validated`, `runtime_active`, `module_complete`, `strategy_validated`, `paper_confidence_authorized` or `live_ready`.
- `src/decision_confidence.py`, `src/data_quality_engine.py`, `src/event_risk_engine.py` and `src/liquidity_volatility_engine.py` are explicitly classified as non-runtime research helpers until promoted with runtime execution proof.

### Boundary
- This is a registry, documentation and guard-test closure.
- No strategy rule, scoring threshold, entry/exit rule or broker execution capability is changed.
- Live trading authorization: unchanged; not granted by code.
- Repository-wide full-regression green is not claimed by this changelog entry.

---

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

---

## BT176 Guarded Entry Confirmation Experiment — 2026-06-10

### Added
- Added `scripts/analyze_bt176_guarded_entry_confirmation_experiment.py`.
- Added `tests/test_bt176_guarded_entry_confirmation_experiment.py`.
- Added `docs/operations/bt176_guarded_entry_confirmation_experiment.md`.
