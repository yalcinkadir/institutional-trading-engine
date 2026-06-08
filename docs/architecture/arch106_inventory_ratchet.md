# ARCH106 Inventory Ratchet

ARCH106 separates three different concepts that must not be collapsed:

1. **Static reachability** — a module can be imported from a script or workflow path.
2. **Runtime execution proof** — the relevant function or branch is executed by a representative runtime-path test or script.
3. **Architecture classification** — every module is either connected to runtime, explicitly test-only/experimental/quarantined, or a delete candidate.

Reachability is necessary but not sufficient. A module may be import-reachable but still never executed by the scheduled decision/report path.

## Guard command

```bash
python scripts/generate_module_inventory.py --check
python scripts/validate_arch106_ratchet.py
pytest tests/test_architecture_runtime_execution_guard.py \
  tests/test_arch106_signal_runtime_helper_proof.py \
  tests/test_arch106_ratchet_guard.py
```

## Current ratchet policy

The repository still carries legacy modules that were present before the full ARCH106 classification pass. These are grandfathered only as a bounded baseline.

The ratchet blocks:

- growth of `unclassified_legacy_modules` beyond `unclassified_legacy_baseline_limit`;
- production-connected modules without `runtime_entrypoint`;
- production-connected modules without `runtime_execution_proof`;
- demotion of known critical report/signal runtime modules out of `connected_runtime`;
- missing or stale committed inventory artifacts.

## What this does not do

This guard does not delete legacy modules. Deletion/quarantine is a separate, slower cleanup step because removing old modules can break hidden imports. The current objective is stronger: from this point forward, new architecture debt cannot enter silently.

## Promotion rule

A module may be promoted to `connected_runtime` only when it has both:

- a declared runtime entrypoint or workflow/script consumer;
- a representative runtime execution proof.

Without both, it must remain `test_only`, `experimental`, `quarantine`, or `delete_candidate`.
