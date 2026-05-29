# EV Evidence Consolidation + Full-Suite Stability Review

Status date: 2026-05-29

## Purpose

This document consolidates the EV finding remediation work into one reviewable evidence map. It links each assessment finding to implementation status, regression coverage, and CI coverage.

## Consolidated status

```text
EV1: done / CI-green
EV2: done / CI-green
EV3: done / CI-green
EV4: done / CI-green
EV5: done / CI-green
EV6: done / CI-green
EV7: done / CI-green
EV8: done / CI-green
EV9: done / CI-green
EV10: done / CI-green
EV11: done / CI-green
EV12: done / CI-green
```

## Evidence matrix

| Finding | Remediation area | Primary code/test evidence | CI status |
|---|---|---|---|
| EV1 | Per-trade Sharpe definition | `src/validation/historical_edge_validation.py`, `tests/test_sharpe_definition_regression.py` | CI-green |
| EV2 | Deflated Sharpe input unit | `src/validation/historical_edge_validation.py`, `tests/test_sharpe_definition_regression.py` | CI-green |
| EV3 | Explicit backtest stop model | `src/backtesting/historical_entry_exit_backtest.py`, `tests/test_backtest_fidelity_ev3_ev6.py` | CI-green |
| EV4 | Breakeven after Target 1 | `src/backtesting/historical_entry_exit_backtest.py`, `tests/test_backtest_fidelity_ev3_ev6.py` | CI-green |
| EV5 | Stop gap fill realism | `src/backtesting/historical_entry_exit_backtest.py`, `tests/test_backtest_fidelity_ev3_ev6.py` | CI-green |
| EV6 | Target-1-only exit date | `src/backtesting/historical_entry_exit_backtest.py`, `tests/test_backtest_fidelity_ev3_ev6.py` | CI-green |
| EV7 | Tier-aware decision ranking | `src/decision_engine.py`, `tests/test_decision_engine.py` | CI-green |
| EV8 | Fixed-date holdout semantics | `src/validation/out_of_sample_lockbox.py`, `tests/test_out_of_sample_lockbox.py` | CI-green |
| EV9 | Drawdown threshold reporting | `src/validation/historical_edge_validation.py`, `tests/test_sharpe_definition_regression.py` | CI-green |
| EV10 | Profit-factor infinity handling | `src/validation/historical_edge_validation.py`, `tests/test_historical_edge_validation.py` | CI-green |
| EV11 | Conservative setup scoring fallback | `src/setup_scoring.py`, `tests/test_setup_scoring.py` | CI-green |
| EV12 | Drawdown magnitude governance | `src/validation/execution_kill_switch.py`, `tests/test_ev12_drawdown_magnitude.py` | CI-green |

## Dedicated CI steps

The main CI workflow contains dedicated targeted regression steps for:

```text
EV1-EV2 Sharpe definition regression tests
EV3-EV6 backtest fidelity tests
EV7 decision ranking regression tests
EV8 fixed-date holdout semantics regression tests
EV10 profit-factor infinity regression tests
EV11 conservative setup scoring regression tests
EV12 drawdown magnitude regression tests
```

EV9 is covered in the EV1-EV2 historical-edge validation regression group because it is part of the same drawdown threshold reporting and historical-edge validation surface.

## Full-suite stability review

The workflow still includes the full regression suite:

```text
pytest -q --ignore=tests/test_artifact_hygiene.py -k "not test_decision_log_path_not_in_gitignore"
```

The full-suite step acts as the integration guard after the targeted EV checks.

## Review notes

- The EV fixes are now represented in source code, regression tests, CI workflow steps, and this consolidated evidence map.
- The current evidence state is suitable for continued paper-observation and stability tracking.
- Future changes to any EV-related module should preserve the targeted regression step and update this matrix if the ownership file changes.

## Recommended next step

Move from EV remediation into a hardening pass focused on:

```text
1. full-suite flake review
2. CI runtime simplification
3. evidence artifact index consistency
4. roadmap cleanup for completed EV items
```
