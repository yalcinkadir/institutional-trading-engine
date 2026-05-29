# IP3 / IP4 Public Demo Defaults and Private Edge Boundary

IP3/IP4 formalizes the split between public framework defaults and private research edge.

## IP3: Public demo defaults

Public repository thresholds are demo defaults only. They are useful for CI, examples, deterministic tests and documentation, but they are not proprietary production edge.

Current public-demo threshold module:

```text
src/config/thresholds.py
```

The module marks its defaults with:

```text
PUBLIC_DEMO_DEFAULTS = True
THRESHOLDS_VERSION = public-demo-...
```

## IP4: Optional external edge provider

The public repo must work without private modules. Private thresholds can be supplied by setting:

```bash
export ITE_EXTERNAL_EDGE_PROVIDER="your_local_module.path"
```

That module must expose:

```python
def get_decision_thresholds() -> DecisionThresholds:
    ...
```

The public boundary resolver lives in:

```text
src/config/external_edge_provider.py
```

## Rules

- Public CI must pass without external modules.
- Public defaults must stay synthetic/demo-only.
- Private thresholds, real setup maps, real scoring weights and production sizing rules must not be committed to the public repository.
- External modules are optional imports only.
- Missing external modules must not break public-demo operation.

## Test command

```bash
pytest tests/test_external_edge_provider.py -q
```

## Related checks

```bash
python scripts/check_ip_boundary.py --root . --no-write
python scripts/validate_public_repo_policy.py --no-write
```
