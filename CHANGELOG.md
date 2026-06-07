# CHANGELOG

## P132 Scanner Runtime Boundary — 2026-06-07

### Added
- Added `src/validation/scanner_runtime_boundary.py`.
- Added `tests/test_p132_scanner_runtime_boundary.py`.
- Added `docs/operations/p132_scanner_runtime_boundary.md`.

### Changed
- Added a scanner runtime boundary guard that requires explicit `selection_mode`, selected symbols and selection reason in runtime-report and Paper Observation evidence payloads.
- Static watchlists are now labelled as research setup only and cannot claim dynamic scanner breadth or trading-edge proof.
- Dynamic scanner claims require a documented `scanner_contract_ref`.
- Updated ROADMAP with P132 status and hard rule.

### Validated
- Static watchlist payloads pass only when the boundary is explicit.
- Missing or invalid `selection_mode` blocks runtime reports.
- Static watchlists cannot claim dynamic scanner behavior or trading edge.
- Dynamic scanner mode requires a scanner contract reference.
- Paper-only safety boundary remains enforced.

### Status
- P132: Implemented.
- Live trading authorization: unchanged; not granted by code.

---

## PortfolioState Fail-Closed Fixture Migration Closure — 2026-06-07

### Validated
- Confirmed runtime PortfolioState parsing requires an explicit boolean `governance_valid` field.
- Confirmed missing or non-boolean `governance_valid` returns a conservative fail-closed state instead of silently passing runtime governance.
- Confirmed valid test fixtures explicitly set `governance_valid=true` where successful runtime flow is expected.
- Confirmed committed default `data/portfolio_state.json` remains `governance_valid=false` until a real paper or broker portfolio-state source exists.

### Status
- #102: Closed / completed.
- Broker execution boundary unchanged: research and paper-observation only.

---

## W1 Entry/Exit Watcher Git-Write Decoupling CI-Green Closure — 2026-06-07

### Changed
- Promoted W1 Entry/Exit Watcher Git-Write Decoupling status from CI-wired to CI-green in documentation.
- Added README runtime-output boundary documentation for the scheduled Entry/Exit Watcher.
- Added W1 to the runtime governance roadmap as a completed CI-green safety control.
- Added W1 targeted test command to README core commands.

### Validated
- `.github/workflows/entry-exit-watcher.yml` uses read-only repository contents permission.
- Checkout credentials are non-persistent.
- Scheduled watcher runtime output is uploaded through `actions/upload-artifact@v4`.
- Scheduled watcher no longer performs `git add`, `git commit`, `git pull --rebase` or `git push`.
- Watcher concurrency is isolated from the shared repo-write group.

### Status
- W1: Done / CI-green.
- Live trading authorization: unchanged; not granted by code.

---

## BT130 Real Historical Backtest Evidence Pack Gate — 2026-06-06

### Added
- Added complete real-data backtest evidence-pack fields to historical backtest JSON output.
- Added explicit trade-plan load reporting with `input_plan_count`, `accepted_plan_count`, `rejected_plan_count` and `rejection_reasons`.
- Added `tests/test_bt130_real_historical_evidence_pack_gate.py`.

### Changed
- Real-data backtest runner now blocks when the coverage manifest is missing.
- Real-data backtest runner now blocks when all trade plans are rejected.
- P121 real-data evidence gate now validates plan counts, rejection reasons, input-pack gate status, artifact paths, results, and paper-only execution boundaries.
- Historical backtest Markdown output now includes evidence-pack metadata and rejected trade-plan details.

### Validated
- Demo backtests cannot pass as real-data evidence.
- Missing coverage manifest blocks real-data evidence creation.
- Fully rejected trade-plan input blocks real-data evidence creation.
- Rejected trade plans are counted and reasoned instead of silently skipped.
- `live_trading_authorized=false` and `broker_execution_mode=paper_only` remain required.

### Status
- BT130: Implemented / CI-pending.
- Live trading authorization: unchanged; not granted by code.

---

## W1 Entry/Exit Watcher Git Write Decoupling Guard — 2026-06-03

### Added
- Added `tests/test_w1_entry_exit_watcher_git_write_decoupling.py`.
- Added `docs/operations/w1_entry_exit_watcher_git_write_decoupling_closure_2026_06_03.md`.

