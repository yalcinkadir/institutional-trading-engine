# CHANGELOG

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

### Added
- Daily evidence input contract validator in `src/validation/daily_evidence_input_validation.py`.
- Daily evidence input builder in `src/validation/daily_evidence_input_builder.py`.
- Observation-only source bootstrap in `src/validation/daily_evidence_source_bootstrap.py`.
- CLI tools:
  - `scripts/validate_daily_evidence_inputs.py`
  - `scripts/build_daily_evidence_inputs.py`
  - `scripts/bootstrap_daily_evidence_sources.py`
- Operational documentation:
  - `docs/operations/daily_evidence_input_pipeline.md`
  - `docs/operations/daily_evidence_input_builder.md`
  - `docs/operations/daily_evidence_source_bootstrap.md`

### Tests Added / Updated
- `tests/test_daily_evidence_input_validation.py`
- `tests/test_daily_evidence_input_builder.py`
- `tests/test_daily_evidence_source_bootstrap.py`
- CI workflow includes explicit Phase B11 input pipeline tests.

### Improved
- Daily Evidence workflow no longer uses placeholder component JSONs.
- Workflow now follows a full evidence chain:
  - source bootstrap when explicitly requested for observation-only Day-0 operation
  - input build
  - input validation
  - B1-B6 component report generation
  - daily evidence report generation
  - artifact upload
- Missing or invalid sources fail closed before evidence generation.
- Observation-only bootstrap records are marked as `observation_only_bootstrap` and are not treated as statistically meaningful forward evidence.

### Stabilization Result
- CI status: green.
- Daily Evidence workflow status: green with explicit observation-only bootstrap input.
- B11 status: done.
- B1.1 remains a long-running 3-6 month observation-only evidence period.
- Broker execution remains intentionally not implemented.
- Live trading remains intentionally not authorized by code.

---

## Phase B Real Forward Evidence — 2026-05-25

### Added
- Paper observation daily reconciliation model in `src/validation/paper_observation_reconciliation.py`.
- Performance drift detection engine in `src/validation/performance_drift_detection.py`.
- SPRT-style sequential edge-decay test in `src/validation/sequential_edge_decay.py`.
- Operational documentation:
  - `docs/operations/paper_observation_reconciliation.md`
  - `docs/operations/performance_drift_detection.md`
  - `docs/operations/sequential_edge_decay.md`
