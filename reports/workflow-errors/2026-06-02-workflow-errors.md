# GitHub Actions Workflow Error Report

Generated: 2026-06-02 08:47 UTC
Repository: `yalcinkadir/institutional-trading-engine`
Filter since: 2026-06-01 08:47 UTC
Failed runs included: 10

## Decision Engine Tests

- Run ID: `26808823021`
- Branch: `main`
- Commit: `6f1bdfcbf54c`
- Title: Document ER5 ER6 CI green closure
- Created: 2026-06-02T08:45:24Z
- Updated: 2026-06-02T08:46:02Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26808823021

### Failed job: tests

- Job ID: `79033122963`
- Started: 2026-06-02T08:45:27Z
- Completed: 2026-06-02T08:46:01Z
- Failed steps: 5. Run pytest

#### Error context

```text
2026-06-02T08:45:58.7896798Z ........................................................................ [ 89%]
2026-06-02T08:45:59.0010632Z ........................................................................ [ 93%]
2026-06-02T08:45:59.0475614Z ........................................................................ [ 98%]
2026-06-02T08:45:59.1119851Z .....................                                                    [100%]
2026-06-02T08:45:59.1121432Z =================================== FAILURES ===================================
2026-06-02T08:45:59.1122279Z _________ TestDataPersistence.test_decision_log_path_not_in_gitignore __________
2026-06-02T08:45:59.1123024Z 
2026-06-02T08:45:59.1123467Z self = <test_priority_fixes.TestDataPersistence object at 0x7f416af36a90>
2026-06-02T08:45:59.1124437Z 
2026-06-02T08:45:59.1124735Z     def test_decision_log_path_not_in_gitignore(self):
2026-06-02T08:45:59.1125427Z         gitignore = Path(".gitignore")
2026-06-02T08:45:59.1126020Z         if not gitignore.exists():
2026-06-02T08:45:59.1126537Z             return
2026-06-02T08:45:59.1126990Z         content = gitignore.read_text()
2026-06-02T08:45:59.1127590Z         # data/ should NOT be in gitignore
2026-06-02T08:45:59.1128007Z >       assert "data/" not in content, (
```

```text
2026-06-02T08:45:59.1127590Z         # data/ should NOT be in gitignore
2026-06-02T08:45:59.1128007Z >       assert "data/" not in content, (
2026-06-02T08:45:59.1128941Z             "data/ is in .gitignore â decision log will be lost on every run"
2026-06-02T08:45:59.1129402Z         )
2026-06-02T08:45:59.1129910Z E       AssertionError: data/ is in .gitignore â decision log will be lost on every run
2026-06-02T08:45:59.1130495Z E       assert 'data/' not in '# Python\n_...\n.vscode/\n'
2026-06-02T08:45:59.1130860Z E         
2026-06-02T08:45:59.1131464Z E         'data/' is contained here:
2026-06-02T08:45:59.1131782Z E           e/
2026-06-02T08:45:59.1131971Z E           cache/
2026-06-02T08:45:59.1132163Z E           data/raw/
2026-06-02T08:45:59.1132366Z E           data/live/
2026-06-02T08:45:59.1132574Z E           data/private/
2026-06-02T08:45:59.1132791Z E           data/vendor/
2026-06-02T08:45:59.1133003Z E           evidence/
2026-06-02T08:45:59.1133196Z E           lockbox/
```

```text
2026-06-02T08:45:59.1140894Z E           .DS_Store
2026-06-02T08:45:59.1141457Z E           .idea/
2026-06-02T08:45:59.1141658Z E           .vscode/
2026-06-02T08:45:59.1141785Z 
2026-06-02T08:45:59.1141910Z tests/test_priority_fixes.py:372: AssertionError
2026-06-02T08:45:59.1142257Z =============================== warnings summary ===============================
2026-06-02T08:45:59.1142892Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbol_writes_csv_and_metadata
2026-06-02T08:45:59.1143622Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbol_merges_without_duplicates
2026-06-02T08:45:59.1144264Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbols_batch_counts_results
2026-06-02T08:45:59.1144890Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbols_batch_counts_results
2026-06-02T08:45:59.1146784Z   /home/runner/work/institutional-trading-engine/institutional-trading-engine/src/historical/polygon_ingestion.py:125: FutureWarning: The behavior of DataFrame concatenation with empty or all-NA entries is deprecated. In a future version, this will no longer exclude empty or all-NA columns when determining the result dtypes. To retain the old behavior, exclude the relevant entries before the concat operation.
2026-06-02T08:45:59.1148389Z     combined = pd.concat([existing, df], ignore_index=True)
2026-06-02T08:45:59.1148767Z 
2026-06-02T08:45:59.1148995Z -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2026-06-02T08:45:59.1149487Z =========================== short test summary info ============================
2026-06-02T08:45:59.1150463Z FAILED tests/test_priority_fixes.py::TestDataPersistence::test_decision_log_path_not_in_gitignore - AssertionError: data/ is in .gitignore â decision log will be lost on every run
```

```text
2026-06-02T08:45:59.1148389Z     combined = pd.concat([existing, df], ignore_index=True)
2026-06-02T08:45:59.1148767Z 
2026-06-02T08:45:59.1148995Z -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2026-06-02T08:45:59.1149487Z =========================== short test summary info ============================
2026-06-02T08:45:59.1150463Z FAILED tests/test_priority_fixes.py::TestDataPersistence::test_decision_log_path_not_in_gitignore - AssertionError: data/ is in .gitignore â decision log will be lost on every run
2026-06-02T08:45:59.1151521Z assert 'data/' not in '# Python\n_...\n.vscode/\n'
2026-06-02T08:45:59.1151809Z   
2026-06-02T08:45:59.1151993Z   'data/' is contained here:
2026-06-02T08:45:59.1152215Z     e/
2026-06-02T08:45:59.1152393Z     cache/
2026-06-02T08:45:59.1152571Z     data/raw/
2026-06-02T08:45:59.1152762Z     data/live/
2026-06-02T08:45:59.1152951Z     data/private/
2026-06-02T08:45:59.1153146Z     data/vendor/
2026-06-02T08:45:59.1153335Z     evidence/
2026-06-02T08:45:59.1153519Z     lockbox/
```

```text
2026-06-02T08:45:59.1160400Z     .DS_Store
2026-06-02T08:45:59.1160578Z     .idea/
2026-06-02T08:45:59.1160748Z     .vscode/
2026-06-02T08:45:59.1161220Z 1 failed, 1531 passed, 1 skipped, 4 warnings in 11.71s
2026-06-02T08:45:59.3334574Z ##[error]Process completed with exit code 1.
2026-06-02T08:45:59.3475421Z Post job cleanup.
2026-06-02T08:45:59.4453811Z [command]/usr/bin/git version
2026-06-02T08:45:59.4490008Z git version 2.54.0
2026-06-02T08:45:59.4532359Z Temporarily overriding HOME='/home/runner/work/_temp/953c849e-d858-4c4b-b27d-9504576d9757' before making global git config changes
2026-06-02T08:45:59.4533300Z Adding repository directory to the temporary git global config as a safe directory
2026-06-02T08:45:59.4547560Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-06-02T08:45:59.4581296Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-06-02T08:45:59.4613638Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-06-02T08:45:59.4838065Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-06-02T08:45:59.4860397Z http.https://github.com/.extraheader
2026-06-02T08:45:59.4872487Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

## Report Quality Validation

- Run ID: `26808822904`
- Branch: `main`
- Commit: `6f1bdfcbf54c`
- Title: Document ER5 ER6 CI green closure
- Created: 2026-06-02T08:45:24Z
- Updated: 2026-06-02T08:46:11Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26808822904

### Failed job: validate-reports (postmarket)

- Job ID: `79033122617`
- Started: 2026-06-02T08:45:27Z
- Completed: 2026-06-02T08:46:10Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-02T08:45:45.9861246Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-02T08:45:45.9861552Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-02T08:45:45.9861900Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-02T08:45:45.9862170Z ##[endgroup]
2026-06-02T08:46:06.9839575Z Traceback (most recent call last):
2026-06-02T08:46:06.9841191Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-29/2026-06-02?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-02T08:46:06.9842901Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-29/2026-06-02?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-02T08:46:06.9844512Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-29/2026-06-02?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-02T08:46:06.9845604Z WARNING: scanner metric loading failed: ModuleNotFoundError: No module named 'config'
2026-06-02T08:46:06.9846103Z WARNING: scanner_metrics_missing:MSFT
2026-06-02T08:46:06.9846419Z WARNING: scanner_metrics_missing:NVDA
2026-06-02T08:46:06.9846722Z WARNING: scanner_metrics_missing:META
2026-06-02T08:46:06.9847024Z WARNING: scanner_metrics_missing:AAPL
2026-06-02T08:46:06.9847327Z WARNING: scanner_metrics_missing:MU
2026-06-02T08:46:06.9847620Z WARNING: scanner_metrics_missing:QQQ
2026-06-02T08:46:06.9847916Z WARNING: scanner_metrics_missing:GLD
```

```text
2026-06-02T08:46:06.9839575Z Traceback (most recent call last):
2026-06-02T08:46:06.9841191Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-29/2026-06-02?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-02T08:46:06.9842901Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-29/2026-06-02?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-02T08:46:06.9844512Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-29/2026-06-02?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-02T08:46:06.9845604Z WARNING: scanner metric loading failed: ModuleNotFoundError: No module named 'config'
2026-06-02T08:46:06.9846103Z WARNING: scanner_metrics_missing:MSFT
2026-06-02T08:46:06.9846419Z WARNING: scanner_metrics_missing:NVDA
2026-06-02T08:46:06.9846722Z WARNING: scanner_metrics_missing:META
2026-06-02T08:46:06.9847024Z WARNING: scanner_metrics_missing:AAPL
2026-06-02T08:46:06.9847327Z WARNING: scanner_metrics_missing:MU
2026-06-02T08:46:06.9847620Z WARNING: scanner_metrics_missing:QQQ
2026-06-02T08:46:06.9847916Z WARNING: scanner_metrics_missing:GLD
2026-06-02T08:46:06.9848225Z WARNING: scanner_metrics_missing:SLV
2026-06-02T08:46:06.9858004Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 247, in <module>
2026-06-02T08:46:06.9859104Z     raise SystemExit(main())
2026-06-02T08:46:06.9859384Z                      ^^^^^^
```

```text
2026-06-02T08:46:06.9863274Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-02T08:46:06.9864233Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-06-02T08:46:06.9865112Z     raise ReportOutputBoundaryError(
2026-06-02T08:46:06.9866204Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/postmarket-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-06-02T08:46:07.0456006Z ##[error]Process completed with exit code 1.
2026-06-02T08:46:07.0522896Z ##[group]Run actions/upload-artifact@v4
2026-06-02T08:46:07.0523128Z with:
2026-06-02T08:46:07.0523310Z   name: validated-postmarket-report
2026-06-02T08:46:07.0523538Z   path: reports/postmarket-report.md
2026-06-02T08:46:07.0523749Z   retention-days: 14
2026-06-02T08:46:07.0523932Z   if-no-files-found: warn
2026-06-02T08:46:07.0524124Z   compression-level: 6
2026-06-02T08:46:07.0524312Z   overwrite: false
2026-06-02T08:46:07.0524490Z   include-hidden-files: false
2026-06-02T08:46:07.0524690Z env:
2026-06-02T08:46:07.0524951Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (weekly)

- Job ID: `79033122628`
- Started: 2026-06-02T08:45:27Z
- Completed: 2026-06-02T08:45:50Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-02T08:45:47.3205100Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-02T08:45:47.3205569Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-02T08:45:47.3206078Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-02T08:45:47.3206479Z ##[endgroup]
2026-06-02T08:45:47.6364050Z Traceback (most recent call last):
2026-06-02T08:45:47.6374759Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 247, in <module>
2026-06-02T08:45:47.6376044Z     raise SystemExit(main())
2026-06-02T08:45:47.6376508Z                      ^^^^^^
2026-06-02T08:45:47.6377651Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 236, in main
2026-06-02T08:45:47.6379054Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-02T08:45:47.6379900Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-02T08:45:47.6381345Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 68, in write_report_text_guarded
2026-06-02T08:45:47.6383306Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-02T08:45:47.6384518Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-06-02T08:45:47.6385530Z     raise ReportOutputBoundaryError(
2026-06-02T08:45:47.6386865Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
```

