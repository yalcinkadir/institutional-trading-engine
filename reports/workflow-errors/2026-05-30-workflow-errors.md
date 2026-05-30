# GitHub Actions Workflow Error Report

Generated: 2026-05-30 08:05 UTC
Repository: `yalcinkadir/institutional-trading-engine`
Filter since: 2026-05-29 08:05 UTC
Failed runs included: 10

## Decision Engine Tests

- Run ID: `26671110839`
- Branch: `main`
- Commit: `f095590b90ab`
- Title: Wire daily evidence run record validator tests into CI
- Created: 2026-05-30T01:46:56Z
- Updated: 2026-05-30T01:47:29Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26671110839

### Failed job: tests

- Job ID: `78614381771`
- Started: 2026-05-30T01:46:58Z
- Completed: 2026-05-30T01:47:28Z
- Failed steps: 5. Run pytest

#### Error context

```text
2026-05-30T01:47:26.3000596Z ........................................................................ [ 87%]
2026-05-30T01:47:26.5051066Z ........................................................................ [ 93%]
2026-05-30T01:47:26.5449323Z ........................................................................ [ 98%]
2026-05-30T01:47:26.8383547Z ................                                                         [100%]
2026-05-30T01:47:26.8384018Z =================================== FAILURES ===================================
2026-05-30T01:47:26.8385324Z _________ TestDataPersistence.test_decision_log_path_not_in_gitignore __________
2026-05-30T01:47:26.8385840Z 
2026-05-30T01:47:26.8386174Z self = <test_priority_fixes.TestDataPersistence object at 0x7f19fed98290>
2026-05-30T01:47:26.8386580Z 
2026-05-30T01:47:26.8386791Z     def test_decision_log_path_not_in_gitignore(self):
2026-05-30T01:47:26.8387164Z         gitignore = Path(".gitignore")
2026-05-30T01:47:26.8387453Z         if not gitignore.exists():
2026-05-30T01:47:26.8387713Z             return
2026-05-30T01:47:26.8387939Z         content = gitignore.read_text()
2026-05-30T01:47:26.8388244Z         # data/ should NOT be in gitignore
2026-05-30T01:47:26.8388527Z >       assert "data/" not in content, (
```

```text
2026-05-30T01:47:26.8388244Z         # data/ should NOT be in gitignore
2026-05-30T01:47:26.8388527Z >       assert "data/" not in content, (
2026-05-30T01:47:26.8389159Z             "data/ is in .gitignore â decision log will be lost on every run"
2026-05-30T01:47:26.8389508Z         )
2026-05-30T01:47:26.8389903Z E       AssertionError: data/ is in .gitignore â decision log will be lost on every run
2026-05-30T01:47:26.8390375Z E       assert 'data/' not in '# Python\n_...\n.vscode/\n'
2026-05-30T01:47:26.8390951Z E         
2026-05-30T01:47:26.8391157Z E         'data/' is contained here:
2026-05-30T01:47:26.8391412Z E           e/
2026-05-30T01:47:26.8391612Z E           cache/
2026-05-30T01:47:26.8391812Z E           data/raw/
2026-05-30T01:47:26.8392023Z E           data/live/
2026-05-30T01:47:26.8392241Z E           data/private/
2026-05-30T01:47:26.8392470Z E           data/vendor/
2026-05-30T01:47:26.8392686Z E           evidence/
2026-05-30T01:47:26.8392887Z E           lockbox/
```

```text
2026-05-30T01:47:26.8401185Z E           .DS_Store
2026-05-30T01:47:26.8401396Z E           .idea/
2026-05-30T01:47:26.8401604Z E           .vscode/
2026-05-30T01:47:26.8401737Z 
2026-05-30T01:47:26.8401871Z tests/test_priority_fixes.py:372: AssertionError
2026-05-30T01:47:26.8402238Z =============================== warnings summary ===============================
2026-05-30T01:47:26.8402776Z ../../../../../opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/fastapi/testclient.py:1
2026-05-30T01:47:26.8403838Z   /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
2026-05-30T01:47:26.8405263Z     from starlette.testclient import TestClient as TestClient  # noqa
2026-05-30T01:47:26.8405628Z 
2026-05-30T01:47:26.8405875Z tests/test_jwt_auth.py::test_create_and_validate_token
2026-05-30T01:47:26.8406269Z tests/test_security_layer.py::test_metrics_accepts_admin_token
2026-05-30T01:47:26.8406683Z tests/test_security_layer.py::test_viewer_cannot_access_metrics
2026-05-30T01:47:26.8407654Z   /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/jwt/api_jwt.py:147: InsecureKeyLengthWarning: The HMAC key is 18 bytes long, which is below the minimum recommended length of 32 bytes for SHA256. See RFC 7518 Section 3.2.
2026-05-30T01:47:26.8408574Z     return self._jws.encode(
2026-05-30T01:47:26.8408723Z
```

```text
2026-05-30T01:47:26.8411640Z     decoded = self.decode_complete(
2026-05-30T01:47:26.8411819Z 
2026-05-30T01:47:26.8412042Z -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2026-05-30T01:47:26.8412489Z =========================== short test summary info ============================
2026-05-30T01:47:26.8413452Z FAILED tests/test_priority_fixes.py::TestDataPersistence::test_decision_log_path_not_in_gitignore - AssertionError: data/ is in .gitignore â decision log will be lost on every run
2026-05-30T01:47:26.8414383Z assert 'data/' not in '# Python\n_...\n.vscode/\n'
2026-05-30T01:47:26.8414695Z   
2026-05-30T01:47:26.8414897Z   'data/' is contained here:
2026-05-30T01:47:26.8415136Z     e/
2026-05-30T01:47:26.8415322Z     cache/
2026-05-30T01:47:26.8415511Z     data/raw/
2026-05-30T01:47:26.8415716Z     data/live/
2026-05-30T01:47:26.8415920Z     data/private/
2026-05-30T01:47:26.8416123Z     data/vendor/
2026-05-30T01:47:26.8416319Z     evidence/
2026-05-30T01:47:26.8416507Z     lockbox/
```

```text
2026-05-30T01:47:26.8423201Z     .DS_Store
2026-05-30T01:47:26.8423391Z     .idea/
2026-05-30T01:47:26.8423572Z     .vscode/
2026-05-30T01:47:26.8423817Z 1 failed, 1310 passed, 1 skipped, 7 warnings in 10.78s
2026-05-30T01:47:27.0728952Z ##[error]Process completed with exit code 1.
2026-05-30T01:47:27.0845752Z Post job cleanup.
2026-05-30T01:47:27.1843761Z [command]/usr/bin/git version
2026-05-30T01:47:27.1880408Z git version 2.54.0
2026-05-30T01:47:27.1921995Z Temporarily overriding HOME='/home/runner/work/_temp/975828a9-75f8-402e-a744-bd403008ef84' before making global git config changes
2026-05-30T01:47:27.1923256Z Adding repository directory to the temporary git global config as a safe directory
2026-05-30T01:47:27.1929727Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-05-30T01:47:27.1983049Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-05-30T01:47:27.2017063Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-05-30T01:47:27.2255842Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-05-30T01:47:27.2279847Z http.https://github.com/.extraheader
2026-05-30T01:47:27.2291652Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

## Report Quality Validation

- Run ID: `26671110847`
- Branch: `main`
- Commit: `f095590b90ab`
- Title: Wire daily evidence run record validator tests into CI
- Created: 2026-05-30T01:46:56Z
- Updated: 2026-05-30T01:47:41Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26671110847

### Failed job: validate-reports (weekly)

- Job ID: `78614381790`
- Started: 2026-05-30T01:46:58Z
- Completed: 2026-05-30T01:47:18Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-05-30T01:47:15.9093589Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-05-30T01:47:15.9093970Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-05-30T01:47:15.9094392Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-05-30T01:47:15.9094718Z ##[endgroup]
2026-05-30T01:47:16.2878797Z Traceback (most recent call last):
2026-05-30T01:47:16.2885869Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 247, in <module>
2026-05-30T01:47:16.2887222Z     raise SystemExit(main())
2026-05-30T01:47:16.2887478Z                      ^^^^^^
2026-05-30T01:47:16.2888122Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 236, in main
2026-05-30T01:47:16.2888887Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-05-30T01:47:16.2889338Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-05-30T01:47:16.2890124Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 68, in write_report_text_guarded
2026-05-30T01:47:16.2890916Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-05-30T01:47:16.2891766Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-05-30T01:47:16.2892526Z     raise ReportOutputBoundaryError(
2026-05-30T01:47:16.2893468Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
```

```text
2026-05-30T01:47:16.2890916Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-05-30T01:47:16.2891766Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-05-30T01:47:16.2892526Z     raise ReportOutputBoundaryError(
2026-05-30T01:47:16.2893468Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-05-30T01:47:16.3105255Z ##[error]Process completed with exit code 1.
2026-05-30T01:47:16.3234238Z Post job cleanup.
2026-05-30T01:47:16.4236442Z [command]/usr/bin/git version
2026-05-30T01:47:16.4273445Z git version 2.54.0
2026-05-30T01:47:16.4317349Z Temporarily overriding HOME='/home/runner/work/_temp/b36e9048-7a6f-4f9f-8b4a-b32dc9219eb8' before making global git config changes
2026-05-30T01:47:16.4318203Z Adding repository directory to the temporary git global config as a safe directory
2026-05-30T01:47:16.4331626Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-05-30T01:47:16.4366858Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-05-30T01:47:16.4402349Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-05-30T01:47:16.4631681Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-05-30T01:47:16.4655940Z http.https://github.com/.extraheader
2026-05-30T01:47:16.4668488Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

### Failed job: validate-reports (postmarket)

- Job ID: `78614381794`
- Started: 2026-05-30T01:46:59Z
- Completed: 2026-05-30T01:47:40Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-05-30T01:47:18.0108329Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-05-30T01:47:18.0108716Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-05-30T01:47:18.0109128Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-05-30T01:47:18.0109458Z ##[endgroup]
2026-05-30T01:47:37.6793348Z Traceback (most recent call last):
2026-05-30T01:47:37.6795741Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-05-30T01:47:37.6807200Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 247, in <module>
2026-05-30T01:47:37.6808288Z     raise SystemExit(main())
2026-05-30T01:47:37.6808649Z                      ^^^^^^
2026-05-30T01:47:37.6809617Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 236, in main
2026-05-30T01:47:37.6810785Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-05-30T01:47:37.6811509Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-05-30T01:47:37.6812762Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 68, in write_report_text_guarded
2026-05-30T01:47:37.6814025Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-05-30T01:47:37.6815925Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-05-30T01:47:37.6817174Z     raise ReportOutputBoundaryError(
```

