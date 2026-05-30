# Evidence Artifact Index

Status date: 2026-05-29

## Purpose

This index makes the repository evidence trail discoverable without manually searching for completion documents, policy documents, CI-green notes and guard tests.

## Current stabilization evidence

| Area | Evidence document | Guard test | Status |
|---|---|---|---|
| EV1-EV12 evidence consolidation | `docs/operations/ev_evidence_consolidation_full_suite_review.md` | `tests/test_ev_evidence_consolidation.py` | Done / CI-green |
| EV evidence consolidation completion | `docs/operations/ev_evidence_consolidation_ci_green_completion.md` | `tests/test_ev_evidence_consolidation.py` | Done / CI-green |
| Roadmap EV completion cleanup | `ROADMAP.md` | `tests/test_roadmap_ev_completion_guard.py` | Done / CI-green |
| Full-suite flake review | `docs/operations/full_suite_flake_review.md` | `tests/test_full_suite_flake_review_policy.py` | Done / CI-green |
| CI runtime simplification | `.github/workflows/ci.yml` | `tests/test_full_suite_flake_review_policy.py` | Done / CI-green |

## Core EV regression evidence

| Area | Primary test evidence | Status |
|---|---|---|
| EV1-EV2 Sharpe / Deflated Sharpe unit correction | `tests/test_sharpe_definition_regression.py` | Done / CI-green |
| EV3-EV6 backtest fidelity | `tests/test_backtest_fidelity_ev3_ev6.py` | Done / CI-green |
| EV7 decision ranking | `tests/test_decision_engine.py` | Done / CI-green |
| EV8 fixed-date holdout semantics | `tests/test_out_of_sample_lockbox.py` | Done / CI-green |
| EV9 drawdown threshold reporting | `tests/test_historical_edge_validation.py` | Done / CI-green |
| EV10 profit-factor infinity handling | `tests/test_historical_edge_validation.py` | Done / CI-green |
| EV11 conservative setup scoring | `tests/test_setup_scoring.py` | Done / CI-green |
| EV12 drawdown magnitude governance | `tests/test_ev12_drawdown_magnitude.py` | Done / CI-green |

## Runtime and governance evidence

| Area | Primary test evidence | Status |
|---|---|---|
| GOV1-GOV3 runtime governance | `tests/test_live_runtime_cycle.py`, `tests/test_portfolio_state.py`, `tests/test_entry_quality.py`, `tests/test_stop_loss_quality.py` | Done / CI-green |
| GOV4-GOV6 runtime stability | `tests/test_negative_override.py`, `tests/test_runtime_state.py`, `tests/test_runtime_loop.py` | Done / CI-green |
| GOV7-GOV10 pre-live hygiene | `tests/test_gov7_gov10_pre_live_hygiene.py` | Done / CI-green |
| Report output boundary | `tests/test_report_output_boundary.py`, `tests/test_generate_report_output_boundary.py` | Done / CI-green |
| BT7 capacity / turnover realism | `tests/test_bt7_capacity_turnover_realism_gate.py` | Done / CI-green |

## Required maintenance rule

Whenever a new CI-green completion document, evidence policy, or guard test is added, this index must be updated in the same change set or protected by a follow-up guard.

## Next recommended action

Add an index guard test that verifies this file links to the current stabilization documents and guard tests.