```text
2026-06-02T08:45:47.6383306Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-02T08:45:47.6384518Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-06-02T08:45:47.6385530Z     raise ReportOutputBoundaryError(
2026-06-02T08:45:47.6386865Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-06-02T08:45:47.6612366Z ##[error]Process completed with exit code 1.
2026-06-02T08:45:47.6702617Z ##[group]Run actions/upload-artifact@v4
2026-06-02T08:45:47.6702965Z with:
2026-06-02T08:45:47.6703194Z   name: validated-weekly-report
2026-06-02T08:45:47.6703479Z   path: reports/weekly-report.md
2026-06-02T08:45:47.6703757Z   retention-days: 14
2026-06-02T08:45:47.6703994Z   if-no-files-found: warn
2026-06-02T08:45:47.6704292Z   compression-level: 6
2026-06-02T08:45:47.6704526Z   overwrite: false
2026-06-02T08:45:47.6704765Z   include-hidden-files: false
2026-06-02T08:45:47.6705031Z env:
2026-06-02T08:45:47.6705392Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (premarket)

- Job ID: `79033122702`
- Started: 2026-06-02T08:45:27Z
- Completed: 2026-06-02T08:46:04Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-02T08:45:43.7989914Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-02T08:45:43.7990284Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-02T08:45:43.7990702Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-02T08:45:43.7991031Z ##[endgroup]
2026-06-02T08:46:01.3041611Z Traceback (most recent call last):
2026-06-02T08:46:01.3043695Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-29/2026-06-02?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-02T08:46:01.3045409Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-29/2026-06-02?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-02T08:46:01.3046666Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-29/2026-06-02?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-02T08:46:01.3047573Z WARNING: scanner metric loading failed: ModuleNotFoundError: No module named 'config'
2026-06-02T08:46:01.3047987Z WARNING: scanner_metrics_missing:MSFT
2026-06-02T08:46:01.3048434Z WARNING: scanner_metrics_missing:NVDA
2026-06-02T08:46:01.3048709Z WARNING: scanner_metrics_missing:META
2026-06-02T08:46:01.3048977Z WARNING: scanner_metrics_missing:AAPL
2026-06-02T08:46:01.3049266Z WARNING: scanner_metrics_missing:MU
2026-06-02T08:46:01.3049542Z WARNING: scanner_metrics_missing:QQQ
2026-06-02T08:46:01.3049807Z WARNING: scanner_metrics_missing:GLD
```

```text
2026-06-02T08:46:01.3041611Z Traceback (most recent call last):
2026-06-02T08:46:01.3043695Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-29/2026-06-02?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-02T08:46:01.3045409Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-29/2026-06-02?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-02T08:46:01.3046666Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-29/2026-06-02?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-02T08:46:01.3047573Z WARNING: scanner metric loading failed: ModuleNotFoundError: No module named 'config'
2026-06-02T08:46:01.3047987Z WARNING: scanner_metrics_missing:MSFT
2026-06-02T08:46:01.3048434Z WARNING: scanner_metrics_missing:NVDA
2026-06-02T08:46:01.3048709Z WARNING: scanner_metrics_missing:META
2026-06-02T08:46:01.3048977Z WARNING: scanner_metrics_missing:AAPL
2026-06-02T08:46:01.3049266Z WARNING: scanner_metrics_missing:MU
2026-06-02T08:46:01.3049542Z WARNING: scanner_metrics_missing:QQQ
2026-06-02T08:46:01.3049807Z WARNING: scanner_metrics_missing:GLD
2026-06-02T08:46:01.3050066Z WARNING: scanner_metrics_missing:SLV
2026-06-02T08:46:01.3056357Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 247, in <module>
2026-06-02T08:46:01.3057031Z     raise SystemExit(main())
2026-06-02T08:46:01.3057273Z                      ^^^^^^
```

```text
2026-06-02T08:46:01.3060419Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-02T08:46:01.3061190Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-06-02T08:46:01.3061878Z     raise ReportOutputBoundaryError(
2026-06-02T08:46:01.3063023Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/premarket-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-06-02T08:46:01.3635847Z ##[error]Process completed with exit code 1.
2026-06-02T08:46:01.3714274Z ##[group]Run actions/upload-artifact@v4
2026-06-02T08:46:01.3714557Z with:
2026-06-02T08:46:01.3714771Z   name: validated-premarket-report
2026-06-02T08:46:01.3715051Z   path: reports/premarket-report.md
2026-06-02T08:46:01.3715318Z   retention-days: 14
2026-06-02T08:46:01.3715546Z   if-no-files-found: warn
2026-06-02T08:46:01.3715781Z   compression-level: 6
2026-06-02T08:46:01.3715995Z   overwrite: false
2026-06-02T08:46:01.3716208Z   include-hidden-files: false
2026-06-02T08:46:01.3716448Z env:
2026-06-02T08:46:01.3716746Z   POLYGON_API_KEY: ***
```

## Decision Engine Tests

- Run ID: `26808620520`
- Branch: `main`
- Commit: `8660b752e736`
- Title: Treat flat expectancy as neutral
- Created: 2026-06-02T08:41:24Z
- Updated: 2026-06-02T08:42:00Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26808620520

### Failed job: tests

- Job ID: `79032453419`
- Started: 2026-06-02T08:41:27Z
- Completed: 2026-06-02T08:42:00Z
- Failed steps: 5. Run pytest

#### Error context

```text
2026-06-02T08:41:58.0102251Z ........................................................................ [ 89%]
2026-06-02T08:41:58.2249371Z ........................................................................ [ 93%]
2026-06-02T08:41:58.2624475Z ........................................................................ [ 98%]
2026-06-02T08:41:58.3236667Z .....................                                                    [100%]
2026-06-02T08:41:58.3237374Z =================================== FAILURES ===================================
2026-06-02T08:41:58.3238198Z _________ TestDataPersistence.test_decision_log_path_not_in_gitignore __________
2026-06-02T08:41:58.3238609Z 
2026-06-02T08:41:58.3239226Z self = <test_priority_fixes.TestDataPersistence object at 0x7fdde77c3150>
2026-06-02T08:41:58.3239957Z 
2026-06-02T08:41:58.3240112Z     def test_decision_log_path_not_in_gitignore(self):
2026-06-02T08:41:58.3240461Z         gitignore = Path(".gitignore")
2026-06-02T08:41:58.3240762Z         if not gitignore.exists():
2026-06-02T08:41:58.3241024Z             return
2026-06-02T08:41:58.3241268Z         content = gitignore.read_text()
2026-06-02T08:41:58.3241564Z         # data/ should NOT be in gitignore
2026-06-02T08:41:58.3241857Z >       assert "data/" not in content, (
```

```text
2026-06-02T08:41:58.3241564Z         # data/ should NOT be in gitignore
2026-06-02T08:41:58.3241857Z >       assert "data/" not in content, (
2026-06-02T08:41:58.3242936Z             "data/ is in .gitignore â decision log will be lost on every run"
2026-06-02T08:41:58.3243313Z         )
2026-06-02T08:41:58.3243736Z E       AssertionError: data/ is in .gitignore â decision log will be lost on every run
2026-06-02T08:41:58.3244217Z E       assert 'data/' not in '# Python\n_...\n.vscode/\n'
2026-06-02T08:41:58.3244530Z E         
2026-06-02T08:41:58.3244749Z E         'data/' is contained here:
2026-06-02T08:41:58.3245030Z E           e/
2026-06-02T08:41:58.3245237Z E           cache/
2026-06-02T08:41:58.3245456Z E           data/raw/
2026-06-02T08:41:58.3245683Z E           data/live/
2026-06-02T08:41:58.3246142Z E           data/private/
2026-06-02T08:41:58.3246421Z E           data/vendor/
2026-06-02T08:41:58.3246654Z E           evidence/
2026-06-02T08:41:58.3246871Z E           lockbox/
```

```text
2026-06-02T08:41:58.3261774Z E           .DS_Store
2026-06-02T08:41:58.3262195Z E           .idea/
2026-06-02T08:41:58.3262560Z E           .vscode/
2026-06-02T08:41:58.3262867Z 
2026-06-02T08:41:58.3266486Z tests/test_priority_fixes.py:372: AssertionError
2026-06-02T08:41:58.3267333Z =============================== warnings summary ===============================
2026-06-02T08:41:58.3268705Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbol_writes_csv_and_metadata
2026-06-02T08:41:58.3269631Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbol_merges_without_duplicates
2026-06-02T08:41:58.3270297Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbols_batch_counts_results
2026-06-02T08:41:58.3270954Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbols_batch_counts_results
2026-06-02T08:41:58.3272928Z   /home/runner/work/institutional-trading-engine/institutional-trading-engine/src/historical/polygon_ingestion.py:125: FutureWarning: The behavior of DataFrame concatenation with empty or all-NA entries is deprecated. In a future version, this will no longer exclude empty or all-NA columns when determining the result dtypes. To retain the old behavior, exclude the relevant entries before the concat operation.
2026-06-02T08:41:58.3274555Z     combined = pd.concat([existing, df], ignore_index=True)
2026-06-02T08:41:58.3274966Z 
2026-06-02T08:41:58.3275229Z -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2026-06-02T08:41:58.3275718Z =========================== short test summary info ============================
2026-06-02T08:41:58.3276944Z FAILED tests/test_priority_fixes.py::TestDataPersistence::test_decision_log_path_not_in_gitignore - AssertionError: data/ is in .gitignore â decision log will be lost on every run
```

```text
2026-06-02T08:41:58.3274555Z     combined = pd.concat([existing, df], ignore_index=True)
2026-06-02T08:41:58.3274966Z 
2026-06-02T08:41:58.3275229Z -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2026-06-02T08:41:58.3275718Z =========================== short test summary info ============================
2026-06-02T08:41:58.3276944Z FAILED tests/test_priority_fixes.py::TestDataPersistence::test_decision_log_path_not_in_gitignore - AssertionError: data/ is in .gitignore â decision log will be lost on every run
2026-06-02T08:41:58.3277725Z assert 'data/' not in '# Python\n_...\n.vscode/\n'
2026-06-02T08:41:58.3278043Z   
2026-06-02T08:41:58.3278249Z   'data/' is contained here:
2026-06-02T08:41:58.3278494Z     e/
2026-06-02T08:41:58.3278716Z     cache/
2026-06-02T08:41:58.3278913Z     data/raw/
2026-06-02T08:41:58.3279115Z     data/live/
2026-06-02T08:41:58.3279330Z     data/private/
2026-06-02T08:41:58.3279547Z     data/vendor/
2026-06-02T08:41:58.3279757Z     evidence/
2026-06-02T08:41:58.3279958Z     lockbox/
```

```text
2026-06-02T08:41:58.3287723Z     .DS_Store
2026-06-02T08:41:58.3287915Z     .idea/
2026-06-02T08:41:58.3288108Z     .vscode/
2026-06-02T08:41:58.3288376Z 1 failed, 1531 passed, 1 skipped, 4 warnings in 12.19s
2026-06-02T08:41:58.7679811Z ##[error]Process completed with exit code 1.
2026-06-02T08:41:58.7799172Z Post job cleanup.
2026-06-02T08:41:58.8811168Z [command]/usr/bin/git version
2026-06-02T08:41:58.8848614Z git version 2.54.0
2026-06-02T08:41:58.8891699Z Temporarily overriding HOME='/home/runner/work/_temp/f152d818-b321-46db-b450-d404d0421b59' before making global git config changes
2026-06-02T08:41:58.8892996Z Adding repository directory to the temporary git global config as a safe directory
2026-06-02T08:41:58.8898792Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-06-02T08:41:58.8950354Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-06-02T08:41:58.8992175Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-06-02T08:41:58.9265627Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-06-02T08:41:58.9296469Z http.https://github.com/.extraheader
2026-06-02T08:41:58.9310362Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

## Report Quality Validation

- Run ID: `26808620539`
- Branch: `main`
- Commit: `8660b752e736`
- Title: Treat flat expectancy as neutral
- Created: 2026-06-02T08:41:24Z
- Updated: 2026-06-02T08:42:03Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26808620539

### Failed job: validate-reports (premarket)

- Job ID: `79032453685`
- Started: 2026-06-02T08:41:27Z
- Completed: 2026-06-02T08:41:59Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-02T08:41:42.9692278Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-02T08:41:42.9692677Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-02T08:41:42.9693104Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-02T08:41:42.9693449Z ##[endgroup]
2026-06-02T08:41:57.4242414Z Traceback (most recent call last):
2026-06-02T08:41:57.4251687Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 247, in <module>
2026-06-02T08:41:57.4254384Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-29/2026-06-02?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-02T08:41:57.4255664Z     raise SystemExit(main())
2026-06-02T08:41:57.4255987Z                      ^^^^^^
2026-06-02T08:41:57.4256831Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 236, in main
2026-06-02T08:41:57.4257875Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-02T08:41:57.4258492Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-02T08:41:57.4259534Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 68, in write_report_text_guarded
2026-06-02T08:41:57.4260611Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-02T08:41:57.4262133Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-06-02T08:41:57.4263148Z     raise ReportOutputBoundaryError(
```

