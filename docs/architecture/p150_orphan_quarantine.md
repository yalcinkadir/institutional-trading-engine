# P150 Orphan Quarantine Boundary

P150 is a controlled quarantine step for modules that are classified as true orphans by static reachability analysis.

## Rule

A module may enter the P150 quarantine manifest only when it is absent from all three reachability sets:

1. scheduled production closure
2. all scripts closure
3. tests closure

This means the module is imported by no script and no test at the time of analysis.

## Non-goal

P150 does not process test/dispatch-only modules. Those modules may be outside the scheduled production path, but they are still exercised by tests or manual/dispatch scripts. They require a separate review path.

## Current action

The current P150 wave parks the initial true-orphan candidates in `docs/architecture/p150_orphan_quarantine_manifest.json`.

Decision value:

- `parked_pending_full_regression_after_removal`

This means the modules are not deleted in this wave. Physical removal or movement requires a later quarantine branch and a green full regression run after the removal.

## Validation

Run:

```bash
python tools/module_reachability.py --json module_reachability.baseline.json
python scripts/validate_p150_orphan_quarantine.py
pytest tests/test_p150_orphan_quarantine_guard.py
```

## Safety principle

Static reachability is necessary but not sufficient for runtime execution proof. P150 only identifies the safest cleanup candidates. It does not prove trading-path correctness and it must not be used to justify deleting test/dispatch-only modules.
