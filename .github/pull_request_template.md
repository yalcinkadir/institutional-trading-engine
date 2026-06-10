# Pull Request

## Summary

- 

## Validation

- [ ] Tests added or updated where behavior changed
- [ ] Relevant targeted tests pass locally
- [ ] Full regression is green or any exception is documented

## TEST1 Operational Stability Decision Gate

Every PR that touches Paper Observation, Backtesting, evidence generation, report generation, signal persistence, outcome tracking, risk/governance gates or CI workflows must answer this before merge:

- [ ] I decided whether the correct outcome is `PASS`, `BLOCKED`, `DEGRADED` or `FAILED`.
- [ ] Expected missing/invalid inputs produce reviewable `BLOCKED` or `DEGRADED` artifacts instead of fake metrics or unnecessary workflow crashes.
- [ ] Hard-fail is used only where continuing would persist unsafe actionable data, corrupt evidence/state, or create misleading executable signals.
- [ ] The artifact/log includes explicit reason codes for blocked/degraded states.
- [ ] Backtesting and Paper Observation remain operationally stable where safe.
- [ ] Guard tests cover the dangerous path and the operational-stability behavior.
- [ ] Documentation was updated when the evidence/status semantics changed.

## Logic Safety Governance

Every PR that touches scanner, signals, quality engines, regime, risk, validator, watcher, reporting, backtesting, outcome tracking, evidence generation, status claims or CI gates must map the change to system invariants before merge:

- [ ] New or changed logic maps to affected System Invariants from `docs/architecture/system-invariants.md`.
- [ ] P0/P1 invariant violations are covered by guard or contract tests.
- [ ] `DEGRADED` states have explicit forbidden claims and cannot behave like `PASS`.
- [ ] Evidence output includes `run_id`, `data_mode`, checksum/provenance and runtime trace when applicable.
- [ ] CI evidence gate result is attached, linked or represented by a concrete validation command.

Affected invariants:
- SI-___

Evidence / test command:
- `...`

## IP9 Public Edge Review

Every PR that touches strategy, scoring, thresholds, setup maps, exit profiles, ranking, reports, evidence, execution, sizing or CI gates must answer the following before merge:

- [ ] No proprietary thresholds, setup maps, scoring weights, exit profiles or production-like parameters are added to public code.
- [ ] Any strategy-like values are clearly marked as public-demo defaults or synthetic fixtures.
- [ ] Any private/research edge belongs behind an external/private boundary, not in the public repository.
- [ ] Generated reports, raw evidence, provider extracts, ranked opportunity output and local artifacts are not committed.
- [ ] No provider or broker access material is included.
- [ ] Research/paper-only and no-live-trading language remains intact.
- [ ] `python scripts/check_ip_boundary.py --root . --no-write` passes when relevant.
- [ ] `pytest tests/test_ip9_ip10_public_repo_governance.py -q` passes.

If any checkbox cannot be honestly satisfied, block the PR until the content is removed, made synthetic, or moved behind the private-edge boundary.
