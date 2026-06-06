# GitHub Actions Workflow Error Report

Generated: 2026-06-06 08:07 UTC
Repository: `yalcinkadir/institutional-trading-engine`
Filter since: 2026-06-05 08:07 UTC
Failed runs included: 6

## Report Quality Validation

- Run ID: `27053237637`
- Branch: `main`
- Commit: `b8d2ac694499`
- Title: Merge BT130 real historical backtest evidence pack gate
- Created: 2026-06-06T05:00:37Z
- Updated: 2026-06-06T05:01:40Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27053237637

### Failed job: validate-reports (weekly)

- Job ID: `79852564696`
- Started: 2026-06-06T05:00:39Z
- Completed: 2026-06-06T05:00:56Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-06T05:00:54.1986216Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-06T05:00:54.1986608Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-06T05:00:54.1987042Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-06T05:00:54.1987378Z ##[endgroup]
2026-06-06T05:00:54.5132616Z Traceback (most recent call last):
2026-06-06T05:00:54.5140050Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 391, in <module>
2026-06-06T05:00:54.5141131Z     raise SystemExit(main())
2026-06-06T05:00:54.5141509Z                      ^^^^^^
2026-06-06T05:00:54.5154487Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 374, in main
2026-06-06T05:00:54.5155359Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-06T05:00:54.5155839Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-06T05:00:54.5156666Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 108, in write_report_text_guarded
2026-06-06T05:00:54.5157444Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-06T05:00:54.5158282Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-06T05:00:54.5159029Z     raise ReportOutputBoundaryError(
2026-06-06T05:00:54.5160349Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
```

```text
2026-06-06T05:00:54.5157444Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-06T05:00:54.5158282Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-06T05:00:54.5159029Z     raise ReportOutputBoundaryError(
2026-06-06T05:00:54.5160349Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
2026-06-06T05:00:54.5370370Z ##[error]Process completed with exit code 1.
2026-06-06T05:00:54.5454980Z ##[group]Run actions/upload-artifact@v4
2026-06-06T05:00:54.5455271Z with:
2026-06-06T05:00:54.5455487Z   name: validated-weekly-report
2026-06-06T05:00:54.5455756Z   path: reports/weekly-report.md
2026-06-06T05:00:54.5456012Z   retention-days: 14
2026-06-06T05:00:54.5456238Z   if-no-files-found: warn
2026-06-06T05:00:54.5456474Z   compression-level: 6
2026-06-06T05:00:54.5456704Z   overwrite: false
2026-06-06T05:00:54.5456926Z   include-hidden-files: false
2026-06-06T05:00:54.5457169Z env:
2026-06-06T05:00:54.5457524Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (postmarket)

- Job ID: `79852564701`
- Started: 2026-06-06T05:00:39Z
- Completed: 2026-06-06T05:01:39Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-06T05:00:55.2160628Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-06T05:00:55.2161023Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-06T05:00:55.2161458Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-06T05:00:55.2161791Z ##[endgroup]
2026-06-06T05:01:36.9450347Z Traceback (most recent call last):
2026-06-06T05:01:36.9459577Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 391, in <module>
2026-06-06T05:01:36.9461466Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-02/2026-06-06?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-06T05:01:36.9462617Z     raise SystemExit(main())
2026-06-06T05:01:36.9462922Z                      ^^^^^^
2026-06-06T05:01:36.9463689Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 374, in main
2026-06-06T05:01:36.9464659Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-06T05:01:36.9465242Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-06T05:01:36.9466431Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 108, in write_report_text_guarded
2026-06-06T05:01:36.9467429Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-06T05:01:36.9468496Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-06T05:01:36.9469448Z     raise ReportOutputBoundaryError(
```

```text
2026-06-06T05:01:36.9469448Z     raise ReportOutputBoundaryError(
2026-06-06T05:01:36.9470995Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/postmarket-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
2026-06-06T05:01:36.9473031Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-02/2026-06-06?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-06T05:01:36.9474443Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-02/2026-06-06?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-06T05:01:37.0030469Z ##[error]Process completed with exit code 1.
2026-06-06T05:01:37.0117695Z ##[group]Run actions/upload-artifact@v4
2026-06-06T05:01:37.0118009Z with:
2026-06-06T05:01:37.0118231Z   name: validated-postmarket-report
2026-06-06T05:01:37.0118532Z   path: reports/postmarket-report.md
2026-06-06T05:01:37.0118991Z   retention-days: 14
2026-06-06T05:01:37.0119224Z   if-no-files-found: warn
2026-06-06T05:01:37.0119466Z   compression-level: 6
2026-06-06T05:01:37.0119697Z   overwrite: false
2026-06-06T05:01:37.0119924Z   include-hidden-files: false
2026-06-06T05:01:37.0120164Z env:
2026-06-06T05:01:37.0120475Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (premarket)

- Job ID: `79852564733`
- Started: 2026-06-06T05:00:39Z
- Completed: 2026-06-06T05:01:34Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-06T05:00:54.5020330Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-06T05:00:54.5020726Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-06T05:00:54.5021161Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-06T05:00:54.5021503Z ##[endgroup]
2026-06-06T05:01:33.0887761Z Traceback (most recent call last):
2026-06-06T05:01:33.0890002Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-02/2026-06-06?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-06T05:01:33.0893585Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-02/2026-06-06?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-06T05:01:33.0901301Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 391, in <module>
2026-06-06T05:01:33.0902046Z     raise SystemExit(main())
2026-06-06T05:01:33.0902301Z                      ^^^^^^
2026-06-06T05:01:33.0903371Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 374, in main
2026-06-06T05:01:33.0904173Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-06T05:01:33.0904636Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-06T05:01:33.0905442Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 108, in write_report_text_guarded
2026-06-06T05:01:33.0906251Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-06T05:01:33.0907102Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
```

```text
2026-06-06T05:01:33.0907102Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-06T05:01:33.0907868Z     raise ReportOutputBoundaryError(
2026-06-06T05:01:33.0909268Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/premarket-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
2026-06-06T05:01:33.0911398Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-02/2026-06-06?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-06T05:01:33.1557460Z ##[error]Process completed with exit code 1.
2026-06-06T05:01:33.1643669Z ##[group]Run actions/upload-artifact@v4
2026-06-06T05:01:33.1643994Z with:
2026-06-06T05:01:33.1644220Z   name: validated-premarket-report
2026-06-06T05:01:33.1644516Z   path: reports/premarket-report.md
2026-06-06T05:01:33.1644785Z   retention-days: 14
2026-06-06T05:01:33.1645199Z   if-no-files-found: warn
2026-06-06T05:01:33.1645442Z   compression-level: 6
2026-06-06T05:01:33.1645675Z   overwrite: false
2026-06-06T05:01:33.1645897Z   include-hidden-files: false
2026-06-06T05:01:33.1646140Z env:
2026-06-06T05:01:33.1646450Z   POLYGON_API_KEY: ***
```

## Report Quality Validation

- Run ID: `27053169467`
- Branch: `fix/bt-evidence-pack-gate`
- Commit: `f0473781ed68`
- Title: BT130 real historical backtest evidence pack gate
- Created: 2026-06-06T04:57:20Z
- Updated: 2026-06-06T04:58:36Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27053169467

### Failed job: validate-reports (weekly)

- Job ID: `79852389410`
- Started: 2026-06-06T04:57:22Z
- Completed: 2026-06-06T04:57:47Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-06T04:57:43.4520012Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-06T04:57:43.4520401Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-06T04:57:43.4520847Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-06T04:57:43.4521189Z ##[endgroup]
2026-06-06T04:57:43.7740358Z Traceback (most recent call last):
2026-06-06T04:57:43.7748897Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 391, in <module>
2026-06-06T04:57:43.7750052Z     raise SystemExit(main())
2026-06-06T04:57:43.7750443Z                      ^^^^^^
2026-06-06T04:57:43.7751421Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 374, in main
2026-06-06T04:57:43.7752592Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-06T04:57:43.7753320Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-06T04:57:43.7754537Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 108, in write_report_text_guarded
2026-06-06T04:57:43.7755786Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-06T04:57:43.7757197Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-06T04:57:43.7758614Z     raise ReportOutputBoundaryError(
2026-06-06T04:57:43.7760857Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
```

```text
2026-06-06T04:57:43.7755786Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-06T04:57:43.7757197Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-06T04:57:43.7758614Z     raise ReportOutputBoundaryError(
2026-06-06T04:57:43.7760857Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
2026-06-06T04:57:43.7963555Z ##[error]Process completed with exit code 1.
2026-06-06T04:57:43.8050503Z ##[group]Run actions/upload-artifact@v4
2026-06-06T04:57:43.8050800Z with:
2026-06-06T04:57:43.8051009Z   name: validated-weekly-report
2026-06-06T04:57:43.8051278Z   path: reports/weekly-report.md
2026-06-06T04:57:43.8051536Z   retention-days: 14
2026-06-06T04:57:43.8051763Z   if-no-files-found: warn
2026-06-06T04:57:43.8051997Z   compression-level: 6
2026-06-06T04:57:43.8052253Z   overwrite: false
2026-06-06T04:57:43.8052472Z   include-hidden-files: false
2026-06-06T04:57:43.8052711Z env:
2026-06-06T04:57:43.8053040Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (premarket)

- Job ID: `79852389415`
- Started: 2026-06-06T04:57:22Z
- Completed: 2026-06-06T04:58:35Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-06T04:57:42.3446077Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-06T04:57:42.3446374Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-06T04:57:42.3446715Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-06T04:57:42.3446975Z ##[endgroup]
2026-06-06T04:58:31.9541511Z Traceback (most recent call last):
2026-06-06T04:58:31.9547811Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 391, in <module>
2026-06-06T04:58:31.9549160Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-02/2026-06-06?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-06T04:58:31.9550408Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-02/2026-06-06?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-06T04:58:31.9551925Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-02/2026-06-06?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-06T04:58:31.9552807Z     raise SystemExit(main())
2026-06-06T04:58:31.9553190Z                      ^^^^^^
2026-06-06T04:58:31.9553951Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 374, in main
2026-06-06T04:58:31.9554776Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-06T04:58:31.9555290Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-06T04:58:31.9556199Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 108, in write_report_text_guarded
2026-06-06T04:58:31.9557253Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
```

```text
2026-06-06T04:58:31.9557253Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-06T04:58:31.9558208Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-06T04:58:31.9558935Z     raise ReportOutputBoundaryError(
2026-06-06T04:58:31.9560314Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/premarket-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
2026-06-06T04:58:32.0279957Z ##[error]Process completed with exit code 1.
2026-06-06T04:58:32.0351848Z ##[group]Run actions/upload-artifact@v4
2026-06-06T04:58:32.0352104Z with:
2026-06-06T04:58:32.0352285Z   name: validated-premarket-report
2026-06-06T04:58:32.0352517Z   path: reports/premarket-report.md
2026-06-06T04:58:32.0352766Z   retention-days: 14
2026-06-06T04:58:32.0352957Z   if-no-files-found: warn
2026-06-06T04:58:32.0353148Z   compression-level: 6
2026-06-06T04:58:32.0353335Z   overwrite: false
2026-06-06T04:58:32.0353516Z   include-hidden-files: false
2026-06-06T04:58:32.0353710Z env:
2026-06-06T04:58:32.0354023Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (postmarket)

- Job ID: `79852389420`
- Started: 2026-06-06T04:57:22Z
- Completed: 2026-06-06T04:58:31Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-06T04:57:41.4371360Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-06T04:57:41.4371761Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-06T04:57:41.4372213Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-06T04:57:41.4372548Z ##[endgroup]
2026-06-06T04:58:28.5389930Z Traceback (most recent call last):
2026-06-06T04:58:28.5392761Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-02/2026-06-06?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-06T04:58:28.5400472Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 391, in <module>
2026-06-06T04:58:28.5401623Z     raise SystemExit(main())
2026-06-06T04:58:28.5401898Z                      ^^^^^^
2026-06-06T04:58:28.5402583Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 374, in main
2026-06-06T04:58:28.5403376Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-06T04:58:28.5403846Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-06T04:58:28.5404614Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 108, in write_report_text_guarded
2026-06-06T04:58:28.5406002Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-02/2026-06-06?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-06T04:58:28.5407399Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-02/2026-06-06?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-06T04:58:28.5408575Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
```

```text
2026-06-06T04:58:28.5408575Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-06T04:58:28.5409456Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-06T04:58:28.5410211Z     raise ReportOutputBoundaryError(
2026-06-06T04:58:28.5411891Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/postmarket-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
2026-06-06T04:58:28.6043794Z ##[error]Process completed with exit code 1.
2026-06-06T04:58:28.6127564Z ##[group]Run actions/upload-artifact@v4
2026-06-06T04:58:28.6127884Z with:
2026-06-06T04:58:28.6128109Z   name: validated-postmarket-report
2026-06-06T04:58:28.6128404Z   path: reports/postmarket-report.md
2026-06-06T04:58:28.6128693Z   retention-days: 14
2026-06-06T04:58:28.6128922Z   if-no-files-found: warn
2026-06-06T04:58:28.6129158Z   compression-level: 6
2026-06-06T04:58:28.6129386Z   overwrite: false
2026-06-06T04:58:28.6129614Z   include-hidden-files: false
2026-06-06T04:58:28.6129854Z env:
2026-06-06T04:58:28.6130161Z   POLYGON_API_KEY: ***
```

## CI

- Run ID: `27053103590`
- Branch: `fix/bt-evidence-pack-gate`
- Commit: `b8d3fe97ad38`
- Title: BT130 real historical backtest evidence pack gate
- Created: 2026-06-06T04:54:08Z
- Updated: 2026-06-06T04:54:42Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27053103590

### Failed job: Pytest

- Job ID: `79852225084`
- Started: 2026-06-06T04:54:10Z
- Completed: 2026-06-06T04:54:41Z
- Failed steps: 16. Roadmap EV completion guard tests

#### Error context

```text
2026-06-06T04:54:37.1389354Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-06T04:54:37.1389697Z   POLYGON_API_KEY: test-key
2026-06-06T04:54:37.1389938Z ##[endgroup]
2026-06-06T04:54:37.3959052Z .F                                                                       [100%]
2026-06-06T04:54:37.3959566Z =================================== FAILURES ===================================
2026-06-06T04:54:37.3960232Z _______ test_roadmap_current_focus_no_longer_points_to_old_ev_next_block _______
2026-06-06T04:54:37.3960666Z 
2026-06-06T04:54:37.3961069Z     def test_roadmap_current_focus_no_longer_points_to_old_ev_next_block() -> None:
2026-06-06T04:54:37.3961745Z         roadmap = ROADMAP.read_text(encoding="utf-8")
2026-06-06T04:54:37.3962196Z     
2026-06-06T04:54:37.3962452Z         stale_phrases = [
2026-06-06T04:54:37.3962777Z             "EV3-EV6 are the next critical backtest-fidelity block",
2026-06-06T04:54:37.3963130Z             "get EV1-EV2 CI-green",
2026-06-06T04:54:37.3963428Z             "After EV1-EV2 are green",
2026-06-06T04:54:37.3963937Z             "Planned / Next",
2026-06-06T04:54:37.3964304Z         ]
```

```text
2026-06-06T04:54:37.3965506Z             assert phrase not in roadmap
2026-06-06T04:54:37.3965978Z     
2026-06-06T04:54:37.3966378Z         assert "EV1-EV12 evidence-integrity remediation" in roadmap
2026-06-06T04:54:37.3967010Z >       assert "CI runtime simplification" in roadmap
2026-06-06T04:54:37.3968510Z E       AssertionError: assert 'CI runtime simplification' in '# Institutional Trading Engine Roadmap\n\nStatus date: 2026-06-06\n\nCurrent state: TEST1 Evidence-Oriented TDD Polic...tal allocation or production deployment.\n\nThe system remains research / decision-support / paper-observation only.\n'
2026-06-06T04:54:37.4035231Z 
2026-06-06T04:54:37.4035582Z tests/test_roadmap_ev_completion_guard.py:47: AssertionError
2026-06-06T04:54:37.4036307Z =========================== short test summary info ============================
2026-06-06T04:54:37.4038937Z FAILED tests/test_roadmap_ev_completion_guard.py::test_roadmap_current_focus_no_longer_points_to_old_ev_next_block - AssertionError: assert 'CI runtime simplification' in '# Institutional Trading Engine Roadmap\n\nStatus date: 2026-06-06\n\nCurrent state: TEST1 Evidence-Oriented TDD Polic...tal allocation or production deployment.\n\nThe system remains research / decision-support / paper-observation only.\n'
2026-06-06T04:54:37.4041387Z 1 failed, 1 passed in 0.05s
2026-06-06T04:54:37.4326809Z ##[error]Process completed with exit code 1.
2026-06-06T04:54:37.4517806Z ##[group]Run actions/upload-artifact@v4
2026-06-06T04:54:37.4518111Z with:
2026-06-06T04:54:37.4518494Z   name: p109-residual-pytest-evidence
2026-06-06T04:54:37.4518816Z   path: artifacts/evidence/p109-residual-pytest/
2026-06-06T04:54:37.4519136Z   if-no-files-found: warn
```

```text
2026-06-06T04:54:37.3966378Z         assert "EV1-EV12 evidence-integrity remediation" in roadmap
2026-06-06T04:54:37.3967010Z >       assert "CI runtime simplification" in roadmap
2026-06-06T04:54:37.3968510Z E       AssertionError: assert 'CI runtime simplification' in '# Institutional Trading Engine Roadmap\n\nStatus date: 2026-06-06\n\nCurrent state: TEST1 Evidence-Oriented TDD Polic...tal allocation or production deployment.\n\nThe system remains research / decision-support / paper-observation only.\n'
2026-06-06T04:54:37.4035231Z 
2026-06-06T04:54:37.4035582Z tests/test_roadmap_ev_completion_guard.py:47: AssertionError
2026-06-06T04:54:37.4036307Z =========================== short test summary info ============================
2026-06-06T04:54:37.4038937Z FAILED tests/test_roadmap_ev_completion_guard.py::test_roadmap_current_focus_no_longer_points_to_old_ev_next_block - AssertionError: assert 'CI runtime simplification' in '# Institutional Trading Engine Roadmap\n\nStatus date: 2026-06-06\n\nCurrent state: TEST1 Evidence-Oriented TDD Polic...tal allocation or production deployment.\n\nThe system remains research / decision-support / paper-observation only.\n'
2026-06-06T04:54:37.4041387Z 1 failed, 1 passed in 0.05s
2026-06-06T04:54:37.4326809Z ##[error]Process completed with exit code 1.
2026-06-06T04:54:37.4517806Z ##[group]Run actions/upload-artifact@v4
2026-06-06T04:54:37.4518111Z with:
2026-06-06T04:54:37.4518494Z   name: p109-residual-pytest-evidence
2026-06-06T04:54:37.4518816Z   path: artifacts/evidence/p109-residual-pytest/
2026-06-06T04:54:37.4519136Z   if-no-files-found: warn
2026-06-06T04:54:37.4519385Z   compression-level: 6
2026-06-06T04:54:37.4519624Z   overwrite: false
```

```text
2026-06-06T04:54:37.3968510Z E       AssertionError: assert 'CI runtime simplification' in '# Institutional Trading Engine Roadmap\n\nStatus date: 2026-06-06\n\nCurrent state: TEST1 Evidence-Oriented TDD Polic...tal allocation or production deployment.\n\nThe system remains research / decision-support / paper-observation only.\n'
2026-06-06T04:54:37.4035231Z 
2026-06-06T04:54:37.4035582Z tests/test_roadmap_ev_completion_guard.py:47: AssertionError
2026-06-06T04:54:37.4036307Z =========================== short test summary info ============================
2026-06-06T04:54:37.4038937Z FAILED tests/test_roadmap_ev_completion_guard.py::test_roadmap_current_focus_no_longer_points_to_old_ev_next_block - AssertionError: assert 'CI runtime simplification' in '# Institutional Trading Engine Roadmap\n\nStatus date: 2026-06-06\n\nCurrent state: TEST1 Evidence-Oriented TDD Polic...tal allocation or production deployment.\n\nThe system remains research / decision-support / paper-observation only.\n'
2026-06-06T04:54:37.4041387Z 1 failed, 1 passed in 0.05s
2026-06-06T04:54:37.4326809Z ##[error]Process completed with exit code 1.
2026-06-06T04:54:37.4517806Z ##[group]Run actions/upload-artifact@v4
2026-06-06T04:54:37.4518111Z with:
2026-06-06T04:54:37.4518494Z   name: p109-residual-pytest-evidence
2026-06-06T04:54:37.4518816Z   path: artifacts/evidence/p109-residual-pytest/
2026-06-06T04:54:37.4519136Z   if-no-files-found: warn
2026-06-06T04:54:37.4519385Z   compression-level: 6
2026-06-06T04:54:37.4519624Z   overwrite: false
2026-06-06T04:54:37.4519857Z   include-hidden-files: false
2026-06-06T04:54:37.4520101Z env:
```

```text
2026-06-06T04:54:37.4035582Z tests/test_roadmap_ev_completion_guard.py:47: AssertionError
2026-06-06T04:54:37.4036307Z =========================== short test summary info ============================
2026-06-06T04:54:37.4038937Z FAILED tests/test_roadmap_ev_completion_guard.py::test_roadmap_current_focus_no_longer_points_to_old_ev_next_block - AssertionError: assert 'CI runtime simplification' in '# Institutional Trading Engine Roadmap\n\nStatus date: 2026-06-06\n\nCurrent state: TEST1 Evidence-Oriented TDD Polic...tal allocation or production deployment.\n\nThe system remains research / decision-support / paper-observation only.\n'
2026-06-06T04:54:37.4041387Z 1 failed, 1 passed in 0.05s
2026-06-06T04:54:37.4326809Z ##[error]Process completed with exit code 1.
2026-06-06T04:54:37.4517806Z ##[group]Run actions/upload-artifact@v4
2026-06-06T04:54:37.4518111Z with:
2026-06-06T04:54:37.4518494Z   name: p109-residual-pytest-evidence
2026-06-06T04:54:37.4518816Z   path: artifacts/evidence/p109-residual-pytest/
2026-06-06T04:54:37.4519136Z   if-no-files-found: warn
2026-06-06T04:54:37.4519385Z   compression-level: 6
2026-06-06T04:54:37.4519624Z   overwrite: false
2026-06-06T04:54:37.4519857Z   include-hidden-files: false
2026-06-06T04:54:37.4520101Z env:
2026-06-06T04:54:37.4520368Z   pythonLocation: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-06T04:54:37.4520803Z   PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib/pkgconfig
```

## Decision Engine Tests

- Run ID: `27053103586`
- Branch: `fix/bt-evidence-pack-gate`
- Commit: `b8d3fe97ad38`
- Title: BT130 real historical backtest evidence pack gate
- Created: 2026-06-06T04:54:08Z
- Updated: 2026-06-06T04:54:44Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27053103586

### Failed job: tests

- Job ID: `79852225086`
- Started: 2026-06-06T04:54:10Z
- Completed: 2026-06-06T04:54:44Z
- Failed steps: 5. Run pytest

#### Error context

```text
2026-06-06T04:54:41.6455753Z ........................................................................ [ 89%]
2026-06-06T04:54:41.8742744Z ........................................................................ [ 93%]
2026-06-06T04:54:41.9220606Z ........................................................................ [ 98%]
2026-06-06T04:54:41.9982245Z ..............................                                           [100%]
2026-06-06T04:54:41.9983412Z =================================== FAILURES ===================================
2026-06-06T04:54:41.9984411Z _______ test_roadmap_current_focus_no_longer_points_to_old_ev_next_block _______
2026-06-06T04:54:41.9985108Z 
2026-06-06T04:54:41.9985641Z     def test_roadmap_current_focus_no_longer_points_to_old_ev_next_block() -> None:
2026-06-06T04:54:41.9986636Z         roadmap = ROADMAP.read_text(encoding="utf-8")
2026-06-06T04:54:41.9987266Z     
2026-06-06T04:54:41.9987655Z         stale_phrases = [
2026-06-06T04:54:41.9988296Z             "EV3-EV6 are the next critical backtest-fidelity block",
2026-06-06T04:54:41.9989026Z             "get EV1-EV2 CI-green",
2026-06-06T04:54:41.9990402Z             "After EV1-EV2 are green",
2026-06-06T04:54:41.9990785Z             "Planned / Next",
2026-06-06T04:54:41.9991084Z         ]
```

```text
2026-06-06T04:54:41.9991912Z             assert phrase not in roadmap
2026-06-06T04:54:41.9992248Z     
2026-06-06T04:54:41.9992584Z         assert "EV1-EV12 evidence-integrity remediation" in roadmap
2026-06-06T04:54:41.9993089Z >       assert "CI runtime simplification" in roadmap
2026-06-06T04:54:41.9994477Z E       AssertionError: assert 'CI runtime simplification' in '# Institutional Trading Engine Roadmap\n\nStatus date: 2026-06-06\n\nCurrent state: TEST1 Evidence-Oriented TDD Polic...tal allocation or production deployment.\n\nThe system remains research / decision-support / paper-observation only.\n'
2026-06-06T04:54:41.9995588Z 
2026-06-06T04:54:41.9995784Z tests/test_roadmap_ev_completion_guard.py:47: AssertionError
2026-06-06T04:54:41.9996195Z =========================== short test summary info ============================
2026-06-06T04:54:41.9997926Z FAILED tests/test_roadmap_ev_completion_guard.py::test_roadmap_current_focus_no_longer_points_to_old_ev_next_block - AssertionError: assert 'CI runtime simplification' in '# Institutional Trading Engine Roadmap\n\nStatus date: 2026-06-06\n\nCurrent state: TEST1 Evidence-Oriented TDD Polic...tal allocation or production deployment.\n\nThe system remains research / decision-support / paper-observation only.\n'
2026-06-06T04:54:41.9999764Z 1 failed, 1684 passed, 1 skipped in 14.70s
2026-06-06T04:54:42.3663231Z ##[error]Process completed with exit code 1.
2026-06-06T04:54:42.3784521Z Post job cleanup.
2026-06-06T04:54:42.4784994Z [command]/usr/bin/git version
2026-06-06T04:54:42.4822423Z git version 2.54.0
2026-06-06T04:54:42.4875959Z Temporarily overriding HOME='/home/runner/work/_temp/22a009c9-69a1-4c74-b5d2-55a2c74c2f3f' before making global git config changes
2026-06-06T04:54:42.4877419Z Adding repository directory to the temporary git global config as a safe directory
```

```text
2026-06-06T04:54:41.9992584Z         assert "EV1-EV12 evidence-integrity remediation" in roadmap
2026-06-06T04:54:41.9993089Z >       assert "CI runtime simplification" in roadmap
2026-06-06T04:54:41.9994477Z E       AssertionError: assert 'CI runtime simplification' in '# Institutional Trading Engine Roadmap\n\nStatus date: 2026-06-06\n\nCurrent state: TEST1 Evidence-Oriented TDD Polic...tal allocation or production deployment.\n\nThe system remains research / decision-support / paper-observation only.\n'
2026-06-06T04:54:41.9995588Z 
2026-06-06T04:54:41.9995784Z tests/test_roadmap_ev_completion_guard.py:47: AssertionError
2026-06-06T04:54:41.9996195Z =========================== short test summary info ============================
2026-06-06T04:54:41.9997926Z FAILED tests/test_roadmap_ev_completion_guard.py::test_roadmap_current_focus_no_longer_points_to_old_ev_next_block - AssertionError: assert 'CI runtime simplification' in '# Institutional Trading Engine Roadmap\n\nStatus date: 2026-06-06\n\nCurrent state: TEST1 Evidence-Oriented TDD Polic...tal allocation or production deployment.\n\nThe system remains research / decision-support / paper-observation only.\n'
2026-06-06T04:54:41.9999764Z 1 failed, 1684 passed, 1 skipped in 14.70s
2026-06-06T04:54:42.3663231Z ##[error]Process completed with exit code 1.
2026-06-06T04:54:42.3784521Z Post job cleanup.
2026-06-06T04:54:42.4784994Z [command]/usr/bin/git version
2026-06-06T04:54:42.4822423Z git version 2.54.0
2026-06-06T04:54:42.4875959Z Temporarily overriding HOME='/home/runner/work/_temp/22a009c9-69a1-4c74-b5d2-55a2c74c2f3f' before making global git config changes
2026-06-06T04:54:42.4877419Z Adding repository directory to the temporary git global config as a safe directory
2026-06-06T04:54:42.4883401Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-06-06T04:54:42.4920461Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
```

```text
2026-06-06T04:54:41.9994477Z E       AssertionError: assert 'CI runtime simplification' in '# Institutional Trading Engine Roadmap\n\nStatus date: 2026-06-06\n\nCurrent state: TEST1 Evidence-Oriented TDD Polic...tal allocation or production deployment.\n\nThe system remains research / decision-support / paper-observation only.\n'
2026-06-06T04:54:41.9995588Z 
2026-06-06T04:54:41.9995784Z tests/test_roadmap_ev_completion_guard.py:47: AssertionError
2026-06-06T04:54:41.9996195Z =========================== short test summary info ============================
2026-06-06T04:54:41.9997926Z FAILED tests/test_roadmap_ev_completion_guard.py::test_roadmap_current_focus_no_longer_points_to_old_ev_next_block - AssertionError: assert 'CI runtime simplification' in '# Institutional Trading Engine Roadmap\n\nStatus date: 2026-06-06\n\nCurrent state: TEST1 Evidence-Oriented TDD Polic...tal allocation or production deployment.\n\nThe system remains research / decision-support / paper-observation only.\n'
2026-06-06T04:54:41.9999764Z 1 failed, 1684 passed, 1 skipped in 14.70s
2026-06-06T04:54:42.3663231Z ##[error]Process completed with exit code 1.
2026-06-06T04:54:42.3784521Z Post job cleanup.
2026-06-06T04:54:42.4784994Z [command]/usr/bin/git version
2026-06-06T04:54:42.4822423Z git version 2.54.0
2026-06-06T04:54:42.4875959Z Temporarily overriding HOME='/home/runner/work/_temp/22a009c9-69a1-4c74-b5d2-55a2c74c2f3f' before making global git config changes
2026-06-06T04:54:42.4877419Z Adding repository directory to the temporary git global config as a safe directory
2026-06-06T04:54:42.4883401Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-06-06T04:54:42.4920461Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-06-06T04:54:42.4954452Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-06-06T04:54:42.5188277Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
```

```text
2026-06-06T04:54:41.9995784Z tests/test_roadmap_ev_completion_guard.py:47: AssertionError
2026-06-06T04:54:41.9996195Z =========================== short test summary info ============================
2026-06-06T04:54:41.9997926Z FAILED tests/test_roadmap_ev_completion_guard.py::test_roadmap_current_focus_no_longer_points_to_old_ev_next_block - AssertionError: assert 'CI runtime simplification' in '# Institutional Trading Engine Roadmap\n\nStatus date: 2026-06-06\n\nCurrent state: TEST1 Evidence-Oriented TDD Polic...tal allocation or production deployment.\n\nThe system remains research / decision-support / paper-observation only.\n'
2026-06-06T04:54:41.9999764Z 1 failed, 1684 passed, 1 skipped in 14.70s
2026-06-06T04:54:42.3663231Z ##[error]Process completed with exit code 1.
2026-06-06T04:54:42.3784521Z Post job cleanup.
2026-06-06T04:54:42.4784994Z [command]/usr/bin/git version
2026-06-06T04:54:42.4822423Z git version 2.54.0
2026-06-06T04:54:42.4875959Z Temporarily overriding HOME='/home/runner/work/_temp/22a009c9-69a1-4c74-b5d2-55a2c74c2f3f' before making global git config changes
2026-06-06T04:54:42.4877419Z Adding repository directory to the temporary git global config as a safe directory
2026-06-06T04:54:42.4883401Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-06-06T04:54:42.4920461Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-06-06T04:54:42.4954452Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-06-06T04:54:42.5188277Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-06-06T04:54:42.5215622Z http.https://github.com/.extraheader
2026-06-06T04:54:42.5228548Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

## Report Quality Validation

- Run ID: `27053103602`
- Branch: `fix/bt-evidence-pack-gate`
- Commit: `b8d3fe97ad38`
- Title: BT130 real historical backtest evidence pack gate
- Created: 2026-06-06T04:54:08Z
- Updated: 2026-06-06T04:55:21Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27053103602

### Failed job: validate-reports (premarket)

- Job ID: `79852225176`
- Started: 2026-06-06T04:54:10Z
- Completed: 2026-06-06T04:55:09Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-06T04:54:27.5730256Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-06T04:54:27.5730633Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-06T04:54:27.5731051Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-06T04:54:27.5731378Z ##[endgroup]
2026-06-06T04:55:07.4538052Z Traceback (most recent call last):
2026-06-06T04:55:07.4539987Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-02/2026-06-06?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-06T04:55:07.4549114Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 391, in <module>
2026-06-06T04:55:07.4551179Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-02/2026-06-06?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-06T04:55:07.4552936Z     raise SystemExit(main())
2026-06-06T04:55:07.4554288Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-02/2026-06-06?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-06T04:55:07.4555546Z                      ^^^^^^
2026-06-06T04:55:07.4556455Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 374, in main
2026-06-06T04:55:07.4557601Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-06T04:55:07.4558249Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-06T04:55:07.4559365Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 108, in write_report_text_guarded
2026-06-06T04:55:07.4560889Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
```

```text
2026-06-06T04:55:07.4560889Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-06T04:55:07.4562490Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-06T04:55:07.4563634Z     raise ReportOutputBoundaryError(
2026-06-06T04:55:07.4565777Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/premarket-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
2026-06-06T04:55:07.5145492Z ##[error]Process completed with exit code 1.
2026-06-06T04:55:07.5230763Z ##[group]Run actions/upload-artifact@v4
2026-06-06T04:55:07.5231053Z with:
2026-06-06T04:55:07.5231274Z   name: validated-premarket-report
2026-06-06T04:55:07.5231559Z   path: reports/premarket-report.md
2026-06-06T04:55:07.5232098Z   retention-days: 14
2026-06-06T04:55:07.5232331Z   if-no-files-found: warn
2026-06-06T04:55:07.5232564Z   compression-level: 6
2026-06-06T04:55:07.5232784Z   overwrite: false
2026-06-06T04:55:07.5233009Z   include-hidden-files: false
2026-06-06T04:55:07.5233248Z env:
2026-06-06T04:55:07.5233603Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (postmarket)

- Job ID: `79852225177`
- Started: 2026-06-06T04:54:10Z
- Completed: 2026-06-06T04:55:20Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-06T04:54:30.1891220Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-06T04:54:30.1891623Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-06T04:54:30.1892077Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-06T04:54:30.1892428Z ##[endgroup]
2026-06-06T04:55:17.5451556Z Traceback (most recent call last):
2026-06-06T04:55:17.5455469Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-02/2026-06-06?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-06T04:55:17.5464437Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 391, in <module>
2026-06-06T04:55:17.5465466Z     raise SystemExit(main())
2026-06-06T04:55:17.5465820Z                      ^^^^^^
2026-06-06T04:55:17.5466765Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 374, in main
2026-06-06T04:55:17.5467935Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-06T04:55:17.5469563Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-02/2026-06-06?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-06T04:55:17.5471877Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-02/2026-06-06?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-06T04:55:17.5473065Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-06T04:55:17.5474221Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 108, in write_report_text_guarded
2026-06-06T04:55:17.5475731Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
```

```text
2026-06-06T04:55:17.5475731Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-06T04:55:17.5476980Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-06T04:55:17.5478092Z     raise ReportOutputBoundaryError(
2026-06-06T04:55:17.5480215Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/postmarket-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
2026-06-06T04:55:17.6066911Z ##[error]Process completed with exit code 1.
2026-06-06T04:55:17.6154249Z ##[group]Run actions/upload-artifact@v4
2026-06-06T04:55:17.6154536Z with:
2026-06-06T04:55:17.6154758Z   name: validated-postmarket-report
2026-06-06T04:55:17.6155048Z   path: reports/postmarket-report.md
2026-06-06T04:55:17.6155329Z   retention-days: 14
2026-06-06T04:55:17.6155571Z   if-no-files-found: warn
2026-06-06T04:55:17.6155817Z   compression-level: 6
2026-06-06T04:55:17.6156048Z   overwrite: false
2026-06-06T04:55:17.6156278Z   include-hidden-files: false
2026-06-06T04:55:17.6156518Z env:
2026-06-06T04:55:17.6156871Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (weekly)

- Job ID: `79852225181`
- Started: 2026-06-06T04:54:10Z
- Completed: 2026-06-06T04:54:27Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-06T04:54:25.0373672Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-06T04:54:25.0374031Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-06T04:54:25.0374445Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-06T04:54:25.0374747Z ##[endgroup]
2026-06-06T04:54:25.3338096Z Traceback (most recent call last):
2026-06-06T04:54:25.3344250Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 391, in <module>
2026-06-06T04:54:25.3345037Z     raise SystemExit(main())
2026-06-06T04:54:25.3345288Z                      ^^^^^^
2026-06-06T04:54:25.3345848Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 374, in main
2026-06-06T04:54:25.3346525Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-06T04:54:25.3346979Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-06T04:54:25.3347695Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 108, in write_report_text_guarded
2026-06-06T04:54:25.3348434Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-06T04:54:25.3349213Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-06T04:54:25.3349889Z     raise ReportOutputBoundaryError(
2026-06-06T04:54:25.3351296Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
```

```text
2026-06-06T04:54:25.3348434Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-06T04:54:25.3349213Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-06T04:54:25.3349889Z     raise ReportOutputBoundaryError(
2026-06-06T04:54:25.3351296Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
2026-06-06T04:54:25.3612347Z ##[error]Process completed with exit code 1.
2026-06-06T04:54:25.3698122Z ##[group]Run actions/upload-artifact@v4
2026-06-06T04:54:25.3698406Z with:
2026-06-06T04:54:25.3698614Z   name: validated-weekly-report
2026-06-06T04:54:25.3698882Z   path: reports/weekly-report.md
2026-06-06T04:54:25.3699125Z   retention-days: 14
2026-06-06T04:54:25.3699340Z   if-no-files-found: warn
2026-06-06T04:54:25.3699572Z   compression-level: 6
2026-06-06T04:54:25.3699785Z   overwrite: false
2026-06-06T04:54:25.3699993Z   include-hidden-files: false
2026-06-06T04:54:25.3700414Z env:
2026-06-06T04:54:25.3700770Z   POLYGON_API_KEY: ***
```

## Report Quality Validation

- Run ID: `27052171009`
- Branch: `main`
- Commit: `f4f419a12570`
- Title: Merge pull request #135 from yalcinkadir/fix/po129-validator-backcompat
- Created: 2026-06-06T04:08:58Z
- Updated: 2026-06-06T04:10:03Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27052171009

### Failed job: validate-reports (postmarket)

- Job ID: `79849727937`
- Started: 2026-06-06T04:09:01Z
- Completed: 2026-06-06T04:10:02Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-06T04:09:19.3650224Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-06T04:09:19.3650640Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-06T04:09:19.3651075Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-06T04:09:19.3651425Z ##[endgroup]
2026-06-06T04:10:00.1167932Z Traceback (most recent call last):
2026-06-06T04:10:00.1170392Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-02/2026-06-06?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-06T04:10:00.1179957Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 391, in <module>
2026-06-06T04:10:00.1180833Z     raise SystemExit(main())
2026-06-06T04:10:00.1181137Z                      ^^^^^^
2026-06-06T04:10:00.1181896Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 374, in main
2026-06-06T04:10:00.1183269Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-06T04:10:00.1183852Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-06T04:10:00.1184833Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 108, in write_report_text_guarded
2026-06-06T04:10:00.1185820Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-06T04:10:00.1186878Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-06T04:10:00.1187807Z     raise ReportOutputBoundaryError(
```

```text
2026-06-06T04:10:00.1187807Z     raise ReportOutputBoundaryError(
2026-06-06T04:10:00.1189244Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/postmarket-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
2026-06-06T04:10:00.1191399Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-02/2026-06-06?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-06T04:10:00.1193220Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-02/2026-06-06?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-06T04:10:00.1728742Z ##[error]Process completed with exit code 1.
2026-06-06T04:10:00.1812157Z ##[group]Run actions/upload-artifact@v4
2026-06-06T04:10:00.1812783Z with:
2026-06-06T04:10:00.1813034Z   name: validated-postmarket-report
2026-06-06T04:10:00.1813348Z   path: reports/postmarket-report.md
2026-06-06T04:10:00.1813826Z   retention-days: 14
2026-06-06T04:10:00.1814065Z   if-no-files-found: warn
2026-06-06T04:10:00.1814315Z   compression-level: 6
2026-06-06T04:10:00.1814548Z   overwrite: false
2026-06-06T04:10:00.1814776Z   include-hidden-files: false
2026-06-06T04:10:00.1815017Z env:
2026-06-06T04:10:00.1815337Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (premarket)

- Job ID: `79849727938`
- Started: 2026-06-06T04:09:00Z
- Completed: 2026-06-06T04:09:57Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-06T04:09:16.3341899Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-06T04:09:16.3342305Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-06T04:09:16.3342758Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-06T04:09:16.3343095Z ##[endgroup]
2026-06-06T04:09:55.3225299Z Traceback (most recent call last):
2026-06-06T04:09:55.3226714Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-02/2026-06-06?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-06T04:09:55.3236889Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 391, in <module>
2026-06-06T04:09:55.3238274Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-02/2026-06-06?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-06T04:09:55.3240129Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-02/2026-06-06?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-06T04:09:55.3241082Z     raise SystemExit(main())
2026-06-06T04:09:55.3241360Z                      ^^^^^^
2026-06-06T04:09:55.3242005Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 374, in main
2026-06-06T04:09:55.3242747Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-06T04:09:55.3243203Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-06T04:09:55.3243977Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 108, in write_report_text_guarded
2026-06-06T04:09:55.3244767Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
```

```text
2026-06-06T04:09:55.3244767Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-06T04:09:55.3245598Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-06T04:09:55.3246337Z     raise ReportOutputBoundaryError(
2026-06-06T04:09:55.3247675Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/premarket-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
2026-06-06T04:09:55.3958043Z ##[error]Process completed with exit code 1.
2026-06-06T04:09:55.4047299Z ##[group]Run actions/upload-artifact@v4
2026-06-06T04:09:55.4047606Z with:
2026-06-06T04:09:55.4047845Z   name: validated-premarket-report
2026-06-06T04:09:55.4048148Z   path: reports/premarket-report.md
2026-06-06T04:09:55.4048424Z   retention-days: 14
2026-06-06T04:09:55.4049012Z   if-no-files-found: warn
2026-06-06T04:09:55.4049263Z   compression-level: 6
2026-06-06T04:09:55.4049503Z   overwrite: false
2026-06-06T04:09:55.4049736Z   include-hidden-files: false
2026-06-06T04:09:55.4049989Z env:
2026-06-06T04:09:55.4050327Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (weekly)

- Job ID: `79849727942`
- Started: 2026-06-06T04:09:02Z
- Completed: 2026-06-06T04:09:28Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-06T04:09:24.3071765Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-06T04:09:24.3072150Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-06T04:09:24.3072564Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-06T04:09:24.3072887Z ##[endgroup]
2026-06-06T04:09:25.0781130Z Traceback (most recent call last):
2026-06-06T04:09:25.0790283Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 391, in <module>
2026-06-06T04:09:25.0791365Z     raise SystemExit(main())
2026-06-06T04:09:25.0791737Z                      ^^^^^^
2026-06-06T04:09:25.0807330Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 374, in main
2026-06-06T04:09:25.0826842Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-06T04:09:25.0856670Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-06T04:09:25.0867768Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 108, in write_report_text_guarded
2026-06-06T04:09:25.0869029Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-06T04:09:25.0870562Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-06T04:09:25.0871861Z     raise ReportOutputBoundaryError(
2026-06-06T04:09:25.0873872Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
```

```text
2026-06-06T04:09:25.0869029Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-06T04:09:25.0870562Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-06T04:09:25.0871861Z     raise ReportOutputBoundaryError(
2026-06-06T04:09:25.0873872Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
2026-06-06T04:09:25.1000683Z ##[error]Process completed with exit code 1.
2026-06-06T04:09:25.1086463Z ##[group]Run actions/upload-artifact@v4
2026-06-06T04:09:25.1086780Z with:
2026-06-06T04:09:25.1086995Z   name: validated-weekly-report
2026-06-06T04:09:25.1087266Z   path: reports/weekly-report.md
2026-06-06T04:09:25.1087519Z   retention-days: 14
2026-06-06T04:09:25.1087742Z   if-no-files-found: warn
2026-06-06T04:09:25.1087975Z   compression-level: 6
2026-06-06T04:09:25.1088198Z   overwrite: false
2026-06-06T04:09:25.1088417Z   include-hidden-files: false
2026-06-06T04:09:25.1088649Z env:
2026-06-06T04:09:25.1088984Z   POLYGON_API_KEY: ***
```