### Changed
- Updated `.github/workflows/entry-exit-watcher.yml` to run with read-only repository contents permission.
- Removed scheduled watcher branch mutation from the workflow.
- Removed watcher `git add`, `git commit`, `git pull --rebase` and `git push` behavior.
- Changed watcher runtime output handling to artifact upload via `actions/upload-artifact@v4`.
- Changed watcher checkout to `persist-credentials: false` and shallow checkout.
- Changed watcher concurrency group from shared repo-write scope to isolated watcher scope.

### Validated
- Watcher workflow no longer requests repository write permission.
- Watcher workflow no longer commits or pushes generated runtime files to the schedule branch.
- Watcher workflow uploads runtime output artifacts.
- Watcher workflow no longer shares the global repo-write concurrency group.

### Status
- W1: Done / CI-wired.
- Live trading authorization: unchanged; not granted by code.

---

## FCM1 / RPW1 Connectivity and Proof-Pack Retention — 2026-06-03

### Added
- Added `src/validation/feature_connectivity_matrix_guard.py`.
- Added `src/validation/runtime_proof_pack_artifact_writer.py`.
- Added `tests/test_fcm1_feature_connectivity_matrix_guard.py`.
- Added `tests/test_rpw1_runtime_proof_pack_artifact_writer.py`.
- Added `.github/workflows/fcm-rpw-ci.yml`.
- Added `docs/operations/fcm1_rpw1_connectivity_proof_pack_retention_closure_2026_06_03.md`.

### Changed
- Added a feature connectivity matrix guard that requires feature identity, runtime gate, guard test, evidence artifact, documentation reference and dependency/consumer connectivity.
- Added a deterministic runtime proof-pack artifact writer that writes JSON artifacts and a retention index with SHA-256 artifact identity.
- Preserved the paper-only boundary by requiring `live_trading_authorized=false` and `broker_execution_mode=paper_only`.
- Updated README and ROADMAP with FCM1 / RPW1 status and commands.

### Validated
- Connected CI-green feature matrix passes.
- Missing guard test or evidence artifact blocks the matrix.
- Unknown upstream dependencies block the matrix.
- Runtime proof-pack artifact and retention index are written deterministically.
- Existing retention index entries are updated without duplicate `proof_pack_id` rows.
- Missing proof-pack identity, observation window or summary blocks artifact writing.
- Live/non-paper boundary violations block and normalize to safe output.

### Status
- FCM1: Done / CI-wired.
- RPW1: Done / CI-wired.
- Live trading authorization: unchanged; not granted by code.

---

## PFA1 Position-level Forward Evidence Attribution — 2026-06-03

### Added
- Added `src/validation/position_forward_evidence_attribution.py`.
- Added `tests/test_pfa1_position_forward_evidence_attribution.py`.
- Added `docs/operations/pfa1_position_forward_evidence_attribution_ci_green_closure_2026_06_03.md`.

### Changed
- Added a position-level forward-evidence attribution builder that joins position-risk attribution with forward outcome records by symbol.
- Exposed per-position risk contribution together with 1D, 5D, 20D, MFE and MAE outcome evidence.
- Summarized portfolio-level 1D, 5D and 20D forward outcomes.
- Preserved the paper-only boundary by requiring `live_trading_authorized=false` and `broker_execution_mode=paper_only`.

### Validated
- Review-ready position forward attribution passes.
- Missing outcome records block forward review.
- Failed position-risk attribution reports block forward review.
- Missing observation window or evidence manifest path blocks forward review.
- Live/non-paper boundary violations block and normalize to safe output.

### Status
- PFA1: Done / CI-green.
- Live trading authorization: unchanged; not granted by code.

---

## CER1 Capacity / Execution Realism Evidence Review Summary — 2026-06-03

### Status
- CER1: Done / CI-green.
- Live trading authorization: unchanged; not granted by code.

---

## RGP13 Runtime Proof Pack Summary Builder — 2026-06-03

### Status
- RGP13: Done / CI-green.
- Live trading authorization: unchanged; not granted by code.

---

## PO14 Forward Evidence Quality Gate — 2026-06-03

### Status
- PO14: Done / CI-green.
- Live trading authorization: unchanged; not granted by code.

---

## IP9/IP10 Public Repository Governance — 2026-06-01

### Status
- IP9: Done / CI-wired.
- IP10: Done / CI-wired.
- Live trading authorization: unchanged; not granted by code.
