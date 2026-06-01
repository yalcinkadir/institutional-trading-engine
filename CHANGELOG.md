# CHANGELOG

## PO1 Paper Observation Timeline — 2026-06-01

### Added
- Added `docs/operations/po1_paper_observation_timeline.md` to formalize the Paper Observation evidence period.
- Added `tests/test_po1_paper_observation_timeline.py` to guard the observation start date, review dates, required evidence families and live-trading block.

### Paper Observation Timeline
- Start date: 2026-06-01.
- Minimum duration: 3 months.
- Target duration: 3-6 months.
- First review date: 2026-07-01.
- Major evidence review date: 2026-09-01.
- Extended review date: 2026-12-01.

### Stabilization Result
- PO1 implementation status: Done / CI-green.
- CI status: green.
- Live trading authorization: unchanged; not granted by code.

---

## BT8 Backtesting Evidence Report — 2026-06-01

### Added
- Added `src/validation/backtesting_evidence_report.py` for reproducible BT8 JSON/Markdown reports from BT3 backtest run contracts.
- Added `scripts/generate_backtesting_evidence_report.py` CLI.
- Added `tests/test_bt8_backtesting_evidence_report.py` and `tests/test_bt8_demo_contracts.py`.
- Added public-safe demo contracts under `examples/backtesting/bt8_demo_contracts.json`.

### Stabilization Result
- BT8 implementation status: Done / CI-green.
- CI status: green.
- Live trading authorization: unchanged; not granted by code.

---

## Post-RGP Stabilization Review — 2026-06-01

### Added
- Added `tests/test_post_rgp_status_consistency.py` as a documentation-status regression guard for the completed RGP proof pack.
- The guard verifies that README and ROADMAP keep RGP1-RGP12 aligned as Done / CI-green after the Post-RGP review.

### Changed
- Corrected remaining README status drift for RGP4 from CI-wired to CI-green.
- Locked the completed Runtime Governance Proof Pack documentation state after RGP1-RGP12 reached CI-green.

### Stabilization Result
- RGP1-RGP12 status: Done / CI-green.
- Post-RGP documentation consistency guard: implemented / CI-wired.
- CI status: pending current run.
- Live trading authorization: unchanged; not granted by code.

---
## RGP12 Partial Exit Lifecycle Persistence — 2026-06-01

### Added
- RGP12: added regression coverage for `PARTIAL_EXIT_FILLED` lifecycle persistence after Target-1 runner activation.
- Added `tests/test_rgp12_partial_exit_lifecycle.py` to prove Target-1 runner management emits a supplemental partial-exit lifecycle event.
- Added coverage proving `append_lifecycle_updates()` persists both `TARGET_1_HIT` and `PARTIAL_EXIT_FILLED` JSONL records and deduplicates repeated writes.

### Changed
- RGP12 is resolved by persisting the `PARTIAL_EXIT_FILLED` path instead of removing it.
- `README.md` and `ROADMAP.md` now document RGP12 as Done / CI-green.

### Stabilization Result
- RGP12 implementation status: Done / CI-green.
- CI status: green.
- Live trading authorization: unchanged; not granted by code.

---

## RGP8 Artifact Upload-On-Failure Governance Guard — 2026-06-01

### Added
- RGP8: added CI guard coverage that protects alert/evidence artifacts from git persistence failure.
- Added `tests/test_rgp8_artifact_upload_on_git_failure.py` to scan repo-writing GitHub Actions workflows.
- Added regression coverage proving repo-writing workflows must upload alert/evidence/runtime artifacts with `if: always()`.

### Changed
- Artifact retention safety is now enforced as a future-proof workflow guard instead of relying on manual review only.
- The RGP documentation now includes alert/evidence artifact upload-on-failure governance.

### Stabilization Result
- RGP8 implementation status: implemented / CI-wired.
- CI status: pending current run.
- Live trading authorization: unchanged; not granted by code.

---

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
