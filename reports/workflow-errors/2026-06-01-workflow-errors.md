# GitHub Actions Workflow Error Report

Generated: 2026-06-01 09:04 UTC
Repository: `yalcinkadir/institutional-trading-engine`
Filter since: 2026-05-31 09:04 UTC
Failed runs included: 10

## Decision Engine Tests

- Run ID: `26745477490`
- Branch: `main`
- Commit: `eaf7dadd12e5`
- Title: Update roadmap for RGP6 strict notification handling
- Created: 2026-06-01T09:03:31Z
- Updated: 2026-06-01T09:04:10Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26745477490

### Failed job: tests

- Job ID: `78819742993`
- Started: 2026-06-01T09:03:35Z
- Completed: 2026-06-01T09:04:08Z
- Failed steps: 5. Run pytest

#### Error context

```text
2026-06-01T09:04:06.0511664Z ........................................................................ [ 87%]
2026-06-01T09:04:06.2820889Z ........................................................................ [ 92%]
2026-06-01T09:04:06.3260966Z ........................................................................ [ 98%]
2026-06-01T09:04:06.3916574Z ...........................                                              [100%]
2026-06-01T09:04:06.3917272Z =================================== FAILURES ===================================
2026-06-01T09:04:06.3918129Z _________ TestDataPersistence.test_decision_log_path_not_in_gitignore __________
2026-06-01T09:04:06.3918701Z 
2026-06-01T09:04:06.3919049Z self = <test_priority_fixes.TestDataPersistence object at 0x7f2196e8f050>
2026-06-01T09:04:06.3919630Z 
2026-06-01T09:04:06.3919873Z     def test_decision_log_path_not_in_gitignore(self):
2026-06-01T09:04:06.3920703Z         gitignore = Path(".gitignore")
2026-06-01T09:04:06.3921415Z         if not gitignore.exists():
2026-06-01T09:04:06.3921718Z             return
2026-06-01T09:04:06.3921981Z         content = gitignore.read_text()
2026-06-01T09:04:06.3922315Z         # data/ should NOT be in gitignore
2026-06-01T09:04:06.3922654Z >       assert "data/" not in content, (
```

```text
2026-06-01T09:04:06.3922315Z         # data/ should NOT be in gitignore
2026-06-01T09:04:06.3922654Z >       assert "data/" not in content, (
2026-06-01T09:04:06.3923317Z             "data/ is in .gitignore â decision log will be lost on every run"
2026-06-01T09:04:06.3923741Z         )
2026-06-01T09:04:06.3924210Z E       AssertionError: data/ is in .gitignore â decision log will be lost on every run
2026-06-01T09:04:06.3924955Z E       assert 'data/' not in '# Python\n_...\n.vscode/\n'
2026-06-01T09:04:06.3925327Z E         
2026-06-01T09:04:06.3925555Z E         'data/' is contained here:
2026-06-01T09:04:06.3925850Z E           e/
2026-06-01T09:04:06.3926073Z E           cache/
2026-06-01T09:04:06.3926306Z E           data/raw/
2026-06-01T09:04:06.3926549Z E           data/live/
2026-06-01T09:04:06.3926800Z E           data/private/
2026-06-01T09:04:06.3927075Z E           data/vendor/
2026-06-01T09:04:06.3927331Z E           evidence/
2026-06-01T09:04:06.3927566Z E           lockbox/
```

```text
2026-06-01T09:04:06.3936731Z E           .DS_Store
2026-06-01T09:04:06.3936916Z E           .idea/
2026-06-01T09:04:06.3937099Z E           .vscode/
2026-06-01T09:04:06.3937234Z 
2026-06-01T09:04:06.3937361Z tests/test_priority_fixes.py:372: AssertionError
2026-06-01T09:04:06.3937765Z =============================== warnings summary ===============================
2026-06-01T09:04:06.3938388Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbol_writes_csv_and_metadata
2026-06-01T09:04:06.3939064Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbol_merges_without_duplicates
2026-06-01T09:04:06.3939711Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbols_batch_counts_results
2026-06-01T09:04:06.3940328Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbols_batch_counts_results
2026-06-01T09:04:06.3942322Z   /home/runner/work/institutional-trading-engine/institutional-trading-engine/src/historical/polygon_ingestion.py:125: FutureWarning: The behavior of DataFrame concatenation with empty or all-NA entries is deprecated. In a future version, this will no longer exclude empty or all-NA columns when determining the result dtypes. To retain the old behavior, exclude the relevant entries before the concat operation.
2026-06-01T09:04:06.3944119Z     combined = pd.concat([existing, df], ignore_index=True)
2026-06-01T09:04:06.3944371Z 
2026-06-01T09:04:06.3944599Z -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2026-06-01T09:04:06.3945198Z =========================== short test summary info ============================
2026-06-01T09:04:06.3946181Z FAILED tests/test_priority_fixes.py::TestDataPersistence::test_decision_log_path_not_in_gitignore - AssertionError: data/ is in .gitignore â decision log will be lost on every run
```

```text
2026-06-01T09:04:06.3944119Z     combined = pd.concat([existing, df], ignore_index=True)
2026-06-01T09:04:06.3944371Z 
2026-06-01T09:04:06.3944599Z -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2026-06-01T09:04:06.3945198Z =========================== short test summary info ============================
2026-06-01T09:04:06.3946181Z FAILED tests/test_priority_fixes.py::TestDataPersistence::test_decision_log_path_not_in_gitignore - AssertionError: data/ is in .gitignore â decision log will be lost on every run
2026-06-01T09:04:06.3946955Z assert 'data/' not in '# Python\n_...\n.vscode/\n'
2026-06-01T09:04:06.3947241Z   
2026-06-01T09:04:06.3947426Z   'data/' is contained here:
2026-06-01T09:04:06.3947654Z     e/
2026-06-01T09:04:06.3947839Z     cache/
2026-06-01T09:04:06.3948008Z     data/raw/
2026-06-01T09:04:06.3948189Z     data/live/
2026-06-01T09:04:06.3948374Z     data/private/
2026-06-01T09:04:06.3948561Z     data/vendor/
2026-06-01T09:04:06.3948744Z     evidence/
2026-06-01T09:04:06.3948928Z     lockbox/
```

```text
2026-06-01T09:04:06.3955881Z     .DS_Store
2026-06-01T09:04:06.3956054Z     .idea/
2026-06-01T09:04:06.3956225Z     .vscode/
2026-06-01T09:04:06.3956460Z 1 failed, 1393 passed, 1 skipped, 4 warnings in 11.72s
2026-06-01T09:04:06.6460984Z ##[error]Process completed with exit code 1.
2026-06-01T09:04:06.6583181Z Post job cleanup.
2026-06-01T09:04:06.7581800Z [command]/usr/bin/git version
2026-06-01T09:04:06.7620723Z git version 2.54.0
2026-06-01T09:04:06.7669532Z Temporarily overriding HOME='/home/runner/work/_temp/40ff3326-73fb-45c0-8c99-e15bf8ee4ebe' before making global git config changes
2026-06-01T09:04:06.7671249Z Adding repository directory to the temporary git global config as a safe directory
2026-06-01T09:04:06.7685200Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-06-01T09:04:06.7723055Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-06-01T09:04:06.7757472Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-06-01T09:04:06.7988127Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-06-01T09:04:06.8013832Z http.https://github.com/.extraheader
2026-06-01T09:04:06.8026587Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

## Report Quality Validation

- Run ID: `26745477563`
- Branch: `main`
- Commit: `eaf7dadd12e5`
- Title: Update roadmap for RGP6 strict notification handling
- Created: 2026-06-01T09:03:31Z
- Updated: 2026-06-01T09:04:11Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26745477563

### Failed job: validate-reports (premarket)

- Job ID: `78819743349`
- Started: 2026-06-01T09:03:34Z
- Completed: 2026-06-01T09:04:10Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-01T09:03:51.7679422Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-01T09:03:51.7679823Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-01T09:03:51.7680255Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-01T09:03:51.7680617Z ##[endgroup]
2026-06-01T09:04:08.2423963Z Traceback (most recent call last):
2026-06-01T09:04:08.2425485Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-28/2026-06-01?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-01T09:04:08.2432617Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 247, in <module>
2026-06-01T09:04:08.2433341Z     raise SystemExit(main())
2026-06-01T09:04:08.2433607Z                      ^^^^^^
2026-06-01T09:04:08.2434248Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 236, in main
2026-06-01T09:04:08.2435028Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-01T09:04:08.2435488Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-01T09:04:08.2436260Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 68, in write_report_text_guarded
2026-06-01T09:04:08.2437029Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-01T09:04:08.2438063Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-28/2026-06-01?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-01T09:04:08.2439593Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-28/2026-06-01?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
```

```text
2026-06-01T09:04:08.2436260Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 68, in write_report_text_guarded
2026-06-01T09:04:08.2437029Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-01T09:04:08.2438063Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-28/2026-06-01?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-01T09:04:08.2439593Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-28/2026-06-01?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-01T09:04:08.2440483Z WARNING: scanner metric loading failed: ModuleNotFoundError: No module named 'config'
2026-06-01T09:04:08.2440925Z WARNING: scanner_metrics_missing:MSFT
2026-06-01T09:04:08.2441207Z WARNING: scanner_metrics_missing:NVDA
2026-06-01T09:04:08.2441491Z WARNING: scanner_metrics_missing:META
2026-06-01T09:04:08.2441760Z WARNING: scanner_metrics_missing:AAPL
2026-06-01T09:04:08.2442024Z WARNING: scanner_metrics_missing:MU
2026-06-01T09:04:08.2442295Z WARNING: scanner_metrics_missing:QQQ
2026-06-01T09:04:08.2442569Z WARNING: scanner_metrics_missing:GLD
2026-06-01T09:04:08.2442824Z WARNING: scanner_metrics_missing:SLV
2026-06-01T09:04:08.2443672Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-06-01T09:04:08.2444419Z     raise ReportOutputBoundaryError(
2026-06-01T09:04:08.2445370Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/premarket-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
```

```text
2026-06-01T09:04:08.2442824Z WARNING: scanner_metrics_missing:SLV
2026-06-01T09:04:08.2443672Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-06-01T09:04:08.2444419Z     raise ReportOutputBoundaryError(
2026-06-01T09:04:08.2445370Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/premarket-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-06-01T09:04:08.3441026Z ##[error]Process completed with exit code 1.
2026-06-01T09:04:08.3564592Z Post job cleanup.
2026-06-01T09:04:08.4559508Z [command]/usr/bin/git version
2026-06-01T09:04:08.4597178Z git version 2.54.0
2026-06-01T09:04:08.4638715Z Temporarily overriding HOME='/home/runner/work/_temp/15bd1668-7156-4e19-85e4-d65966e3d091' before making global git config changes
2026-06-01T09:04:08.4639651Z Adding repository directory to the temporary git global config as a safe directory
2026-06-01T09:04:08.4654865Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-06-01T09:04:08.4696165Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-06-01T09:04:08.4731980Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-06-01T09:04:08.4987666Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-06-01T09:04:08.5015257Z http.https://github.com/.extraheader
2026-06-01T09:04:08.5028098Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

### Failed job: validate-reports (postmarket)

- Job ID: `78819743380`
- Started: 2026-06-01T09:03:34Z
- Completed: 2026-06-01T09:04:08Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-01T09:03:50.8296576Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-01T09:03:50.8296970Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-01T09:03:50.8297411Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-01T09:03:50.8297748Z ##[endgroup]
2026-06-01T09:04:06.6041224Z Traceback (most recent call last):
2026-06-01T09:04:06.6043531Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-28/2026-06-01?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-01T09:04:06.6053932Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 247, in <module>
2026-06-01T09:04:06.6055070Z     raise SystemExit(main())
2026-06-01T09:04:06.6055452Z                      ^^^^^^
2026-06-01T09:04:06.6056434Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 236, in main
2026-06-01T09:04:06.6057640Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-01T09:04:06.6058354Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-01T09:04:06.6059833Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 68, in write_report_text_guarded
2026-06-01T09:04:06.6061109Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-01T09:04:06.6062505Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-06-01T09:04:06.6063736Z     raise ReportOutputBoundaryError(
```

