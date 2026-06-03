# GitHub Actions Workflow Error Report

Generated: 2026-06-03 08:55 UTC
Repository: `yalcinkadir/institutional-trading-engine`
Filter since: 2026-06-02 08:55 UTC
Failed runs included: 10

## Report Quality Validation

- Run ID: `26872335203`
- Branch: `main`
- Commit: `5041b9c3d0ff`
- Title: Add RGP13 runtime proof pack summary builder
- Created: 2026-06-03T08:13:56Z
- Updated: 2026-06-03T08:14:39Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26872335203

### Failed job: validate-reports (premarket)

- Job ID: `79250531974`
- Started: 2026-06-03T08:13:59Z
- Completed: 2026-06-03T08:14:37Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-03T08:14:14.9365274Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-03T08:14:14.9365653Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-03T08:14:14.9366082Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-03T08:14:14.9366419Z ##[endgroup]
2026-06-03T08:14:34.2189491Z Traceback (most recent call last):
2026-06-03T08:14:34.2197702Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 247, in <module>
2026-06-03T08:14:34.2198390Z     raise SystemExit(main())
2026-06-03T08:14:34.2198656Z                      ^^^^^^
2026-06-03T08:14:34.2199248Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 236, in main
2026-06-03T08:14:34.2200617Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-30/2026-06-03?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-03T08:14:34.2201545Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-03T08:14:34.2202215Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-03T08:14:34.2202938Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 68, in write_report_text_guarded
2026-06-03T08:14:34.2203676Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-03T08:14:34.2204466Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-06-03T08:14:34.2205163Z     raise ReportOutputBoundaryError(
```

```text
2026-06-03T08:14:34.2205163Z     raise ReportOutputBoundaryError(
2026-06-03T08:14:34.2206049Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/premarket-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-06-03T08:14:34.2207536Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-30/2026-06-03?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-03T08:14:34.2208800Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-30/2026-06-03?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-03T08:14:34.2209651Z WARNING: scanner metric loading failed: ModuleNotFoundError: No module named 'config'
2026-06-03T08:14:34.2210083Z WARNING: scanner_metrics_missing:MSFT
2026-06-03T08:14:34.2210363Z WARNING: scanner_metrics_missing:NVDA
2026-06-03T08:14:34.2210631Z WARNING: scanner_metrics_missing:META
2026-06-03T08:14:34.2210903Z WARNING: scanner_metrics_missing:AAPL
2026-06-03T08:14:34.2211323Z WARNING: scanner_metrics_missing:MU
2026-06-03T08:14:34.2211789Z WARNING: scanner_metrics_missing:QQQ
2026-06-03T08:14:34.2212313Z WARNING: scanner_metrics_missing:GLD
2026-06-03T08:14:34.2212581Z WARNING: scanner_metrics_missing:SLV
2026-06-03T08:14:34.2837279Z ##[error]Process completed with exit code 1.
2026-06-03T08:14:34.2915857Z ##[group]Run actions/upload-artifact@v4
2026-06-03T08:14:34.2916158Z with:
```

```text
2026-06-03T08:14:34.2211323Z WARNING: scanner_metrics_missing:MU
2026-06-03T08:14:34.2211789Z WARNING: scanner_metrics_missing:QQQ
2026-06-03T08:14:34.2212313Z WARNING: scanner_metrics_missing:GLD
2026-06-03T08:14:34.2212581Z WARNING: scanner_metrics_missing:SLV
2026-06-03T08:14:34.2837279Z ##[error]Process completed with exit code 1.
2026-06-03T08:14:34.2915857Z ##[group]Run actions/upload-artifact@v4
2026-06-03T08:14:34.2916158Z with:
2026-06-03T08:14:34.2916389Z   name: validated-premarket-report
2026-06-03T08:14:34.2916687Z   path: reports/premarket-report.md
2026-06-03T08:14:34.2916963Z   retention-days: 14
2026-06-03T08:14:34.2917189Z   if-no-files-found: warn
2026-06-03T08:14:34.2917423Z   compression-level: 6
2026-06-03T08:14:34.2917650Z   overwrite: false
2026-06-03T08:14:34.2917873Z   include-hidden-files: false
2026-06-03T08:14:34.2918111Z env:
2026-06-03T08:14:34.2918411Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (postmarket)

- Job ID: `79250532047`
- Started: 2026-06-03T08:13:58Z
- Completed: 2026-06-03T08:14:36Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-03T08:14:18.9490362Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-03T08:14:18.9490760Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-03T08:14:18.9491182Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-03T08:14:18.9491529Z ##[endgroup]
2026-06-03T08:14:33.7816574Z Traceback (most recent call last):
2026-06-03T08:14:33.7818956Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-30/2026-06-03?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-03T08:14:33.7821280Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-30/2026-06-03?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-03T08:14:33.7823420Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-30/2026-06-03?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-03T08:14:33.7824841Z WARNING: scanner metric loading failed: ModuleNotFoundError: No module named 'config'
2026-06-03T08:14:33.7825507Z WARNING: scanner_metrics_missing:MSFT
2026-06-03T08:14:33.7825934Z WARNING: scanner_metrics_missing:NVDA
2026-06-03T08:14:33.7826367Z WARNING: scanner_metrics_missing:META
2026-06-03T08:14:33.7826774Z WARNING: scanner_metrics_missing:AAPL
2026-06-03T08:14:33.7827178Z WARNING: scanner_metrics_missing:MU
2026-06-03T08:14:33.7827597Z WARNING: scanner_metrics_missing:QQQ
2026-06-03T08:14:33.7828245Z WARNING: scanner_metrics_missing:GLD
```

```text
2026-06-03T08:14:33.7816574Z Traceback (most recent call last):
2026-06-03T08:14:33.7818956Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-30/2026-06-03?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-03T08:14:33.7821280Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-30/2026-06-03?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-03T08:14:33.7823420Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-30/2026-06-03?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-03T08:14:33.7824841Z WARNING: scanner metric loading failed: ModuleNotFoundError: No module named 'config'
2026-06-03T08:14:33.7825507Z WARNING: scanner_metrics_missing:MSFT
2026-06-03T08:14:33.7825934Z WARNING: scanner_metrics_missing:NVDA
2026-06-03T08:14:33.7826367Z WARNING: scanner_metrics_missing:META
2026-06-03T08:14:33.7826774Z WARNING: scanner_metrics_missing:AAPL
2026-06-03T08:14:33.7827178Z WARNING: scanner_metrics_missing:MU
2026-06-03T08:14:33.7827597Z WARNING: scanner_metrics_missing:QQQ
2026-06-03T08:14:33.7828245Z WARNING: scanner_metrics_missing:GLD
2026-06-03T08:14:33.7828632Z WARNING: scanner_metrics_missing:SLV
2026-06-03T08:14:33.7836038Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 247, in <module>
2026-06-03T08:14:33.7837057Z     raise SystemExit(main())
2026-06-03T08:14:33.7837422Z                      ^^^^^^
```

```text
2026-06-03T08:14:33.7842752Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-03T08:14:33.7844063Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-06-03T08:14:33.7845195Z     raise ReportOutputBoundaryError(
2026-06-03T08:14:33.7846688Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/postmarket-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-06-03T08:14:33.8502397Z ##[error]Process completed with exit code 1.
2026-06-03T08:14:33.8589288Z ##[group]Run actions/upload-artifact@v4
2026-06-03T08:14:33.8589617Z with:
2026-06-03T08:14:33.8589851Z   name: validated-postmarket-report
2026-06-03T08:14:33.8590158Z   path: reports/postmarket-report.md
2026-06-03T08:14:33.8590444Z   retention-days: 14
2026-06-03T08:14:33.8590685Z   if-no-files-found: warn
2026-06-03T08:14:33.8590942Z   compression-level: 6
2026-06-03T08:14:33.8591176Z   overwrite: false
2026-06-03T08:14:33.8591411Z   include-hidden-files: false
2026-06-03T08:14:33.8591677Z env:
2026-06-03T08:14:33.8592019Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (weekly)

- Job ID: `79250532133`
- Started: 2026-06-03T08:13:59Z
- Completed: 2026-06-03T08:14:19Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-03T08:14:17.4328168Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-03T08:14:17.4328555Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-03T08:14:17.4328994Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-03T08:14:17.4329325Z ##[endgroup]
2026-06-03T08:14:17.7853242Z Traceback (most recent call last):
2026-06-03T08:14:17.7862001Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 247, in <module>
2026-06-03T08:14:17.7863097Z     raise SystemExit(main())
2026-06-03T08:14:17.7863514Z                      ^^^^^^
2026-06-03T08:14:17.7864500Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 236, in main
2026-06-03T08:14:17.7865701Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-03T08:14:17.7866404Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-03T08:14:17.7867653Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 68, in write_report_text_guarded
2026-06-03T08:14:17.7868904Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-03T08:14:17.7870198Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-06-03T08:14:17.7871515Z     raise ReportOutputBoundaryError(
2026-06-03T08:14:17.7872968Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
```

```text
2026-06-03T08:14:17.7868904Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-03T08:14:17.7870198Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-06-03T08:14:17.7871515Z     raise ReportOutputBoundaryError(
2026-06-03T08:14:17.7872968Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-06-03T08:14:17.8111926Z ##[error]Process completed with exit code 1.
2026-06-03T08:14:17.8197701Z ##[group]Run actions/upload-artifact@v4
2026-06-03T08:14:17.8198015Z with:
2026-06-03T08:14:17.8198231Z   name: validated-weekly-report
2026-06-03T08:14:17.8198499Z   path: reports/weekly-report.md
2026-06-03T08:14:17.8198760Z   retention-days: 14
2026-06-03T08:14:17.8198983Z   if-no-files-found: warn
2026-06-03T08:14:17.8199224Z   compression-level: 6
2026-06-03T08:14:17.8199452Z   overwrite: false
2026-06-03T08:14:17.8199675Z   include-hidden-files: false
2026-06-03T08:14:17.8199927Z env:
2026-06-03T08:14:17.8200298Z   POLYGON_API_KEY: ***
```

## Decision Engine Tests

- Run ID: `26872335080`
- Branch: `main`
- Commit: `5041b9c3d0ff`
- Title: Add RGP13 runtime proof pack summary builder
- Created: 2026-06-03T08:13:56Z
- Updated: 2026-06-03T08:14:36Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26872335080

### Failed job: tests

- Job ID: `79250531542`
- Started: 2026-06-03T08:14:00Z
- Completed: 2026-06-03T08:14:35Z
- Failed steps: 5. Run pytest

#### Error context

```text
2026-06-03T08:14:31.9380293Z ........................................................................ [ 87%]
2026-06-03T08:14:32.0426679Z ........................................................................ [ 92%]
2026-06-03T08:14:32.2094818Z ........................................................................ [ 96%]
2026-06-03T08:14:32.2956316Z .....................................................                    [100%]
2026-06-03T08:14:32.2957047Z =================================== FAILURES ===================================
2026-06-03T08:14:32.2957861Z _________ TestDataPersistence.test_decision_log_path_not_in_gitignore __________
2026-06-03T08:14:32.2958482Z 
2026-06-03T08:14:32.2958870Z self = <test_priority_fixes.TestDataPersistence object at 0x7fd9f966d850>
2026-06-03T08:14:32.2959859Z 
2026-06-03T08:14:32.2960150Z     def test_decision_log_path_not_in_gitignore(self):
2026-06-03T08:14:32.2960740Z         gitignore = Path(".gitignore")
2026-06-03T08:14:32.2961220Z         if not gitignore.exists():
2026-06-03T08:14:32.2961659Z             return
2026-06-03T08:14:32.2962295Z         content = gitignore.read_text()
2026-06-03T08:14:32.2962787Z         # data/ should NOT be in gitignore
2026-06-03T08:14:32.2963273Z >       assert "data/" not in content, (
```

```text
2026-06-03T08:14:32.2962787Z         # data/ should NOT be in gitignore
2026-06-03T08:14:32.2963273Z >       assert "data/" not in content, (
2026-06-03T08:14:32.2964554Z             "data/ is in .gitignore â decision log will be lost on every run"
2026-06-03T08:14:32.2964942Z         )
2026-06-03T08:14:32.2965351Z E       AssertionError: data/ is in .gitignore â decision log will be lost on every run
2026-06-03T08:14:32.2965835Z E       assert 'data/' not in '# Python\n_...\n.vscode/\n'
2026-06-03T08:14:32.2966136Z E         
2026-06-03T08:14:32.2966336Z E         'data/' is contained here:
2026-06-03T08:14:32.2966594Z E           e/
2026-06-03T08:14:32.2966783Z E           cache/
2026-06-03T08:14:32.2966980Z E           data/raw/
2026-06-03T08:14:32.2967185Z E           data/live/
2026-06-03T08:14:32.2967406Z E           data/private/
2026-06-03T08:14:32.2967630Z E           data/vendor/
2026-06-03T08:14:32.2967844Z E           evidence/
2026-06-03T08:14:32.2968045Z E           lockbox/
```

```text
2026-06-03T08:14:32.2976256Z E           .DS_Store
2026-06-03T08:14:32.2976451Z E           .idea/
2026-06-03T08:14:32.2976642Z E           .vscode/
2026-06-03T08:14:32.2976772Z 
2026-06-03T08:14:32.2976907Z tests/test_priority_fixes.py:372: AssertionError
2026-06-03T08:14:32.2977265Z =============================== warnings summary ===============================
2026-06-03T08:14:32.2977913Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbol_writes_csv_and_metadata
2026-06-03T08:14:32.2978653Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbol_merges_without_duplicates
2026-06-03T08:14:32.2979303Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbols_batch_counts_results
2026-06-03T08:14:32.2979927Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbols_batch_counts_results
2026-06-03T08:14:32.2981823Z   /home/runner/work/institutional-trading-engine/institutional-trading-engine/src/historical/polygon_ingestion.py:125: FutureWarning: The behavior of DataFrame concatenation with empty or all-NA entries is deprecated. In a future version, this will no longer exclude empty or all-NA columns when determining the result dtypes. To retain the old behavior, exclude the relevant entries before the concat operation.
2026-06-03T08:14:32.2983455Z     combined = pd.concat([existing, df], ignore_index=True)
2026-06-03T08:14:32.2984143Z 
2026-06-03T08:14:32.2984384Z -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2026-06-03T08:14:32.2984844Z =========================== short test summary info ============================
2026-06-03T08:14:32.2985819Z FAILED tests/test_priority_fixes.py::TestDataPersistence::test_decision_log_path_not_in_gitignore - AssertionError: data/ is in .gitignore â decision log will be lost on every run
```

```text
2026-06-03T08:14:32.2983455Z     combined = pd.concat([existing, df], ignore_index=True)
2026-06-03T08:14:32.2984143Z 
2026-06-03T08:14:32.2984384Z -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2026-06-03T08:14:32.2984844Z =========================== short test summary info ============================
2026-06-03T08:14:32.2985819Z FAILED tests/test_priority_fixes.py::TestDataPersistence::test_decision_log_path_not_in_gitignore - AssertionError: data/ is in .gitignore â decision log will be lost on every run
2026-06-03T08:14:32.2986603Z assert 'data/' not in '# Python\n_...\n.vscode/\n'
2026-06-03T08:14:32.2986901Z   
2026-06-03T08:14:32.2987098Z   'data/' is contained here:
2026-06-03T08:14:32.2987324Z     e/
2026-06-03T08:14:32.2987500Z     cache/
2026-06-03T08:14:32.2987685Z     data/raw/
2026-06-03T08:14:32.2987889Z     data/live/
2026-06-03T08:14:32.2988086Z     data/private/
2026-06-03T08:14:32.2988285Z     data/vendor/
2026-06-03T08:14:32.2988480Z     evidence/
2026-06-03T08:14:32.2988663Z     lockbox/
```

```text
2026-06-03T08:14:32.2995991Z     .DS_Store
2026-06-03T08:14:32.2996169Z     .idea/
2026-06-03T08:14:32.2996342Z     .vscode/
2026-06-03T08:14:32.2996585Z 1 failed, 1563 passed, 1 skipped, 4 warnings in 12.87s
2026-06-03T08:14:32.6439358Z ##[error]Process completed with exit code 1.
2026-06-03T08:14:32.6556185Z Post job cleanup.
2026-06-03T08:14:32.7563455Z [command]/usr/bin/git version
2026-06-03T08:14:32.7601722Z git version 2.54.0
2026-06-03T08:14:32.7645932Z Temporarily overriding HOME='/home/runner/work/_temp/0cc1df99-6844-4de1-914c-84f008163c0d' before making global git config changes
2026-06-03T08:14:32.7647298Z Adding repository directory to the temporary git global config as a safe directory
2026-06-03T08:14:32.7653059Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-06-03T08:14:32.7695428Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-06-03T08:14:32.7728051Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-06-03T08:14:32.7958281Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-06-03T08:14:32.7983488Z http.https://github.com/.extraheader
2026-06-03T08:14:32.7996477Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

## Decision Engine Tests

- Run ID: `26872198958`
- Branch: `main`
- Commit: `d00e7a897931`
- Title: Add RGP13 runtime proof pack summary guard tests
- Created: 2026-06-03T08:10:59Z
- Updated: 2026-06-03T08:11:29Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26872198958

### Failed job: tests

- Job ID: `79250070264`
- Started: 2026-06-03T08:11:01Z
- Completed: 2026-06-03T08:11:28Z
- Failed steps: 5. Run pytest

#### Error context

```text
2026-06-03T08:11:20.9614853Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-03T08:11:20.9615246Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-03T08:11:20.9615591Z ##[endgroup]
2026-06-03T08:11:26.5351675Z 
2026-06-03T08:11:26.5352477Z ==================================== ERRORS ====================================
2026-06-03T08:11:26.5354896Z _______ ERROR collecting tests/test_rgp13_runtime_proof_pack_summary.py ________
2026-06-03T08:11:26.5356384Z ImportError while importing test module '/home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_rgp13_runtime_proof_pack_summary.py'.
2026-06-03T08:11:26.5357868Z Hint: make sure your test modules/packages have valid Python names.
2026-06-03T08:11:26.5358494Z Traceback:
2026-06-03T08:11:26.5359184Z /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/importlib/__init__.py:126: in import_module
2026-06-03T08:11:26.5360119Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-06-03T08:11:26.5360846Z tests/test_rgp13_runtime_proof_pack_summary.py:3: in <module>
2026-06-03T08:11:26.5361683Z     from src.runtime.runtime_proof_pack_summary import build_runtime_proof_pack_summary
2026-06-03T08:11:26.5362648Z E   ModuleNotFoundError: No module named 'src.runtime.runtime_proof_pack_summary'
2026-06-03T08:11:26.5363675Z =========================== short test summary info ============================
2026-06-03T08:11:26.5364350Z ERROR tests/test_rgp13_runtime_proof_pack_summary.py
```

```text
2026-06-03T08:11:20.9615246Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-03T08:11:20.9615591Z ##[endgroup]
2026-06-03T08:11:26.5351675Z 
2026-06-03T08:11:26.5352477Z ==================================== ERRORS ====================================
2026-06-03T08:11:26.5354896Z _______ ERROR collecting tests/test_rgp13_runtime_proof_pack_summary.py ________
2026-06-03T08:11:26.5356384Z ImportError while importing test module '/home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_rgp13_runtime_proof_pack_summary.py'.
2026-06-03T08:11:26.5357868Z Hint: make sure your test modules/packages have valid Python names.
2026-06-03T08:11:26.5358494Z Traceback:
2026-06-03T08:11:26.5359184Z /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/importlib/__init__.py:126: in import_module
2026-06-03T08:11:26.5360119Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-06-03T08:11:26.5360846Z tests/test_rgp13_runtime_proof_pack_summary.py:3: in <module>
2026-06-03T08:11:26.5361683Z     from src.runtime.runtime_proof_pack_summary import build_runtime_proof_pack_summary
2026-06-03T08:11:26.5362648Z E   ModuleNotFoundError: No module named 'src.runtime.runtime_proof_pack_summary'
2026-06-03T08:11:26.5363675Z =========================== short test summary info ============================
2026-06-03T08:11:26.5364350Z ERROR tests/test_rgp13_runtime_proof_pack_summary.py
2026-06-03T08:11:26.5365032Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
```

```text
2026-06-03T08:11:20.9615591Z ##[endgroup]
2026-06-03T08:11:26.5351675Z 
2026-06-03T08:11:26.5352477Z ==================================== ERRORS ====================================
2026-06-03T08:11:26.5354896Z _______ ERROR collecting tests/test_rgp13_runtime_proof_pack_summary.py ________
2026-06-03T08:11:26.5356384Z ImportError while importing test module '/home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_rgp13_runtime_proof_pack_summary.py'.
2026-06-03T08:11:26.5357868Z Hint: make sure your test modules/packages have valid Python names.
2026-06-03T08:11:26.5358494Z Traceback:
2026-06-03T08:11:26.5359184Z /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/importlib/__init__.py:126: in import_module
2026-06-03T08:11:26.5360119Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-06-03T08:11:26.5360846Z tests/test_rgp13_runtime_proof_pack_summary.py:3: in <module>
2026-06-03T08:11:26.5361683Z     from src.runtime.runtime_proof_pack_summary import build_runtime_proof_pack_summary
2026-06-03T08:11:26.5362648Z E   ModuleNotFoundError: No module named 'src.runtime.runtime_proof_pack_summary'
2026-06-03T08:11:26.5363675Z =========================== short test summary info ============================
2026-06-03T08:11:26.5364350Z ERROR tests/test_rgp13_runtime_proof_pack_summary.py
2026-06-03T08:11:26.5365032Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-06-03T08:11:26.5365984Z 1 error in 4.94s
```

```text
2026-06-03T08:11:26.5352477Z ==================================== ERRORS ====================================
2026-06-03T08:11:26.5354896Z _______ ERROR collecting tests/test_rgp13_runtime_proof_pack_summary.py ________
2026-06-03T08:11:26.5356384Z ImportError while importing test module '/home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_rgp13_runtime_proof_pack_summary.py'.
2026-06-03T08:11:26.5357868Z Hint: make sure your test modules/packages have valid Python names.
2026-06-03T08:11:26.5358494Z Traceback:
2026-06-03T08:11:26.5359184Z /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/importlib/__init__.py:126: in import_module
2026-06-03T08:11:26.5360119Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-06-03T08:11:26.5360846Z tests/test_rgp13_runtime_proof_pack_summary.py:3: in <module>
2026-06-03T08:11:26.5361683Z     from src.runtime.runtime_proof_pack_summary import build_runtime_proof_pack_summary
2026-06-03T08:11:26.5362648Z E   ModuleNotFoundError: No module named 'src.runtime.runtime_proof_pack_summary'
2026-06-03T08:11:26.5363675Z =========================== short test summary info ============================
2026-06-03T08:11:26.5364350Z ERROR tests/test_rgp13_runtime_proof_pack_summary.py
2026-06-03T08:11:26.5365032Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-06-03T08:11:26.5365984Z 1 error in 4.94s
2026-06-03T08:11:26.7150564Z ##[error]Process completed with exit code 2.
2026-06-03T08:11:26.7264927Z Post job cleanup.
```

```text
2026-06-03T08:11:26.5359184Z /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/importlib/__init__.py:126: in import_module
2026-06-03T08:11:26.5360119Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-06-03T08:11:26.5360846Z tests/test_rgp13_runtime_proof_pack_summary.py:3: in <module>
2026-06-03T08:11:26.5361683Z     from src.runtime.runtime_proof_pack_summary import build_runtime_proof_pack_summary
2026-06-03T08:11:26.5362648Z E   ModuleNotFoundError: No module named 'src.runtime.runtime_proof_pack_summary'
2026-06-03T08:11:26.5363675Z =========================== short test summary info ============================
2026-06-03T08:11:26.5364350Z ERROR tests/test_rgp13_runtime_proof_pack_summary.py
2026-06-03T08:11:26.5365032Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-06-03T08:11:26.5365984Z 1 error in 4.94s
2026-06-03T08:11:26.7150564Z ##[error]Process completed with exit code 2.
2026-06-03T08:11:26.7264927Z Post job cleanup.
2026-06-03T08:11:26.8225966Z [command]/usr/bin/git version
2026-06-03T08:11:26.8261488Z git version 2.54.0
2026-06-03T08:11:26.8304177Z Temporarily overriding HOME='/home/runner/work/_temp/f0383769-5595-4677-ac9d-a57362d638fd' before making global git config changes
2026-06-03T08:11:26.8305603Z Adding repository directory to the temporary git global config as a safe directory
2026-06-03T08:11:26.8309973Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
```

```text
2026-06-03T08:11:26.5360846Z tests/test_rgp13_runtime_proof_pack_summary.py:3: in <module>
2026-06-03T08:11:26.5361683Z     from src.runtime.runtime_proof_pack_summary import build_runtime_proof_pack_summary
2026-06-03T08:11:26.5362648Z E   ModuleNotFoundError: No module named 'src.runtime.runtime_proof_pack_summary'
2026-06-03T08:11:26.5363675Z =========================== short test summary info ============================
2026-06-03T08:11:26.5364350Z ERROR tests/test_rgp13_runtime_proof_pack_summary.py
2026-06-03T08:11:26.5365032Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-06-03T08:11:26.5365984Z 1 error in 4.94s
2026-06-03T08:11:26.7150564Z ##[error]Process completed with exit code 2.
2026-06-03T08:11:26.7264927Z Post job cleanup.
2026-06-03T08:11:26.8225966Z [command]/usr/bin/git version
2026-06-03T08:11:26.8261488Z git version 2.54.0
2026-06-03T08:11:26.8304177Z Temporarily overriding HOME='/home/runner/work/_temp/f0383769-5595-4677-ac9d-a57362d638fd' before making global git config changes
2026-06-03T08:11:26.8305603Z Adding repository directory to the temporary git global config as a safe directory
2026-06-03T08:11:26.8309973Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-06-03T08:11:26.8346066Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-06-03T08:11:26.8377813Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
```

```text
2026-06-03T08:11:26.5363675Z =========================== short test summary info ============================
2026-06-03T08:11:26.5364350Z ERROR tests/test_rgp13_runtime_proof_pack_summary.py
2026-06-03T08:11:26.5365032Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-06-03T08:11:26.5365984Z 1 error in 4.94s
2026-06-03T08:11:26.7150564Z ##[error]Process completed with exit code 2.
2026-06-03T08:11:26.7264927Z Post job cleanup.
2026-06-03T08:11:26.8225966Z [command]/usr/bin/git version
2026-06-03T08:11:26.8261488Z git version 2.54.0
2026-06-03T08:11:26.8304177Z Temporarily overriding HOME='/home/runner/work/_temp/f0383769-5595-4677-ac9d-a57362d638fd' before making global git config changes
2026-06-03T08:11:26.8305603Z Adding repository directory to the temporary git global config as a safe directory
2026-06-03T08:11:26.8309973Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-06-03T08:11:26.8346066Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-06-03T08:11:26.8377813Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-06-03T08:11:26.8598636Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-06-03T08:11:26.8622069Z http.https://github.com/.extraheader
2026-06-03T08:11:26.8635592Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

## CI

- Run ID: `26872198899`
- Branch: `main`
- Commit: `d00e7a897931`
- Title: Add RGP13 runtime proof pack summary guard tests
- Created: 2026-06-03T08:10:59Z
- Updated: 2026-06-03T08:11:51Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26872198899

### Failed job: Pytest

- Job ID: `79250069966`
- Started: 2026-06-03T08:11:02Z
- Completed: 2026-06-03T08:11:50Z
- Failed steps: 52. Full regression suite residual tests

#### Error context

```text
2026-06-03T08:11:43.4006304Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-03T08:11:43.4006632Z   POLYGON_API_KEY: test-key
2026-06-03T08:11:43.4006851Z ##[endgroup]
2026-06-03T08:11:47.4757296Z 
2026-06-03T08:11:47.4757849Z ==================================== ERRORS ====================================
2026-06-03T08:11:47.4758605Z _______ ERROR collecting tests/test_rgp13_runtime_proof_pack_summary.py ________
2026-06-03T08:11:47.4760021Z ImportError while importing test module '/home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_rgp13_runtime_proof_pack_summary.py'.
2026-06-03T08:11:47.4761379Z Hint: make sure your test modules/packages have valid Python names.
2026-06-03T08:11:47.4762010Z Traceback:
2026-06-03T08:11:47.4762635Z /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/importlib/__init__.py:126: in import_module
2026-06-03T08:11:47.4763649Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-06-03T08:11:47.4764156Z tests/test_rgp13_runtime_proof_pack_summary.py:3: in <module>
2026-06-03T08:11:47.4764737Z     from src.runtime.runtime_proof_pack_summary import build_runtime_proof_pack_summary
2026-06-03T08:11:47.4765418Z E   ModuleNotFoundError: No module named 'src.runtime.runtime_proof_pack_summary'
2026-06-03T08:11:47.4765992Z =========================== short test summary info ============================
2026-06-03T08:11:47.4766444Z ERROR tests/test_rgp13_runtime_proof_pack_summary.py
```

```text
2026-06-03T08:11:43.4006632Z   POLYGON_API_KEY: test-key
2026-06-03T08:11:43.4006851Z ##[endgroup]
2026-06-03T08:11:47.4757296Z 
2026-06-03T08:11:47.4757849Z ==================================== ERRORS ====================================
2026-06-03T08:11:47.4758605Z _______ ERROR collecting tests/test_rgp13_runtime_proof_pack_summary.py ________
2026-06-03T08:11:47.4760021Z ImportError while importing test module '/home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_rgp13_runtime_proof_pack_summary.py'.
2026-06-03T08:11:47.4761379Z Hint: make sure your test modules/packages have valid Python names.
2026-06-03T08:11:47.4762010Z Traceback:
2026-06-03T08:11:47.4762635Z /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/importlib/__init__.py:126: in import_module
2026-06-03T08:11:47.4763649Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-06-03T08:11:47.4764156Z tests/test_rgp13_runtime_proof_pack_summary.py:3: in <module>
2026-06-03T08:11:47.4764737Z     from src.runtime.runtime_proof_pack_summary import build_runtime_proof_pack_summary
2026-06-03T08:11:47.4765418Z E   ModuleNotFoundError: No module named 'src.runtime.runtime_proof_pack_summary'
2026-06-03T08:11:47.4765992Z =========================== short test summary info ============================
2026-06-03T08:11:47.4766444Z ERROR tests/test_rgp13_runtime_proof_pack_summary.py
2026-06-03T08:11:47.4766905Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
```

```text
2026-06-03T08:11:43.4006851Z ##[endgroup]
2026-06-03T08:11:47.4757296Z 
2026-06-03T08:11:47.4757849Z ==================================== ERRORS ====================================
2026-06-03T08:11:47.4758605Z _______ ERROR collecting tests/test_rgp13_runtime_proof_pack_summary.py ________
2026-06-03T08:11:47.4760021Z ImportError while importing test module '/home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_rgp13_runtime_proof_pack_summary.py'.
2026-06-03T08:11:47.4761379Z Hint: make sure your test modules/packages have valid Python names.
2026-06-03T08:11:47.4762010Z Traceback:
2026-06-03T08:11:47.4762635Z /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/importlib/__init__.py:126: in import_module
2026-06-03T08:11:47.4763649Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-06-03T08:11:47.4764156Z tests/test_rgp13_runtime_proof_pack_summary.py:3: in <module>
2026-06-03T08:11:47.4764737Z     from src.runtime.runtime_proof_pack_summary import build_runtime_proof_pack_summary
2026-06-03T08:11:47.4765418Z E   ModuleNotFoundError: No module named 'src.runtime.runtime_proof_pack_summary'
2026-06-03T08:11:47.4765992Z =========================== short test summary info ============================
2026-06-03T08:11:47.4766444Z ERROR tests/test_rgp13_runtime_proof_pack_summary.py
2026-06-03T08:11:47.4766905Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-06-03T08:11:47.4767340Z 1 deselected, 1 error in 3.87s
```

```text
2026-06-03T08:11:47.4757849Z ==================================== ERRORS ====================================
2026-06-03T08:11:47.4758605Z _______ ERROR collecting tests/test_rgp13_runtime_proof_pack_summary.py ________
2026-06-03T08:11:47.4760021Z ImportError while importing test module '/home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_rgp13_runtime_proof_pack_summary.py'.
2026-06-03T08:11:47.4761379Z Hint: make sure your test modules/packages have valid Python names.
2026-06-03T08:11:47.4762010Z Traceback:
2026-06-03T08:11:47.4762635Z /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/importlib/__init__.py:126: in import_module
2026-06-03T08:11:47.4763649Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-06-03T08:11:47.4764156Z tests/test_rgp13_runtime_proof_pack_summary.py:3: in <module>
2026-06-03T08:11:47.4764737Z     from src.runtime.runtime_proof_pack_summary import build_runtime_proof_pack_summary
2026-06-03T08:11:47.4765418Z E   ModuleNotFoundError: No module named 'src.runtime.runtime_proof_pack_summary'
2026-06-03T08:11:47.4765992Z =========================== short test summary info ============================
2026-06-03T08:11:47.4766444Z ERROR tests/test_rgp13_runtime_proof_pack_summary.py
2026-06-03T08:11:47.4766905Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-06-03T08:11:47.4767340Z 1 deselected, 1 error in 3.87s
2026-06-03T08:11:47.6568161Z ##[error]Process completed with exit code 2.
2026-06-03T08:11:47.6676389Z Post job cleanup.
```

```text
2026-06-03T08:11:47.4762635Z /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/importlib/__init__.py:126: in import_module
2026-06-03T08:11:47.4763649Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-06-03T08:11:47.4764156Z tests/test_rgp13_runtime_proof_pack_summary.py:3: in <module>
2026-06-03T08:11:47.4764737Z     from src.runtime.runtime_proof_pack_summary import build_runtime_proof_pack_summary
2026-06-03T08:11:47.4765418Z E   ModuleNotFoundError: No module named 'src.runtime.runtime_proof_pack_summary'
2026-06-03T08:11:47.4765992Z =========================== short test summary info ============================
2026-06-03T08:11:47.4766444Z ERROR tests/test_rgp13_runtime_proof_pack_summary.py
2026-06-03T08:11:47.4766905Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-06-03T08:11:47.4767340Z 1 deselected, 1 error in 3.87s
2026-06-03T08:11:47.6568161Z ##[error]Process completed with exit code 2.
2026-06-03T08:11:47.6676389Z Post job cleanup.
2026-06-03T08:11:47.7692623Z [command]/usr/bin/git version
2026-06-03T08:11:47.7728088Z git version 2.54.0
2026-06-03T08:11:47.7771805Z Temporarily overriding HOME='/home/runner/work/_temp/e1ffda73-0d7e-45b2-b50c-60820497bc79' before making global git config changes
2026-06-03T08:11:47.7773548Z Adding repository directory to the temporary git global config as a safe directory
2026-06-03T08:11:47.7778345Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
```

```text
2026-06-03T08:11:47.4764156Z tests/test_rgp13_runtime_proof_pack_summary.py:3: in <module>
2026-06-03T08:11:47.4764737Z     from src.runtime.runtime_proof_pack_summary import build_runtime_proof_pack_summary
2026-06-03T08:11:47.4765418Z E   ModuleNotFoundError: No module named 'src.runtime.runtime_proof_pack_summary'
2026-06-03T08:11:47.4765992Z =========================== short test summary info ============================
2026-06-03T08:11:47.4766444Z ERROR tests/test_rgp13_runtime_proof_pack_summary.py
2026-06-03T08:11:47.4766905Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-06-03T08:11:47.4767340Z 1 deselected, 1 error in 3.87s
2026-06-03T08:11:47.6568161Z ##[error]Process completed with exit code 2.
2026-06-03T08:11:47.6676389Z Post job cleanup.
2026-06-03T08:11:47.7692623Z [command]/usr/bin/git version
2026-06-03T08:11:47.7728088Z git version 2.54.0
2026-06-03T08:11:47.7771805Z Temporarily overriding HOME='/home/runner/work/_temp/e1ffda73-0d7e-45b2-b50c-60820497bc79' before making global git config changes
2026-06-03T08:11:47.7773548Z Adding repository directory to the temporary git global config as a safe directory
2026-06-03T08:11:47.7778345Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-06-03T08:11:47.7813429Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-06-03T08:11:47.7846214Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
```

```text
2026-06-03T08:11:47.4765992Z =========================== short test summary info ============================
2026-06-03T08:11:47.4766444Z ERROR tests/test_rgp13_runtime_proof_pack_summary.py
2026-06-03T08:11:47.4766905Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-06-03T08:11:47.4767340Z 1 deselected, 1 error in 3.87s
2026-06-03T08:11:47.6568161Z ##[error]Process completed with exit code 2.
2026-06-03T08:11:47.6676389Z Post job cleanup.
2026-06-03T08:11:47.7692623Z [command]/usr/bin/git version
2026-06-03T08:11:47.7728088Z git version 2.54.0
2026-06-03T08:11:47.7771805Z Temporarily overriding HOME='/home/runner/work/_temp/e1ffda73-0d7e-45b2-b50c-60820497bc79' before making global git config changes
2026-06-03T08:11:47.7773548Z Adding repository directory to the temporary git global config as a safe directory
2026-06-03T08:11:47.7778345Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-06-03T08:11:47.7813429Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-06-03T08:11:47.7846214Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-06-03T08:11:47.8073106Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-06-03T08:11:47.8097305Z http.https://github.com/.extraheader
2026-06-03T08:11:47.8110591Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

## Report Quality Validation

- Run ID: `26872198890`
- Branch: `main`
- Commit: `d00e7a897931`
- Title: Add RGP13 runtime proof pack summary guard tests
- Created: 2026-06-03T08:10:58Z
- Updated: 2026-06-03T08:11:41Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26872198890

### Failed job: validate-reports (postmarket)

- Job ID: `79250070467`
- Started: 2026-06-03T08:11:01Z
- Completed: 2026-06-03T08:11:40Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-03T08:11:22.7118904Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-03T08:11:22.7119293Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-03T08:11:22.7119731Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-03T08:11:22.7120066Z ##[endgroup]
2026-06-03T08:11:37.7996397Z Traceback (most recent call last):
2026-06-03T08:11:37.7998643Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-30/2026-06-03?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-03T08:11:37.8001681Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-30/2026-06-03?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-03T08:11:37.8003973Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-30/2026-06-03?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-03T08:11:37.8005475Z WARNING: scanner metric loading failed: ModuleNotFoundError: No module named 'config'
2026-06-03T08:11:37.8006181Z WARNING: scanner_metrics_missing:MSFT
2026-06-03T08:11:37.8006644Z WARNING: scanner_metrics_missing:NVDA
2026-06-03T08:11:37.8007084Z WARNING: scanner_metrics_missing:META
2026-06-03T08:11:37.8007535Z WARNING: scanner_metrics_missing:AAPL
2026-06-03T08:11:37.8007954Z WARNING: scanner_metrics_missing:MU
2026-06-03T08:11:37.8008382Z WARNING: scanner_metrics_missing:QQQ
2026-06-03T08:11:37.8008822Z WARNING: scanner_metrics_missing:GLD
```

```text
2026-06-03T08:11:37.7996397Z Traceback (most recent call last):
2026-06-03T08:11:37.7998643Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-30/2026-06-03?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-03T08:11:37.8001681Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-30/2026-06-03?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-03T08:11:37.8003973Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-30/2026-06-03?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-03T08:11:37.8005475Z WARNING: scanner metric loading failed: ModuleNotFoundError: No module named 'config'
2026-06-03T08:11:37.8006181Z WARNING: scanner_metrics_missing:MSFT
2026-06-03T08:11:37.8006644Z WARNING: scanner_metrics_missing:NVDA
2026-06-03T08:11:37.8007084Z WARNING: scanner_metrics_missing:META
2026-06-03T08:11:37.8007535Z WARNING: scanner_metrics_missing:AAPL
2026-06-03T08:11:37.8007954Z WARNING: scanner_metrics_missing:MU
2026-06-03T08:11:37.8008382Z WARNING: scanner_metrics_missing:QQQ
2026-06-03T08:11:37.8008822Z WARNING: scanner_metrics_missing:GLD
2026-06-03T08:11:37.8009243Z WARNING: scanner_metrics_missing:SLV
2026-06-03T08:11:37.8017692Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 247, in <module>
2026-06-03T08:11:37.8018781Z     raise SystemExit(main())
2026-06-03T08:11:37.8019184Z                      ^^^^^^
```

```text
2026-06-03T08:11:37.8024916Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-03T08:11:37.8026287Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-06-03T08:11:37.8027507Z     raise ReportOutputBoundaryError(
2026-06-03T08:11:37.8029070Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/postmarket-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-06-03T08:11:37.8870769Z ##[error]Process completed with exit code 1.
2026-06-03T08:11:37.8957648Z ##[group]Run actions/upload-artifact@v4
2026-06-03T08:11:37.8958007Z with:
2026-06-03T08:11:37.8958243Z   name: validated-postmarket-report
2026-06-03T08:11:37.8958555Z   path: reports/postmarket-report.md
2026-06-03T08:11:37.8958834Z   retention-days: 14
2026-06-03T08:11:37.8959066Z   if-no-files-found: warn
2026-06-03T08:11:37.8959308Z   compression-level: 6
2026-06-03T08:11:37.8959546Z   overwrite: false
2026-06-03T08:11:37.8959785Z   include-hidden-files: false
2026-06-03T08:11:37.8960035Z env:
2026-06-03T08:11:37.8960368Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (premarket)

- Job ID: `79250070489`
- Started: 2026-06-03T08:11:01Z
- Completed: 2026-06-03T08:11:35Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-03T08:11:17.1946812Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-03T08:11:17.1947206Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-03T08:11:17.1947644Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-03T08:11:17.1947983Z ##[endgroup]
2026-06-03T08:11:32.5687289Z Traceback (most recent call last):
2026-06-03T08:11:32.5694810Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 247, in <module>
2026-06-03T08:11:32.5696676Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-30/2026-06-03?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-03T08:11:32.5697631Z     raise SystemExit(main())
2026-06-03T08:11:32.5697893Z                      ^^^^^^
2026-06-03T08:11:32.5698540Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 236, in main
2026-06-03T08:11:32.5699336Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-03T08:11:32.5699802Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-03T08:11:32.5700543Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 68, in write_report_text_guarded
2026-06-03T08:11:32.5701340Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-03T08:11:32.5702185Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-06-03T08:11:32.5702906Z     raise ReportOutputBoundaryError(
```

```text
2026-06-03T08:11:32.5702906Z     raise ReportOutputBoundaryError(
2026-06-03T08:11:32.5703841Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/premarket-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-06-03T08:11:32.5705407Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-30/2026-06-03?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-03T08:11:32.5707070Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-30/2026-06-03?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-03T08:11:32.5707970Z WARNING: scanner metric loading failed: ModuleNotFoundError: No module named 'config'
2026-06-03T08:11:32.5708415Z WARNING: scanner_metrics_missing:MSFT
2026-06-03T08:11:32.5708710Z WARNING: scanner_metrics_missing:NVDA
2026-06-03T08:11:32.5708982Z WARNING: scanner_metrics_missing:META
2026-06-03T08:11:32.5709252Z WARNING: scanner_metrics_missing:AAPL
2026-06-03T08:11:32.5709533Z WARNING: scanner_metrics_missing:MU
2026-06-03T08:11:32.5710137Z WARNING: scanner_metrics_missing:QQQ
2026-06-03T08:11:32.5710413Z WARNING: scanner_metrics_missing:GLD
2026-06-03T08:11:32.5710682Z WARNING: scanner_metrics_missing:SLV
2026-06-03T08:11:32.6382469Z ##[error]Process completed with exit code 1.
2026-06-03T08:11:32.6468062Z ##[group]Run actions/upload-artifact@v4
2026-06-03T08:11:32.6468366Z with:
```

```text
2026-06-03T08:11:32.5709533Z WARNING: scanner_metrics_missing:MU
2026-06-03T08:11:32.5710137Z WARNING: scanner_metrics_missing:QQQ
2026-06-03T08:11:32.5710413Z WARNING: scanner_metrics_missing:GLD
2026-06-03T08:11:32.5710682Z WARNING: scanner_metrics_missing:SLV
2026-06-03T08:11:32.6382469Z ##[error]Process completed with exit code 1.
2026-06-03T08:11:32.6468062Z ##[group]Run actions/upload-artifact@v4
2026-06-03T08:11:32.6468366Z with:
2026-06-03T08:11:32.6468597Z   name: validated-premarket-report
2026-06-03T08:11:32.6468893Z   path: reports/premarket-report.md
2026-06-03T08:11:32.6469164Z   retention-days: 14
2026-06-03T08:11:32.6469401Z   if-no-files-found: warn
2026-06-03T08:11:32.6469648Z   compression-level: 6
2026-06-03T08:11:32.6469893Z   overwrite: false
2026-06-03T08:11:32.6470133Z   include-hidden-files: false
2026-06-03T08:11:32.6470400Z env:
2026-06-03T08:11:32.6470729Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (weekly)

- Job ID: `79250070561`
- Started: 2026-06-03T08:11:02Z
- Completed: 2026-06-03T08:11:21Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-03T08:11:17.6752740Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-03T08:11:17.6753114Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-03T08:11:17.6753543Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-03T08:11:17.6753858Z ##[endgroup]
2026-06-03T08:11:17.9409493Z Traceback (most recent call last):
2026-06-03T08:11:17.9417537Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 247, in <module>
2026-06-03T08:11:17.9418556Z     raise SystemExit(main())
2026-06-03T08:11:17.9419101Z                      ^^^^^^
2026-06-03T08:11:17.9430198Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 236, in main
2026-06-03T08:11:17.9431355Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-03T08:11:17.9432056Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-03T08:11:17.9433233Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 68, in write_report_text_guarded
2026-06-03T08:11:17.9434386Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-03T08:11:17.9435645Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-06-03T08:11:17.9436786Z     raise ReportOutputBoundaryError(
2026-06-03T08:11:17.9438147Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
```

```text
2026-06-03T08:11:17.9434386Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-03T08:11:17.9435645Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-06-03T08:11:17.9436786Z     raise ReportOutputBoundaryError(
2026-06-03T08:11:17.9438147Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-06-03T08:11:17.9635006Z ##[error]Process completed with exit code 1.
2026-06-03T08:11:17.9714515Z ##[group]Run actions/upload-artifact@v4
2026-06-03T08:11:17.9714812Z with:
2026-06-03T08:11:17.9715020Z   name: validated-weekly-report
2026-06-03T08:11:17.9715282Z   path: reports/weekly-report.md
2026-06-03T08:11:17.9715534Z   retention-days: 14
2026-06-03T08:11:17.9715749Z   if-no-files-found: warn
2026-06-03T08:11:17.9715977Z   compression-level: 6
2026-06-03T08:11:17.9716196Z   overwrite: false
2026-06-03T08:11:17.9716405Z   include-hidden-files: false
2026-06-03T08:11:17.9716631Z env:
2026-06-03T08:11:17.9716956Z   POLYGON_API_KEY: ***
```

## Decision Engine Tests

- Run ID: `26871836198`
- Branch: `main`
- Commit: `04aac221b382`
- Title: Document PO14 CI green status in roadmap
- Created: 2026-06-03T08:03:05Z
- Updated: 2026-06-03T08:03:39Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26871836198

### Failed job: tests

- Job ID: `79248820485`
- Started: 2026-06-03T08:03:08Z
- Completed: 2026-06-03T08:03:38Z
- Failed steps: 5. Run pytest

#### Error context

```text
2026-06-03T08:03:36.1689968Z ........................................................................ [ 87%]
2026-06-03T08:03:36.3078447Z ........................................................................ [ 92%]
2026-06-03T08:03:36.3992282Z ........................................................................ [ 96%]
2026-06-03T08:03:36.4650792Z .................................................                        [100%]
2026-06-03T08:03:36.4651591Z =================================== FAILURES ===================================
2026-06-03T08:03:36.4652260Z _________ TestDataPersistence.test_decision_log_path_not_in_gitignore __________
2026-06-03T08:03:36.4652746Z 
2026-06-03T08:03:36.4653281Z self = <test_priority_fixes.TestDataPersistence object at 0x7fd5e7ae1810>
2026-06-03T08:03:36.4653875Z 
2026-06-03T08:03:36.4654010Z     def test_decision_log_path_not_in_gitignore(self):
2026-06-03T08:03:36.4654321Z         gitignore = Path(".gitignore")
2026-06-03T08:03:36.4654596Z         if not gitignore.exists():
2026-06-03T08:03:36.4654836Z             return
2026-06-03T08:03:36.4655045Z         content = gitignore.read_text()
2026-06-03T08:03:36.4655306Z         # data/ should NOT be in gitignore
2026-06-03T08:03:36.4656017Z >       assert "data/" not in content, (
```

```text
2026-06-03T08:03:36.4655306Z         # data/ should NOT be in gitignore
2026-06-03T08:03:36.4656017Z >       assert "data/" not in content, (
2026-06-03T08:03:36.4656728Z             "data/ is in .gitignore â decision log will be lost on every run"
2026-06-03T08:03:36.4657059Z         )
2026-06-03T08:03:36.4657430Z E       AssertionError: data/ is in .gitignore â decision log will be lost on every run
2026-06-03T08:03:36.4657867Z E       assert 'data/' not in '# Python\n_...\n.vscode/\n'
2026-06-03T08:03:36.4658151Z E         
2026-06-03T08:03:36.4658343Z E         'data/' is contained here:
2026-06-03T08:03:36.4658588Z E           e/
2026-06-03T08:03:36.4658772Z E           cache/
2026-06-03T08:03:36.4658961Z E           data/raw/
2026-06-03T08:03:36.4659167Z E           data/live/
2026-06-03T08:03:36.4659373Z E           data/private/
2026-06-03T08:03:36.4659593Z E           data/vendor/
2026-06-03T08:03:36.4659803Z E           evidence/
2026-06-03T08:03:36.4660002Z E           lockbox/
```

```text
2026-06-03T08:03:36.4667635Z E           .DS_Store
2026-06-03T08:03:36.4667821Z E           .idea/
2026-06-03T08:03:36.4668002Z E           .vscode/
2026-06-03T08:03:36.4668114Z 
2026-06-03T08:03:36.4668238Z tests/test_priority_fixes.py:372: AssertionError
2026-06-03T08:03:36.4668588Z =============================== warnings summary ===============================
2026-06-03T08:03:36.4669428Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbol_writes_csv_and_metadata
2026-06-03T08:03:36.4670066Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbol_merges_without_duplicates
2026-06-03T08:03:36.4670669Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbols_batch_counts_results
2026-06-03T08:03:36.4671243Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbols_batch_counts_results
2026-06-03T08:03:36.4672982Z   /home/runner/work/institutional-trading-engine/institutional-trading-engine/src/historical/polygon_ingestion.py:125: FutureWarning: The behavior of DataFrame concatenation with empty or all-NA entries is deprecated. In a future version, this will no longer exclude empty or all-NA columns when determining the result dtypes. To retain the old behavior, exclude the relevant entries before the concat operation.
2026-06-03T08:03:36.4674460Z     combined = pd.concat([existing, df], ignore_index=True)
2026-06-03T08:03:36.4674769Z 
2026-06-03T08:03:36.4674985Z -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2026-06-03T08:03:36.4675531Z =========================== short test summary info ============================
2026-06-03T08:03:36.4676469Z FAILED tests/test_priority_fixes.py::TestDataPersistence::test_decision_log_path_not_in_gitignore - AssertionError: data/ is in .gitignore â decision log will be lost on every run
```

```text
2026-06-03T08:03:36.4674460Z     combined = pd.concat([existing, df], ignore_index=True)
2026-06-03T08:03:36.4674769Z 
2026-06-03T08:03:36.4674985Z -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2026-06-03T08:03:36.4675531Z =========================== short test summary info ============================
2026-06-03T08:03:36.4676469Z FAILED tests/test_priority_fixes.py::TestDataPersistence::test_decision_log_path_not_in_gitignore - AssertionError: data/ is in .gitignore â decision log will be lost on every run
2026-06-03T08:03:36.4677190Z assert 'data/' not in '# Python\n_...\n.vscode/\n'
2026-06-03T08:03:36.4677470Z   
2026-06-03T08:03:36.4677662Z   'data/' is contained here:
2026-06-03T08:03:36.4677885Z     e/
2026-06-03T08:03:36.4678060Z     cache/
2026-06-03T08:03:36.4678256Z     data/raw/
2026-06-03T08:03:36.4678470Z     data/live/
2026-06-03T08:03:36.4678661Z     data/private/
2026-06-03T08:03:36.4678853Z     data/vendor/
2026-06-03T08:03:36.4679042Z     evidence/
2026-06-03T08:03:36.4679217Z     lockbox/
```

```text
2026-06-03T08:03:36.4686160Z     .DS_Store
2026-06-03T08:03:36.4686335Z     .idea/
2026-06-03T08:03:36.4686513Z     .vscode/
2026-06-03T08:03:36.4686751Z 1 failed, 1559 passed, 1 skipped, 4 warnings in 10.92s
2026-06-03T08:03:36.6871488Z ##[error]Process completed with exit code 1.
2026-06-03T08:03:36.6979398Z Post job cleanup.
2026-06-03T08:03:36.7895173Z [command]/usr/bin/git version
2026-06-03T08:03:36.7928537Z git version 2.54.0
2026-06-03T08:03:36.7967777Z Temporarily overriding HOME='/home/runner/work/_temp/35f7eae4-ac2a-4176-8e4f-5504c3c6d3ef' before making global git config changes
2026-06-03T08:03:36.7969018Z Adding repository directory to the temporary git global config as a safe directory
2026-06-03T08:03:36.7981033Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-06-03T08:03:36.8011389Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-06-03T08:03:36.8038689Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-06-03T08:03:36.8217910Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-06-03T08:03:36.8238311Z http.https://github.com/.extraheader
2026-06-03T08:03:36.8249279Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

## Report Quality Validation

- Run ID: `26871836069`
- Branch: `main`
- Commit: `04aac221b382`
- Title: Document PO14 CI green status in roadmap
- Created: 2026-06-03T08:03:05Z
- Updated: 2026-06-03T08:03:46Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26871836069

### Failed job: validate-reports (weekly)

- Job ID: `79248820599`
- Started: 2026-06-03T08:03:08Z
- Completed: 2026-06-03T08:03:27Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-03T08:03:25.2986097Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-03T08:03:25.2986509Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-03T08:03:25.2986941Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-03T08:03:25.2987449Z ##[endgroup]
2026-06-03T08:03:25.5943676Z Traceback (most recent call last):
2026-06-03T08:03:25.5951610Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 247, in <module>
2026-06-03T08:03:25.5952574Z     raise SystemExit(main())
2026-06-03T08:03:25.5952858Z                      ^^^^^^
2026-06-03T08:03:25.5953515Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 236, in main
2026-06-03T08:03:25.5954276Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-03T08:03:25.5954735Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-03T08:03:25.5955537Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 68, in write_report_text_guarded
2026-06-03T08:03:25.5956313Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-03T08:03:25.5957526Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-06-03T08:03:25.5958609Z     raise ReportOutputBoundaryError(
2026-06-03T08:03:25.5959548Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
```

```text
2026-06-03T08:03:25.5956313Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-03T08:03:25.5957526Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-06-03T08:03:25.5958609Z     raise ReportOutputBoundaryError(
2026-06-03T08:03:25.5959548Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-06-03T08:03:25.6177409Z ##[error]Process completed with exit code 1.
2026-06-03T08:03:25.6263403Z ##[group]Run actions/upload-artifact@v4
2026-06-03T08:03:25.6263730Z with:
2026-06-03T08:03:25.6263964Z   name: validated-weekly-report
2026-06-03T08:03:25.6264254Z   path: reports/weekly-report.md
2026-06-03T08:03:25.6264528Z   retention-days: 14
2026-06-03T08:03:25.6264772Z   if-no-files-found: warn
2026-06-03T08:03:25.6265030Z   compression-level: 6
2026-06-03T08:03:25.6265282Z   overwrite: false
2026-06-03T08:03:25.6265521Z   include-hidden-files: false
2026-06-03T08:03:25.6265775Z env:
2026-06-03T08:03:25.6266140Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (postmarket)

- Job ID: `79248820600`
- Started: 2026-06-03T08:03:09Z
- Completed: 2026-06-03T08:03:45Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-03T08:03:26.1758873Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-03T08:03:26.1759289Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-03T08:03:26.1759750Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-03T08:03:26.1760096Z ##[endgroup]
2026-06-03T08:03:42.5840140Z Traceback (most recent call last):
2026-06-03T08:03:42.5848363Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 247, in <module>
2026-06-03T08:03:42.5850022Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-30/2026-06-03?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-03T08:03:42.5851273Z     raise SystemExit(main())
2026-06-03T08:03:42.5851545Z                      ^^^^^^
2026-06-03T08:03:42.5852198Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 236, in main
2026-06-03T08:03:42.5852980Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-03T08:03:42.5853442Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-03T08:03:42.5854196Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 68, in write_report_text_guarded
2026-06-03T08:03:42.5854992Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-03T08:03:42.5855829Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-06-03T08:03:42.5856548Z     raise ReportOutputBoundaryError(
```

```text
2026-06-03T08:03:42.5856548Z     raise ReportOutputBoundaryError(
2026-06-03T08:03:42.5857502Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/postmarket-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-06-03T08:03:42.5859119Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-30/2026-06-03?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-03T08:03:42.5860684Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-30/2026-06-03?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-03T08:03:42.5861609Z WARNING: scanner metric loading failed: ModuleNotFoundError: No module named 'config'
2026-06-03T08:03:42.5862062Z WARNING: scanner_metrics_missing:MSFT
2026-06-03T08:03:42.5862364Z WARNING: scanner_metrics_missing:NVDA
2026-06-03T08:03:42.5862648Z WARNING: scanner_metrics_missing:META
2026-06-03T08:03:42.5862926Z WARNING: scanner_metrics_missing:AAPL
2026-06-03T08:03:42.5863219Z WARNING: scanner_metrics_missing:MU
2026-06-03T08:03:42.5863795Z WARNING: scanner_metrics_missing:QQQ
2026-06-03T08:03:42.5864101Z WARNING: scanner_metrics_missing:GLD
2026-06-03T08:03:42.5864382Z WARNING: scanner_metrics_missing:SLV
2026-06-03T08:03:42.6535410Z ##[error]Process completed with exit code 1.
2026-06-03T08:03:42.6621787Z ##[group]Run actions/upload-artifact@v4
2026-06-03T08:03:42.6622101Z with:
```

```text
2026-06-03T08:03:42.5863219Z WARNING: scanner_metrics_missing:MU
2026-06-03T08:03:42.5863795Z WARNING: scanner_metrics_missing:QQQ
2026-06-03T08:03:42.5864101Z WARNING: scanner_metrics_missing:GLD
2026-06-03T08:03:42.5864382Z WARNING: scanner_metrics_missing:SLV
2026-06-03T08:03:42.6535410Z ##[error]Process completed with exit code 1.
2026-06-03T08:03:42.6621787Z ##[group]Run actions/upload-artifact@v4
2026-06-03T08:03:42.6622101Z with:
2026-06-03T08:03:42.6622345Z   name: validated-postmarket-report
2026-06-03T08:03:42.6622663Z   path: reports/postmarket-report.md
2026-06-03T08:03:42.6622950Z   retention-days: 14
2026-06-03T08:03:42.6623190Z   if-no-files-found: warn
2026-06-03T08:03:42.6623441Z   compression-level: 6
2026-06-03T08:03:42.6623687Z   overwrite: false
2026-06-03T08:03:42.6623926Z   include-hidden-files: false
2026-06-03T08:03:42.6624221Z env:
2026-06-03T08:03:42.6624564Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (premarket)

- Job ID: `79248820653`
- Started: 2026-06-03T08:03:08Z
- Completed: 2026-06-03T08:03:44Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-03T08:03:26.4047175Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-03T08:03:26.4047577Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-03T08:03:26.4048001Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-03T08:03:26.4048345Z ##[endgroup]
2026-06-03T08:03:42.2279321Z Traceback (most recent call last):
2026-06-03T08:03:42.2280763Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-30/2026-06-03?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-03T08:03:42.2289648Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 247, in <module>
2026-06-03T08:03:42.2291767Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-30/2026-06-03?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-03T08:03:42.2293273Z     raise SystemExit(main())
2026-06-03T08:03:42.2293556Z                      ^^^^^^
2026-06-03T08:03:42.2294231Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 236, in main
2026-06-03T08:03:42.2295234Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-03T08:03:42.2295690Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-03T08:03:42.2296440Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 68, in write_report_text_guarded
2026-06-03T08:03:42.2297247Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-03T08:03:42.2298107Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
```

```text
2026-06-03T08:03:42.2298107Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-06-03T08:03:42.2298851Z     raise ReportOutputBoundaryError(
2026-06-03T08:03:42.2299799Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/premarket-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-06-03T08:03:42.2301354Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-30/2026-06-03?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-03T08:03:42.2302260Z WARNING: scanner metric loading failed: ModuleNotFoundError: No module named 'config'
2026-06-03T08:03:42.2302703Z WARNING: scanner_metrics_missing:MSFT
2026-06-03T08:03:42.2302995Z WARNING: scanner_metrics_missing:NVDA
2026-06-03T08:03:42.2303278Z WARNING: scanner_metrics_missing:META
2026-06-03T08:03:42.2303584Z WARNING: scanner_metrics_missing:AAPL
2026-06-03T08:03:42.2303865Z WARNING: scanner_metrics_missing:MU
2026-06-03T08:03:42.2304725Z WARNING: scanner_metrics_missing:QQQ
2026-06-03T08:03:42.2305010Z WARNING: scanner_metrics_missing:GLD
2026-06-03T08:03:42.2305285Z WARNING: scanner_metrics_missing:SLV
2026-06-03T08:03:42.3121920Z ##[error]Process completed with exit code 1.
2026-06-03T08:03:42.3207570Z ##[group]Run actions/upload-artifact@v4
2026-06-03T08:03:42.3207875Z with:
```

```text
2026-06-03T08:03:42.2303865Z WARNING: scanner_metrics_missing:MU
2026-06-03T08:03:42.2304725Z WARNING: scanner_metrics_missing:QQQ
2026-06-03T08:03:42.2305010Z WARNING: scanner_metrics_missing:GLD
2026-06-03T08:03:42.2305285Z WARNING: scanner_metrics_missing:SLV
2026-06-03T08:03:42.3121920Z ##[error]Process completed with exit code 1.
2026-06-03T08:03:42.3207570Z ##[group]Run actions/upload-artifact@v4
2026-06-03T08:03:42.3207875Z with:
2026-06-03T08:03:42.3208106Z   name: validated-premarket-report
2026-06-03T08:03:42.3208404Z   path: reports/premarket-report.md
2026-06-03T08:03:42.3208687Z   retention-days: 14
2026-06-03T08:03:42.3208926Z   if-no-files-found: warn
2026-06-03T08:03:42.3209174Z   compression-level: 6
2026-06-03T08:03:42.3209412Z   overwrite: false
2026-06-03T08:03:42.3209645Z   include-hidden-files: false
2026-06-03T08:03:42.3209895Z env:
2026-06-03T08:03:42.3210242Z   POLYGON_API_KEY: ***
```

## Decision Engine Tests

- Run ID: `26871635949`
- Branch: `main`
- Commit: `2597af623fcc`
- Title: Document PO14 forward evidence quality gate in changelog
- Created: 2026-06-03T07:59:00Z
- Updated: 2026-06-03T07:59:35Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26871635949

### Failed job: tests

- Job ID: `79248149453`
- Started: 2026-06-03T07:59:03Z
- Completed: 2026-06-03T07:59:34Z
- Failed steps: 5. Run pytest

#### Error context

```text
2026-06-03T07:59:31.6777612Z ........................................................................ [ 87%]
2026-06-03T07:59:31.8566029Z ........................................................................ [ 92%]
2026-06-03T07:59:31.9605034Z ........................................................................ [ 96%]
2026-06-03T07:59:32.0438846Z .................................................                        [100%]
2026-06-03T07:59:32.0439980Z =================================== FAILURES ===================================
2026-06-03T07:59:32.0441018Z _________ TestDataPersistence.test_decision_log_path_not_in_gitignore __________
2026-06-03T07:59:32.0441485Z 
2026-06-03T07:59:32.0441918Z self = <test_priority_fixes.TestDataPersistence object at 0x7f957e7ccfd0>
2026-06-03T07:59:32.0442963Z 
2026-06-03T07:59:32.0443255Z     def test_decision_log_path_not_in_gitignore(self):
2026-06-03T07:59:32.0443950Z         gitignore = Path(".gitignore")
2026-06-03T07:59:32.0444534Z         if not gitignore.exists():
2026-06-03T07:59:32.0445047Z             return
2026-06-03T07:59:32.0445492Z         content = gitignore.read_text()
2026-06-03T07:59:32.0445967Z         # data/ should NOT be in gitignore
2026-06-03T07:59:32.0446446Z >       assert "data/" not in content, (
```

```text
2026-06-03T07:59:32.0445967Z         # data/ should NOT be in gitignore
2026-06-03T07:59:32.0446446Z >       assert "data/" not in content, (
2026-06-03T07:59:32.0447543Z             "data/ is in .gitignore â decision log will be lost on every run"
2026-06-03T07:59:32.0447957Z         )
2026-06-03T07:59:32.0448725Z E       AssertionError: data/ is in .gitignore â decision log will be lost on every run
2026-06-03T07:59:32.0449269Z E       assert 'data/' not in '# Python\n_...\n.vscode/\n'
2026-06-03T07:59:32.0449601Z E         
2026-06-03T07:59:32.0449814Z E         'data/' is contained here:
2026-06-03T07:59:32.0450102Z E           e/
2026-06-03T07:59:32.0450305Z E           cache/
2026-06-03T07:59:32.0450523Z E           data/raw/
2026-06-03T07:59:32.0450749Z E           data/live/
2026-06-03T07:59:32.0450982Z E           data/private/
2026-06-03T07:59:32.0451263Z E           data/vendor/
2026-06-03T07:59:32.0451499Z E           evidence/
2026-06-03T07:59:32.0451718Z E           lockbox/
```

```text
2026-06-03T07:59:32.0460152Z E           .DS_Store
2026-06-03T07:59:32.0460342Z E           .idea/
2026-06-03T07:59:32.0460527Z E           .vscode/
2026-06-03T07:59:32.0460670Z 
2026-06-03T07:59:32.0460796Z tests/test_priority_fixes.py:372: AssertionError
2026-06-03T07:59:32.0461237Z =============================== warnings summary ===============================
2026-06-03T07:59:32.0461859Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbol_writes_csv_and_metadata
2026-06-03T07:59:32.0462512Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbol_merges_without_duplicates
2026-06-03T07:59:32.0463156Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbols_batch_counts_results
2026-06-03T07:59:32.0463778Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbols_batch_counts_results
2026-06-03T07:59:32.0465662Z   /home/runner/work/institutional-trading-engine/institutional-trading-engine/src/historical/polygon_ingestion.py:125: FutureWarning: The behavior of DataFrame concatenation with empty or all-NA entries is deprecated. In a future version, this will no longer exclude empty or all-NA columns when determining the result dtypes. To retain the old behavior, exclude the relevant entries before the concat operation.
2026-06-03T07:59:32.0467275Z     combined = pd.concat([existing, df], ignore_index=True)
2026-06-03T07:59:32.0467651Z 
2026-06-03T07:59:32.0467884Z -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2026-06-03T07:59:32.0468601Z =========================== short test summary info ============================
2026-06-03T07:59:32.0469584Z FAILED tests/test_priority_fixes.py::TestDataPersistence::test_decision_log_path_not_in_gitignore - AssertionError: data/ is in .gitignore â decision log will be lost on every run
```

```text
2026-06-03T07:59:32.0467275Z     combined = pd.concat([existing, df], ignore_index=True)
2026-06-03T07:59:32.0467651Z 
2026-06-03T07:59:32.0467884Z -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2026-06-03T07:59:32.0468601Z =========================== short test summary info ============================
2026-06-03T07:59:32.0469584Z FAILED tests/test_priority_fixes.py::TestDataPersistence::test_decision_log_path_not_in_gitignore - AssertionError: data/ is in .gitignore â decision log will be lost on every run
2026-06-03T07:59:32.0470371Z assert 'data/' not in '# Python\n_...\n.vscode/\n'
2026-06-03T07:59:32.0470659Z   
2026-06-03T07:59:32.0470853Z   'data/' is contained here:
2026-06-03T07:59:32.0471081Z     e/
2026-06-03T07:59:32.0471274Z     cache/
2026-06-03T07:59:32.0471450Z     data/raw/
2026-06-03T07:59:32.0471634Z     data/live/
2026-06-03T07:59:32.0471825Z     data/private/
2026-06-03T07:59:32.0472020Z     data/vendor/
2026-06-03T07:59:32.0472207Z     evidence/
2026-06-03T07:59:32.0472390Z     lockbox/
```

```text
2026-06-03T07:59:32.0479592Z     .DS_Store
2026-06-03T07:59:32.0479769Z     .idea/
2026-06-03T07:59:32.0479943Z     .vscode/
2026-06-03T07:59:32.0480186Z 1 failed, 1559 passed, 1 skipped, 4 warnings in 12.00s
2026-06-03T07:59:32.2796182Z ##[error]Process completed with exit code 1.
2026-06-03T07:59:32.2912506Z Post job cleanup.
2026-06-03T07:59:32.3893831Z [command]/usr/bin/git version
2026-06-03T07:59:32.3930925Z git version 2.54.0
2026-06-03T07:59:32.3973794Z Temporarily overriding HOME='/home/runner/work/_temp/ad18fb16-227c-486c-b716-aa99cb521a9e' before making global git config changes
2026-06-03T07:59:32.3975117Z Adding repository directory to the temporary git global config as a safe directory
2026-06-03T07:59:32.3986774Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-06-03T07:59:32.4022061Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-06-03T07:59:32.4053855Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-06-03T07:59:32.4276921Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-06-03T07:59:32.4300939Z http.https://github.com/.extraheader
2026-06-03T07:59:32.4312994Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

## Report Quality Validation

- Run ID: `26871635969`
- Branch: `main`
- Commit: `2597af623fcc`
- Title: Document PO14 forward evidence quality gate in changelog
- Created: 2026-06-03T07:59:00Z
- Updated: 2026-06-03T07:59:38Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26871635969

### Failed job: validate-reports (postmarket)

- Job ID: `79248149582`
- Started: 2026-06-03T07:59:02Z
- Completed: 2026-06-03T07:59:37Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-03T07:59:18.3485598Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-03T07:59:18.3486005Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-03T07:59:18.3486429Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-03T07:59:18.3486776Z ##[endgroup]
2026-06-03T07:59:34.3010984Z Traceback (most recent call last):
2026-06-03T07:59:34.3019990Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 247, in <module>
2026-06-03T07:59:34.3022217Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-30/2026-06-03?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-03T07:59:34.3023118Z     raise SystemExit(main())
2026-06-03T07:59:34.3023385Z                      ^^^^^^
2026-06-03T07:59:34.3024285Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 236, in main
2026-06-03T07:59:34.3025075Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-03T07:59:34.3025560Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-03T07:59:34.3026325Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 68, in write_report_text_guarded
2026-06-03T07:59:34.3027093Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-03T07:59:34.3027934Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-06-03T07:59:34.3028658Z     raise ReportOutputBoundaryError(
```

```text
2026-06-03T07:59:34.3028658Z     raise ReportOutputBoundaryError(
2026-06-03T07:59:34.3029607Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/postmarket-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-06-03T07:59:34.3031195Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-30/2026-06-03?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-03T07:59:34.3032546Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-30/2026-06-03?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-03T07:59:34.3033429Z WARNING: scanner metric loading failed: ModuleNotFoundError: No module named 'config'
2026-06-03T07:59:34.3034086Z WARNING: scanner_metrics_missing:MSFT
2026-06-03T07:59:34.3034379Z WARNING: scanner_metrics_missing:NVDA
2026-06-03T07:59:34.3034655Z WARNING: scanner_metrics_missing:META
2026-06-03T07:59:34.3034930Z WARNING: scanner_metrics_missing:AAPL
2026-06-03T07:59:34.3035215Z WARNING: scanner_metrics_missing:MU
2026-06-03T07:59:34.3035790Z WARNING: scanner_metrics_missing:QQQ
2026-06-03T07:59:34.3036083Z WARNING: scanner_metrics_missing:GLD
2026-06-03T07:59:34.3036363Z WARNING: scanner_metrics_missing:SLV
2026-06-03T07:59:34.3625300Z ##[error]Process completed with exit code 1.
2026-06-03T07:59:34.3709818Z ##[group]Run actions/upload-artifact@v4
2026-06-03T07:59:34.3710122Z with:
```

```text
2026-06-03T07:59:34.3035215Z WARNING: scanner_metrics_missing:MU
2026-06-03T07:59:34.3035790Z WARNING: scanner_metrics_missing:QQQ
2026-06-03T07:59:34.3036083Z WARNING: scanner_metrics_missing:GLD
2026-06-03T07:59:34.3036363Z WARNING: scanner_metrics_missing:SLV
2026-06-03T07:59:34.3625300Z ##[error]Process completed with exit code 1.
2026-06-03T07:59:34.3709818Z ##[group]Run actions/upload-artifact@v4
2026-06-03T07:59:34.3710122Z with:
2026-06-03T07:59:34.3710354Z   name: validated-postmarket-report
2026-06-03T07:59:34.3710656Z   path: reports/postmarket-report.md
2026-06-03T07:59:34.3710947Z   retention-days: 14
2026-06-03T07:59:34.3711182Z   if-no-files-found: warn
2026-06-03T07:59:34.3711433Z   compression-level: 6
2026-06-03T07:59:34.3711673Z   overwrite: false
2026-06-03T07:59:34.3711907Z   include-hidden-files: false
2026-06-03T07:59:34.3712157Z env:
2026-06-03T07:59:34.3712486Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (premarket)

- Job ID: `79248149591`
- Started: 2026-06-03T07:59:02Z
- Completed: 2026-06-03T07:59:34Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-03T07:59:17.9257355Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-03T07:59:17.9257753Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-03T07:59:17.9258194Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-03T07:59:17.9258551Z ##[endgroup]
2026-06-03T07:59:31.9687503Z Traceback (most recent call last):
2026-06-03T07:59:31.9697729Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 247, in <module>
2026-06-03T07:59:31.9700182Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-30/2026-06-03?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-03T07:59:31.9701846Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-30/2026-06-03?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-03T07:59:31.9703465Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-30/2026-06-03?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-03T07:59:31.9704540Z WARNING: scanner metric loading failed: ModuleNotFoundError: No module named 'config'
2026-06-03T07:59:31.9705050Z WARNING: scanner_metrics_missing:MSFT
2026-06-03T07:59:31.9705378Z WARNING: scanner_metrics_missing:NVDA
2026-06-03T07:59:31.9705677Z WARNING: scanner_metrics_missing:META
2026-06-03T07:59:31.9705958Z WARNING: scanner_metrics_missing:AAPL
2026-06-03T07:59:31.9706237Z WARNING: scanner_metrics_missing:MU
2026-06-03T07:59:31.9706517Z WARNING: scanner_metrics_missing:QQQ
```

```text
2026-06-03T07:59:31.9697729Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 247, in <module>
2026-06-03T07:59:31.9700182Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-30/2026-06-03?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-03T07:59:31.9701846Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-30/2026-06-03?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-03T07:59:31.9703465Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-30/2026-06-03?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-03T07:59:31.9704540Z WARNING: scanner metric loading failed: ModuleNotFoundError: No module named 'config'
2026-06-03T07:59:31.9705050Z WARNING: scanner_metrics_missing:MSFT
2026-06-03T07:59:31.9705378Z WARNING: scanner_metrics_missing:NVDA
2026-06-03T07:59:31.9705677Z WARNING: scanner_metrics_missing:META
2026-06-03T07:59:31.9705958Z WARNING: scanner_metrics_missing:AAPL
2026-06-03T07:59:31.9706237Z WARNING: scanner_metrics_missing:MU
2026-06-03T07:59:31.9706517Z WARNING: scanner_metrics_missing:QQQ
2026-06-03T07:59:31.9706798Z WARNING: scanner_metrics_missing:GLD
2026-06-03T07:59:31.9707073Z WARNING: scanner_metrics_missing:SLV
2026-06-03T07:59:31.9707499Z     raise SystemExit(main())
2026-06-03T07:59:31.9707763Z                      ^^^^^^
2026-06-03T07:59:31.9708419Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 236, in main
```

```text
2026-06-03T07:59:31.9711513Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-03T07:59:31.9712355Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-06-03T07:59:31.9713097Z     raise ReportOutputBoundaryError(
2026-06-03T07:59:31.9714072Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/premarket-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-06-03T07:59:32.0361414Z ##[error]Process completed with exit code 1.
2026-06-03T07:59:32.0447267Z ##[group]Run actions/upload-artifact@v4
2026-06-03T07:59:32.0447581Z with:
2026-06-03T07:59:32.0447809Z   name: validated-premarket-report
2026-06-03T07:59:32.0448105Z   path: reports/premarket-report.md
2026-06-03T07:59:32.0448379Z   retention-days: 14
2026-06-03T07:59:32.0448611Z   if-no-files-found: warn
2026-06-03T07:59:32.0448856Z   compression-level: 6
2026-06-03T07:59:32.0449152Z   overwrite: false
2026-06-03T07:59:32.0449382Z   include-hidden-files: false
2026-06-03T07:59:32.0449878Z env:
2026-06-03T07:59:32.0450200Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (weekly)

- Job ID: `79248149622`
- Started: 2026-06-03T07:59:02Z
- Completed: 2026-06-03T07:59:21Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-03T07:59:18.7318038Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-03T07:59:18.7318437Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-03T07:59:18.7318892Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-03T07:59:18.7319237Z ##[endgroup]
2026-06-03T07:59:19.0811583Z Traceback (most recent call last):
2026-06-03T07:59:19.0820962Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 247, in <module>
2026-06-03T07:59:19.0822059Z     raise SystemExit(main())
2026-06-03T07:59:19.0822432Z                      ^^^^^^
2026-06-03T07:59:19.0823382Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 236, in main
2026-06-03T07:59:19.0824776Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-03T07:59:19.0825441Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-03T07:59:19.0826646Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 68, in write_report_text_guarded
2026-06-03T07:59:19.0827888Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-03T07:59:19.0829197Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-06-03T07:59:19.0830343Z     raise ReportOutputBoundaryError(
2026-06-03T07:59:19.0831821Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
```

```text
2026-06-03T07:59:19.0827888Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-03T07:59:19.0829197Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-06-03T07:59:19.0830343Z     raise ReportOutputBoundaryError(
2026-06-03T07:59:19.0831821Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-06-03T07:59:19.1063501Z ##[error]Process completed with exit code 1.
2026-06-03T07:59:19.1151036Z ##[group]Run actions/upload-artifact@v4
2026-06-03T07:59:19.1151357Z with:
2026-06-03T07:59:19.1151591Z   name: validated-weekly-report
2026-06-03T07:59:19.1151882Z   path: reports/weekly-report.md
2026-06-03T07:59:19.1152153Z   retention-days: 14
2026-06-03T07:59:19.1152392Z   if-no-files-found: warn
2026-06-03T07:59:19.1152643Z   compression-level: 6
2026-06-03T07:59:19.1152891Z   overwrite: false
2026-06-03T07:59:19.1153129Z   include-hidden-files: false
2026-06-03T07:59:19.1153385Z env:
2026-06-03T07:59:19.1153768Z   POLYGON_API_KEY: ***
```

## Decision Engine Tests

- Run ID: `26871549448`
- Branch: `main`
- Commit: `5e16adbe22e9`
- Title: Document PO14 CI green status in README
- Created: 2026-06-03T07:57:10Z
- Updated: 2026-06-03T07:57:50Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26871549448

### Failed job: tests

- Job ID: `79247856964`
- Started: 2026-06-03T07:57:13Z
- Completed: 2026-06-03T07:57:49Z
- Failed steps: 5. Run pytest

#### Error context

```text
2026-06-03T07:57:45.7797029Z ........................................................................ [ 87%]
2026-06-03T07:57:45.9558728Z ........................................................................ [ 92%]
2026-06-03T07:57:46.0671815Z ........................................................................ [ 96%]
2026-06-03T07:57:46.1547731Z .................................................                        [100%]
2026-06-03T07:57:46.1548746Z =================================== FAILURES ===================================
2026-06-03T07:57:46.1549506Z _________ TestDataPersistence.test_decision_log_path_not_in_gitignore __________
2026-06-03T07:57:46.1550028Z 
2026-06-03T07:57:46.1550341Z self = <test_priority_fixes.TestDataPersistence object at 0x7f0e963974d0>
2026-06-03T07:57:46.1551217Z 
2026-06-03T07:57:46.1551425Z     def test_decision_log_path_not_in_gitignore(self):
2026-06-03T07:57:46.1551917Z         gitignore = Path(".gitignore")
2026-06-03T07:57:46.1552360Z         if not gitignore.exists():
2026-06-03T07:57:46.1552741Z             return
2026-06-03T07:57:46.1553069Z         content = gitignore.read_text()
2026-06-03T07:57:46.1553785Z         # data/ should NOT be in gitignore
2026-06-03T07:57:46.1554209Z >       assert "data/" not in content, (
```

```text
2026-06-03T07:57:46.1553785Z         # data/ should NOT be in gitignore
2026-06-03T07:57:46.1554209Z >       assert "data/" not in content, (
2026-06-03T07:57:46.1555385Z             "data/ is in .gitignore â decision log will be lost on every run"
2026-06-03T07:57:46.1555951Z         )
2026-06-03T07:57:46.1556548Z E       AssertionError: data/ is in .gitignore â decision log will be lost on every run
2026-06-03T07:57:46.1557245Z E       assert 'data/' not in '# Python\n_...\n.vscode/\n'
2026-06-03T07:57:46.1557700Z E         
2026-06-03T07:57:46.1557989Z E         'data/' is contained here:
2026-06-03T07:57:46.1558378Z E           e/
2026-06-03T07:57:46.1558658Z E           cache/
2026-06-03T07:57:46.1558954Z E           data/raw/
2026-06-03T07:57:46.1559274Z E           data/live/
2026-06-03T07:57:46.1559608Z E           data/private/
2026-06-03T07:57:46.1559944Z E           data/vendor/
2026-06-03T07:57:46.1560270Z E           evidence/
2026-06-03T07:57:46.1560574Z E           lockbox/
```

```text
2026-06-03T07:57:46.1572645Z E           .DS_Store
2026-06-03T07:57:46.1572944Z E           .idea/
2026-06-03T07:57:46.1573574Z E           .vscode/
2026-06-03T07:57:46.1573764Z 
2026-06-03T07:57:46.1573959Z tests/test_priority_fixes.py:372: AssertionError
2026-06-03T07:57:46.1574514Z =============================== warnings summary ===============================
2026-06-03T07:57:46.1575584Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbol_writes_csv_and_metadata
2026-06-03T07:57:46.1576612Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbol_merges_without_duplicates
2026-06-03T07:57:46.1577631Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbols_batch_counts_results
2026-06-03T07:57:46.1578601Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbols_batch_counts_results
2026-06-03T07:57:46.1581566Z   /home/runner/work/institutional-trading-engine/institutional-trading-engine/src/historical/polygon_ingestion.py:125: FutureWarning: The behavior of DataFrame concatenation with empty or all-NA entries is deprecated. In a future version, this will no longer exclude empty or all-NA columns when determining the result dtypes. To retain the old behavior, exclude the relevant entries before the concat operation.
2026-06-03T07:57:46.1584364Z     combined = pd.concat([existing, df], ignore_index=True)
2026-06-03T07:57:46.1584982Z 
2026-06-03T07:57:46.1585330Z -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2026-06-03T07:57:46.1586041Z =========================== short test summary info ============================
2026-06-03T07:57:46.1587523Z FAILED tests/test_priority_fixes.py::TestDataPersistence::test_decision_log_path_not_in_gitignore - AssertionError: data/ is in .gitignore â decision log will be lost on every run
```

```text
2026-06-03T07:57:46.1584364Z     combined = pd.concat([existing, df], ignore_index=True)
2026-06-03T07:57:46.1584982Z 
2026-06-03T07:57:46.1585330Z -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2026-06-03T07:57:46.1586041Z =========================== short test summary info ============================
2026-06-03T07:57:46.1587523Z FAILED tests/test_priority_fixes.py::TestDataPersistence::test_decision_log_path_not_in_gitignore - AssertionError: data/ is in .gitignore â decision log will be lost on every run
2026-06-03T07:57:46.1588766Z assert 'data/' not in '# Python\n_...\n.vscode/\n'
2026-06-03T07:57:46.1589200Z   
2026-06-03T07:57:46.1589474Z   'data/' is contained here:
2026-06-03T07:57:46.1589816Z     e/
2026-06-03T07:57:46.1590090Z     cache/
2026-06-03T07:57:46.1590386Z     data/raw/
2026-06-03T07:57:46.1590665Z     data/live/
2026-06-03T07:57:46.1590955Z     data/private/
2026-06-03T07:57:46.1591247Z     data/vendor/
2026-06-03T07:57:46.1591540Z     evidence/
2026-06-03T07:57:46.1591815Z     lockbox/
```

```text
2026-06-03T07:57:46.1602746Z     .DS_Store
2026-06-03T07:57:46.1603008Z     .idea/
2026-06-03T07:57:46.1603469Z     .vscode/
2026-06-03T07:57:46.1603850Z 1 failed, 1559 passed, 1 skipped, 4 warnings in 14.55s
2026-06-03T07:57:46.5854421Z ##[error]Process completed with exit code 1.
2026-06-03T07:57:46.5976203Z Post job cleanup.
2026-06-03T07:57:46.7016387Z [command]/usr/bin/git version
2026-06-03T07:57:46.7055641Z git version 2.54.0
2026-06-03T07:57:46.7101785Z Temporarily overriding HOME='/home/runner/work/_temp/d062d177-c92b-4662-bb30-a5a3ce64995d' before making global git config changes
2026-06-03T07:57:46.7103415Z Adding repository directory to the temporary git global config as a safe directory
2026-06-03T07:57:46.7108785Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-06-03T07:57:46.7160760Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-06-03T07:57:46.7198977Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-06-03T07:57:46.7439227Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-06-03T07:57:46.7466990Z http.https://github.com/.extraheader
2026-06-03T07:57:46.7480291Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```
