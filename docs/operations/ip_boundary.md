# IP1 Public / Private Edge Boundary

IP1 adds a conservative repository hygiene gate that separates public-safe framework artefacts from likely private-edge material.

## Purpose

The scanner helps prevent accidental publication of:

- private edge indicators
- proprietary setup names
- secret threshold terminology
- live/production threshold assignments
- alpha-weight style parameter leaks

It is not a legal IP classifier. It is a deterministic CI/PR guardrail.

## Inputs

Default policy file:

```text
.ip-boundary.yml
```

The policy contains:

- public-safe paths
- ignored/private paths
- forbidden terms
- suspicious regex patterns

## CLI

```bash
python scripts/check_ip_boundary.py --root .
```

Optional outputs:

```bash
python scripts/check_ip_boundary.py \
  --root . \
  --json-output reports/ip-boundary-report.json \
  --markdown-output reports/ip-boundary-report.md
```

Use `--no-write` for a pure check:

```bash
python scripts/check_ip_boundary.py --root . --no-write
```

## Status semantics

| Status | Meaning |
|---|---|
| PASS | No private-edge indicators detected |
| WARN | Suspicious edge-like pattern detected |
| FAIL | Forbidden private-edge term detected |

## Design boundaries

IP1 is intentionally conservative:

- It scans text artefacts only.
- It ignores `private/`, `data/private/`, `reports/`, caches and virtual environments.
- It does not inspect secrets managers.
- It does not execute trading logic.
- It does not authorize publication.

## Recommended CI usage

Run the scanner on pull requests before merge:

```bash
python scripts/check_ip_boundary.py --root . --no-write
```

A failure should block the PR until the finding is removed, renamed, or moved into an intentionally private path.

## Public-safe principle

The public repository should expose:

- architecture
- deterministic validation engines
- audit/reporting logic
- tests and documentation
- paper-only execution controls

Private repositories or private configuration should contain:

- real alpha weights
- proprietary setup rankings
- production thresholds
- live signal parameters
- confidential model factors