```text
2026-06-02T08:41:57.4263148Z     raise ReportOutputBoundaryError(
2026-06-02T08:41:57.4264166Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/premarket-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-06-02T08:41:57.4265933Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-29/2026-06-02?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-02T08:41:57.4267388Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-29/2026-06-02?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-02T08:41:57.4268349Z WARNING: scanner metric loading failed: ModuleNotFoundError: No module named 'config'
2026-06-02T08:41:57.4268807Z WARNING: scanner_metrics_missing:MSFT
2026-06-02T08:41:57.4269095Z WARNING: scanner_metrics_missing:NVDA
2026-06-02T08:41:57.4269374Z WARNING: scanner_metrics_missing:META
2026-06-02T08:41:57.4269652Z WARNING: scanner_metrics_missing:AAPL
2026-06-02T08:41:57.4269931Z WARNING: scanner_metrics_missing:MU
2026-06-02T08:41:57.4270563Z WARNING: scanner_metrics_missing:QQQ
2026-06-02T08:41:57.4270849Z WARNING: scanner_metrics_missing:GLD
2026-06-02T08:41:57.4271123Z WARNING: scanner_metrics_missing:SLV
2026-06-02T08:41:57.4959559Z ##[error]Process completed with exit code 1.
2026-06-02T08:41:57.5047194Z ##[group]Run actions/upload-artifact@v4
2026-06-02T08:41:57.5047598Z with:
```

```text
2026-06-02T08:41:57.4269931Z WARNING: scanner_metrics_missing:MU
2026-06-02T08:41:57.4270563Z WARNING: scanner_metrics_missing:QQQ
2026-06-02T08:41:57.4270849Z WARNING: scanner_metrics_missing:GLD
2026-06-02T08:41:57.4271123Z WARNING: scanner_metrics_missing:SLV
2026-06-02T08:41:57.4959559Z ##[error]Process completed with exit code 1.
2026-06-02T08:41:57.5047194Z ##[group]Run actions/upload-artifact@v4
2026-06-02T08:41:57.5047598Z with:
2026-06-02T08:41:57.5047904Z   name: validated-premarket-report
2026-06-02T08:41:57.5048257Z   path: reports/premarket-report.md
2026-06-02T08:41:57.5048595Z   retention-days: 14
2026-06-02T08:41:57.5048894Z   if-no-files-found: warn
2026-06-02T08:41:57.5049207Z   compression-level: 6
2026-06-02T08:41:57.5049513Z   overwrite: false
2026-06-02T08:41:57.5049805Z   include-hidden-files: false
2026-06-02T08:41:57.5050114Z env:
2026-06-02T08:41:57.5050495Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (postmarket)

- Job ID: `79032453704`
- Started: 2026-06-02T08:41:27Z
- Completed: 2026-06-02T08:42:03Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-02T08:41:44.6455856Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-02T08:41:44.6456281Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-02T08:41:44.6456712Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-02T08:41:44.6457044Z ##[endgroup]
2026-06-02T08:42:00.7037068Z Traceback (most recent call last):
2026-06-02T08:42:00.7039089Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-29/2026-06-02?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-02T08:42:00.7048286Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 247, in <module>
2026-06-02T08:42:00.7049049Z     raise SystemExit(main())
2026-06-02T08:42:00.7049321Z                      ^^^^^^
2026-06-02T08:42:00.7050007Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 236, in main
2026-06-02T08:42:00.7050839Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-02T08:42:00.7051344Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-02T08:42:00.7052175Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 68, in write_report_text_guarded
2026-06-02T08:42:00.7053646Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-29/2026-06-02?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-02T08:42:00.7055543Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-29/2026-06-02?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-02T08:42:00.7056521Z WARNING: scanner metric loading failed: ModuleNotFoundError: No module named 'config'
```

```text
2026-06-02T08:42:00.7051344Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-02T08:42:00.7052175Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 68, in write_report_text_guarded
2026-06-02T08:42:00.7053646Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-29/2026-06-02?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-02T08:42:00.7055543Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-29/2026-06-02?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-02T08:42:00.7056521Z WARNING: scanner metric loading failed: ModuleNotFoundError: No module named 'config'
2026-06-02T08:42:00.7056976Z WARNING: scanner_metrics_missing:MSFT
2026-06-02T08:42:00.7057266Z WARNING: scanner_metrics_missing:NVDA
2026-06-02T08:42:00.7057550Z WARNING: scanner_metrics_missing:META
2026-06-02T08:42:00.7057835Z WARNING: scanner_metrics_missing:AAPL
2026-06-02T08:42:00.7058123Z WARNING: scanner_metrics_missing:MU
2026-06-02T08:42:00.7058404Z WARNING: scanner_metrics_missing:QQQ
2026-06-02T08:42:00.7058682Z WARNING: scanner_metrics_missing:GLD
2026-06-02T08:42:00.7058955Z WARNING: scanner_metrics_missing:SLV
2026-06-02T08:42:00.7059335Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-02T08:42:00.7065441Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-06-02T08:42:00.7066796Z     raise ReportOutputBoundaryError(
```

```text
2026-06-02T08:42:00.7059335Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-02T08:42:00.7065441Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-06-02T08:42:00.7066796Z     raise ReportOutputBoundaryError(
2026-06-02T08:42:00.7068393Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/postmarket-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-06-02T08:42:00.7618393Z ##[error]Process completed with exit code 1.
2026-06-02T08:42:00.7704252Z ##[group]Run actions/upload-artifact@v4
2026-06-02T08:42:00.7704572Z with:
2026-06-02T08:42:00.7704873Z   name: validated-postmarket-report
2026-06-02T08:42:00.7705185Z   path: reports/postmarket-report.md
2026-06-02T08:42:00.7705473Z   retention-days: 14
2026-06-02T08:42:00.7705710Z   if-no-files-found: warn
2026-06-02T08:42:00.7705954Z   compression-level: 6
2026-06-02T08:42:00.7706190Z   overwrite: false
2026-06-02T08:42:00.7706420Z   include-hidden-files: false
2026-06-02T08:42:00.7706662Z env:
2026-06-02T08:42:00.7706979Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (weekly)

- Job ID: `79032453800`
- Started: 2026-06-02T08:41:27Z
- Completed: 2026-06-02T08:41:50Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-02T08:41:47.2437897Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-02T08:41:47.2438299Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-02T08:41:47.2438739Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-02T08:41:47.2439086Z ##[endgroup]
2026-06-02T08:41:48.1285804Z Traceback (most recent call last):
2026-06-02T08:41:48.1292944Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 247, in <module>
2026-06-02T08:41:48.1293979Z     raise SystemExit(main())
2026-06-02T08:41:48.1294265Z                      ^^^^^^
2026-06-02T08:41:48.1294930Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 236, in main
2026-06-02T08:41:48.1295717Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-02T08:41:48.1296175Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-02T08:41:48.1296962Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 68, in write_report_text_guarded
2026-06-02T08:41:48.1297794Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-02T08:41:48.1298640Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-06-02T08:41:48.1299392Z     raise ReportOutputBoundaryError(
2026-06-02T08:41:48.1300334Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
```

```text
2026-06-02T08:41:48.1297794Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-02T08:41:48.1298640Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-06-02T08:41:48.1299392Z     raise ReportOutputBoundaryError(
2026-06-02T08:41:48.1300334Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-06-02T08:41:48.1542610Z ##[error]Process completed with exit code 1.
2026-06-02T08:41:48.1627944Z ##[group]Run actions/upload-artifact@v4
2026-06-02T08:41:48.1628277Z with:
2026-06-02T08:41:48.1628510Z   name: validated-weekly-report
2026-06-02T08:41:48.1628807Z   path: reports/weekly-report.md
2026-06-02T08:41:48.1629077Z   retention-days: 14
2026-06-02T08:41:48.1629316Z   if-no-files-found: warn
2026-06-02T08:41:48.1629571Z   compression-level: 6
2026-06-02T08:41:48.1629812Z   overwrite: false
2026-06-02T08:41:48.1630050Z   include-hidden-files: false
2026-06-02T08:41:48.1630300Z env:
2026-06-02T08:41:48.1630702Z   POLYGON_API_KEY: ***
```

## Report Quality Validation

- Run ID: `26807732129`
- Branch: `main`
- Commit: `0dfe9e8f13e9`
- Title: Exclude missing edge evidence results from breakeven metrics
- Created: 2026-06-02T08:23:32Z
- Updated: 2026-06-02T08:24:20Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26807732129

### Failed job: validate-reports (postmarket)

