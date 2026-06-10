# GitHub Actions Workflow Error Report

Generated: 2026-06-10 08:34 UTC
Repository: `yalcinkadir/institutional-trading-engine`
Filter since: 2026-06-09 08:34 UTC
Failed runs included: 9

## Report Quality Validation

- Run ID: `27263622164`
- Branch: `main`
- Commit: `c2874bd8f882`
- Title: Wire BT133 entry confirmation reports into BT131 evidence workflow
- Created: 2026-06-10T08:30:38Z
- Updated: 2026-06-10T08:31:39Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27263622164

### Failed job: validate-reports (postmarket)

- Job ID: `80515199889`
- Started: 2026-06-10T08:30:40Z
- Completed: 2026-06-10T08:31:38Z
- Failed steps: 6. Validate report quality

#### Error context

```text
2026-06-10T08:31:36.5008893Z - Report used fallback data; content is structurally valid but not analytically strong
2026-06-10T08:31:36.5009285Z 
2026-06-10T08:31:36.5009372Z Errors:
2026-06-10T08:31:36.5009595Z - Missing analytical term: Risk Tier
2026-06-10T08:31:36.5077997Z ##[error]Process completed with exit code 1.
2026-06-10T08:31:36.5156347Z ##[group]Run actions/upload-artifact@v4
2026-06-10T08:31:36.5156652Z with:
2026-06-10T08:31:36.5156887Z   name: validated-postmarket-report
2026-06-10T08:31:36.5157224Z   path: reports/generated/postmarket-report.md
2026-06-10T08:31:36.5157538Z   retention-days: 14
2026-06-10T08:31:36.5157780Z   if-no-files-found: warn
2026-06-10T08:31:36.5158033Z   compression-level: 6
2026-06-10T08:31:36.5158266Z   overwrite: false
2026-06-10T08:31:36.5158508Z   include-hidden-files: false
2026-06-10T08:31:36.5158759Z env:
2026-06-10T08:31:36.5159100Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (premarket)

- Job ID: `80515200075`
- Started: 2026-06-10T08:30:40Z
- Completed: 2026-06-10T08:31:37Z
- Failed steps: 6. Validate report quality

#### Error context

```text
2026-06-10T08:31:35.6571634Z - Report used fallback data; content is structurally valid but not analytically strong
2026-06-10T08:31:35.6572413Z 
2026-06-10T08:31:35.6572535Z Errors:
2026-06-10T08:31:35.6572852Z - Missing analytical term: Risk Tier
2026-06-10T08:31:35.6647804Z ##[error]Process completed with exit code 1.
2026-06-10T08:31:35.6725466Z ##[group]Run actions/upload-artifact@v4
2026-06-10T08:31:35.6725767Z with:
2026-06-10T08:31:35.6726002Z   name: validated-premarket-report
2026-06-10T08:31:35.6726322Z   path: reports/generated/premarket-report.md
2026-06-10T08:31:35.6726632Z   retention-days: 14
2026-06-10T08:31:35.6726874Z   if-no-files-found: warn
2026-06-10T08:31:35.6727130Z   compression-level: 6
2026-06-10T08:31:35.6727364Z   overwrite: false
2026-06-10T08:31:35.6727606Z   include-hidden-files: false
2026-06-10T08:31:35.6727855Z env:
2026-06-10T08:31:35.6728184Z   POLYGON_API_KEY: ***
```

## Decision Engine Tests

- Run ID: `27263622099`
- Branch: `main`
- Commit: `c2874bd8f882`
- Title: Wire BT133 entry confirmation reports into BT131 evidence workflow
- Created: 2026-06-10T08:30:38Z
- Updated: 2026-06-10T08:31:24Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27263622099

### Failed job: tests

- Job ID: `80515199195`
- Started: 2026-06-10T08:30:41Z
- Completed: 2026-06-10T08:31:23Z
- Failed steps: 5. Run pytest

#### Error context

```text
2026-06-10T08:31:21.6863480Z ........................................................................ [ 90%]
2026-06-10T08:31:21.9383313Z ........................................................................ [ 94%]
2026-06-10T08:31:21.9850451Z ........................................................................ [ 98%]
2026-06-10T08:31:22.0721867Z ....................................                                     [100%]
2026-06-10T08:31:22.0723858Z =================================== FAILURES ===================================
2026-06-10T08:31:22.0724749Z ___ test_bt131_workflow_persists_validated_reports_to_repo_without_telegram ____
2026-06-10T08:31:22.0725352Z 
2026-06-10T08:31:22.0725856Z     def test_bt131_workflow_persists_validated_reports_to_repo_without_telegram() -> None:
2026-06-10T08:31:22.0726631Z         text = _workflow_text()
2026-06-10T08:31:22.0727014Z     
2026-06-10T08:31:22.0727831Z         assert "Persist validated backtest reports to repository" in text
2026-06-10T08:31:22.0728634Z         assert "reports/backtests/real_data/runs/${GITHUB_RUN_ID_VALUE}" in text
2026-06-10T08:31:22.0729334Z         assert "reports/backtests/real_data/latest" in text
2026-06-10T08:31:22.0729955Z         assert "reports/backtests/real_data/index.json" in text
2026-06-10T08:31:22.0730873Z         assert "bt132-strategy-improvement-report.json" in text
2026-06-10T08:31:22.0731536Z         assert "bt132-strategy-improvement-report.md" in text
```

```text
2026-06-10T08:31:22.0733586Z         assert "git add reports/backtests/real_data/" in text
2026-06-10T08:31:22.0734284Z >       assert "git commit -m \"Persist BT131/BT132 real-data backtest reports" in text
2026-06-10T08:31:22.0736258Z E       assert 'git commit -m "Persist BT131/BT132 real-data backtest reports' in 'name: BT131 Real Data Backtest Evidence\n\non:\n  workflow_dispatch:\n    inputs:\n      symbols:\n        descriptio...json\n            data/trade_plans/*manifest*.json\n          if-no-files-found: error\n          retention-days: 90\n'
2026-06-10T08:31:22.0737842Z 
2026-06-10T08:31:22.0738171Z tests/test_bt131_real_data_backtest_evidence_workflow.py:120: AssertionError
2026-06-10T08:31:22.0738966Z _______________ test_bt133_flags_oos_degradation_as_overfit_risk _______________
2026-06-10T08:31:22.0739413Z 
2026-06-10T08:31:22.0739796Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-0/test_bt133_flags_oos_degradati0')
2026-06-10T08:31:22.0740507Z 
2026-06-10T08:31:22.0740851Z     def test_bt133_flags_oos_degradation_as_overfit_risk(tmp_path: Path) -> None:
2026-06-10T08:31:22.0741487Z         path = _evidence(tmp_path)
2026-06-10T08:31:22.0741972Z         payload = json.loads(path.read_text(encoding="utf-8"))
2026-06-10T08:31:22.0742500Z         payload["results"] = [
2026-06-10T08:31:22.0743136Z             _row("s1", "2024-01-01", r_multiple=-1.0, false_breakout=True, stop_hit=True, mfe=0.2, mae=-1.1),
2026-06-10T08:31:22.0744198Z             _row("s2", "2024-02-01", r_multiple=2.0, false_breakout=False, stop_hit=False, mfe=1.5, mae=-0.2),
2026-06-10T08:31:22.0745164Z             _row("s3", "2024-03-01", r_multiple=1.5, false_breakout=False, stop_hit=False, mfe=1.2, mae=-0.3),
```

```text
2026-06-10T08:31:22.0750844Z >       assert any(item.recommendation == "OVERFIT_RISK" for item in report.variant_results)
2026-06-10T08:31:22.0751539Z E       assert False
2026-06-10T08:31:22.0752319Z E        +  where False = any(<generator object test_bt133_flags_oos_degradation_as_overfit_risk.<locals>.<genexpr> at 0x7f797b830380>)
2026-06-10T08:31:22.0753279Z 
2026-06-10T08:31:22.0753558Z tests/test_bt133_entry_confirmation_variants.py:167: AssertionError
2026-06-10T08:31:22.0754209Z =========================== short test summary info ============================
2026-06-10T08:31:22.0757012Z FAILED tests/test_bt131_real_data_backtest_evidence_workflow.py::test_bt131_workflow_persists_validated_reports_to_repo_without_telegram - assert 'git commit -m "Persist BT131/BT132 real-data backtest reports' in 'name: BT131 Real Data Backtest Evidence\n\non:\n  workflow_dispatch:\n    inputs:\n      symbols:\n        descriptio...json\n            data/trade_plans/*manifest*.json\n          if-no-files-found: error\n          retention-days: 90\n'
2026-06-10T08:31:22.0759881Z FAILED tests/test_bt133_entry_confirmation_variants.py::test_bt133_flags_oos_degradation_as_overfit_risk - assert False
2026-06-10T08:31:22.0761435Z  +  where False = any(<generator object test_bt133_flags_oos_degradation_as_overfit_risk.<locals>.<genexpr> at 0x7f797b830380>)
2026-06-10T08:31:22.0762317Z 2 failed, 1833 passed, 1 skipped in 23.81s
2026-06-10T08:31:22.2991946Z ##[error]Process completed with exit code 1.
2026-06-10T08:31:22.3109941Z Post job cleanup.
2026-06-10T08:31:22.4063140Z [command]/usr/bin/git version
2026-06-10T08:31:22.4099049Z git version 2.54.0
2026-06-10T08:31:22.4141772Z Temporarily overriding HOME='/home/runner/work/_temp/89cfff37-6d2f-4906-8ea2-2854c52f3012' before making global git config changes
2026-06-10T08:31:22.4143116Z Adding repository directory to the temporary git global config as a safe directory
```

```text
2026-06-10T08:31:22.0752319Z E        +  where False = any(<generator object test_bt133_flags_oos_degradation_as_overfit_risk.<locals>.<genexpr> at 0x7f797b830380>)
2026-06-10T08:31:22.0753279Z 
2026-06-10T08:31:22.0753558Z tests/test_bt133_entry_confirmation_variants.py:167: AssertionError
2026-06-10T08:31:22.0754209Z =========================== short test summary info ============================
2026-06-10T08:31:22.0757012Z FAILED tests/test_bt131_real_data_backtest_evidence_workflow.py::test_bt131_workflow_persists_validated_reports_to_repo_without_telegram - assert 'git commit -m "Persist BT131/BT132 real-data backtest reports' in 'name: BT131 Real Data Backtest Evidence\n\non:\n  workflow_dispatch:\n    inputs:\n      symbols:\n        descriptio...json\n            data/trade_plans/*manifest*.json\n          if-no-files-found: error\n          retention-days: 90\n'
2026-06-10T08:31:22.0759881Z FAILED tests/test_bt133_entry_confirmation_variants.py::test_bt133_flags_oos_degradation_as_overfit_risk - assert False
2026-06-10T08:31:22.0761435Z  +  where False = any(<generator object test_bt133_flags_oos_degradation_as_overfit_risk.<locals>.<genexpr> at 0x7f797b830380>)
2026-06-10T08:31:22.0762317Z 2 failed, 1833 passed, 1 skipped in 23.81s
2026-06-10T08:31:22.2991946Z ##[error]Process completed with exit code 1.
2026-06-10T08:31:22.3109941Z Post job cleanup.
2026-06-10T08:31:22.4063140Z [command]/usr/bin/git version
2026-06-10T08:31:22.4099049Z git version 2.54.0
2026-06-10T08:31:22.4141772Z Temporarily overriding HOME='/home/runner/work/_temp/89cfff37-6d2f-4906-8ea2-2854c52f3012' before making global git config changes
2026-06-10T08:31:22.4143116Z Adding repository directory to the temporary git global config as a safe directory
2026-06-10T08:31:22.4154369Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-06-10T08:31:22.4188069Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
```

```text
2026-06-10T08:31:22.0753279Z 
2026-06-10T08:31:22.0753558Z tests/test_bt133_entry_confirmation_variants.py:167: AssertionError
2026-06-10T08:31:22.0754209Z =========================== short test summary info ============================
2026-06-10T08:31:22.0757012Z FAILED tests/test_bt131_real_data_backtest_evidence_workflow.py::test_bt131_workflow_persists_validated_reports_to_repo_without_telegram - assert 'git commit -m "Persist BT131/BT132 real-data backtest reports' in 'name: BT131 Real Data Backtest Evidence\n\non:\n  workflow_dispatch:\n    inputs:\n      symbols:\n        descriptio...json\n            data/trade_plans/*manifest*.json\n          if-no-files-found: error\n          retention-days: 90\n'
2026-06-10T08:31:22.0759881Z FAILED tests/test_bt133_entry_confirmation_variants.py::test_bt133_flags_oos_degradation_as_overfit_risk - assert False
2026-06-10T08:31:22.0761435Z  +  where False = any(<generator object test_bt133_flags_oos_degradation_as_overfit_risk.<locals>.<genexpr> at 0x7f797b830380>)
2026-06-10T08:31:22.0762317Z 2 failed, 1833 passed, 1 skipped in 23.81s
2026-06-10T08:31:22.2991946Z ##[error]Process completed with exit code 1.
2026-06-10T08:31:22.3109941Z Post job cleanup.
2026-06-10T08:31:22.4063140Z [command]/usr/bin/git version
2026-06-10T08:31:22.4099049Z git version 2.54.0
2026-06-10T08:31:22.4141772Z Temporarily overriding HOME='/home/runner/work/_temp/89cfff37-6d2f-4906-8ea2-2854c52f3012' before making global git config changes
2026-06-10T08:31:22.4143116Z Adding repository directory to the temporary git global config as a safe directory
2026-06-10T08:31:22.4154369Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-06-10T08:31:22.4188069Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-06-10T08:31:22.4220163Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
```

```text
2026-06-10T08:31:22.0757012Z FAILED tests/test_bt131_real_data_backtest_evidence_workflow.py::test_bt131_workflow_persists_validated_reports_to_repo_without_telegram - assert 'git commit -m "Persist BT131/BT132 real-data backtest reports' in 'name: BT131 Real Data Backtest Evidence\n\non:\n  workflow_dispatch:\n    inputs:\n      symbols:\n        descriptio...json\n            data/trade_plans/*manifest*.json\n          if-no-files-found: error\n          retention-days: 90\n'
2026-06-10T08:31:22.0759881Z FAILED tests/test_bt133_entry_confirmation_variants.py::test_bt133_flags_oos_degradation_as_overfit_risk - assert False
2026-06-10T08:31:22.0761435Z  +  where False = any(<generator object test_bt133_flags_oos_degradation_as_overfit_risk.<locals>.<genexpr> at 0x7f797b830380>)
2026-06-10T08:31:22.0762317Z 2 failed, 1833 passed, 1 skipped in 23.81s
2026-06-10T08:31:22.2991946Z ##[error]Process completed with exit code 1.
2026-06-10T08:31:22.3109941Z Post job cleanup.
2026-06-10T08:31:22.4063140Z [command]/usr/bin/git version
2026-06-10T08:31:22.4099049Z git version 2.54.0
2026-06-10T08:31:22.4141772Z Temporarily overriding HOME='/home/runner/work/_temp/89cfff37-6d2f-4906-8ea2-2854c52f3012' before making global git config changes
2026-06-10T08:31:22.4143116Z Adding repository directory to the temporary git global config as a safe directory
2026-06-10T08:31:22.4154369Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-06-10T08:31:22.4188069Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-06-10T08:31:22.4220163Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-06-10T08:31:22.4445778Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-06-10T08:31:22.4469874Z http.https://github.com/.extraheader
2026-06-10T08:31:22.4481729Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

## CI

- Run ID: `27263621976`
- Branch: `main`
- Commit: `c2874bd8f882`
- Title: Wire BT133 entry confirmation reports into BT131 evidence workflow
- Created: 2026-06-10T08:30:37Z
- Updated: 2026-06-10T08:31:43Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27263621976

### Failed job: Pytest

- Job ID: `80515199217`
- Started: 2026-06-10T08:30:40Z
- Completed: 2026-06-10T08:31:42Z
- Failed steps: 53. Full regression suite residual tests

#### Error context

```text
2026-06-10T08:31:39.8374784Z ........................................................................ [ 88%]
2026-06-10T08:31:40.0525525Z ........................................................................ [ 93%]
2026-06-10T08:31:40.0980920Z ........................................................................ [ 98%]
2026-06-10T08:31:40.1601219Z ...............                                                          [100%]
2026-06-10T08:31:40.1602122Z =================================== FAILURES ===================================
2026-06-10T08:31:40.1603280Z ___ test_bt131_workflow_persists_validated_reports_to_repo_without_telegram ____
2026-06-10T08:31:40.1603886Z 
2026-06-10T08:31:40.1604907Z     def test_bt131_workflow_persists_validated_reports_to_repo_without_telegram() -> None:
2026-06-10T08:31:40.1605743Z         text = _workflow_text()
2026-06-10T08:31:40.1606174Z     
2026-06-10T08:31:40.1606712Z         assert "Persist validated backtest reports to repository" in text
2026-06-10T08:31:40.1607628Z         assert "reports/backtests/real_data/runs/${GITHUB_RUN_ID_VALUE}" in text
2026-06-10T08:31:40.1608429Z         assert "reports/backtests/real_data/latest" in text
2026-06-10T08:31:40.1609121Z         assert "reports/backtests/real_data/index.json" in text
2026-06-10T08:31:40.1609776Z         assert "bt132-strategy-improvement-report.json" in text
2026-06-10T08:31:40.1610364Z         assert "bt132-strategy-improvement-report.md" in text
```

```text
2026-06-10T08:31:40.1612271Z         assert "git add reports/backtests/real_data/" in text
2026-06-10T08:31:40.1612926Z >       assert "git commit -m \"Persist BT131/BT132 real-data backtest reports" in text
2026-06-10T08:31:40.1614985Z E       assert 'git commit -m "Persist BT131/BT132 real-data backtest reports' in 'name: BT131 Real Data Backtest Evidence\n\non:\n  workflow_dispatch:\n    inputs:\n      symbols:\n        descriptio...json\n            data/trade_plans/*manifest*.json\n          if-no-files-found: error\n          retention-days: 90\n'
2026-06-10T08:31:40.1616549Z 
2026-06-10T08:31:40.1616862Z tests/test_bt131_real_data_backtest_evidence_workflow.py:120: AssertionError
2026-06-10T08:31:40.1617608Z _______________ test_bt133_flags_oos_degradation_as_overfit_risk _______________
2026-06-10T08:31:40.1618052Z 
2026-06-10T08:31:40.1618409Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-33/test_bt133_flags_oos_degradati0')
2026-06-10T08:31:40.1618925Z 
2026-06-10T08:31:40.1619270Z     def test_bt133_flags_oos_degradation_as_overfit_risk(tmp_path: Path) -> None:
2026-06-10T08:31:40.1619883Z         path = _evidence(tmp_path)
2026-06-10T08:31:40.1620237Z         payload = json.loads(path.read_text(encoding="utf-8"))
2026-06-10T08:31:40.1620597Z         payload["results"] = [
2026-06-10T08:31:40.1621048Z             _row("s1", "2024-01-01", r_multiple=-1.0, false_breakout=True, stop_hit=True, mfe=0.2, mae=-1.1),
2026-06-10T08:31:40.1621707Z             _row("s2", "2024-02-01", r_multiple=2.0, false_breakout=False, stop_hit=False, mfe=1.5, mae=-0.2),
2026-06-10T08:31:40.1622528Z             _row("s3", "2024-03-01", r_multiple=1.5, false_breakout=False, stop_hit=False, mfe=1.2, mae=-0.3),
```

```text
2026-06-10T08:31:40.1626533Z >       assert any(item.recommendation == "OVERFIT_RISK" for item in report.variant_results)
2026-06-10T08:31:40.1626998Z E       assert False
2026-06-10T08:31:40.1627553Z E        +  where False = any(<generator object test_bt133_flags_oos_degradation_as_overfit_risk.<locals>.<genexpr> at 0x7f1aa19b6dc0>)
2026-06-10T08:31:40.1628076Z 
2026-06-10T08:31:40.1628268Z tests/test_bt133_entry_confirmation_variants.py:167: AssertionError
2026-06-10T08:31:40.1628862Z =========================== short test summary info ============================
2026-06-10T08:31:40.1630691Z FAILED tests/test_bt131_real_data_backtest_evidence_workflow.py::test_bt131_workflow_persists_validated_reports_to_repo_without_telegram - assert 'git commit -m "Persist BT131/BT132 real-data backtest reports' in 'name: BT131 Real Data Backtest Evidence\n\non:\n  workflow_dispatch:\n    inputs:\n      symbols:\n        descriptio...json\n            data/trade_plans/*manifest*.json\n          if-no-files-found: error\n          retention-days: 90\n'
2026-06-10T08:31:40.1632517Z FAILED tests/test_bt133_entry_confirmation_variants.py::test_bt133_flags_oos_degradation_as_overfit_risk - assert False
2026-06-10T08:31:40.1633330Z  +  where False = any(<generator object test_bt133_flags_oos_degradation_as_overfit_risk.<locals>.<genexpr> at 0x7f1aa19b6dc0>)
2026-06-10T08:31:40.1633899Z 2 failed, 1380 passed, 1 skipped in 21.27s
2026-06-10T08:31:40.3611445Z ##[error]Process completed with exit code 1.
2026-06-10T08:31:40.3687748Z ##[group]Run actions/upload-artifact@v4
2026-06-10T08:31:40.3688059Z with:
2026-06-10T08:31:40.3688282Z   name: p109-residual-pytest-evidence
2026-06-10T08:31:40.3688606Z   path: artifacts/evidence/p109-residual-pytest/
2026-06-10T08:31:40.3688920Z   if-no-files-found: warn
```

```text
2026-06-10T08:31:40.1627553Z E        +  where False = any(<generator object test_bt133_flags_oos_degradation_as_overfit_risk.<locals>.<genexpr> at 0x7f1aa19b6dc0>)
2026-06-10T08:31:40.1628076Z 
2026-06-10T08:31:40.1628268Z tests/test_bt133_entry_confirmation_variants.py:167: AssertionError
2026-06-10T08:31:40.1628862Z =========================== short test summary info ============================
2026-06-10T08:31:40.1630691Z FAILED tests/test_bt131_real_data_backtest_evidence_workflow.py::test_bt131_workflow_persists_validated_reports_to_repo_without_telegram - assert 'git commit -m "Persist BT131/BT132 real-data backtest reports' in 'name: BT131 Real Data Backtest Evidence\n\non:\n  workflow_dispatch:\n    inputs:\n      symbols:\n        descriptio...json\n            data/trade_plans/*manifest*.json\n          if-no-files-found: error\n          retention-days: 90\n'
2026-06-10T08:31:40.1632517Z FAILED tests/test_bt133_entry_confirmation_variants.py::test_bt133_flags_oos_degradation_as_overfit_risk - assert False
2026-06-10T08:31:40.1633330Z  +  where False = any(<generator object test_bt133_flags_oos_degradation_as_overfit_risk.<locals>.<genexpr> at 0x7f1aa19b6dc0>)
2026-06-10T08:31:40.1633899Z 2 failed, 1380 passed, 1 skipped in 21.27s
2026-06-10T08:31:40.3611445Z ##[error]Process completed with exit code 1.
2026-06-10T08:31:40.3687748Z ##[group]Run actions/upload-artifact@v4
2026-06-10T08:31:40.3688059Z with:
2026-06-10T08:31:40.3688282Z   name: p109-residual-pytest-evidence
2026-06-10T08:31:40.3688606Z   path: artifacts/evidence/p109-residual-pytest/
2026-06-10T08:31:40.3688920Z   if-no-files-found: warn
2026-06-10T08:31:40.3689161Z   compression-level: 6
2026-06-10T08:31:40.3689382Z   overwrite: false
```

```text
2026-06-10T08:31:40.1628076Z 
2026-06-10T08:31:40.1628268Z tests/test_bt133_entry_confirmation_variants.py:167: AssertionError
2026-06-10T08:31:40.1628862Z =========================== short test summary info ============================
2026-06-10T08:31:40.1630691Z FAILED tests/test_bt131_real_data_backtest_evidence_workflow.py::test_bt131_workflow_persists_validated_reports_to_repo_without_telegram - assert 'git commit -m "Persist BT131/BT132 real-data backtest reports' in 'name: BT131 Real Data Backtest Evidence\n\non:\n  workflow_dispatch:\n    inputs:\n      symbols:\n        descriptio...json\n            data/trade_plans/*manifest*.json\n          if-no-files-found: error\n          retention-days: 90\n'
2026-06-10T08:31:40.1632517Z FAILED tests/test_bt133_entry_confirmation_variants.py::test_bt133_flags_oos_degradation_as_overfit_risk - assert False
2026-06-10T08:31:40.1633330Z  +  where False = any(<generator object test_bt133_flags_oos_degradation_as_overfit_risk.<locals>.<genexpr> at 0x7f1aa19b6dc0>)
2026-06-10T08:31:40.1633899Z 2 failed, 1380 passed, 1 skipped in 21.27s
2026-06-10T08:31:40.3611445Z ##[error]Process completed with exit code 1.
2026-06-10T08:31:40.3687748Z ##[group]Run actions/upload-artifact@v4
2026-06-10T08:31:40.3688059Z with:
2026-06-10T08:31:40.3688282Z   name: p109-residual-pytest-evidence
2026-06-10T08:31:40.3688606Z   path: artifacts/evidence/p109-residual-pytest/
2026-06-10T08:31:40.3688920Z   if-no-files-found: warn
2026-06-10T08:31:40.3689161Z   compression-level: 6
2026-06-10T08:31:40.3689382Z   overwrite: false
2026-06-10T08:31:40.3689626Z   include-hidden-files: false
```

```text
2026-06-10T08:31:40.1630691Z FAILED tests/test_bt131_real_data_backtest_evidence_workflow.py::test_bt131_workflow_persists_validated_reports_to_repo_without_telegram - assert 'git commit -m "Persist BT131/BT132 real-data backtest reports' in 'name: BT131 Real Data Backtest Evidence\n\non:\n  workflow_dispatch:\n    inputs:\n      symbols:\n        descriptio...json\n            data/trade_plans/*manifest*.json\n          if-no-files-found: error\n          retention-days: 90\n'
2026-06-10T08:31:40.1632517Z FAILED tests/test_bt133_entry_confirmation_variants.py::test_bt133_flags_oos_degradation_as_overfit_risk - assert False
2026-06-10T08:31:40.1633330Z  +  where False = any(<generator object test_bt133_flags_oos_degradation_as_overfit_risk.<locals>.<genexpr> at 0x7f1aa19b6dc0>)
2026-06-10T08:31:40.1633899Z 2 failed, 1380 passed, 1 skipped in 21.27s
2026-06-10T08:31:40.3611445Z ##[error]Process completed with exit code 1.
2026-06-10T08:31:40.3687748Z ##[group]Run actions/upload-artifact@v4
2026-06-10T08:31:40.3688059Z with:
2026-06-10T08:31:40.3688282Z   name: p109-residual-pytest-evidence
2026-06-10T08:31:40.3688606Z   path: artifacts/evidence/p109-residual-pytest/
2026-06-10T08:31:40.3688920Z   if-no-files-found: warn
2026-06-10T08:31:40.3689161Z   compression-level: 6
2026-06-10T08:31:40.3689382Z   overwrite: false
2026-06-10T08:31:40.3689626Z   include-hidden-files: false
2026-06-10T08:31:40.3689868Z env:
2026-06-10T08:31:40.3690131Z   pythonLocation: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-10T08:31:40.3690583Z   PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib/pkgconfig
```

## Decision Engine Tests

- Run ID: `27258582315`
- Branch: `main`
- Commit: `82519f3948aa`
- Title: Add BT133 entry confirmation variant tests
- Created: 2026-06-10T06:48:33Z
- Updated: 2026-06-10T06:49:22Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27258582315

### Failed job: tests

- Job ID: `80498571246`
- Started: 2026-06-10T06:48:35Z
- Completed: 2026-06-10T06:49:20Z
- Failed steps: 5. Run pytest

#### Error context

```text
2026-06-10T06:49:18.7162166Z ........................................................................ [ 90%]
2026-06-10T06:49:18.9234467Z ........................................................................ [ 94%]
2026-06-10T06:49:18.9673528Z ........................................................................ [ 98%]
2026-06-10T06:49:19.0510553Z ....................................                                     [100%]
2026-06-10T06:49:19.0511647Z =================================== FAILURES ===================================
2026-06-10T06:49:19.0512470Z _______________ test_bt133_flags_oos_degradation_as_overfit_risk _______________
2026-06-10T06:49:19.0513032Z 
2026-06-10T06:49:19.0513507Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-0/test_bt133_flags_oos_degradati0')
2026-06-10T06:49:19.0514135Z 
2026-06-10T06:49:19.0514945Z     def test_bt133_flags_oos_degradation_as_overfit_risk(tmp_path: Path) -> None:
2026-06-10T06:49:19.0515658Z         path = _evidence(tmp_path)
2026-06-10T06:49:19.0516372Z         payload = json.loads(path.read_text(encoding="utf-8"))
2026-06-10T06:49:19.0517418Z         payload["results"] = [
2026-06-10T06:49:19.0518084Z             _row("s1", "2024-01-01", r_multiple=-1.0, false_breakout=True, stop_hit=True, mfe=0.2, mae=-1.1),
2026-06-10T06:49:19.0519059Z             _row("s2", "2024-02-01", r_multiple=2.0, false_breakout=False, stop_hit=False, mfe=1.5, mae=-0.2),
2026-06-10T06:49:19.0520005Z             _row("s3", "2024-03-01", r_multiple=1.5, false_breakout=False, stop_hit=False, mfe=1.2, mae=-0.3),
```

```text
2026-06-10T06:49:19.0525577Z >       assert any(item.recommendation == "OVERFIT_RISK" for item in report.variant_results)
2026-06-10T06:49:19.0526241Z E       assert False
2026-06-10T06:49:19.0527218Z E        +  where False = any(<generator object test_bt133_flags_oos_degradation_as_overfit_risk.<locals>.<genexpr> at 0x7fcf7e9052f0>)
2026-06-10T06:49:19.0527977Z 
2026-06-10T06:49:19.0528258Z tests/test_bt133_entry_confirmation_variants.py:167: AssertionError
2026-06-10T06:49:19.0528909Z =========================== short test summary info ============================
2026-06-10T06:49:19.0529968Z FAILED tests/test_bt133_entry_confirmation_variants.py::test_bt133_flags_oos_degradation_as_overfit_risk - assert False
2026-06-10T06:49:19.0531227Z  +  where False = any(<generator object test_bt133_flags_oos_degradation_as_overfit_risk.<locals>.<genexpr> at 0x7fcf7e9052f0>)
2026-06-10T06:49:19.0532110Z 1 failed, 1834 passed, 1 skipped in 24.17s
2026-06-10T06:49:19.2941308Z ##[error]Process completed with exit code 1.
2026-06-10T06:49:19.3050041Z Post job cleanup.
2026-06-10T06:49:19.4039289Z [command]/usr/bin/git version
2026-06-10T06:49:19.4075340Z git version 2.54.0
2026-06-10T06:49:19.4118019Z Temporarily overriding HOME='/home/runner/work/_temp/75f83a29-b007-41c6-81ae-528d24912e63' before making global git config changes
2026-06-10T06:49:19.4119225Z Adding repository directory to the temporary git global config as a safe directory
2026-06-10T06:49:19.4123811Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
```

```text
2026-06-10T06:49:19.0527218Z E        +  where False = any(<generator object test_bt133_flags_oos_degradation_as_overfit_risk.<locals>.<genexpr> at 0x7fcf7e9052f0>)
2026-06-10T06:49:19.0527977Z 
2026-06-10T06:49:19.0528258Z tests/test_bt133_entry_confirmation_variants.py:167: AssertionError
2026-06-10T06:49:19.0528909Z =========================== short test summary info ============================
2026-06-10T06:49:19.0529968Z FAILED tests/test_bt133_entry_confirmation_variants.py::test_bt133_flags_oos_degradation_as_overfit_risk - assert False
2026-06-10T06:49:19.0531227Z  +  where False = any(<generator object test_bt133_flags_oos_degradation_as_overfit_risk.<locals>.<genexpr> at 0x7fcf7e9052f0>)
2026-06-10T06:49:19.0532110Z 1 failed, 1834 passed, 1 skipped in 24.17s
2026-06-10T06:49:19.2941308Z ##[error]Process completed with exit code 1.
2026-06-10T06:49:19.3050041Z Post job cleanup.
2026-06-10T06:49:19.4039289Z [command]/usr/bin/git version
2026-06-10T06:49:19.4075340Z git version 2.54.0
2026-06-10T06:49:19.4118019Z Temporarily overriding HOME='/home/runner/work/_temp/75f83a29-b007-41c6-81ae-528d24912e63' before making global git config changes
2026-06-10T06:49:19.4119225Z Adding repository directory to the temporary git global config as a safe directory
2026-06-10T06:49:19.4123811Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-06-10T06:49:19.4165698Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-06-10T06:49:19.4197212Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
```

```text
2026-06-10T06:49:19.0528909Z =========================== short test summary info ============================
2026-06-10T06:49:19.0529968Z FAILED tests/test_bt133_entry_confirmation_variants.py::test_bt133_flags_oos_degradation_as_overfit_risk - assert False
2026-06-10T06:49:19.0531227Z  +  where False = any(<generator object test_bt133_flags_oos_degradation_as_overfit_risk.<locals>.<genexpr> at 0x7fcf7e9052f0>)
2026-06-10T06:49:19.0532110Z 1 failed, 1834 passed, 1 skipped in 24.17s
2026-06-10T06:49:19.2941308Z ##[error]Process completed with exit code 1.
2026-06-10T06:49:19.3050041Z Post job cleanup.
2026-06-10T06:49:19.4039289Z [command]/usr/bin/git version
2026-06-10T06:49:19.4075340Z git version 2.54.0
2026-06-10T06:49:19.4118019Z Temporarily overriding HOME='/home/runner/work/_temp/75f83a29-b007-41c6-81ae-528d24912e63' before making global git config changes
2026-06-10T06:49:19.4119225Z Adding repository directory to the temporary git global config as a safe directory
2026-06-10T06:49:19.4123811Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-06-10T06:49:19.4165698Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-06-10T06:49:19.4197212Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-06-10T06:49:19.4419043Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-06-10T06:49:19.4440760Z http.https://github.com/.extraheader
2026-06-10T06:49:19.4452336Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

## CI

- Run ID: `27258582294`
- Branch: `main`
- Commit: `82519f3948aa`
- Title: Add BT133 entry confirmation variant tests
- Created: 2026-06-10T06:48:33Z
- Updated: 2026-06-10T06:49:45Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27258582294

### Failed job: Pytest

- Job ID: `80498571264`
- Started: 2026-06-10T06:48:35Z
- Completed: 2026-06-10T06:49:44Z
- Failed steps: 53. Full regression suite residual tests

#### Error context

```text
2026-06-10T06:49:40.6182654Z ........................................................................ [ 88%]
2026-06-10T06:49:40.8717649Z ........................................................................ [ 93%]
2026-06-10T06:49:40.9035721Z ........................................................................ [ 98%]
2026-06-10T06:49:40.9506680Z ...............                                                          [100%]
2026-06-10T06:49:40.9507189Z =================================== FAILURES ===================================
2026-06-10T06:49:40.9508230Z _______________ test_bt133_flags_oos_degradation_as_overfit_risk _______________
2026-06-10T06:49:40.9508706Z 
2026-06-10T06:49:40.9509186Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-33/test_bt133_flags_oos_degradati0')
2026-06-10T06:49:40.9509945Z 
2026-06-10T06:49:40.9510455Z     def test_bt133_flags_oos_degradation_as_overfit_risk(tmp_path: Path) -> None:
2026-06-10T06:49:40.9511055Z         path = _evidence(tmp_path)
2026-06-10T06:49:40.9511561Z         payload = json.loads(path.read_text(encoding="utf-8"))
2026-06-10T06:49:40.9512116Z         payload["results"] = [
2026-06-10T06:49:40.9512747Z             _row("s1", "2024-01-01", r_multiple=-1.0, false_breakout=True, stop_hit=True, mfe=0.2, mae=-1.1),
2026-06-10T06:49:40.9513647Z             _row("s2", "2024-02-01", r_multiple=2.0, false_breakout=False, stop_hit=False, mfe=1.5, mae=-0.2),
2026-06-10T06:49:40.9514413Z             _row("s3", "2024-03-01", r_multiple=1.5, false_breakout=False, stop_hit=False, mfe=1.2, mae=-0.3),
```

```text
2026-06-10T06:49:40.9519989Z >       assert any(item.recommendation == "OVERFIT_RISK" for item in report.variant_results)
2026-06-10T06:49:40.9520658Z E       assert False
2026-06-10T06:49:40.9521416Z E        +  where False = any(<generator object test_bt133_flags_oos_degradation_as_overfit_risk.<locals>.<genexpr> at 0x7f4124d84c70>)
2026-06-10T06:49:40.9522100Z 
2026-06-10T06:49:40.9522482Z tests/test_bt133_entry_confirmation_variants.py:167: AssertionError
2026-06-10T06:49:40.9523161Z =========================== short test summary info ============================
2026-06-10T06:49:40.9523992Z FAILED tests/test_bt133_entry_confirmation_variants.py::test_bt133_flags_oos_degradation_as_overfit_risk - assert False
2026-06-10T06:49:40.9524779Z  +  where False = any(<generator object test_bt133_flags_oos_degradation_as_overfit_risk.<locals>.<genexpr> at 0x7f4124d84c70>)
2026-06-10T06:49:40.9525235Z 1 failed, 1381 passed, 1 skipped in 18.19s
2026-06-10T06:49:41.1880312Z ##[error]Process completed with exit code 1.
2026-06-10T06:49:41.1939937Z ##[group]Run actions/upload-artifact@v4
2026-06-10T06:49:41.1940172Z with:
2026-06-10T06:49:41.1940363Z   name: p109-residual-pytest-evidence
2026-06-10T06:49:41.1940622Z   path: artifacts/evidence/p109-residual-pytest/
2026-06-10T06:49:41.1940880Z   if-no-files-found: warn
2026-06-10T06:49:41.1941094Z   compression-level: 6
```

```text
2026-06-10T06:49:40.9521416Z E        +  where False = any(<generator object test_bt133_flags_oos_degradation_as_overfit_risk.<locals>.<genexpr> at 0x7f4124d84c70>)
2026-06-10T06:49:40.9522100Z 
2026-06-10T06:49:40.9522482Z tests/test_bt133_entry_confirmation_variants.py:167: AssertionError
2026-06-10T06:49:40.9523161Z =========================== short test summary info ============================
2026-06-10T06:49:40.9523992Z FAILED tests/test_bt133_entry_confirmation_variants.py::test_bt133_flags_oos_degradation_as_overfit_risk - assert False
2026-06-10T06:49:40.9524779Z  +  where False = any(<generator object test_bt133_flags_oos_degradation_as_overfit_risk.<locals>.<genexpr> at 0x7f4124d84c70>)
2026-06-10T06:49:40.9525235Z 1 failed, 1381 passed, 1 skipped in 18.19s
2026-06-10T06:49:41.1880312Z ##[error]Process completed with exit code 1.
2026-06-10T06:49:41.1939937Z ##[group]Run actions/upload-artifact@v4
2026-06-10T06:49:41.1940172Z with:
2026-06-10T06:49:41.1940363Z   name: p109-residual-pytest-evidence
2026-06-10T06:49:41.1940622Z   path: artifacts/evidence/p109-residual-pytest/
2026-06-10T06:49:41.1940880Z   if-no-files-found: warn
2026-06-10T06:49:41.1941094Z   compression-level: 6
2026-06-10T06:49:41.1941282Z   overwrite: false
2026-06-10T06:49:41.1941466Z   include-hidden-files: false
```

```text
2026-06-10T06:49:40.9523161Z =========================== short test summary info ============================
2026-06-10T06:49:40.9523992Z FAILED tests/test_bt133_entry_confirmation_variants.py::test_bt133_flags_oos_degradation_as_overfit_risk - assert False
2026-06-10T06:49:40.9524779Z  +  where False = any(<generator object test_bt133_flags_oos_degradation_as_overfit_risk.<locals>.<genexpr> at 0x7f4124d84c70>)
2026-06-10T06:49:40.9525235Z 1 failed, 1381 passed, 1 skipped in 18.19s
2026-06-10T06:49:41.1880312Z ##[error]Process completed with exit code 1.
2026-06-10T06:49:41.1939937Z ##[group]Run actions/upload-artifact@v4
2026-06-10T06:49:41.1940172Z with:
2026-06-10T06:49:41.1940363Z   name: p109-residual-pytest-evidence
2026-06-10T06:49:41.1940622Z   path: artifacts/evidence/p109-residual-pytest/
2026-06-10T06:49:41.1940880Z   if-no-files-found: warn
2026-06-10T06:49:41.1941094Z   compression-level: 6
2026-06-10T06:49:41.1941282Z   overwrite: false
2026-06-10T06:49:41.1941466Z   include-hidden-files: false
2026-06-10T06:49:41.1941670Z env:
2026-06-10T06:49:41.1941878Z   pythonLocation: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-10T06:49:41.1942224Z   PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib/pkgconfig
```

## Report Quality Validation

- Run ID: `27258582289`
- Branch: `main`
- Commit: `82519f3948aa`
- Title: Add BT133 entry confirmation variant tests
- Created: 2026-06-10T06:48:33Z
- Updated: 2026-06-10T06:49:46Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27258582289

### Failed job: validate-reports (postmarket)

- Job ID: `80498571254`
- Started: 2026-06-10T06:48:35Z
- Completed: 2026-06-10T06:49:34Z
- Failed steps: 6. Validate report quality

#### Error context

```text
2026-06-10T06:49:32.2887548Z - Report used fallback data; content is structurally valid but not analytically strong
2026-06-10T06:49:32.2888210Z 
2026-06-10T06:49:32.2888349Z Errors:
2026-06-10T06:49:32.2888695Z - Missing analytical term: Risk Tier
2026-06-10T06:49:32.2951879Z ##[error]Process completed with exit code 1.
2026-06-10T06:49:32.3027671Z ##[group]Run actions/upload-artifact@v4
2026-06-10T06:49:32.3027968Z with:
2026-06-10T06:49:32.3028177Z   name: validated-postmarket-report
2026-06-10T06:49:32.3028483Z   path: reports/generated/postmarket-report.md
2026-06-10T06:49:32.3028776Z   retention-days: 14
2026-06-10T06:49:32.3028992Z   if-no-files-found: warn
2026-06-10T06:49:32.3029217Z   compression-level: 6
2026-06-10T06:49:32.3029490Z   overwrite: false
2026-06-10T06:49:32.3029707Z   include-hidden-files: false
2026-06-10T06:49:32.3029939Z env:
2026-06-10T06:49:32.3030535Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (premarket)

- Job ID: `80498571267`
- Started: 2026-06-10T06:48:35Z
- Completed: 2026-06-10T06:49:45Z
- Failed steps: 6. Validate report quality

#### Error context

```text
2026-06-10T06:49:42.2328048Z - Report used fallback data; content is structurally valid but not analytically strong
2026-06-10T06:49:42.2328648Z 
2026-06-10T06:49:42.2328774Z Errors:
2026-06-10T06:49:42.2329080Z - Missing analytical term: Risk Tier
2026-06-10T06:49:42.2400447Z ##[error]Process completed with exit code 1.
2026-06-10T06:49:42.2475592Z ##[group]Run actions/upload-artifact@v4
2026-06-10T06:49:42.2475884Z with:
2026-06-10T06:49:42.2476113Z   name: validated-premarket-report
2026-06-10T06:49:42.2476422Z   path: reports/generated/premarket-report.md
2026-06-10T06:49:42.2476715Z   retention-days: 14
2026-06-10T06:49:42.2477256Z   if-no-files-found: warn
2026-06-10T06:49:42.2477506Z   compression-level: 6
2026-06-10T06:49:42.2477733Z   overwrite: false
2026-06-10T06:49:42.2477969Z   include-hidden-files: false
2026-06-10T06:49:42.2478220Z env:
2026-06-10T06:49:42.2478598Z   POLYGON_API_KEY: ***
```

## Report Quality Validation

- Run ID: `27257426367`
- Branch: `main`
- Commit: `9e0a0afb5416`
- Title: analyze_bt133_entry_confirmation_variants.py erstellen
- Created: 2026-06-10T06:21:36Z
- Updated: 2026-06-10T06:22:41Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27257426367

### Failed job: validate-reports (premarket)

- Job ID: `80494791247`
- Started: 2026-06-10T06:21:38Z
- Completed: 2026-06-10T06:22:39Z
- Failed steps: 6. Validate report quality

#### Error context

```text
2026-06-10T06:22:36.2402852Z - Report used fallback data; content is structurally valid but not analytically strong
2026-06-10T06:22:36.2403520Z 
2026-06-10T06:22:36.2403662Z Errors:
2026-06-10T06:22:36.2404030Z - Missing analytical term: Risk Tier
2026-06-10T06:22:36.2471382Z ##[error]Process completed with exit code 1.
2026-06-10T06:22:36.2551957Z ##[group]Run actions/upload-artifact@v4
2026-06-10T06:22:36.2552258Z with:
2026-06-10T06:22:36.2552477Z   name: validated-premarket-report
2026-06-10T06:22:36.2552790Z   path: reports/generated/premarket-report.md
2026-06-10T06:22:36.2553096Z   retention-days: 14
2026-06-10T06:22:36.2553327Z   if-no-files-found: warn
2026-06-10T06:22:36.2553571Z   compression-level: 6
2026-06-10T06:22:36.2553794Z   overwrite: false
2026-06-10T06:22:36.2554035Z   include-hidden-files: false
2026-06-10T06:22:36.2554274Z env:
2026-06-10T06:22:36.2554583Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (postmarket)

- Job ID: `80494791321`
- Started: 2026-06-10T06:21:38Z
- Completed: 2026-06-10T06:22:40Z
- Failed steps: 6. Validate report quality

#### Error context

```text
2026-06-10T06:22:37.6012077Z - Report used fallback data; content is structurally valid but not analytically strong
2026-06-10T06:22:37.6012669Z 
2026-06-10T06:22:37.6012803Z Errors:
2026-06-10T06:22:37.6013129Z - Missing analytical term: Risk Tier
2026-06-10T06:22:37.6082226Z ##[error]Process completed with exit code 1.
2026-06-10T06:22:37.6159941Z ##[group]Run actions/upload-artifact@v4
2026-06-10T06:22:37.6160253Z with:
2026-06-10T06:22:37.6160495Z   name: validated-postmarket-report
2026-06-10T06:22:37.6161108Z   path: reports/generated/postmarket-report.md
2026-06-10T06:22:37.6161428Z   retention-days: 14
2026-06-10T06:22:37.6161675Z   if-no-files-found: warn
2026-06-10T06:22:37.6161930Z   compression-level: 6
2026-06-10T06:22:37.6162164Z   overwrite: false
2026-06-10T06:22:37.6162414Z   include-hidden-files: false
2026-06-10T06:22:37.6162680Z env:
2026-06-10T06:22:37.6163020Z   POLYGON_API_KEY: ***
```

## Daily Evidence Report

- Run ID: `27241419102`
- Branch: `main`
- Commit: `5f6a8b1ef373`
- Title: Daily Evidence Report
- Created: 2026-06-09T23:02:15Z
- Updated: 2026-06-09T23:02:40Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27241419102

### Failed job: Build daily evidence report

- Job ID: `80445791165`
- Started: 2026-06-09T23:02:18Z
- Completed: 2026-06-09T23:02:39Z
- Failed steps: 7. Build scheduled paper observation incoming sources

#### Error context

```text
2026-06-09T23:02:34.8008322Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-09T23:02:34.8008642Z ##[endgroup]
2026-06-09T23:02:34.8468544Z Daily paper observation source status: FAIL
2026-06-09T23:02:34.8469218Z Built files: 0
2026-06-09T23:02:34.8469672Z ERROR: missing source file: paper_observations.json
2026-06-09T23:02:34.8470295Z ERROR: missing source file: backtest_results.json
2026-06-09T23:02:34.8470916Z ERROR: missing source file: regime_observations.json
2026-06-09T23:02:34.8471544Z ERROR: missing source file: position_snapshots.json
2026-06-09T23:02:34.8540883Z ##[error]Process completed with exit code 1.
2026-06-09T23:02:34.8681188Z ##[group]Run actions/upload-artifact@v4
2026-06-09T23:02:34.8681497Z with:
2026-06-09T23:02:34.8681720Z   name: daily-evidence-report-2026-06-09
2026-06-09T23:02:34.8682029Z   if-no-files-found: error
2026-06-09T23:02:34.8683274Z   path: reports/daily_evidence_source_bootstrap/
reports/daily_paper_observation_source/
reports/daily_observation_cadence/
```

```text
2026-06-09T23:02:34.8008642Z ##[endgroup]
2026-06-09T23:02:34.8468544Z Daily paper observation source status: FAIL
2026-06-09T23:02:34.8469218Z Built files: 0
2026-06-09T23:02:34.8469672Z ERROR: missing source file: paper_observations.json
2026-06-09T23:02:34.8470295Z ERROR: missing source file: backtest_results.json
2026-06-09T23:02:34.8470916Z ERROR: missing source file: regime_observations.json
2026-06-09T23:02:34.8471544Z ERROR: missing source file: position_snapshots.json
2026-06-09T23:02:34.8540883Z ##[error]Process completed with exit code 1.
2026-06-09T23:02:34.8681188Z ##[group]Run actions/upload-artifact@v4
2026-06-09T23:02:34.8681497Z with:
2026-06-09T23:02:34.8681720Z   name: daily-evidence-report-2026-06-09
2026-06-09T23:02:34.8682029Z   if-no-files-found: error
2026-06-09T23:02:34.8683274Z   path: reports/daily_evidence_source_bootstrap/
reports/daily_paper_observation_source/
reports/daily_observation_cadence/
reports/daily_observation_source_feed/
```

```text
2026-06-09T23:02:34.8468544Z Daily paper observation source status: FAIL
2026-06-09T23:02:34.8469218Z Built files: 0
2026-06-09T23:02:34.8469672Z ERROR: missing source file: paper_observations.json
2026-06-09T23:02:34.8470295Z ERROR: missing source file: backtest_results.json
2026-06-09T23:02:34.8470916Z ERROR: missing source file: regime_observations.json
2026-06-09T23:02:34.8471544Z ERROR: missing source file: position_snapshots.json
2026-06-09T23:02:34.8540883Z ##[error]Process completed with exit code 1.
2026-06-09T23:02:34.8681188Z ##[group]Run actions/upload-artifact@v4
2026-06-09T23:02:34.8681497Z with:
2026-06-09T23:02:34.8681720Z   name: daily-evidence-report-2026-06-09
2026-06-09T23:02:34.8682029Z   if-no-files-found: error
2026-06-09T23:02:34.8683274Z   path: reports/daily_evidence_source_bootstrap/
reports/daily_paper_observation_source/
reports/daily_observation_cadence/
reports/daily_observation_source_feed/
reports/daily_observation_feed/
```

```text
2026-06-09T23:02:34.8469218Z Built files: 0
2026-06-09T23:02:34.8469672Z ERROR: missing source file: paper_observations.json
2026-06-09T23:02:34.8470295Z ERROR: missing source file: backtest_results.json
2026-06-09T23:02:34.8470916Z ERROR: missing source file: regime_observations.json
2026-06-09T23:02:34.8471544Z ERROR: missing source file: position_snapshots.json
2026-06-09T23:02:34.8540883Z ##[error]Process completed with exit code 1.
2026-06-09T23:02:34.8681188Z ##[group]Run actions/upload-artifact@v4
2026-06-09T23:02:34.8681497Z with:
2026-06-09T23:02:34.8681720Z   name: daily-evidence-report-2026-06-09
2026-06-09T23:02:34.8682029Z   if-no-files-found: error
2026-06-09T23:02:34.8683274Z   path: reports/daily_evidence_source_bootstrap/
reports/daily_paper_observation_source/
reports/daily_observation_cadence/
reports/daily_observation_source_feed/
reports/daily_observation_feed/
reports/daily_evidence_input_build/
```

```text
2026-06-09T23:02:34.8469672Z ERROR: missing source file: paper_observations.json
2026-06-09T23:02:34.8470295Z ERROR: missing source file: backtest_results.json
2026-06-09T23:02:34.8470916Z ERROR: missing source file: regime_observations.json
2026-06-09T23:02:34.8471544Z ERROR: missing source file: position_snapshots.json
2026-06-09T23:02:34.8540883Z ##[error]Process completed with exit code 1.
2026-06-09T23:02:34.8681188Z ##[group]Run actions/upload-artifact@v4
2026-06-09T23:02:34.8681497Z with:
2026-06-09T23:02:34.8681720Z   name: daily-evidence-report-2026-06-09
2026-06-09T23:02:34.8682029Z   if-no-files-found: error
2026-06-09T23:02:34.8683274Z   path: reports/daily_evidence_source_bootstrap/
reports/daily_paper_observation_source/
reports/daily_observation_cadence/
reports/daily_observation_source_feed/
reports/daily_observation_feed/
reports/daily_evidence_input_build/
reports/daily_evidence_input_validation/
```

## Report Quality Validation

- Run ID: `27239585572`
- Branch: `main`
- Commit: `5f6a8b1ef373`
- Title: test_issue_162_scanner_metrics_signal_path.py aktualisieren
- Created: 2026-06-09T22:19:52Z
- Updated: 2026-06-09T22:21:10Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27239585572

### Failed job: validate-reports (postmarket)

- Job ID: `80439856460`
- Started: 2026-06-09T22:19:56Z
- Completed: 2026-06-09T22:21:09Z
- Failed steps: 6. Validate report quality

#### Error context

```text
2026-06-09T22:21:04.9609079Z - Report used fallback data; content is structurally valid but not analytically strong
2026-06-09T22:21:04.9609688Z 
2026-06-09T22:21:04.9609819Z Errors:
2026-06-09T22:21:04.9610153Z - Missing analytical term: Risk Tier
2026-06-09T22:21:04.9677088Z ##[error]Process completed with exit code 1.
2026-06-09T22:21:04.9757087Z ##[group]Run actions/upload-artifact@v4
2026-06-09T22:21:04.9757399Z with:
2026-06-09T22:21:04.9757616Z   name: validated-postmarket-report
2026-06-09T22:21:04.9757927Z   path: reports/generated/postmarket-report.md
2026-06-09T22:21:04.9758230Z   retention-days: 14
2026-06-09T22:21:04.9758449Z   if-no-files-found: warn
2026-06-09T22:21:04.9758694Z   compression-level: 6
2026-06-09T22:21:04.9758906Z   overwrite: false
2026-06-09T22:21:04.9759120Z   include-hidden-files: false
2026-06-09T22:21:04.9759348Z env:
2026-06-09T22:21:04.9759669Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (premarket)

- Job ID: `80439856509`
- Started: 2026-06-09T22:19:55Z
- Completed: 2026-06-09T22:21:05Z
- Failed steps: 6. Validate report quality

#### Error context

```text
2026-06-09T22:21:01.9290024Z - Report used fallback data; content is structurally valid but not analytically strong
2026-06-09T22:21:01.9290664Z 
2026-06-09T22:21:01.9290801Z Errors:
2026-06-09T22:21:01.9291143Z - Missing analytical term: Risk Tier
2026-06-09T22:21:01.9353816Z ##[error]Process completed with exit code 1.
2026-06-09T22:21:01.9429826Z ##[group]Run actions/upload-artifact@v4
2026-06-09T22:21:01.9430323Z with:
2026-06-09T22:21:01.9430686Z   name: validated-premarket-report
2026-06-09T22:21:01.9431005Z   path: reports/generated/premarket-report.md
2026-06-09T22:21:01.9431308Z   retention-days: 14
2026-06-09T22:21:01.9431534Z   if-no-files-found: warn
2026-06-09T22:21:01.9431765Z   compression-level: 6
2026-06-09T22:21:01.9431976Z   overwrite: false
2026-06-09T22:21:01.9432205Z   include-hidden-files: false
2026-06-09T22:21:01.9432443Z env:
2026-06-09T22:21:01.9432753Z   POLYGON_API_KEY: ***
```
