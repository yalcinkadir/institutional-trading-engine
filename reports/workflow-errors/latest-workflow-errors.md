# GitHub Actions Workflow Error Report

Generated: 2026-05-20 20:50 UTC
Repository: `yalcinkadir/institutional-trading-engine`
Failed runs included: 4

## .github/workflows/entry-exit-watcher.yml

- Run ID: `26189143246`
- Branch: `main`
- Commit: `85bc5d865486`
- Title: Initialize workflow error reports directory
- Created: 2026-05-20T20:49:35Z
- Updated: 2026-05-20T20:49:35Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26189143246

- No failed jobs returned by API, although run concluded as failure.

## .github/workflows/entry-exit-watcher.yml

- Run ID: `26189058499`
- Branch: `main`
- Commit: `c91b6a909ac1`
- Title: Commit generated workflow error reports reliably
- Created: 2026-05-20T20:47:54Z
- Updated: 2026-05-20T20:47:54Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26189058499

- No failed jobs returned by API, although run concluded as failure.

## .github/workflows/entry-exit-watcher.yml

- Run ID: `26188808905`
- Branch: `main`
- Commit: `16426c335a63`
- Title: Fix workflow error report commit rebase handling
- Created: 2026-05-20T20:42:58Z
- Updated: 2026-05-20T20:42:58Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26188808905

- No failed jobs returned by API, although run concluded as failure.

## Workflow Error Report

- Run ID: `26188749416`
- Branch: `main`
- Commit: `996a346322e4`
- Title: Workflow Error Report
- Created: 2026-05-20T20:41:47Z
- Updated: 2026-05-20T20:42:05Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26188749416

### Failed job: Generate workflow error report

- Job ID: `77051237897`
- Started: 2026-05-20T20:41:51Z
- Completed: 2026-05-20T20:42:04Z
- Failed steps: 6. Commit workflow error report

#### Error context

```text
2026-05-20T20:42:01.5144341Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-05-20T20:42:01.5144656Z ##[endgroup]
2026-05-20T20:42:01.5369459Z error: cannot pull with rebase: Your index contains uncommitted changes.
2026-05-20T20:42:01.5370174Z error: Please commit or stash them.
2026-05-20T20:42:01.5385149Z ##[error]Process completed with exit code 128.
2026-05-20T20:42:01.5503462Z Post job cleanup.
2026-05-20T20:42:01.6501164Z [command]/usr/bin/git version
2026-05-20T20:42:01.6537987Z git version 2.54.0
2026-05-20T20:42:01.6584261Z Temporarily overriding HOME='/home/runner/work/_temp/cc0b4d02-ae92-477a-8a6f-9158d3b156ee' before making global git config changes
2026-05-20T20:42:01.6586038Z Adding repository directory to the temporary git global config as a safe directory
2026-05-20T20:42:01.6598257Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-05-20T20:42:01.6632505Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-05-20T20:42:01.6665866Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-05-20T20:42:01.6890940Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-05-20T20:42:01.6915447Z http.https://github.com/.extraheader
2026-05-20T20:42:01.6928653Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```
