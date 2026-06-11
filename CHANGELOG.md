# CHANGELOG

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

## IP9/IP10 Public Repository Governance — 2026-06-10

### Added
- Added public-edge review language for PRs touching strategy, scoring, thresholds, exits, reports or evidence artifacts.
- Added license/disclaimer governance around research-only, paper-observation-only and no-live-trading boundaries.

### Guardrails
- Public repository changes must not expose proprietary thresholds, setup maps, scoring weights, exit profiles or production-like parameters.
- Public-safe defaults, synthetic fixtures and demo evidence remain separated from production-grade claims.
- Generated reports, raw evidence, provider extracts, ranked opportunity output and local artifacts must not be committed unless explicitly allowed by artifact policy.

### Boundary
- This is public repository hygiene and IP-boundary governance.
- It does not authorize live trading, broker execution or capital allocation.

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
