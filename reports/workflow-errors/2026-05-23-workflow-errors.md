# GitHub Actions Workflow Error Report

Generated: 2026-05-23 07:58 UTC
Repository: `yalcinkadir/institutional-trading-engine`
Filter since: 2026-05-22 07:58 UTC
Failed runs included: 10

## Report Quality Validation

- Run ID: `26326678507`
- Branch: `main`
- Commit: `5014673f704a`
- Title: feat(validation): add out-of-sample validation CLI
- Created: 2026-05-23T07:14:58Z
- Updated: 2026-05-23T07:15:53Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26326678507

### Failed job: Commit validated reports

- Job ID: `77505642640`
- Started: 2026-05-23T07:15:44Z
- Completed: 2026-05-23T07:15:52Z
- Failed steps: 5. Commit validated reports

#### Error context

```text
2026-05-23T07:15:49.7993386Z hint: You can instead skip this commit: run "git rebase --skip".
2026-05-23T07:15:49.7994013Z hint: To abort and get back to the state before "git rebase", run "git rebase --abort".
2026-05-23T07:15:49.7994867Z hint: Disable this message with "git config set advice.mergeConflict false"
2026-05-23T07:15:49.7995488Z Could not apply 2647312... # Update validated reports 2026-05-23_07-15-49_UTC
2026-05-23T07:15:49.8015884Z ##[error]Process completed with exit code 1.
2026-05-23T07:15:49.8129260Z Post job cleanup.
2026-05-23T07:15:49.9096858Z [command]/usr/bin/git version
2026-05-23T07:15:49.9133116Z git version 2.54.0
2026-05-23T07:15:49.9178597Z Temporarily overriding HOME='/home/runner/work/_temp/a777d80d-5e09-4f85-acd7-d4df9fe11260' before making global git config changes
2026-05-23T07:15:49.9180105Z Adding repository directory to the temporary git global config as a safe directory
2026-05-23T07:15:49.9192878Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-05-23T07:15:49.9226543Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-05-23T07:15:49.9264469Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-05-23T07:15:49.9509438Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-05-23T07:15:49.9535508Z http.https://github.com/.extraheader
2026-05-23T07:15:49.9549976Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

## .github/workflows/weekly-expectancy-feedback.yml

- Run ID: `26326678240`
- Branch: `main`
- Commit: `5014673f704a`
- Title: feat(validation): add out-of-sample validation CLI
- Created: 2026-05-23T07:14:57Z
- Updated: 2026-05-23T07:14:57Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26326678240

- No failed jobs returned by API, although run concluded as failure.

## .github/workflows/entry-exit-watcher.yml

- Run ID: `26326678348`
- Branch: `main`
- Commit: `5014673f704a`
- Title: feat(validation): add out-of-sample validation CLI
- Created: 2026-05-23T07:14:57Z
- Updated: 2026-05-23T07:14:57Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26326678348

- No failed jobs returned by API, although run concluded as failure.

## .github/workflows/weekly-expectancy-feedback.yml

- Run ID: `26326670968`
- Branch: `main`
- Commit: `a03831d07082`
- Title: feat(validation): add historical reconstruction and oos validation
- Created: 2026-05-23T07:14:32Z
- Updated: 2026-05-23T07:14:32Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26326670968

- No failed jobs returned by API, although run concluded as failure.

## .github/workflows/entry-exit-watcher.yml

- Run ID: `26326670874`
- Branch: `main`
- Commit: `a03831d07082`
- Title: feat(validation): add historical reconstruction and oos validation
- Created: 2026-05-23T07:14:31Z
- Updated: 2026-05-23T07:14:31Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26326670874

- No failed jobs returned by API, although run concluded as failure.

## Report Quality Validation

- Run ID: `26326358213`
- Branch: `main`
- Commit: `592dacb155dd`
- Title: docs(readme): add historical backtest workflow
- Created: 2026-05-23T06:58:57Z
- Updated: 2026-05-23T07:00:12Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26326358213

### Failed job: Commit validated reports

- Job ID: `77504760662`
- Started: 2026-05-23T06:59:42Z
- Completed: 2026-05-23T07:00:12Z
- Failed steps: 2. Checkout repository

#### Error context

```text
2026-05-23T06:59:44.3975327Z [command]/usr/bin/git config --local http.https://github.com/.extraheader AUTHORIZATION: basic ***
2026-05-23T06:59:44.4020323Z ##[endgroup]
2026-05-23T06:59:44.4021045Z ##[group]Fetching the repository
2026-05-23T06:59:44.4029582Z [command]/usr/bin/git -c protocol.version=2 fetch --prune --no-recurse-submodules origin +refs/heads/*:refs/remotes/origin/* +refs/tags/*:refs/tags/*
2026-05-23T06:59:44.4767126Z ##[error]fatal: could not read Username for 'https://github.com': terminal prompts disabled
2026-05-23T06:59:44.4776015Z The process '/usr/bin/git' failed with exit code 128
2026-05-23T06:59:44.4776692Z Waiting 11 seconds before trying again
2026-05-23T06:59:55.4786460Z [command]/usr/bin/git -c protocol.version=2 fetch --prune --no-recurse-submodules origin +refs/heads/*:refs/remotes/origin/* +refs/tags/*:refs/tags/*
2026-05-23T06:59:55.5426746Z ##[error]fatal: could not read Username for 'https://github.com': terminal prompts disabled
2026-05-23T06:59:55.5443688Z The process '/usr/bin/git' failed with exit code 128
2026-05-23T06:59:55.5444188Z Waiting 15 seconds before trying again
2026-05-23T07:00:10.5495360Z [command]/usr/bin/git -c protocol.version=2 fetch --prune --no-recurse-submodules origin +refs/heads/*:refs/remotes/origin/* +refs/tags/*:refs/tags/*
2026-05-23T07:00:10.6157993Z ##[error]fatal: could not read Username for 'https://github.com': terminal prompts disabled
2026-05-23T07:00:10.6211832Z ##[error]The process '/usr/bin/git' failed with exit code 128
2026-05-23T07:00:10.6413146Z Post job cleanup.
2026-05-23T07:00:10.7370300Z [command]/usr/bin/git version
```

```text
2026-05-23T06:59:44.4767126Z ##[error]fatal: could not read Username for 'https://github.com': terminal prompts disabled
2026-05-23T06:59:44.4776015Z The process '/usr/bin/git' failed with exit code 128
2026-05-23T06:59:44.4776692Z Waiting 11 seconds before trying again
2026-05-23T06:59:55.4786460Z [command]/usr/bin/git -c protocol.version=2 fetch --prune --no-recurse-submodules origin +refs/heads/*:refs/remotes/origin/* +refs/tags/*:refs/tags/*
2026-05-23T06:59:55.5426746Z ##[error]fatal: could not read Username for 'https://github.com': terminal prompts disabled
2026-05-23T06:59:55.5443688Z The process '/usr/bin/git' failed with exit code 128
2026-05-23T06:59:55.5444188Z Waiting 15 seconds before trying again
2026-05-23T07:00:10.5495360Z [command]/usr/bin/git -c protocol.version=2 fetch --prune --no-recurse-submodules origin +refs/heads/*:refs/remotes/origin/* +refs/tags/*:refs/tags/*
2026-05-23T07:00:10.6157993Z ##[error]fatal: could not read Username for 'https://github.com': terminal prompts disabled
2026-05-23T07:00:10.6211832Z ##[error]The process '/usr/bin/git' failed with exit code 128
2026-05-23T07:00:10.6413146Z Post job cleanup.
2026-05-23T07:00:10.7370300Z [command]/usr/bin/git version
2026-05-23T07:00:10.7405831Z git version 2.54.0
2026-05-23T07:00:10.7446140Z Temporarily overriding HOME='/home/runner/work/_temp/5377bf16-9b56-4922-84cd-00d34855dda2' before making global git config changes
2026-05-23T07:00:10.7447036Z Adding repository directory to the temporary git global config as a safe directory
2026-05-23T07:00:10.7452101Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
```

```text
2026-05-23T06:59:55.5426746Z ##[error]fatal: could not read Username for 'https://github.com': terminal prompts disabled
2026-05-23T06:59:55.5443688Z The process '/usr/bin/git' failed with exit code 128
2026-05-23T06:59:55.5444188Z Waiting 15 seconds before trying again
2026-05-23T07:00:10.5495360Z [command]/usr/bin/git -c protocol.version=2 fetch --prune --no-recurse-submodules origin +refs/heads/*:refs/remotes/origin/* +refs/tags/*:refs/tags/*
2026-05-23T07:00:10.6157993Z ##[error]fatal: could not read Username for 'https://github.com': terminal prompts disabled
2026-05-23T07:00:10.6211832Z ##[error]The process '/usr/bin/git' failed with exit code 128
2026-05-23T07:00:10.6413146Z Post job cleanup.
2026-05-23T07:00:10.7370300Z [command]/usr/bin/git version
2026-05-23T07:00:10.7405831Z git version 2.54.0
2026-05-23T07:00:10.7446140Z Temporarily overriding HOME='/home/runner/work/_temp/5377bf16-9b56-4922-84cd-00d34855dda2' before making global git config changes
2026-05-23T07:00:10.7447036Z Adding repository directory to the temporary git global config as a safe directory
2026-05-23T07:00:10.7452101Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-05-23T07:00:10.7486573Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-05-23T07:00:10.7518852Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-05-23T07:00:10.7749878Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-05-23T07:00:10.7773233Z http.https://github.com/.extraheader
```

```text
2026-05-23T06:59:55.5443688Z The process '/usr/bin/git' failed with exit code 128
2026-05-23T06:59:55.5444188Z Waiting 15 seconds before trying again
2026-05-23T07:00:10.5495360Z [command]/usr/bin/git -c protocol.version=2 fetch --prune --no-recurse-submodules origin +refs/heads/*:refs/remotes/origin/* +refs/tags/*:refs/tags/*
2026-05-23T07:00:10.6157993Z ##[error]fatal: could not read Username for 'https://github.com': terminal prompts disabled
2026-05-23T07:00:10.6211832Z ##[error]The process '/usr/bin/git' failed with exit code 128
2026-05-23T07:00:10.6413146Z Post job cleanup.
2026-05-23T07:00:10.7370300Z [command]/usr/bin/git version
2026-05-23T07:00:10.7405831Z git version 2.54.0
2026-05-23T07:00:10.7446140Z Temporarily overriding HOME='/home/runner/work/_temp/5377bf16-9b56-4922-84cd-00d34855dda2' before making global git config changes
2026-05-23T07:00:10.7447036Z Adding repository directory to the temporary git global config as a safe directory
2026-05-23T07:00:10.7452101Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-05-23T07:00:10.7486573Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-05-23T07:00:10.7518852Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-05-23T07:00:10.7749878Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-05-23T07:00:10.7773233Z http.https://github.com/.extraheader
2026-05-23T07:00:10.7785096Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

## .github/workflows/entry-exit-watcher.yml

- Run ID: `26326355209`
- Branch: `main`
- Commit: `592dacb155dd`
- Title: docs(readme): add historical backtest workflow
- Created: 2026-05-23T06:58:46Z
- Updated: 2026-05-23T06:58:46Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26326355209

- No failed jobs returned by API, although run concluded as failure.

## .github/workflows/entry-exit-watcher.yml

- Run ID: `26326273654`
- Branch: `main`
- Commit: `7c7e53d4b997`
- Title: docs(backtest): document historical backtest workflow
- Created: 2026-05-23T06:54:34Z
- Updated: 2026-05-23T06:54:34Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26326273654

- No failed jobs returned by API, although run concluded as failure.

## .github/workflows/weekly-expectancy-feedback.yml

- Run ID: `26326273748`
- Branch: `main`
- Commit: `7c7e53d4b997`
- Title: docs(backtest): document historical backtest workflow
- Created: 2026-05-23T06:54:34Z
- Updated: 2026-05-23T06:54:34Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26326273748

- No failed jobs returned by API, although run concluded as failure.

## Report Quality Validation

- Run ID: `26326247508`
- Branch: `main`
- Commit: `1d589cbe25e9`
- Title: ci(backtest): add historical entry exit backtest workflow
- Created: 2026-05-23T06:53:11Z
- Updated: 2026-05-23T06:53:56Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26326247508

### Failed job: Commit validated reports

- Job ID: `77504443627`
- Started: 2026-05-23T06:53:50Z
- Completed: 2026-05-23T06:53:55Z
- Failed steps: 5. Commit validated reports

#### Error context

```text
2026-05-23T06:53:54.1624376Z hint: You can instead skip this commit: run "git rebase --skip".
2026-05-23T06:53:54.1627445Z hint: To abort and get back to the state before "git rebase", run "git rebase --abort".
2026-05-23T06:53:54.1630829Z hint: Disable this message with "git config set advice.mergeConflict false"
2026-05-23T06:53:54.1633216Z Could not apply bc9564a... # Update validated reports 2026-05-23_06-53-53_UTC
2026-05-23T06:53:54.1645976Z ##[error]Process completed with exit code 1.
2026-05-23T06:53:54.1863309Z Post job cleanup.
2026-05-23T06:53:54.2868424Z [command]/usr/bin/git version
2026-05-23T06:53:54.2905135Z git version 2.54.0
2026-05-23T06:53:54.2950195Z Temporarily overriding HOME='/home/runner/work/_temp/a7af92eb-11de-4123-8486-9392cc1907f1' before making global git config changes
2026-05-23T06:53:54.2953519Z Adding repository directory to the temporary git global config as a safe directory
2026-05-23T06:53:54.2964675Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-05-23T06:53:54.2998725Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-05-23T06:53:54.3033992Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-05-23T06:53:54.3258563Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-05-23T06:53:54.3284356Z http.https://github.com/.extraheader
2026-05-23T06:53:54.3299669Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```