```text
2026-05-30T01:47:37.6817174Z     raise ReportOutputBoundaryError(
2026-05-30T01:47:37.6818747Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/postmarket-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-05-30T01:47:37.6821463Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-05-30T01:47:37.6823828Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-05-30T01:47:37.6825857Z WARNING: scanner metric loading failed: ModuleNotFoundError: No module named 'config'
2026-05-30T01:47:37.6826634Z WARNING: scanner_metrics_missing:MSFT
2026-05-30T01:47:37.6827065Z WARNING: scanner_metrics_missing:NVDA
2026-05-30T01:47:37.6827519Z WARNING: scanner_metrics_missing:META
2026-05-30T01:47:37.6827951Z WARNING: scanner_metrics_missing:AAPL
2026-05-30T01:47:37.6828374Z WARNING: scanner_metrics_missing:MU
2026-05-30T01:47:37.6828801Z WARNING: scanner_metrics_missing:QQQ
2026-05-30T01:47:37.6829211Z WARNING: scanner_metrics_missing:GLD
2026-05-30T01:47:37.6829625Z WARNING: scanner_metrics_missing:SLV
2026-05-30T01:47:37.7376686Z ##[error]Process completed with exit code 1.
2026-05-30T01:47:37.7493859Z Post job cleanup.
2026-05-30T01:47:37.8463263Z [command]/usr/bin/git version
```

```text
2026-05-30T01:47:37.6828374Z WARNING: scanner_metrics_missing:MU
2026-05-30T01:47:37.6828801Z WARNING: scanner_metrics_missing:QQQ
2026-05-30T01:47:37.6829211Z WARNING: scanner_metrics_missing:GLD
2026-05-30T01:47:37.6829625Z WARNING: scanner_metrics_missing:SLV
2026-05-30T01:47:37.7376686Z ##[error]Process completed with exit code 1.
2026-05-30T01:47:37.7493859Z Post job cleanup.
2026-05-30T01:47:37.8463263Z [command]/usr/bin/git version
2026-05-30T01:47:37.8501813Z git version 2.54.0
2026-05-30T01:47:37.8544825Z Temporarily overriding HOME='/home/runner/work/_temp/c5d76e98-baf2-46a6-927c-d03779dfb4a1' before making global git config changes
2026-05-30T01:47:37.8546069Z Adding repository directory to the temporary git global config as a safe directory
2026-05-30T01:47:37.8552571Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-05-30T01:47:37.8588670Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-05-30T01:47:37.8622478Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-05-30T01:47:37.8866579Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-05-30T01:47:37.8884860Z http.https://github.com/.extraheader
2026-05-30T01:47:37.8903227Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

### Failed job: validate-reports (premarket)

- Job ID: `78614381796`
- Started: 2026-05-30T01:46:58Z
- Completed: 2026-05-30T01:47:29Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-05-30T01:47:13.2944423Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-05-30T01:47:13.2944822Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-05-30T01:47:13.2945240Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-05-30T01:47:13.2945584Z ##[endgroup]
2026-05-30T01:47:28.4056292Z Traceback (most recent call last):
2026-05-30T01:47:28.4058281Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-05-30T01:47:28.4060560Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-05-30T01:47:28.4062623Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-05-30T01:47:28.4064284Z WARNING: scanner metric loading failed: ModuleNotFoundError: No module named 'config'
2026-05-30T01:47:28.4064950Z WARNING: scanner_metrics_missing:MSFT
2026-05-30T01:47:28.4065388Z WARNING: scanner_metrics_missing:NVDA
2026-05-30T01:47:28.4065794Z WARNING: scanner_metrics_missing:META
2026-05-30T01:47:28.4066198Z WARNING: scanner_metrics_missing:AAPL
2026-05-30T01:47:28.4066595Z WARNING: scanner_metrics_missing:MU
2026-05-30T01:47:28.4066997Z WARNING: scanner_metrics_missing:QQQ
2026-05-30T01:47:28.4067395Z WARNING: scanner_metrics_missing:GLD
```

```text
2026-05-30T01:47:28.4056292Z Traceback (most recent call last):
2026-05-30T01:47:28.4058281Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-05-30T01:47:28.4060560Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-05-30T01:47:28.4062623Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-05-30T01:47:28.4064284Z WARNING: scanner metric loading failed: ModuleNotFoundError: No module named 'config'
2026-05-30T01:47:28.4064950Z WARNING: scanner_metrics_missing:MSFT
2026-05-30T01:47:28.4065388Z WARNING: scanner_metrics_missing:NVDA
2026-05-30T01:47:28.4065794Z WARNING: scanner_metrics_missing:META
2026-05-30T01:47:28.4066198Z WARNING: scanner_metrics_missing:AAPL
2026-05-30T01:47:28.4066595Z WARNING: scanner_metrics_missing:MU
2026-05-30T01:47:28.4066997Z WARNING: scanner_metrics_missing:QQQ
2026-05-30T01:47:28.4067395Z WARNING: scanner_metrics_missing:GLD
2026-05-30T01:47:28.4067787Z WARNING: scanner_metrics_missing:SLV
2026-05-30T01:47:28.4076291Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 247, in <module>
2026-05-30T01:47:28.4077338Z     raise SystemExit(main())
2026-05-30T01:47:28.4077716Z                      ^^^^^^
```

```text
2026-05-30T01:47:28.4083168Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-05-30T01:47:28.4084647Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-05-30T01:47:28.4085791Z     raise ReportOutputBoundaryError(
2026-05-30T01:47:28.4087241Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/premarket-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-05-30T01:47:28.4668728Z ##[error]Process completed with exit code 1.
2026-05-30T01:47:28.4791706Z Post job cleanup.
2026-05-30T01:47:28.5790144Z [command]/usr/bin/git version
2026-05-30T01:47:28.5826912Z git version 2.54.0
2026-05-30T01:47:28.5867572Z Temporarily overriding HOME='/home/runner/work/_temp/3cd7cac7-70be-4a2f-a4e0-f9f958e38204' before making global git config changes
2026-05-30T01:47:28.5868532Z Adding repository directory to the temporary git global config as a safe directory
2026-05-30T01:47:28.5882487Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-05-30T01:47:28.5918062Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-05-30T01:47:28.5950750Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-05-30T01:47:28.6199934Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-05-30T01:47:28.6231404Z http.https://github.com/.extraheader
2026-05-30T01:47:28.6245074Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

## Report Quality Validation

- Run ID: `26671014779`
- Branch: `main`
- Commit: `a8aef499dcd3`
- Title: Add daily evidence run record schema validator tests
- Created: 2026-05-30T01:42:47Z
- Updated: 2026-05-30T01:43:31Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26671014779

### Failed job: validate-reports (premarket)

- Job ID: `78614112550`
- Started: 2026-05-30T01:42:49Z
- Completed: 2026-05-30T01:43:31Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-05-30T01:43:07.6344549Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-05-30T01:43:07.6344918Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-05-30T01:43:07.6345343Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-05-30T01:43:07.6345653Z ##[endgroup]
2026-05-30T01:43:28.7418893Z Traceback (most recent call last):
2026-05-30T01:43:28.7420589Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-05-30T01:43:28.7422705Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-05-30T01:43:28.7424587Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-05-30T01:43:28.7425854Z WARNING: scanner metric loading failed: ModuleNotFoundError: No module named 'config'
2026-05-30T01:43:28.7426502Z WARNING: scanner_metrics_missing:MSFT
2026-05-30T01:43:28.7426985Z WARNING: scanner_metrics_missing:NVDA
2026-05-30T01:43:28.7427391Z WARNING: scanner_metrics_missing:META
2026-05-30T01:43:28.7427860Z WARNING: scanner_metrics_missing:AAPL
2026-05-30T01:43:28.7428345Z WARNING: scanner_metrics_missing:MU
2026-05-30T01:43:28.7428797Z WARNING: scanner_metrics_missing:QQQ
2026-05-30T01:43:28.7429392Z WARNING: scanner_metrics_missing:GLD
```

```text
2026-05-30T01:43:28.7418893Z Traceback (most recent call last):
2026-05-30T01:43:28.7420589Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-05-30T01:43:28.7422705Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-05-30T01:43:28.7424587Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-05-30T01:43:28.7425854Z WARNING: scanner metric loading failed: ModuleNotFoundError: No module named 'config'
2026-05-30T01:43:28.7426502Z WARNING: scanner_metrics_missing:MSFT
2026-05-30T01:43:28.7426985Z WARNING: scanner_metrics_missing:NVDA
2026-05-30T01:43:28.7427391Z WARNING: scanner_metrics_missing:META
2026-05-30T01:43:28.7427860Z WARNING: scanner_metrics_missing:AAPL
2026-05-30T01:43:28.7428345Z WARNING: scanner_metrics_missing:MU
2026-05-30T01:43:28.7428797Z WARNING: scanner_metrics_missing:QQQ
2026-05-30T01:43:28.7429392Z WARNING: scanner_metrics_missing:GLD
2026-05-30T01:43:28.7429757Z WARNING: scanner_metrics_missing:SLV
2026-05-30T01:43:28.7436447Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 247, in <module>
2026-05-30T01:43:28.7437121Z     raise SystemExit(main())
2026-05-30T01:43:28.7437356Z                      ^^^^^^
```

