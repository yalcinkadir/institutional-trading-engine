# CHANGELOG

## PO2 Daily Observation Acceptance Gate — 2026-06-01

### Added
- Added `docs/operations/po2_daily_observation_acceptance_gate.md` to define when a Paper Observation day is accepted as valid evidence.
- Added `tests/test_po2_daily_observation_acceptance_gate.py` to guard required evidence families, rejection reasons, status vocabulary and the research-only safety boundary.

### Acceptance Vocabulary
- ACCEPTED.
- REJECTED.
- NEEDS_REVIEW.

### Stabilization Result
- PO2 implementation status: Done / CI-green.
- CI status: green.
- Live trading authorization: unchanged; not granted by code.

---

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

## IP9/IP10 Public Repository Governance — 2026-06-01

### Added
- Added public-edge pull request review governance for newly introduced edge constants.
- Added license and usage disclaimer documentation for the public decision-support research framework.
- Added `docs/operations/ip9_ip10_public_repo_governance.md` and `tests/test_ip9_ip10_public_repo_governance.py`.

### Stabilization Result
- IP9/IP10 implementation status: Done / CI-wired.
- CI status: guarded by `tests/test_ip9_ip10_public_repo_governance.py`.
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
