# CHANGELOG

## PSR3 Fill-Quality Evidence — 2026-05-31

### Added
- PSR3: added fill-quality evidence generation for paper/observation execution review.
- Added `src/operations/fill_quality_evidence.py` with normalized fill records, slippage calculation, reconciliation checks and PASS/WARN/FAIL summary status.
- Added `scripts/generate_fill_quality_evidence.py` for CLI-based fill-quality evidence generation from JSON fill records.
- Added regression coverage for buy/sell slippage, failed fills, unreconciled fills, required-field validation, summary status, JSON round-trip loading and live-trading authorization guardrails.

### Changed
- Paper execution quality can now be represented as a daily audit artifact and included in the runtime evidence manifest chain.
- Slippage, fill status and reconciliation status are no longer treated as loose observation details; they can be persisted as structured evidence.

### Stabilization Result
- PSR3 implementation status: done.
- CI status: green.
- Live trading authorization: unchanged; not granted by code.

---

## PSR2 Runtime Evidence Manifest Guard — 2026-05-31

### Added
- PSR2: added runtime evidence manifest guard for paper/observation acceptance.
- Added `src/operations/runtime_evidence_manifest_guard.py` with fail-closed manifest evaluation.
- Added `scripts/guard_runtime_evidence_manifest.py` for CLI-based manifest guard execution and optional JSON guard reports.
- Added regression coverage for missing manifests, invalid JSON/schema, PASS manifests, FAIL manifests, live-trading authorization mutation and date-based manifest lookup.

### Changed
- Daily observation evidence now requires a valid PASS manifest before the day can be accepted.
- Missing evidence, missing manifests or invalid manifest state now block acceptance instead of being silently tolerated.

### Stabilization Result
- PSR2 implementation status: done.
- CI status: green.
- Live trading authorization: unchanged; not granted by code.

---

## PSR1 Daily Runtime Evidence Manifest — 2026-05-31

### Added
- PSR1: added daily runtime evidence manifest generation for paper/observation evidence integrity.
- Added `src/operations/runtime_evidence_manifest.py` with deterministic artifact metadata, SHA256 hashing, PASS/FAIL status and manifest validation.
- Added `scripts/generate_runtime_evidence_manifest.py` for CLI-based manifest generation.
- Added regression coverage for hashing, required/optional artifacts, manifest PASS/FAIL semantics, JSON round-trip loading and live-trading authorization guardrails.

### Changed
- Post-SR work now starts with runtime evidence quality instead of new strategy complexity.
- Daily observation evidence can now be audited through required input/output/governance artifact hashes.

### Stabilization Result
- PSR1 implementation status: done.
- CI status: green.
- Live trading authorization: unchanged; not granted by code.

---

## SR8 Dependency Reproducibility Contract — 2026-05-31

### Added
- SR8: dependency installation now delegates from `requirements.txt` to `requirements.lock`.
- Added exact top-level runtime/test dependency pins for the current public research/test stack.
- Added regression coverage proving requirements are locked and that workflow-local requirements files cannot become a second dependency source of truth.

### Changed
- `requirements.txt` now acts as a stable entry point for CI and local installs while `requirements.lock` carries the pinned dependency contract.
- Runtime/test dependency drift is now guarded before further signal-runtime or governance work is trusted.

### Stabilization Result
- SR8 implementation status: done.
- CI status: green.
- Live trading authorization: unchanged; not granted by code.

---

## SR7 Completed-Bar Watcher Semantics — 2026-05-31

### Added
- SR7: watcher lifecycle evaluation now respects completed-bar semantics before emitting entry, stop or target lifecycle events.
- Added `PriceBar.is_complete`, `completed_at` and `completion_source` metadata for watcher auditability.
- Added regression coverage proving incomplete bars do not trigger entries, stops or targets.

### Changed
- `evaluate_signal_against_bar()` now preserves signal state when a price bar is explicitly incomplete.
- Polygon aggregate conversion now derives completion metadata from provider flags or daily-bar timestamps.
- Watcher evaluation remains deterministic and conservative while preventing intrabar high/low noise from being treated as final.

### Stabilization Result
- SR7 implementation status: done.
- CI status: green.
- Live trading authorization: unchanged; not granted by code.

---

## SR6 Governance Thresholds Single Source of Truth — 2026-05-31

### Added
- SR6: centralized runtime governance thresholds in `src/governance/governance_thresholds.py`.
- Added `GovernanceThresholds` and `DEFAULT_GOVERNANCE_THRESHOLDS` as the shared threshold source for kill-switch and runtime risk-limit checks.
- Added regression coverage proving custom threshold injection changes kill-switch behavior and that runtime cycle threshold configuration is injectable.

### Changed
- `evaluate_kill_switch()` now reads VIX, drawdown and anomaly kill thresholds from a shared `GovernanceThresholds` object instead of local magic numbers.
- `LiveRuntimeCycle` now accepts `governance_thresholds` and persists threshold configuration in decision payloads and governance-block payloads.
- Runtime risk-limit checks now use the same injected threshold source for max drawdown and daily loss limits.

### Stabilization Result
- SR6 implementation status: done.
- CI status: green.
- Live trading authorization: unchanged; not granted by code.

---

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