```text
2026-05-30T01:43:28.7440956Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-05-30T01:43:28.7441730Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-05-30T01:43:28.7442419Z     raise ReportOutputBoundaryError(
2026-05-30T01:43:28.7443313Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/premarket-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-05-30T01:43:28.8020191Z ##[error]Process completed with exit code 1.
2026-05-30T01:43:28.8129793Z Post job cleanup.
2026-05-30T01:43:28.9034202Z [command]/usr/bin/git version
2026-05-30T01:43:28.9066853Z git version 2.54.0
2026-05-30T01:43:28.9106703Z Temporarily overriding HOME='/home/runner/work/_temp/36eb1593-56ec-435e-9d1d-4bcad3d1128a' before making global git config changes
2026-05-30T01:43:28.9107938Z Adding repository directory to the temporary git global config as a safe directory
2026-05-30T01:43:28.9121137Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-05-30T01:43:28.9152069Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-05-30T01:43:28.9178776Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-05-30T01:43:28.9358172Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-05-30T01:43:28.9379539Z http.https://github.com/.extraheader
2026-05-30T01:43:28.9390135Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

### Failed job: validate-reports (postmarket)

- Job ID: `78614112551`
- Started: 2026-05-30T01:42:49Z
- Completed: 2026-05-30T01:43:22Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-05-30T01:43:05.1039238Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-05-30T01:43:05.1039640Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-05-30T01:43:05.1040065Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-05-30T01:43:05.1040411Z ##[endgroup]
2026-05-30T01:43:21.5293471Z Traceback (most recent call last):
2026-05-30T01:43:21.5295648Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-05-30T01:43:21.5298693Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-05-30T01:43:21.5300864Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-05-30T01:43:21.5302305Z WARNING: scanner metric loading failed: ModuleNotFoundError: No module named 'config'
2026-05-30T01:43:21.5302998Z WARNING: scanner_metrics_missing:MSFT
2026-05-30T01:43:21.5303451Z WARNING: scanner_metrics_missing:NVDA
2026-05-30T01:43:21.5303864Z WARNING: scanner_metrics_missing:META
2026-05-30T01:43:21.5304266Z WARNING: scanner_metrics_missing:AAPL
2026-05-30T01:43:21.5304691Z WARNING: scanner_metrics_missing:MU
2026-05-30T01:43:21.5305102Z WARNING: scanner_metrics_missing:QQQ
2026-05-30T01:43:21.5305513Z WARNING: scanner_metrics_missing:GLD
```

```text
2026-05-30T01:43:21.5293471Z Traceback (most recent call last):
2026-05-30T01:43:21.5295648Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-05-30T01:43:21.5298693Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-05-30T01:43:21.5300864Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-05-30T01:43:21.5302305Z WARNING: scanner metric loading failed: ModuleNotFoundError: No module named 'config'
2026-05-30T01:43:21.5302998Z WARNING: scanner_metrics_missing:MSFT
2026-05-30T01:43:21.5303451Z WARNING: scanner_metrics_missing:NVDA
2026-05-30T01:43:21.5303864Z WARNING: scanner_metrics_missing:META
2026-05-30T01:43:21.5304266Z WARNING: scanner_metrics_missing:AAPL
2026-05-30T01:43:21.5304691Z WARNING: scanner_metrics_missing:MU
2026-05-30T01:43:21.5305102Z WARNING: scanner_metrics_missing:QQQ
2026-05-30T01:43:21.5305513Z WARNING: scanner_metrics_missing:GLD
2026-05-30T01:43:21.5305914Z WARNING: scanner_metrics_missing:SLV
2026-05-30T01:43:21.5314287Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 247, in <module>
2026-05-30T01:43:21.5315358Z     raise SystemExit(main())
2026-05-30T01:43:21.5315738Z                      ^^^^^^
```

```text
2026-05-30T01:43:21.5321679Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-05-30T01:43:21.5323017Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-05-30T01:43:21.5324183Z     raise ReportOutputBoundaryError(
2026-05-30T01:43:21.5325735Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/postmarket-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-05-30T01:43:21.5925844Z ##[error]Process completed with exit code 1.
2026-05-30T01:43:21.6049181Z Post job cleanup.
2026-05-30T01:43:21.7024867Z [command]/usr/bin/git version
2026-05-30T01:43:21.7061688Z git version 2.54.0
2026-05-30T01:43:21.7104460Z Temporarily overriding HOME='/home/runner/work/_temp/ed3c7a57-5c89-4c81-b61c-d70360648c52' before making global git config changes
2026-05-30T01:43:21.7105964Z Adding repository directory to the temporary git global config as a safe directory
2026-05-30T01:43:21.7119863Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-05-30T01:43:21.7160528Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-05-30T01:43:21.7194644Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-05-30T01:43:21.7438008Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-05-30T01:43:21.7460759Z http.https://github.com/.extraheader
2026-05-30T01:43:21.7472536Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

### Failed job: validate-reports (weekly)

- Job ID: `78614112574`
- Started: 2026-05-30T01:42:49Z
- Completed: 2026-05-30T01:43:10Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-05-30T01:43:07.9575142Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-05-30T01:43:07.9575534Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-05-30T01:43:07.9575966Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-05-30T01:43:07.9576295Z ##[endgroup]
2026-05-30T01:43:08.2645387Z Traceback (most recent call last):
2026-05-30T01:43:08.2652796Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 247, in <module>
2026-05-30T01:43:08.2653535Z     raise SystemExit(main())
2026-05-30T01:43:08.2653800Z                      ^^^^^^
2026-05-30T01:43:08.2654468Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 236, in main
2026-05-30T01:43:08.2655212Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-05-30T01:43:08.2657780Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-05-30T01:43:08.2659094Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 68, in write_report_text_guarded
2026-05-30T01:43:08.2659897Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-05-30T01:43:08.2660738Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-05-30T01:43:08.2661780Z     raise ReportOutputBoundaryError(
2026-05-30T01:43:08.2662712Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
```

