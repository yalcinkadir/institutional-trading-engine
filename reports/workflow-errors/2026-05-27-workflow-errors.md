# GitHub Actions Workflow Error Report

Generated: 2026-05-27 08:30 UTC
Repository: `yalcinkadir/institutional-trading-engine`
Filter since: 2026-05-26 08:30 UTC
Failed runs included: 1

## Daily Evidence Report

- Run ID: `26479777683`
- Branch: `main`
- Commit: `0a89c41d5866`
- Title: Daily Evidence Report
- Created: 2026-05-26T22:53:19Z
- Updated: 2026-05-26T22:53:42Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26479777683

### Failed job: Build daily evidence report

- Job ID: `77974142432`
- Started: 2026-05-26T22:53:21Z
- Completed: 2026-05-26T22:53:41Z
- Failed steps: 7. Persist daily observation sources

#### Error context

```text
2026-05-26T22:53:40.3274953Z - missing incoming source file: backtest_results.json
2026-05-26T22:53:40.3275333Z - missing incoming source file: forward_results.json
2026-05-26T22:53:40.3275718Z - missing incoming source file: regime_observations.json
2026-05-26T22:53:40.3276113Z - missing incoming source file: position_snapshots.json
2026-05-26T22:53:40.3368013Z ##[error]Process completed with exit code 1.
2026-05-26T22:53:40.3505842Z Post job cleanup.
2026-05-26T22:53:40.4542501Z [command]/usr/bin/git version
2026-05-26T22:53:40.4584828Z git version 2.54.0
2026-05-26T22:53:40.4629069Z Temporarily overriding HOME='/home/runner/work/_temp/3fd86859-d248-41fe-9589-8396f9f5fbaf' before making global git config changes
2026-05-26T22:53:40.4630790Z Adding repository directory to the temporary git global config as a safe directory
2026-05-26T22:53:40.4644944Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-05-26T22:53:40.4687603Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-05-26T22:53:40.4728059Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-05-26T22:53:40.5039938Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-05-26T22:53:40.5067585Z http.https://github.com/.extraheader
2026-05-26T22:53:40.5082204Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```
