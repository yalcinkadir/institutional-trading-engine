# GitHub Actions Workflow Error Report

Generated: 2026-05-28 08:32 UTC
Repository: `yalcinkadir/institutional-trading-engine`
Filter since: 2026-05-27 08:32 UTC
Failed runs included: 7

## Decision Engine Tests

- Run ID: `26562124255`
- Branch: `main`
- Commit: `c56aae4afaac`
- Title: Merge pull request #87 from yalcinkadir/daily-reconciliation-workflow
- Created: 2026-05-28T07:53:06Z
- Updated: 2026-05-28T07:53:42Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26562124255

### Failed job: tests

- Job ID: `78247464014`
- Started: 2026-05-28T07:53:09Z
- Completed: 2026-05-28T07:53:41Z
- Failed steps: 5. Run pytest

#### Error context

```text
2026-05-28T07:53:37.7827308Z ........................................................................ [ 82%]
2026-05-28T07:53:37.8286546Z ........................................................................ [ 89%]
2026-05-28T07:53:38.0438422Z ........................................................................ [ 96%]
2026-05-28T07:53:38.5624659Z .................................                                        [100%]
2026-05-28T07:53:38.5625693Z =================================== FAILURES ===================================
2026-05-28T07:53:38.5626385Z ___ test_daily_execution_reconciliation_can_warn_on_missing_observed_record ____
2026-05-28T07:53:38.5626897Z 
2026-05-28T07:53:38.5627205Z     def test_daily_execution_reconciliation_can_warn_on_missing_observed_record():
2026-05-28T07:53:38.5627837Z         report = reconcile_daily_execution(
2026-05-28T07:53:38.5628295Z             expected_records=[_expected()],
2026-05-28T07:53:38.5629166Z             observed_records=[],
2026-05-28T07:53:38.5629881Z             config=DailyExecutionReconciliationConfig(require_observed_for_each_expected=False),
2026-05-28T07:53:38.5630599Z         )
2026-05-28T07:53:38.5630866Z     
2026-05-28T07:53:38.5631164Z >       assert report.passed
2026-05-28T07:53:38.5631565Z E       AssertionError: assert False
```

```text
2026-05-28T07:53:38.5629881Z             config=DailyExecutionReconciliationConfig(require_observed_for_each_expected=False),
2026-05-28T07:53:38.5630599Z         )
2026-05-28T07:53:38.5630866Z     
2026-05-28T07:53:38.5631164Z >       assert report.passed
2026-05-28T07:53:38.5631565Z E       AssertionError: assert False
2026-05-28T07:53:38.5633323Z E        +  where False = DailyExecutionReconciliationReport(passed=False, status=<DailyExecutionStatus.FAIL: 'FAIL'>, metrics=DailyExecutionMet...expected_vs_observed_paper_or_live_records', 'no_order_submission_performed', 'no_live_trading_authorization_granted']).passed
2026-05-28T07:53:38.5635204Z 
2026-05-28T07:53:38.5635482Z tests/test_daily_execution_reconciliation.py:78: AssertionError
2026-05-28T07:53:38.5635936Z =============================== warnings summary ===============================
2026-05-28T07:53:38.5636451Z tests/test_jwt_auth.py::test_create_and_validate_token
2026-05-28T07:53:38.5636862Z tests/test_security_layer.py::test_metrics_accepts_admin_token
2026-05-28T07:53:38.5637576Z tests/test_security_layer.py::test_viewer_cannot_access_metrics
2026-05-28T07:53:38.5638572Z   /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/jwt/api_jwt.py:147: InsecureKeyLengthWarning: The HMAC key is 18 bytes long, which is below the minimum recommended length of 32 bytes for SHA256. See RFC 7518 Section 3.2.
2026-05-28T07:53:38.5639464Z     return self._jws.encode(
2026-05-28T07:53:38.5639619Z 
2026-05-28T07:53:38.5639773Z tests/test_jwt_auth.py::test_create_and_validate_token
```

```text
2026-05-28T07:53:38.5631164Z >       assert report.passed
2026-05-28T07:53:38.5631565Z E       AssertionError: assert False
2026-05-28T07:53:38.5633323Z E        +  where False = DailyExecutionReconciliationReport(passed=False, status=<DailyExecutionStatus.FAIL: 'FAIL'>, metrics=DailyExecutionMet...expected_vs_observed_paper_or_live_records', 'no_order_submission_performed', 'no_live_trading_authorization_granted']).passed
2026-05-28T07:53:38.5635204Z 
2026-05-28T07:53:38.5635482Z tests/test_daily_execution_reconciliation.py:78: AssertionError
2026-05-28T07:53:38.5635936Z =============================== warnings summary ===============================
2026-05-28T07:53:38.5636451Z tests/test_jwt_auth.py::test_create_and_validate_token
2026-05-28T07:53:38.5636862Z tests/test_security_layer.py::test_metrics_accepts_admin_token
2026-05-28T07:53:38.5637576Z tests/test_security_layer.py::test_viewer_cannot_access_metrics
2026-05-28T07:53:38.5638572Z   /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/jwt/api_jwt.py:147: InsecureKeyLengthWarning: The HMAC key is 18 bytes long, which is below the minimum recommended length of 32 bytes for SHA256. See RFC 7518 Section 3.2.
2026-05-28T07:53:38.5639464Z     return self._jws.encode(
2026-05-28T07:53:38.5639619Z 
2026-05-28T07:53:38.5639773Z tests/test_jwt_auth.py::test_create_and_validate_token
2026-05-28T07:53:38.5640161Z tests/test_security_layer.py::test_metrics_accepts_admin_token
2026-05-28T07:53:38.5640581Z tests/test_security_layer.py::test_viewer_cannot_access_metrics
2026-05-28T07:53:38.5641536Z   /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/jwt/api_jwt.py:368: InsecureKeyLengthWarning: The HMAC key is 18 bytes long, which is below the minimum recommended length of 32 bytes for SHA256. See RFC 7518 Section 3.2.
```

```text
2026-05-28T07:53:38.5642455Z     decoded = self.decode_complete(
2026-05-28T07:53:38.5642644Z 
2026-05-28T07:53:38.5642882Z -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2026-05-28T07:53:38.5643370Z =========================== short test summary info ============================
2026-05-28T07:53:38.5644362Z FAILED tests/test_daily_execution_reconciliation.py::test_daily_execution_reconciliation_can_warn_on_missing_observed_record - AssertionError: assert False
2026-05-28T07:53:38.5645768Z  +  where False = DailyExecutionReconciliationReport(passed=False, status=<DailyExecutionStatus.FAIL: 'FAIL'>, metrics=DailyExecutionMet...expected_vs_observed_paper_or_live_records', 'no_order_submission_performed', 'no_live_trading_authorization_granted']).passed
2026-05-28T07:53:38.5646832Z 1 failed, 1039 passed, 1 skipped, 6 warnings in 10.10s
2026-05-28T07:53:39.0478201Z ##[error]Process completed with exit code 1.
2026-05-28T07:53:39.0597901Z Post job cleanup.
2026-05-28T07:53:39.1629387Z [command]/usr/bin/git version
2026-05-28T07:53:39.1668930Z git version 2.54.0
2026-05-28T07:53:39.1712066Z Temporarily overriding HOME='/home/runner/work/_temp/0e903fac-8198-49ac-83d4-083e47367869' before making global git config changes
2026-05-28T07:53:39.1713254Z Adding repository directory to the temporary git global config as a safe directory
2026-05-28T07:53:39.1727634Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-05-28T07:53:39.1768979Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-05-28T07:53:39.1805774Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
```

