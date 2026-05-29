# CHANGELOG

## BT7 Capacity / Turnover / Realism Gate — 2026-05-29

### Added
- BT7 capacity, turnover and transaction-cost realism gate model in `src/validation/capacity_turnover_realism_gate.py`.
- Public-safe synthetic capacity/turnover fixture in `data/demo_bt7_capacity_turnover.json`.
- CLI report generator in `scripts/generate_bt7_capacity_turnover_report.py`.
- Operational documentation in `docs/operations/bt7_capacity_turnover_realism_gate.md`.
- Dedicated BT7 GitHub Actions workflow in `.github/workflows/bt7.yml`.
- Main CI step for `tests/test_bt7_capacity_turnover_realism_gate.py`.

### Tests Added / Updated
- `tests/test_bt7_capacity_turnover_realism_gate.py`.
- BT7 tests cover happy path, missing identity fields, missing and non-numeric metrics, non-positive scale, position ADV limits, portfolio ADV limits, daily turnover limits, annual turnover limits, transaction-cost drag, net expectancy floor, holding-period floor, trade-count floor, slippage-model coverage, missing artifact hashes, missing public-safe tags, missing research-only footer, JSON loading, report writing and Markdown rendering.

### Improved
- Historical evidence now has a deterministic capacity and turnover realism gate before any private production sizing work.
- BT7 blocks results that look attractive but require unrealistic liquidity usage, excessive turnover, excessive transaction-cost drag or incomplete slippage coverage.
- Generated BT7 reports remain research-only and do not authorize execution.

### Stabilization Result
- BT7 implementation status: done.
- BT7 local test status: 19 tests passing.
- BT7 CI status: green.
- Full regression status: green.
- Public demo capacity and turnover data remains synthetic/demo-only.
- Broker execution remains intentionally paper-only infrastructure.
- Live trading remains intentionally not authorized by code.

---

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
- BT6 implementation status: done.
- BT6 CI status: green.
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
