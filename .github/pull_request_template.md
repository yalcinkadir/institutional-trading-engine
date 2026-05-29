# Pull Request

## Summary

- 

## Validation

- [ ] Tests added or updated where behavior changed
- [ ] Relevant targeted tests pass locally
- [ ] Full regression is green or any exception is documented

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
