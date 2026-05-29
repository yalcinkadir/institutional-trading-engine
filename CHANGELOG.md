# CHANGELOG

## BT6 Evidence Baseline Regression Gate — 2026-05-29

### Added
- BT6 evidence baseline regression gate model in `src/validation/evidence_baseline_regression_gate.py`.
- Public-safe synthetic baseline/current fixture in `data/demo_bt6_evidence_baseline.json`.
- CLI report generator in `scripts/generate_bt6_baseline_regression_report.py`.
- Operational documentation in `docs/operations/bt6_evidence_baseline_regression_gate.md`.
- Dedicated BT6 GitHub Actions workflow in `.github/workflows/bt6.yml`.

### Tests Added / Updated
- `tests/test_bt6_evidence_baseline_regression_gate.py`.
- BT6 tests cover happy path, missing required identity fields, strategy mismatch, dataset mismatch, missing/non-numeric metrics, missing artifact hashes, expectancy regression, Sharpe regression, OOS pass-rate regression, drawdown regression, trade-count collapse, missing public-safe tags, missing research-only footer, JSON loading, report writing and Markdown rendering.

### Improved
- Historical evidence can now be compared against an accepted baseline before a new result is treated as acceptable.
- BT6 blocks silent degradation across expectancy, Sharpe, OOS pass rate, drawdown and trade count.
- Generated BT6 reports remain research-only and do not authorize execution.

### Stabilization Result
- BT6 implementation status: implemented.
- BT6 CI workflow status: added / pending confirmation.
- Public demo evidence remains synthetic/demo-only.
- Broker execution remains intentionally not implemented.
- Live trading remains intentionally not authorized by code.

---

## BT5 Walk-Forward / Out-of-Sample Robustness Gate — 2026-05-29

### Added
- BT5 walk-forward / out-of-sample robustness gate model in `src/validation/walk_forward_robustness_gate.py`.
- Public-safe synthetic demo fold fixture in `data/demo_bt5_walk_forward_folds.json`.
- CLI report generator in `scripts/generate_bt5_walk_forward_report.py`.
- Operational documentation in `docs/operations/bt5_walk_forward_robustness_gate.md`.
- Dedicated BT5 GitHub Actions workflow in `.github/workflows/bt5.yml`.

### Tests Added / Updated
- `tests/test_bt5_walk_forward_robustness_gate.py`.
- BT5 tests cover happy path, missing required fields, too few folds, invalid chronology, overlapping OOS windows, missing/non-numeric metrics, low OOS trade count, excessive OOS drawdown, weak OOS pass rate, excessive train-to-OOS degradation, missing public-safe tags and missing research-only footer.

### Improved
- Walk-forward validation now has a deterministic report-level robustness gate.
- OOS evidence is checked against pass rate, positive primary metric rate, drawdown, trade count and train-to-OOS degradation constraints.
- Generated BT5 reports remain research-only and do not authorize execution.

### Stabilization Result
- BT5 implementation status: done.
- BT5 CI status: green.
- Public demo folds remain synthetic/demo-only.
- Broker execution remains intentionally not implemented.
- Live trading remains intentionally not authorized by code.

---

## BT3 Reproducibility Contract Gate — 2026-05-28

### Added
- BT3 reproducibility contract report model in `src/validation/backtest_run_contract.py`.
- Public-safe demo contracts in `data/demo_backtest_run_contracts.json`.
- CLI report generator in `scripts/generate_bt3_contract_report.py`.
- Operational documentation in `docs/operations/bt3_reproducibility_contract.md`.

### Tests Added / Updated
- `tests/test_bt3_backtest_run_contract.py`.
- CI workflow includes an explicit BT3 reproducibility contract test step before the full regression suite.

### Improved
- Historical validation evidence can now be checked for pinned run identity, strategy version, parameter version, dataset fingerprint, symbol set, date window, deterministic seed, result metrics and artifact hashes.
- BT3 complements the older deterministic backtest contract with a report-level evidence gate.
- Generated BT3 reports remain research-only and do not authorize execution.

### Stabilization Result
- BT3 implementation status: PR-open / CI pending.
- Public demo contracts remain synthetic or paper-observation only.
- Broker execution remains intentionally not implemented.

---

## BT2 Strategy Test Matrix — 2026-05-28

### Added
- Strategy Test Matrix model in `src/validation/strategy_test_matrix.py`.
- Public-safe demo matrix in `data/demo_strategy_test_matrix.json`.
- CLI report generator in `scripts/generate_strategy_test_matrix.py`.
- Operational documentation in `docs/operations/strategy_test_matrix.md`.

### Tests Added / Updated
- `tests/test_strategy_test_matrix.py`.
- CI workflow includes an explicit BT2 Strategy Test Matrix test step before the full regression suite.

### Improved
- Strategy coverage can now be validated across regimes, setup families, validation stages and data modes.
- BT2 blocks live-trading authorization terms and private/proprietary edge terminology in public matrix cases.
- Generated matrix reports remain research/paper-observation only.

### Stabilization Result
- BT2 implementation status: PR-ready.
- Live trading remains intentionally not authorized by code.
- Broker execution remains paper-only infrastructure.
- Public matrix data remains synthetic/demo-only.

---

## Phase B11 Daily Evidence Pipeline — 2026-05-26
