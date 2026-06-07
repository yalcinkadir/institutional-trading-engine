# CHANGELOG

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