```text
2026-05-30T01:43:08.2659897Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-05-30T01:43:08.2660738Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-05-30T01:43:08.2661780Z     raise ReportOutputBoundaryError(
2026-05-30T01:43:08.2662712Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-05-30T01:43:08.2902897Z ##[error]Process completed with exit code 1.
2026-05-30T01:43:08.3028815Z Post job cleanup.
2026-05-30T01:43:08.4029123Z [command]/usr/bin/git version
2026-05-30T01:43:08.4066184Z git version 2.54.0
2026-05-30T01:43:08.4108374Z Temporarily overriding HOME='/home/runner/work/_temp/cb485c4a-4768-495b-8420-e9149a93d638' before making global git config changes
2026-05-30T01:43:08.4109558Z Adding repository directory to the temporary git global config as a safe directory
2026-05-30T01:43:08.4122747Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-05-30T01:43:08.4160768Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-05-30T01:43:08.4196371Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-05-30T01:43:08.4443635Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-05-30T01:43:08.4470329Z http.https://github.com/.extraheader
2026-05-30T01:43:08.4484037Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

## Decision Engine Tests

- Run ID: `26671014785`
- Branch: `main`
- Commit: `a8aef499dcd3`
- Title: Add daily evidence run record schema validator tests
- Created: 2026-05-30T01:42:47Z
- Updated: 2026-05-30T01:43:20Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26671014785

### Failed job: tests

- Job ID: `78614112499`
- Started: 2026-05-30T01:42:49Z
- Completed: 2026-05-30T01:43:19Z
- Failed steps: 5. Run pytest

#### Error context

```text
2026-05-30T01:43:16.0428968Z ........................................................................ [ 87%]
2026-05-30T01:43:16.2557541Z ........................................................................ [ 93%]
2026-05-30T01:43:16.3001337Z ........................................................................ [ 98%]
2026-05-30T01:43:16.5508763Z ................                                                         [100%]
2026-05-30T01:43:16.5510637Z =================================== FAILURES ===================================
2026-05-30T01:43:16.5511938Z _________ TestDataPersistence.test_decision_log_path_not_in_gitignore __________
2026-05-30T01:43:16.5512535Z 
2026-05-30T01:43:16.5512904Z self = <test_priority_fixes.TestDataPersistence object at 0x7fe4c5be1f90>
2026-05-30T01:43:16.5513414Z 
2026-05-30T01:43:16.5513631Z     def test_decision_log_path_not_in_gitignore(self):
2026-05-30T01:43:16.5514202Z         gitignore = Path(".gitignore")
2026-05-30T01:43:16.5514652Z         if not gitignore.exists():
2026-05-30T01:43:16.5515044Z             return
2026-05-30T01:43:16.5515370Z         content = gitignore.read_text()
2026-05-30T01:43:16.5515799Z         # data/ should NOT be in gitignore
2026-05-30T01:43:16.5516224Z >       assert "data/" not in content, (
```

```text
2026-05-30T01:43:16.5515799Z         # data/ should NOT be in gitignore
2026-05-30T01:43:16.5516224Z >       assert "data/" not in content, (
2026-05-30T01:43:16.5517041Z             "data/ is in .gitignore â decision log will be lost on every run"
2026-05-30T01:43:16.5517562Z         )
2026-05-30T01:43:16.5518438Z E       AssertionError: data/ is in .gitignore â decision log will be lost on every run
2026-05-30T01:43:16.5519232Z E       assert 'data/' not in '# Python\n_...\n.vscode/\n'
2026-05-30T01:43:16.5519992Z E         
2026-05-30T01:43:16.5520300Z E         'data/' is contained here:
2026-05-30T01:43:16.5520677Z E           e/
2026-05-30T01:43:16.5520949Z E           cache/
2026-05-30T01:43:16.5521235Z E           data/raw/
2026-05-30T01:43:16.5521541Z E           data/live/
2026-05-30T01:43:16.5521855Z E           data/private/
2026-05-30T01:43:16.5522194Z E           data/vendor/
2026-05-30T01:43:16.5522512Z E           evidence/
2026-05-30T01:43:16.5522817Z E           lockbox/
```

```text
2026-05-30T01:43:16.5534048Z E           .DS_Store
2026-05-30T01:43:16.5534336Z E           .idea/
2026-05-30T01:43:16.5534615Z E           .vscode/
2026-05-30T01:43:16.5534794Z 
2026-05-30T01:43:16.5534984Z tests/test_priority_fixes.py:372: AssertionError
2026-05-30T01:43:16.5535493Z =============================== warnings summary ===============================
2026-05-30T01:43:16.5536298Z ../../../../../opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/fastapi/testclient.py:1
2026-05-30T01:43:16.5538119Z   /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
2026-05-30T01:43:16.5539807Z     from starlette.testclient import TestClient as TestClient  # noqa
2026-05-30T01:43:16.5540359Z 
2026-05-30T01:43:16.5540682Z tests/test_jwt_auth.py::test_create_and_validate_token
2026-05-30T01:43:16.5541290Z tests/test_security_layer.py::test_metrics_accepts_admin_token
2026-05-30T01:43:16.5541962Z tests/test_security_layer.py::test_viewer_cannot_access_metrics
2026-05-30T01:43:16.5543539Z   /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/jwt/api_jwt.py:147: InsecureKeyLengthWarning: The HMAC key is 18 bytes long, which is below the minimum recommended length of 32 bytes for SHA256. See RFC 7518 Section 3.2.
2026-05-30T01:43:16.5545005Z     return self._jws.encode(
2026-05-30T01:43:16.5545242Z
```

```text
2026-05-30T01:43:16.5550188Z     decoded = self.decode_complete(
2026-05-30T01:43:16.5550463Z 
2026-05-30T01:43:16.5550858Z -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2026-05-30T01:43:16.5551572Z =========================== short test summary info ============================
2026-05-30T01:43:16.5553080Z FAILED tests/test_priority_fixes.py::TestDataPersistence::test_decision_log_path_not_in_gitignore - AssertionError: data/ is in .gitignore â decision log will be lost on every run
2026-05-30T01:43:16.5554279Z assert 'data/' not in '# Python\n_...\n.vscode/\n'
2026-05-30T01:43:16.5554730Z   
2026-05-30T01:43:16.5555016Z   'data/' is contained here:
2026-05-30T01:43:16.5555362Z     e/
2026-05-30T01:43:16.5555623Z     cache/
2026-05-30T01:43:16.5555883Z     data/raw/
2026-05-30T01:43:16.5556170Z     data/live/
2026-05-30T01:43:16.5556454Z     data/private/
2026-05-30T01:43:16.5556760Z     data/vendor/
2026-05-30T01:43:16.5557056Z     evidence/
2026-05-30T01:43:16.5557331Z     lockbox/
```

```text
2026-05-30T01:43:16.5567438Z     .DS_Store
2026-05-30T01:43:16.5567709Z     .idea/
2026-05-30T01:43:16.5568165Z     .vscode/
2026-05-30T01:43:16.5568538Z 1 failed, 1310 passed, 1 skipped, 7 warnings in 10.69s
2026-05-30T01:43:16.7488277Z ##[error]Process completed with exit code 1.
2026-05-30T01:43:16.7606318Z Post job cleanup.
2026-05-30T01:43:16.8570016Z [command]/usr/bin/git version
2026-05-30T01:43:16.8605688Z git version 2.54.0
2026-05-30T01:43:16.8649211Z Temporarily overriding HOME='/home/runner/work/_temp/03857c93-179a-4a90-9ae6-edbad9a31c64' before making global git config changes
2026-05-30T01:43:16.8650869Z Adding repository directory to the temporary git global config as a safe directory
2026-05-30T01:43:16.8663139Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-05-30T01:43:16.8696970Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-05-30T01:43:16.8730796Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-05-30T01:43:16.8952756Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-05-30T01:43:16.8975961Z http.https://github.com/.extraheader
2026-05-30T01:43:16.8987678Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

## Decision Engine Tests

- Run ID: `26670991185`
- Branch: `main`
- Commit: `080e3ee901b9`
- Title: Add daily evidence run record schema validator
- Created: 2026-05-30T01:41:43Z
- Updated: 2026-05-30T01:42:09Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26670991185

### Failed job: tests

- Job ID: `78614043477`
- Started: 2026-05-30T01:41:46Z
- Completed: 2026-05-30T01:42:08Z
- Failed steps: 5. Run pytest

#### Error context

```text
2026-05-30T01:42:06.4941221Z ........................................................................ [ 88%]
2026-05-30T01:42:06.6534156Z ........................................................................ [ 93%]
2026-05-30T01:42:06.6757013Z ........................................................................ [ 99%]
2026-05-30T01:42:06.8931588Z .........                                                                [100%]
2026-05-30T01:42:06.8932174Z =================================== FAILURES ===================================
2026-05-30T01:42:06.8932937Z _________ TestDataPersistence.test_decision_log_path_not_in_gitignore __________
2026-05-30T01:42:06.8933208Z 
2026-05-30T01:42:06.8933387Z self = <test_priority_fixes.TestDataPersistence object at 0x7fa538326c10>
2026-05-30T01:42:06.8933640Z 
2026-05-30T01:42:06.8933766Z     def test_decision_log_path_not_in_gitignore(self):
2026-05-30T01:42:06.8934049Z         gitignore = Path(".gitignore")
2026-05-30T01:42:06.8934287Z         if not gitignore.exists():
2026-05-30T01:42:06.8934496Z             return
2026-05-30T01:42:06.8934685Z         content = gitignore.read_text()
2026-05-30T01:42:06.8934927Z         # data/ should NOT be in gitignore
2026-05-30T01:42:06.8935162Z >       assert "data/" not in content, (
```

```text
2026-05-30T01:42:06.8934927Z         # data/ should NOT be in gitignore
2026-05-30T01:42:06.8935162Z >       assert "data/" not in content, (
2026-05-30T01:42:06.8935769Z             "data/ is in .gitignore â decision log will be lost on every run"
2026-05-30T01:42:06.8936064Z         )
2026-05-30T01:42:06.8936400Z E       AssertionError: data/ is in .gitignore â decision log will be lost on every run
2026-05-30T01:42:06.8936794Z E       assert 'data/' not in '# Python\n_...\n.vscode/\n'
2026-05-30T01:42:06.8937315Z E         
2026-05-30T01:42:06.8937488Z E         'data/' is contained here:
2026-05-30T01:42:06.8937703Z E           e/
2026-05-30T01:42:06.8937869Z E           cache/
2026-05-30T01:42:06.8938043Z E           data/raw/
2026-05-30T01:42:06.8938225Z E           data/live/
2026-05-30T01:42:06.8938414Z E           data/private/
2026-05-30T01:42:06.8938609Z E           data/vendor/
2026-05-30T01:42:06.8938797Z E           evidence/
2026-05-30T01:42:06.8938982Z E           lockbox/
```

```text
2026-05-30T01:42:06.8944692Z E           .DS_Store
2026-05-30T01:42:06.8944805Z E           .idea/
2026-05-30T01:42:06.8944920Z E           .vscode/
2026-05-30T01:42:06.8944989Z 
2026-05-30T01:42:06.8945063Z tests/test_priority_fixes.py:372: AssertionError
2026-05-30T01:42:06.8945255Z =============================== warnings summary ===============================
2026-05-30T01:42:06.8945543Z ../../../../../opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/fastapi/testclient.py:1
2026-05-30T01:42:06.8946116Z   /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
2026-05-30T01:42:06.8946839Z     from starlette.testclient import TestClient as TestClient  # noqa
2026-05-30T01:42:06.8946991Z 
2026-05-30T01:42:06.8947172Z tests/test_jwt_auth.py::test_create_and_validate_token
2026-05-30T01:42:06.8947385Z tests/test_security_layer.py::test_metrics_accepts_admin_token
2026-05-30T01:42:06.8947607Z tests/test_security_layer.py::test_viewer_cannot_access_metrics
2026-05-30T01:42:06.8948112Z   /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/jwt/api_jwt.py:147: InsecureKeyLengthWarning: The HMAC key is 18 bytes long, which is below the minimum recommended length of 32 bytes for SHA256. See RFC 7518 Section 3.2.
2026-05-30T01:42:06.8948601Z     return self._jws.encode(
2026-05-30T01:42:06.8948688Z
```

```text
2026-05-30T01:42:06.8950414Z     decoded = self.decode_complete(
2026-05-30T01:42:06.8950509Z 
2026-05-30T01:42:06.8950640Z -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2026-05-30T01:42:06.8950884Z =========================== short test summary info ============================
2026-05-30T01:42:06.8951384Z FAILED tests/test_priority_fixes.py::TestDataPersistence::test_decision_log_path_not_in_gitignore - AssertionError: data/ is in .gitignore â decision log will be lost on every run
2026-05-30T01:42:06.8951786Z assert 'data/' not in '# Python\n_...\n.vscode/\n'
2026-05-30T01:42:06.8951952Z   
2026-05-30T01:42:06.8952063Z   'data/' is contained here:
2026-05-30T01:42:06.8952195Z     e/
2026-05-30T01:42:06.8952299Z     cache/
2026-05-30T01:42:06.8952406Z     data/raw/
2026-05-30T01:42:06.8952521Z     data/live/
2026-05-30T01:42:06.8952632Z     data/private/
2026-05-30T01:42:06.8952745Z     data/vendor/
2026-05-30T01:42:06.8952854Z     evidence/
2026-05-30T01:42:06.8952960Z     lockbox/
```

```text
2026-05-30T01:42:06.8956755Z     .DS_Store
2026-05-30T01:42:06.8956859Z     .idea/
2026-05-30T01:42:06.8956962Z     .vscode/
2026-05-30T01:42:06.8957097Z 1 failed, 1303 passed, 1 skipped, 7 warnings in 8.07s
2026-05-30T01:42:07.0571862Z ##[error]Process completed with exit code 1.
2026-05-30T01:42:07.0643813Z Post job cleanup.
2026-05-30T01:42:07.1228204Z [command]/usr/bin/git version
2026-05-30T01:42:07.1253676Z git version 2.54.0
2026-05-30T01:42:07.1277982Z Temporarily overriding HOME='/home/runner/work/_temp/eb939c2c-5285-41ca-b8f9-da4f6ba54937' before making global git config changes
2026-05-30T01:42:07.1278632Z Adding repository directory to the temporary git global config as a safe directory
2026-05-30T01:42:07.1287087Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-05-30T01:42:07.1313654Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-05-30T01:42:07.1337954Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-05-30T01:42:07.1505735Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-05-30T01:42:07.1520800Z http.https://github.com/.extraheader
2026-05-30T01:42:07.1529111Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

## Report Quality Validation

- Run ID: `26670991175`
- Branch: `main`
- Commit: `080e3ee901b9`
- Title: Add daily evidence run record schema validator
- Created: 2026-05-30T01:41:43Z
- Updated: 2026-05-30T01:42:23Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26670991175

### Failed job: validate-reports (premarket)

- Job ID: `78614043591`
- Started: 2026-05-30T01:41:45Z
- Completed: 2026-05-30T01:42:22Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-05-30T01:42:04.3551093Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-05-30T01:42:04.3551492Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-05-30T01:42:04.3551917Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-05-30T01:42:04.3552269Z ##[endgroup]
2026-05-30T01:42:20.6402953Z Traceback (most recent call last):
2026-05-30T01:42:20.6405316Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-05-30T01:42:20.6414805Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 247, in <module>
2026-05-30T01:42:20.6415845Z     raise SystemExit(main())
2026-05-30T01:42:20.6416234Z                      ^^^^^^
2026-05-30T01:42:20.6417181Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 236, in main
2026-05-30T01:42:20.6418328Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-05-30T01:42:20.6419008Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-05-30T01:42:20.6420161Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 68, in write_report_text_guarded
2026-05-30T01:42:20.6421338Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-05-30T01:42:20.6422627Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-05-30T01:42:20.6423781Z     raise ReportOutputBoundaryError(
```

```text
2026-05-30T01:42:20.6423781Z     raise ReportOutputBoundaryError(
2026-05-30T01:42:20.6425476Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/premarket-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-05-30T01:42:20.6428064Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-05-30T01:42:20.6430230Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-05-30T01:42:20.6432063Z WARNING: scanner metric loading failed: ModuleNotFoundError: No module named 'config'
2026-05-30T01:42:20.6432730Z WARNING: scanner_metrics_missing:MSFT
2026-05-30T01:42:20.6433141Z WARNING: scanner_metrics_missing:NVDA
2026-05-30T01:42:20.6433547Z WARNING: scanner_metrics_missing:META
2026-05-30T01:42:20.6433952Z WARNING: scanner_metrics_missing:AAPL
2026-05-30T01:42:20.6434512Z WARNING: scanner_metrics_missing:MU
2026-05-30T01:42:20.6434918Z WARNING: scanner_metrics_missing:QQQ
2026-05-30T01:42:20.6435331Z WARNING: scanner_metrics_missing:GLD
2026-05-30T01:42:20.6435728Z WARNING: scanner_metrics_missing:SLV
2026-05-30T01:42:20.7087482Z ##[error]Process completed with exit code 1.
2026-05-30T01:42:20.7213867Z Post job cleanup.
2026-05-30T01:42:20.8224397Z [command]/usr/bin/git version
```

```text
2026-05-30T01:42:20.6434512Z WARNING: scanner_metrics_missing:MU
2026-05-30T01:42:20.6434918Z WARNING: scanner_metrics_missing:QQQ
2026-05-30T01:42:20.6435331Z WARNING: scanner_metrics_missing:GLD
2026-05-30T01:42:20.6435728Z WARNING: scanner_metrics_missing:SLV
2026-05-30T01:42:20.7087482Z ##[error]Process completed with exit code 1.
2026-05-30T01:42:20.7213867Z Post job cleanup.
2026-05-30T01:42:20.8224397Z [command]/usr/bin/git version
2026-05-30T01:42:20.8261961Z git version 2.54.0
2026-05-30T01:42:20.8304208Z Temporarily overriding HOME='/home/runner/work/_temp/19ab62b8-0063-4ff7-9c86-bb74c9b8e3f6' before making global git config changes
2026-05-30T01:42:20.8305767Z Adding repository directory to the temporary git global config as a safe directory
2026-05-30T01:42:20.8311330Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-05-30T01:42:20.8358893Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-05-30T01:42:20.8395896Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-05-30T01:42:20.8668962Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-05-30T01:42:20.8696029Z http.https://github.com/.extraheader
2026-05-30T01:42:20.8708577Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

### Failed job: validate-reports (postmarket)

- Job ID: `78614043595`
- Started: 2026-05-30T01:41:45Z
- Completed: 2026-05-30T01:42:17Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-05-30T01:42:00.7970572Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-05-30T01:42:00.7970956Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-05-30T01:42:00.7971385Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-05-30T01:42:00.7971718Z ##[endgroup]
2026-05-30T01:42:15.8198869Z Traceback (most recent call last):
2026-05-30T01:42:15.8201432Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-05-30T01:42:15.8204748Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-05-30T01:42:15.8208434Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-05-30T01:42:15.8210622Z WARNING: scanner metric loading failed: ModuleNotFoundError: No module named 'config'
2026-05-30T01:42:15.8211564Z WARNING: scanner_metrics_missing:MSFT
2026-05-30T01:42:15.8212164Z WARNING: scanner_metrics_missing:NVDA
2026-05-30T01:42:15.8212735Z WARNING: scanner_metrics_missing:META
2026-05-30T01:42:15.8213304Z WARNING: scanner_metrics_missing:AAPL
2026-05-30T01:42:15.8213894Z WARNING: scanner_metrics_missing:MU
2026-05-30T01:42:15.8214462Z WARNING: scanner_metrics_missing:QQQ
2026-05-30T01:42:15.8214930Z WARNING: scanner_metrics_missing:GLD
```

```text
2026-05-30T01:42:15.8198869Z Traceback (most recent call last):
2026-05-30T01:42:15.8201432Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-05-30T01:42:15.8204748Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-05-30T01:42:15.8208434Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-05-30T01:42:15.8210622Z WARNING: scanner metric loading failed: ModuleNotFoundError: No module named 'config'
2026-05-30T01:42:15.8211564Z WARNING: scanner_metrics_missing:MSFT
2026-05-30T01:42:15.8212164Z WARNING: scanner_metrics_missing:NVDA
2026-05-30T01:42:15.8212735Z WARNING: scanner_metrics_missing:META
2026-05-30T01:42:15.8213304Z WARNING: scanner_metrics_missing:AAPL
2026-05-30T01:42:15.8213894Z WARNING: scanner_metrics_missing:MU
2026-05-30T01:42:15.8214462Z WARNING: scanner_metrics_missing:QQQ
2026-05-30T01:42:15.8214930Z WARNING: scanner_metrics_missing:GLD
2026-05-30T01:42:15.8215383Z WARNING: scanner_metrics_missing:SLV
2026-05-30T01:42:15.8221779Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 247, in <module>
2026-05-30T01:42:15.8222499Z     raise SystemExit(main())
2026-05-30T01:42:15.8222745Z                      ^^^^^^
```

```text
2026-05-30T01:42:15.8226388Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-05-30T01:42:15.8227239Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-05-30T01:42:15.8227982Z     raise ReportOutputBoundaryError(
2026-05-30T01:42:15.8229265Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/postmarket-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-05-30T01:42:15.8747705Z ##[error]Process completed with exit code 1.
2026-05-30T01:42:15.8873248Z Post job cleanup.
2026-05-30T01:42:15.9841556Z [command]/usr/bin/git version
2026-05-30T01:42:15.9877677Z git version 2.54.0
2026-05-30T01:42:15.9920478Z Temporarily overriding HOME='/home/runner/work/_temp/35279556-8e23-4aca-a85a-16f8bf278907' before making global git config changes
2026-05-30T01:42:15.9921691Z Adding repository directory to the temporary git global config as a safe directory
2026-05-30T01:42:15.9933051Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-05-30T01:42:15.9967716Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-05-30T01:42:15.9999665Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-05-30T01:42:16.0223305Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-05-30T01:42:16.0250486Z http.https://github.com/.extraheader
2026-05-30T01:42:16.0263669Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

### Failed job: validate-reports (weekly)

- Job ID: `78614043605`
- Started: 2026-05-30T01:41:46Z
- Completed: 2026-05-30T01:42:03Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-05-30T01:42:01.4527391Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-05-30T01:42:01.4527792Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-05-30T01:42:01.4528254Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-05-30T01:42:01.4528593Z ##[endgroup]
2026-05-30T01:42:01.7564695Z Traceback (most recent call last):
2026-05-30T01:42:01.7573109Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 247, in <module>
2026-05-30T01:42:01.7574709Z     raise SystemExit(main())
2026-05-30T01:42:01.7575138Z                      ^^^^^^
2026-05-30T01:42:01.7576263Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 236, in main
2026-05-30T01:42:01.7577687Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-05-30T01:42:01.7578511Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-05-30T01:42:01.7579972Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 68, in write_report_text_guarded
2026-05-30T01:42:01.7581488Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-05-30T01:42:01.7583031Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-05-30T01:42:01.7584204Z     raise ReportOutputBoundaryError(
2026-05-30T01:42:01.7585189Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
```

```text
2026-05-30T01:42:01.7581488Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-05-30T01:42:01.7583031Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-05-30T01:42:01.7584204Z     raise ReportOutputBoundaryError(
2026-05-30T01:42:01.7585189Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-05-30T01:42:01.7782750Z ##[error]Process completed with exit code 1.
2026-05-30T01:42:01.7906450Z Post job cleanup.
2026-05-30T01:42:01.8879418Z [command]/usr/bin/git version
2026-05-30T01:42:01.8916963Z git version 2.54.0
2026-05-30T01:42:01.8962638Z Temporarily overriding HOME='/home/runner/work/_temp/1cf76240-343c-41e2-b332-6994afe9077b' before making global git config changes
2026-05-30T01:42:01.8964146Z Adding repository directory to the temporary git global config as a safe directory
2026-05-30T01:42:01.8969137Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-05-30T01:42:01.9011084Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-05-30T01:42:01.9043022Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-05-30T01:42:01.9267365Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-05-30T01:42:01.9291293Z http.https://github.com/.extraheader
2026-05-30T01:42:01.9303286Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

## Decision Engine Tests

- Run ID: `26670963281`
- Branch: `main`
- Commit: `6b25c52811af`
- Title: Add B1.1 daily evidence run record schema CI-green completion note
- Created: 2026-05-30T01:40:31Z
- Updated: 2026-05-30T01:41:06Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26670963281

### Failed job: tests

- Job ID: `78613962450`
- Started: 2026-05-30T01:40:34Z
- Completed: 2026-05-30T01:41:05Z
- Failed steps: 5. Run pytest

#### Error context

```text
2026-05-30T01:41:02.8310603Z ........................................................................ [ 88%]
2026-05-30T01:41:03.0503924Z ........................................................................ [ 93%]
2026-05-30T01:41:03.0959560Z ........................................................................ [ 99%]
2026-05-30T01:41:03.4159264Z .........                                                                [100%]
2026-05-30T01:41:03.4160388Z =================================== FAILURES ===================================
2026-05-30T01:41:03.4161749Z _________ TestDataPersistence.test_decision_log_path_not_in_gitignore __________
2026-05-30T01:41:03.4162329Z 
2026-05-30T01:41:03.4162705Z self = <test_priority_fixes.TestDataPersistence object at 0x7fe2bde1ff50>
2026-05-30T01:41:03.4163243Z 
2026-05-30T01:41:03.4163509Z     def test_decision_log_path_not_in_gitignore(self):
2026-05-30T01:41:03.4164055Z         gitignore = Path(".gitignore")
2026-05-30T01:41:03.4164561Z         if not gitignore.exists():
2026-05-30T01:41:03.4164958Z             return
2026-05-30T01:41:03.4165302Z         content = gitignore.read_text()
2026-05-30T01:41:03.4165773Z         # data/ should NOT be in gitignore
2026-05-30T01:41:03.4166241Z >       assert "data/" not in content, (
```

```text
2026-05-30T01:41:03.4165773Z         # data/ should NOT be in gitignore
2026-05-30T01:41:03.4166241Z >       assert "data/" not in content, (
2026-05-30T01:41:03.4167110Z             "data/ is in .gitignore â decision log will be lost on every run"
2026-05-30T01:41:03.4167670Z         )
2026-05-30T01:41:03.4168585Z E       AssertionError: data/ is in .gitignore â decision log will be lost on every run
2026-05-30T01:41:03.4169351Z E       assert 'data/' not in '# Python\n_...\n.vscode/\n'
2026-05-30T01:41:03.4170152Z E         
2026-05-30T01:41:03.4170482Z E         'data/' is contained here:
2026-05-30T01:41:03.4170874Z E           e/
2026-05-30T01:41:03.4171169Z E           cache/
2026-05-30T01:41:03.4171491Z E           data/raw/
2026-05-30T01:41:03.4171820Z E           data/live/
2026-05-30T01:41:03.4172172Z E           data/private/
2026-05-30T01:41:03.4172530Z E           data/vendor/
2026-05-30T01:41:03.4172879Z E           evidence/
2026-05-30T01:41:03.4173191Z E           lockbox/
```

```text
2026-05-30T01:41:03.4185421Z E           .DS_Store
2026-05-30T01:41:03.4185743Z E           .idea/
2026-05-30T01:41:03.4186063Z E           .vscode/
2026-05-30T01:41:03.4186263Z 
2026-05-30T01:41:03.4186472Z tests/test_priority_fixes.py:372: AssertionError
2026-05-30T01:41:03.4187085Z =============================== warnings summary ===============================
2026-05-30T01:41:03.4188151Z ../../../../../opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/fastapi/testclient.py:1
2026-05-30T01:41:03.4189898Z   /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
2026-05-30T01:41:03.4191637Z     from starlette.testclient import TestClient as TestClient  # noqa
2026-05-30T01:41:03.4192198Z 
2026-05-30T01:41:03.4192524Z tests/test_jwt_auth.py::test_create_and_validate_token
2026-05-30T01:41:03.4193131Z tests/test_security_layer.py::test_metrics_accepts_admin_token
2026-05-30T01:41:03.4193802Z tests/test_security_layer.py::test_viewer_cannot_access_metrics
2026-05-30T01:41:03.4195392Z   /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/jwt/api_jwt.py:147: InsecureKeyLengthWarning: The HMAC key is 18 bytes long, which is below the minimum recommended length of 32 bytes for SHA256. See RFC 7518 Section 3.2.
2026-05-30T01:41:03.4196896Z     return self._jws.encode(
2026-05-30T01:41:03.4197137Z
```

```text
2026-05-30T01:41:03.4202294Z     decoded = self.decode_complete(
2026-05-30T01:41:03.4202580Z 
2026-05-30T01:41:03.4202909Z -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2026-05-30T01:41:03.4203642Z =========================== short test summary info ============================
2026-05-30T01:41:03.4205157Z FAILED tests/test_priority_fixes.py::TestDataPersistence::test_decision_log_path_not_in_gitignore - AssertionError: data/ is in .gitignore â decision log will be lost on every run
2026-05-30T01:41:03.4206347Z assert 'data/' not in '# Python\n_...\n.vscode/\n'
2026-05-30T01:41:03.4206827Z   
2026-05-30T01:41:03.4207120Z   'data/' is contained here:
2026-05-30T01:41:03.4207499Z     e/
2026-05-30T01:41:03.4207968Z     cache/
2026-05-30T01:41:03.4208266Z     data/raw/
2026-05-30T01:41:03.4208566Z     data/live/
2026-05-30T01:41:03.4208864Z     data/private/
2026-05-30T01:41:03.4209176Z     data/vendor/
2026-05-30T01:41:03.4209476Z     evidence/
2026-05-30T01:41:03.4209766Z     lockbox/
```

```text
2026-05-30T01:41:03.4220326Z     .DS_Store
2026-05-30T01:41:03.4220610Z     .idea/
2026-05-30T01:41:03.4220884Z     .vscode/
2026-05-30T01:41:03.4221264Z 1 failed, 1303 passed, 1 skipped, 7 warnings in 10.94s
2026-05-30T01:41:03.6305780Z ##[error]Process completed with exit code 1.
2026-05-30T01:41:03.6421848Z Post job cleanup.
2026-05-30T01:41:03.7385034Z [command]/usr/bin/git version
2026-05-30T01:41:03.7420932Z git version 2.54.0
2026-05-30T01:41:03.7465109Z Temporarily overriding HOME='/home/runner/work/_temp/f56ff94c-d28d-4a69-8ab8-fb8afceee410' before making global git config changes
2026-05-30T01:41:03.7466544Z Adding repository directory to the temporary git global config as a safe directory
2026-05-30T01:41:03.7472223Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-05-30T01:41:03.7512026Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-05-30T01:41:03.7543703Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-05-30T01:41:03.7767782Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-05-30T01:41:03.7791225Z http.https://github.com/.extraheader
2026-05-30T01:41:03.7802968Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

## Report Quality Validation

- Run ID: `26670963290`
- Branch: `main`
- Commit: `6b25c52811af`
- Title: Add B1.1 daily evidence run record schema CI-green completion note
- Created: 2026-05-30T01:40:31Z
- Updated: 2026-05-30T01:41:06Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26670963290

### Failed job: validate-reports (premarket)

- Job ID: `78613962520`
- Started: 2026-05-30T01:40:33Z
- Completed: 2026-05-30T01:41:06Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-05-30T01:40:48.5053927Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-05-30T01:40:48.5054541Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-05-30T01:40:48.5054989Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-05-30T01:40:48.5055335Z ##[endgroup]
2026-05-30T01:41:04.4193463Z Traceback (most recent call last):
2026-05-30T01:41:04.4202838Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 247, in <module>
2026-05-30T01:41:04.4205048Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-05-30T01:41:04.4206722Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-05-30T01:41:04.4208186Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-05-30T01:41:04.4209167Z WARNING: scanner metric loading failed: ModuleNotFoundError: No module named 'config'
2026-05-30T01:41:04.4209631Z WARNING: scanner_metrics_missing:MSFT
2026-05-30T01:41:04.4209924Z WARNING: scanner_metrics_missing:NVDA
2026-05-30T01:41:04.4210201Z WARNING: scanner_metrics_missing:META
2026-05-30T01:41:04.4210479Z WARNING: scanner_metrics_missing:AAPL
2026-05-30T01:41:04.4210766Z WARNING: scanner_metrics_missing:MU
2026-05-30T01:41:04.4211045Z WARNING: scanner_metrics_missing:QQQ
```

```text
2026-05-30T01:41:04.4202838Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 247, in <module>
2026-05-30T01:41:04.4205048Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-05-30T01:41:04.4206722Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-05-30T01:41:04.4208186Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-05-30T01:41:04.4209167Z WARNING: scanner metric loading failed: ModuleNotFoundError: No module named 'config'
2026-05-30T01:41:04.4209631Z WARNING: scanner_metrics_missing:MSFT
2026-05-30T01:41:04.4209924Z WARNING: scanner_metrics_missing:NVDA
2026-05-30T01:41:04.4210201Z WARNING: scanner_metrics_missing:META
2026-05-30T01:41:04.4210479Z WARNING: scanner_metrics_missing:AAPL
2026-05-30T01:41:04.4210766Z WARNING: scanner_metrics_missing:MU
2026-05-30T01:41:04.4211045Z WARNING: scanner_metrics_missing:QQQ
2026-05-30T01:41:04.4211321Z WARNING: scanner_metrics_missing:GLD
2026-05-30T01:41:04.4211588Z WARNING: scanner_metrics_missing:SLV
2026-05-30T01:41:04.4211988Z     raise SystemExit(main())
2026-05-30T01:41:04.4212234Z                      ^^^^^^
2026-05-30T01:41:04.4212878Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 236, in main
```

```text
2026-05-30T01:41:04.4216307Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-05-30T01:41:04.4217170Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-05-30T01:41:04.4217930Z     raise ReportOutputBoundaryError(
2026-05-30T01:41:04.4219237Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/premarket-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-05-30T01:41:04.4711079Z ##[error]Process completed with exit code 1.
2026-05-30T01:41:04.4835177Z Post job cleanup.
2026-05-30T01:41:04.5800250Z [command]/usr/bin/git version
2026-05-30T01:41:04.5836916Z git version 2.54.0
2026-05-30T01:41:04.5883588Z Temporarily overriding HOME='/home/runner/work/_temp/ef420840-fac7-4c07-bc56-78fbdb82cb3a' before making global git config changes
2026-05-30T01:41:04.5884842Z Adding repository directory to the temporary git global config as a safe directory
2026-05-30T01:41:04.5898578Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-05-30T01:41:04.5933244Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-05-30T01:41:04.5966228Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-05-30T01:41:04.6192338Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-05-30T01:41:04.6216054Z http.https://github.com/.extraheader
2026-05-30T01:41:04.6228656Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

### Failed job: validate-reports (postmarket)

- Job ID: `78613962531`
- Started: 2026-05-30T01:40:33Z
- Completed: 2026-05-30T01:41:06Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-05-30T01:40:48.8047440Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-05-30T01:40:48.8047823Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-05-30T01:40:48.8048231Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-05-30T01:40:48.8048567Z ##[endgroup]
2026-05-30T01:41:04.3866580Z Traceback (most recent call last):
2026-05-30T01:41:04.3868204Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-05-30T01:41:04.3870351Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-05-30T01:41:04.3872222Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-05-30T01:41:04.3873178Z WARNING: scanner metric loading failed: ModuleNotFoundError: No module named 'config'
2026-05-30T01:41:04.3873625Z WARNING: scanner_metrics_missing:MSFT
2026-05-30T01:41:04.3873927Z WARNING: scanner_metrics_missing:NVDA
2026-05-30T01:41:04.3874198Z WARNING: scanner_metrics_missing:META
2026-05-30T01:41:04.3874472Z WARNING: scanner_metrics_missing:AAPL
2026-05-30T01:41:04.3874750Z WARNING: scanner_metrics_missing:MU
2026-05-30T01:41:04.3875029Z WARNING: scanner_metrics_missing:QQQ
2026-05-30T01:41:04.3882121Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 247, in <module>
```

```text
2026-05-30T01:41:04.3866580Z Traceback (most recent call last):
2026-05-30T01:41:04.3868204Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-05-30T01:41:04.3870351Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-05-30T01:41:04.3872222Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-05-30T01:41:04.3873178Z WARNING: scanner metric loading failed: ModuleNotFoundError: No module named 'config'
2026-05-30T01:41:04.3873625Z WARNING: scanner_metrics_missing:MSFT
2026-05-30T01:41:04.3873927Z WARNING: scanner_metrics_missing:NVDA
2026-05-30T01:41:04.3874198Z WARNING: scanner_metrics_missing:META
2026-05-30T01:41:04.3874472Z WARNING: scanner_metrics_missing:AAPL
2026-05-30T01:41:04.3874750Z WARNING: scanner_metrics_missing:MU
2026-05-30T01:41:04.3875029Z WARNING: scanner_metrics_missing:QQQ
2026-05-30T01:41:04.3882121Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 247, in <module>
2026-05-30T01:41:04.3882862Z     raise SystemExit(main())
2026-05-30T01:41:04.3883125Z                      ^^^^^^
2026-05-30T01:41:04.3883766Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 236, in main
2026-05-30T01:41:04.3884494Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
```

```text
2026-05-30T01:41:04.3888264Z     raise ReportOutputBoundaryError(
2026-05-30T01:41:04.3889206Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/postmarket-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-05-30T01:41:04.3890161Z WARNING: scanner_metrics_missing:GLD
2026-05-30T01:41:04.3890436Z WARNING: scanner_metrics_missing:SLV
2026-05-30T01:41:04.4557156Z ##[error]Process completed with exit code 1.
2026-05-30T01:41:04.4680769Z Post job cleanup.
2026-05-30T01:41:04.5666473Z [command]/usr/bin/git version
2026-05-30T01:41:04.5702359Z git version 2.54.0
2026-05-30T01:41:04.5742535Z Temporarily overriding HOME='/home/runner/work/_temp/c02d5795-8911-4831-95ed-b469583ec6f1' before making global git config changes
2026-05-30T01:41:04.5743478Z Adding repository directory to the temporary git global config as a safe directory
2026-05-30T01:41:04.5757562Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-05-30T01:41:04.5793727Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-05-30T01:41:04.5827981Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-05-30T01:41:04.6087924Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-05-30T01:41:04.6114171Z http.https://github.com/.extraheader
2026-05-30T01:41:04.6130756Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

### Failed job: validate-reports (weekly)

- Job ID: `78613962538`
- Started: 2026-05-30T01:40:33Z
- Completed: 2026-05-30T01:40:52Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-05-30T01:40:50.7335992Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-05-30T01:40:50.7336423Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-05-30T01:40:50.7336899Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-05-30T01:40:50.7337265Z ##[endgroup]
2026-05-30T01:40:51.4972169Z Traceback (most recent call last):
2026-05-30T01:40:51.4982187Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 247, in <module>
2026-05-30T01:40:51.4983396Z     raise SystemExit(main())
2026-05-30T01:40:51.4983857Z                      ^^^^^^
2026-05-30T01:40:51.4996882Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 236, in main
2026-05-30T01:40:51.5016172Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-05-30T01:40:51.5046485Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-05-30T01:40:51.5057303Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 68, in write_report_text_guarded
2026-05-30T01:40:51.5058586Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-05-30T01:40:51.5059926Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-05-30T01:40:51.5061173Z     raise ReportOutputBoundaryError(
2026-05-30T01:40:51.5062613Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
```

```text
2026-05-30T01:40:51.5058586Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-05-30T01:40:51.5059926Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-05-30T01:40:51.5061173Z     raise ReportOutputBoundaryError(
2026-05-30T01:40:51.5062613Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-05-30T01:40:51.5237730Z ##[error]Process completed with exit code 1.
2026-05-30T01:40:51.5362345Z Post job cleanup.
2026-05-30T01:40:51.6361592Z [command]/usr/bin/git version
2026-05-30T01:40:51.6399912Z git version 2.54.0
2026-05-30T01:40:51.6441073Z Temporarily overriding HOME='/home/runner/work/_temp/5e9d3c79-4bf6-4303-96ea-db81fe984279' before making global git config changes
2026-05-30T01:40:51.6442227Z Adding repository directory to the temporary git global config as a safe directory
2026-05-30T01:40:51.6455224Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-05-30T01:40:51.6492639Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-05-30T01:40:51.6526131Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-05-30T01:40:51.6769721Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-05-30T01:40:51.6795516Z http.https://github.com/.extraheader
2026-05-30T01:40:51.6807761Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

## Decision Engine Tests

- Run ID: `26670641296`
- Branch: `main`
- Commit: `56ab99be84b7`
- Title: Wire B1.1 daily evidence run record schema guard into CI
- Created: 2026-05-30T01:26:37Z
- Updated: 2026-05-30T01:27:10Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26670641296

### Failed job: tests

- Job ID: `78613064060`
- Started: 2026-05-30T01:26:39Z
- Completed: 2026-05-30T01:27:09Z
- Failed steps: 5. Run pytest

#### Error context

```text
2026-05-30T01:27:06.9944039Z ........................................................................ [ 88%]
2026-05-30T01:27:07.1957328Z ........................................................................ [ 93%]
2026-05-30T01:27:07.2334966Z ........................................................................ [ 99%]
2026-05-30T01:27:07.5687071Z .........                                                                [100%]
2026-05-30T01:27:07.5688099Z =================================== FAILURES ===================================
2026-05-30T01:27:07.5689268Z _________ TestDataPersistence.test_decision_log_path_not_in_gitignore __________
2026-05-30T01:27:07.5689763Z 
2026-05-30T01:27:07.5690089Z self = <test_priority_fixes.TestDataPersistence object at 0x7f1118f02d10>
2026-05-30T01:27:07.5690534Z 
2026-05-30T01:27:07.5690750Z     def test_decision_log_path_not_in_gitignore(self):
2026-05-30T01:27:07.5691252Z         gitignore = Path(".gitignore")
2026-05-30T01:27:07.5691674Z         if not gitignore.exists():
2026-05-30T01:27:07.5692050Z             return
2026-05-30T01:27:07.5692390Z         content = gitignore.read_text()
2026-05-30T01:27:07.5692819Z         # data/ should NOT be in gitignore
2026-05-30T01:27:07.5693245Z >       assert "data/" not in content, (
```

```text
2026-05-30T01:27:07.5692819Z         # data/ should NOT be in gitignore
2026-05-30T01:27:07.5693245Z >       assert "data/" not in content, (
2026-05-30T01:27:07.5694045Z             "data/ is in .gitignore â decision log will be lost on every run"
2026-05-30T01:27:07.5694404Z         )
2026-05-30T01:27:07.5695174Z E       AssertionError: data/ is in .gitignore â decision log will be lost on every run
2026-05-30T01:27:07.5695655Z E       assert 'data/' not in '# Python\n_...\n.vscode/\n'
2026-05-30T01:27:07.5696241Z E         
2026-05-30T01:27:07.5696445Z E         'data/' is contained here:
2026-05-30T01:27:07.5696699Z E           e/
2026-05-30T01:27:07.5696892Z E           cache/
2026-05-30T01:27:07.5697096Z E           data/raw/
2026-05-30T01:27:07.5697307Z E           data/live/
2026-05-30T01:27:07.5697523Z E           data/private/
2026-05-30T01:27:07.5697748Z E           data/vendor/
2026-05-30T01:27:07.5697961Z E           evidence/
2026-05-30T01:27:07.5698161Z E           lockbox/
```

```text
2026-05-30T01:27:07.5706494Z E           .DS_Store
2026-05-30T01:27:07.5706693Z E           .idea/
2026-05-30T01:27:07.5706891Z E           .vscode/
2026-05-30T01:27:07.5707044Z 
2026-05-30T01:27:07.5707173Z tests/test_priority_fixes.py:372: AssertionError
2026-05-30T01:27:07.5707516Z =============================== warnings summary ===============================
2026-05-30T01:27:07.5708073Z ../../../../../opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/fastapi/testclient.py:1
2026-05-30T01:27:07.5709182Z   /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
2026-05-30T01:27:07.5710316Z     from starlette.testclient import TestClient as TestClient  # noqa
2026-05-30T01:27:07.5710705Z 
2026-05-30T01:27:07.5710997Z tests/test_jwt_auth.py::test_create_and_validate_token
2026-05-30T01:27:07.5711390Z tests/test_security_layer.py::test_metrics_accepts_admin_token
2026-05-30T01:27:07.5711799Z tests/test_security_layer.py::test_viewer_cannot_access_metrics
2026-05-30T01:27:07.5712781Z   /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/jwt/api_jwt.py:147: InsecureKeyLengthWarning: The HMAC key is 18 bytes long, which is below the minimum recommended length of 32 bytes for SHA256. See RFC 7518 Section 3.2.
2026-05-30T01:27:07.5713736Z     return self._jws.encode(
2026-05-30T01:27:07.5713897Z
```

```text
2026-05-30T01:27:07.5717131Z     decoded = self.decode_complete(
2026-05-30T01:27:07.5717311Z 
2026-05-30T01:27:07.5717551Z -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2026-05-30T01:27:07.5717996Z =========================== short test summary info ============================
2026-05-30T01:27:07.5718959Z FAILED tests/test_priority_fixes.py::TestDataPersistence::test_decision_log_path_not_in_gitignore - AssertionError: data/ is in .gitignore â decision log will be lost on every run
2026-05-30T01:27:07.5719722Z assert 'data/' not in '# Python\n_...\n.vscode/\n'
2026-05-30T01:27:07.5720020Z   
2026-05-30T01:27:07.5720217Z   'data/' is contained here:
2026-05-30T01:27:07.5720455Z     e/
2026-05-30T01:27:07.5720637Z     cache/
2026-05-30T01:27:07.5720823Z     data/raw/
2026-05-30T01:27:07.5721023Z     data/live/
2026-05-30T01:27:07.5721221Z     data/private/
2026-05-30T01:27:07.5721423Z     data/vendor/
2026-05-30T01:27:07.5721614Z     evidence/
2026-05-30T01:27:07.5721799Z     lockbox/
```

```text
2026-05-30T01:27:07.5728775Z     .DS_Store
2026-05-30T01:27:07.5728964Z     .idea/
2026-05-30T01:27:07.5729153Z     .vscode/
2026-05-30T01:27:07.5729406Z 1 failed, 1303 passed, 1 skipped, 7 warnings in 12.16s
2026-05-30T01:27:07.8800665Z ##[error]Process completed with exit code 1.
2026-05-30T01:27:07.8906609Z Post job cleanup.
2026-05-30T01:27:07.9872551Z [command]/usr/bin/git version
2026-05-30T01:27:07.9915153Z git version 2.54.0
2026-05-30T01:27:07.9957315Z Temporarily overriding HOME='/home/runner/work/_temp/87b838ec-0275-4ea9-8b1d-7a88b4f4182e' before making global git config changes
2026-05-30T01:27:07.9958279Z Adding repository directory to the temporary git global config as a safe directory
2026-05-30T01:27:07.9972321Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-05-30T01:27:08.0008845Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-05-30T01:27:08.0041799Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-05-30T01:27:08.0284027Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-05-30T01:27:08.0309742Z http.https://github.com/.extraheader
2026-05-30T01:27:08.0322113Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

## Report Quality Validation

- Run ID: `26670641293`
- Branch: `main`
- Commit: `56ab99be84b7`
- Title: Wire B1.1 daily evidence run record schema guard into CI
- Created: 2026-05-30T01:26:37Z
- Updated: 2026-05-30T01:27:23Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26670641293

### Failed job: validate-reports (weekly)

- Job ID: `78613064200`
- Started: 2026-05-30T01:26:39Z
- Completed: 2026-05-30T01:26:57Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-05-30T01:26:54.9636986Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-05-30T01:26:54.9637371Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-05-30T01:26:54.9637805Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-05-30T01:26:54.9638135Z ##[endgroup]
2026-05-30T01:26:55.2746776Z Traceback (most recent call last):
2026-05-30T01:26:55.2752322Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 247, in <module>
2026-05-30T01:26:55.2753245Z     raise SystemExit(main())
2026-05-30T01:26:55.2754155Z                      ^^^^^^
2026-05-30T01:26:55.2755214Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 236, in main
2026-05-30T01:26:55.2756122Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-05-30T01:26:55.2756752Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-05-30T01:26:55.2757936Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 68, in write_report_text_guarded
2026-05-30T01:26:55.2758842Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-05-30T01:26:55.2760101Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-05-30T01:26:55.2760936Z     raise ReportOutputBoundaryError(
2026-05-30T01:26:55.2762189Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
```

```text
2026-05-30T01:26:55.2758842Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-05-30T01:26:55.2760101Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-05-30T01:26:55.2760936Z     raise ReportOutputBoundaryError(
2026-05-30T01:26:55.2762189Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-05-30T01:26:55.2971039Z ##[error]Process completed with exit code 1.
2026-05-30T01:26:55.3092899Z Post job cleanup.
2026-05-30T01:26:55.4054857Z [command]/usr/bin/git version
2026-05-30T01:26:55.4090480Z git version 2.54.0
2026-05-30T01:26:55.4131598Z Temporarily overriding HOME='/home/runner/work/_temp/880fe1eb-651b-4c1a-ab15-14c8ff130fa0' before making global git config changes
2026-05-30T01:26:55.4132875Z Adding repository directory to the temporary git global config as a safe directory
2026-05-30T01:26:55.4137776Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-05-30T01:26:55.4174367Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-05-30T01:26:55.4209725Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-05-30T01:26:55.4458383Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-05-30T01:26:55.4482335Z http.https://github.com/.extraheader
2026-05-30T01:26:55.4494557Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

### Failed job: validate-reports (premarket)

- Job ID: `78613064201`
- Started: 2026-05-30T01:26:40Z
- Completed: 2026-05-30T01:27:22Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-05-30T01:26:59.0517470Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-05-30T01:26:59.0517859Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-05-30T01:26:59.0518271Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-05-30T01:26:59.0518598Z ##[endgroup]
2026-05-30T01:27:19.9288682Z Traceback (most recent call last):
2026-05-30T01:27:19.9290889Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-05-30T01:27:19.9296015Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-05-30T01:27:19.9298262Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-05-30T01:27:19.9299746Z WARNING: scanner metric loading failed: ModuleNotFoundError: No module named 'config'
2026-05-30T01:27:19.9300429Z WARNING: scanner_metrics_missing:MSFT
2026-05-30T01:27:19.9300873Z WARNING: scanner_metrics_missing:NVDA
2026-05-30T01:27:19.9301279Z WARNING: scanner_metrics_missing:META
2026-05-30T01:27:19.9301681Z WARNING: scanner_metrics_missing:AAPL
2026-05-30T01:27:19.9302096Z WARNING: scanner_metrics_missing:MU
2026-05-30T01:27:19.9309974Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 247, in <module>
2026-05-30T01:27:19.9311037Z     raise SystemExit(main())
```

```text
2026-05-30T01:27:19.9288682Z Traceback (most recent call last):
2026-05-30T01:27:19.9290889Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-05-30T01:27:19.9296015Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-05-30T01:27:19.9298262Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-05-30T01:27:19.9299746Z WARNING: scanner metric loading failed: ModuleNotFoundError: No module named 'config'
2026-05-30T01:27:19.9300429Z WARNING: scanner_metrics_missing:MSFT
2026-05-30T01:27:19.9300873Z WARNING: scanner_metrics_missing:NVDA
2026-05-30T01:27:19.9301279Z WARNING: scanner_metrics_missing:META
2026-05-30T01:27:19.9301681Z WARNING: scanner_metrics_missing:AAPL
2026-05-30T01:27:19.9302096Z WARNING: scanner_metrics_missing:MU
2026-05-30T01:27:19.9309974Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 247, in <module>
2026-05-30T01:27:19.9311037Z     raise SystemExit(main())
2026-05-30T01:27:19.9311409Z                      ^^^^^^
2026-05-30T01:27:19.9312399Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 236, in main
2026-05-30T01:27:19.9313571Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-05-30T01:27:19.9314283Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```

```text
2026-05-30T01:27:19.9321498Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/premarket-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-05-30T01:27:19.9323042Z WARNING: scanner_metrics_missing:QQQ
2026-05-30T01:27:19.9323457Z WARNING: scanner_metrics_missing:GLD
2026-05-30T01:27:19.9323875Z WARNING: scanner_metrics_missing:SLV
2026-05-30T01:27:19.9925079Z ##[error]Process completed with exit code 1.
2026-05-30T01:27:20.0051879Z Post job cleanup.
2026-05-30T01:27:20.1051429Z [command]/usr/bin/git version
2026-05-30T01:27:20.1088991Z git version 2.54.0
2026-05-30T01:27:20.1134076Z Temporarily overriding HOME='/home/runner/work/_temp/be2aa646-a2ce-445f-aa22-39507e6fd06b' before making global git config changes
2026-05-30T01:27:20.1135757Z Adding repository directory to the temporary git global config as a safe directory
2026-05-30T01:27:20.1147734Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-05-30T01:27:20.1182030Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-05-30T01:27:20.1213844Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-05-30T01:27:20.1457496Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-05-30T01:27:20.1483513Z http.https://github.com/.extraheader
2026-05-30T01:27:20.1496854Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

### Failed job: validate-reports (postmarket)

- Job ID: `78613064204`
- Started: 2026-05-30T01:26:39Z
- Completed: 2026-05-30T01:27:19Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-05-30T01:26:55.3080287Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-05-30T01:26:55.3080671Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-05-30T01:26:55.3081109Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-05-30T01:26:55.3081431Z ##[endgroup]
2026-05-30T01:27:16.9561497Z Traceback (most recent call last):
2026-05-30T01:27:16.9571269Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 247, in <module>
2026-05-30T01:27:16.9573671Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-05-30T01:27:16.9576272Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-05-30T01:27:16.9578566Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-05-30T01:27:16.9580100Z WARNING: scanner metric loading failed: ModuleNotFoundError: No module named 'config'
2026-05-30T01:27:16.9580796Z WARNING: scanner_metrics_missing:MSFT
2026-05-30T01:27:16.9581264Z WARNING: scanner_metrics_missing:NVDA
2026-05-30T01:27:16.9581692Z WARNING: scanner_metrics_missing:META
2026-05-30T01:27:16.9582120Z WARNING: scanner_metrics_missing:AAPL
2026-05-30T01:27:16.9582535Z WARNING: scanner_metrics_missing:MU
2026-05-30T01:27:16.9582960Z WARNING: scanner_metrics_missing:QQQ
```

```text
2026-05-30T01:27:16.9571269Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 247, in <module>
2026-05-30T01:27:16.9573671Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-05-30T01:27:16.9576272Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-05-30T01:27:16.9578566Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-05-30T01:27:16.9580100Z WARNING: scanner metric loading failed: ModuleNotFoundError: No module named 'config'
2026-05-30T01:27:16.9580796Z WARNING: scanner_metrics_missing:MSFT
2026-05-30T01:27:16.9581264Z WARNING: scanner_metrics_missing:NVDA
2026-05-30T01:27:16.9581692Z WARNING: scanner_metrics_missing:META
2026-05-30T01:27:16.9582120Z WARNING: scanner_metrics_missing:AAPL
2026-05-30T01:27:16.9582535Z WARNING: scanner_metrics_missing:MU
2026-05-30T01:27:16.9582960Z WARNING: scanner_metrics_missing:QQQ
2026-05-30T01:27:16.9583371Z WARNING: scanner_metrics_missing:GLD
2026-05-30T01:27:16.9583776Z WARNING: scanner_metrics_missing:SLV
2026-05-30T01:27:16.9584378Z     raise SystemExit(main())
2026-05-30T01:27:16.9585265Z                      ^^^^^^
2026-05-30T01:27:16.9586293Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 236, in main
```

```text
2026-05-30T01:27:16.9591051Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-05-30T01:27:16.9592423Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-05-30T01:27:16.9593611Z     raise ReportOutputBoundaryError(
2026-05-30T01:27:16.9595339Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/postmarket-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-05-30T01:27:17.0097766Z ##[error]Process completed with exit code 1.
2026-05-30T01:27:17.0225319Z Post job cleanup.
2026-05-30T01:27:17.1208159Z [command]/usr/bin/git version
2026-05-30T01:27:17.1243683Z git version 2.54.0
2026-05-30T01:27:17.1286409Z Temporarily overriding HOME='/home/runner/work/_temp/f0a41791-711d-4b7d-a507-565dac1f5839' before making global git config changes
2026-05-30T01:27:17.1287780Z Adding repository directory to the temporary git global config as a safe directory
2026-05-30T01:27:17.1298974Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-05-30T01:27:17.1332109Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-05-30T01:27:17.1363623Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-05-30T01:27:17.1589191Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-05-30T01:27:17.1612691Z http.https://github.com/.extraheader
2026-05-30T01:27:17.1624866Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```
