# GitHub Actions Workflow Error Report

Generated: 2026-05-29 08:31 UTC
Repository: `yalcinkadir/institutional-trading-engine`
Filter since: 2026-05-28 08:31 UTC
Failed runs included: 1

## BT6 Evidence Baseline Regression Gate

- Run ID: `26625574700`
- Branch: `main`
- Commit: `d5406544842f`
- Title: Add BT6 CI workflow
- Created: 2026-05-29T07:58:49Z
- Updated: 2026-05-29T07:59:12Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26625574700

### Failed job: bt6

- Job ID: `78461368759`
- Started: 2026-05-29T07:58:51Z
- Completed: 2026-05-29T07:59:11Z
- Failed steps: 6. Generate BT6 demo report

#### Error context

```text
2026-05-29T07:59:08.0553435Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-05-29T07:59:08.0553826Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-05-29T07:59:08.0554222Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-05-29T07:59:08.0554701Z ##[endgroup]
2026-05-29T07:59:08.0811377Z Traceback (most recent call last):
2026-05-29T07:59:08.0821373Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_bt6_baseline_regression_report.py", line 8, in <module>
2026-05-29T07:59:08.0822853Z     from src.validation.evidence_baseline_regression_gate import (
2026-05-29T07:59:08.0823533Z ModuleNotFoundError: No module named 'src'
2026-05-29T07:59:08.0862247Z ##[error]Process completed with exit code 1.
2026-05-29T07:59:08.0978760Z Post job cleanup.
2026-05-29T07:59:08.1965638Z [command]/usr/bin/git version
2026-05-29T07:59:08.2002578Z git version 2.54.0
2026-05-29T07:59:08.2046234Z Temporarily overriding HOME='/home/runner/work/_temp/9d027261-7978-46d4-a0f0-dc96ef0056de' before making global git config changes
2026-05-29T07:59:08.2047574Z Adding repository directory to the temporary git global config as a safe directory
2026-05-29T07:59:08.2058996Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-05-29T07:59:08.2092226Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
```

```text
2026-05-29T07:59:08.0554701Z ##[endgroup]
2026-05-29T07:59:08.0811377Z Traceback (most recent call last):
2026-05-29T07:59:08.0821373Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_bt6_baseline_regression_report.py", line 8, in <module>
2026-05-29T07:59:08.0822853Z     from src.validation.evidence_baseline_regression_gate import (
2026-05-29T07:59:08.0823533Z ModuleNotFoundError: No module named 'src'
2026-05-29T07:59:08.0862247Z ##[error]Process completed with exit code 1.
2026-05-29T07:59:08.0978760Z Post job cleanup.
2026-05-29T07:59:08.1965638Z [command]/usr/bin/git version
2026-05-29T07:59:08.2002578Z git version 2.54.0
2026-05-29T07:59:08.2046234Z Temporarily overriding HOME='/home/runner/work/_temp/9d027261-7978-46d4-a0f0-dc96ef0056de' before making global git config changes
2026-05-29T07:59:08.2047574Z Adding repository directory to the temporary git global config as a safe directory
2026-05-29T07:59:08.2058996Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-05-29T07:59:08.2092226Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-05-29T07:59:08.2124019Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-05-29T07:59:08.2346552Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-05-29T07:59:08.2371323Z http.https://github.com/.extraheader
```

```text
2026-05-29T07:59:08.0811377Z Traceback (most recent call last):
2026-05-29T07:59:08.0821373Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_bt6_baseline_regression_report.py", line 8, in <module>
2026-05-29T07:59:08.0822853Z     from src.validation.evidence_baseline_regression_gate import (
2026-05-29T07:59:08.0823533Z ModuleNotFoundError: No module named 'src'
2026-05-29T07:59:08.0862247Z ##[error]Process completed with exit code 1.
2026-05-29T07:59:08.0978760Z Post job cleanup.
2026-05-29T07:59:08.1965638Z [command]/usr/bin/git version
2026-05-29T07:59:08.2002578Z git version 2.54.0
2026-05-29T07:59:08.2046234Z Temporarily overriding HOME='/home/runner/work/_temp/9d027261-7978-46d4-a0f0-dc96ef0056de' before making global git config changes
2026-05-29T07:59:08.2047574Z Adding repository directory to the temporary git global config as a safe directory
2026-05-29T07:59:08.2058996Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-05-29T07:59:08.2092226Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-05-29T07:59:08.2124019Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-05-29T07:59:08.2346552Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-05-29T07:59:08.2371323Z http.https://github.com/.extraheader
2026-05-29T07:59:08.2383758Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```