```text
2026-06-01T09:04:06.6063736Z     raise ReportOutputBoundaryError(
2026-06-01T09:04:06.6065312Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/postmarket-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-06-01T09:04:06.6068101Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-28/2026-06-01?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-01T09:04:06.6070829Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-28/2026-06-01?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-01T09:04:06.6072370Z WARNING: scanner metric loading failed: ModuleNotFoundError: No module named 'config'
2026-06-01T09:04:06.6073090Z WARNING: scanner_metrics_missing:MSFT
2026-06-01T09:04:06.6073530Z WARNING: scanner_metrics_missing:NVDA
2026-06-01T09:04:06.6073963Z WARNING: scanner_metrics_missing:META
2026-06-01T09:04:06.6074392Z WARNING: scanner_metrics_missing:AAPL
2026-06-01T09:04:06.6074840Z WARNING: scanner_metrics_missing:MU
2026-06-01T09:04:06.6075645Z WARNING: scanner_metrics_missing:QQQ
2026-06-01T09:04:06.6076068Z WARNING: scanner_metrics_missing:GLD
2026-06-01T09:04:06.6076478Z WARNING: scanner_metrics_missing:SLV
2026-06-01T09:04:06.6885396Z ##[error]Process completed with exit code 1.
2026-06-01T09:04:06.7015966Z Post job cleanup.
2026-06-01T09:04:06.8029250Z [command]/usr/bin/git version
```

```text
2026-06-01T09:04:06.6074840Z WARNING: scanner_metrics_missing:MU
2026-06-01T09:04:06.6075645Z WARNING: scanner_metrics_missing:QQQ
2026-06-01T09:04:06.6076068Z WARNING: scanner_metrics_missing:GLD
2026-06-01T09:04:06.6076478Z WARNING: scanner_metrics_missing:SLV
2026-06-01T09:04:06.6885396Z ##[error]Process completed with exit code 1.
2026-06-01T09:04:06.7015966Z Post job cleanup.
2026-06-01T09:04:06.8029250Z [command]/usr/bin/git version
2026-06-01T09:04:06.8068562Z git version 2.54.0
2026-06-01T09:04:06.8116394Z Temporarily overriding HOME='/home/runner/work/_temp/4f80a9da-53eb-4fc8-bc52-5ff0e0856d3f' before making global git config changes
2026-06-01T09:04:06.8117877Z Adding repository directory to the temporary git global config as a safe directory
2026-06-01T09:04:06.8123698Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-06-01T09:04:06.8170239Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-06-01T09:04:06.8204241Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-06-01T09:04:06.8441007Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-06-01T09:04:06.8468009Z http.https://github.com/.extraheader
2026-06-01T09:04:06.8482399Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

### Failed job: validate-reports (weekly)

- Job ID: `78819743473`
- Started: 2026-06-01T09:03:35Z
- Completed: 2026-06-01T09:03:57Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-01T09:03:52.2896414Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-01T09:03:52.2897102Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-01T09:03:52.2897852Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-01T09:03:52.2898350Z ##[endgroup]
2026-06-01T09:03:55.5836865Z Traceback (most recent call last):
2026-06-01T09:03:55.5847284Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 247, in <module>
2026-06-01T09:03:55.5848228Z     raise SystemExit(main())
2026-06-01T09:03:55.5848551Z                      ^^^^^^
2026-06-01T09:03:55.5849692Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 236, in main
2026-06-01T09:03:55.5850698Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-01T09:03:55.5851290Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-01T09:03:55.5852324Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 68, in write_report_text_guarded
2026-06-01T09:03:55.5853376Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-01T09:03:55.5854504Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-06-01T09:03:55.5855572Z     raise ReportOutputBoundaryError(
2026-06-01T09:03:55.5856786Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
```

