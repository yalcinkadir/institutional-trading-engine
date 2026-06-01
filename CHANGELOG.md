# CHANGELOG

## RGP7 Repo-Write Workflow Governance Guard — 2026-06-01

### Added
- RGP7: added CI guard coverage for repo-writing GitHub Actions workflow governance.
- Added `tests/test_rgp7_repo_write_workflow_governance.py` to scan `.github/workflows/*.yml` and `.github/workflows/*.yaml`.
- Added regression coverage that fails when a workflow uses `git commit`, `git push`, `git pull` or `git rebase` without repo-wide concurrency or a robust push retry strategy.

### Changed
- Repo-write safety is now enforced as a future-proof guard instead of relying on manual workflow review only.
- The RGP documentation now includes repo-write workflow serialization/retry governance.

### Stabilization Result
- RGP7 implementation status: implemented / CI-wired.
- CI status: pending current run.
- Live trading authorization: unchanged; not granted by code.

---

## RGP6 Strict Critical Notification Handling — 2026-06-01

### Added
- RGP6: added strict notification handling for critical STOP/EXIT runtime alerts.
- Added `CriticalRuntimeAlertNotificationError` so critical notification transport failures and guardrail blocks cannot be silently masked.
- Added `NOTIFICATION_FAILED` failure evidence persistence before raising critical notification failures.
- Added regression coverage proving repository persistence is not attempted after critical notification failure or guardrail blocking.

### Changed
- Critical alert delivery now treats notification failure as a hard runtime failure, while repository persistence failure remains captured as evidence after alert persistence.
- Critical STOP/EXIT alert messages now identify the combined RGP5/RGP6 ordering and strict-notification guard.

### Stabilization Result
- RGP6 implementation status: implemented / CI-wired.
- CI status: pending current run.
- Live trading authorization: unchanged; not granted by code.

---

## RGP5 Critical Alert Ordering Guard — 2026-06-01

### Added
- RGP5: added critical STOP/EXIT runtime alert ordering guard.
- Added `src/notifications/critical_runtime_alert.py` to dispatch and persist critical lifecycle alerts before repository commit/rebase/push style persistence can fail.
- Added regression coverage proving alert JSON evidence exists before repository persistence runs and survives repository persistence failure.

### Changed
- Critical lifecycle alert handling now reuses the existing Telegram report dispatcher instead of introducing a parallel notification path.
- Critical STOP/EXIT alerts remain research/paper-only and explicitly state that no execution or live-trading authorization is granted.

### Stabilization Result
- RGP5 implementation status: implemented / CI-wired.
- CI status: pending current run.
- Live trading authorization: unchanged; not granted by code.

---

## RGP4 Provider Fetch Failure Governance — 2026-06-01

### Added
- RGP4: added actionable-signal provider/data-fetch failure blocking in the runtime governance approval gate.
- Added `DATA_PROVIDER_FETCH_FAILURE_REASON` so provider degradation is explicit in approval-block reasons.
- Added regression coverage proving actionable signal fetch failures block approval and non-actionable fetch failures are recorded without blocking.

### Changed
- `evaluate_runtime_governance_approval()` now accepts `actionable_signal` and `provider_fetch_errors` inputs.
- Runtime approval now fails closed when an actionable signal cannot be evaluated because required provider data is degraded or unavailable.
- Approval serialization now includes provider-fetch errors and actionable-signal context for auditability.

### Stabilization Result
- RGP4 implementation status: implemented / CI-wired.
- CI status: pending current run.
- Live trading authorization: unchanged; not granted by code.

---

## IP9/IP10 Public Repository Governance — 2026-05-31

### Added
- IP9/IP10 Public Repository Governance documentation restored for CI status-file guard coverage.
- Public repository governance remains research/paper-only and does not authorize live trading.

### Stabilization Result
- IP9 implementation status: Done / CI-wired.
- IP10 implementation status: Done / CI-wired.
- CI status: guard documented.
- Live trading authorization: unchanged; not granted by code.

---

## RGP3 Stale Portfolio State Governance — 2026-05-31

### Added
- RGP3: added stale `PortfolioState.updated_at` blocking in the runtime governance approval gate.
- Added `is_portfolio_state_stale()` with deterministic `now` injection for CI-stable regression tests.
- Added `STALE_PORTFOLIO_STATE_REASON` so stale governance evidence is explicit in approval-block reasons.
- Added regression coverage for stale portfolio state, recent portfolio state and invalid portfolio-state timestamps.

### Changed
- `evaluate_runtime_governance_approval()` now blocks approval when portfolio state is older than the configured maximum age.
- Invalid or future portfolio-state timestamps are treated as stale instead of silently trusted.
- Runtime governance approval now fails closed for missing, invalid or stale portfolio-state evidence before further expansion work is trusted.

### Stabilization Result
- RGP3 implementation status: done.
- CI status: green.
- Live trading authorization: unchanged; not granted by code.

---

## PSR4 Drift and Regime Evidence — 2026-05-31

### Added
- PSR4: added drift and regime-change evidence generation for paper/observation review.
- Added `src/operations/drift_regime_evidence.py` with drift metrics, cumulative drift status, regime-transition classification and PASS/WARN/FAIL summary status.
- Added `scripts/generate_drift_regime_evidence.py` for CLI-based evidence generation from JSON drift/regime input.
- Added regression coverage for PASS/WARN/FAIL drift thresholds, stable/minor/major/unknown regime transitions, cumulative drift, JSON round-trip loading and live-trading authorization guardrails.

### Changed
- Observation-day evidence can now document behavior drift and market-regime changes as structured audit artifacts.
- The PSR evidence chain now covers manifest presence, manifest validation, fill quality and drift/regime state.

### Stabilization Result
- PSR4 implementation status: done.
- CI status: green.
- Live trading authorization: unchanged; not granted by code.

---

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