```text
2026-05-28T07:53:38.5643370Z =========================== short test summary info ============================
2026-05-28T07:53:38.5644362Z FAILED tests/test_daily_execution_reconciliation.py::test_daily_execution_reconciliation_can_warn_on_missing_observed_record - AssertionError: assert False
2026-05-28T07:53:38.5645768Z  +  where False = DailyExecutionReconciliationReport(passed=False, status=<DailyExecutionStatus.FAIL: 'FAIL'>, metrics=DailyExecutionMet...expected_vs_observed_paper_or_live_records', 'no_order_submission_performed', 'no_live_trading_authorization_granted']).passed
2026-05-28T07:53:38.5646832Z 1 failed, 1039 passed, 1 skipped, 6 warnings in 10.10s
2026-05-28T07:53:39.0478201Z ##[error]Process completed with exit code 1.
2026-05-28T07:53:39.0597901Z Post job cleanup.
2026-05-28T07:53:39.1629387Z [command]/usr/bin/git version
2026-05-28T07:53:39.1668930Z git version 2.54.0
2026-05-28T07:53:39.1712066Z Temporarily overriding HOME='/home/runner/work/_temp/0e903fac-8198-49ac-83d4-083e47367869' before making global git config changes
2026-05-28T07:53:39.1713254Z Adding repository directory to the temporary git global config as a safe directory
2026-05-28T07:53:39.1727634Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-05-28T07:53:39.1768979Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-05-28T07:53:39.1805774Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-05-28T07:53:39.2054910Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-05-28T07:53:39.2083138Z http.https://github.com/.extraheader
2026-05-28T07:53:39.2096344Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

## CI

- Run ID: `26562124307`
- Branch: `main`
- Commit: `c56aae4afaac`
- Title: Merge pull request #87 from yalcinkadir/daily-reconciliation-workflow
- Created: 2026-05-28T07:53:06Z
- Updated: 2026-05-28T07:53:50Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26562124307

### Failed job: Pytest

- Job ID: `78247464045`
- Started: 2026-05-28T07:53:09Z
- Completed: 2026-05-28T07:53:49Z
- Failed steps: 22. Full regression suite

#### Error context

```text
2026-05-28T07:53:46.8678327Z ........................................................................ [ 82%]
2026-05-28T07:53:46.9072259Z ........................................................................ [ 89%]
2026-05-28T07:53:47.1070899Z ........................................................................ [ 96%]
2026-05-28T07:53:47.4332910Z .................................                                        [100%]
2026-05-28T07:53:47.4333567Z =================================== FAILURES ===================================
2026-05-28T07:53:47.4334245Z ___ test_daily_execution_reconciliation_can_warn_on_missing_observed_record ____
2026-05-28T07:53:47.4334699Z 
2026-05-28T07:53:47.4335019Z     def test_daily_execution_reconciliation_can_warn_on_missing_observed_record():
2026-05-28T07:53:47.4335617Z         report = reconcile_daily_execution(
2026-05-28T07:53:47.4336031Z             expected_records=[_expected()],
2026-05-28T07:53:47.4336424Z             observed_records=[],
2026-05-28T07:53:47.4337080Z             config=DailyExecutionReconciliationConfig(require_observed_for_each_expected=False),
2026-05-28T07:53:47.4337598Z         )
2026-05-28T07:53:47.4337801Z     
2026-05-28T07:53:47.4338022Z >       assert report.passed
2026-05-28T07:53:47.4338552Z E       AssertionError: assert False
```

```text
2026-05-28T07:53:47.4337080Z             config=DailyExecutionReconciliationConfig(require_observed_for_each_expected=False),
2026-05-28T07:53:47.4337598Z         )
2026-05-28T07:53:47.4337801Z     
2026-05-28T07:53:47.4338022Z >       assert report.passed
2026-05-28T07:53:47.4338552Z E       AssertionError: assert False
2026-05-28T07:53:47.4339677Z E        +  where False = DailyExecutionReconciliationReport(passed=False, status=<DailyExecutionStatus.FAIL: 'FAIL'>, metrics=DailyExecutionMet...expected_vs_observed_paper_or_live_records', 'no_order_submission_performed', 'no_live_trading_authorization_granted']).passed
2026-05-28T07:53:47.4340985Z 
2026-05-28T07:53:47.4341186Z tests/test_daily_execution_reconciliation.py:78: AssertionError
2026-05-28T07:53:47.4341609Z =============================== warnings summary ===============================
2026-05-28T07:53:47.4342336Z tests/test_jwt_auth.py::test_create_and_validate_token
2026-05-28T07:53:47.4342748Z tests/test_security_layer.py::test_metrics_accepts_admin_token
2026-05-28T07:53:47.4343379Z tests/test_security_layer.py::test_viewer_cannot_access_metrics
2026-05-28T07:53:47.4344417Z   /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/jwt/api_jwt.py:147: InsecureKeyLengthWarning: The HMAC key is 18 bytes long, which is below the minimum recommended length of 32 bytes for SHA256. See RFC 7518 Section 3.2.
2026-05-28T07:53:47.4345339Z     return self._jws.encode(
2026-05-28T07:53:47.4345508Z 
2026-05-28T07:53:47.4345669Z tests/test_jwt_auth.py::test_create_and_validate_token
```

```text
2026-05-28T07:53:47.4338022Z >       assert report.passed
2026-05-28T07:53:47.4338552Z E       AssertionError: assert False
2026-05-28T07:53:47.4339677Z E        +  where False = DailyExecutionReconciliationReport(passed=False, status=<DailyExecutionStatus.FAIL: 'FAIL'>, metrics=DailyExecutionMet...expected_vs_observed_paper_or_live_records', 'no_order_submission_performed', 'no_live_trading_authorization_granted']).passed
2026-05-28T07:53:47.4340985Z 
2026-05-28T07:53:47.4341186Z tests/test_daily_execution_reconciliation.py:78: AssertionError
2026-05-28T07:53:47.4341609Z =============================== warnings summary ===============================
2026-05-28T07:53:47.4342336Z tests/test_jwt_auth.py::test_create_and_validate_token
2026-05-28T07:53:47.4342748Z tests/test_security_layer.py::test_metrics_accepts_admin_token
2026-05-28T07:53:47.4343379Z tests/test_security_layer.py::test_viewer_cannot_access_metrics
2026-05-28T07:53:47.4344417Z   /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/jwt/api_jwt.py:147: InsecureKeyLengthWarning: The HMAC key is 18 bytes long, which is below the minimum recommended length of 32 bytes for SHA256. See RFC 7518 Section 3.2.
2026-05-28T07:53:47.4345339Z     return self._jws.encode(
2026-05-28T07:53:47.4345508Z 
2026-05-28T07:53:47.4345669Z tests/test_jwt_auth.py::test_create_and_validate_token
2026-05-28T07:53:47.4346072Z tests/test_security_layer.py::test_metrics_accepts_admin_token
2026-05-28T07:53:47.4346500Z tests/test_security_layer.py::test_viewer_cannot_access_metrics
2026-05-28T07:53:47.4347449Z   /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/jwt/api_jwt.py:368: InsecureKeyLengthWarning: The HMAC key is 18 bytes long, which is below the minimum recommended length of 32 bytes for SHA256. See RFC 7518 Section 3.2.
```

```text
2026-05-28T07:53:47.4348536Z     decoded = self.decode_complete(
2026-05-28T07:53:47.4348732Z 
2026-05-28T07:53:47.4348959Z -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2026-05-28T07:53:47.4349437Z =========================== short test summary info ============================
2026-05-28T07:53:47.4350174Z FAILED tests/test_daily_execution_reconciliation.py::test_daily_execution_reconciliation_can_warn_on_missing_observed_record - AssertionError: assert False
2026-05-28T07:53:47.4351601Z  +  where False = DailyExecutionReconciliationReport(passed=False, status=<DailyExecutionStatus.FAIL: 'FAIL'>, metrics=DailyExecutionMet...expected_vs_observed_paper_or_live_records', 'no_order_submission_performed', 'no_live_trading_authorization_granted']).passed
2026-05-28T07:53:47.4352772Z 1 failed, 1039 passed, 1 skipped, 6 warnings in 9.24s
2026-05-28T07:53:47.6848445Z ##[error]Process completed with exit code 1.
2026-05-28T07:53:47.6958521Z Post job cleanup.
2026-05-28T07:53:47.7943541Z [command]/usr/bin/git version
2026-05-28T07:53:47.7982071Z git version 2.54.0
2026-05-28T07:53:47.8024136Z Temporarily overriding HOME='/home/runner/work/_temp/b598269d-cb3a-4c50-8a48-65e680e8f262' before making global git config changes
2026-05-28T07:53:47.8025311Z Adding repository directory to the temporary git global config as a safe directory
2026-05-28T07:53:47.8038837Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-05-28T07:53:47.8078748Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-05-28T07:53:47.8112301Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
```

```text
2026-05-28T07:53:47.4349437Z =========================== short test summary info ============================
2026-05-28T07:53:47.4350174Z FAILED tests/test_daily_execution_reconciliation.py::test_daily_execution_reconciliation_can_warn_on_missing_observed_record - AssertionError: assert False
2026-05-28T07:53:47.4351601Z  +  where False = DailyExecutionReconciliationReport(passed=False, status=<DailyExecutionStatus.FAIL: 'FAIL'>, metrics=DailyExecutionMet...expected_vs_observed_paper_or_live_records', 'no_order_submission_performed', 'no_live_trading_authorization_granted']).passed
2026-05-28T07:53:47.4352772Z 1 failed, 1039 passed, 1 skipped, 6 warnings in 9.24s
2026-05-28T07:53:47.6848445Z ##[error]Process completed with exit code 1.
2026-05-28T07:53:47.6958521Z Post job cleanup.
2026-05-28T07:53:47.7943541Z [command]/usr/bin/git version
2026-05-28T07:53:47.7982071Z git version 2.54.0
2026-05-28T07:53:47.8024136Z Temporarily overriding HOME='/home/runner/work/_temp/b598269d-cb3a-4c50-8a48-65e680e8f262' before making global git config changes
2026-05-28T07:53:47.8025311Z Adding repository directory to the temporary git global config as a safe directory
2026-05-28T07:53:47.8038837Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-05-28T07:53:47.8078748Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-05-28T07:53:47.8112301Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-05-28T07:53:47.8360554Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-05-28T07:53:47.8386348Z http.https://github.com/.extraheader
2026-05-28T07:53:47.8399432Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

## Decision Engine Tests

- Run ID: `26561954955`
- Branch: `daily-reconciliation-workflow`
- Commit: `5b0809ab41c3`
- Title: Add C5 daily execution reconciliation workflow
- Created: 2026-05-28T07:49:21Z
- Updated: 2026-05-28T07:49:53Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26561954955

### Failed job: tests

- Job ID: `78246898015`
- Started: 2026-05-28T07:49:24Z
- Completed: 2026-05-28T07:49:52Z
- Failed steps: 5. Run pytest

#### Error context

```text
2026-05-28T07:49:50.4517177Z ........................................................................ [ 82%]
2026-05-28T07:49:50.4834458Z ........................................................................ [ 89%]
2026-05-28T07:49:50.7075957Z ........................................................................ [ 96%]
2026-05-28T07:49:50.9403092Z .................................                                        [100%]
2026-05-28T07:49:50.9403814Z =================================== FAILURES ===================================
2026-05-28T07:49:50.9404349Z ___ test_daily_execution_reconciliation_can_warn_on_missing_observed_record ____
2026-05-28T07:49:50.9404710Z 
2026-05-28T07:49:50.9404976Z     def test_daily_execution_reconciliation_can_warn_on_missing_observed_record():
2026-05-28T07:49:50.9405446Z         report = reconcile_daily_execution(
2026-05-28T07:49:50.9405794Z             expected_records=[_expected()],
2026-05-28T07:49:50.9406092Z             observed_records=[],
2026-05-28T07:49:50.9406632Z             config=DailyExecutionReconciliationConfig(require_observed_for_each_expected=False),
2026-05-28T07:49:50.9407144Z         )
2026-05-28T07:49:50.9407324Z     
2026-05-28T07:49:50.9407513Z >       assert report.passed
2026-05-28T07:49:50.9407789Z E       AssertionError: assert False
```

```text
2026-05-28T07:49:50.9406632Z             config=DailyExecutionReconciliationConfig(require_observed_for_each_expected=False),
2026-05-28T07:49:50.9407144Z         )
2026-05-28T07:49:50.9407324Z     
2026-05-28T07:49:50.9407513Z >       assert report.passed
2026-05-28T07:49:50.9407789Z E       AssertionError: assert False
2026-05-28T07:49:50.9409067Z E        +  where False = DailyExecutionReconciliationReport(passed=False, status=<DailyExecutionStatus.FAIL: 'FAIL'>, metrics=DailyExecutionMet...expected_vs_observed_paper_or_live_records', 'no_order_submission_performed', 'no_live_trading_authorization_granted']).passed
2026-05-28T07:49:50.9410258Z 
2026-05-28T07:49:50.9410452Z tests/test_daily_execution_reconciliation.py:78: AssertionError
2026-05-28T07:49:50.9410894Z =============================== warnings summary ===============================
2026-05-28T07:49:50.9411427Z tests/test_jwt_auth.py::test_create_and_validate_token
2026-05-28T07:49:50.9411869Z tests/test_security_layer.py::test_metrics_accepts_admin_token
2026-05-28T07:49:50.9412907Z tests/test_security_layer.py::test_viewer_cannot_access_metrics
2026-05-28T07:49:50.9414084Z   /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/jwt/api_jwt.py:147: InsecureKeyLengthWarning: The HMAC key is 18 bytes long, which is below the minimum recommended length of 32 bytes for SHA256. See RFC 7518 Section 3.2.
2026-05-28T07:49:50.9415147Z     return self._jws.encode(
2026-05-28T07:49:50.9415315Z 
2026-05-28T07:49:50.9415470Z tests/test_jwt_auth.py::test_create_and_validate_token
```

```text
2026-05-28T07:49:50.9407513Z >       assert report.passed
2026-05-28T07:49:50.9407789Z E       AssertionError: assert False
2026-05-28T07:49:50.9409067Z E        +  where False = DailyExecutionReconciliationReport(passed=False, status=<DailyExecutionStatus.FAIL: 'FAIL'>, metrics=DailyExecutionMet...expected_vs_observed_paper_or_live_records', 'no_order_submission_performed', 'no_live_trading_authorization_granted']).passed
2026-05-28T07:49:50.9410258Z 
2026-05-28T07:49:50.9410452Z tests/test_daily_execution_reconciliation.py:78: AssertionError
2026-05-28T07:49:50.9410894Z =============================== warnings summary ===============================
2026-05-28T07:49:50.9411427Z tests/test_jwt_auth.py::test_create_and_validate_token
2026-05-28T07:49:50.9411869Z tests/test_security_layer.py::test_metrics_accepts_admin_token
2026-05-28T07:49:50.9412907Z tests/test_security_layer.py::test_viewer_cannot_access_metrics
2026-05-28T07:49:50.9414084Z   /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/jwt/api_jwt.py:147: InsecureKeyLengthWarning: The HMAC key is 18 bytes long, which is below the minimum recommended length of 32 bytes for SHA256. See RFC 7518 Section 3.2.
2026-05-28T07:49:50.9415147Z     return self._jws.encode(
2026-05-28T07:49:50.9415315Z 
2026-05-28T07:49:50.9415470Z tests/test_jwt_auth.py::test_create_and_validate_token
2026-05-28T07:49:50.9415904Z tests/test_security_layer.py::test_metrics_accepts_admin_token
2026-05-28T07:49:50.9416368Z tests/test_security_layer.py::test_viewer_cannot_access_metrics
2026-05-28T07:49:50.9417501Z   /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/jwt/api_jwt.py:368: InsecureKeyLengthWarning: The HMAC key is 18 bytes long, which is below the minimum recommended length of 32 bytes for SHA256. See RFC 7518 Section 3.2.
```

```text
2026-05-28T07:49:50.9418542Z     decoded = self.decode_complete(
2026-05-28T07:49:50.9418740Z 
2026-05-28T07:49:50.9418981Z -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2026-05-28T07:49:50.9419506Z =========================== short test summary info ============================
2026-05-28T07:49:50.9420377Z FAILED tests/test_daily_execution_reconciliation.py::test_daily_execution_reconciliation_can_warn_on_missing_observed_record - AssertionError: assert False
2026-05-28T07:49:50.9422094Z  +  where False = DailyExecutionReconciliationReport(passed=False, status=<DailyExecutionStatus.FAIL: 'FAIL'>, metrics=DailyExecutionMet...expected_vs_observed_paper_or_live_records', 'no_order_submission_performed', 'no_live_trading_authorization_granted']).passed
2026-05-28T07:49:50.9423535Z 1 failed, 1039 passed, 1 skipped, 6 warnings in 8.80s
2026-05-28T07:49:51.1189735Z ##[error]Process completed with exit code 1.
2026-05-28T07:49:51.1276325Z Post job cleanup.
2026-05-28T07:49:51.2101735Z [command]/usr/bin/git version
2026-05-28T07:49:51.2129586Z git version 2.54.0
2026-05-28T07:49:51.2161792Z Temporarily overriding HOME='/home/runner/work/_temp/75f55190-ce55-4164-aeb3-2d809febf5dd' before making global git config changes
2026-05-28T07:49:51.2162896Z Adding repository directory to the temporary git global config as a safe directory
2026-05-28T07:49:51.2172986Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-05-28T07:49:51.2200977Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-05-28T07:49:51.2229360Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
```

```text
2026-05-28T07:49:50.9419506Z =========================== short test summary info ============================
2026-05-28T07:49:50.9420377Z FAILED tests/test_daily_execution_reconciliation.py::test_daily_execution_reconciliation_can_warn_on_missing_observed_record - AssertionError: assert False
2026-05-28T07:49:50.9422094Z  +  where False = DailyExecutionReconciliationReport(passed=False, status=<DailyExecutionStatus.FAIL: 'FAIL'>, metrics=DailyExecutionMet...expected_vs_observed_paper_or_live_records', 'no_order_submission_performed', 'no_live_trading_authorization_granted']).passed
2026-05-28T07:49:50.9423535Z 1 failed, 1039 passed, 1 skipped, 6 warnings in 8.80s
2026-05-28T07:49:51.1189735Z ##[error]Process completed with exit code 1.
2026-05-28T07:49:51.1276325Z Post job cleanup.
2026-05-28T07:49:51.2101735Z [command]/usr/bin/git version
2026-05-28T07:49:51.2129586Z git version 2.54.0
2026-05-28T07:49:51.2161792Z Temporarily overriding HOME='/home/runner/work/_temp/75f55190-ce55-4164-aeb3-2d809febf5dd' before making global git config changes
2026-05-28T07:49:51.2162896Z Adding repository directory to the temporary git global config as a safe directory
2026-05-28T07:49:51.2172986Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-05-28T07:49:51.2200977Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-05-28T07:49:51.2229360Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-05-28T07:49:51.2418056Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-05-28T07:49:51.2435042Z http.https://github.com/.extraheader
2026-05-28T07:49:51.2445379Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

## CI

- Run ID: `26561954981`
- Branch: `daily-reconciliation-workflow`
- Commit: `5b0809ab41c3`
- Title: Add C5 daily execution reconciliation workflow
- Created: 2026-05-28T07:49:21Z
- Updated: 2026-05-28T07:50:05Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26561954981

### Failed job: Pytest

- Job ID: `78246898262`
- Started: 2026-05-28T07:49:24Z
- Completed: 2026-05-28T07:50:04Z
- Failed steps: 22. Full regression suite

#### Error context

```text
2026-05-28T07:50:01.9388001Z ........................................................................ [ 82%]
2026-05-28T07:50:01.9813377Z ........................................................................ [ 89%]
2026-05-28T07:50:02.1861426Z ........................................................................ [ 96%]
2026-05-28T07:50:02.5391541Z .................................                                        [100%]
2026-05-28T07:50:02.5392640Z =================================== FAILURES ===================================
2026-05-28T07:50:02.5394150Z ___ test_daily_execution_reconciliation_can_warn_on_missing_observed_record ____
2026-05-28T07:50:02.5394606Z 
2026-05-28T07:50:02.5394928Z     def test_daily_execution_reconciliation_can_warn_on_missing_observed_record():
2026-05-28T07:50:02.5395493Z         report = reconcile_daily_execution(
2026-05-28T07:50:02.5395888Z             expected_records=[_expected()],
2026-05-28T07:50:02.5396308Z             observed_records=[],
2026-05-28T07:50:02.5397017Z             config=DailyExecutionReconciliationConfig(require_observed_for_each_expected=False),
2026-05-28T07:50:02.5397724Z         )
2026-05-28T07:50:02.5398005Z     
2026-05-28T07:50:02.5398297Z >       assert report.passed
2026-05-28T07:50:02.5398676Z E       AssertionError: assert False
```

```text
2026-05-28T07:50:02.5397017Z             config=DailyExecutionReconciliationConfig(require_observed_for_each_expected=False),
2026-05-28T07:50:02.5397724Z         )
2026-05-28T07:50:02.5398005Z     
2026-05-28T07:50:02.5398297Z >       assert report.passed
2026-05-28T07:50:02.5398676Z E       AssertionError: assert False
2026-05-28T07:50:02.5400109Z E        +  where False = DailyExecutionReconciliationReport(passed=False, status=<DailyExecutionStatus.FAIL: 'FAIL'>, metrics=DailyExecutionMet...expected_vs_observed_paper_or_live_records', 'no_order_submission_performed', 'no_live_trading_authorization_granted']).passed
2026-05-28T07:50:02.5401098Z 
2026-05-28T07:50:02.5401287Z tests/test_daily_execution_reconciliation.py:78: AssertionError
2026-05-28T07:50:02.5401693Z =============================== warnings summary ===============================
2026-05-28T07:50:02.5402204Z tests/test_jwt_auth.py::test_create_and_validate_token
2026-05-28T07:50:02.5402597Z tests/test_security_layer.py::test_metrics_accepts_admin_token
2026-05-28T07:50:02.5403536Z tests/test_security_layer.py::test_viewer_cannot_access_metrics
2026-05-28T07:50:02.5404566Z   /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/jwt/api_jwt.py:147: InsecureKeyLengthWarning: The HMAC key is 18 bytes long, which is below the minimum recommended length of 32 bytes for SHA256. See RFC 7518 Section 3.2.
2026-05-28T07:50:02.5405461Z     return self._jws.encode(
2026-05-28T07:50:02.5405622Z 
2026-05-28T07:50:02.5405765Z tests/test_jwt_auth.py::test_create_and_validate_token
```

```text
2026-05-28T07:50:02.5398297Z >       assert report.passed
2026-05-28T07:50:02.5398676Z E       AssertionError: assert False
2026-05-28T07:50:02.5400109Z E        +  where False = DailyExecutionReconciliationReport(passed=False, status=<DailyExecutionStatus.FAIL: 'FAIL'>, metrics=DailyExecutionMet...expected_vs_observed_paper_or_live_records', 'no_order_submission_performed', 'no_live_trading_authorization_granted']).passed
2026-05-28T07:50:02.5401098Z 
2026-05-28T07:50:02.5401287Z tests/test_daily_execution_reconciliation.py:78: AssertionError
2026-05-28T07:50:02.5401693Z =============================== warnings summary ===============================
2026-05-28T07:50:02.5402204Z tests/test_jwt_auth.py::test_create_and_validate_token
2026-05-28T07:50:02.5402597Z tests/test_security_layer.py::test_metrics_accepts_admin_token
2026-05-28T07:50:02.5403536Z tests/test_security_layer.py::test_viewer_cannot_access_metrics
2026-05-28T07:50:02.5404566Z   /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/jwt/api_jwt.py:147: InsecureKeyLengthWarning: The HMAC key is 18 bytes long, which is below the minimum recommended length of 32 bytes for SHA256. See RFC 7518 Section 3.2.
2026-05-28T07:50:02.5405461Z     return self._jws.encode(
2026-05-28T07:50:02.5405622Z 
2026-05-28T07:50:02.5405765Z tests/test_jwt_auth.py::test_create_and_validate_token
2026-05-28T07:50:02.5406152Z tests/test_security_layer.py::test_metrics_accepts_admin_token
2026-05-28T07:50:02.5406562Z tests/test_security_layer.py::test_viewer_cannot_access_metrics
2026-05-28T07:50:02.5407495Z   /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/jwt/api_jwt.py:368: InsecureKeyLengthWarning: The HMAC key is 18 bytes long, which is below the minimum recommended length of 32 bytes for SHA256. See RFC 7518 Section 3.2.
```

```text
2026-05-28T07:50:02.5408367Z     decoded = self.decode_complete(
2026-05-28T07:50:02.5408537Z 
2026-05-28T07:50:02.5408767Z -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2026-05-28T07:50:02.5409237Z =========================== short test summary info ============================
2026-05-28T07:50:02.5409960Z FAILED tests/test_daily_execution_reconciliation.py::test_daily_execution_reconciliation_can_warn_on_missing_observed_record - AssertionError: assert False
2026-05-28T07:50:02.5411364Z  +  where False = DailyExecutionReconciliationReport(passed=False, status=<DailyExecutionStatus.FAIL: 'FAIL'>, metrics=DailyExecutionMet...expected_vs_observed_paper_or_live_records', 'no_order_submission_performed', 'no_live_trading_authorization_granted']).passed
2026-05-28T07:50:02.5412426Z 1 failed, 1039 passed, 1 skipped, 6 warnings in 9.24s
2026-05-28T07:50:02.8217276Z ##[error]Process completed with exit code 1.
2026-05-28T07:50:02.8333460Z Post job cleanup.
2026-05-28T07:50:02.9331235Z [command]/usr/bin/git version
2026-05-28T07:50:02.9371650Z git version 2.54.0
2026-05-28T07:50:02.9422111Z Temporarily overriding HOME='/home/runner/work/_temp/74f46cc5-ebfe-44a2-8fd2-aa4e4372a515' before making global git config changes
2026-05-28T07:50:02.9423572Z Adding repository directory to the temporary git global config as a safe directory
2026-05-28T07:50:02.9428713Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-05-28T07:50:02.9467777Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-05-28T07:50:02.9503844Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
```

```text
2026-05-28T07:50:02.5409237Z =========================== short test summary info ============================
2026-05-28T07:50:02.5409960Z FAILED tests/test_daily_execution_reconciliation.py::test_daily_execution_reconciliation_can_warn_on_missing_observed_record - AssertionError: assert False
2026-05-28T07:50:02.5411364Z  +  where False = DailyExecutionReconciliationReport(passed=False, status=<DailyExecutionStatus.FAIL: 'FAIL'>, metrics=DailyExecutionMet...expected_vs_observed_paper_or_live_records', 'no_order_submission_performed', 'no_live_trading_authorization_granted']).passed
2026-05-28T07:50:02.5412426Z 1 failed, 1039 passed, 1 skipped, 6 warnings in 9.24s
2026-05-28T07:50:02.8217276Z ##[error]Process completed with exit code 1.
2026-05-28T07:50:02.8333460Z Post job cleanup.
2026-05-28T07:50:02.9331235Z [command]/usr/bin/git version
2026-05-28T07:50:02.9371650Z git version 2.54.0
2026-05-28T07:50:02.9422111Z Temporarily overriding HOME='/home/runner/work/_temp/74f46cc5-ebfe-44a2-8fd2-aa4e4372a515' before making global git config changes
2026-05-28T07:50:02.9423572Z Adding repository directory to the temporary git global config as a safe directory
2026-05-28T07:50:02.9428713Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-05-28T07:50:02.9467777Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-05-28T07:50:02.9503844Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-05-28T07:50:02.9749929Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-05-28T07:50:02.9774841Z http.https://github.com/.extraheader
2026-05-28T07:50:02.9787187Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

## CI

- Run ID: `26560210009`
- Branch: `feature/c4-order-reconciliation`
- Commit: `9747adcc567f`
- Title: Add C4 order reconciliation engine
- Created: 2026-05-28T07:08:36Z
- Updated: 2026-05-28T07:09:13Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26560210009

### Failed job: Pytest

- Job ID: `78241116679`
- Started: 2026-05-28T07:08:39Z
- Completed: 2026-05-28T07:09:12Z
- Failed steps: 22. Full regression suite

#### Error context

```text
2026-05-28T07:09:07.3003355Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-05-28T07:09:07.3003680Z   POLYGON_API_KEY: test-key
2026-05-28T07:09:07.3003904Z ##[endgroup]
2026-05-28T07:09:10.5093899Z 
2026-05-28T07:09:10.5094391Z ==================================== ERRORS ====================================
2026-05-28T07:09:10.5094947Z _____________ ERROR collecting tests/test_order_reconciliation.py ______________
2026-05-28T07:09:10.5095723Z ImportError while importing test module '/home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_order_reconciliation.py'.
2026-05-28T07:09:10.5096460Z Hint: make sure your test modules/packages have valid Python names.
2026-05-28T07:09:10.5096795Z Traceback:
2026-05-28T07:09:10.5097174Z /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/importlib/__init__.py:126: in import_module
2026-05-28T07:09:10.5097689Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-05-28T07:09:10.5098016Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-05-28T07:09:10.5098313Z tests/test_order_reconciliation.py:2: in <module>
2026-05-28T07:09:10.5098627Z     from src.execution.reconciliation import (
2026-05-28T07:09:10.5099008Z E   ModuleNotFoundError: No module named 'src.execution.reconciliation'
2026-05-28T07:09:10.5099433Z =========================== short test summary info ============================
```

```text
2026-05-28T07:09:07.3003680Z   POLYGON_API_KEY: test-key
2026-05-28T07:09:07.3003904Z ##[endgroup]
2026-05-28T07:09:10.5093899Z 
2026-05-28T07:09:10.5094391Z ==================================== ERRORS ====================================
2026-05-28T07:09:10.5094947Z _____________ ERROR collecting tests/test_order_reconciliation.py ______________
2026-05-28T07:09:10.5095723Z ImportError while importing test module '/home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_order_reconciliation.py'.
2026-05-28T07:09:10.5096460Z Hint: make sure your test modules/packages have valid Python names.
2026-05-28T07:09:10.5096795Z Traceback:
2026-05-28T07:09:10.5097174Z /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/importlib/__init__.py:126: in import_module
2026-05-28T07:09:10.5097689Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-05-28T07:09:10.5098016Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-05-28T07:09:10.5098313Z tests/test_order_reconciliation.py:2: in <module>
2026-05-28T07:09:10.5098627Z     from src.execution.reconciliation import (
2026-05-28T07:09:10.5099008Z E   ModuleNotFoundError: No module named 'src.execution.reconciliation'
2026-05-28T07:09:10.5099433Z =========================== short test summary info ============================
2026-05-28T07:09:10.5099770Z ERROR tests/test_order_reconciliation.py
```

```text
2026-05-28T07:09:07.3003904Z ##[endgroup]
2026-05-28T07:09:10.5093899Z 
2026-05-28T07:09:10.5094391Z ==================================== ERRORS ====================================
2026-05-28T07:09:10.5094947Z _____________ ERROR collecting tests/test_order_reconciliation.py ______________
2026-05-28T07:09:10.5095723Z ImportError while importing test module '/home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_order_reconciliation.py'.
2026-05-28T07:09:10.5096460Z Hint: make sure your test modules/packages have valid Python names.
2026-05-28T07:09:10.5096795Z Traceback:
2026-05-28T07:09:10.5097174Z /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/importlib/__init__.py:126: in import_module
2026-05-28T07:09:10.5097689Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-05-28T07:09:10.5098016Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-05-28T07:09:10.5098313Z tests/test_order_reconciliation.py:2: in <module>
2026-05-28T07:09:10.5098627Z     from src.execution.reconciliation import (
2026-05-28T07:09:10.5099008Z E   ModuleNotFoundError: No module named 'src.execution.reconciliation'
2026-05-28T07:09:10.5099433Z =========================== short test summary info ============================
2026-05-28T07:09:10.5099770Z ERROR tests/test_order_reconciliation.py
2026-05-28T07:09:10.5100344Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
```

```text
2026-05-28T07:09:10.5094391Z ==================================== ERRORS ====================================
2026-05-28T07:09:10.5094947Z _____________ ERROR collecting tests/test_order_reconciliation.py ______________
2026-05-28T07:09:10.5095723Z ImportError while importing test module '/home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_order_reconciliation.py'.
2026-05-28T07:09:10.5096460Z Hint: make sure your test modules/packages have valid Python names.
2026-05-28T07:09:10.5096795Z Traceback:
2026-05-28T07:09:10.5097174Z /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/importlib/__init__.py:126: in import_module
2026-05-28T07:09:10.5097689Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-05-28T07:09:10.5098016Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-05-28T07:09:10.5098313Z tests/test_order_reconciliation.py:2: in <module>
2026-05-28T07:09:10.5098627Z     from src.execution.reconciliation import (
2026-05-28T07:09:10.5099008Z E   ModuleNotFoundError: No module named 'src.execution.reconciliation'
2026-05-28T07:09:10.5099433Z =========================== short test summary info ============================
2026-05-28T07:09:10.5099770Z ERROR tests/test_order_reconciliation.py
2026-05-28T07:09:10.5100344Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-05-28T07:09:10.5100748Z 1 error in 2.81s
2026-05-28T07:09:10.7197945Z ##[error]Process completed with exit code 2.
```

```text
2026-05-28T07:09:10.5097689Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-05-28T07:09:10.5098016Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-05-28T07:09:10.5098313Z tests/test_order_reconciliation.py:2: in <module>
2026-05-28T07:09:10.5098627Z     from src.execution.reconciliation import (
2026-05-28T07:09:10.5099008Z E   ModuleNotFoundError: No module named 'src.execution.reconciliation'
2026-05-28T07:09:10.5099433Z =========================== short test summary info ============================
2026-05-28T07:09:10.5099770Z ERROR tests/test_order_reconciliation.py
2026-05-28T07:09:10.5100344Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-05-28T07:09:10.5100748Z 1 error in 2.81s
2026-05-28T07:09:10.7197945Z ##[error]Process completed with exit code 2.
2026-05-28T07:09:10.7302883Z Post job cleanup.
2026-05-28T07:09:10.8274601Z [command]/usr/bin/git version
2026-05-28T07:09:10.8318414Z git version 2.54.0
2026-05-28T07:09:10.8359836Z Temporarily overriding HOME='/home/runner/work/_temp/c19690e0-4fc0-46f0-b20d-dfd4ec549768' before making global git config changes
2026-05-28T07:09:10.8361274Z Adding repository directory to the temporary git global config as a safe directory
2026-05-28T07:09:10.8366546Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
```

```text
2026-05-28T07:09:10.5098313Z tests/test_order_reconciliation.py:2: in <module>
2026-05-28T07:09:10.5098627Z     from src.execution.reconciliation import (
2026-05-28T07:09:10.5099008Z E   ModuleNotFoundError: No module named 'src.execution.reconciliation'
2026-05-28T07:09:10.5099433Z =========================== short test summary info ============================
2026-05-28T07:09:10.5099770Z ERROR tests/test_order_reconciliation.py
2026-05-28T07:09:10.5100344Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-05-28T07:09:10.5100748Z 1 error in 2.81s
2026-05-28T07:09:10.7197945Z ##[error]Process completed with exit code 2.
2026-05-28T07:09:10.7302883Z Post job cleanup.
2026-05-28T07:09:10.8274601Z [command]/usr/bin/git version
2026-05-28T07:09:10.8318414Z git version 2.54.0
2026-05-28T07:09:10.8359836Z Temporarily overriding HOME='/home/runner/work/_temp/c19690e0-4fc0-46f0-b20d-dfd4ec549768' before making global git config changes
2026-05-28T07:09:10.8361274Z Adding repository directory to the temporary git global config as a safe directory
2026-05-28T07:09:10.8366546Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-05-28T07:09:10.8402147Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-05-28T07:09:10.8435736Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
```

```text
2026-05-28T07:09:10.5099433Z =========================== short test summary info ============================
2026-05-28T07:09:10.5099770Z ERROR tests/test_order_reconciliation.py
2026-05-28T07:09:10.5100344Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-05-28T07:09:10.5100748Z 1 error in 2.81s
2026-05-28T07:09:10.7197945Z ##[error]Process completed with exit code 2.
2026-05-28T07:09:10.7302883Z Post job cleanup.
2026-05-28T07:09:10.8274601Z [command]/usr/bin/git version
2026-05-28T07:09:10.8318414Z git version 2.54.0
2026-05-28T07:09:10.8359836Z Temporarily overriding HOME='/home/runner/work/_temp/c19690e0-4fc0-46f0-b20d-dfd4ec549768' before making global git config changes
2026-05-28T07:09:10.8361274Z Adding repository directory to the temporary git global config as a safe directory
2026-05-28T07:09:10.8366546Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-05-28T07:09:10.8402147Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-05-28T07:09:10.8435736Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-05-28T07:09:10.8676192Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-05-28T07:09:10.8701141Z http.https://github.com/.extraheader
2026-05-28T07:09:10.8714641Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

## Decision Engine Tests

- Run ID: `26560209959`
- Branch: `feature/c4-order-reconciliation`
- Commit: `9747adcc567f`
- Title: Add C4 order reconciliation engine
- Created: 2026-05-28T07:08:36Z
- Updated: 2026-05-28T07:09:06Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26560209959

### Failed job: tests

- Job ID: `78241116377`
- Started: 2026-05-28T07:08:39Z
- Completed: 2026-05-28T07:09:05Z
- Failed steps: 5. Run pytest

#### Error context

```text
2026-05-28T07:08:58.8194783Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-05-28T07:08:58.8195185Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-05-28T07:08:58.8195528Z ##[endgroup]
2026-05-28T07:09:04.0682829Z 
2026-05-28T07:09:04.0683404Z ==================================== ERRORS ====================================
2026-05-28T07:09:04.0684341Z _____________ ERROR collecting tests/test_order_reconciliation.py ______________
2026-05-28T07:09:04.0685774Z ImportError while importing test module '/home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_order_reconciliation.py'.
2026-05-28T07:09:04.0687205Z Hint: make sure your test modules/packages have valid Python names.
2026-05-28T07:09:04.0687858Z Traceback:
2026-05-28T07:09:04.0688927Z /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/importlib/__init__.py:126: in import_module
2026-05-28T07:09:04.0689914Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-05-28T07:09:04.0690573Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-05-28T07:09:04.0691186Z tests/test_order_reconciliation.py:2: in <module>
2026-05-28T07:09:04.0691988Z     from src.execution.reconciliation import (
2026-05-28T07:09:04.0692790Z E   ModuleNotFoundError: No module named 'src.execution.reconciliation'
2026-05-28T07:09:04.0693948Z =========================== short test summary info ============================
```

```text
2026-05-28T07:08:58.8195185Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-05-28T07:08:58.8195528Z ##[endgroup]
2026-05-28T07:09:04.0682829Z 
2026-05-28T07:09:04.0683404Z ==================================== ERRORS ====================================
2026-05-28T07:09:04.0684341Z _____________ ERROR collecting tests/test_order_reconciliation.py ______________
2026-05-28T07:09:04.0685774Z ImportError while importing test module '/home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_order_reconciliation.py'.
2026-05-28T07:09:04.0687205Z Hint: make sure your test modules/packages have valid Python names.
2026-05-28T07:09:04.0687858Z Traceback:
2026-05-28T07:09:04.0688927Z /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/importlib/__init__.py:126: in import_module
2026-05-28T07:09:04.0689914Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-05-28T07:09:04.0690573Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-05-28T07:09:04.0691186Z tests/test_order_reconciliation.py:2: in <module>
2026-05-28T07:09:04.0691988Z     from src.execution.reconciliation import (
2026-05-28T07:09:04.0692790Z E   ModuleNotFoundError: No module named 'src.execution.reconciliation'
2026-05-28T07:09:04.0693948Z =========================== short test summary info ============================
2026-05-28T07:09:04.0694574Z ERROR tests/test_order_reconciliation.py
```

```text
2026-05-28T07:08:58.8195528Z ##[endgroup]
2026-05-28T07:09:04.0682829Z 
2026-05-28T07:09:04.0683404Z ==================================== ERRORS ====================================
2026-05-28T07:09:04.0684341Z _____________ ERROR collecting tests/test_order_reconciliation.py ______________
2026-05-28T07:09:04.0685774Z ImportError while importing test module '/home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_order_reconciliation.py'.
2026-05-28T07:09:04.0687205Z Hint: make sure your test modules/packages have valid Python names.
2026-05-28T07:09:04.0687858Z Traceback:
2026-05-28T07:09:04.0688927Z /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/importlib/__init__.py:126: in import_module
2026-05-28T07:09:04.0689914Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-05-28T07:09:04.0690573Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-05-28T07:09:04.0691186Z tests/test_order_reconciliation.py:2: in <module>
2026-05-28T07:09:04.0691988Z     from src.execution.reconciliation import (
2026-05-28T07:09:04.0692790Z E   ModuleNotFoundError: No module named 'src.execution.reconciliation'
2026-05-28T07:09:04.0693948Z =========================== short test summary info ============================
2026-05-28T07:09:04.0694574Z ERROR tests/test_order_reconciliation.py
2026-05-28T07:09:04.0695059Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
```

```text
2026-05-28T07:09:04.0683404Z ==================================== ERRORS ====================================
2026-05-28T07:09:04.0684341Z _____________ ERROR collecting tests/test_order_reconciliation.py ______________
2026-05-28T07:09:04.0685774Z ImportError while importing test module '/home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_order_reconciliation.py'.
2026-05-28T07:09:04.0687205Z Hint: make sure your test modules/packages have valid Python names.
2026-05-28T07:09:04.0687858Z Traceback:
2026-05-28T07:09:04.0688927Z /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/importlib/__init__.py:126: in import_module
2026-05-28T07:09:04.0689914Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-05-28T07:09:04.0690573Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-05-28T07:09:04.0691186Z tests/test_order_reconciliation.py:2: in <module>
2026-05-28T07:09:04.0691988Z     from src.execution.reconciliation import (
2026-05-28T07:09:04.0692790Z E   ModuleNotFoundError: No module named 'src.execution.reconciliation'
2026-05-28T07:09:04.0693948Z =========================== short test summary info ============================
2026-05-28T07:09:04.0694574Z ERROR tests/test_order_reconciliation.py
2026-05-28T07:09:04.0695059Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-05-28T07:09:04.0695424Z 1 error in 4.19s
2026-05-28T07:09:04.2208896Z ##[error]Process completed with exit code 2.
```

```text
2026-05-28T07:09:04.0689914Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-05-28T07:09:04.0690573Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-05-28T07:09:04.0691186Z tests/test_order_reconciliation.py:2: in <module>
2026-05-28T07:09:04.0691988Z     from src.execution.reconciliation import (
2026-05-28T07:09:04.0692790Z E   ModuleNotFoundError: No module named 'src.execution.reconciliation'
2026-05-28T07:09:04.0693948Z =========================== short test summary info ============================
2026-05-28T07:09:04.0694574Z ERROR tests/test_order_reconciliation.py
2026-05-28T07:09:04.0695059Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-05-28T07:09:04.0695424Z 1 error in 4.19s
2026-05-28T07:09:04.2208896Z ##[error]Process completed with exit code 2.
2026-05-28T07:09:04.2327517Z Post job cleanup.
2026-05-28T07:09:04.3299293Z [command]/usr/bin/git version
2026-05-28T07:09:04.3334694Z git version 2.54.0
2026-05-28T07:09:04.3380611Z Temporarily overriding HOME='/home/runner/work/_temp/5725ecc5-0b2b-4a6c-8608-fd325d443c68' before making global git config changes
2026-05-28T07:09:04.3382083Z Adding repository directory to the temporary git global config as a safe directory
2026-05-28T07:09:04.3387471Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
```

```text
2026-05-28T07:09:04.0691186Z tests/test_order_reconciliation.py:2: in <module>
2026-05-28T07:09:04.0691988Z     from src.execution.reconciliation import (
2026-05-28T07:09:04.0692790Z E   ModuleNotFoundError: No module named 'src.execution.reconciliation'
2026-05-28T07:09:04.0693948Z =========================== short test summary info ============================
2026-05-28T07:09:04.0694574Z ERROR tests/test_order_reconciliation.py
2026-05-28T07:09:04.0695059Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-05-28T07:09:04.0695424Z 1 error in 4.19s
2026-05-28T07:09:04.2208896Z ##[error]Process completed with exit code 2.
2026-05-28T07:09:04.2327517Z Post job cleanup.
2026-05-28T07:09:04.3299293Z [command]/usr/bin/git version
2026-05-28T07:09:04.3334694Z git version 2.54.0
2026-05-28T07:09:04.3380611Z Temporarily overriding HOME='/home/runner/work/_temp/5725ecc5-0b2b-4a6c-8608-fd325d443c68' before making global git config changes
2026-05-28T07:09:04.3382083Z Adding repository directory to the temporary git global config as a safe directory
2026-05-28T07:09:04.3387471Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-05-28T07:09:04.3422503Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-05-28T07:09:04.3454235Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
```

```text
2026-05-28T07:09:04.0693948Z =========================== short test summary info ============================
2026-05-28T07:09:04.0694574Z ERROR tests/test_order_reconciliation.py
2026-05-28T07:09:04.0695059Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-05-28T07:09:04.0695424Z 1 error in 4.19s
2026-05-28T07:09:04.2208896Z ##[error]Process completed with exit code 2.
2026-05-28T07:09:04.2327517Z Post job cleanup.
2026-05-28T07:09:04.3299293Z [command]/usr/bin/git version
2026-05-28T07:09:04.3334694Z git version 2.54.0
2026-05-28T07:09:04.3380611Z Temporarily overriding HOME='/home/runner/work/_temp/5725ecc5-0b2b-4a6c-8608-fd325d443c68' before making global git config changes
2026-05-28T07:09:04.3382083Z Adding repository directory to the temporary git global config as a safe directory
2026-05-28T07:09:04.3387471Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-05-28T07:09:04.3422503Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-05-28T07:09:04.3454235Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-05-28T07:09:04.3675305Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-05-28T07:09:04.3698600Z http.https://github.com/.extraheader
2026-05-28T07:09:04.3710790Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

## Decision Engine Tests

- Run ID: `26560207571`
- Branch: `feature/c4-order-reconciliation`
- Commit: `9747adcc567f`
- Title: Remove duplicate reconciliation module
- Created: 2026-05-28T07:08:32Z
- Updated: 2026-05-28T07:08:58Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26560207571

### Failed job: tests

- Job ID: `78241108770`
- Started: 2026-05-28T07:08:35Z
- Completed: 2026-05-28T07:08:57Z
- Failed steps: 5. Run pytest

#### Error context

```text
2026-05-28T07:08:50.3422767Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-05-28T07:08:50.3423129Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-05-28T07:08:50.3423457Z ##[endgroup]
2026-05-28T07:08:54.6793834Z 
2026-05-28T07:08:54.6794379Z ==================================== ERRORS ====================================
2026-05-28T07:08:54.6795045Z _____________ ERROR collecting tests/test_order_reconciliation.py ______________
2026-05-28T07:08:54.6795972Z ImportError while importing test module '/home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_order_reconciliation.py'.
2026-05-28T07:08:54.6796767Z Hint: make sure your test modules/packages have valid Python names.
2026-05-28T07:08:54.6797093Z Traceback:
2026-05-28T07:08:54.6797470Z /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/importlib/__init__.py:126: in import_module
2026-05-28T07:08:54.6797978Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-05-28T07:08:54.6798313Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-05-28T07:08:54.6798623Z tests/test_order_reconciliation.py:2: in <module>
2026-05-28T07:08:54.6798956Z     from src.execution.reconciliation import (
2026-05-28T07:08:54.6799348Z E   ModuleNotFoundError: No module named 'src.execution.reconciliation'
2026-05-28T07:08:54.6799761Z =========================== short test summary info ============================
```

```text
2026-05-28T07:08:50.3423129Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-05-28T07:08:50.3423457Z ##[endgroup]
2026-05-28T07:08:54.6793834Z 
2026-05-28T07:08:54.6794379Z ==================================== ERRORS ====================================
2026-05-28T07:08:54.6795045Z _____________ ERROR collecting tests/test_order_reconciliation.py ______________
2026-05-28T07:08:54.6795972Z ImportError while importing test module '/home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_order_reconciliation.py'.
2026-05-28T07:08:54.6796767Z Hint: make sure your test modules/packages have valid Python names.
2026-05-28T07:08:54.6797093Z Traceback:
2026-05-28T07:08:54.6797470Z /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/importlib/__init__.py:126: in import_module
2026-05-28T07:08:54.6797978Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-05-28T07:08:54.6798313Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-05-28T07:08:54.6798623Z tests/test_order_reconciliation.py:2: in <module>
2026-05-28T07:08:54.6798956Z     from src.execution.reconciliation import (
2026-05-28T07:08:54.6799348Z E   ModuleNotFoundError: No module named 'src.execution.reconciliation'
2026-05-28T07:08:54.6799761Z =========================== short test summary info ============================
2026-05-28T07:08:54.6800456Z ERROR tests/test_order_reconciliation.py
```

```text
2026-05-28T07:08:50.3423457Z ##[endgroup]
2026-05-28T07:08:54.6793834Z 
2026-05-28T07:08:54.6794379Z ==================================== ERRORS ====================================
2026-05-28T07:08:54.6795045Z _____________ ERROR collecting tests/test_order_reconciliation.py ______________
2026-05-28T07:08:54.6795972Z ImportError while importing test module '/home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_order_reconciliation.py'.
2026-05-28T07:08:54.6796767Z Hint: make sure your test modules/packages have valid Python names.
2026-05-28T07:08:54.6797093Z Traceback:
2026-05-28T07:08:54.6797470Z /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/importlib/__init__.py:126: in import_module
2026-05-28T07:08:54.6797978Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-05-28T07:08:54.6798313Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-05-28T07:08:54.6798623Z tests/test_order_reconciliation.py:2: in <module>
2026-05-28T07:08:54.6798956Z     from src.execution.reconciliation import (
2026-05-28T07:08:54.6799348Z E   ModuleNotFoundError: No module named 'src.execution.reconciliation'
2026-05-28T07:08:54.6799761Z =========================== short test summary info ============================
2026-05-28T07:08:54.6800456Z ERROR tests/test_order_reconciliation.py
2026-05-28T07:08:54.6800805Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
```

```text
2026-05-28T07:08:54.6794379Z ==================================== ERRORS ====================================
2026-05-28T07:08:54.6795045Z _____________ ERROR collecting tests/test_order_reconciliation.py ______________
2026-05-28T07:08:54.6795972Z ImportError while importing test module '/home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_order_reconciliation.py'.
2026-05-28T07:08:54.6796767Z Hint: make sure your test modules/packages have valid Python names.
2026-05-28T07:08:54.6797093Z Traceback:
2026-05-28T07:08:54.6797470Z /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/importlib/__init__.py:126: in import_module
2026-05-28T07:08:54.6797978Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-05-28T07:08:54.6798313Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-05-28T07:08:54.6798623Z tests/test_order_reconciliation.py:2: in <module>
2026-05-28T07:08:54.6798956Z     from src.execution.reconciliation import (
2026-05-28T07:08:54.6799348Z E   ModuleNotFoundError: No module named 'src.execution.reconciliation'
2026-05-28T07:08:54.6799761Z =========================== short test summary info ============================
2026-05-28T07:08:54.6800456Z ERROR tests/test_order_reconciliation.py
2026-05-28T07:08:54.6800805Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-05-28T07:08:54.6801131Z 1 error in 3.58s
2026-05-28T07:08:54.8897446Z ##[error]Process completed with exit code 2.
```

```text
2026-05-28T07:08:54.6797978Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-05-28T07:08:54.6798313Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-05-28T07:08:54.6798623Z tests/test_order_reconciliation.py:2: in <module>
2026-05-28T07:08:54.6798956Z     from src.execution.reconciliation import (
2026-05-28T07:08:54.6799348Z E   ModuleNotFoundError: No module named 'src.execution.reconciliation'
2026-05-28T07:08:54.6799761Z =========================== short test summary info ============================
2026-05-28T07:08:54.6800456Z ERROR tests/test_order_reconciliation.py
2026-05-28T07:08:54.6800805Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-05-28T07:08:54.6801131Z 1 error in 3.58s
2026-05-28T07:08:54.8897446Z ##[error]Process completed with exit code 2.
2026-05-28T07:08:54.9006522Z Post job cleanup.
2026-05-28T07:08:54.9923565Z [command]/usr/bin/git version
2026-05-28T07:08:54.9956334Z git version 2.54.0
2026-05-28T07:08:54.9996637Z Temporarily overriding HOME='/home/runner/work/_temp/092667a2-cfeb-4a0d-8791-b24e68285c9f' before making global git config changes
2026-05-28T07:08:54.9997890Z Adding repository directory to the temporary git global config as a safe directory
2026-05-28T07:08:55.0011359Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
```

```text
2026-05-28T07:08:54.6798623Z tests/test_order_reconciliation.py:2: in <module>
2026-05-28T07:08:54.6798956Z     from src.execution.reconciliation import (
2026-05-28T07:08:54.6799348Z E   ModuleNotFoundError: No module named 'src.execution.reconciliation'
2026-05-28T07:08:54.6799761Z =========================== short test summary info ============================
2026-05-28T07:08:54.6800456Z ERROR tests/test_order_reconciliation.py
2026-05-28T07:08:54.6800805Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-05-28T07:08:54.6801131Z 1 error in 3.58s
2026-05-28T07:08:54.8897446Z ##[error]Process completed with exit code 2.
2026-05-28T07:08:54.9006522Z Post job cleanup.
2026-05-28T07:08:54.9923565Z [command]/usr/bin/git version
2026-05-28T07:08:54.9956334Z git version 2.54.0
2026-05-28T07:08:54.9996637Z Temporarily overriding HOME='/home/runner/work/_temp/092667a2-cfeb-4a0d-8791-b24e68285c9f' before making global git config changes
2026-05-28T07:08:54.9997890Z Adding repository directory to the temporary git global config as a safe directory
2026-05-28T07:08:55.0011359Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-05-28T07:08:55.0042400Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-05-28T07:08:55.0070893Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
```

```text
2026-05-28T07:08:54.6799761Z =========================== short test summary info ============================
2026-05-28T07:08:54.6800456Z ERROR tests/test_order_reconciliation.py
2026-05-28T07:08:54.6800805Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-05-28T07:08:54.6801131Z 1 error in 3.58s
2026-05-28T07:08:54.8897446Z ##[error]Process completed with exit code 2.
2026-05-28T07:08:54.9006522Z Post job cleanup.
2026-05-28T07:08:54.9923565Z [command]/usr/bin/git version
2026-05-28T07:08:54.9956334Z git version 2.54.0
2026-05-28T07:08:54.9996637Z Temporarily overriding HOME='/home/runner/work/_temp/092667a2-cfeb-4a0d-8791-b24e68285c9f' before making global git config changes
2026-05-28T07:08:54.9997890Z Adding repository directory to the temporary git global config as a safe directory
2026-05-28T07:08:55.0011359Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-05-28T07:08:55.0042400Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-05-28T07:08:55.0070893Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-05-28T07:08:55.0247511Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-05-28T07:08:55.0267891Z http.https://github.com/.extraheader
2026-05-28T07:08:55.0279044Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```
