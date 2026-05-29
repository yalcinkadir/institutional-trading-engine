# IP9 / IP10 Public Repository Governance

IP9/IP10 closes the immediate public-repository governance gap before new strategy complexity is added.

## IP9: PR edge-constant review

Every pull request that touches strategy, scoring, thresholds, setup maps, exit profiles, ranking, reports, evidence, execution, sizing or CI gates must pass an explicit public-edge review before merge.

The PR checklist lives in:

```text
.github/pull_request_template.md
```

Required review outcome:

- no proprietary thresholds, setup maps, scoring weights, exit profiles or production-like parameters in public code
- strategy-like public values are marked as demo defaults or synthetic fixtures
- research/private configuration belongs behind the external/private boundary
- generated reports, raw evidence and ranked opportunity output are not committed
- research-only and no-live-trading language remains intact

## IP10: License and usage disclaimer

The public repository now includes:

```text
LICENSE
DISCLAIMER.md
```

The disclaimer makes the repository scope explicit:

- research and decision support only
- no financial advice
- paper observation only
- public demo defaults only
- no performance guarantee
- no live trading permission

## Required checks

```bash
pytest tests/test_ip9_ip10_public_repo_governance.py -q
python scripts/check_ip_boundary.py --root . --no-write
pytest tests/test_ip_boundary.py -q
python scripts/validate_public_repo_policy.py --no-write
```

## CI wiring

IP9/IP10 has a dedicated GitHub Actions governance workflow and is also suitable for inclusion in the main CI gate.

## Non-goals

IP9/IP10 does not prove trading edge, certify legal protection, authorize live execution or replace professional legal/compliance review.
