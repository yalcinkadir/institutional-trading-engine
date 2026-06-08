# CI-Truthful Status Claims Policy

This policy exists to keep ROADMAP, CHANGELOG and README status language audit-safe.

## Rule

Documentation must not claim that the repository, main branch, full regression suite or production/report pipeline is green unless the claim is tied to concrete evidence.

Acceptable evidence includes at least one of:

- a successful GitHub Actions run URL
- a successful GitHub Actions job URL
- a commit SHA whose checks are known green
- a committed evidence artifact path
- an explicit note that the claim is scoped to targeted tests only

## Status language

Use explicit status language:

- `implemented`
- `tests added`
- `CI green on main: <run/job URL or commit SHA>`
- `CI pending`
- `blocked`
- `scoped feature-level CI-green: <feature/test evidence>`

## Forbidden without evidence

These are not allowed unless the same line or nearby evidence block provides a run, job, commit SHA or artifact reference:

- `CI is green`
- `Full regression green`
- `main is green`
- `production is green`
- `all workflows green`
- `report pipeline green`

## Feature-level historical labels

Feature tables may use scoped labels such as `Done / CI-green` only as feature-level historical status. They must not be read as a current full-regression or main-branch claim.

When a document needs to claim current repository health, it must use the stronger form:

`CI green on main: <successful run/job URL or commit SHA>`

## Single-test success is not full-regression success

A targeted test passing proves only the guarded behavior for that test scope. It is not equivalent to a full regression suite passing.

A safe completion sequence is:

1. implementation committed
2. guard tests added
3. targeted tests pass
4. full regression passes
5. CI run/job evidence is recorded
6. documentation is updated

## Live trading boundary

No CI-green documentation claim authorizes live trading, broker execution, capital allocation or production deployment.
