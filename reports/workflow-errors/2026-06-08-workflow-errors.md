# GitHub Actions Workflow Error Report

Generated: 2026-06-08 08:54 UTC
Repository: `yalcinkadir/institutional-trading-engine`
Filter since: 2026-06-07 08:54 UTC
Failed runs included: 5

## Report Quality Validation

- Run ID: `27126572415`
- Branch: `main`
- Commit: `28cb9afc1804`
- Title: Wire ARCH106 OS delete-candidate test into CI
- Created: 2026-06-08T08:53:19Z
- Updated: 2026-06-08T08:54:32Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27126572415

### Failed job: validate-reports (premarket)

- Job ID: `80056597448`
- Started: 2026-06-08T08:53:22Z
- Completed: 2026-06-08T08:54:23Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-08T08:53:40.5110665Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-08T08:53:40.5111073Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-08T08:53:40.5111524Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-08T08:53:40.5111862Z ##[endgroup]
2026-06-08T08:54:20.6301135Z Traceback (most recent call last):
2026-06-08T08:54:20.6303264Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-04/2026-06-08?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-08T08:54:20.6305756Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-04/2026-06-08?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-08T08:54:20.6308163Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-04/2026-06-08?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-08T08:54:20.6316866Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 491, in <module>
2026-06-08T08:54:20.6318162Z     raise SystemExit(main())
2026-06-08T08:54:20.6318521Z                      ^^^^^^
2026-06-08T08:54:20.6319440Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 474, in main
2026-06-08T08:54:20.6320537Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-08T08:54:20.6321195Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-08T08:54:20.6322317Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 108, in write_report_text_guarded
2026-06-08T08:54:20.6323506Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
```

```text
2026-06-08T08:54:20.6323506Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-08T08:54:20.6324781Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-08T08:54:20.6325892Z     raise ReportOutputBoundaryError(
2026-06-08T08:54:20.6328335Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/premarket-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
2026-06-08T08:54:20.6976968Z ##[error]Process completed with exit code 1.
2026-06-08T08:54:20.7061974Z ##[group]Run actions/upload-artifact@v4
2026-06-08T08:54:20.7062274Z with:
2026-06-08T08:54:20.7062504Z   name: validated-premarket-report
2026-06-08T08:54:20.7062800Z   path: reports/premarket-report.md
2026-06-08T08:54:20.7063083Z   retention-days: 14
2026-06-08T08:54:20.7063513Z   if-no-files-found: warn
2026-06-08T08:54:20.7063764Z   compression-level: 6
2026-06-08T08:54:20.7063997Z   overwrite: false
2026-06-08T08:54:20.7064229Z   include-hidden-files: false
2026-06-08T08:54:20.7064478Z env:
2026-06-08T08:54:20.7064814Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (weekly)

- Job ID: `80056597471`
- Started: 2026-06-08T08:53:22Z
- Completed: 2026-06-08T08:53:40Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-08T08:53:38.0469422Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-08T08:53:38.0469825Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-08T08:53:38.0470252Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-08T08:53:38.0470595Z ##[endgroup]
2026-06-08T08:53:38.3673556Z Traceback (most recent call last):
2026-06-08T08:53:38.3681602Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 491, in <module>
2026-06-08T08:53:38.3682954Z     raise SystemExit(main())
2026-06-08T08:53:38.3683379Z                      ^^^^^^
2026-06-08T08:53:38.3684469Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 474, in main
2026-06-08T08:53:38.3685863Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-08T08:53:38.3687034Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-08T08:53:38.3688510Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 108, in write_report_text_guarded
2026-06-08T08:53:38.3690004Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-08T08:53:38.3691594Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-08T08:53:38.3692947Z     raise ReportOutputBoundaryError(
2026-06-08T08:53:38.3695506Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
```

```text
2026-06-08T08:53:38.3690004Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-08T08:53:38.3691594Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-08T08:53:38.3692947Z     raise ReportOutputBoundaryError(
2026-06-08T08:53:38.3695506Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
2026-06-08T08:53:38.3888087Z ##[error]Process completed with exit code 1.
2026-06-08T08:53:38.3968464Z ##[group]Run actions/upload-artifact@v4
2026-06-08T08:53:38.3968774Z with:
2026-06-08T08:53:38.3968990Z   name: validated-weekly-report
2026-06-08T08:53:38.3969276Z   path: reports/weekly-report.md
2026-06-08T08:53:38.3969542Z   retention-days: 14
2026-06-08T08:53:38.3969772Z   if-no-files-found: warn
2026-06-08T08:53:38.3970014Z   compression-level: 6
2026-06-08T08:53:38.3970248Z   overwrite: false
2026-06-08T08:53:38.3970482Z   include-hidden-files: false
2026-06-08T08:53:38.3970725Z env:
2026-06-08T08:53:38.3971053Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (postmarket)

- Job ID: `80056597524`
- Started: 2026-06-08T08:53:23Z
- Completed: 2026-06-08T08:54:31Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-08T08:53:39.2324707Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-08T08:53:39.2325112Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-08T08:53:39.2325547Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-08T08:53:39.2325882Z ##[endgroup]
2026-06-08T08:54:28.0420249Z Traceback (most recent call last):
2026-06-08T08:54:28.0427869Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 491, in <module>
2026-06-08T08:54:28.0430592Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-04/2026-06-08?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-08T08:54:28.0432395Z     raise SystemExit(main())
2026-06-08T08:54:28.0432889Z                      ^^^^^^
2026-06-08T08:54:28.0434148Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 474, in main
2026-06-08T08:54:28.0435646Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-08T08:54:28.0436432Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-08T08:54:28.0437615Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 108, in write_report_text_guarded
2026-06-08T08:54:28.0438452Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-08T08:54:28.0439755Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-08T08:54:28.0440527Z     raise ReportOutputBoundaryError(
```

```text
2026-06-08T08:54:28.0440527Z     raise ReportOutputBoundaryError(
2026-06-08T08:54:28.0441926Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/postmarket-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
2026-06-08T08:54:28.0444158Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-04/2026-06-08?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-08T08:54:28.0445622Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-04/2026-06-08?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-08T08:54:28.1132564Z ##[error]Process completed with exit code 1.
2026-06-08T08:54:28.1217204Z ##[group]Run actions/upload-artifact@v4
2026-06-08T08:54:28.1217522Z with:
2026-06-08T08:54:28.1217745Z   name: validated-postmarket-report
2026-06-08T08:54:28.1218041Z   path: reports/postmarket-report.md
2026-06-08T08:54:28.1218506Z   retention-days: 14
2026-06-08T08:54:28.1218727Z   if-no-files-found: warn
2026-06-08T08:54:28.1219305Z   compression-level: 6
2026-06-08T08:54:28.1219555Z   overwrite: false
2026-06-08T08:54:28.1219772Z   include-hidden-files: false
2026-06-08T08:54:28.1220007Z env:
2026-06-08T08:54:28.1220352Z   POLYGON_API_KEY: ***
```

## Report Quality Validation

- Run ID: `27126323981`
- Branch: `main`
- Commit: `d0552c95f529`
- Title: Test ARCH106 OS delete-candidate promotion helper
- Created: 2026-06-08T08:48:21Z
- Updated: 2026-06-08T08:49:39Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27126323981

### Failed job: validate-reports (premarket)

- Job ID: `80055783621`
- Started: 2026-06-08T08:48:37Z
- Completed: 2026-06-08T08:49:37Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-08T08:48:55.1361038Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-08T08:48:55.1361438Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-08T08:48:55.1361854Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-08T08:48:55.1362199Z ##[endgroup]
2026-06-08T08:49:34.9566601Z Traceback (most recent call last):
2026-06-08T08:49:34.9568021Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-04/2026-06-08?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-08T08:49:34.9577450Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 491, in <module>
2026-06-08T08:49:34.9579517Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-04/2026-06-08?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-08T08:49:34.9580792Z     raise SystemExit(main())
2026-06-08T08:49:34.9581065Z                      ^^^^^^
2026-06-08T08:49:34.9581722Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 474, in main
2026-06-08T08:49:34.9582705Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-08T08:49:34.9583184Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-08T08:49:34.9583969Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 108, in write_report_text_guarded
2026-06-08T08:49:34.9584744Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-08T08:49:34.9585562Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
```

```text
2026-06-08T08:49:34.9585562Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-08T08:49:34.9586286Z     raise ReportOutputBoundaryError(
2026-06-08T08:49:34.9587609Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/premarket-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
2026-06-08T08:49:34.9589522Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-04/2026-06-08?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-08T08:49:35.0187044Z ##[error]Process completed with exit code 1.
2026-06-08T08:49:35.0271528Z ##[group]Run actions/upload-artifact@v4
2026-06-08T08:49:35.0271833Z with:
2026-06-08T08:49:35.0272064Z   name: validated-premarket-report
2026-06-08T08:49:35.0272365Z   path: reports/premarket-report.md
2026-06-08T08:49:35.0272939Z   retention-days: 14
2026-06-08T08:49:35.0273363Z   if-no-files-found: warn
2026-06-08T08:49:35.0273615Z   compression-level: 6
2026-06-08T08:49:35.0273849Z   overwrite: false
2026-06-08T08:49:35.0274078Z   include-hidden-files: false
2026-06-08T08:49:35.0274328Z env:
2026-06-08T08:49:35.0274663Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (postmarket)

- Job ID: `80055783668`
- Started: 2026-06-08T08:48:37Z
- Completed: 2026-06-08T08:49:38Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-08T08:48:53.4988404Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-08T08:48:53.4988836Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-08T08:48:53.4989285Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-08T08:48:53.4989634Z ##[endgroup]
2026-06-08T08:49:35.7066377Z Traceback (most recent call last):
2026-06-08T08:49:35.7068627Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-04/2026-06-08?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-08T08:49:35.7078416Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 491, in <module>
2026-06-08T08:49:35.7079529Z     raise SystemExit(main())
2026-06-08T08:49:35.7079913Z                      ^^^^^^
2026-06-08T08:49:35.7080896Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 474, in main
2026-06-08T08:49:35.7082136Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-08T08:49:35.7083896Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-04/2026-06-08?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-08T08:49:35.7086436Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-04/2026-06-08?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-08T08:49:35.7087846Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-08T08:49:35.7089142Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 108, in write_report_text_guarded
2026-06-08T08:49:35.7090470Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
```

```text
2026-06-08T08:49:35.7090470Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-08T08:49:35.7091911Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-08T08:49:35.7093166Z     raise ReportOutputBoundaryError(
2026-06-08T08:49:35.7095489Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/postmarket-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
2026-06-08T08:49:35.7625939Z ##[error]Process completed with exit code 1.
2026-06-08T08:49:35.7710398Z ##[group]Run actions/upload-artifact@v4
2026-06-08T08:49:35.7710705Z with:
2026-06-08T08:49:35.7710929Z   name: validated-postmarket-report
2026-06-08T08:49:35.7711225Z   path: reports/postmarket-report.md
2026-06-08T08:49:35.7711680Z   retention-days: 14
2026-06-08T08:49:35.7711912Z   if-no-files-found: warn
2026-06-08T08:49:35.7712155Z   compression-level: 6
2026-06-08T08:49:35.7712390Z   overwrite: false
2026-06-08T08:49:35.7712613Z   include-hidden-files: false
2026-06-08T08:49:35.7712856Z env:
2026-06-08T08:49:35.7713168Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (weekly)

- Job ID: `80055783754`
- Started: 2026-06-08T08:48:37Z
- Completed: 2026-06-08T08:48:56Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-08T08:48:54.6847006Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-08T08:48:54.6847402Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-08T08:48:54.6847856Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-08T08:48:54.6848221Z ##[endgroup]
2026-06-08T08:48:54.9934756Z Traceback (most recent call last):
2026-06-08T08:48:54.9943664Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 491, in <module>
2026-06-08T08:48:54.9945025Z     raise SystemExit(main())
2026-06-08T08:48:54.9945479Z                      ^^^^^^
2026-06-08T08:48:54.9946499Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 474, in main
2026-06-08T08:48:54.9947718Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-08T08:48:54.9948436Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-08T08:48:54.9949718Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 108, in write_report_text_guarded
2026-06-08T08:48:54.9950991Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-08T08:48:54.9952329Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-08T08:48:54.9953508Z     raise ReportOutputBoundaryError(
2026-06-08T08:48:54.9955803Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
```

```text
2026-06-08T08:48:54.9950991Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-08T08:48:54.9952329Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-08T08:48:54.9953508Z     raise ReportOutputBoundaryError(
2026-06-08T08:48:54.9955803Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
2026-06-08T08:48:55.0197296Z ##[error]Process completed with exit code 1.
2026-06-08T08:48:55.0281479Z ##[group]Run actions/upload-artifact@v4
2026-06-08T08:48:55.0281795Z with:
2026-06-08T08:48:55.0282027Z   name: validated-weekly-report
2026-06-08T08:48:55.0282312Z   path: reports/weekly-report.md
2026-06-08T08:48:55.0282590Z   retention-days: 14
2026-06-08T08:48:55.0282834Z   if-no-files-found: warn
2026-06-08T08:48:55.0283090Z   compression-level: 6
2026-06-08T08:48:55.0283337Z   overwrite: false
2026-06-08T08:48:55.0283578Z   include-hidden-files: false
2026-06-08T08:48:55.0283829Z env:
2026-06-08T08:48:55.0284211Z   POLYGON_API_KEY: ***
```

## Report Quality Validation

- Run ID: `27126271547`
- Branch: `main`
- Commit: `5ced370ea018`
- Title: Add ARCH106 OS delete-candidate helper
- Created: 2026-06-08T08:47:18Z
- Updated: 2026-06-08T08:48:35Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27126271547

### Failed job: validate-reports (premarket)

- Job ID: `80055563259`
- Started: 2026-06-08T08:47:21Z
- Completed: 2026-06-08T08:48:19Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-08T08:47:36.9495814Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-08T08:47:36.9496210Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-08T08:47:36.9496636Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-08T08:47:36.9496986Z ##[endgroup]
2026-06-08T08:48:17.0200711Z Traceback (most recent call last):
2026-06-08T08:48:17.0203375Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-04/2026-06-08?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-08T08:48:17.0207979Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-04/2026-06-08?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-08T08:48:17.0211132Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-04/2026-06-08?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-08T08:48:17.0219502Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 491, in <module>
2026-06-08T08:48:17.0220268Z     raise SystemExit(main())
2026-06-08T08:48:17.0220536Z                      ^^^^^^
2026-06-08T08:48:17.0221192Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 474, in main
2026-06-08T08:48:17.0221980Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-08T08:48:17.0222791Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-08T08:48:17.0223608Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 108, in write_report_text_guarded
2026-06-08T08:48:17.0224433Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
```

```text
2026-06-08T08:48:17.0224433Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-08T08:48:17.0225321Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-08T08:48:17.0226100Z     raise ReportOutputBoundaryError(
2026-06-08T08:48:17.0227551Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/premarket-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
2026-06-08T08:48:17.0780518Z ##[error]Process completed with exit code 1.
2026-06-08T08:48:17.0865570Z ##[group]Run actions/upload-artifact@v4
2026-06-08T08:48:17.0865892Z with:
2026-06-08T08:48:17.0866124Z   name: validated-premarket-report
2026-06-08T08:48:17.0866430Z   path: reports/premarket-report.md
2026-06-08T08:48:17.0866705Z   retention-days: 14
2026-06-08T08:48:17.0867119Z   if-no-files-found: warn
2026-06-08T08:48:17.0867367Z   compression-level: 6
2026-06-08T08:48:17.0867600Z   overwrite: false
2026-06-08T08:48:17.0867825Z   include-hidden-files: false
2026-06-08T08:48:17.0868066Z env:
2026-06-08T08:48:17.0868374Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (postmarket)

- Job ID: `80055563292`
- Started: 2026-06-08T08:47:21Z
- Completed: 2026-06-08T08:48:34Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-08T08:47:40.7443258Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-08T08:47:40.7443656Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-08T08:47:40.7444094Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-08T08:47:40.7444432Z ##[endgroup]
2026-06-08T08:48:30.6951571Z Traceback (most recent call last):
2026-06-08T08:48:30.6954224Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-04/2026-06-08?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-08T08:48:30.6965741Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 491, in <module>
2026-06-08T08:48:30.6966695Z     raise SystemExit(main())
2026-06-08T08:48:30.6967020Z                      ^^^^^^
2026-06-08T08:48:30.6967835Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 474, in main
2026-06-08T08:48:30.6968864Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-08T08:48:30.6969479Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-08T08:48:30.6970604Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 108, in write_report_text_guarded
2026-06-08T08:48:30.6972036Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-04/2026-06-08?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-08T08:48:30.6973441Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-04/2026-06-08?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-08T08:48:30.6974328Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
```

```text
2026-06-08T08:48:30.6974328Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-08T08:48:30.6975184Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-08T08:48:30.6975930Z     raise ReportOutputBoundaryError(
2026-06-08T08:48:30.6977309Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/postmarket-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
2026-06-08T08:48:30.7597145Z ##[error]Process completed with exit code 1.
2026-06-08T08:48:30.7683878Z ##[group]Run actions/upload-artifact@v4
2026-06-08T08:48:30.7684196Z with:
2026-06-08T08:48:30.7684422Z   name: validated-postmarket-report
2026-06-08T08:48:30.7684723Z   path: reports/postmarket-report.md
2026-06-08T08:48:30.7685204Z   retention-days: 14
2026-06-08T08:48:30.7685438Z   if-no-files-found: warn
2026-06-08T08:48:30.7685685Z   compression-level: 6
2026-06-08T08:48:30.7685919Z   overwrite: false
2026-06-08T08:48:30.7686145Z   include-hidden-files: false
2026-06-08T08:48:30.7686388Z env:
2026-06-08T08:48:30.7686715Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (weekly)

- Job ID: `80055563295`
- Started: 2026-06-08T08:47:20Z
- Completed: 2026-06-08T08:47:42Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-08T08:47:39.1060960Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-08T08:47:39.1061391Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-08T08:47:39.1062039Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-08T08:47:39.1062407Z ##[endgroup]
2026-06-08T08:47:39.9755715Z Traceback (most recent call last):
2026-06-08T08:47:39.9763976Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 491, in <module>
2026-06-08T08:47:39.9765122Z     raise SystemExit(main())
2026-06-08T08:47:39.9765557Z                      ^^^^^^
2026-06-08T08:47:39.9766582Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 474, in main
2026-06-08T08:47:39.9767798Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-08T08:47:39.9768525Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-08T08:47:39.9769739Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 108, in write_report_text_guarded
2026-06-08T08:47:39.9770558Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-08T08:47:39.9771441Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-08T08:47:39.9772522Z     raise ReportOutputBoundaryError(
2026-06-08T08:47:39.9773881Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
```

```text
2026-06-08T08:47:39.9770558Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-08T08:47:39.9771441Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-08T08:47:39.9772522Z     raise ReportOutputBoundaryError(
2026-06-08T08:47:39.9773881Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
2026-06-08T08:47:40.0125902Z ##[error]Process completed with exit code 1.
2026-06-08T08:47:40.0212622Z ##[group]Run actions/upload-artifact@v4
2026-06-08T08:47:40.0212966Z with:
2026-06-08T08:47:40.0213204Z   name: validated-weekly-report
2026-06-08T08:47:40.0213499Z   path: reports/weekly-report.md
2026-06-08T08:47:40.0213774Z   retention-days: 14
2026-06-08T08:47:40.0214021Z   if-no-files-found: warn
2026-06-08T08:47:40.0214281Z   compression-level: 6
2026-06-08T08:47:40.0214531Z   overwrite: false
2026-06-08T08:47:40.0214768Z   include-hidden-files: false
2026-06-08T08:47:40.0215020Z env:
2026-06-08T08:47:40.0215424Z   POLYGON_API_KEY: ***
```

## Report Quality Validation

- Run ID: `27125520455`
- Branch: `main`
- Commit: `d25193992d35`
- Title: Add manual ARCH106 operations quarantine promotion workflow
- Created: 2026-06-08T08:32:09Z
- Updated: 2026-06-08T08:33:24Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27125520455

### Failed job: validate-reports (premarket)

- Job ID: `80052981166`
- Started: 2026-06-08T08:32:12Z
- Completed: 2026-06-08T08:33:23Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-08T08:32:31.5900361Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-08T08:32:31.5900766Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-08T08:32:31.5901202Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-08T08:32:31.5901543Z ##[endgroup]
2026-06-08T08:33:19.9142473Z Traceback (most recent call last):
2026-06-08T08:33:19.9144804Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-04/2026-06-08?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-08T08:33:19.9148134Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-04/2026-06-08?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-08T08:33:19.9150658Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-04/2026-06-08?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-08T08:33:19.9157612Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 491, in <module>
2026-06-08T08:33:19.9158823Z     raise SystemExit(main())
2026-06-08T08:33:19.9159125Z                      ^^^^^^
2026-06-08T08:33:19.9159883Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 474, in main
2026-06-08T08:33:19.9160818Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-08T08:33:19.9161368Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-08T08:33:19.9162324Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 108, in write_report_text_guarded
2026-06-08T08:33:19.9163312Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
```

```text
2026-06-08T08:33:19.9163312Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-08T08:33:19.9164177Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-08T08:33:19.9164935Z     raise ReportOutputBoundaryError(
2026-06-08T08:33:19.9166328Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/premarket-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
2026-06-08T08:33:19.9691895Z ##[error]Process completed with exit code 1.
2026-06-08T08:33:19.9777281Z ##[group]Run actions/upload-artifact@v4
2026-06-08T08:33:19.9777583Z with:
2026-06-08T08:33:19.9778055Z   name: validated-premarket-report
2026-06-08T08:33:19.9778364Z   path: reports/premarket-report.md
2026-06-08T08:33:19.9778637Z   retention-days: 14
2026-06-08T08:33:19.9779055Z   if-no-files-found: warn
2026-06-08T08:33:19.9779294Z   compression-level: 6
2026-06-08T08:33:19.9779518Z   overwrite: false
2026-06-08T08:33:19.9779739Z   include-hidden-files: false
2026-06-08T08:33:19.9779986Z env:
2026-06-08T08:33:19.9780330Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (weekly)

- Job ID: `80052981213`
- Started: 2026-06-08T08:32:12Z
- Completed: 2026-06-08T08:32:35Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-08T08:32:32.0812082Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-08T08:32:32.0812454Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-08T08:32:32.0812881Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-08T08:32:32.0813199Z ##[endgroup]
2026-06-08T08:32:32.9324671Z Traceback (most recent call last):
2026-06-08T08:32:32.9335147Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 491, in <module>
2026-06-08T08:32:32.9337137Z     raise SystemExit(main())
2026-06-08T08:32:32.9337788Z                      ^^^^^^
2026-06-08T08:32:32.9338984Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 474, in main
2026-06-08T08:32:32.9340152Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-08T08:32:32.9340833Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-08T08:32:32.9342056Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 108, in write_report_text_guarded
2026-06-08T08:32:32.9343274Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-08T08:32:32.9344717Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-08T08:32:32.9345825Z     raise ReportOutputBoundaryError(
2026-06-08T08:32:32.9347825Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
```

```text
2026-06-08T08:32:32.9343274Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-08T08:32:32.9344717Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-08T08:32:32.9345825Z     raise ReportOutputBoundaryError(
2026-06-08T08:32:32.9347825Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
2026-06-08T08:32:32.9546450Z ##[error]Process completed with exit code 1.
2026-06-08T08:32:32.9622778Z ##[group]Run actions/upload-artifact@v4
2026-06-08T08:32:32.9623063Z with:
2026-06-08T08:32:32.9623278Z   name: validated-weekly-report
2026-06-08T08:32:32.9623829Z   path: reports/weekly-report.md
2026-06-08T08:32:32.9624085Z   retention-days: 14
2026-06-08T08:32:32.9624311Z   if-no-files-found: warn
2026-06-08T08:32:32.9624547Z   compression-level: 6
2026-06-08T08:32:32.9624774Z   overwrite: false
2026-06-08T08:32:32.9625004Z   include-hidden-files: false
2026-06-08T08:32:32.9625242Z env:
2026-06-08T08:32:32.9625598Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (postmarket)

- Job ID: `80052981252`
- Started: 2026-06-08T08:32:12Z
- Completed: 2026-06-08T08:33:11Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-08T08:32:28.5242407Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-08T08:32:28.5242823Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-08T08:32:28.5243255Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-08T08:32:28.5243613Z ##[endgroup]
2026-06-08T08:33:09.1697034Z Traceback (most recent call last):
2026-06-08T08:33:09.1698813Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-04/2026-06-08?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-08T08:33:09.1707876Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 491, in <module>
2026-06-08T08:33:09.1709298Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-04/2026-06-08?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-08T08:33:09.1710297Z     raise SystemExit(main())
2026-06-08T08:33:09.1710570Z                      ^^^^^^
2026-06-08T08:33:09.1711580Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 474, in main
2026-06-08T08:33:09.1712361Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-08T08:33:09.1712837Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-08T08:33:09.1713639Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 108, in write_report_text_guarded
2026-06-08T08:33:09.1714452Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-08T08:33:09.1715313Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
```

```text
2026-06-08T08:33:09.1715313Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-08T08:33:09.1716064Z     raise ReportOutputBoundaryError(
2026-06-08T08:33:09.1717443Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/postmarket-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
2026-06-08T08:33:09.1719448Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-04/2026-06-08?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-08T08:33:09.2298564Z ##[error]Process completed with exit code 1.
2026-06-08T08:33:09.2384802Z ##[group]Run actions/upload-artifact@v4
2026-06-08T08:33:09.2385113Z with:
2026-06-08T08:33:09.2385355Z   name: validated-postmarket-report
2026-06-08T08:33:09.2385663Z   path: reports/postmarket-report.md
2026-06-08T08:33:09.2386134Z   retention-days: 14
2026-06-08T08:33:09.2386377Z   if-no-files-found: warn
2026-06-08T08:33:09.2386632Z   compression-level: 6
2026-06-08T08:33:09.2386878Z   overwrite: false
2026-06-08T08:33:09.2387116Z   include-hidden-files: false
2026-06-08T08:33:09.2387376Z env:
2026-06-08T08:33:09.2387710Z   POLYGON_API_KEY: ***
```

## Report Quality Validation

- Run ID: `27125172250`
- Branch: `main`
- Commit: `98c0faf303dd`
- Title: Wire ARCH106 operations quarantine test into CI
- Created: 2026-06-08T08:24:59Z
- Updated: 2026-06-08T08:26:39Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27125172250

### Failed job: validate-reports (postmarket)

- Job ID: `80051834788`
- Started: 2026-06-08T08:25:24Z
- Completed: 2026-06-08T08:26:34Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-08T08:25:42.1443102Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-08T08:25:42.1443493Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-08T08:25:42.1443943Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-08T08:25:42.1444275Z ##[endgroup]
2026-06-08T08:26:31.2166242Z Traceback (most recent call last):
2026-06-08T08:26:31.2167773Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-04/2026-06-08?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-08T08:26:31.2169884Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-04/2026-06-08?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-08T08:26:31.2172341Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-04/2026-06-08?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-08T08:26:31.2181362Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 491, in <module>
2026-06-08T08:26:31.2182069Z     raise SystemExit(main())
2026-06-08T08:26:31.2182377Z                      ^^^^^^
2026-06-08T08:26:31.2182971Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 474, in main
2026-06-08T08:26:31.2183666Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-08T08:26:31.2184096Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-08T08:26:31.2184804Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 108, in write_report_text_guarded
2026-06-08T08:26:31.2185542Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
```

```text
2026-06-08T08:26:31.2185542Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-08T08:26:31.2186332Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-08T08:26:31.2187032Z     raise ReportOutputBoundaryError(
2026-06-08T08:26:31.2188317Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/postmarket-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
2026-06-08T08:26:31.2857155Z ##[error]Process completed with exit code 1.
2026-06-08T08:26:31.2931326Z ##[group]Run actions/upload-artifact@v4
2026-06-08T08:26:31.2931618Z with:
2026-06-08T08:26:31.2931841Z   name: validated-postmarket-report
2026-06-08T08:26:31.2932127Z   path: reports/postmarket-report.md
2026-06-08T08:26:31.2932404Z   retention-days: 14
2026-06-08T08:26:31.2932765Z   if-no-files-found: warn
2026-06-08T08:26:31.2933003Z   compression-level: 6
2026-06-08T08:26:31.2933234Z   overwrite: false
2026-06-08T08:26:31.2933464Z   include-hidden-files: false
2026-06-08T08:26:31.2933703Z env:
2026-06-08T08:26:31.2934007Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (weekly)

- Job ID: `80051834817`
- Started: 2026-06-08T08:25:24Z
- Completed: 2026-06-08T08:25:44Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-08T08:25:42.2814896Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-08T08:25:42.2815282Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-08T08:25:42.2815715Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-08T08:25:42.2816048Z ##[endgroup]
2026-06-08T08:25:43.1409448Z Traceback (most recent call last):
2026-06-08T08:25:43.1417673Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 491, in <module>
2026-06-08T08:25:43.1418732Z     raise SystemExit(main())
2026-06-08T08:25:43.1428441Z                      ^^^^^^
2026-06-08T08:25:43.1429506Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 474, in main
2026-06-08T08:25:43.1430289Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-08T08:25:43.1430783Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-08T08:25:43.1431559Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 108, in write_report_text_guarded
2026-06-08T08:25:43.1432372Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-08T08:25:43.1433216Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-08T08:25:43.1433964Z     raise ReportOutputBoundaryError(
2026-06-08T08:25:43.1435333Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
```

```text
2026-06-08T08:25:43.1432372Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-08T08:25:43.1433216Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-08T08:25:43.1433964Z     raise ReportOutputBoundaryError(
2026-06-08T08:25:43.1435333Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
2026-06-08T08:25:43.1648783Z ##[error]Process completed with exit code 1.
2026-06-08T08:25:43.1732982Z ##[group]Run actions/upload-artifact@v4
2026-06-08T08:25:43.1733296Z with:
2026-06-08T08:25:43.1733518Z   name: validated-weekly-report
2026-06-08T08:25:43.1733795Z   path: reports/weekly-report.md
2026-06-08T08:25:43.1734064Z   retention-days: 14
2026-06-08T08:25:43.1734302Z   if-no-files-found: warn
2026-06-08T08:25:43.1734548Z   compression-level: 6
2026-06-08T08:25:43.1734781Z   overwrite: false
2026-06-08T08:25:43.1735007Z   include-hidden-files: false
2026-06-08T08:25:43.1735250Z env:
2026-06-08T08:25:43.1735610Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (premarket)

- Job ID: `80051834846`
- Started: 2026-06-08T08:25:24Z
- Completed: 2026-06-08T08:26:38Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-08T08:25:44.3283653Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-08T08:25:44.3284051Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-08T08:25:44.3284484Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-08T08:25:44.3284825Z ##[endgroup]
2026-06-08T08:26:34.6338935Z Traceback (most recent call last):
2026-06-08T08:26:34.6352004Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 491, in <module>
2026-06-08T08:26:34.6353897Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-04/2026-06-08?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-08T08:26:34.6355446Z     raise SystemExit(main())
2026-06-08T08:26:34.6355747Z                      ^^^^^^
2026-06-08T08:26:34.6356518Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 474, in main
2026-06-08T08:26:34.6357479Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-08T08:26:34.6358037Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-08T08:26:34.6359000Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 108, in write_report_text_guarded
2026-06-08T08:26:34.6360022Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-08T08:26:34.6360946Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-08T08:26:34.6361703Z     raise ReportOutputBoundaryError(
```

```text
2026-06-08T08:26:34.6361703Z     raise ReportOutputBoundaryError(
2026-06-08T08:26:34.6363102Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/premarket-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
2026-06-08T08:26:34.6365440Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-04/2026-06-08?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-08T08:26:34.6366903Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-04/2026-06-08?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-08T08:26:34.6889384Z ##[error]Process completed with exit code 1.
2026-06-08T08:26:34.6976483Z ##[group]Run actions/upload-artifact@v4
2026-06-08T08:26:34.6976783Z with:
2026-06-08T08:26:34.6977001Z   name: validated-premarket-report
2026-06-08T08:26:34.6977291Z   path: reports/premarket-report.md
2026-06-08T08:26:34.6977554Z   retention-days: 14
2026-06-08T08:26:34.6977968Z   if-no-files-found: warn
2026-06-08T08:26:34.6978201Z   compression-level: 6
2026-06-08T08:26:34.6978421Z   overwrite: false
2026-06-08T08:26:34.6978635Z   include-hidden-files: false
2026-06-08T08:26:34.6978877Z env:
2026-06-08T08:26:34.6979209Z   POLYGON_API_KEY: ***
```
