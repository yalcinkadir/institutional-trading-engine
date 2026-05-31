# CHANGELOG

## SR5 Persistent Anomaly-State Governance — 2026-05-31

### Added
- SR5: runtime governance now reads anomaly kill-switch evidence from persistent `data/anomaly_state.json` via `AnomalyStateStore`.
- Added `src/runtime/anomaly_state.py` with JSON-backed anomaly-state loading, input sanitization, legacy `severe_count` alias support and auditable warning output.
- Added regression coverage for missing, invalid, negative and persistent anomaly-state inputs.

### Changed
- `LiveRuntimeCycle` now includes `anomaly_state` in the decision payload and runtime state update.
- `severe_anomaly_count` is now sourced from persistent anomaly state first; process-local cache is retained only as a fallback for tests/development when persistent state is unavailable.

### Stabilization Result
- SR5 implementation status: done.
- CI status: green.
- Live trading authorization: unchanged; not granted by code.

---

## IP9/IP10 Public Repository Governance — 2026-05-31

### Added
- IP9/IP10 Public Repository Governance documentation status restored for CI evidence checks.
- Public repository governance documentation confirms proprietary logic boundaries, public-safe artifacts, and non-secret repository operation.
- Project status files now consistently document IP9/IP10 as completed and CI-wired.

### Stabilization Result
- IP9/IP10 implementation status: done.
- CI status: wired.
- Live trading authorization: unchanged; not granted by code.

---

## SR4 Trusted Portfolio Governance Source — 2026-05-31

### Fixed
- SR4: runtime portfolio override arguments no longer mark portfolio governance as valid.
- `portfolio_drawdown_percent` and `daily_loss_percent` supplied directly to `LiveRuntimeCycle.run()` are treated as untrusted runtime arguments and fail closed.
- Governance now requires a trusted portfolio-state source such as `PortfolioStateStore` / `data/portfolio_state.json` before runtime checks can pass.

### Added
- Regression coverage proving runtime portfolio argument overrides are rejected with `runtime_argument_override_rejected`.
- Regression coverage proving valid runtime-cycle tests use an injected trusted portfolio-state store instead of runtime governance overrides.

### Stabilization Result
- SR4 implementation status: done.
- CI status: green.
- Live trading authorization: unchanged; not granted by code.

---

## B1.1 Daily Evidence Operating Procedure — 2026-05-29

### Added
- Daily evidence operating procedure in `docs/operations/b11_daily_evidence_operating_procedure.md`.
- Guard regression coverage in `tests/test_b11_daily_evidence_operating_procedure.py`.
- Dedicated main CI step for B1.1 daily evidence operating procedure guard tests.

### Stabilization Result
- B1.1 daily evidence operating procedure status: done.
- CI status: green.
- Live trading authorization: unchanged; not granted by code.

---

## Evidence Artifact Index Consistency — 2026-05-29

### Added
- Central evidence artifact index in `docs/operations/evidence_artifact_index.md`.
- Guard regression coverage in `tests/test_evidence_artifact_index.py`.
- Dedicated main CI step for evidence artifact index guard tests.
