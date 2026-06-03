# W1 Entry/Exit Watcher Git Write Decoupling Closure — 2026-06-03

Status: implemented / CI-wired

## Scope

W1 removes branch mutation from the scheduled Entry/Exit Watcher workflow.

The watcher still runs, validates its signal input, sends notifications and preserves runtime output. The difference is that runtime output is now retained as GitHub Actions artifacts instead of being written back to the schedule branch.

This is workflow stability infrastructure only. It does not alter trading logic, does not authorize live trading and does not create broker execution capability.

## TEST1 workflow

```text
real watcher workflow inspected
guard test added first
watcher workflow changed to read-only repository access
runtime output changed to artifact upload
branch mutation removed from scheduled watcher path
documentation updated after implementation
```

## Implemented behavior

```text
entry-exit-watcher workflow uses read-only repository contents permission
checkout does not persist write credentials
watcher runtime output is uploaded as an artifact
watcher alert output is retained as an artifact
watcher signal output is retained as an artifact
watcher data output is retained as an artifact
watcher concurrency is isolated from shared repository writer workflows
scheduled watcher runs no longer mutate the schedule branch
```

## Files

```text
.github/workflows/entry-exit-watcher.yml
tests/test_w1_entry_exit_watcher_git_write_decoupling.py
```

## Guard coverage

```text
tests/test_w1_entry_exit_watcher_git_write_decoupling.py
```

Validated behavior:

```text
workflow does not request repository write permission
workflow does not contain branch-mutation commands
workflow uploads watcher runtime artifacts
workflow uses an isolated watcher concurrency group
```

## CI

```text
pytest tests/test_w1_entry_exit_watcher_git_write_decoupling.py -q
```

## Safety boundary

```text
Live trading authorization: not granted by code
Broker execution: paper_only
Capital allocation: not authorized
Production deployment: not authorized
```

W1 is a workflow reliability fix. It is not a strategy expansion and not evidence of live edge by itself.