- Job ID: `79029444691`
- Started: 2026-06-02T08:23:35Z
- Completed: 2026-06-02T08:24:19Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-02T08:23:55.0692477Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-02T08:23:55.0692879Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-02T08:23:55.0693310Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-02T08:23:55.0693648Z ##[endgroup]
2026-06-02T08:24:15.5192740Z Traceback (most recent call last):
2026-06-02T08:24:15.5194699Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-29/2026-06-02?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-02T08:24:15.5204241Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 247, in <module>
2026-06-02T08:24:15.5205148Z     raise SystemExit(main())
2026-06-02T08:24:15.5205464Z                      ^^^^^^
2026-06-02T08:24:15.5206273Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 236, in main
2026-06-02T08:24:15.5207293Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-02T08:24:15.5207846Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-02T08:24:15.5208928Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 68, in write_report_text_guarded
2026-06-02T08:24:15.5209725Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-02T08:24:15.5210613Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-06-02T08:24:15.5211367Z     raise ReportOutputBoundaryError(
```

```text
2026-06-02T08:24:15.5211367Z     raise ReportOutputBoundaryError(
2026-06-02T08:24:15.5212326Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/postmarket-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-06-02T08:24:15.5214007Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-29/2026-06-02?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-02T08:24:15.5215414Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-29/2026-06-02?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-02T08:24:15.5216339Z WARNING: scanner metric loading failed: ModuleNotFoundError: No module named 'config'
2026-06-02T08:24:15.5216777Z WARNING: scanner_metrics_missing:MSFT
2026-06-02T08:24:15.5217060Z WARNING: scanner_metrics_missing:NVDA
2026-06-02T08:24:15.5217323Z WARNING: scanner_metrics_missing:META
2026-06-02T08:24:15.5217582Z WARNING: scanner_metrics_missing:AAPL
2026-06-02T08:24:15.5217863Z WARNING: scanner_metrics_missing:MU
2026-06-02T08:24:15.5219060Z WARNING: scanner_metrics_missing:QQQ
2026-06-02T08:24:15.5219522Z WARNING: scanner_metrics_missing:GLD
2026-06-02T08:24:15.5219830Z WARNING: scanner_metrics_missing:SLV
2026-06-02T08:24:15.5769395Z ##[error]Process completed with exit code 1.
2026-06-02T08:24:15.5854727Z ##[group]Run actions/upload-artifact@v4
2026-06-02T08:24:15.5855025Z with:
```

```text
2026-06-02T08:24:15.5217863Z WARNING: scanner_metrics_missing:MU
2026-06-02T08:24:15.5219060Z WARNING: scanner_metrics_missing:QQQ
2026-06-02T08:24:15.5219522Z WARNING: scanner_metrics_missing:GLD
2026-06-02T08:24:15.5219830Z WARNING: scanner_metrics_missing:SLV
2026-06-02T08:24:15.5769395Z ##[error]Process completed with exit code 1.
2026-06-02T08:24:15.5854727Z ##[group]Run actions/upload-artifact@v4
2026-06-02T08:24:15.5855025Z with:
2026-06-02T08:24:15.5855241Z   name: validated-postmarket-report
2026-06-02T08:24:15.5855524Z   path: reports/postmarket-report.md
2026-06-02T08:24:15.5855783Z   retention-days: 14
2026-06-02T08:24:15.5856003Z   if-no-files-found: warn
2026-06-02T08:24:15.5856235Z   compression-level: 6
2026-06-02T08:24:15.5856452Z   overwrite: false
2026-06-02T08:24:15.5856667Z   include-hidden-files: false
2026-06-02T08:24:15.5856907Z env:
2026-06-02T08:24:15.5857245Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (premarket)

- Job ID: `79029444698`
- Started: 2026-06-02T08:23:35Z
- Completed: 2026-06-02T08:24:10Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-02T08:23:52.7338523Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-02T08:23:52.7338928Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-02T08:23:52.7339368Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-02T08:23:52.7339719Z ##[endgroup]
2026-06-02T08:24:07.9205778Z Traceback (most recent call last):
2026-06-02T08:24:07.9207881Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-29/2026-06-02?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-02T08:24:07.9215612Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 247, in <module>
2026-06-02T08:24:07.9216417Z     raise SystemExit(main())
2026-06-02T08:24:07.9216690Z                      ^^^^^^
2026-06-02T08:24:07.9217325Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 236, in main
2026-06-02T08:24:07.9218124Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-02T08:24:07.9218617Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-02T08:24:07.9219394Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 68, in write_report_text_guarded
2026-06-02T08:24:07.9220172Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-02T08:24:07.9221016Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-06-02T08:24:07.9222394Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-29/2026-06-02?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
```

```text
2026-06-02T08:24:07.9220172Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-02T08:24:07.9221016Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-06-02T08:24:07.9222394Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-29/2026-06-02?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-02T08:24:07.9223748Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-29/2026-06-02?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-02T08:24:07.9224649Z WARNING: scanner metric loading failed: ModuleNotFoundError: No module named 'config'
2026-06-02T08:24:07.9225104Z WARNING: scanner_metrics_missing:MSFT
2026-06-02T08:24:07.9225607Z WARNING: scanner_metrics_missing:NVDA
2026-06-02T08:24:07.9225888Z WARNING: scanner_metrics_missing:META
2026-06-02T08:24:07.9226185Z WARNING: scanner_metrics_missing:AAPL
2026-06-02T08:24:07.9226475Z WARNING: scanner_metrics_missing:MU
2026-06-02T08:24:07.9226758Z WARNING: scanner_metrics_missing:QQQ
2026-06-02T08:24:07.9227045Z WARNING: scanner_metrics_missing:GLD
2026-06-02T08:24:07.9227316Z WARNING: scanner_metrics_missing:SLV
2026-06-02T08:24:07.9227636Z     raise ReportOutputBoundaryError(
2026-06-02T08:24:07.9228564Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/premarket-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-06-02T08:24:08.0126024Z ##[error]Process completed with exit code 1.
```

```text
2026-06-02T08:24:07.9227045Z WARNING: scanner_metrics_missing:GLD
2026-06-02T08:24:07.9227316Z WARNING: scanner_metrics_missing:SLV
2026-06-02T08:24:07.9227636Z     raise ReportOutputBoundaryError(
2026-06-02T08:24:07.9228564Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/premarket-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-06-02T08:24:08.0126024Z ##[error]Process completed with exit code 1.
2026-06-02T08:24:08.0213249Z ##[group]Run actions/upload-artifact@v4
2026-06-02T08:24:08.0213568Z with:
2026-06-02T08:24:08.0213806Z   name: validated-premarket-report
2026-06-02T08:24:08.0214109Z   path: reports/premarket-report.md
2026-06-02T08:24:08.0214392Z   retention-days: 14
2026-06-02T08:24:08.0214641Z   if-no-files-found: warn
2026-06-02T08:24:08.0214895Z   compression-level: 6
2026-06-02T08:24:08.0215144Z   overwrite: false
2026-06-02T08:24:08.0215628Z   include-hidden-files: false
2026-06-02T08:24:08.0215886Z env:
2026-06-02T08:24:08.0216251Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (weekly)

- Job ID: `79029444702`
- Started: 2026-06-02T08:23:36Z
- Completed: 2026-06-02T08:23:57Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-02T08:23:54.6029236Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-02T08:23:54.6029638Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-02T08:23:54.6030080Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-02T08:23:54.6030416Z ##[endgroup]
2026-06-02T08:23:54.9202708Z Traceback (most recent call last):
2026-06-02T08:23:54.9211772Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 247, in <module>
2026-06-02T08:23:54.9212907Z     raise SystemExit(main())
2026-06-02T08:23:54.9213275Z                      ^^^^^^
2026-06-02T08:23:54.9214555Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 236, in main
2026-06-02T08:23:54.9215844Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-02T08:23:54.9224676Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-02T08:23:54.9226021Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 68, in write_report_text_guarded
2026-06-02T08:23:54.9227311Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-02T08:23:54.9228674Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-06-02T08:23:54.9229944Z     raise ReportOutputBoundaryError(
2026-06-02T08:23:54.9231439Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
```

```text
2026-06-02T08:23:54.9227311Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-02T08:23:54.9228674Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-06-02T08:23:54.9229944Z     raise ReportOutputBoundaryError(
2026-06-02T08:23:54.9231439Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-06-02T08:23:54.9438039Z ##[error]Process completed with exit code 1.
2026-06-02T08:23:54.9522326Z ##[group]Run actions/upload-artifact@v4
2026-06-02T08:23:54.9522664Z with:
2026-06-02T08:23:54.9522872Z   name: validated-weekly-report
2026-06-02T08:23:54.9523144Z   path: reports/weekly-report.md
2026-06-02T08:23:54.9523404Z   retention-days: 14
2026-06-02T08:23:54.9523990Z   if-no-files-found: warn
2026-06-02T08:23:54.9524410Z   compression-level: 6
2026-06-02T08:23:54.9524801Z   overwrite: false
2026-06-02T08:23:54.9525194Z   include-hidden-files: false
2026-06-02T08:23:54.9525610Z env:
2026-06-02T08:23:54.9526110Z   POLYGON_API_KEY: ***
```

## CI

- Run ID: `26807732203`
- Branch: `main`
- Commit: `0dfe9e8f13e9`
- Title: Exclude missing edge evidence results from breakeven metrics
- Created: 2026-06-02T08:23:32Z
- Updated: 2026-06-02T08:24:27Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26807732203

### Failed job: Pytest

- Job ID: `79029444571`
- Started: 2026-06-02T08:23:35Z
- Completed: 2026-06-02T08:24:26Z
- Failed steps: 52. Full regression suite residual tests

#### Error context

```text
2026-06-02T08:24:24.2270951Z ........................................................................ [ 85%]
2026-06-02T08:24:24.3844863Z ........................................................................ [ 92%]
2026-06-02T08:24:24.4813915Z ........................................................................ [ 98%]
2026-06-02T08:24:24.5338155Z ...............                                                          [100%]
2026-06-02T08:24:24.5338853Z =================================== FAILURES ===================================
2026-06-02T08:24:24.5339591Z ________ test_er5_zero_result_5d_is_not_replaced_by_performance_percent ________
2026-06-02T08:24:24.5340316Z 
2026-06-02T08:24:24.5340728Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-33/test_er5_zero_result_5d_is_not0')
2026-06-02T08:24:24.5341322Z 
2026-06-02T08:24:24.5341830Z     def test_er5_zero_result_5d_is_not_replaced_by_performance_percent(tmp_path: Path) -> None:
2026-06-02T08:24:24.5342595Z         path = tmp_path / "history.json"
2026-06-02T08:24:24.5343035Z         outcomes = [
2026-06-02T08:24:24.5343371Z             {
2026-06-02T08:24:24.5343695Z                 "symbol": "TEST",
2026-06-02T08:24:24.5344134Z                 "setup_type": "momentum_breakout",
2026-06-02T08:24:24.5344623Z                 "market_regime": "low_vol_bull",
```

```text
2026-06-02T08:24:24.5352686Z         assert adjustment.sample_size == 6
2026-06-02T08:24:24.5353147Z         assert adjustment.expectancy == 0.0
2026-06-02T08:24:24.5353578Z         assert adjustment.win_rate == 0.0
2026-06-02T08:24:24.5353990Z >       assert adjustment.score_delta == 0.0
2026-06-02T08:24:24.5354451Z E       AssertionError: assert -12.0 == 0.0
2026-06-02T08:24:24.5356399Z E        +  where -12.0 = ExpectancyAdjustment(profile_key='regime_setup_entry::low_vol_bull::momentum_breakout::break_above', source='regime_se... expectancy=0.0, score_delta=-12.0, size_multiplier=0.5, recommendation='avoid_or_block', reason='negative_expectancy').score_delta
2026-06-02T08:24:24.5357830Z 
2026-06-02T08:24:24.5358084Z tests/test_er5_expectancy_zero_result_guard.py:34: AssertionError
2026-06-02T08:24:24.5358694Z =============================== warnings summary ===============================
2026-06-02T08:24:24.5359481Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbol_writes_csv_and_metadata
2026-06-02T08:24:24.5360668Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbol_merges_without_duplicates
2026-06-02T08:24:24.5361672Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbols_batch_counts_results
2026-06-02T08:24:24.5362615Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbols_batch_counts_results
2026-06-02T08:24:24.5365254Z   /home/runner/work/institutional-trading-engine/institutional-trading-engine/src/historical/polygon_ingestion.py:125: FutureWarning: The behavior of DataFrame concatenation with empty or all-NA entries is deprecated. In a future version, this will no longer exclude empty or all-NA columns when determining the result dtypes. To retain the old behavior, exclude the relevant entries before the concat operation.
2026-06-02T08:24:24.5367665Z     combined = pd.concat([existing, df], ignore_index=True)
2026-06-02T08:24:24.5368024Z
```

```text
2026-06-02T08:24:24.5353990Z >       assert adjustment.score_delta == 0.0
2026-06-02T08:24:24.5354451Z E       AssertionError: assert -12.0 == 0.0
2026-06-02T08:24:24.5356399Z E        +  where -12.0 = ExpectancyAdjustment(profile_key='regime_setup_entry::low_vol_bull::momentum_breakout::break_above', source='regime_se... expectancy=0.0, score_delta=-12.0, size_multiplier=0.5, recommendation='avoid_or_block', reason='negative_expectancy').score_delta
2026-06-02T08:24:24.5357830Z 
2026-06-02T08:24:24.5358084Z tests/test_er5_expectancy_zero_result_guard.py:34: AssertionError
2026-06-02T08:24:24.5358694Z =============================== warnings summary ===============================
2026-06-02T08:24:24.5359481Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbol_writes_csv_and_metadata
2026-06-02T08:24:24.5360668Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbol_merges_without_duplicates
2026-06-02T08:24:24.5361672Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbols_batch_counts_results
2026-06-02T08:24:24.5362615Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbols_batch_counts_results
2026-06-02T08:24:24.5365254Z   /home/runner/work/institutional-trading-engine/institutional-trading-engine/src/historical/polygon_ingestion.py:125: FutureWarning: The behavior of DataFrame concatenation with empty or all-NA entries is deprecated. In a future version, this will no longer exclude empty or all-NA columns when determining the result dtypes. To retain the old behavior, exclude the relevant entries before the concat operation.
2026-06-02T08:24:24.5367665Z     combined = pd.concat([existing, df], ignore_index=True)
2026-06-02T08:24:24.5368024Z 
2026-06-02T08:24:24.5368507Z -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2026-06-02T08:24:24.5369145Z =========================== short test summary info ============================
2026-06-02T08:24:24.5370375Z FAILED tests/test_er5_expectancy_zero_result_guard.py::test_er5_zero_result_5d_is_not_replaced_by_performance_percent - AssertionError: assert -12.0 == 0.0
```

```text
2026-06-02T08:24:24.5367665Z     combined = pd.concat([existing, df], ignore_index=True)
2026-06-02T08:24:24.5368024Z 
2026-06-02T08:24:24.5368507Z -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2026-06-02T08:24:24.5369145Z =========================== short test summary info ============================
2026-06-02T08:24:24.5370375Z FAILED tests/test_er5_expectancy_zero_result_guard.py::test_er5_zero_result_5d_is_not_replaced_by_performance_percent - AssertionError: assert -12.0 == 0.0
2026-06-02T08:24:24.5372510Z  +  where -12.0 = ExpectancyAdjustment(profile_key='regime_setup_entry::low_vol_bull::momentum_breakout::break_above', source='regime_se... expectancy=0.0, score_delta=-12.0, size_multiplier=0.5, recommendation='avoid_or_block', reason='negative_expectancy').score_delta
2026-06-02T08:24:24.5374162Z 1 failed, 1093 passed, 1 skipped, 1 deselected, 4 warnings in 9.57s
2026-06-02T08:24:24.8611167Z ##[error]Process completed with exit code 1.
2026-06-02T08:24:24.8722957Z Post job cleanup.
2026-06-02T08:24:24.9736020Z [command]/usr/bin/git version
2026-06-02T08:24:24.9776742Z git version 2.54.0
2026-06-02T08:24:24.9818907Z Temporarily overriding HOME='/home/runner/work/_temp/73d877af-c317-4650-9ac0-42016805ca3b' before making global git config changes
2026-06-02T08:24:24.9820261Z Adding repository directory to the temporary git global config as a safe directory
2026-06-02T08:24:24.9834074Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-06-02T08:24:24.9873816Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-06-02T08:24:24.9910875Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
```

```text
2026-06-02T08:24:24.5369145Z =========================== short test summary info ============================
2026-06-02T08:24:24.5370375Z FAILED tests/test_er5_expectancy_zero_result_guard.py::test_er5_zero_result_5d_is_not_replaced_by_performance_percent - AssertionError: assert -12.0 == 0.0
2026-06-02T08:24:24.5372510Z  +  where -12.0 = ExpectancyAdjustment(profile_key='regime_setup_entry::low_vol_bull::momentum_breakout::break_above', source='regime_se... expectancy=0.0, score_delta=-12.0, size_multiplier=0.5, recommendation='avoid_or_block', reason='negative_expectancy').score_delta
2026-06-02T08:24:24.5374162Z 1 failed, 1093 passed, 1 skipped, 1 deselected, 4 warnings in 9.57s
2026-06-02T08:24:24.8611167Z ##[error]Process completed with exit code 1.
2026-06-02T08:24:24.8722957Z Post job cleanup.
2026-06-02T08:24:24.9736020Z [command]/usr/bin/git version
2026-06-02T08:24:24.9776742Z git version 2.54.0
2026-06-02T08:24:24.9818907Z Temporarily overriding HOME='/home/runner/work/_temp/73d877af-c317-4650-9ac0-42016805ca3b' before making global git config changes
2026-06-02T08:24:24.9820261Z Adding repository directory to the temporary git global config as a safe directory
2026-06-02T08:24:24.9834074Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-06-02T08:24:24.9873816Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-06-02T08:24:24.9910875Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-06-02T08:24:25.0164598Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-06-02T08:24:25.0192917Z http.https://github.com/.extraheader
2026-06-02T08:24:25.0205564Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

## Decision Engine Tests

- Run ID: `26807732137`
- Branch: `main`
- Commit: `0dfe9e8f13e9`
- Title: Exclude missing edge evidence results from breakeven metrics
- Created: 2026-06-02T08:23:32Z
- Updated: 2026-06-02T08:24:04Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26807732137

### Failed job: tests

- Job ID: `79029444454`
- Started: 2026-06-02T08:23:35Z
- Completed: 2026-06-02T08:24:04Z
- Failed steps: 5. Run pytest

#### Error context

```text
2026-06-02T08:24:02.0828943Z ........................................................................ [ 89%]
2026-06-02T08:24:02.3026870Z ........................................................................ [ 93%]
2026-06-02T08:24:02.3464852Z ........................................................................ [ 98%]
2026-06-02T08:24:02.4102372Z .....................                                                    [100%]
2026-06-02T08:24:02.4103594Z =================================== FAILURES ===================================
2026-06-02T08:24:02.4104664Z ________ test_er5_zero_result_5d_is_not_replaced_by_performance_percent ________
2026-06-02T08:24:02.4105473Z 
2026-06-02T08:24:02.4106016Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-0/test_er5_zero_result_5d_is_not0')
2026-06-02T08:24:02.4107158Z 
2026-06-02T08:24:02.4107736Z     def test_er5_zero_result_5d_is_not_replaced_by_performance_percent(tmp_path: Path) -> None:
2026-06-02T08:24:02.4108678Z         path = tmp_path / "history.json"
2026-06-02T08:24:02.4109241Z         outcomes = [
2026-06-02T08:24:02.4109649Z             {
2026-06-02T08:24:02.4110059Z                 "symbol": "TEST",
2026-06-02T08:24:02.4110820Z                 "setup_type": "momentum_breakout",
2026-06-02T08:24:02.4111530Z                 "market_regime": "low_vol_bull",
```

```text
2026-06-02T08:24:02.4119092Z         assert adjustment.sample_size == 6
2026-06-02T08:24:02.4119387Z         assert adjustment.expectancy == 0.0
2026-06-02T08:24:02.4119675Z         assert adjustment.win_rate == 0.0
2026-06-02T08:24:02.4119963Z >       assert adjustment.score_delta == 0.0
2026-06-02T08:24:02.4120257Z E       AssertionError: assert -12.0 == 0.0
2026-06-02T08:24:02.4121436Z E        +  where -12.0 = ExpectancyAdjustment(profile_key='regime_setup_entry::low_vol_bull::momentum_breakout::break_above', source='regime_se... expectancy=0.0, score_delta=-12.0, size_multiplier=0.5, recommendation='avoid_or_block', reason='negative_expectancy').score_delta
2026-06-02T08:24:02.4122674Z 
2026-06-02T08:24:02.4122873Z tests/test_er5_expectancy_zero_result_guard.py:34: AssertionError
2026-06-02T08:24:02.4123377Z _________ TestDataPersistence.test_decision_log_path_not_in_gitignore __________
2026-06-02T08:24:02.4123705Z 
2026-06-02T08:24:02.4123915Z self = <test_priority_fixes.TestDataPersistence object at 0x7f262c1c3c50>
2026-06-02T08:24:02.4124218Z 
2026-06-02T08:24:02.4124355Z     def test_decision_log_path_not_in_gitignore(self):
2026-06-02T08:24:02.4124675Z         gitignore = Path(".gitignore")
2026-06-02T08:24:02.4124948Z         if not gitignore.exists():
2026-06-02T08:24:02.4125201Z             return
```

```text
2026-06-02T08:24:02.4119963Z >       assert adjustment.score_delta == 0.0
2026-06-02T08:24:02.4120257Z E       AssertionError: assert -12.0 == 0.0
2026-06-02T08:24:02.4121436Z E        +  where -12.0 = ExpectancyAdjustment(profile_key='regime_setup_entry::low_vol_bull::momentum_breakout::break_above', source='regime_se... expectancy=0.0, score_delta=-12.0, size_multiplier=0.5, recommendation='avoid_or_block', reason='negative_expectancy').score_delta
2026-06-02T08:24:02.4122674Z 
2026-06-02T08:24:02.4122873Z tests/test_er5_expectancy_zero_result_guard.py:34: AssertionError
2026-06-02T08:24:02.4123377Z _________ TestDataPersistence.test_decision_log_path_not_in_gitignore __________
2026-06-02T08:24:02.4123705Z 
2026-06-02T08:24:02.4123915Z self = <test_priority_fixes.TestDataPersistence object at 0x7f262c1c3c50>
2026-06-02T08:24:02.4124218Z 
2026-06-02T08:24:02.4124355Z     def test_decision_log_path_not_in_gitignore(self):
2026-06-02T08:24:02.4124675Z         gitignore = Path(".gitignore")
2026-06-02T08:24:02.4124948Z         if not gitignore.exists():
2026-06-02T08:24:02.4125201Z             return
2026-06-02T08:24:02.4125417Z         content = gitignore.read_text()
2026-06-02T08:24:02.4125709Z         # data/ should NOT be in gitignore
2026-06-02T08:24:02.4125985Z >       assert "data/" not in content, (
```

```text
2026-06-02T08:24:02.4125709Z         # data/ should NOT be in gitignore
2026-06-02T08:24:02.4125985Z >       assert "data/" not in content, (
2026-06-02T08:24:02.4126567Z             "data/ is in .gitignore â decision log will be lost on every run"
2026-06-02T08:24:02.4126919Z         )
2026-06-02T08:24:02.4127308Z E       AssertionError: data/ is in .gitignore â decision log will be lost on every run
2026-06-02T08:24:02.4127768Z E       assert 'data/' not in '# Python\n_...\n.vscode/\n'
2026-06-02T08:24:02.4128068Z E         
2026-06-02T08:24:02.4128280Z E         'data/' is contained here:
2026-06-02T08:24:02.4128544Z E           e/
2026-06-02T08:24:02.4128739Z E           cache/
2026-06-02T08:24:02.4128941Z E           data/raw/
2026-06-02T08:24:02.4129155Z E           data/live/
2026-06-02T08:24:02.4129375Z E           data/private/
2026-06-02T08:24:02.4129605Z E           data/vendor/
2026-06-02T08:24:02.4129828Z E           evidence/
2026-06-02T08:24:02.4130033Z E           lockbox/
```

```text
2026-06-02T08:24:02.4138536Z E           .DS_Store
2026-06-02T08:24:02.4138735Z E           .idea/
2026-06-02T08:24:02.4138932Z E           .vscode/
2026-06-02T08:24:02.4139064Z 
2026-06-02T08:24:02.4139190Z tests/test_priority_fixes.py:372: AssertionError
2026-06-02T08:24:02.4139547Z =============================== warnings summary ===============================
2026-06-02T08:24:02.4140087Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbol_writes_csv_and_metadata
2026-06-02T08:24:02.4140747Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbol_merges_without_duplicates
2026-06-02T08:24:02.4141395Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbols_batch_counts_results
2026-06-02T08:24:02.4142319Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbols_batch_counts_results
2026-06-02T08:24:02.4144064Z   /home/runner/work/institutional-trading-engine/institutional-trading-engine/src/historical/polygon_ingestion.py:125: FutureWarning: The behavior of DataFrame concatenation with empty or all-NA entries is deprecated. In a future version, this will no longer exclude empty or all-NA columns when determining the result dtypes. To retain the old behavior, exclude the relevant entries before the concat operation.
2026-06-02T08:24:02.4145653Z     combined = pd.concat([existing, df], ignore_index=True)
2026-06-02T08:24:02.4145897Z 
2026-06-02T08:24:02.4146128Z -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2026-06-02T08:24:02.4146613Z =========================== short test summary info ============================
2026-06-02T08:24:02.4147345Z FAILED tests/test_er5_expectancy_zero_result_guard.py::test_er5_zero_result_5d_is_not_replaced_by_performance_percent - AssertionError: assert -12.0 == 0.0
```

```text
2026-06-02T08:24:02.4145653Z     combined = pd.concat([existing, df], ignore_index=True)
2026-06-02T08:24:02.4145897Z 
2026-06-02T08:24:02.4146128Z -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2026-06-02T08:24:02.4146613Z =========================== short test summary info ============================
2026-06-02T08:24:02.4147345Z FAILED tests/test_er5_expectancy_zero_result_guard.py::test_er5_zero_result_5d_is_not_replaced_by_performance_percent - AssertionError: assert -12.0 == 0.0
2026-06-02T08:24:02.4148767Z  +  where -12.0 = ExpectancyAdjustment(profile_key='regime_setup_entry::low_vol_bull::momentum_breakout::break_above', source='regime_se... expectancy=0.0, score_delta=-12.0, size_multiplier=0.5, recommendation='avoid_or_block', reason='negative_expectancy').score_delta
2026-06-02T08:24:02.4150376Z FAILED tests/test_priority_fixes.py::TestDataPersistence::test_decision_log_path_not_in_gitignore - AssertionError: data/ is in .gitignore â decision log will be lost on every run
2026-06-02T08:24:02.4151289Z assert 'data/' not in '# Python\n_...\n.vscode/\n'
2026-06-02T08:24:02.4151580Z   
2026-06-02T08:24:02.4151771Z   'data/' is contained here:
2026-06-02T08:24:02.4152276Z     e/
2026-06-02T08:24:02.4152464Z     cache/
2026-06-02T08:24:02.4152649Z     data/raw/
2026-06-02T08:24:02.4152836Z     data/live/
2026-06-02T08:24:02.4153028Z     data/private/
2026-06-02T08:24:02.4153254Z     data/vendor/
```

```text
2026-06-02T08:24:02.4146128Z -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2026-06-02T08:24:02.4146613Z =========================== short test summary info ============================
2026-06-02T08:24:02.4147345Z FAILED tests/test_er5_expectancy_zero_result_guard.py::test_er5_zero_result_5d_is_not_replaced_by_performance_percent - AssertionError: assert -12.0 == 0.0
2026-06-02T08:24:02.4148767Z  +  where -12.0 = ExpectancyAdjustment(profile_key='regime_setup_entry::low_vol_bull::momentum_breakout::break_above', source='regime_se... expectancy=0.0, score_delta=-12.0, size_multiplier=0.5, recommendation='avoid_or_block', reason='negative_expectancy').score_delta
2026-06-02T08:24:02.4150376Z FAILED tests/test_priority_fixes.py::TestDataPersistence::test_decision_log_path_not_in_gitignore - AssertionError: data/ is in .gitignore â decision log will be lost on every run
2026-06-02T08:24:02.4151289Z assert 'data/' not in '# Python\n_...\n.vscode/\n'
2026-06-02T08:24:02.4151580Z   
2026-06-02T08:24:02.4151771Z   'data/' is contained here:
2026-06-02T08:24:02.4152276Z     e/
2026-06-02T08:24:02.4152464Z     cache/
2026-06-02T08:24:02.4152649Z     data/raw/
2026-06-02T08:24:02.4152836Z     data/live/
2026-06-02T08:24:02.4153028Z     data/private/
2026-06-02T08:24:02.4153254Z     data/vendor/
2026-06-02T08:24:02.4153445Z     evidence/
2026-06-02T08:24:02.4153776Z     lockbox/
```

```text
2026-06-02T08:24:02.4160889Z     .DS_Store
2026-06-02T08:24:02.4161069Z     .idea/
2026-06-02T08:24:02.4161258Z     .vscode/
2026-06-02T08:24:02.4161501Z 2 failed, 1530 passed, 1 skipped, 4 warnings in 11.65s
2026-06-02T08:24:02.6413798Z ##[error]Process completed with exit code 1.
2026-06-02T08:24:02.6530608Z Post job cleanup.
2026-06-02T08:24:02.7506042Z [command]/usr/bin/git version
2026-06-02T08:24:02.7541654Z git version 2.54.0
2026-06-02T08:24:02.7584993Z Temporarily overriding HOME='/home/runner/work/_temp/cfcfd00c-bf7c-411b-9597-14d49bd38a74' before making global git config changes
2026-06-02T08:24:02.7586308Z Adding repository directory to the temporary git global config as a safe directory
2026-06-02T08:24:02.7597852Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-06-02T08:24:02.7630709Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-06-02T08:24:02.7661819Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-06-02T08:24:02.7885101Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-06-02T08:24:02.7907659Z http.https://github.com/.extraheader
2026-06-02T08:24:02.7919658Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

## Decision Engine Tests

- Run ID: `26807653215`
- Branch: `main`
- Commit: `a7ad248b17d4`
- Title: Preserve zero outcome results in expectancy adjustment
- Created: 2026-06-02T08:21:52Z
- Updated: 2026-06-02T08:22:26Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26807653215

### Failed job: tests

- Job ID: `79029176302`
- Started: 2026-06-02T08:21:56Z
- Completed: 2026-06-02T08:22:25Z
- Failed steps: 5. Run pytest

#### Error context

```text
2026-06-02T08:22:22.6599870Z ........................................................................ [ 89%]
2026-06-02T08:22:22.8559594Z ........................................................................ [ 93%]
2026-06-02T08:22:22.8892015Z ........................................................................ [ 98%]
2026-06-02T08:22:22.9437813Z .....................                                                    [100%]
2026-06-02T08:22:22.9438831Z =================================== FAILURES ===================================
2026-06-02T08:22:22.9439690Z ________ test_er5_zero_result_5d_is_not_replaced_by_performance_percent ________
2026-06-02T08:22:22.9440278Z 
2026-06-02T08:22:22.9440727Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-0/test_er5_zero_result_5d_is_not0')
2026-06-02T08:22:22.9441674Z 
2026-06-02T08:22:22.9442224Z     def test_er5_zero_result_5d_is_not_replaced_by_performance_percent(tmp_path: Path) -> None:
2026-06-02T08:22:22.9443183Z         path = tmp_path / "history.json"
2026-06-02T08:22:22.9443738Z         outcomes = [
2026-06-02T08:22:22.9444156Z             {
2026-06-02T08:22:22.9444574Z                 "symbol": "TEST",
2026-06-02T08:22:22.9445133Z                 "setup_type": "momentum_breakout",
2026-06-02T08:22:22.9445986Z                 "market_regime": "low_vol_bull",
```

```text
2026-06-02T08:22:22.9452559Z         assert adjustment.sample_size == 6
2026-06-02T08:22:22.9452849Z         assert adjustment.expectancy == 0.0
2026-06-02T08:22:22.9453136Z         assert adjustment.win_rate == 0.0
2026-06-02T08:22:22.9453421Z >       assert adjustment.score_delta == 0.0
2026-06-02T08:22:22.9453712Z E       AssertionError: assert -12.0 == 0.0
2026-06-02T08:22:22.9454806Z E        +  where -12.0 = ExpectancyAdjustment(profile_key='regime_setup_entry::low_vol_bull::momentum_breakout::break_above', source='regime_se... expectancy=0.0, score_delta=-12.0, size_multiplier=0.5, recommendation='avoid_or_block', reason='negative_expectancy').score_delta
2026-06-02T08:22:22.9455878Z 
2026-06-02T08:22:22.9456067Z tests/test_er5_expectancy_zero_result_guard.py:34: AssertionError
2026-06-02T08:22:22.9456520Z ____________ test_er6_missing_result_r_is_not_counted_as_breakeven _____________
2026-06-02T08:22:22.9456797Z 
2026-06-02T08:22:22.9456988Z     def test_er6_missing_result_r_is_not_counted_as_breakeven() -> None:
2026-06-02T08:22:22.9457384Z         diagnostics = build_edge_evidence_diagnostics(
2026-06-02T08:22:22.9457683Z             [
2026-06-02T08:22:22.9457939Z                 {"signal_id": "missing", "exit_date": "2026-06-01"},
2026-06-02T08:22:22.9458322Z                 {"signal_id": "zero", "exit_date": "2026-06-01", "result_r": 0.0},
2026-06-02T08:22:22.9458736Z                 {"signal_id": "win", "exit_date": "2026-06-01", "result_r": 1.0},
```

```text
2026-06-02T08:22:22.9453421Z >       assert adjustment.score_delta == 0.0
2026-06-02T08:22:22.9453712Z E       AssertionError: assert -12.0 == 0.0
2026-06-02T08:22:22.9454806Z E        +  where -12.0 = ExpectancyAdjustment(profile_key='regime_setup_entry::low_vol_bull::momentum_breakout::break_above', source='regime_se... expectancy=0.0, score_delta=-12.0, size_multiplier=0.5, recommendation='avoid_or_block', reason='negative_expectancy').score_delta
2026-06-02T08:22:22.9455878Z 
2026-06-02T08:22:22.9456067Z tests/test_er5_expectancy_zero_result_guard.py:34: AssertionError
2026-06-02T08:22:22.9456520Z ____________ test_er6_missing_result_r_is_not_counted_as_breakeven _____________
2026-06-02T08:22:22.9456797Z 
2026-06-02T08:22:22.9456988Z     def test_er6_missing_result_r_is_not_counted_as_breakeven() -> None:
2026-06-02T08:22:22.9457384Z         diagnostics = build_edge_evidence_diagnostics(
2026-06-02T08:22:22.9457683Z             [
2026-06-02T08:22:22.9457939Z                 {"signal_id": "missing", "exit_date": "2026-06-01"},
2026-06-02T08:22:22.9458322Z                 {"signal_id": "zero", "exit_date": "2026-06-01", "result_r": 0.0},
2026-06-02T08:22:22.9458736Z                 {"signal_id": "win", "exit_date": "2026-06-01", "result_r": 1.0},
2026-06-02T08:22:22.9459061Z             ],
2026-06-02T08:22:22.9459310Z             walk_forward_report=_walk_forward_report(),
2026-06-02T08:22:22.9459606Z             oos_report=_oos_report(),
```

```text
2026-06-02T08:22:22.9460537Z     
2026-06-02T08:22:22.9460730Z >       assert historical["total"] == 2
2026-06-02T08:22:22.9461021Z E       assert 3 == 2
2026-06-02T08:22:22.9461161Z 
2026-06-02T08:22:22.9461347Z tests/test_er6_edge_evidence_missing_result_guard.py:62: AssertionError
2026-06-02T08:22:22.9461822Z _________ TestDataPersistence.test_decision_log_path_not_in_gitignore __________
2026-06-02T08:22:22.9462126Z 
2026-06-02T08:22:22.9462325Z self = <test_priority_fixes.TestDataPersistence object at 0x7fc413733050>
2026-06-02T08:22:22.9462600Z 
2026-06-02T08:22:22.9462870Z     def test_decision_log_path_not_in_gitignore(self):
2026-06-02T08:22:22.9463194Z         gitignore = Path(".gitignore")
2026-06-02T08:22:22.9463477Z         if not gitignore.exists():
2026-06-02T08:22:22.9463723Z             return
2026-06-02T08:22:22.9463948Z         content = gitignore.read_text()
2026-06-02T08:22:22.9464225Z         # data/ should NOT be in gitignore
2026-06-02T08:22:22.9464500Z >       assert "data/" not in content, (
```

```text
2026-06-02T08:22:22.9464225Z         # data/ should NOT be in gitignore
2026-06-02T08:22:22.9464500Z >       assert "data/" not in content, (
2026-06-02T08:22:22.9465066Z             "data/ is in .gitignore â decision log will be lost on every run"
2026-06-02T08:22:22.9465621Z         )
2026-06-02T08:22:22.9466136Z E       AssertionError: data/ is in .gitignore â decision log will be lost on every run
2026-06-02T08:22:22.9466607Z E       assert 'data/' not in '# Python\n_...\n.vscode/\n'
2026-06-02T08:22:22.9466902Z E         
2026-06-02T08:22:22.9467105Z E         'data/' is contained here:
2026-06-02T08:22:22.9467363Z E           e/
2026-06-02T08:22:22.9467561Z E           cache/
2026-06-02T08:22:22.9467772Z E           data/raw/
2026-06-02T08:22:22.9467978Z E           data/live/
2026-06-02T08:22:22.9468198Z E           data/private/
2026-06-02T08:22:22.9468427Z E           data/vendor/
2026-06-02T08:22:22.9468645Z E           evidence/
2026-06-02T08:22:22.9468852Z E           lockbox/
```

```text
2026-06-02T08:22:22.9477073Z E           .DS_Store
2026-06-02T08:22:22.9477289Z E           .idea/
2026-06-02T08:22:22.9477486Z E           .vscode/
2026-06-02T08:22:22.9477607Z 
2026-06-02T08:22:22.9477736Z tests/test_priority_fixes.py:372: AssertionError
2026-06-02T08:22:22.9478230Z =============================== warnings summary ===============================
2026-06-02T08:22:22.9478790Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbol_writes_csv_and_metadata
2026-06-02T08:22:22.9479407Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbol_merges_without_duplicates
2026-06-02T08:22:22.9480017Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbols_batch_counts_results
2026-06-02T08:22:22.9480616Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbols_batch_counts_results
2026-06-02T08:22:22.9482369Z   /home/runner/work/institutional-trading-engine/institutional-trading-engine/src/historical/polygon_ingestion.py:125: FutureWarning: The behavior of DataFrame concatenation with empty or all-NA entries is deprecated. In a future version, this will no longer exclude empty or all-NA columns when determining the result dtypes. To retain the old behavior, exclude the relevant entries before the concat operation.
2026-06-02T08:22:22.9483880Z     combined = pd.concat([existing, df], ignore_index=True)
2026-06-02T08:22:22.9484112Z 
2026-06-02T08:22:22.9484417Z -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2026-06-02T08:22:22.9484848Z =========================== short test summary info ============================
2026-06-02T08:22:22.9485660Z FAILED tests/test_er5_expectancy_zero_result_guard.py::test_er5_zero_result_5d_is_not_replaced_by_performance_percent - AssertionError: assert -12.0 == 0.0
```

```text
2026-06-02T08:22:22.9483880Z     combined = pd.concat([existing, df], ignore_index=True)
2026-06-02T08:22:22.9484112Z 
2026-06-02T08:22:22.9484417Z -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2026-06-02T08:22:22.9484848Z =========================== short test summary info ============================
2026-06-02T08:22:22.9485660Z FAILED tests/test_er5_expectancy_zero_result_guard.py::test_er5_zero_result_5d_is_not_replaced_by_performance_percent - AssertionError: assert -12.0 == 0.0
2026-06-02T08:22:22.9486961Z  +  where -12.0 = ExpectancyAdjustment(profile_key='regime_setup_entry::low_vol_bull::momentum_breakout::break_above', source='regime_se... expectancy=0.0, score_delta=-12.0, size_multiplier=0.5, recommendation='avoid_or_block', reason='negative_expectancy').score_delta
2026-06-02T08:22:22.9488165Z FAILED tests/test_er6_edge_evidence_missing_result_guard.py::test_er6_missing_result_r_is_not_counted_as_breakeven - assert 3 == 2
2026-06-02T08:22:22.9489294Z FAILED tests/test_priority_fixes.py::TestDataPersistence::test_decision_log_path_not_in_gitignore - AssertionError: data/ is in .gitignore â decision log will be lost on every run
2026-06-02T08:22:22.9490006Z assert 'data/' not in '# Python\n_...\n.vscode/\n'
2026-06-02T08:22:22.9490291Z   
2026-06-02T08:22:22.9490493Z   'data/' is contained here:
2026-06-02T08:22:22.9490756Z     e/
2026-06-02T08:22:22.9490950Z     cache/
2026-06-02T08:22:22.9491143Z     data/raw/
2026-06-02T08:22:22.9491342Z     data/live/
2026-06-02T08:22:22.9491544Z     data/private/
```

```text
2026-06-02T08:22:22.9484417Z -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2026-06-02T08:22:22.9484848Z =========================== short test summary info ============================
2026-06-02T08:22:22.9485660Z FAILED tests/test_er5_expectancy_zero_result_guard.py::test_er5_zero_result_5d_is_not_replaced_by_performance_percent - AssertionError: assert -12.0 == 0.0
2026-06-02T08:22:22.9486961Z  +  where -12.0 = ExpectancyAdjustment(profile_key='regime_setup_entry::low_vol_bull::momentum_breakout::break_above', source='regime_se... expectancy=0.0, score_delta=-12.0, size_multiplier=0.5, recommendation='avoid_or_block', reason='negative_expectancy').score_delta
2026-06-02T08:22:22.9488165Z FAILED tests/test_er6_edge_evidence_missing_result_guard.py::test_er6_missing_result_r_is_not_counted_as_breakeven - assert 3 == 2
2026-06-02T08:22:22.9489294Z FAILED tests/test_priority_fixes.py::TestDataPersistence::test_decision_log_path_not_in_gitignore - AssertionError: data/ is in .gitignore â decision log will be lost on every run
2026-06-02T08:22:22.9490006Z assert 'data/' not in '# Python\n_...\n.vscode/\n'
2026-06-02T08:22:22.9490291Z   
2026-06-02T08:22:22.9490493Z   'data/' is contained here:
2026-06-02T08:22:22.9490756Z     e/
2026-06-02T08:22:22.9490950Z     cache/
2026-06-02T08:22:22.9491143Z     data/raw/
2026-06-02T08:22:22.9491342Z     data/live/
2026-06-02T08:22:22.9491544Z     data/private/
2026-06-02T08:22:22.9491743Z     data/vendor/
2026-06-02T08:22:22.9491946Z     evidence/
```

## Report Quality Validation

- Run ID: `26807653341`
- Branch: `main`
- Commit: `a7ad248b17d4`
- Title: Preserve zero outcome results in expectancy adjustment
- Created: 2026-06-02T08:21:52Z
- Updated: 2026-06-02T08:22:32Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26807653341

### Failed job: validate-reports (postmarket)

- Job ID: `79029176781`
- Started: 2026-06-02T08:21:56Z
- Completed: 2026-06-02T08:22:30Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-02T08:22:12.2281694Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-02T08:22:12.2282098Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-02T08:22:12.2282527Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-02T08:22:12.2282883Z ##[endgroup]
2026-06-02T08:22:27.9599203Z Traceback (most recent call last):
2026-06-02T08:22:27.9607661Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 247, in <module>
2026-06-02T08:22:27.9609298Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-29/2026-06-02?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-02T08:22:27.9610740Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-29/2026-06-02?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-02T08:22:27.9612121Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-29/2026-06-02?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-02T08:22:27.9613061Z WARNING: scanner metric loading failed: ModuleNotFoundError: No module named 'config'
2026-06-02T08:22:27.9613516Z WARNING: scanner_metrics_missing:MSFT
2026-06-02T08:22:27.9613811Z WARNING: scanner_metrics_missing:NVDA
2026-06-02T08:22:27.9614088Z WARNING: scanner_metrics_missing:META
2026-06-02T08:22:27.9614364Z WARNING: scanner_metrics_missing:AAPL
2026-06-02T08:22:27.9614645Z WARNING: scanner_metrics_missing:MU
2026-06-02T08:22:27.9614930Z WARNING: scanner_metrics_missing:QQQ
```

```text
2026-06-02T08:22:27.9607661Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 247, in <module>
2026-06-02T08:22:27.9609298Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-29/2026-06-02?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-02T08:22:27.9610740Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-29/2026-06-02?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-02T08:22:27.9612121Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-29/2026-06-02?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-02T08:22:27.9613061Z WARNING: scanner metric loading failed: ModuleNotFoundError: No module named 'config'
2026-06-02T08:22:27.9613516Z WARNING: scanner_metrics_missing:MSFT
2026-06-02T08:22:27.9613811Z WARNING: scanner_metrics_missing:NVDA
2026-06-02T08:22:27.9614088Z WARNING: scanner_metrics_missing:META
2026-06-02T08:22:27.9614364Z WARNING: scanner_metrics_missing:AAPL
2026-06-02T08:22:27.9614645Z WARNING: scanner_metrics_missing:MU
2026-06-02T08:22:27.9614930Z WARNING: scanner_metrics_missing:QQQ
2026-06-02T08:22:27.9615227Z WARNING: scanner_metrics_missing:GLD
2026-06-02T08:22:27.9615518Z WARNING: scanner_metrics_missing:SLV
2026-06-02T08:22:27.9616075Z     raise SystemExit(main())
2026-06-02T08:22:27.9616339Z                      ^^^^^^
2026-06-02T08:22:27.9616985Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 236, in main
```

```text
2026-06-02T08:22:27.9619738Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-02T08:22:27.9620571Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-06-02T08:22:27.9621301Z     raise ReportOutputBoundaryError(
2026-06-02T08:22:27.9622279Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/postmarket-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-06-02T08:22:28.0260254Z ##[error]Process completed with exit code 1.
2026-06-02T08:22:28.0347467Z ##[group]Run actions/upload-artifact@v4
2026-06-02T08:22:28.0347808Z with:
2026-06-02T08:22:28.0348053Z   name: validated-postmarket-report
2026-06-02T08:22:28.0348364Z   path: reports/postmarket-report.md
2026-06-02T08:22:28.0348645Z   retention-days: 14
2026-06-02T08:22:28.0348889Z   if-no-files-found: warn
2026-06-02T08:22:28.0349143Z   compression-level: 6
2026-06-02T08:22:28.0349393Z   overwrite: false
2026-06-02T08:22:28.0349631Z   include-hidden-files: false
2026-06-02T08:22:28.0349886Z env:
2026-06-02T08:22:28.0350237Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (weekly)

- Job ID: `79029176800`
- Started: 2026-06-02T08:21:55Z
- Completed: 2026-06-02T08:22:14Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-02T08:22:10.9582187Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-02T08:22:10.9582586Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-02T08:22:10.9583005Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-02T08:22:10.9583346Z ##[endgroup]
2026-06-02T08:22:11.9694942Z Traceback (most recent call last):
2026-06-02T08:22:11.9702456Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 247, in <module>
2026-06-02T08:22:11.9703379Z     raise SystemExit(main())
2026-06-02T08:22:11.9703669Z                      ^^^^^^
2026-06-02T08:22:11.9704385Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 236, in main
2026-06-02T08:22:11.9705262Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-02T08:22:11.9705790Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-02T08:22:11.9706695Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 68, in write_report_text_guarded
2026-06-02T08:22:11.9707625Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-02T08:22:11.9708835Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-06-02T08:22:11.9709727Z     raise ReportOutputBoundaryError(
2026-06-02T08:22:11.9710847Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
```

```text
2026-06-02T08:22:11.9707625Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-02T08:22:11.9708835Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-06-02T08:22:11.9709727Z     raise ReportOutputBoundaryError(
2026-06-02T08:22:11.9710847Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-06-02T08:22:11.9909574Z ##[error]Process completed with exit code 1.
2026-06-02T08:22:11.9995188Z ##[group]Run actions/upload-artifact@v4
2026-06-02T08:22:11.9995507Z with:
2026-06-02T08:22:11.9995722Z   name: validated-weekly-report
2026-06-02T08:22:11.9995998Z   path: reports/weekly-report.md
2026-06-02T08:22:11.9996268Z   retention-days: 14
2026-06-02T08:22:11.9996498Z   if-no-files-found: warn
2026-06-02T08:22:11.9996739Z   compression-level: 6
2026-06-02T08:22:11.9996966Z   overwrite: false
2026-06-02T08:22:11.9997187Z   include-hidden-files: false
2026-06-02T08:22:11.9997423Z env:
2026-06-02T08:22:11.9998070Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (premarket)

- Job ID: `79029176848`
- Started: 2026-06-02T08:21:56Z
- Completed: 2026-06-02T08:22:31Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-02T08:22:11.3678092Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-02T08:22:11.3678695Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-02T08:22:11.3679150Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-02T08:22:11.3679495Z ##[endgroup]
2026-06-02T08:22:28.6839428Z Traceback (most recent call last):
2026-06-02T08:22:28.6846270Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 247, in <module>
2026-06-02T08:22:28.6848035Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-29/2026-06-02?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-02T08:22:28.6850909Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-29/2026-06-02?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-02T08:22:28.6852756Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-29/2026-06-02?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-02T08:22:28.6853813Z WARNING: scanner metric loading failed: ModuleNotFoundError: No module named 'config'
2026-06-02T08:22:28.6854342Z WARNING: scanner_metrics_missing:MSFT
2026-06-02T08:22:28.6854686Z WARNING: scanner_metrics_missing:NVDA
2026-06-02T08:22:28.6855018Z WARNING: scanner_metrics_missing:META
2026-06-02T08:22:28.6855347Z WARNING: scanner_metrics_missing:AAPL
2026-06-02T08:22:28.6855674Z WARNING: scanner_metrics_missing:MU
2026-06-02T08:22:28.6855999Z WARNING: scanner_metrics_missing:QQQ
```

```text
2026-06-02T08:22:28.6846270Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 247, in <module>
2026-06-02T08:22:28.6848035Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-29/2026-06-02?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-02T08:22:28.6850909Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-29/2026-06-02?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-02T08:22:28.6852756Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-29/2026-06-02?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-02T08:22:28.6853813Z WARNING: scanner metric loading failed: ModuleNotFoundError: No module named 'config'
2026-06-02T08:22:28.6854342Z WARNING: scanner_metrics_missing:MSFT
2026-06-02T08:22:28.6854686Z WARNING: scanner_metrics_missing:NVDA
2026-06-02T08:22:28.6855018Z WARNING: scanner_metrics_missing:META
2026-06-02T08:22:28.6855347Z WARNING: scanner_metrics_missing:AAPL
2026-06-02T08:22:28.6855674Z WARNING: scanner_metrics_missing:MU
2026-06-02T08:22:28.6855999Z WARNING: scanner_metrics_missing:QQQ
2026-06-02T08:22:28.6856519Z     raise SystemExit(main())
2026-06-02T08:22:28.6856822Z                      ^^^^^^
2026-06-02T08:22:28.6857569Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 236, in main
2026-06-02T08:22:28.6858580Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-02T08:22:28.6859107Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```

```text
2026-06-02T08:22:28.6862663Z     raise ReportOutputBoundaryError(
2026-06-02T08:22:28.6863747Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/premarket-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-06-02T08:22:28.6865061Z WARNING: scanner_metrics_missing:GLD
2026-06-02T08:22:28.6865399Z WARNING: scanner_metrics_missing:SLV
2026-06-02T08:22:28.7368839Z ##[error]Process completed with exit code 1.
2026-06-02T08:22:28.7453870Z ##[group]Run actions/upload-artifact@v4
2026-06-02T08:22:28.7454165Z with:
2026-06-02T08:22:28.7454398Z   name: validated-premarket-report
2026-06-02T08:22:28.7454695Z   path: reports/premarket-report.md
2026-06-02T08:22:28.7454972Z   retention-days: 14
2026-06-02T08:22:28.7455217Z   if-no-files-found: warn
2026-06-02T08:22:28.7455464Z   compression-level: 6
2026-06-02T08:22:28.7455704Z   overwrite: false
2026-06-02T08:22:28.7455936Z   include-hidden-files: false
2026-06-02T08:22:28.7456189Z env:
2026-06-02T08:22:28.7456507Z   POLYGON_API_KEY: ***
```

## CI

- Run ID: `26807653260`
- Branch: `main`
- Commit: `a7ad248b17d4`
- Title: Preserve zero outcome results in expectancy adjustment
- Created: 2026-06-02T08:21:52Z
- Updated: 2026-06-02T08:22:48Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26807653260

### Failed job: Pytest

- Job ID: `79029176554`
- Started: 2026-06-02T08:21:56Z
- Completed: 2026-06-02T08:22:47Z
- Failed steps: 52. Full regression suite residual tests

#### Error context

```text
2026-06-02T08:22:43.3267431Z ........................................................................ [ 85%]
2026-06-02T08:22:43.5013501Z ........................................................................ [ 92%]
2026-06-02T08:22:43.5978455Z ........................................................................ [ 98%]
2026-06-02T08:22:43.6521923Z ...............                                                          [100%]
2026-06-02T08:22:43.6522759Z =================================== FAILURES ===================================
2026-06-02T08:22:43.6523585Z ________ test_er5_zero_result_5d_is_not_replaced_by_performance_percent ________
2026-06-02T08:22:43.6524175Z 
2026-06-02T08:22:43.6524634Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-33/test_er5_zero_result_5d_is_not0')
2026-06-02T08:22:43.6525567Z 
2026-06-02T08:22:43.6526097Z     def test_er5_zero_result_5d_is_not_replaced_by_performance_percent(tmp_path: Path) -> None:
2026-06-02T08:22:43.6526957Z         path = tmp_path / "history.json"
2026-06-02T08:22:43.6527441Z         outcomes = [
2026-06-02T08:22:43.6527806Z             {
2026-06-02T08:22:43.6528171Z                 "symbol": "TEST",
2026-06-02T08:22:43.6528665Z                 "setup_type": "momentum_breakout",
2026-06-02T08:22:43.6529208Z                 "market_regime": "low_vol_bull",
```

```text
2026-06-02T08:22:43.6538297Z         assert adjustment.sample_size == 6
2026-06-02T08:22:43.6538763Z         assert adjustment.expectancy == 0.0
2026-06-02T08:22:43.6539217Z         assert adjustment.win_rate == 0.0
2026-06-02T08:22:43.6539647Z >       assert adjustment.score_delta == 0.0
2026-06-02T08:22:43.6540102Z E       AssertionError: assert -12.0 == 0.0
2026-06-02T08:22:43.6542088Z E        +  where -12.0 = ExpectancyAdjustment(profile_key='regime_setup_entry::low_vol_bull::momentum_breakout::break_above', source='regime_se... expectancy=0.0, score_delta=-12.0, size_multiplier=0.5, recommendation='avoid_or_block', reason='negative_expectancy').score_delta
2026-06-02T08:22:43.6543648Z 
2026-06-02T08:22:43.6543923Z tests/test_er5_expectancy_zero_result_guard.py:34: AssertionError
2026-06-02T08:22:43.6544637Z ____________ test_er6_missing_result_r_is_not_counted_as_breakeven _____________
2026-06-02T08:22:43.6545364Z 
2026-06-02T08:22:43.6545646Z     def test_er6_missing_result_r_is_not_counted_as_breakeven() -> None:
2026-06-02T08:22:43.6546341Z         diagnostics = build_edge_evidence_diagnostics(
2026-06-02T08:22:43.6546797Z             [
2026-06-02T08:22:43.6547178Z                 {"signal_id": "missing", "exit_date": "2026-06-01"},
2026-06-02T08:22:43.6547797Z                 {"signal_id": "zero", "exit_date": "2026-06-01", "result_r": 0.0},
2026-06-02T08:22:43.6548475Z                 {"signal_id": "win", "exit_date": "2026-06-01", "result_r": 1.0},
```

```text
2026-06-02T08:22:43.6539647Z >       assert adjustment.score_delta == 0.0
2026-06-02T08:22:43.6540102Z E       AssertionError: assert -12.0 == 0.0
2026-06-02T08:22:43.6542088Z E        +  where -12.0 = ExpectancyAdjustment(profile_key='regime_setup_entry::low_vol_bull::momentum_breakout::break_above', source='regime_se... expectancy=0.0, score_delta=-12.0, size_multiplier=0.5, recommendation='avoid_or_block', reason='negative_expectancy').score_delta
2026-06-02T08:22:43.6543648Z 
2026-06-02T08:22:43.6543923Z tests/test_er5_expectancy_zero_result_guard.py:34: AssertionError
2026-06-02T08:22:43.6544637Z ____________ test_er6_missing_result_r_is_not_counted_as_breakeven _____________
2026-06-02T08:22:43.6545364Z 
2026-06-02T08:22:43.6545646Z     def test_er6_missing_result_r_is_not_counted_as_breakeven() -> None:
2026-06-02T08:22:43.6546341Z         diagnostics = build_edge_evidence_diagnostics(
2026-06-02T08:22:43.6546797Z             [
2026-06-02T08:22:43.6547178Z                 {"signal_id": "missing", "exit_date": "2026-06-01"},
2026-06-02T08:22:43.6547797Z                 {"signal_id": "zero", "exit_date": "2026-06-01", "result_r": 0.0},
2026-06-02T08:22:43.6548475Z                 {"signal_id": "win", "exit_date": "2026-06-01", "result_r": 1.0},
2026-06-02T08:22:43.6548987Z             ],
2026-06-02T08:22:43.6549338Z             walk_forward_report=_walk_forward_report(),
2026-06-02T08:22:43.6549813Z             oos_report=_oos_report(),
```

```text
2026-06-02T08:22:43.6551238Z     
2026-06-02T08:22:43.6551521Z >       assert historical["total"] == 2
2026-06-02T08:22:43.6551959Z E       assert 3 == 2
2026-06-02T08:22:43.6552156Z 
2026-06-02T08:22:43.6552651Z tests/test_er6_edge_evidence_missing_result_guard.py:62: AssertionError
2026-06-02T08:22:43.6553313Z =============================== warnings summary ===============================
2026-06-02T08:22:43.6554166Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbol_writes_csv_and_metadata
2026-06-02T08:22:43.6555438Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbol_merges_without_duplicates
2026-06-02T08:22:43.6556469Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbols_batch_counts_results
2026-06-02T08:22:43.6557450Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbols_batch_counts_results
2026-06-02T08:22:43.6560134Z   /home/runner/work/institutional-trading-engine/institutional-trading-engine/src/historical/polygon_ingestion.py:125: FutureWarning: The behavior of DataFrame concatenation with empty or all-NA entries is deprecated. In a future version, this will no longer exclude empty or all-NA columns when determining the result dtypes. To retain the old behavior, exclude the relevant entries before the concat operation.
2026-06-02T08:22:43.6562666Z     combined = pd.concat([existing, df], ignore_index=True)
2026-06-02T08:22:43.6563045Z 
2026-06-02T08:22:43.6563352Z -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2026-06-02T08:22:43.6564034Z =========================== short test summary info ============================
2026-06-02T08:22:43.6565357Z FAILED tests/test_er5_expectancy_zero_result_guard.py::test_er5_zero_result_5d_is_not_replaced_by_performance_percent - AssertionError: assert -12.0 == 0.0
```

```text
2026-06-02T08:22:43.6562666Z     combined = pd.concat([existing, df], ignore_index=True)
2026-06-02T08:22:43.6563045Z 
2026-06-02T08:22:43.6563352Z -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2026-06-02T08:22:43.6564034Z =========================== short test summary info ============================
2026-06-02T08:22:43.6565357Z FAILED tests/test_er5_expectancy_zero_result_guard.py::test_er5_zero_result_5d_is_not_replaced_by_performance_percent - AssertionError: assert -12.0 == 0.0
2026-06-02T08:22:43.6567507Z  +  where -12.0 = ExpectancyAdjustment(profile_key='regime_setup_entry::low_vol_bull::momentum_breakout::break_above', source='regime_se... expectancy=0.0, score_delta=-12.0, size_multiplier=0.5, recommendation='avoid_or_block', reason='negative_expectancy').score_delta
2026-06-02T08:22:43.6569532Z FAILED tests/test_er6_edge_evidence_missing_result_guard.py::test_er6_missing_result_r_is_not_counted_as_breakeven - assert 3 == 2
2026-06-02T08:22:43.6570560Z 2 failed, 1092 passed, 1 skipped, 1 deselected, 4 warnings in 9.46s
2026-06-02T08:22:43.8417123Z ##[error]Process completed with exit code 1.
2026-06-02T08:22:43.8527604Z Post job cleanup.
2026-06-02T08:22:43.9495080Z [command]/usr/bin/git version
2026-06-02T08:22:43.9533048Z git version 2.54.0
2026-06-02T08:22:43.9580017Z Temporarily overriding HOME='/home/runner/work/_temp/114fefd4-98bb-4b36-a592-0319c26bd5ec' before making global git config changes
2026-06-02T08:22:43.9581472Z Adding repository directory to the temporary git global config as a safe directory
2026-06-02T08:22:43.9594456Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-06-02T08:22:43.9630385Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
```

```text
2026-06-02T08:22:43.6563352Z -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2026-06-02T08:22:43.6564034Z =========================== short test summary info ============================
2026-06-02T08:22:43.6565357Z FAILED tests/test_er5_expectancy_zero_result_guard.py::test_er5_zero_result_5d_is_not_replaced_by_performance_percent - AssertionError: assert -12.0 == 0.0
2026-06-02T08:22:43.6567507Z  +  where -12.0 = ExpectancyAdjustment(profile_key='regime_setup_entry::low_vol_bull::momentum_breakout::break_above', source='regime_se... expectancy=0.0, score_delta=-12.0, size_multiplier=0.5, recommendation='avoid_or_block', reason='negative_expectancy').score_delta
2026-06-02T08:22:43.6569532Z FAILED tests/test_er6_edge_evidence_missing_result_guard.py::test_er6_missing_result_r_is_not_counted_as_breakeven - assert 3 == 2
2026-06-02T08:22:43.6570560Z 2 failed, 1092 passed, 1 skipped, 1 deselected, 4 warnings in 9.46s
2026-06-02T08:22:43.8417123Z ##[error]Process completed with exit code 1.
2026-06-02T08:22:43.8527604Z Post job cleanup.
2026-06-02T08:22:43.9495080Z [command]/usr/bin/git version
2026-06-02T08:22:43.9533048Z git version 2.54.0
2026-06-02T08:22:43.9580017Z Temporarily overriding HOME='/home/runner/work/_temp/114fefd4-98bb-4b36-a592-0319c26bd5ec' before making global git config changes
2026-06-02T08:22:43.9581472Z Adding repository directory to the temporary git global config as a safe directory
2026-06-02T08:22:43.9594456Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-06-02T08:22:43.9630385Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-06-02T08:22:43.9665107Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-06-02T08:22:43.9899781Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
```

```text
2026-06-02T08:22:43.6565357Z FAILED tests/test_er5_expectancy_zero_result_guard.py::test_er5_zero_result_5d_is_not_replaced_by_performance_percent - AssertionError: assert -12.0 == 0.0
2026-06-02T08:22:43.6567507Z  +  where -12.0 = ExpectancyAdjustment(profile_key='regime_setup_entry::low_vol_bull::momentum_breakout::break_above', source='regime_se... expectancy=0.0, score_delta=-12.0, size_multiplier=0.5, recommendation='avoid_or_block', reason='negative_expectancy').score_delta
2026-06-02T08:22:43.6569532Z FAILED tests/test_er6_edge_evidence_missing_result_guard.py::test_er6_missing_result_r_is_not_counted_as_breakeven - assert 3 == 2
2026-06-02T08:22:43.6570560Z 2 failed, 1092 passed, 1 skipped, 1 deselected, 4 warnings in 9.46s
2026-06-02T08:22:43.8417123Z ##[error]Process completed with exit code 1.
2026-06-02T08:22:43.8527604Z Post job cleanup.
2026-06-02T08:22:43.9495080Z [command]/usr/bin/git version
2026-06-02T08:22:43.9533048Z git version 2.54.0
2026-06-02T08:22:43.9580017Z Temporarily overriding HOME='/home/runner/work/_temp/114fefd4-98bb-4b36-a592-0319c26bd5ec' before making global git config changes
2026-06-02T08:22:43.9581472Z Adding repository directory to the temporary git global config as a safe directory
2026-06-02T08:22:43.9594456Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-06-02T08:22:43.9630385Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-06-02T08:22:43.9665107Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-06-02T08:22:43.9899781Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-06-02T08:22:43.9924307Z http.https://github.com/.extraheader
2026-06-02T08:22:43.9937010Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```