```text
2026-06-01T09:03:55.5853376Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-01T09:03:55.5854504Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-06-01T09:03:55.5855572Z     raise ReportOutputBoundaryError(
2026-06-01T09:03:55.5856786Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-06-01T09:03:55.6053841Z ##[error]Process completed with exit code 1.
2026-06-01T09:03:55.6178093Z Post job cleanup.
2026-06-01T09:03:55.7150451Z [command]/usr/bin/git version
2026-06-01T09:03:55.7186078Z git version 2.54.0
2026-06-01T09:03:55.7227503Z Temporarily overriding HOME='/home/runner/work/_temp/4dfb098c-03bc-4966-b761-46f3d52e591a' before making global git config changes
2026-06-01T09:03:55.7228525Z Adding repository directory to the temporary git global config as a safe directory
2026-06-01T09:03:55.7235545Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-06-01T09:03:55.7271280Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-06-01T09:03:55.7303049Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-06-01T09:03:55.7531048Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-06-01T09:03:55.7556083Z http.https://github.com/.extraheader
2026-06-01T09:03:55.7568439Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

## Decision Engine Tests

- Run ID: `26745179692`
- Branch: `main`
- Commit: `13263b855e75`
- Title: Document RGP6 strict notification handling
- Created: 2026-06-01T08:57:21Z
- Updated: 2026-06-01T08:57:57Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26745179692

### Failed job: tests

- Job ID: `78818732660`
- Started: 2026-06-01T08:57:24Z
- Completed: 2026-06-01T08:57:56Z
- Failed steps: 5. Run pytest

#### Error context

```text
2026-06-01T08:57:53.8379905Z ........................................................................ [ 87%]
2026-06-01T08:57:54.0549916Z ........................................................................ [ 92%]
2026-06-01T08:57:54.0986337Z ........................................................................ [ 98%]
2026-06-01T08:57:54.1656083Z ...........................                                              [100%]
2026-06-01T08:57:54.1657014Z =================================== FAILURES ===================================
2026-06-01T08:57:54.1657900Z _________ TestDataPersistence.test_decision_log_path_not_in_gitignore __________
2026-06-01T08:57:54.1658520Z 
2026-06-01T08:57:54.1658896Z self = <test_priority_fixes.TestDataPersistence object at 0x7f5946cbfe50>
2026-06-01T08:57:54.1659442Z 
2026-06-01T08:57:54.1659688Z     def test_decision_log_path_not_in_gitignore(self):
2026-06-01T08:57:54.1660239Z         gitignore = Path(".gitignore")
2026-06-01T08:57:54.1660946Z         if not gitignore.exists():
2026-06-01T08:57:54.1661319Z             return
2026-06-01T08:57:54.1661649Z         content = gitignore.read_text()
2026-06-01T08:57:54.1662086Z         # data/ should NOT be in gitignore
2026-06-01T08:57:54.1662515Z >       assert "data/" not in content, (
```

```text
2026-06-01T08:57:54.1662086Z         # data/ should NOT be in gitignore
2026-06-01T08:57:54.1662515Z >       assert "data/" not in content, (
2026-06-01T08:57:54.1663351Z             "data/ is in .gitignore â decision log will be lost on every run"
2026-06-01T08:57:54.1663890Z         )
2026-06-01T08:57:54.1664487Z E       AssertionError: data/ is in .gitignore â decision log will be lost on every run
2026-06-01T08:57:54.1665788Z E       assert 'data/' not in '# Python\n_...\n.vscode/\n'
2026-06-01T08:57:54.1666285Z E         
2026-06-01T08:57:54.1666580Z E         'data/' is contained here:
2026-06-01T08:57:54.1666949Z E           e/
2026-06-01T08:57:54.1667221Z E           cache/
2026-06-01T08:57:54.1667506Z E           data/raw/
2026-06-01T08:57:54.1667812Z E           data/live/
2026-06-01T08:57:54.1668126Z E           data/private/
2026-06-01T08:57:54.1668471Z E           data/vendor/
2026-06-01T08:57:54.1668793Z E           evidence/
2026-06-01T08:57:54.1669083Z E           lockbox/
```

```text
2026-06-01T08:57:54.1680738Z E           .DS_Store
2026-06-01T08:57:54.1681030Z E           .idea/
2026-06-01T08:57:54.1681310Z E           .vscode/
2026-06-01T08:57:54.1681494Z 
2026-06-01T08:57:54.1681682Z tests/test_priority_fixes.py:372: AssertionError
2026-06-01T08:57:54.1682204Z =============================== warnings summary ===============================
2026-06-01T08:57:54.1683120Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbol_writes_csv_and_metadata
2026-06-01T08:57:54.1684243Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbol_merges_without_duplicates
2026-06-01T08:57:54.1685409Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbols_batch_counts_results
2026-06-01T08:57:54.1686460Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbols_batch_counts_results
2026-06-01T08:57:54.1689216Z   /home/runner/work/institutional-trading-engine/institutional-trading-engine/src/historical/polygon_ingestion.py:125: FutureWarning: The behavior of DataFrame concatenation with empty or all-NA entries is deprecated. In a future version, this will no longer exclude empty or all-NA columns when determining the result dtypes. To retain the old behavior, exclude the relevant entries before the concat operation.
2026-06-01T08:57:54.1691965Z     combined = pd.concat([existing, df], ignore_index=True)
2026-06-01T08:57:54.1692326Z 
2026-06-01T08:57:54.1692639Z -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2026-06-01T08:57:54.1693513Z =========================== short test summary info ============================
2026-06-01T08:57:54.1695227Z FAILED tests/test_priority_fixes.py::TestDataPersistence::test_decision_log_path_not_in_gitignore - AssertionError: data/ is in .gitignore â decision log will be lost on every run
```

```text
2026-06-01T08:57:54.1691965Z     combined = pd.concat([existing, df], ignore_index=True)
2026-06-01T08:57:54.1692326Z 
2026-06-01T08:57:54.1692639Z -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2026-06-01T08:57:54.1693513Z =========================== short test summary info ============================
2026-06-01T08:57:54.1695227Z FAILED tests/test_priority_fixes.py::TestDataPersistence::test_decision_log_path_not_in_gitignore - AssertionError: data/ is in .gitignore â decision log will be lost on every run
2026-06-01T08:57:54.1696446Z assert 'data/' not in '# Python\n_...\n.vscode/\n'
2026-06-01T08:57:54.1696866Z   
2026-06-01T08:57:54.1697141Z   'data/' is contained here:
2026-06-01T08:57:54.1697495Z     e/
2026-06-01T08:57:54.1697749Z     cache/
2026-06-01T08:57:54.1698011Z     data/raw/
2026-06-01T08:57:54.1698309Z     data/live/
2026-06-01T08:57:54.1698602Z     data/private/
2026-06-01T08:57:54.1698918Z     data/vendor/
2026-06-01T08:57:54.1699208Z     evidence/
2026-06-01T08:57:54.1699483Z     lockbox/
```

```text
2026-06-01T08:57:54.1710201Z     .DS_Store
2026-06-01T08:57:54.1710477Z     .idea/
2026-06-01T08:57:54.1710731Z     .vscode/
2026-06-01T08:57:54.1711104Z 1 failed, 1393 passed, 1 skipped, 4 warnings in 10.84s
2026-06-01T08:57:54.3626139Z ##[error]Process completed with exit code 1.
2026-06-01T08:57:54.3743026Z Post job cleanup.
2026-06-01T08:57:54.4733905Z [command]/usr/bin/git version
2026-06-01T08:57:54.4768079Z git version 2.54.0
2026-06-01T08:57:54.4808890Z Temporarily overriding HOME='/home/runner/work/_temp/d201e6e1-41e4-4193-9797-dc280f2d2751' before making global git config changes
2026-06-01T08:57:54.4809825Z Adding repository directory to the temporary git global config as a safe directory
2026-06-01T08:57:54.4816895Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-06-01T08:57:54.4854711Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-06-01T08:57:54.4883829Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-06-01T08:57:54.5106969Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-06-01T08:57:54.5130342Z http.https://github.com/.extraheader
2026-06-01T08:57:54.5142968Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

## Report Quality Validation

- Run ID: `26745179675`
- Branch: `main`
- Commit: `13263b855e75`
- Title: Document RGP6 strict notification handling
- Created: 2026-06-01T08:57:21Z
- Updated: 2026-06-01T08:58:00Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26745179675

### Failed job: validate-reports (postmarket)

- Job ID: `78818732904`
- Started: 2026-06-01T08:57:23Z
- Completed: 2026-06-01T08:57:59Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-01T08:57:41.6261409Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-01T08:57:41.6261815Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-01T08:57:41.6262287Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-01T08:57:41.6262634Z ##[endgroup]
2026-06-01T08:57:57.4878302Z Traceback (most recent call last):
2026-06-01T08:57:57.4885365Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 247, in <module>
2026-06-01T08:57:57.4887404Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-28/2026-06-01?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-01T08:57:57.4888288Z     raise SystemExit(main())
2026-06-01T08:57:57.4888564Z                      ^^^^^^
2026-06-01T08:57:57.4889231Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 236, in main
2026-06-01T08:57:57.4890019Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-01T08:57:57.4890490Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-01T08:57:57.4891231Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 68, in write_report_text_guarded
2026-06-01T08:57:57.4891996Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-01T08:57:57.4892822Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-06-01T08:57:57.4893545Z     raise ReportOutputBoundaryError(
```

```text
2026-06-01T08:57:57.4893545Z     raise ReportOutputBoundaryError(
2026-06-01T08:57:57.4894633Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/postmarket-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-06-01T08:57:57.4896230Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-28/2026-06-01?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-01T08:57:57.4897582Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-28/2026-06-01?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-01T08:57:57.4898509Z WARNING: scanner metric loading failed: ModuleNotFoundError: No module named 'config'
2026-06-01T08:57:57.4898968Z WARNING: scanner_metrics_missing:MSFT
2026-06-01T08:57:57.4899260Z WARNING: scanner_metrics_missing:NVDA
2026-06-01T08:57:57.4899562Z WARNING: scanner_metrics_missing:META
2026-06-01T08:57:57.4899848Z WARNING: scanner_metrics_missing:AAPL
2026-06-01T08:57:57.4900133Z WARNING: scanner_metrics_missing:MU
2026-06-01T08:57:57.4900757Z WARNING: scanner_metrics_missing:QQQ
2026-06-01T08:57:57.4901035Z WARNING: scanner_metrics_missing:GLD
2026-06-01T08:57:57.4901311Z WARNING: scanner_metrics_missing:SLV
2026-06-01T08:57:57.5654303Z ##[error]Process completed with exit code 1.
2026-06-01T08:57:57.5779473Z Post job cleanup.
2026-06-01T08:57:57.6770545Z [command]/usr/bin/git version
```

```text
2026-06-01T08:57:57.4900133Z WARNING: scanner_metrics_missing:MU
2026-06-01T08:57:57.4900757Z WARNING: scanner_metrics_missing:QQQ
2026-06-01T08:57:57.4901035Z WARNING: scanner_metrics_missing:GLD
2026-06-01T08:57:57.4901311Z WARNING: scanner_metrics_missing:SLV
2026-06-01T08:57:57.5654303Z ##[error]Process completed with exit code 1.
2026-06-01T08:57:57.5779473Z Post job cleanup.
2026-06-01T08:57:57.6770545Z [command]/usr/bin/git version
2026-06-01T08:57:57.6808356Z git version 2.54.0
2026-06-01T08:57:57.6850190Z Temporarily overriding HOME='/home/runner/work/_temp/2d1668a7-2415-449a-ac1f-8df2f4f5819f' before making global git config changes
2026-06-01T08:57:57.6851450Z Adding repository directory to the temporary git global config as a safe directory
2026-06-01T08:57:57.6865260Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-06-01T08:57:57.6907553Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-06-01T08:57:57.6953444Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-06-01T08:57:57.7224287Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-06-01T08:57:57.7252318Z http.https://github.com/.extraheader
2026-06-01T08:57:57.7264987Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

### Failed job: validate-reports (premarket)

- Job ID: `78818732921`
- Started: 2026-06-01T08:57:23Z
- Completed: 2026-06-01T08:57:57Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-01T08:57:40.3906578Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-01T08:57:40.3906979Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-01T08:57:40.3907417Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-01T08:57:40.3907785Z ##[endgroup]
2026-06-01T08:57:55.2671009Z Traceback (most recent call last):
2026-06-01T08:57:55.2679247Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 247, in <module>
2026-06-01T08:57:55.2680914Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-28/2026-06-01?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-01T08:57:55.2681863Z     raise SystemExit(main())
2026-06-01T08:57:55.2682140Z                      ^^^^^^
2026-06-01T08:57:55.2682798Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 236, in main
2026-06-01T08:57:55.2683605Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-01T08:57:55.2684452Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-01T08:57:55.2685223Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 68, in write_report_text_guarded
2026-06-01T08:57:55.2686036Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-01T08:57:55.2686862Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-06-01T08:57:55.2687604Z     raise ReportOutputBoundaryError(
```

```text
2026-06-01T08:57:55.2687604Z     raise ReportOutputBoundaryError(
2026-06-01T08:57:55.2688554Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/premarket-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-06-01T08:57:55.2690132Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-28/2026-06-01?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-01T08:57:55.2691478Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-28/2026-06-01?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-01T08:57:55.2692386Z WARNING: scanner metric loading failed: ModuleNotFoundError: No module named 'config'
2026-06-01T08:57:55.2692836Z WARNING: scanner_metrics_missing:MSFT
2026-06-01T08:57:55.2693132Z WARNING: scanner_metrics_missing:NVDA
2026-06-01T08:57:55.2693409Z WARNING: scanner_metrics_missing:META
2026-06-01T08:57:55.2693695Z WARNING: scanner_metrics_missing:AAPL
2026-06-01T08:57:55.2694161Z WARNING: scanner_metrics_missing:MU
2026-06-01T08:57:55.2694731Z WARNING: scanner_metrics_missing:QQQ
2026-06-01T08:57:55.2695016Z WARNING: scanner_metrics_missing:GLD
2026-06-01T08:57:55.2695299Z WARNING: scanner_metrics_missing:SLV
2026-06-01T08:57:55.3394052Z ##[error]Process completed with exit code 1.
2026-06-01T08:57:55.3519132Z Post job cleanup.
2026-06-01T08:57:55.4507225Z [command]/usr/bin/git version
```

```text
2026-06-01T08:57:55.2694161Z WARNING: scanner_metrics_missing:MU
2026-06-01T08:57:55.2694731Z WARNING: scanner_metrics_missing:QQQ
2026-06-01T08:57:55.2695016Z WARNING: scanner_metrics_missing:GLD
2026-06-01T08:57:55.2695299Z WARNING: scanner_metrics_missing:SLV
2026-06-01T08:57:55.3394052Z ##[error]Process completed with exit code 1.
2026-06-01T08:57:55.3519132Z Post job cleanup.
2026-06-01T08:57:55.4507225Z [command]/usr/bin/git version
2026-06-01T08:57:55.4544664Z git version 2.54.0
2026-06-01T08:57:55.4586442Z Temporarily overriding HOME='/home/runner/work/_temp/c3240ec8-b711-4368-b009-3f04380d8a5e' before making global git config changes
2026-06-01T08:57:55.4587754Z Adding repository directory to the temporary git global config as a safe directory
2026-06-01T08:57:55.4592786Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-06-01T08:57:55.4631053Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-06-01T08:57:55.4665979Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-06-01T08:57:55.4912503Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-06-01T08:57:55.4939429Z http.https://github.com/.extraheader
2026-06-01T08:57:55.4951625Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

### Failed job: validate-reports (weekly)

- Job ID: `78818732940`
- Started: 2026-06-01T08:57:24Z
- Completed: 2026-06-01T08:57:43Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-01T08:57:41.0266733Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-01T08:57:41.0267144Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-01T08:57:41.0267610Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-01T08:57:41.0267968Z ##[endgroup]
2026-06-01T08:57:41.3685612Z Traceback (most recent call last):
2026-06-01T08:57:41.3692960Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 247, in <module>
2026-06-01T08:57:41.3694061Z     raise SystemExit(main())
2026-06-01T08:57:41.3694407Z                      ^^^^^^
2026-06-01T08:57:41.3695606Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 236, in main
2026-06-01T08:57:41.3696794Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-01T08:57:41.3705821Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-01T08:57:41.3706851Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 68, in write_report_text_guarded
2026-06-01T08:57:41.3707729Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-01T08:57:41.3708663Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-06-01T08:57:41.3709487Z     raise ReportOutputBoundaryError(
2026-06-01T08:57:41.3710521Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
```

```text
2026-06-01T08:57:41.3707729Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-01T08:57:41.3708663Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-06-01T08:57:41.3709487Z     raise ReportOutputBoundaryError(
2026-06-01T08:57:41.3710521Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-06-01T08:57:41.3929448Z ##[error]Process completed with exit code 1.
2026-06-01T08:57:41.4056303Z Post job cleanup.
2026-06-01T08:57:41.5028262Z [command]/usr/bin/git version
2026-06-01T08:57:41.5066903Z git version 2.54.0
2026-06-01T08:57:41.5112174Z Temporarily overriding HOME='/home/runner/work/_temp/ce42b33c-7ca2-47b6-808a-9a602fde8ba1' before making global git config changes
2026-06-01T08:57:41.5113741Z Adding repository directory to the temporary git global config as a safe directory
2026-06-01T08:57:41.5126476Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-06-01T08:57:41.5162066Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-06-01T08:57:41.5195278Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-06-01T08:57:41.5424278Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-06-01T08:57:41.5450723Z http.https://github.com/.extraheader
2026-06-01T08:57:41.5463090Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

## Report Quality Validation

- Run ID: `26744750758`
- Branch: `main`
- Commit: `b51c200140d6`
- Title: Add RGP6 strict critical notification tests
- Created: 2026-06-01T08:48:19Z
- Updated: 2026-06-01T08:48:59Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26744750758

### Failed job: validate-reports (premarket)

- Job ID: `78817275199`
- Started: 2026-06-01T08:48:22Z
- Completed: 2026-06-01T08:48:53Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-01T08:48:38.2081076Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-01T08:48:38.2081477Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-01T08:48:38.2081902Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-01T08:48:38.2082255Z ##[endgroup]
2026-06-01T08:48:52.7396422Z Traceback (most recent call last):
2026-06-01T08:48:52.7406231Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 247, in <module>
2026-06-01T08:48:52.7408345Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-28/2026-06-01?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-01T08:48:52.7409534Z     raise SystemExit(main())
2026-06-01T08:48:52.7409840Z                      ^^^^^^
2026-06-01T08:48:52.7410520Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 236, in main
2026-06-01T08:48:52.7411312Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-01T08:48:52.7411786Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-01T08:48:52.7412585Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 68, in write_report_text_guarded
2026-06-01T08:48:52.7413366Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-01T08:48:52.7414196Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-06-01T08:48:52.7414920Z     raise ReportOutputBoundaryError(
```

```text
2026-06-01T08:48:52.7414920Z     raise ReportOutputBoundaryError(
2026-06-01T08:48:52.7415855Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/premarket-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-06-01T08:48:52.7417461Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-28/2026-06-01?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-01T08:48:52.7418791Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-28/2026-06-01?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-01T08:48:52.7419840Z WARNING: scanner metric loading failed: ModuleNotFoundError: No module named 'config'
2026-06-01T08:48:52.7420294Z WARNING: scanner_metrics_missing:MSFT
2026-06-01T08:48:52.7420606Z WARNING: scanner_metrics_missing:NVDA
2026-06-01T08:48:52.7420892Z WARNING: scanner_metrics_missing:META
2026-06-01T08:48:52.7421171Z WARNING: scanner_metrics_missing:AAPL
2026-06-01T08:48:52.7421454Z WARNING: scanner_metrics_missing:MU
2026-06-01T08:48:52.7422025Z WARNING: scanner_metrics_missing:QQQ
2026-06-01T08:48:52.7422310Z WARNING: scanner_metrics_missing:GLD
2026-06-01T08:48:52.7422581Z WARNING: scanner_metrics_missing:SLV
2026-06-01T08:48:52.8112307Z ##[error]Process completed with exit code 1.
2026-06-01T08:48:52.8237947Z Post job cleanup.
2026-06-01T08:48:52.9228819Z [command]/usr/bin/git version
```

```text
2026-06-01T08:48:52.7421454Z WARNING: scanner_metrics_missing:MU
2026-06-01T08:48:52.7422025Z WARNING: scanner_metrics_missing:QQQ
2026-06-01T08:48:52.7422310Z WARNING: scanner_metrics_missing:GLD
2026-06-01T08:48:52.7422581Z WARNING: scanner_metrics_missing:SLV
2026-06-01T08:48:52.8112307Z ##[error]Process completed with exit code 1.
2026-06-01T08:48:52.8237947Z Post job cleanup.
2026-06-01T08:48:52.9228819Z [command]/usr/bin/git version
2026-06-01T08:48:52.9266647Z git version 2.54.0
2026-06-01T08:48:52.9307298Z Temporarily overriding HOME='/home/runner/work/_temp/292a7845-430f-4151-8bc5-ab89f0cb943d' before making global git config changes
2026-06-01T08:48:52.9308234Z Adding repository directory to the temporary git global config as a safe directory
2026-06-01T08:48:52.9322827Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-06-01T08:48:52.9359920Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-06-01T08:48:52.9393819Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-06-01T08:48:52.9640463Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-06-01T08:48:52.9665134Z http.https://github.com/.extraheader
2026-06-01T08:48:52.9678255Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

### Failed job: validate-reports (postmarket)

- Job ID: `78817275206`
- Started: 2026-06-01T08:48:22Z
- Completed: 2026-06-01T08:48:58Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-01T08:48:41.1526678Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-01T08:48:41.1527088Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-01T08:48:41.1527538Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-01T08:48:41.1527907Z ##[endgroup]
2026-06-01T08:48:56.8313778Z Traceback (most recent call last):
2026-06-01T08:48:56.8315271Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-28/2026-06-01?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-01T08:48:56.8325559Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 247, in <module>
2026-06-01T08:48:56.8327764Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-28/2026-06-01?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-01T08:48:56.8328821Z     raise SystemExit(main())
2026-06-01T08:48:56.8329097Z                      ^^^^^^
2026-06-01T08:48:56.8330079Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 236, in main
2026-06-01T08:48:56.8330878Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-01T08:48:56.8331373Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-01T08:48:56.8332160Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 68, in write_report_text_guarded
2026-06-01T08:48:56.8332937Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-01T08:48:56.8333779Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
```

```text
2026-06-01T08:48:56.8333779Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-06-01T08:48:56.8334534Z     raise ReportOutputBoundaryError(
2026-06-01T08:48:56.8335495Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/postmarket-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-06-01T08:48:56.8337056Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-28/2026-06-01?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-01T08:48:56.8338008Z WARNING: scanner metric loading failed: ModuleNotFoundError: No module named 'config'
2026-06-01T08:48:56.8338467Z WARNING: scanner_metrics_missing:MSFT
2026-06-01T08:48:56.8338755Z WARNING: scanner_metrics_missing:NVDA
2026-06-01T08:48:56.8339031Z WARNING: scanner_metrics_missing:META
2026-06-01T08:48:56.8339526Z WARNING: scanner_metrics_missing:AAPL
2026-06-01T08:48:56.8339807Z WARNING: scanner_metrics_missing:MU
2026-06-01T08:48:56.8340408Z WARNING: scanner_metrics_missing:QQQ
2026-06-01T08:48:56.8340689Z WARNING: scanner_metrics_missing:GLD
2026-06-01T08:48:56.8340971Z WARNING: scanner_metrics_missing:SLV
2026-06-01T08:48:56.9524499Z ##[error]Process completed with exit code 1.
2026-06-01T08:48:56.9651903Z Post job cleanup.
2026-06-01T08:48:57.0725318Z [command]/usr/bin/git version
```

```text
2026-06-01T08:48:56.8339807Z WARNING: scanner_metrics_missing:MU
2026-06-01T08:48:56.8340408Z WARNING: scanner_metrics_missing:QQQ
2026-06-01T08:48:56.8340689Z WARNING: scanner_metrics_missing:GLD
2026-06-01T08:48:56.8340971Z WARNING: scanner_metrics_missing:SLV
2026-06-01T08:48:56.9524499Z ##[error]Process completed with exit code 1.
2026-06-01T08:48:56.9651903Z Post job cleanup.
2026-06-01T08:48:57.0725318Z [command]/usr/bin/git version
2026-06-01T08:48:57.0765625Z git version 2.54.0
2026-06-01T08:48:57.0812093Z Temporarily overriding HOME='/home/runner/work/_temp/0eab85c7-9b89-4fd4-a026-91d52b0b58e8' before making global git config changes
2026-06-01T08:48:57.0813347Z Adding repository directory to the temporary git global config as a safe directory
2026-06-01T08:48:57.0828551Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-06-01T08:48:57.0874386Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-06-01T08:48:57.0914542Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-06-01T08:48:57.1173603Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-06-01T08:48:57.1201345Z http.https://github.com/.extraheader
2026-06-01T08:48:57.1215053Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

### Failed job: validate-reports (weekly)

- Job ID: `78817275251`
- Started: 2026-06-01T08:48:22Z
- Completed: 2026-06-01T08:48:41Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-01T08:48:37.7221420Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-01T08:48:37.7221730Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-01T08:48:37.7222069Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-01T08:48:37.7222340Z ##[endgroup]
2026-06-01T08:48:38.3187579Z Traceback (most recent call last):
2026-06-01T08:48:38.3194501Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 247, in <module>
2026-06-01T08:48:38.3195068Z     raise SystemExit(main())
2026-06-01T08:48:38.3195281Z                      ^^^^^^
2026-06-01T08:48:38.3195786Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 236, in main
2026-06-01T08:48:38.3196376Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-01T08:48:38.3196726Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-01T08:48:38.3197316Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 68, in write_report_text_guarded
2026-06-01T08:48:38.3197920Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-01T08:48:38.3198562Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-06-01T08:48:38.3199133Z     raise ReportOutputBoundaryError(
2026-06-01T08:48:38.3199857Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
```

```text
2026-06-01T08:48:38.3197920Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-01T08:48:38.3198562Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-06-01T08:48:38.3199133Z     raise ReportOutputBoundaryError(
2026-06-01T08:48:38.3199857Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-06-01T08:48:38.3388626Z ##[error]Process completed with exit code 1.
2026-06-01T08:48:38.3480416Z Post job cleanup.
2026-06-01T08:48:38.4260598Z [command]/usr/bin/git version
2026-06-01T08:48:38.4290258Z git version 2.54.0
2026-06-01T08:48:38.4322286Z Temporarily overriding HOME='/home/runner/work/_temp/f749ac3b-bfde-4ef5-9d18-3f9e88659366' before making global git config changes
2026-06-01T08:48:38.4323247Z Adding repository directory to the temporary git global config as a safe directory
2026-06-01T08:48:38.4332513Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-06-01T08:48:38.4360471Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-06-01T08:48:38.4386229Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-06-01T08:48:38.4583683Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-06-01T08:48:38.4610454Z http.https://github.com/.extraheader
2026-06-01T08:48:38.4641719Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

## Decision Engine Tests

- Run ID: `26744750858`
- Branch: `main`
- Commit: `b51c200140d6`
- Title: Add RGP6 strict critical notification tests
- Created: 2026-06-01T08:48:19Z
- Updated: 2026-06-01T08:48:52Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26744750858

### Failed job: tests

- Job ID: `78817275046`
- Started: 2026-06-01T08:48:22Z
- Completed: 2026-06-01T08:48:51Z
- Failed steps: 5. Run pytest

#### Error context

```text
2026-06-01T08:48:49.4130123Z ........................................................................ [ 87%]
2026-06-01T08:48:49.6277787Z ........................................................................ [ 92%]
2026-06-01T08:48:49.6654298Z ........................................................................ [ 98%]
2026-06-01T08:48:49.7266418Z ...........................                                              [100%]
2026-06-01T08:48:49.7267385Z =================================== FAILURES ===================================
2026-06-01T08:48:49.7268432Z _________ TestDataPersistence.test_decision_log_path_not_in_gitignore __________
2026-06-01T08:48:49.7268945Z 
2026-06-01T08:48:49.7269256Z self = <test_priority_fixes.TestDataPersistence object at 0x7f1a2034b610>
2026-06-01T08:48:49.7269714Z 
2026-06-01T08:48:49.7269937Z     def test_decision_log_path_not_in_gitignore(self):
2026-06-01T08:48:49.7270436Z         gitignore = Path(".gitignore")
2026-06-01T08:48:49.7271188Z         if not gitignore.exists():
2026-06-01T08:48:49.7271539Z             return
2026-06-01T08:48:49.7271843Z         content = gitignore.read_text()
2026-06-01T08:48:49.7272232Z         # data/ should NOT be in gitignore
2026-06-01T08:48:49.7272617Z >       assert "data/" not in content, (
```

```text
2026-06-01T08:48:49.7272232Z         # data/ should NOT be in gitignore
2026-06-01T08:48:49.7272617Z >       assert "data/" not in content, (
2026-06-01T08:48:49.7273453Z             "data/ is in .gitignore â decision log will be lost on every run"
2026-06-01T08:48:49.7273952Z         )
2026-06-01T08:48:49.7274504Z E       AssertionError: data/ is in .gitignore â decision log will be lost on every run
2026-06-01T08:48:49.7275446Z E       assert 'data/' not in '# Python\n_...\n.vscode/\n'
2026-06-01T08:48:49.7275872Z E         
2026-06-01T08:48:49.7276147Z E         'data/' is contained here:
2026-06-01T08:48:49.7276500Z E           e/
2026-06-01T08:48:49.7276757Z E           cache/
2026-06-01T08:48:49.7277019Z E           data/raw/
2026-06-01T08:48:49.7277302Z E           data/live/
2026-06-01T08:48:49.7277595Z E           data/private/
2026-06-01T08:48:49.7277917Z E           data/vendor/
2026-06-01T08:48:49.7278423Z E           evidence/
2026-06-01T08:48:49.7278699Z E           lockbox/
```

```text
2026-06-01T08:48:49.7289457Z E           .DS_Store
2026-06-01T08:48:49.7289734Z E           .idea/
2026-06-01T08:48:49.7289995Z E           .vscode/
2026-06-01T08:48:49.7290165Z 
2026-06-01T08:48:49.7290330Z tests/test_priority_fixes.py:372: AssertionError
2026-06-01T08:48:49.7290843Z =============================== warnings summary ===============================
2026-06-01T08:48:49.7291923Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbol_writes_csv_and_metadata
2026-06-01T08:48:49.7292888Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbol_merges_without_duplicates
2026-06-01T08:48:49.7293835Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbols_batch_counts_results
2026-06-01T08:48:49.7294754Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbols_batch_counts_results
2026-06-01T08:48:49.7297263Z   /home/runner/work/institutional-trading-engine/institutional-trading-engine/src/historical/polygon_ingestion.py:125: FutureWarning: The behavior of DataFrame concatenation with empty or all-NA entries is deprecated. In a future version, this will no longer exclude empty or all-NA columns when determining the result dtypes. To retain the old behavior, exclude the relevant entries before the concat operation.
2026-06-01T08:48:49.7299972Z     combined = pd.concat([existing, df], ignore_index=True)
2026-06-01T08:48:49.7300316Z 
2026-06-01T08:48:49.7300618Z -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2026-06-01T08:48:49.7301471Z =========================== short test summary info ============================
2026-06-01T08:48:49.7302883Z FAILED tests/test_priority_fixes.py::TestDataPersistence::test_decision_log_path_not_in_gitignore - AssertionError: data/ is in .gitignore â decision log will be lost on every run
```

```text
2026-06-01T08:48:49.7299972Z     combined = pd.concat([existing, df], ignore_index=True)
2026-06-01T08:48:49.7300316Z 
2026-06-01T08:48:49.7300618Z -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2026-06-01T08:48:49.7301471Z =========================== short test summary info ============================
2026-06-01T08:48:49.7302883Z FAILED tests/test_priority_fixes.py::TestDataPersistence::test_decision_log_path_not_in_gitignore - AssertionError: data/ is in .gitignore â decision log will be lost on every run
2026-06-01T08:48:49.7303991Z assert 'data/' not in '# Python\n_...\n.vscode/\n'
2026-06-01T08:48:49.7304385Z   
2026-06-01T08:48:49.7304640Z   'data/' is contained here:
2026-06-01T08:48:49.7304955Z     e/
2026-06-01T08:48:49.7305186Z     cache/
2026-06-01T08:48:49.7305438Z     data/raw/
2026-06-01T08:48:49.7305687Z     data/live/
2026-06-01T08:48:49.7305940Z     data/private/
2026-06-01T08:48:49.7306211Z     data/vendor/
2026-06-01T08:48:49.7306468Z     evidence/
2026-06-01T08:48:49.7306715Z     lockbox/
```

```text
2026-06-01T08:48:49.7316456Z     .DS_Store
2026-06-01T08:48:49.7316707Z     .idea/
2026-06-01T08:48:49.7316960Z     .vscode/
2026-06-01T08:48:49.7317305Z 1 failed, 1393 passed, 1 skipped, 4 warnings in 11.39s
2026-06-01T08:48:50.1489463Z ##[error]Process completed with exit code 1.
2026-06-01T08:48:50.1605403Z Post job cleanup.
2026-06-01T08:48:50.2605375Z [command]/usr/bin/git version
2026-06-01T08:48:50.2642819Z git version 2.54.0
2026-06-01T08:48:50.2684555Z Temporarily overriding HOME='/home/runner/work/_temp/f92f4fa9-56b9-451b-b42d-510b87c12f14' before making global git config changes
2026-06-01T08:48:50.2685731Z Adding repository directory to the temporary git global config as a safe directory
2026-06-01T08:48:50.2698970Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-06-01T08:48:50.2737575Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-06-01T08:48:50.2773089Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-06-01T08:48:50.3023154Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-06-01T08:48:50.3050785Z http.https://github.com/.extraheader
2026-06-01T08:48:50.3063366Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

## Decision Engine Tests

- Run ID: `26744237408`
- Branch: `main`
- Commit: `9988fccb5b17`
- Title: Implement RGP6 strict critical notification handling
- Created: 2026-06-01T08:37:31Z
- Updated: 2026-06-01T08:38:05Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26744237408

### Failed job: tests

- Job ID: `78815553114`
- Started: 2026-06-01T08:37:34Z
- Completed: 2026-06-01T08:38:04Z
- Failed steps: 5. Run pytest

#### Error context

```text
2026-06-01T08:38:02.3371805Z ........................................................................ [ 87%]
2026-06-01T08:38:02.5755378Z ........................................................................ [ 93%]
2026-06-01T08:38:02.6203402Z ........................................................................ [ 98%]
2026-06-01T08:38:02.6864134Z .........................                                                [100%]
2026-06-01T08:38:02.6865155Z =================================== FAILURES ===================================
2026-06-01T08:38:02.6865855Z _______ test_critical_stop_alert_message_is_research_only_and_order_safe _______
2026-06-01T08:38:02.6866319Z 
2026-06-01T08:38:02.6866690Z     def test_critical_stop_alert_message_is_research_only_and_order_safe() -> None:
2026-06-01T08:38:02.6867300Z         message = build_critical_runtime_alert_message(
2026-06-01T08:38:02.6868093Z             CriticalRuntimeAlert(
2026-06-01T08:38:02.6868704Z                 alert_type="STOP",
2026-06-01T08:38:02.6869019Z                 signal_id="sig-001",
2026-06-01T08:38:02.6869335Z                 symbol="AAPL",
2026-06-01T08:38:02.6869689Z                 reason="stop lifecycle threshold reached",
2026-06-01T08:38:02.6870055Z             )
2026-06-01T08:38:02.6870287Z         )
```

```text
2026-06-01T08:38:02.6870287Z         )
2026-06-01T08:38:02.6870525Z         rendered = message.render()
2026-06-01T08:38:02.6870870Z     
2026-06-01T08:38:02.6871169Z >       assert "RGP5 Critical STOP Runtime Alert" in rendered
2026-06-01T08:38:02.6872942Z E       AssertionError: assert 'RGP5 Critical STOP Runtime Alert' in '*RGP5/RGP6 Critical STOP Runtime Alert*\nAlert type: STOP\nSignal ID: sig-001\nSymbol: AAPL\nLifecycle status: critic...elivery only\nReal-money authorization: not granted\nResearch / Paper Observation Only. No live trading authorization.'
2026-06-01T08:38:02.6874385Z 
2026-06-01T08:38:02.6874567Z tests/test_critical_runtime_alert.py:25: AssertionError
2026-06-01T08:38:02.6875143Z _________ TestDataPersistence.test_decision_log_path_not_in_gitignore __________
2026-06-01T08:38:02.6875555Z 
2026-06-01T08:38:02.6875799Z self = <test_priority_fixes.TestDataPersistence object at 0x7f6d2507b5d0>
2026-06-01T08:38:02.6876176Z 
2026-06-01T08:38:02.6876342Z     def test_decision_log_path_not_in_gitignore(self):
2026-06-01T08:38:02.6876736Z         gitignore = Path(".gitignore")
2026-06-01T08:38:02.6877075Z         if not gitignore.exists():
2026-06-01T08:38:02.6877519Z             return
2026-06-01T08:38:02.6877777Z         content = gitignore.read_text()
```

```text
2026-06-01T08:38:02.6870870Z     
2026-06-01T08:38:02.6871169Z >       assert "RGP5 Critical STOP Runtime Alert" in rendered
2026-06-01T08:38:02.6872942Z E       AssertionError: assert 'RGP5 Critical STOP Runtime Alert' in '*RGP5/RGP6 Critical STOP Runtime Alert*\nAlert type: STOP\nSignal ID: sig-001\nSymbol: AAPL\nLifecycle status: critic...elivery only\nReal-money authorization: not granted\nResearch / Paper Observation Only. No live trading authorization.'
2026-06-01T08:38:02.6874385Z 
2026-06-01T08:38:02.6874567Z tests/test_critical_runtime_alert.py:25: AssertionError
2026-06-01T08:38:02.6875143Z _________ TestDataPersistence.test_decision_log_path_not_in_gitignore __________
2026-06-01T08:38:02.6875555Z 
2026-06-01T08:38:02.6875799Z self = <test_priority_fixes.TestDataPersistence object at 0x7f6d2507b5d0>
2026-06-01T08:38:02.6876176Z 
2026-06-01T08:38:02.6876342Z     def test_decision_log_path_not_in_gitignore(self):
2026-06-01T08:38:02.6876736Z         gitignore = Path(".gitignore")
2026-06-01T08:38:02.6877075Z         if not gitignore.exists():
2026-06-01T08:38:02.6877519Z             return
2026-06-01T08:38:02.6877777Z         content = gitignore.read_text()
2026-06-01T08:38:02.6878091Z         # data/ should NOT be in gitignore
2026-06-01T08:38:02.6878392Z >       assert "data/" not in content, (
```

```text
2026-06-01T08:38:02.6878091Z         # data/ should NOT be in gitignore
2026-06-01T08:38:02.6878392Z >       assert "data/" not in content, (
2026-06-01T08:38:02.6878986Z             "data/ is in .gitignore â decision log will be lost on every run"
2026-06-01T08:38:02.6879354Z         )
2026-06-01T08:38:02.6879763Z E       AssertionError: data/ is in .gitignore â decision log will be lost on every run
2026-06-01T08:38:02.6880241Z E       assert 'data/' not in '# Python\n_...\n.vscode/\n'
2026-06-01T08:38:02.6880566Z E         
2026-06-01T08:38:02.6880786Z E         'data/' is contained here:
2026-06-01T08:38:02.6881056Z E           e/
2026-06-01T08:38:02.6881265Z E           cache/
2026-06-01T08:38:02.6881486Z E           data/raw/
2026-06-01T08:38:02.6881711Z E           data/live/
2026-06-01T08:38:02.6881946Z E           data/private/
2026-06-01T08:38:02.6882190Z E           data/vendor/
2026-06-01T08:38:02.6882426Z E           evidence/
2026-06-01T08:38:02.6882650Z E           lockbox/
```

```text
2026-06-01T08:38:02.6891522Z E           .DS_Store
2026-06-01T08:38:02.6891735Z E           .idea/
2026-06-01T08:38:02.6891944Z E           .vscode/
2026-06-01T08:38:02.6892079Z 
2026-06-01T08:38:02.6892358Z tests/test_priority_fixes.py:372: AssertionError
2026-06-01T08:38:02.6892751Z =============================== warnings summary ===============================
2026-06-01T08:38:02.6893433Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbol_writes_csv_and_metadata
2026-06-01T08:38:02.6894141Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbol_merges_without_duplicates
2026-06-01T08:38:02.6894834Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbols_batch_counts_results
2026-06-01T08:38:02.6895512Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbols_batch_counts_results
2026-06-01T08:38:02.6897477Z   /home/runner/work/institutional-trading-engine/institutional-trading-engine/src/historical/polygon_ingestion.py:125: FutureWarning: The behavior of DataFrame concatenation with empty or all-NA entries is deprecated. In a future version, this will no longer exclude empty or all-NA columns when determining the result dtypes. To retain the old behavior, exclude the relevant entries before the concat operation.
2026-06-01T08:38:02.6899150Z     combined = pd.concat([existing, df], ignore_index=True)
2026-06-01T08:38:02.6899408Z 
2026-06-01T08:38:02.6899657Z -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2026-06-01T08:38:02.6900159Z =========================== short test summary info ============================
2026-06-01T08:38:02.6901802Z FAILED tests/test_critical_runtime_alert.py::test_critical_stop_alert_message_is_research_only_and_order_safe - AssertionError: assert 'RGP5 Critical STOP Runtime Alert' in '*RGP5/RGP6 Critical STOP Runtime Alert*\nAlert type: STOP\nSignal ID: sig-001\nSymbol: AAPL\nLifecycle status: critic...elivery only\nReal-money authorization: not granted\nResearch / Paper Observation Only. No live trading authorization.'
```

```text
2026-06-01T08:38:02.6899150Z     combined = pd.concat([existing, df], ignore_index=True)
2026-06-01T08:38:02.6899408Z 
2026-06-01T08:38:02.6899657Z -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2026-06-01T08:38:02.6900159Z =========================== short test summary info ============================
2026-06-01T08:38:02.6901802Z FAILED tests/test_critical_runtime_alert.py::test_critical_stop_alert_message_is_research_only_and_order_safe - AssertionError: assert 'RGP5 Critical STOP Runtime Alert' in '*RGP5/RGP6 Critical STOP Runtime Alert*\nAlert type: STOP\nSignal ID: sig-001\nSymbol: AAPL\nLifecycle status: critic...elivery only\nReal-money authorization: not granted\nResearch / Paper Observation Only. No live trading authorization.'
2026-06-01T08:38:02.6903975Z FAILED tests/test_priority_fixes.py::TestDataPersistence::test_decision_log_path_not_in_gitignore - AssertionError: data/ is in .gitignore â decision log will be lost on every run
2026-06-01T08:38:02.6904771Z assert 'data/' not in '# Python\n_...\n.vscode/\n'
2026-06-01T08:38:02.6905084Z   
2026-06-01T08:38:02.6905291Z   'data/' is contained here:
2026-06-01T08:38:02.6905538Z     e/
2026-06-01T08:38:02.6905737Z     cache/
2026-06-01T08:38:02.6905940Z     data/raw/
2026-06-01T08:38:02.6906144Z     data/live/
2026-06-01T08:38:02.6906360Z     data/private/
2026-06-01T08:38:02.6906591Z     data/vendor/
2026-06-01T08:38:02.6906802Z     evidence/
```

```text
2026-06-01T08:38:02.6899408Z 
2026-06-01T08:38:02.6899657Z -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2026-06-01T08:38:02.6900159Z =========================== short test summary info ============================
2026-06-01T08:38:02.6901802Z FAILED tests/test_critical_runtime_alert.py::test_critical_stop_alert_message_is_research_only_and_order_safe - AssertionError: assert 'RGP5 Critical STOP Runtime Alert' in '*RGP5/RGP6 Critical STOP Runtime Alert*\nAlert type: STOP\nSignal ID: sig-001\nSymbol: AAPL\nLifecycle status: critic...elivery only\nReal-money authorization: not granted\nResearch / Paper Observation Only. No live trading authorization.'
2026-06-01T08:38:02.6903975Z FAILED tests/test_priority_fixes.py::TestDataPersistence::test_decision_log_path_not_in_gitignore - AssertionError: data/ is in .gitignore â decision log will be lost on every run
2026-06-01T08:38:02.6904771Z assert 'data/' not in '# Python\n_...\n.vscode/\n'
2026-06-01T08:38:02.6905084Z   
2026-06-01T08:38:02.6905291Z   'data/' is contained here:
2026-06-01T08:38:02.6905538Z     e/
2026-06-01T08:38:02.6905737Z     cache/
2026-06-01T08:38:02.6905940Z     data/raw/
2026-06-01T08:38:02.6906144Z     data/live/
2026-06-01T08:38:02.6906360Z     data/private/
2026-06-01T08:38:02.6906591Z     data/vendor/
2026-06-01T08:38:02.6906802Z     evidence/
2026-06-01T08:38:02.6907005Z     lockbox/
```

```text
2026-06-01T08:38:02.6915512Z     .DS_Store
2026-06-01T08:38:02.6915715Z     .idea/
2026-06-01T08:38:02.6915909Z     .vscode/
2026-06-01T08:38:02.6916184Z 2 failed, 1390 passed, 1 skipped, 4 warnings in 11.53s
2026-06-01T08:38:03.0015934Z ##[error]Process completed with exit code 1.
2026-06-01T08:38:03.0132160Z Post job cleanup.
2026-06-01T08:38:03.1115215Z [command]/usr/bin/git version
2026-06-01T08:38:03.1154035Z git version 2.54.0
2026-06-01T08:38:03.1199430Z Temporarily overriding HOME='/home/runner/work/_temp/e813c988-06a1-4efc-b90d-bcfcbd8b36ca' before making global git config changes
2026-06-01T08:38:03.1200637Z Adding repository directory to the temporary git global config as a safe directory
2026-06-01T08:38:03.1215063Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-06-01T08:38:03.1251660Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-06-01T08:38:03.1284970Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-06-01T08:38:03.1518540Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-06-01T08:38:03.1543813Z http.https://github.com/.extraheader
2026-06-01T08:38:03.1557107Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

## CI

- Run ID: `26744237405`
- Branch: `main`
- Commit: `9988fccb5b17`
- Title: Implement RGP6 strict critical notification handling
- Created: 2026-06-01T08:37:31Z
- Updated: 2026-06-01T08:38:23Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26744237405

### Failed job: Pytest

- Job ID: `78815553507`
- Started: 2026-06-01T08:37:34Z
- Completed: 2026-06-01T08:38:22Z
- Failed steps: 52. Full regression suite residual tests

#### Error context

```text
2026-06-01T08:38:19.6059649Z ........................................................................ [ 82%]
2026-06-01T08:38:19.7293789Z ........................................................................ [ 90%]
2026-06-01T08:38:19.8123627Z ........................................................................ [ 98%]
2026-06-01T08:38:19.8606272Z ...................                                                      [100%]
2026-06-01T08:38:19.8606946Z =================================== FAILURES ===================================
2026-06-01T08:38:19.8607991Z _______ test_critical_stop_alert_message_is_research_only_and_order_safe _______
2026-06-01T08:38:19.8608359Z 
2026-06-01T08:38:19.8608923Z     def test_critical_stop_alert_message_is_research_only_and_order_safe() -> None:
2026-06-01T08:38:19.8609349Z         message = build_critical_runtime_alert_message(
2026-06-01T08:38:19.8609647Z             CriticalRuntimeAlert(
2026-06-01T08:38:19.8609910Z                 alert_type="STOP",
2026-06-01T08:38:19.8610171Z                 signal_id="sig-001",
2026-06-01T08:38:19.8610420Z                 symbol="AAPL",
2026-06-01T08:38:19.8610685Z                 reason="stop lifecycle threshold reached",
2026-06-01T08:38:19.8610960Z             )
2026-06-01T08:38:19.8611137Z         )
```

```text
2026-06-01T08:38:19.8611137Z         )
2026-06-01T08:38:19.8611327Z         rendered = message.render()
2026-06-01T08:38:19.8611558Z     
2026-06-01T08:38:19.8611968Z >       assert "RGP5 Critical STOP Runtime Alert" in rendered
2026-06-01T08:38:19.8613228Z E       AssertionError: assert 'RGP5 Critical STOP Runtime Alert' in '*RGP5/RGP6 Critical STOP Runtime Alert*\nAlert type: STOP\nSignal ID: sig-001\nSymbol: AAPL\nLifecycle status: critic...elivery only\nReal-money authorization: not granted\nResearch / Paper Observation Only. No live trading authorization.'
2026-06-01T08:38:19.8614276Z 
2026-06-01T08:38:19.8614564Z tests/test_critical_runtime_alert.py:25: AssertionError
2026-06-01T08:38:19.8616894Z =============================== warnings summary ===============================
2026-06-01T08:38:19.8618245Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbol_writes_csv_and_metadata
2026-06-01T08:38:19.8619211Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbol_merges_without_duplicates
2026-06-01T08:38:19.8620237Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbols_batch_counts_results
2026-06-01T08:38:19.8621255Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbols_batch_counts_results
2026-06-01T08:38:19.8623382Z   /home/runner/work/institutional-trading-engine/institutional-trading-engine/src/historical/polygon_ingestion.py:125: FutureWarning: The behavior of DataFrame concatenation with empty or all-NA entries is deprecated. In a future version, this will no longer exclude empty or all-NA columns when determining the result dtypes. To retain the old behavior, exclude the relevant entries before the concat operation.
2026-06-01T08:38:19.8626308Z     combined = pd.concat([existing, df], ignore_index=True)
2026-06-01T08:38:19.8626842Z 
2026-06-01T08:38:19.8627529Z -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
```

```text
2026-06-01T08:38:19.8611558Z     
2026-06-01T08:38:19.8611968Z >       assert "RGP5 Critical STOP Runtime Alert" in rendered
2026-06-01T08:38:19.8613228Z E       AssertionError: assert 'RGP5 Critical STOP Runtime Alert' in '*RGP5/RGP6 Critical STOP Runtime Alert*\nAlert type: STOP\nSignal ID: sig-001\nSymbol: AAPL\nLifecycle status: critic...elivery only\nReal-money authorization: not granted\nResearch / Paper Observation Only. No live trading authorization.'
2026-06-01T08:38:19.8614276Z 
2026-06-01T08:38:19.8614564Z tests/test_critical_runtime_alert.py:25: AssertionError
2026-06-01T08:38:19.8616894Z =============================== warnings summary ===============================
2026-06-01T08:38:19.8618245Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbol_writes_csv_and_metadata
2026-06-01T08:38:19.8619211Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbol_merges_without_duplicates
2026-06-01T08:38:19.8620237Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbols_batch_counts_results
2026-06-01T08:38:19.8621255Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbols_batch_counts_results
2026-06-01T08:38:19.8623382Z   /home/runner/work/institutional-trading-engine/institutional-trading-engine/src/historical/polygon_ingestion.py:125: FutureWarning: The behavior of DataFrame concatenation with empty or all-NA entries is deprecated. In a future version, this will no longer exclude empty or all-NA columns when determining the result dtypes. To retain the old behavior, exclude the relevant entries before the concat operation.
2026-06-01T08:38:19.8626308Z     combined = pd.concat([existing, df], ignore_index=True)
2026-06-01T08:38:19.8626842Z 
2026-06-01T08:38:19.8627529Z -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2026-06-01T08:38:19.8628155Z =========================== short test summary info ============================
2026-06-01T08:38:19.8629650Z FAILED tests/test_critical_runtime_alert.py::test_critical_stop_alert_message_is_research_only_and_order_safe - AssertionError: assert 'RGP5 Critical STOP Runtime Alert' in '*RGP5/RGP6 Critical STOP Runtime Alert*\nAlert type: STOP\nSignal ID: sig-001\nSymbol: AAPL\nLifecycle status: critic...elivery only\nReal-money authorization: not granted\nResearch / Paper Observation Only. No live trading authorization.'
```

```text
2026-06-01T08:38:19.8626308Z     combined = pd.concat([existing, df], ignore_index=True)
2026-06-01T08:38:19.8626842Z 
2026-06-01T08:38:19.8627529Z -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2026-06-01T08:38:19.8628155Z =========================== short test summary info ============================
2026-06-01T08:38:19.8629650Z FAILED tests/test_critical_runtime_alert.py::test_critical_stop_alert_message_is_research_only_and_order_safe - AssertionError: assert 'RGP5 Critical STOP Runtime Alert' in '*RGP5/RGP6 Critical STOP Runtime Alert*\nAlert type: STOP\nSignal ID: sig-001\nSymbol: AAPL\nLifecycle status: critic...elivery only\nReal-money authorization: not granted\nResearch / Paper Observation Only. No live trading authorization.'
2026-06-01T08:38:19.8631109Z 1 failed, 953 passed, 1 skipped, 1 deselected, 4 warnings in 8.15s
2026-06-01T08:38:20.0919347Z ##[error]Process completed with exit code 1.
2026-06-01T08:38:20.1020840Z Post job cleanup.
2026-06-01T08:38:20.2039154Z [command]/usr/bin/git version
2026-06-01T08:38:20.2071603Z git version 2.54.0
2026-06-01T08:38:20.2111689Z Temporarily overriding HOME='/home/runner/work/_temp/3c9eca17-6e16-4189-9dd5-b4c2cf99df38' before making global git config changes
2026-06-01T08:38:20.2112984Z Adding repository directory to the temporary git global config as a safe directory
2026-06-01T08:38:20.2125107Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-06-01T08:38:20.2156398Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-06-01T08:38:20.2184849Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-06-01T08:38:20.2369291Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
```

```text
2026-06-01T08:38:19.8627529Z -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2026-06-01T08:38:19.8628155Z =========================== short test summary info ============================
2026-06-01T08:38:19.8629650Z FAILED tests/test_critical_runtime_alert.py::test_critical_stop_alert_message_is_research_only_and_order_safe - AssertionError: assert 'RGP5 Critical STOP Runtime Alert' in '*RGP5/RGP6 Critical STOP Runtime Alert*\nAlert type: STOP\nSignal ID: sig-001\nSymbol: AAPL\nLifecycle status: critic...elivery only\nReal-money authorization: not granted\nResearch / Paper Observation Only. No live trading authorization.'
2026-06-01T08:38:19.8631109Z 1 failed, 953 passed, 1 skipped, 1 deselected, 4 warnings in 8.15s
2026-06-01T08:38:20.0919347Z ##[error]Process completed with exit code 1.
2026-06-01T08:38:20.1020840Z Post job cleanup.
2026-06-01T08:38:20.2039154Z [command]/usr/bin/git version
2026-06-01T08:38:20.2071603Z git version 2.54.0
2026-06-01T08:38:20.2111689Z Temporarily overriding HOME='/home/runner/work/_temp/3c9eca17-6e16-4189-9dd5-b4c2cf99df38' before making global git config changes
2026-06-01T08:38:20.2112984Z Adding repository directory to the temporary git global config as a safe directory
2026-06-01T08:38:20.2125107Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-06-01T08:38:20.2156398Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-06-01T08:38:20.2184849Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-06-01T08:38:20.2369291Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-06-01T08:38:20.2391663Z http.https://github.com/.extraheader
2026-06-01T08:38:20.2402310Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

## Report Quality Validation

- Run ID: `26744237396`
- Branch: `main`
- Commit: `9988fccb5b17`
- Title: Implement RGP6 strict critical notification handling
- Created: 2026-06-01T08:37:31Z
- Updated: 2026-06-01T08:38:18Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26744237396

### Failed job: validate-reports (premarket)

- Job ID: `78815553194`
- Started: 2026-06-01T08:37:34Z
- Completed: 2026-06-01T08:38:17Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-01T08:37:54.3522162Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-01T08:37:54.3522476Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-01T08:37:54.3522823Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-01T08:37:54.3523090Z ##[endgroup]
2026-06-01T08:38:15.0105347Z Traceback (most recent call last):
2026-06-01T08:38:15.0112911Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 247, in <module>
2026-06-01T08:38:15.0114215Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-28/2026-06-01?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-01T08:38:15.0115281Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-28/2026-06-01?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-01T08:38:15.0116377Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-28/2026-06-01?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-01T08:38:15.0117079Z WARNING: scanner metric loading failed: ModuleNotFoundError: No module named 'config'
2026-06-01T08:38:15.0117425Z WARNING: scanner_metrics_missing:MSFT
2026-06-01T08:38:15.0117704Z     raise SystemExit(main())
2026-06-01T08:38:15.0117909Z                      ^^^^^^
2026-06-01T08:38:15.0118404Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 236, in main
2026-06-01T08:38:15.0118978Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-01T08:38:15.0119332Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```

```text
2026-06-01T08:38:15.0112911Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 247, in <module>
2026-06-01T08:38:15.0114215Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-28/2026-06-01?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-01T08:38:15.0115281Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-28/2026-06-01?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-01T08:38:15.0116377Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-28/2026-06-01?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-01T08:38:15.0117079Z WARNING: scanner metric loading failed: ModuleNotFoundError: No module named 'config'
2026-06-01T08:38:15.0117425Z WARNING: scanner_metrics_missing:MSFT
2026-06-01T08:38:15.0117704Z     raise SystemExit(main())
2026-06-01T08:38:15.0117909Z                      ^^^^^^
2026-06-01T08:38:15.0118404Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 236, in main
2026-06-01T08:38:15.0118978Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-01T08:38:15.0119332Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-01T08:38:15.0119915Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 68, in write_report_text_guarded
2026-06-01T08:38:15.0120513Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-01T08:38:15.0121345Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-06-01T08:38:15.0121945Z     raise ReportOutputBoundaryError(
2026-06-01T08:38:15.0122682Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/premarket-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
```

```text
2026-06-01T08:38:15.0124068Z WARNING: scanner_metrics_missing:MU
2026-06-01T08:38:15.0124524Z WARNING: scanner_metrics_missing:QQQ
2026-06-01T08:38:15.0124744Z WARNING: scanner_metrics_missing:GLD
2026-06-01T08:38:15.0124952Z WARNING: scanner_metrics_missing:SLV
2026-06-01T08:38:15.0653907Z ##[error]Process completed with exit code 1.
2026-06-01T08:38:15.0747271Z Post job cleanup.
2026-06-01T08:38:15.1510501Z [command]/usr/bin/git version
2026-06-01T08:38:15.1539620Z git version 2.54.0
2026-06-01T08:38:15.1572185Z Temporarily overriding HOME='/home/runner/work/_temp/b0238623-e41d-4a6d-b3e9-55517e116aa7' before making global git config changes
2026-06-01T08:38:15.1573161Z Adding repository directory to the temporary git global config as a safe directory
2026-06-01T08:38:15.1578074Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-06-01T08:38:15.1606822Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-06-01T08:38:15.1633848Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-06-01T08:38:15.1824947Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-06-01T08:38:15.1842404Z http.https://github.com/.extraheader
2026-06-01T08:38:15.1851731Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

### Failed job: validate-reports (weekly)

- Job ID: `78815553250`
- Started: 2026-06-01T08:37:33Z
- Completed: 2026-06-01T08:37:51Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-01T08:37:48.2888554Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-01T08:37:48.2888854Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-01T08:37:48.2889293Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-01T08:37:48.2889556Z ##[endgroup]
2026-06-01T08:37:49.0705105Z Traceback (most recent call last):
2026-06-01T08:37:49.0712460Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 247, in <module>
2026-06-01T08:37:49.0713326Z     raise SystemExit(main())
2026-06-01T08:37:49.0713636Z                      ^^^^^^
2026-06-01T08:37:49.0714516Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 236, in main
2026-06-01T08:37:49.0715129Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-01T08:37:49.0715501Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-01T08:37:49.0720228Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 68, in write_report_text_guarded
2026-06-01T08:37:49.0720878Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-01T08:37:49.0721565Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-06-01T08:37:49.0722139Z     raise ReportOutputBoundaryError(
2026-06-01T08:37:49.0722868Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
```

```text
2026-06-01T08:37:49.0720878Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-01T08:37:49.0721565Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-06-01T08:37:49.0722139Z     raise ReportOutputBoundaryError(
2026-06-01T08:37:49.0722868Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-06-01T08:37:49.0909807Z ##[error]Process completed with exit code 1.
2026-06-01T08:37:49.1004342Z Post job cleanup.
2026-06-01T08:37:49.1774276Z [command]/usr/bin/git version
2026-06-01T08:37:49.1803450Z git version 2.54.0
2026-06-01T08:37:49.1835254Z Temporarily overriding HOME='/home/runner/work/_temp/0e2abb5e-a5b4-4b1b-9013-86ea84530589' before making global git config changes
2026-06-01T08:37:49.1836181Z Adding repository directory to the temporary git global config as a safe directory
2026-06-01T08:37:49.1846584Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-06-01T08:37:49.1875282Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-06-01T08:37:49.1908923Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-06-01T08:37:49.2097358Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-06-01T08:37:49.2115414Z http.https://github.com/.extraheader
2026-06-01T08:37:49.2125795Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

### Failed job: validate-reports (postmarket)

- Job ID: `78815553310`
- Started: 2026-06-01T08:37:33Z
- Completed: 2026-06-01T08:38:07Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-01T08:37:50.1595560Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-01T08:37:50.1595962Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-01T08:37:50.1596390Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-01T08:37:50.1596733Z ##[endgroup]
2026-06-01T08:38:05.7622449Z Traceback (most recent call last):
2026-06-01T08:38:05.7629442Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 247, in <module>
2026-06-01T08:38:05.7631091Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-28/2026-06-01?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-01T08:38:05.7632457Z     raise SystemExit(main())
2026-06-01T08:38:05.7633498Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-28/2026-06-01?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-01T08:38:05.7634490Z                      ^^^^^^
2026-06-01T08:38:05.7635448Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-28/2026-06-01?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-01T08:38:05.7636906Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 236, in main
2026-06-01T08:38:05.7637679Z WARNING: scanner metric loading failed: ModuleNotFoundError: No module named 'config'
2026-06-01T08:38:05.7638526Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-01T08:38:05.7638966Z WARNING: scanner_metrics_missing:MSFT
2026-06-01T08:38:05.7639484Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```

```text
2026-06-01T08:38:05.7633498Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-28/2026-06-01?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-01T08:38:05.7634490Z                      ^^^^^^
2026-06-01T08:38:05.7635448Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-28/2026-06-01?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-01T08:38:05.7636906Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 236, in main
2026-06-01T08:38:05.7637679Z WARNING: scanner metric loading failed: ModuleNotFoundError: No module named 'config'
2026-06-01T08:38:05.7638526Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-01T08:38:05.7638966Z WARNING: scanner_metrics_missing:MSFT
2026-06-01T08:38:05.7639484Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-01T08:38:05.7639914Z WARNING: scanner_metrics_missing:NVDA
2026-06-01T08:38:05.7640930Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 68, in write_report_text_guarded
2026-06-01T08:38:05.7641738Z WARNING: scanner_metrics_missing:META
2026-06-01T08:38:05.7642360Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-01T08:38:05.7642813Z WARNING: scanner_metrics_missing:AAPL
2026-06-01T08:38:05.7643868Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-06-01T08:38:05.7644610Z WARNING: scanner_metrics_missing:MU
2026-06-01T08:38:05.7645119Z     raise ReportOutputBoundaryError(
```

```text
2026-06-01T08:38:05.7645501Z WARNING: scanner_metrics_missing:QQQ
2026-06-01T08:38:05.7646633Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/postmarket-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-06-01T08:38:05.7647820Z WARNING: scanner_metrics_missing:GLD
2026-06-01T08:38:05.7648177Z WARNING: scanner_metrics_missing:SLV
2026-06-01T08:38:05.8244209Z ##[error]Process completed with exit code 1.
2026-06-01T08:38:05.8367713Z Post job cleanup.
2026-06-01T08:38:05.9344495Z [command]/usr/bin/git version
2026-06-01T08:38:05.9379855Z git version 2.54.0
2026-06-01T08:38:05.9421953Z Temporarily overriding HOME='/home/runner/work/_temp/65d5bd5c-41a5-4778-bc4f-5ec0bde2f0dc' before making global git config changes
2026-06-01T08:38:05.9423092Z Adding repository directory to the temporary git global config as a safe directory
2026-06-01T08:38:05.9434959Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-06-01T08:38:05.9469803Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-06-01T08:38:05.9503007Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-06-01T08:38:05.9743369Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-06-01T08:38:05.9766884Z http.https://github.com/.extraheader
2026-06-01T08:38:05.9779111Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

## Report Quality Validation

- Run ID: `26743075465`
- Branch: `main`
- Commit: `cf2d50e2d39f`
- Title: Document RGP5 critical alert ordering guard
- Created: 2026-06-01T08:11:07Z
- Updated: 2026-06-01T08:11:45Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26743075465

### Failed job: validate-reports (postmarket)

- Job ID: `78811630644`
- Started: 2026-06-01T08:11:10Z
- Completed: 2026-06-01T08:11:44Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-01T08:11:26.2347802Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-01T08:11:26.2348209Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-01T08:11:26.2348635Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-01T08:11:26.2348986Z ##[endgroup]
2026-06-01T08:11:42.7376577Z Traceback (most recent call last):
2026-06-01T08:11:42.7378558Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-28/2026-06-01?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-01T08:11:42.7388071Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 247, in <module>
2026-06-01T08:11:42.7388796Z     raise SystemExit(main())
2026-06-01T08:11:42.7389069Z                      ^^^^^^
2026-06-01T08:11:42.7389711Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 236, in main
2026-06-01T08:11:42.7390480Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-01T08:11:42.7390938Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-01T08:11:42.7391675Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 68, in write_report_text_guarded
2026-06-01T08:11:42.7392442Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-01T08:11:42.7393268Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-06-01T08:11:42.7393993Z     raise ReportOutputBoundaryError(
```

```text
2026-06-01T08:11:42.7393993Z     raise ReportOutputBoundaryError(
2026-06-01T08:11:42.7395228Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/postmarket-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-06-01T08:11:42.7396894Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-28/2026-06-01?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-01T08:11:42.7398256Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-28/2026-06-01?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-01T08:11:42.7399182Z WARNING: scanner metric loading failed: ModuleNotFoundError: No module named 'config'
2026-06-01T08:11:42.7399629Z WARNING: scanner_metrics_missing:MSFT
2026-06-01T08:11:42.7399914Z WARNING: scanner_metrics_missing:NVDA
2026-06-01T08:11:42.7400188Z WARNING: scanner_metrics_missing:META
2026-06-01T08:11:42.7400463Z WARNING: scanner_metrics_missing:AAPL
2026-06-01T08:11:42.7400750Z WARNING: scanner_metrics_missing:MU
2026-06-01T08:11:42.7401299Z WARNING: scanner_metrics_missing:QQQ
2026-06-01T08:11:42.7401597Z WARNING: scanner_metrics_missing:GLD
2026-06-01T08:11:42.7401878Z WARNING: scanner_metrics_missing:SLV
2026-06-01T08:11:42.8015478Z ##[error]Process completed with exit code 1.
2026-06-01T08:11:42.8138958Z Post job cleanup.
2026-06-01T08:11:42.9093622Z [command]/usr/bin/git version
```

```text
2026-06-01T08:11:42.7400750Z WARNING: scanner_metrics_missing:MU
2026-06-01T08:11:42.7401299Z WARNING: scanner_metrics_missing:QQQ
2026-06-01T08:11:42.7401597Z WARNING: scanner_metrics_missing:GLD
2026-06-01T08:11:42.7401878Z WARNING: scanner_metrics_missing:SLV
2026-06-01T08:11:42.8015478Z ##[error]Process completed with exit code 1.
2026-06-01T08:11:42.8138958Z Post job cleanup.
2026-06-01T08:11:42.9093622Z [command]/usr/bin/git version
2026-06-01T08:11:42.9130481Z git version 2.54.0
2026-06-01T08:11:42.9170857Z Temporarily overriding HOME='/home/runner/work/_temp/15a61f1d-9c38-4e4c-abee-ddfc09ee71e9' before making global git config changes
2026-06-01T08:11:42.9171956Z Adding repository directory to the temporary git global config as a safe directory
2026-06-01T08:11:42.9184441Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-06-01T08:11:42.9219785Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-06-01T08:11:42.9252358Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-06-01T08:11:42.9508761Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-06-01T08:11:42.9529536Z http.https://github.com/.extraheader
2026-06-01T08:11:42.9542693Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

### Failed job: validate-reports (premarket)

- Job ID: `78811630664`
- Started: 2026-06-01T08:11:10Z
- Completed: 2026-06-01T08:11:40Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-01T08:11:23.7356957Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-01T08:11:23.7357323Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-01T08:11:23.7357748Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-01T08:11:23.7358063Z ##[endgroup]
2026-06-01T08:11:38.8951051Z Traceback (most recent call last):
2026-06-01T08:11:38.8952649Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-28/2026-06-01?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-01T08:11:38.8959918Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 247, in <module>
2026-06-01T08:11:38.8960594Z     raise SystemExit(main())
2026-06-01T08:11:38.8960905Z                      ^^^^^^
2026-06-01T08:11:38.8961501Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 236, in main
2026-06-01T08:11:38.8962231Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-01T08:11:38.8962672Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-01T08:11:38.8963390Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 68, in write_report_text_guarded
2026-06-01T08:11:38.8964130Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-01T08:11:38.8964911Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-06-01T08:11:38.8965614Z     raise ReportOutputBoundaryError(
```

```text
2026-06-01T08:11:38.8965614Z     raise ReportOutputBoundaryError(
2026-06-01T08:11:38.8966514Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/premarket-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-06-01T08:11:38.8968169Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-28/2026-06-01?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-01T08:11:38.8969672Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-28/2026-06-01?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-01T08:11:38.8970565Z WARNING: scanner metric loading failed: ModuleNotFoundError: No module named 'config'
2026-06-01T08:11:38.8971000Z WARNING: scanner_metrics_missing:MSFT
2026-06-01T08:11:38.8971287Z WARNING: scanner_metrics_missing:NVDA
2026-06-01T08:11:38.8971563Z WARNING: scanner_metrics_missing:META
2026-06-01T08:11:38.8971836Z WARNING: scanner_metrics_missing:AAPL
2026-06-01T08:11:38.8972116Z WARNING: scanner_metrics_missing:MU
2026-06-01T08:11:38.8972591Z WARNING: scanner_metrics_missing:QQQ
2026-06-01T08:11:38.8972869Z WARNING: scanner_metrics_missing:GLD
2026-06-01T08:11:38.8973125Z WARNING: scanner_metrics_missing:SLV
2026-06-01T08:11:38.9583739Z ##[error]Process completed with exit code 1.
2026-06-01T08:11:38.9701126Z Post job cleanup.
2026-06-01T08:11:39.0656528Z [command]/usr/bin/git version
```

```text
2026-06-01T08:11:38.8972116Z WARNING: scanner_metrics_missing:MU
2026-06-01T08:11:38.8972591Z WARNING: scanner_metrics_missing:QQQ
2026-06-01T08:11:38.8972869Z WARNING: scanner_metrics_missing:GLD
2026-06-01T08:11:38.8973125Z WARNING: scanner_metrics_missing:SLV
2026-06-01T08:11:38.9583739Z ##[error]Process completed with exit code 1.
2026-06-01T08:11:38.9701126Z Post job cleanup.
2026-06-01T08:11:39.0656528Z [command]/usr/bin/git version
2026-06-01T08:11:39.0689628Z git version 2.54.0
2026-06-01T08:11:39.0727567Z Temporarily overriding HOME='/home/runner/work/_temp/d41f8fd1-3b13-4b80-9c39-57db3599f389' before making global git config changes
2026-06-01T08:11:39.0728857Z Adding repository directory to the temporary git global config as a safe directory
2026-06-01T08:11:39.0733468Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-06-01T08:11:39.0766101Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-06-01T08:11:39.0795421Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-06-01T08:11:39.0983549Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-06-01T08:11:39.1007648Z http.https://github.com/.extraheader
2026-06-01T08:11:39.1023132Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

### Failed job: validate-reports (weekly)

- Job ID: `78811630716`
- Started: 2026-06-01T08:11:10Z
- Completed: 2026-06-01T08:11:30Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-01T08:11:26.8891791Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-01T08:11:26.8892183Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-01T08:11:26.8892607Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-01T08:11:26.8892931Z ##[endgroup]
2026-06-01T08:11:27.2087772Z Traceback (most recent call last):
2026-06-01T08:11:27.2096058Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 247, in <module>
2026-06-01T08:11:27.2097184Z     raise SystemExit(main())
2026-06-01T08:11:27.2097572Z                      ^^^^^^
2026-06-01T08:11:27.2098532Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 236, in main
2026-06-01T08:11:27.2100048Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-01T08:11:27.2110127Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-01T08:11:27.2111514Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 68, in write_report_text_guarded
2026-06-01T08:11:27.2112924Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-01T08:11:27.2114524Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-06-01T08:11:27.2115887Z     raise ReportOutputBoundaryError(
2026-06-01T08:11:27.2117122Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
```

```text
2026-06-01T08:11:27.2112924Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-01T08:11:27.2114524Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-06-01T08:11:27.2115887Z     raise ReportOutputBoundaryError(
2026-06-01T08:11:27.2117122Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-06-01T08:11:27.2303610Z ##[error]Process completed with exit code 1.
2026-06-01T08:11:27.2431459Z Post job cleanup.
2026-06-01T08:11:27.3396906Z [command]/usr/bin/git version
2026-06-01T08:11:27.3433159Z git version 2.54.0
2026-06-01T08:11:27.3476882Z Temporarily overriding HOME='/home/runner/work/_temp/4b3a6494-8c2a-420c-891b-e6794f4edb2b' before making global git config changes
2026-06-01T08:11:27.3478320Z Adding repository directory to the temporary git global config as a safe directory
2026-06-01T08:11:27.3483284Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-06-01T08:11:27.3525911Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-06-01T08:11:27.3557873Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-06-01T08:11:27.3782327Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-06-01T08:11:27.3806581Z http.https://github.com/.extraheader
2026-06-01T08:11:27.3818835Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```
