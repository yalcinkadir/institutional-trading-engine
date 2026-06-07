# GitHub Actions Workflow Error Report

Generated: 2026-06-07 08:24 UTC
Repository: `yalcinkadir/institutional-trading-engine`
Filter since: 2026-06-06 08:24 UTC
Failed runs included: 10

## Report Quality Validation

- Run ID: `27085302075`
- Branch: `main`
- Commit: `4c37bcdd6dac`
- Title: P124 align P121 real-data fixture with health fields
- Created: 2026-06-07T06:47:11Z
- Updated: 2026-06-07T06:48:25Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27085302075

### Failed job: validate-reports (premarket)

- Job ID: `79938528713`
- Started: 2026-06-07T06:47:14Z
- Completed: 2026-06-07T06:48:13Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-07T06:47:29.8604365Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-07T06:47:29.8604757Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-07T06:47:29.8605182Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-07T06:47:29.8605509Z ##[endgroup]
2026-06-07T06:48:11.5421332Z Traceback (most recent call last):
2026-06-07T06:48:11.5423776Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-03/2026-06-07?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-07T06:48:11.5437043Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 491, in <module>
2026-06-07T06:48:11.5438127Z     raise SystemExit(main())
2026-06-07T06:48:11.5438489Z                      ^^^^^^
2026-06-07T06:48:11.5439431Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 474, in main
2026-06-07T06:48:11.5441543Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-03/2026-06-07?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-07T06:48:11.5444172Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-03/2026-06-07?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-07T06:48:11.5445674Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-07T06:48:11.5446402Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-07T06:48:11.5447644Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 108, in write_report_text_guarded
2026-06-07T06:48:11.5448902Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
```

```text
2026-06-07T06:48:11.5448902Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-07T06:48:11.5450274Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-07T06:48:11.5451487Z     raise ReportOutputBoundaryError(
2026-06-07T06:48:11.5453905Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/premarket-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
2026-06-07T06:48:11.5980048Z ##[error]Process completed with exit code 1.
2026-06-07T06:48:11.6065113Z ##[group]Run actions/upload-artifact@v4
2026-06-07T06:48:11.6065417Z with:
2026-06-07T06:48:11.6065633Z   name: validated-premarket-report
2026-06-07T06:48:11.6065914Z   path: reports/premarket-report.md
2026-06-07T06:48:11.6066356Z   retention-days: 14
2026-06-07T06:48:11.6066575Z   if-no-files-found: warn
2026-06-07T06:48:11.6066807Z   compression-level: 6
2026-06-07T06:48:11.6067026Z   overwrite: false
2026-06-07T06:48:11.6067237Z   include-hidden-files: false
2026-06-07T06:48:11.6067467Z env:
2026-06-07T06:48:11.6067801Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (weekly)

- Job ID: `79938528714`
- Started: 2026-06-07T06:47:13Z
- Completed: 2026-06-07T06:47:32Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-07T06:47:30.3090203Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-07T06:47:30.3090609Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-07T06:47:30.3091036Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-07T06:47:30.3091363Z ##[endgroup]
2026-06-07T06:47:31.0342428Z Traceback (most recent call last):
2026-06-07T06:47:31.0350524Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 491, in <module>
2026-06-07T06:47:31.0351476Z     raise SystemExit(main())
2026-06-07T06:47:31.0351791Z                      ^^^^^^
2026-06-07T06:47:31.0352602Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 474, in main
2026-06-07T06:47:31.0353594Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-07T06:47:31.0354179Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-07T06:47:31.0355197Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 108, in write_report_text_guarded
2026-06-07T06:47:31.0357181Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-07T06:47:31.0358470Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-07T06:47:31.0359235Z     raise ReportOutputBoundaryError(
2026-06-07T06:47:31.0360596Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
```

```text
2026-06-07T06:47:31.0357181Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-07T06:47:31.0358470Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-07T06:47:31.0359235Z     raise ReportOutputBoundaryError(
2026-06-07T06:47:31.0360596Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
2026-06-07T06:47:31.0565442Z ##[error]Process completed with exit code 1.
2026-06-07T06:47:31.0649133Z ##[group]Run actions/upload-artifact@v4
2026-06-07T06:47:31.0649420Z with:
2026-06-07T06:47:31.0649622Z   name: validated-weekly-report
2026-06-07T06:47:31.0649889Z   path: reports/weekly-report.md
2026-06-07T06:47:31.0650134Z   retention-days: 14
2026-06-07T06:47:31.0650349Z   if-no-files-found: warn
2026-06-07T06:47:31.0650578Z   compression-level: 6
2026-06-07T06:47:31.0650792Z   overwrite: false
2026-06-07T06:47:31.0651001Z   include-hidden-files: false
2026-06-07T06:47:31.0651226Z env:
2026-06-07T06:47:31.0651559Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (postmarket)

- Job ID: `79938528722`
- Started: 2026-06-07T06:47:14Z
- Completed: 2026-06-07T06:48:24Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-07T06:47:31.8671327Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-07T06:47:31.8671715Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-07T06:47:31.8672129Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-07T06:47:31.8672465Z ##[endgroup]
2026-06-07T06:48:21.2277951Z Traceback (most recent call last):
2026-06-07T06:48:21.2280234Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-03/2026-06-07?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-07T06:48:21.2289837Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 491, in <module>
2026-06-07T06:48:21.2290722Z     raise SystemExit(main())
2026-06-07T06:48:21.2291017Z                      ^^^^^^
2026-06-07T06:48:21.2291784Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 474, in main
2026-06-07T06:48:21.2292752Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-07T06:48:21.2293317Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-07T06:48:21.2294273Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 108, in write_report_text_guarded
2026-06-07T06:48:21.2295253Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-07T06:48:21.2296301Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-07T06:48:21.2297233Z     raise ReportOutputBoundaryError(
```

```text
2026-06-07T06:48:21.2297233Z     raise ReportOutputBoundaryError(
2026-06-07T06:48:21.2298876Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-03/2026-06-07?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-07T06:48:21.2300641Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-03/2026-06-07?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-07T06:48:21.2302566Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/postmarket-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
2026-06-07T06:48:21.2894589Z ##[error]Process completed with exit code 1.
2026-06-07T06:48:21.2979444Z ##[group]Run actions/upload-artifact@v4
2026-06-07T06:48:21.2979752Z with:
2026-06-07T06:48:21.2979966Z   name: validated-postmarket-report
2026-06-07T06:48:21.2980247Z   path: reports/postmarket-report.md
2026-06-07T06:48:21.2980515Z   retention-days: 14
2026-06-07T06:48:21.2980920Z   if-no-files-found: warn
2026-06-07T06:48:21.2981151Z   compression-level: 6
2026-06-07T06:48:21.2981363Z   overwrite: false
2026-06-07T06:48:21.2981580Z   include-hidden-files: false
2026-06-07T06:48:21.2981812Z env:
2026-06-07T06:48:21.2982136Z   POLYGON_API_KEY: ***
```

## CI

- Run ID: `27084932698`
- Branch: `main`
- Commit: `80bf3c48e193`
- Title: P124 document silent failure run health gate
- Created: 2026-06-07T06:28:03Z
- Updated: 2026-06-07T06:29:05Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27084932698

### Failed job: Pytest

- Job ID: `79937417224`
- Started: 2026-06-07T06:28:06Z
- Completed: 2026-06-07T06:29:04Z
- Failed steps: 53. Full regression suite residual tests

#### Error context

```text
2026-06-07T06:29:01.0000021Z ........................................................................ [ 86%]
2026-06-07T06:29:01.0969782Z ........................................................................ [ 91%]
2026-06-07T06:29:01.2508767Z ........................................................................ [ 97%]
2026-06-07T06:29:01.3192991Z .............................                                            [100%]
2026-06-07T06:29:01.3193831Z =================================== FAILURES ===================================
2026-06-07T06:29:01.3196654Z ______________ test_p121_valid_real_data_backtest_evidence_passes ______________
2026-06-07T06:29:01.3197406Z 
2026-06-07T06:29:01.3197980Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-33/test_p121_valid_real_data_back0')
2026-06-07T06:29:01.3198900Z 
2026-06-07T06:29:01.3199261Z     def test_p121_valid_real_data_backtest_evidence_passes(tmp_path: Path) -> None:
2026-06-07T06:29:01.3199995Z         artifact = tmp_path / "real-data-backtest-evidence.json"
2026-06-07T06:29:01.3200676Z         artifact.write_text(json.dumps(_valid_real_payload()), encoding="utf-8")
2026-06-07T06:29:01.3201230Z     
2026-06-07T06:29:01.3201616Z         gate = validate_real_data_backtest_evidence_artifact(artifact)
2026-06-07T06:29:01.3202111Z     
2026-06-07T06:29:01.3202388Z >       assert gate.passed is True
```

```text
2026-06-07T06:29:01.3201230Z     
2026-06-07T06:29:01.3201616Z         gate = validate_real_data_backtest_evidence_artifact(artifact)
2026-06-07T06:29:01.3202111Z     
2026-06-07T06:29:01.3202388Z >       assert gate.passed is True
2026-06-07T06:29:01.3202807Z E       AssertionError: assert False is True
2026-06-07T06:29:01.3204721Z E        +  where False = RealDataBacktestEvidenceGateReport(passed=False, artifact_path='/tmp/pytest-of-runner/pytest-33/test_p121_valid_real_d...cktest-evidence.json', missing_fields=['input_completeness_status', 'run_health_status'], invalid_fields=[], errors=[]).passed
2026-06-07T06:29:01.3206241Z 
2026-06-07T06:29:01.3206528Z tests/test_p121_real_data_backtest_evidence_gate.py:92: AssertionError
2026-06-07T06:29:01.3207167Z __________________ test_p121_missing_date_range_fails_schema ___________________
2026-06-07T06:29:01.3207456Z 
2026-06-07T06:29:01.3207709Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-33/test_p121_missing_date_range_f0')
2026-06-07T06:29:01.3208056Z 
2026-06-07T06:29:01.3208260Z     def test_p121_missing_date_range_fails_schema(tmp_path: Path) -> None:
2026-06-07T06:29:01.3208661Z         payload = _valid_real_payload()
2026-06-07T06:29:01.3208943Z         del payload["date_range"]
2026-06-07T06:29:01.3209246Z         artifact = tmp_path / "missing-date-range.json"
```

```text
2026-06-07T06:29:01.3202388Z >       assert gate.passed is True
2026-06-07T06:29:01.3202807Z E       AssertionError: assert False is True
2026-06-07T06:29:01.3204721Z E        +  where False = RealDataBacktestEvidenceGateReport(passed=False, artifact_path='/tmp/pytest-of-runner/pytest-33/test_p121_valid_real_d...cktest-evidence.json', missing_fields=['input_completeness_status', 'run_health_status'], invalid_fields=[], errors=[]).passed
2026-06-07T06:29:01.3206241Z 
2026-06-07T06:29:01.3206528Z tests/test_p121_real_data_backtest_evidence_gate.py:92: AssertionError
2026-06-07T06:29:01.3207167Z __________________ test_p121_missing_date_range_fails_schema ___________________
2026-06-07T06:29:01.3207456Z 
2026-06-07T06:29:01.3207709Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-33/test_p121_missing_date_range_f0')
2026-06-07T06:29:01.3208056Z 
2026-06-07T06:29:01.3208260Z     def test_p121_missing_date_range_fails_schema(tmp_path: Path) -> None:
2026-06-07T06:29:01.3208661Z         payload = _valid_real_payload()
2026-06-07T06:29:01.3208943Z         del payload["date_range"]
2026-06-07T06:29:01.3209246Z         artifact = tmp_path / "missing-date-range.json"
2026-06-07T06:29:01.3209664Z         artifact.write_text(json.dumps(payload), encoding="utf-8")
2026-06-07T06:29:01.3210003Z     
2026-06-07T06:29:01.3210280Z         gate = validate_real_data_backtest_evidence_artifact(artifact)
```

```text
2026-06-07T06:29:01.3210280Z         gate = validate_real_data_backtest_evidence_artifact(artifact)
2026-06-07T06:29:01.3210636Z     
2026-06-07T06:29:01.3210846Z         assert gate.passed is False
2026-06-07T06:29:01.3211152Z >       assert gate.missing_fields == ["date_range"]
2026-06-07T06:29:01.3211572Z E       AssertionError: assert ['date_range'...ealth_status'] == ['date_range']
2026-06-07T06:29:01.3211954Z E         
2026-06-07T06:29:01.3212269Z E         Left contains 2 more items, first extra item: 'input_completeness_status'
2026-06-07T06:29:01.3212656Z E         
2026-06-07T06:29:01.3212842Z E         Full diff:
2026-06-07T06:29:01.3213042Z E           [
2026-06-07T06:29:01.3213241Z E               'date_range',
2026-06-07T06:29:01.3213498Z E         +     'input_completeness_status',
2026-06-07T06:29:01.3213780Z E         +     'run_health_status',
2026-06-07T06:29:01.3214223Z E           ]
2026-06-07T06:29:01.3214379Z 
2026-06-07T06:29:01.3214770Z tests/test_p121_real_data_backtest_evidence_gate.py:122: AssertionError
```

```text
2026-06-07T06:29:01.3213498Z E         +     'input_completeness_status',
2026-06-07T06:29:01.3213780Z E         +     'run_health_status',
2026-06-07T06:29:01.3214223Z E           ]
2026-06-07T06:29:01.3214379Z 
2026-06-07T06:29:01.3214770Z tests/test_p121_real_data_backtest_evidence_gate.py:122: AssertionError
2026-06-07T06:29:01.3215233Z =========================== short test summary info ============================
2026-06-07T06:29:01.3216079Z FAILED tests/test_p121_real_data_backtest_evidence_gate.py::test_p121_valid_real_data_backtest_evidence_passes - AssertionError: assert False is True
2026-06-07T06:29:01.3217549Z  +  where False = RealDataBacktestEvidenceGateReport(passed=False, artifact_path='/tmp/pytest-of-runner/pytest-33/test_p121_valid_real_d...cktest-evidence.json', missing_fields=['input_completeness_status', 'run_health_status'], invalid_fields=[], errors=[]).passed
2026-06-07T06:29:01.3219047Z FAILED tests/test_p121_real_data_backtest_evidence_gate.py::test_p121_missing_date_range_fails_schema - AssertionError: assert ['date_range'...ealth_status'] == ['date_range']
2026-06-07T06:29:01.3219753Z   
2026-06-07T06:29:01.3220050Z   Left contains 2 more items, first extra item: 'input_completeness_status'
2026-06-07T06:29:01.3220416Z   
2026-06-07T06:29:01.3220593Z   Full diff:
2026-06-07T06:29:01.3220777Z     [
2026-06-07T06:29:01.3220961Z         'date_range',
2026-06-07T06:29:01.3221185Z   +     'input_completeness_status',
```

```text
2026-06-07T06:29:01.3214223Z E           ]
2026-06-07T06:29:01.3214379Z 
2026-06-07T06:29:01.3214770Z tests/test_p121_real_data_backtest_evidence_gate.py:122: AssertionError
2026-06-07T06:29:01.3215233Z =========================== short test summary info ============================
2026-06-07T06:29:01.3216079Z FAILED tests/test_p121_real_data_backtest_evidence_gate.py::test_p121_valid_real_data_backtest_evidence_passes - AssertionError: assert False is True
2026-06-07T06:29:01.3217549Z  +  where False = RealDataBacktestEvidenceGateReport(passed=False, artifact_path='/tmp/pytest-of-runner/pytest-33/test_p121_valid_real_d...cktest-evidence.json', missing_fields=['input_completeness_status', 'run_health_status'], invalid_fields=[], errors=[]).passed
2026-06-07T06:29:01.3219047Z FAILED tests/test_p121_real_data_backtest_evidence_gate.py::test_p121_missing_date_range_fails_schema - AssertionError: assert ['date_range'...ealth_status'] == ['date_range']
2026-06-07T06:29:01.3219753Z   
2026-06-07T06:29:01.3220050Z   Left contains 2 more items, first extra item: 'input_completeness_status'
2026-06-07T06:29:01.3220416Z   
2026-06-07T06:29:01.3220593Z   Full diff:
2026-06-07T06:29:01.3220777Z     [
2026-06-07T06:29:01.3220961Z         'date_range',
2026-06-07T06:29:01.3221185Z   +     'input_completeness_status',
2026-06-07T06:29:01.3221581Z   +     'run_health_status',
2026-06-07T06:29:01.3221800Z     ]
```

```text
2026-06-07T06:29:01.3214770Z tests/test_p121_real_data_backtest_evidence_gate.py:122: AssertionError
2026-06-07T06:29:01.3215233Z =========================== short test summary info ============================
2026-06-07T06:29:01.3216079Z FAILED tests/test_p121_real_data_backtest_evidence_gate.py::test_p121_valid_real_data_backtest_evidence_passes - AssertionError: assert False is True
2026-06-07T06:29:01.3217549Z  +  where False = RealDataBacktestEvidenceGateReport(passed=False, artifact_path='/tmp/pytest-of-runner/pytest-33/test_p121_valid_real_d...cktest-evidence.json', missing_fields=['input_completeness_status', 'run_health_status'], invalid_fields=[], errors=[]).passed
2026-06-07T06:29:01.3219047Z FAILED tests/test_p121_real_data_backtest_evidence_gate.py::test_p121_missing_date_range_fails_schema - AssertionError: assert ['date_range'...ealth_status'] == ['date_range']
2026-06-07T06:29:01.3219753Z   
2026-06-07T06:29:01.3220050Z   Left contains 2 more items, first extra item: 'input_completeness_status'
2026-06-07T06:29:01.3220416Z   
2026-06-07T06:29:01.3220593Z   Full diff:
2026-06-07T06:29:01.3220777Z     [
2026-06-07T06:29:01.3220961Z         'date_range',
2026-06-07T06:29:01.3221185Z   +     'input_completeness_status',
2026-06-07T06:29:01.3221581Z   +     'run_health_status',
2026-06-07T06:29:01.3221800Z     ]
2026-06-07T06:29:01.3222004Z 2 failed, 1250 passed, 1 skipped in 11.53s
2026-06-07T06:29:01.5548608Z ##[error]Process completed with exit code 1.
```

```text
2026-06-07T06:29:01.3221185Z   +     'input_completeness_status',
2026-06-07T06:29:01.3221581Z   +     'run_health_status',
2026-06-07T06:29:01.3221800Z     ]
2026-06-07T06:29:01.3222004Z 2 failed, 1250 passed, 1 skipped in 11.53s
2026-06-07T06:29:01.5548608Z ##[error]Process completed with exit code 1.
2026-06-07T06:29:01.5622284Z ##[group]Run actions/upload-artifact@v4
2026-06-07T06:29:01.5622587Z with:
2026-06-07T06:29:01.5622814Z   name: p109-residual-pytest-evidence
2026-06-07T06:29:01.5623135Z   path: artifacts/evidence/p109-residual-pytest/
2026-06-07T06:29:01.5623451Z   if-no-files-found: warn
2026-06-07T06:29:01.5623692Z   compression-level: 6
2026-06-07T06:29:01.5623916Z   overwrite: false
2026-06-07T06:29:01.5624466Z   include-hidden-files: false
2026-06-07T06:29:01.5624714Z env:
2026-06-07T06:29:01.5624969Z   pythonLocation: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-07T06:29:01.5625406Z   PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib/pkgconfig
```

## Decision Engine Tests

- Run ID: `27084932709`
- Branch: `main`
- Commit: `80bf3c48e193`
- Title: P124 document silent failure run health gate
- Created: 2026-06-07T06:28:03Z
- Updated: 2026-06-07T06:28:42Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27084932709

### Failed job: tests

- Job ID: `79937417210`
- Started: 2026-06-07T06:28:07Z
- Completed: 2026-06-07T06:28:42Z
- Failed steps: 5. Run pytest

#### Error context

```text
2026-06-07T06:28:39.1403307Z ........................................................................ [ 88%]
2026-06-07T06:28:39.3003977Z ........................................................................ [ 92%]
2026-06-07T06:28:39.4046960Z ........................................................................ [ 97%]
2026-06-07T06:28:39.4958856Z ..................................................                       [100%]
2026-06-07T06:28:39.4959686Z =================================== FAILURES ===================================
2026-06-07T06:28:39.4961098Z ______________ test_p121_valid_real_data_backtest_evidence_passes ______________
2026-06-07T06:28:39.4961785Z 
2026-06-07T06:28:39.4962291Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-0/test_p121_valid_real_data_back0')
2026-06-07T06:28:39.4963113Z 
2026-06-07T06:28:39.4964158Z     def test_p121_valid_real_data_backtest_evidence_passes(tmp_path: Path) -> None:
2026-06-07T06:28:39.4965424Z         artifact = tmp_path / "real-data-backtest-evidence.json"
2026-06-07T06:28:39.4967035Z         artifact.write_text(json.dumps(_valid_real_payload()), encoding="utf-8")
2026-06-07T06:28:39.4967830Z     
2026-06-07T06:28:39.4968252Z         gate = validate_real_data_backtest_evidence_artifact(artifact)
2026-06-07T06:28:39.4968662Z     
2026-06-07T06:28:39.4968893Z >       assert gate.passed is True
```

```text
2026-06-07T06:28:39.4967830Z     
2026-06-07T06:28:39.4968252Z         gate = validate_real_data_backtest_evidence_artifact(artifact)
2026-06-07T06:28:39.4968662Z     
2026-06-07T06:28:39.4968893Z >       assert gate.passed is True
2026-06-07T06:28:39.4969229Z E       AssertionError: assert False is True
2026-06-07T06:28:39.4970581Z E        +  where False = RealDataBacktestEvidenceGateReport(passed=False, artifact_path='/tmp/pytest-of-runner/pytest-0/test_p121_valid_real_da...cktest-evidence.json', missing_fields=['input_completeness_status', 'run_health_status'], invalid_fields=[], errors=[]).passed
2026-06-07T06:28:39.4971838Z 
2026-06-07T06:28:39.4972066Z tests/test_p121_real_data_backtest_evidence_gate.py:92: AssertionError
2026-06-07T06:28:39.4972633Z __________________ test_p121_missing_date_range_fails_schema ___________________
2026-06-07T06:28:39.4972984Z 
2026-06-07T06:28:39.4973268Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-0/test_p121_missing_date_range_f0')
2026-06-07T06:28:39.4973965Z 
2026-06-07T06:28:39.4974200Z     def test_p121_missing_date_range_fails_schema(tmp_path: Path) -> None:
2026-06-07T06:28:39.4974672Z         payload = _valid_real_payload()
2026-06-07T06:28:39.4975003Z         del payload["date_range"]
2026-06-07T06:28:39.4975356Z         artifact = tmp_path / "missing-date-range.json"
```

```text
2026-06-07T06:28:39.4968893Z >       assert gate.passed is True
2026-06-07T06:28:39.4969229Z E       AssertionError: assert False is True
2026-06-07T06:28:39.4970581Z E        +  where False = RealDataBacktestEvidenceGateReport(passed=False, artifact_path='/tmp/pytest-of-runner/pytest-0/test_p121_valid_real_da...cktest-evidence.json', missing_fields=['input_completeness_status', 'run_health_status'], invalid_fields=[], errors=[]).passed
2026-06-07T06:28:39.4971838Z 
2026-06-07T06:28:39.4972066Z tests/test_p121_real_data_backtest_evidence_gate.py:92: AssertionError
2026-06-07T06:28:39.4972633Z __________________ test_p121_missing_date_range_fails_schema ___________________
2026-06-07T06:28:39.4972984Z 
2026-06-07T06:28:39.4973268Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-0/test_p121_missing_date_range_f0')
2026-06-07T06:28:39.4973965Z 
2026-06-07T06:28:39.4974200Z     def test_p121_missing_date_range_fails_schema(tmp_path: Path) -> None:
2026-06-07T06:28:39.4974672Z         payload = _valid_real_payload()
2026-06-07T06:28:39.4975003Z         del payload["date_range"]
2026-06-07T06:28:39.4975356Z         artifact = tmp_path / "missing-date-range.json"
2026-06-07T06:28:39.4975816Z         artifact.write_text(json.dumps(payload), encoding="utf-8")
2026-06-07T06:28:39.4976215Z     
2026-06-07T06:28:39.4976527Z         gate = validate_real_data_backtest_evidence_artifact(artifact)
```

```text
2026-06-07T06:28:39.4976527Z         gate = validate_real_data_backtest_evidence_artifact(artifact)
2026-06-07T06:28:39.4976925Z     
2026-06-07T06:28:39.4977152Z         assert gate.passed is False
2026-06-07T06:28:39.4977508Z >       assert gate.missing_fields == ["date_range"]
2026-06-07T06:28:39.4977979Z E       AssertionError: assert ['date_range'...ealth_status'] == ['date_range']
2026-06-07T06:28:39.4978348Z E         
2026-06-07T06:28:39.4978660Z E         Left contains 2 more items, first extra item: 'input_completeness_status'
2026-06-07T06:28:39.4979383Z E         
2026-06-07T06:28:39.4979589Z E         Full diff:
2026-06-07T06:28:39.4979795Z E           [
2026-06-07T06:28:39.4979999Z E               'date_range',
2026-06-07T06:28:39.4980261Z E         +     'input_completeness_status',
2026-06-07T06:28:39.4980546Z E         +     'run_health_status',
2026-06-07T06:28:39.4980787Z E           ]
2026-06-07T06:28:39.4980893Z 
2026-06-07T06:28:39.4981095Z tests/test_p121_real_data_backtest_evidence_gate.py:122: AssertionError
```

```text
2026-06-07T06:28:39.4980261Z E         +     'input_completeness_status',
2026-06-07T06:28:39.4980546Z E         +     'run_health_status',
2026-06-07T06:28:39.4980787Z E           ]
2026-06-07T06:28:39.4980893Z 
2026-06-07T06:28:39.4981095Z tests/test_p121_real_data_backtest_evidence_gate.py:122: AssertionError
2026-06-07T06:28:39.4981525Z =========================== short test summary info ============================
2026-06-07T06:28:39.4982324Z FAILED tests/test_p121_real_data_backtest_evidence_gate.py::test_p121_valid_real_data_backtest_evidence_passes - AssertionError: assert False is True
2026-06-07T06:28:39.4984008Z  +  where False = RealDataBacktestEvidenceGateReport(passed=False, artifact_path='/tmp/pytest-of-runner/pytest-0/test_p121_valid_real_da...cktest-evidence.json', missing_fields=['input_completeness_status', 'run_health_status'], invalid_fields=[], errors=[]).passed
2026-06-07T06:28:39.4985526Z FAILED tests/test_p121_real_data_backtest_evidence_gate.py::test_p121_missing_date_range_fails_schema - AssertionError: assert ['date_range'...ealth_status'] == ['date_range']
2026-06-07T06:28:39.4986237Z   
2026-06-07T06:28:39.4986534Z   Left contains 2 more items, first extra item: 'input_completeness_status'
2026-06-07T06:28:39.4987067Z   
2026-06-07T06:28:39.4987247Z   Full diff:
2026-06-07T06:28:39.4987430Z     [
2026-06-07T06:28:39.4987609Z         'date_range',
2026-06-07T06:28:39.4987833Z   +     'input_completeness_status',
```

```text
2026-06-07T06:28:39.4980787Z E           ]
2026-06-07T06:28:39.4980893Z 
2026-06-07T06:28:39.4981095Z tests/test_p121_real_data_backtest_evidence_gate.py:122: AssertionError
2026-06-07T06:28:39.4981525Z =========================== short test summary info ============================
2026-06-07T06:28:39.4982324Z FAILED tests/test_p121_real_data_backtest_evidence_gate.py::test_p121_valid_real_data_backtest_evidence_passes - AssertionError: assert False is True
2026-06-07T06:28:39.4984008Z  +  where False = RealDataBacktestEvidenceGateReport(passed=False, artifact_path='/tmp/pytest-of-runner/pytest-0/test_p121_valid_real_da...cktest-evidence.json', missing_fields=['input_completeness_status', 'run_health_status'], invalid_fields=[], errors=[]).passed
2026-06-07T06:28:39.4985526Z FAILED tests/test_p121_real_data_backtest_evidence_gate.py::test_p121_missing_date_range_fails_schema - AssertionError: assert ['date_range'...ealth_status'] == ['date_range']
2026-06-07T06:28:39.4986237Z   
2026-06-07T06:28:39.4986534Z   Left contains 2 more items, first extra item: 'input_completeness_status'
2026-06-07T06:28:39.4987067Z   
2026-06-07T06:28:39.4987247Z   Full diff:
2026-06-07T06:28:39.4987430Z     [
2026-06-07T06:28:39.4987609Z         'date_range',
2026-06-07T06:28:39.4987833Z   +     'input_completeness_status',
2026-06-07T06:28:39.4988092Z   +     'run_health_status',
2026-06-07T06:28:39.4988311Z     ]
```

```text
2026-06-07T06:28:39.4981095Z tests/test_p121_real_data_backtest_evidence_gate.py:122: AssertionError
2026-06-07T06:28:39.4981525Z =========================== short test summary info ============================
2026-06-07T06:28:39.4982324Z FAILED tests/test_p121_real_data_backtest_evidence_gate.py::test_p121_valid_real_data_backtest_evidence_passes - AssertionError: assert False is True
2026-06-07T06:28:39.4984008Z  +  where False = RealDataBacktestEvidenceGateReport(passed=False, artifact_path='/tmp/pytest-of-runner/pytest-0/test_p121_valid_real_da...cktest-evidence.json', missing_fields=['input_completeness_status', 'run_health_status'], invalid_fields=[], errors=[]).passed
2026-06-07T06:28:39.4985526Z FAILED tests/test_p121_real_data_backtest_evidence_gate.py::test_p121_missing_date_range_fails_schema - AssertionError: assert ['date_range'...ealth_status'] == ['date_range']
2026-06-07T06:28:39.4986237Z   
2026-06-07T06:28:39.4986534Z   Left contains 2 more items, first extra item: 'input_completeness_status'
2026-06-07T06:28:39.4987067Z   
2026-06-07T06:28:39.4987247Z   Full diff:
2026-06-07T06:28:39.4987430Z     [
2026-06-07T06:28:39.4987609Z         'date_range',
2026-06-07T06:28:39.4987833Z   +     'input_completeness_status',
2026-06-07T06:28:39.4988092Z   +     'run_health_status',
2026-06-07T06:28:39.4988311Z     ]
2026-06-07T06:28:39.4988520Z 2 failed, 1703 passed, 1 skipped in 14.82s
2026-06-07T06:28:39.8132240Z ##[error]Process completed with exit code 1.
```

```text
2026-06-07T06:28:39.4987833Z   +     'input_completeness_status',
2026-06-07T06:28:39.4988092Z   +     'run_health_status',
2026-06-07T06:28:39.4988311Z     ]
2026-06-07T06:28:39.4988520Z 2 failed, 1703 passed, 1 skipped in 14.82s
2026-06-07T06:28:39.8132240Z ##[error]Process completed with exit code 1.
2026-06-07T06:28:39.8246439Z Post job cleanup.
2026-06-07T06:28:39.9233117Z [command]/usr/bin/git version
2026-06-07T06:28:39.9269282Z git version 2.54.0
2026-06-07T06:28:39.9312794Z Temporarily overriding HOME='/home/runner/work/_temp/e2089b5d-189a-4498-b827-2516cc857323' before making global git config changes
2026-06-07T06:28:39.9314317Z Adding repository directory to the temporary git global config as a safe directory
2026-06-07T06:28:39.9326105Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-06-07T06:28:39.9361574Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-06-07T06:28:39.9394002Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-06-07T06:28:39.9623829Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-06-07T06:28:39.9647580Z http.https://github.com/.extraheader
2026-06-07T06:28:39.9660151Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

## Report Quality Validation

- Run ID: `27084932705`
- Branch: `main`
- Commit: `80bf3c48e193`
- Title: P124 document silent failure run health gate
- Created: 2026-06-07T06:28:03Z
- Updated: 2026-06-07T06:29:22Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27084932705

### Failed job: validate-reports (premarket)

- Job ID: `79937417293`
- Started: 2026-06-07T06:28:05Z
- Completed: 2026-06-07T06:29:01Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-07T06:28:20.8827770Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-07T06:28:20.8828154Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-07T06:28:20.8828589Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-07T06:28:20.8828920Z ##[endgroup]
2026-06-07T06:28:59.7289868Z Traceback (most recent call last):
2026-06-07T06:28:59.7291458Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-03/2026-06-07?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-07T06:28:59.7300948Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 491, in <module>
2026-06-07T06:28:59.7301683Z     raise SystemExit(main())
2026-06-07T06:28:59.7301949Z                      ^^^^^^
2026-06-07T06:28:59.7302580Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 474, in main
2026-06-07T06:28:59.7303358Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-07T06:28:59.7303841Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-07T06:28:59.7304598Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 108, in write_report_text_guarded
2026-06-07T06:28:59.7305368Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-07T06:28:59.7307125Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-03/2026-06-07?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-07T06:28:59.7308646Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-03/2026-06-07?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
```

```text
2026-06-07T06:28:59.7308646Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-03/2026-06-07?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-07T06:28:59.7317291Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-07T06:28:59.7337238Z     raise ReportOutputBoundaryError(
2026-06-07T06:28:59.7338992Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/premarket-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
2026-06-07T06:28:59.8008754Z ##[error]Process completed with exit code 1.
2026-06-07T06:28:59.8093907Z ##[group]Run actions/upload-artifact@v4
2026-06-07T06:28:59.8094203Z with:
2026-06-07T06:28:59.8094428Z   name: validated-premarket-report
2026-06-07T06:28:59.8094715Z   path: reports/premarket-report.md
2026-06-07T06:28:59.8094984Z   retention-days: 14
2026-06-07T06:28:59.8095417Z   if-no-files-found: warn
2026-06-07T06:28:59.8095672Z   compression-level: 6
2026-06-07T06:28:59.8095900Z   overwrite: false
2026-06-07T06:28:59.8096123Z   include-hidden-files: false
2026-06-07T06:28:59.8096581Z env:
2026-06-07T06:28:59.8096959Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (postmarket)

- Job ID: `79937417299`
- Started: 2026-06-07T06:28:06Z
- Completed: 2026-06-07T06:29:21Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-07T06:28:24.3592186Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-07T06:28:24.3592582Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-07T06:28:24.3592993Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-07T06:28:24.3593334Z ##[endgroup]
2026-06-07T06:29:17.6722114Z Traceback (most recent call last):
2026-06-07T06:29:17.6732521Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 491, in <module>
2026-06-07T06:29:17.6734561Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-03/2026-06-07?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-07T06:29:17.6735814Z     raise SystemExit(main())
2026-06-07T06:29:17.6736128Z                      ^^^^^^
2026-06-07T06:29:17.6736954Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 474, in main
2026-06-07T06:29:17.6738011Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-07T06:29:17.6738623Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-07T06:29:17.6739670Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 108, in write_report_text_guarded
2026-06-07T06:29:17.6740809Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-07T06:29:17.6741709Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-07T06:29:17.6742465Z     raise ReportOutputBoundaryError(
```

```text
2026-06-07T06:29:17.6742465Z     raise ReportOutputBoundaryError(
2026-06-07T06:29:17.6743847Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/postmarket-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
2026-06-07T06:29:17.6745923Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-03/2026-06-07?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-07T06:29:17.6747339Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-03/2026-06-07?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-07T06:29:17.7541972Z ##[error]Process completed with exit code 1.
2026-06-07T06:29:17.7629323Z ##[group]Run actions/upload-artifact@v4
2026-06-07T06:29:17.7629642Z with:
2026-06-07T06:29:17.7629879Z   name: validated-postmarket-report
2026-06-07T06:29:17.7630185Z   path: reports/postmarket-report.md
2026-06-07T06:29:17.7630761Z   retention-days: 14
2026-06-07T06:29:17.7631208Z   if-no-files-found: warn
2026-06-07T06:29:17.7631469Z   compression-level: 6
2026-06-07T06:29:17.7631716Z   overwrite: false
2026-06-07T06:29:17.7631957Z   include-hidden-files: false
2026-06-07T06:29:17.7632211Z env:
2026-06-07T06:29:17.7632572Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (weekly)

- Job ID: `79937417309`
- Started: 2026-06-07T06:28:05Z
- Completed: 2026-06-07T06:28:22Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-07T06:28:20.4034138Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-07T06:28:20.4034530Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-07T06:28:20.4034952Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-07T06:28:20.4035291Z ##[endgroup]
2026-06-07T06:28:21.1305180Z Traceback (most recent call last):
2026-06-07T06:28:21.1315127Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 491, in <module>
2026-06-07T06:28:21.1316012Z     raise SystemExit(main())
2026-06-07T06:28:21.1316290Z                      ^^^^^^
2026-06-07T06:28:21.1317241Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 474, in main
2026-06-07T06:28:21.1318010Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-07T06:28:21.1318472Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-07T06:28:21.1319244Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 108, in write_report_text_guarded
2026-06-07T06:28:21.1320029Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-07T06:28:21.1320846Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-07T06:28:21.1321565Z     raise ReportOutputBoundaryError(
2026-06-07T06:28:21.1322896Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
```

```text
2026-06-07T06:28:21.1320029Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-07T06:28:21.1320846Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-07T06:28:21.1321565Z     raise ReportOutputBoundaryError(
2026-06-07T06:28:21.1322896Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
2026-06-07T06:28:21.1548855Z ##[error]Process completed with exit code 1.
2026-06-07T06:28:21.1634278Z ##[group]Run actions/upload-artifact@v4
2026-06-07T06:28:21.1634581Z with:
2026-06-07T06:28:21.1634802Z   name: validated-weekly-report
2026-06-07T06:28:21.1635080Z   path: reports/weekly-report.md
2026-06-07T06:28:21.1635338Z   retention-days: 14
2026-06-07T06:28:21.1635564Z   if-no-files-found: warn
2026-06-07T06:28:21.1635804Z   compression-level: 6
2026-06-07T06:28:21.1636034Z   overwrite: false
2026-06-07T06:28:21.1636260Z   include-hidden-files: false
2026-06-07T06:28:21.1636498Z env:
2026-06-07T06:28:21.1637163Z   POLYGON_API_KEY: ***
```

## Decision Engine Tests

- Run ID: `27084827349`
- Branch: `main`
- Commit: `1a446863235c`
- Title: P124 align BT130 evidence fixture with health fields
- Created: 2026-06-07T06:22:29Z
- Updated: 2026-06-07T06:22:59Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27084827349

### Failed job: tests

- Job ID: `79937107701`
- Started: 2026-06-07T06:22:31Z
- Completed: 2026-06-07T06:22:58Z
- Failed steps: 5. Run pytest

#### Error context

```text
2026-06-07T06:22:56.3662772Z ........................................................................ [ 88%]
2026-06-07T06:22:56.4808171Z ........................................................................ [ 92%]
2026-06-07T06:22:56.5385311Z ........................................................................ [ 97%]
2026-06-07T06:22:56.5881590Z ..................................................                       [100%]
2026-06-07T06:22:56.5881916Z =================================== FAILURES ===================================
2026-06-07T06:22:56.5882572Z ______________ test_p121_valid_real_data_backtest_evidence_passes ______________
2026-06-07T06:22:56.5882733Z 
2026-06-07T06:22:56.5882874Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-0/test_p121_valid_real_data_back0')
2026-06-07T06:22:56.5883065Z 
2026-06-07T06:22:56.5883226Z     def test_p121_valid_real_data_backtest_evidence_passes(tmp_path: Path) -> None:
2026-06-07T06:22:56.5883491Z         artifact = tmp_path / "real-data-backtest-evidence.json"
2026-06-07T06:22:56.5883882Z         artifact.write_text(json.dumps(_valid_real_payload()), encoding="utf-8")
2026-06-07T06:22:56.5884078Z     
2026-06-07T06:22:56.5884223Z         gate = validate_real_data_backtest_evidence_artifact(artifact)
2026-06-07T06:22:56.5884394Z     
2026-06-07T06:22:56.5884500Z >       assert gate.passed is True
```

```text
2026-06-07T06:22:56.5884078Z     
2026-06-07T06:22:56.5884223Z         gate = validate_real_data_backtest_evidence_artifact(artifact)
2026-06-07T06:22:56.5884394Z     
2026-06-07T06:22:56.5884500Z >       assert gate.passed is True
2026-06-07T06:22:56.5884654Z E       AssertionError: assert False is True
2026-06-07T06:22:56.5885206Z E        +  where False = RealDataBacktestEvidenceGateReport(passed=False, artifact_path='/tmp/pytest-of-runner/pytest-0/test_p121_valid_real_da...cktest-evidence.json', missing_fields=['input_completeness_status', 'run_health_status'], invalid_fields=[], errors=[]).passed
2026-06-07T06:22:56.5885721Z 
2026-06-07T06:22:56.5885823Z tests/test_p121_real_data_backtest_evidence_gate.py:92: AssertionError
2026-06-07T06:22:56.5886064Z __________________ test_p121_missing_date_range_fails_schema ___________________
2026-06-07T06:22:56.5886207Z 
2026-06-07T06:22:56.5886333Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-0/test_p121_missing_date_range_f0')
2026-06-07T06:22:56.5886506Z 
2026-06-07T06:22:56.5886611Z     def test_p121_missing_date_range_fails_schema(tmp_path: Path) -> None:
2026-06-07T06:22:56.5886815Z         payload = _valid_real_payload()
2026-06-07T06:22:56.5886959Z         del payload["date_range"]
2026-06-07T06:22:56.5887119Z         artifact = tmp_path / "missing-date-range.json"
```

```text
2026-06-07T06:22:56.5884500Z >       assert gate.passed is True
2026-06-07T06:22:56.5884654Z E       AssertionError: assert False is True
2026-06-07T06:22:56.5885206Z E        +  where False = RealDataBacktestEvidenceGateReport(passed=False, artifact_path='/tmp/pytest-of-runner/pytest-0/test_p121_valid_real_da...cktest-evidence.json', missing_fields=['input_completeness_status', 'run_health_status'], invalid_fields=[], errors=[]).passed
2026-06-07T06:22:56.5885721Z 
2026-06-07T06:22:56.5885823Z tests/test_p121_real_data_backtest_evidence_gate.py:92: AssertionError
2026-06-07T06:22:56.5886064Z __________________ test_p121_missing_date_range_fails_schema ___________________
2026-06-07T06:22:56.5886207Z 
2026-06-07T06:22:56.5886333Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-0/test_p121_missing_date_range_f0')
2026-06-07T06:22:56.5886506Z 
2026-06-07T06:22:56.5886611Z     def test_p121_missing_date_range_fails_schema(tmp_path: Path) -> None:
2026-06-07T06:22:56.5886815Z         payload = _valid_real_payload()
2026-06-07T06:22:56.5886959Z         del payload["date_range"]
2026-06-07T06:22:56.5887119Z         artifact = tmp_path / "missing-date-range.json"
2026-06-07T06:22:56.5887320Z         artifact.write_text(json.dumps(payload), encoding="utf-8")
2026-06-07T06:22:56.5887492Z     
2026-06-07T06:22:56.5887629Z         gate = validate_real_data_backtest_evidence_artifact(artifact)
```

```text
2026-06-07T06:22:56.5887629Z         gate = validate_real_data_backtest_evidence_artifact(artifact)
2026-06-07T06:22:56.5887797Z     
2026-06-07T06:22:56.5887901Z         assert gate.passed is False
2026-06-07T06:22:56.5888057Z >       assert gate.missing_fields == ["date_range"]
2026-06-07T06:22:56.5888267Z E       AssertionError: assert ['date_range'...ealth_status'] == ['date_range']
2026-06-07T06:22:56.5888456Z E         
2026-06-07T06:22:56.5888619Z E         Left contains 2 more items, first extra item: 'input_completeness_status'
2026-06-07T06:22:56.5888813Z E         
2026-06-07T06:22:56.5888912Z E         Full diff:
2026-06-07T06:22:56.5889022Z E           [
2026-06-07T06:22:56.5889131Z E               'date_range',
2026-06-07T06:22:56.5889268Z E         +     'input_completeness_status',
2026-06-07T06:22:56.5889415Z E         +     'run_health_status',
2026-06-07T06:22:56.5889541Z E           ]
2026-06-07T06:22:56.5889601Z 
2026-06-07T06:22:56.5889704Z tests/test_p121_real_data_backtest_evidence_gate.py:122: AssertionError
```

```text
2026-06-07T06:22:56.5889268Z E         +     'input_completeness_status',
2026-06-07T06:22:56.5889415Z E         +     'run_health_status',
2026-06-07T06:22:56.5889541Z E           ]
2026-06-07T06:22:56.5889601Z 
2026-06-07T06:22:56.5889704Z tests/test_p121_real_data_backtest_evidence_gate.py:122: AssertionError
2026-06-07T06:22:56.5889926Z =========================== short test summary info ============================
2026-06-07T06:22:56.5890774Z FAILED tests/test_p121_real_data_backtest_evidence_gate.py::test_p121_valid_real_data_backtest_evidence_passes - AssertionError: assert False is True
2026-06-07T06:22:56.5891498Z  +  where False = RealDataBacktestEvidenceGateReport(passed=False, artifact_path='/tmp/pytest-of-runner/pytest-0/test_p121_valid_real_da...cktest-evidence.json', missing_fields=['input_completeness_status', 'run_health_status'], invalid_fields=[], errors=[]).passed
2026-06-07T06:22:56.5892243Z FAILED tests/test_p121_real_data_backtest_evidence_gate.py::test_p121_missing_date_range_fails_schema - AssertionError: assert ['date_range'...ealth_status'] == ['date_range']
2026-06-07T06:22:56.5892612Z   
2026-06-07T06:22:56.5892770Z   Left contains 2 more items, first extra item: 'input_completeness_status'
2026-06-07T06:22:56.5893067Z   
2026-06-07T06:22:56.5893159Z   Full diff:
2026-06-07T06:22:56.5893276Z     [
2026-06-07T06:22:56.5893374Z         'date_range',
2026-06-07T06:22:56.5893497Z   +     'input_completeness_status',
```

```text
2026-06-07T06:22:56.5889541Z E           ]
2026-06-07T06:22:56.5889601Z 
2026-06-07T06:22:56.5889704Z tests/test_p121_real_data_backtest_evidence_gate.py:122: AssertionError
2026-06-07T06:22:56.5889926Z =========================== short test summary info ============================
2026-06-07T06:22:56.5890774Z FAILED tests/test_p121_real_data_backtest_evidence_gate.py::test_p121_valid_real_data_backtest_evidence_passes - AssertionError: assert False is True
2026-06-07T06:22:56.5891498Z  +  where False = RealDataBacktestEvidenceGateReport(passed=False, artifact_path='/tmp/pytest-of-runner/pytest-0/test_p121_valid_real_da...cktest-evidence.json', missing_fields=['input_completeness_status', 'run_health_status'], invalid_fields=[], errors=[]).passed
2026-06-07T06:22:56.5892243Z FAILED tests/test_p121_real_data_backtest_evidence_gate.py::test_p121_missing_date_range_fails_schema - AssertionError: assert ['date_range'...ealth_status'] == ['date_range']
2026-06-07T06:22:56.5892612Z   
2026-06-07T06:22:56.5892770Z   Left contains 2 more items, first extra item: 'input_completeness_status'
2026-06-07T06:22:56.5893067Z   
2026-06-07T06:22:56.5893159Z   Full diff:
2026-06-07T06:22:56.5893276Z     [
2026-06-07T06:22:56.5893374Z         'date_range',
2026-06-07T06:22:56.5893497Z   +     'input_completeness_status',
2026-06-07T06:22:56.5893635Z   +     'run_health_status',
2026-06-07T06:22:56.5893753Z     ]
```

```text
2026-06-07T06:22:56.5889704Z tests/test_p121_real_data_backtest_evidence_gate.py:122: AssertionError
2026-06-07T06:22:56.5889926Z =========================== short test summary info ============================
2026-06-07T06:22:56.5890774Z FAILED tests/test_p121_real_data_backtest_evidence_gate.py::test_p121_valid_real_data_backtest_evidence_passes - AssertionError: assert False is True
2026-06-07T06:22:56.5891498Z  +  where False = RealDataBacktestEvidenceGateReport(passed=False, artifact_path='/tmp/pytest-of-runner/pytest-0/test_p121_valid_real_da...cktest-evidence.json', missing_fields=['input_completeness_status', 'run_health_status'], invalid_fields=[], errors=[]).passed
2026-06-07T06:22:56.5892243Z FAILED tests/test_p121_real_data_backtest_evidence_gate.py::test_p121_missing_date_range_fails_schema - AssertionError: assert ['date_range'...ealth_status'] == ['date_range']
2026-06-07T06:22:56.5892612Z   
2026-06-07T06:22:56.5892770Z   Left contains 2 more items, first extra item: 'input_completeness_status'
2026-06-07T06:22:56.5893067Z   
2026-06-07T06:22:56.5893159Z   Full diff:
2026-06-07T06:22:56.5893276Z     [
2026-06-07T06:22:56.5893374Z         'date_range',
2026-06-07T06:22:56.5893497Z   +     'input_completeness_status',
2026-06-07T06:22:56.5893635Z   +     'run_health_status',
2026-06-07T06:22:56.5893753Z     ]
2026-06-07T06:22:56.5893862Z 2 failed, 1703 passed, 1 skipped in 10.12s
2026-06-07T06:22:56.7781808Z ##[error]Process completed with exit code 1.
```

```text
2026-06-07T06:22:56.5893497Z   +     'input_completeness_status',
2026-06-07T06:22:56.5893635Z   +     'run_health_status',
2026-06-07T06:22:56.5893753Z     ]
2026-06-07T06:22:56.5893862Z 2 failed, 1703 passed, 1 skipped in 10.12s
2026-06-07T06:22:56.7781808Z ##[error]Process completed with exit code 1.
2026-06-07T06:22:56.7848992Z Post job cleanup.
2026-06-07T06:22:56.8428636Z [command]/usr/bin/git version
2026-06-07T06:22:56.8453151Z git version 2.54.0
2026-06-07T06:22:56.8475638Z Temporarily overriding HOME='/home/runner/work/_temp/5a106550-c9a2-4d53-83c7-3ce76e587b0d' before making global git config changes
2026-06-07T06:22:56.8476247Z Adding repository directory to the temporary git global config as a safe directory
2026-06-07T06:22:56.8483520Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-06-07T06:22:56.8508653Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-06-07T06:22:56.8530387Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-06-07T06:22:56.8699083Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-06-07T06:22:56.8714371Z http.https://github.com/.extraheader
2026-06-07T06:22:56.8722522Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

## Report Quality Validation

- Run ID: `27084827348`
- Branch: `main`
- Commit: `1a446863235c`
- Title: P124 align BT130 evidence fixture with health fields
- Created: 2026-06-07T06:22:29Z
- Updated: 2026-06-07T06:23:42Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27084827348

### Failed job: validate-reports (postmarket)

- Job ID: `79937107732`
- Started: 2026-06-07T06:22:31Z
- Completed: 2026-06-07T06:23:34Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-07T06:22:51.0364644Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-07T06:22:51.0365035Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-07T06:22:51.0365458Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-07T06:22:51.0365787Z ##[endgroup]
2026-06-07T06:23:33.1682539Z Traceback (most recent call last):
2026-06-07T06:23:33.1684245Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-03/2026-06-07?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-07T06:23:33.1693585Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 491, in <module>
2026-06-07T06:23:33.1694476Z     raise SystemExit(main())
2026-06-07T06:23:33.1694746Z                      ^^^^^^
2026-06-07T06:23:33.1695386Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 474, in main
2026-06-07T06:23:33.1696153Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-07T06:23:33.1696631Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-07T06:23:33.1697690Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 108, in write_report_text_guarded
2026-06-07T06:23:33.1698470Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-07T06:23:33.1699295Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-07T06:23:33.1700010Z     raise ReportOutputBoundaryError(
```

```text
2026-06-07T06:23:33.1700010Z     raise ReportOutputBoundaryError(
2026-06-07T06:23:33.1701324Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/postmarket-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
2026-06-07T06:23:33.1704164Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-03/2026-06-07?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-07T06:23:33.1706150Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-03/2026-06-07?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-07T06:23:33.2338512Z ##[error]Process completed with exit code 1.
2026-06-07T06:23:33.2420586Z ##[group]Run actions/upload-artifact@v4
2026-06-07T06:23:33.2420891Z with:
2026-06-07T06:23:33.2421129Z   name: validated-postmarket-report
2026-06-07T06:23:33.2421429Z   path: reports/postmarket-report.md
2026-06-07T06:23:33.2421924Z   retention-days: 14
2026-06-07T06:23:33.2422156Z   if-no-files-found: warn
2026-06-07T06:23:33.2422394Z   compression-level: 6
2026-06-07T06:23:33.2422625Z   overwrite: false
2026-06-07T06:23:33.2422849Z   include-hidden-files: false
2026-06-07T06:23:33.2423089Z env:
2026-06-07T06:23:33.2423447Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (premarket)

- Job ID: `79937107737`
- Started: 2026-06-07T06:22:31Z
- Completed: 2026-06-07T06:23:41Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-07T06:22:51.0104814Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-07T06:22:51.0105223Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-07T06:22:51.0105643Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-07T06:22:51.0105976Z ##[endgroup]
2026-06-07T06:23:37.9746051Z Traceback (most recent call last):
2026-06-07T06:23:37.9747622Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-03/2026-06-07?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-07T06:23:37.9749578Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-03/2026-06-07?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-07T06:23:37.9750918Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-03/2026-06-07?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-07T06:23:37.9758015Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 491, in <module>
2026-06-07T06:23:37.9758762Z     raise SystemExit(main())
2026-06-07T06:23:37.9759022Z                      ^^^^^^
2026-06-07T06:23:37.9759643Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 474, in main
2026-06-07T06:23:37.9760369Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-07T06:23:37.9760809Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-07T06:23:37.9761564Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 108, in write_report_text_guarded
2026-06-07T06:23:37.9762512Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
```

```text
2026-06-07T06:23:37.9762512Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-07T06:23:37.9763344Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-07T06:23:37.9764060Z     raise ReportOutputBoundaryError(
2026-06-07T06:23:37.9765407Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/premarket-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
2026-06-07T06:23:38.0345650Z ##[error]Process completed with exit code 1.
2026-06-07T06:23:38.0430336Z ##[group]Run actions/upload-artifact@v4
2026-06-07T06:23:38.0430626Z with:
2026-06-07T06:23:38.0430853Z   name: validated-premarket-report
2026-06-07T06:23:38.0431145Z   path: reports/premarket-report.md
2026-06-07T06:23:38.0431421Z   retention-days: 14
2026-06-07T06:23:38.0431830Z   if-no-files-found: warn
2026-06-07T06:23:38.0432070Z   compression-level: 6
2026-06-07T06:23:38.0432294Z   overwrite: false
2026-06-07T06:23:38.0432787Z   include-hidden-files: false
2026-06-07T06:23:38.0433031Z env:
2026-06-07T06:23:38.0433408Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (weekly)

- Job ID: `79937107739`
- Started: 2026-06-07T06:22:31Z
- Completed: 2026-06-07T06:22:51Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-07T06:22:49.6725473Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-07T06:22:49.6725875Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-07T06:22:49.6726302Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-07T06:22:49.6726645Z ##[endgroup]
2026-06-07T06:22:50.4246801Z Traceback (most recent call last):
2026-06-07T06:22:50.4256527Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 491, in <module>
2026-06-07T06:22:50.4257699Z     raise SystemExit(main())
2026-06-07T06:22:50.4258085Z                      ^^^^^^
2026-06-07T06:22:50.4259349Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 474, in main
2026-06-07T06:22:50.4260552Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-07T06:22:50.4261219Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-07T06:22:50.4262429Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 108, in write_report_text_guarded
2026-06-07T06:22:50.4263664Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-07T06:22:50.4264932Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-07T06:22:50.4266064Z     raise ReportOutputBoundaryError(
2026-06-07T06:22:50.4268167Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
```

```text
2026-06-07T06:22:50.4263664Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-07T06:22:50.4264932Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-07T06:22:50.4266064Z     raise ReportOutputBoundaryError(
2026-06-07T06:22:50.4268167Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
2026-06-07T06:22:50.4534570Z ##[error]Process completed with exit code 1.
2026-06-07T06:22:50.4619989Z ##[group]Run actions/upload-artifact@v4
2026-06-07T06:22:50.4620302Z with:
2026-06-07T06:22:50.4620537Z   name: validated-weekly-report
2026-06-07T06:22:50.4620824Z   path: reports/weekly-report.md
2026-06-07T06:22:50.4621095Z   retention-days: 14
2026-06-07T06:22:50.4621338Z   if-no-files-found: warn
2026-06-07T06:22:50.4621596Z   compression-level: 6
2026-06-07T06:22:50.4621838Z   overwrite: false
2026-06-07T06:22:50.4622072Z   include-hidden-files: false
2026-06-07T06:22:50.4622324Z env:
2026-06-07T06:22:50.4622700Z   POLYGON_API_KEY: ***
```

## CI

- Run ID: `27084827360`
- Branch: `main`
- Commit: `1a446863235c`
- Title: P124 align BT130 evidence fixture with health fields
- Created: 2026-06-07T06:22:29Z
- Updated: 2026-06-07T06:23:29Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27084827360

### Failed job: Pytest

- Job ID: `79937107723`
- Started: 2026-06-07T06:22:33Z
- Completed: 2026-06-07T06:23:28Z
- Failed steps: 53. Full regression suite residual tests

#### Error context

```text
2026-06-07T06:23:24.1617562Z ........................................................................ [ 86%]
2026-06-07T06:23:24.2639069Z ........................................................................ [ 91%]
2026-06-07T06:23:24.4233102Z ........................................................................ [ 97%]
2026-06-07T06:23:24.4938320Z .............................                                            [100%]
2026-06-07T06:23:24.4939549Z =================================== FAILURES ===================================
2026-06-07T06:23:24.4940935Z ______________ test_p121_valid_real_data_backtest_evidence_passes ______________
2026-06-07T06:23:24.4942335Z 
2026-06-07T06:23:24.4943198Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-33/test_p121_valid_real_data_back0')
2026-06-07T06:23:24.4944665Z 
2026-06-07T06:23:24.4945444Z     def test_p121_valid_real_data_backtest_evidence_passes(tmp_path: Path) -> None:
2026-06-07T06:23:24.4946803Z         artifact = tmp_path / "real-data-backtest-evidence.json"
2026-06-07T06:23:24.4947748Z         artifact.write_text(json.dumps(_valid_real_payload()), encoding="utf-8")
2026-06-07T06:23:24.4948514Z     
2026-06-07T06:23:24.4949032Z         gate = validate_real_data_backtest_evidence_artifact(artifact)
2026-06-07T06:23:24.4949570Z     
2026-06-07T06:23:24.4949869Z >       assert gate.passed is True
```

```text
2026-06-07T06:23:24.4948514Z     
2026-06-07T06:23:24.4949032Z         gate = validate_real_data_backtest_evidence_artifact(artifact)
2026-06-07T06:23:24.4949570Z     
2026-06-07T06:23:24.4949869Z >       assert gate.passed is True
2026-06-07T06:23:24.4950314Z E       AssertionError: assert False is True
2026-06-07T06:23:24.4952404Z E        +  where False = RealDataBacktestEvidenceGateReport(passed=False, artifact_path='/tmp/pytest-of-runner/pytest-33/test_p121_valid_real_d...cktest-evidence.json', missing_fields=['input_completeness_status', 'run_health_status'], invalid_fields=[], errors=[]).passed
2026-06-07T06:23:24.4954065Z 
2026-06-07T06:23:24.4954371Z tests/test_p121_real_data_backtest_evidence_gate.py:92: AssertionError
2026-06-07T06:23:24.4955129Z __________________ test_p121_missing_date_range_fails_schema ___________________
2026-06-07T06:23:24.4955598Z 
2026-06-07T06:23:24.4955988Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-33/test_p121_missing_date_range_f0')
2026-06-07T06:23:24.4956548Z 
2026-06-07T06:23:24.4956853Z     def test_p121_missing_date_range_fails_schema(tmp_path: Path) -> None:
2026-06-07T06:23:24.4957489Z         payload = _valid_real_payload()
2026-06-07T06:23:24.4957932Z         del payload["date_range"]
2026-06-07T06:23:24.4958415Z         artifact = tmp_path / "missing-date-range.json"
```

```text
2026-06-07T06:23:24.4949869Z >       assert gate.passed is True
2026-06-07T06:23:24.4950314Z E       AssertionError: assert False is True
2026-06-07T06:23:24.4952404Z E        +  where False = RealDataBacktestEvidenceGateReport(passed=False, artifact_path='/tmp/pytest-of-runner/pytest-33/test_p121_valid_real_d...cktest-evidence.json', missing_fields=['input_completeness_status', 'run_health_status'], invalid_fields=[], errors=[]).passed
2026-06-07T06:23:24.4954065Z 
2026-06-07T06:23:24.4954371Z tests/test_p121_real_data_backtest_evidence_gate.py:92: AssertionError
2026-06-07T06:23:24.4955129Z __________________ test_p121_missing_date_range_fails_schema ___________________
2026-06-07T06:23:24.4955598Z 
2026-06-07T06:23:24.4955988Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-33/test_p121_missing_date_range_f0')
2026-06-07T06:23:24.4956548Z 
2026-06-07T06:23:24.4956853Z     def test_p121_missing_date_range_fails_schema(tmp_path: Path) -> None:
2026-06-07T06:23:24.4957489Z         payload = _valid_real_payload()
2026-06-07T06:23:24.4957932Z         del payload["date_range"]
2026-06-07T06:23:24.4958415Z         artifact = tmp_path / "missing-date-range.json"
2026-06-07T06:23:24.4959059Z         artifact.write_text(json.dumps(payload), encoding="utf-8")
2026-06-07T06:23:24.4959556Z     
2026-06-07T06:23:24.4959867Z         gate = validate_real_data_backtest_evidence_artifact(artifact)
```

```text
2026-06-07T06:23:24.4959867Z         gate = validate_real_data_backtest_evidence_artifact(artifact)
2026-06-07T06:23:24.4960269Z     
2026-06-07T06:23:24.4960497Z         assert gate.passed is False
2026-06-07T06:23:24.4960841Z >       assert gate.missing_fields == ["date_range"]
2026-06-07T06:23:24.4961328Z E       AssertionError: assert ['date_range'...ealth_status'] == ['date_range']
2026-06-07T06:23:24.4961968Z E         
2026-06-07T06:23:24.4962351Z E         Left contains 2 more items, first extra item: 'input_completeness_status'
2026-06-07T06:23:24.4962823Z E         
2026-06-07T06:23:24.4963043Z E         Full diff:
2026-06-07T06:23:24.4963286Z E           [
2026-06-07T06:23:24.4963542Z E               'date_range',
2026-06-07T06:23:24.4963842Z E         +     'input_completeness_status',
2026-06-07T06:23:24.4964178Z E         +     'run_health_status',
2026-06-07T06:23:24.4964467Z E           ]
2026-06-07T06:23:24.4964599Z 
2026-06-07T06:23:24.4965022Z tests/test_p121_real_data_backtest_evidence_gate.py:122: AssertionError
```

```text
2026-06-07T06:23:24.4963842Z E         +     'input_completeness_status',
2026-06-07T06:23:24.4964178Z E         +     'run_health_status',
2026-06-07T06:23:24.4964467Z E           ]
2026-06-07T06:23:24.4964599Z 
2026-06-07T06:23:24.4965022Z tests/test_p121_real_data_backtest_evidence_gate.py:122: AssertionError
2026-06-07T06:23:24.4965552Z =========================== short test summary info ============================
2026-06-07T06:23:24.4966561Z FAILED tests/test_p121_real_data_backtest_evidence_gate.py::test_p121_valid_real_data_backtest_evidence_passes - AssertionError: assert False is True
2026-06-07T06:23:24.4968353Z  +  where False = RealDataBacktestEvidenceGateReport(passed=False, artifact_path='/tmp/pytest-of-runner/pytest-33/test_p121_valid_real_d...cktest-evidence.json', missing_fields=['input_completeness_status', 'run_health_status'], invalid_fields=[], errors=[]).passed
2026-06-07T06:23:24.4970097Z FAILED tests/test_p121_real_data_backtest_evidence_gate.py::test_p121_missing_date_range_fails_schema - AssertionError: assert ['date_range'...ealth_status'] == ['date_range']
2026-06-07T06:23:24.4970820Z   
2026-06-07T06:23:24.4971114Z   Left contains 2 more items, first extra item: 'input_completeness_status'
2026-06-07T06:23:24.4971613Z   
2026-06-07T06:23:24.4971796Z   Full diff:
2026-06-07T06:23:24.4971979Z     [
2026-06-07T06:23:24.4972157Z         'date_range',
2026-06-07T06:23:24.4972381Z   +     'input_completeness_status',
```

```text
2026-06-07T06:23:24.4964467Z E           ]
2026-06-07T06:23:24.4964599Z 
2026-06-07T06:23:24.4965022Z tests/test_p121_real_data_backtest_evidence_gate.py:122: AssertionError
2026-06-07T06:23:24.4965552Z =========================== short test summary info ============================
2026-06-07T06:23:24.4966561Z FAILED tests/test_p121_real_data_backtest_evidence_gate.py::test_p121_valid_real_data_backtest_evidence_passes - AssertionError: assert False is True
2026-06-07T06:23:24.4968353Z  +  where False = RealDataBacktestEvidenceGateReport(passed=False, artifact_path='/tmp/pytest-of-runner/pytest-33/test_p121_valid_real_d...cktest-evidence.json', missing_fields=['input_completeness_status', 'run_health_status'], invalid_fields=[], errors=[]).passed
2026-06-07T06:23:24.4970097Z FAILED tests/test_p121_real_data_backtest_evidence_gate.py::test_p121_missing_date_range_fails_schema - AssertionError: assert ['date_range'...ealth_status'] == ['date_range']
2026-06-07T06:23:24.4970820Z   
2026-06-07T06:23:24.4971114Z   Left contains 2 more items, first extra item: 'input_completeness_status'
2026-06-07T06:23:24.4971613Z   
2026-06-07T06:23:24.4971796Z   Full diff:
2026-06-07T06:23:24.4971979Z     [
2026-06-07T06:23:24.4972157Z         'date_range',
2026-06-07T06:23:24.4972381Z   +     'input_completeness_status',
2026-06-07T06:23:24.4972780Z   +     'run_health_status',
2026-06-07T06:23:24.4973006Z     ]
```

```text
2026-06-07T06:23:24.4965022Z tests/test_p121_real_data_backtest_evidence_gate.py:122: AssertionError
2026-06-07T06:23:24.4965552Z =========================== short test summary info ============================
2026-06-07T06:23:24.4966561Z FAILED tests/test_p121_real_data_backtest_evidence_gate.py::test_p121_valid_real_data_backtest_evidence_passes - AssertionError: assert False is True
2026-06-07T06:23:24.4968353Z  +  where False = RealDataBacktestEvidenceGateReport(passed=False, artifact_path='/tmp/pytest-of-runner/pytest-33/test_p121_valid_real_d...cktest-evidence.json', missing_fields=['input_completeness_status', 'run_health_status'], invalid_fields=[], errors=[]).passed
2026-06-07T06:23:24.4970097Z FAILED tests/test_p121_real_data_backtest_evidence_gate.py::test_p121_missing_date_range_fails_schema - AssertionError: assert ['date_range'...ealth_status'] == ['date_range']
2026-06-07T06:23:24.4970820Z   
2026-06-07T06:23:24.4971114Z   Left contains 2 more items, first extra item: 'input_completeness_status'
2026-06-07T06:23:24.4971613Z   
2026-06-07T06:23:24.4971796Z   Full diff:
2026-06-07T06:23:24.4971979Z     [
2026-06-07T06:23:24.4972157Z         'date_range',
2026-06-07T06:23:24.4972381Z   +     'input_completeness_status',
2026-06-07T06:23:24.4972780Z   +     'run_health_status',
2026-06-07T06:23:24.4973006Z     ]
2026-06-07T06:23:24.4973208Z 2 failed, 1250 passed, 1 skipped in 11.72s
2026-06-07T06:23:24.7186273Z ##[error]Process completed with exit code 1.
```

```text
2026-06-07T06:23:24.4972381Z   +     'input_completeness_status',
2026-06-07T06:23:24.4972780Z   +     'run_health_status',
2026-06-07T06:23:24.4973006Z     ]
2026-06-07T06:23:24.4973208Z 2 failed, 1250 passed, 1 skipped in 11.72s
2026-06-07T06:23:24.7186273Z ##[error]Process completed with exit code 1.
2026-06-07T06:23:24.7262287Z ##[group]Run actions/upload-artifact@v4
2026-06-07T06:23:24.7262607Z with:
2026-06-07T06:23:24.7262827Z   name: p109-residual-pytest-evidence
2026-06-07T06:23:24.7263151Z   path: artifacts/evidence/p109-residual-pytest/
2026-06-07T06:23:24.7263472Z   if-no-files-found: warn
2026-06-07T06:23:24.7263710Z   compression-level: 6
2026-06-07T06:23:24.7263927Z   overwrite: false
2026-06-07T06:23:24.7264144Z   include-hidden-files: false
2026-06-07T06:23:24.7264380Z env:
2026-06-07T06:23:24.7264631Z   pythonLocation: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-07T06:23:24.7265072Z   PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib/pkgconfig
```

## Decision Engine Tests

- Run ID: `27084626827`
- Branch: `main`
- Commit: `068124df8549`
- Title: P124 require backtest health fields in real-data evidence
- Created: 2026-06-07T06:12:04Z
- Updated: 2026-06-07T06:12:43Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27084626827

### Failed job: tests

- Job ID: `79936521087`
- Started: 2026-06-07T06:12:08Z
- Completed: 2026-06-07T06:12:43Z
- Failed steps: 5. Run pytest

#### Error context

```text
2026-06-07T06:12:39.7595590Z ........................................................................ [ 88%]
2026-06-07T06:12:39.9321577Z ........................................................................ [ 92%]
2026-06-07T06:12:40.0395902Z ........................................................................ [ 97%]
2026-06-07T06:12:40.1343555Z ..................................................                       [100%]
2026-06-07T06:12:40.1344649Z =================================== FAILURES ===================================
2026-06-07T06:12:40.1346020Z ______________ test_p121_valid_real_data_backtest_evidence_passes ______________
2026-06-07T06:12:40.1347020Z 
2026-06-07T06:12:40.1347519Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-0/test_p121_valid_real_data_back0')
2026-06-07T06:12:40.1348299Z 
2026-06-07T06:12:40.1348842Z     def test_p121_valid_real_data_backtest_evidence_passes(tmp_path: Path) -> None:
2026-06-07T06:12:40.1349682Z         artifact = tmp_path / "real-data-backtest-evidence.json"
2026-06-07T06:12:40.1350715Z         artifact.write_text(json.dumps(_valid_real_payload()), encoding="utf-8")
2026-06-07T06:12:40.1351304Z     
2026-06-07T06:12:40.1351699Z         gate = validate_real_data_backtest_evidence_artifact(artifact)
2026-06-07T06:12:40.1352213Z     
2026-06-07T06:12:40.1352489Z >       assert gate.passed is True
```

```text
2026-06-07T06:12:40.1351304Z     
2026-06-07T06:12:40.1351699Z         gate = validate_real_data_backtest_evidence_artifact(artifact)
2026-06-07T06:12:40.1352213Z     
2026-06-07T06:12:40.1352489Z >       assert gate.passed is True
2026-06-07T06:12:40.1352907Z E       AssertionError: assert False is True
2026-06-07T06:12:40.1354588Z E        +  where False = RealDataBacktestEvidenceGateReport(passed=False, artifact_path='/tmp/pytest-of-runner/pytest-0/test_p121_valid_real_da...cktest-evidence.json', missing_fields=['input_completeness_status', 'run_health_status'], invalid_fields=[], errors=[]).passed
2026-06-07T06:12:40.1356101Z 
2026-06-07T06:12:40.1356322Z tests/test_p121_real_data_backtest_evidence_gate.py:92: AssertionError
2026-06-07T06:12:40.1357195Z __________________ test_p121_missing_date_range_fails_schema ___________________
2026-06-07T06:12:40.1357536Z 
2026-06-07T06:12:40.1357816Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-0/test_p121_missing_date_range_f0')
2026-06-07T06:12:40.1358229Z 
2026-06-07T06:12:40.1358455Z     def test_p121_missing_date_range_fails_schema(tmp_path: Path) -> None:
2026-06-07T06:12:40.1358896Z         payload = _valid_real_payload()
2026-06-07T06:12:40.1359207Z         del payload["date_range"]
2026-06-07T06:12:40.1359544Z         artifact = tmp_path / "missing-date-range.json"
```

```text
2026-06-07T06:12:40.1352489Z >       assert gate.passed is True
2026-06-07T06:12:40.1352907Z E       AssertionError: assert False is True
2026-06-07T06:12:40.1354588Z E        +  where False = RealDataBacktestEvidenceGateReport(passed=False, artifact_path='/tmp/pytest-of-runner/pytest-0/test_p121_valid_real_da...cktest-evidence.json', missing_fields=['input_completeness_status', 'run_health_status'], invalid_fields=[], errors=[]).passed
2026-06-07T06:12:40.1356101Z 
2026-06-07T06:12:40.1356322Z tests/test_p121_real_data_backtest_evidence_gate.py:92: AssertionError
2026-06-07T06:12:40.1357195Z __________________ test_p121_missing_date_range_fails_schema ___________________
2026-06-07T06:12:40.1357536Z 
2026-06-07T06:12:40.1357816Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-0/test_p121_missing_date_range_f0')
2026-06-07T06:12:40.1358229Z 
2026-06-07T06:12:40.1358455Z     def test_p121_missing_date_range_fails_schema(tmp_path: Path) -> None:
2026-06-07T06:12:40.1358896Z         payload = _valid_real_payload()
2026-06-07T06:12:40.1359207Z         del payload["date_range"]
2026-06-07T06:12:40.1359544Z         artifact = tmp_path / "missing-date-range.json"
2026-06-07T06:12:40.1359975Z         artifact.write_text(json.dumps(payload), encoding="utf-8")
2026-06-07T06:12:40.1360355Z     
2026-06-07T06:12:40.1360646Z         gate = validate_real_data_backtest_evidence_artifact(artifact)
```

```text
2026-06-07T06:12:40.1360646Z         gate = validate_real_data_backtest_evidence_artifact(artifact)
2026-06-07T06:12:40.1361023Z     
2026-06-07T06:12:40.1361231Z         assert gate.passed is False
2026-06-07T06:12:40.1361554Z >       assert gate.missing_fields == ["date_range"]
2026-06-07T06:12:40.1362015Z E       AssertionError: assert ['date_range'...ealth_status'] == ['date_range']
2026-06-07T06:12:40.1362440Z E         
2026-06-07T06:12:40.1362785Z E         Left contains 2 more items, first extra item: 'input_completeness_status'
2026-06-07T06:12:40.1363226Z E         
2026-06-07T06:12:40.1363426Z E         Full diff:
2026-06-07T06:12:40.1363644Z E           [
2026-06-07T06:12:40.1363853Z E               'date_range',
2026-06-07T06:12:40.1364131Z E         +     'input_completeness_status',
2026-06-07T06:12:40.1364439Z E         +     'run_health_status',
2026-06-07T06:12:40.1364706Z E           ]
2026-06-07T06:12:40.1364827Z 
2026-06-07T06:12:40.1365044Z tests/test_p121_real_data_backtest_evidence_gate.py:122: AssertionError
```

```text
2026-06-07T06:12:40.1364131Z E         +     'input_completeness_status',
2026-06-07T06:12:40.1364439Z E         +     'run_health_status',
2026-06-07T06:12:40.1364706Z E           ]
2026-06-07T06:12:40.1364827Z 
2026-06-07T06:12:40.1365044Z tests/test_p121_real_data_backtest_evidence_gate.py:122: AssertionError
2026-06-07T06:12:40.1365478Z =========================== short test summary info ============================
2026-06-07T06:12:40.1366292Z FAILED tests/test_p121_real_data_backtest_evidence_gate.py::test_p121_valid_real_data_backtest_evidence_passes - AssertionError: assert False is True
2026-06-07T06:12:40.1367884Z  +  where False = RealDataBacktestEvidenceGateReport(passed=False, artifact_path='/tmp/pytest-of-runner/pytest-0/test_p121_valid_real_da...cktest-evidence.json', missing_fields=['input_completeness_status', 'run_health_status'], invalid_fields=[], errors=[]).passed
2026-06-07T06:12:40.1369396Z FAILED tests/test_p121_real_data_backtest_evidence_gate.py::test_p121_missing_date_range_fails_schema - AssertionError: assert ['date_range'...ealth_status'] == ['date_range']
2026-06-07T06:12:40.1370108Z   
2026-06-07T06:12:40.1370415Z   Left contains 2 more items, first extra item: 'input_completeness_status'
2026-06-07T06:12:40.1370943Z   
2026-06-07T06:12:40.1371108Z   Full diff:
2026-06-07T06:12:40.1371299Z     [
2026-06-07T06:12:40.1371478Z         'date_range',
2026-06-07T06:12:40.1371709Z   +     'input_completeness_status',
```

```text
2026-06-07T06:12:40.1364706Z E           ]
2026-06-07T06:12:40.1364827Z 
2026-06-07T06:12:40.1365044Z tests/test_p121_real_data_backtest_evidence_gate.py:122: AssertionError
2026-06-07T06:12:40.1365478Z =========================== short test summary info ============================
2026-06-07T06:12:40.1366292Z FAILED tests/test_p121_real_data_backtest_evidence_gate.py::test_p121_valid_real_data_backtest_evidence_passes - AssertionError: assert False is True
2026-06-07T06:12:40.1367884Z  +  where False = RealDataBacktestEvidenceGateReport(passed=False, artifact_path='/tmp/pytest-of-runner/pytest-0/test_p121_valid_real_da...cktest-evidence.json', missing_fields=['input_completeness_status', 'run_health_status'], invalid_fields=[], errors=[]).passed
2026-06-07T06:12:40.1369396Z FAILED tests/test_p121_real_data_backtest_evidence_gate.py::test_p121_missing_date_range_fails_schema - AssertionError: assert ['date_range'...ealth_status'] == ['date_range']
2026-06-07T06:12:40.1370108Z   
2026-06-07T06:12:40.1370415Z   Left contains 2 more items, first extra item: 'input_completeness_status'
2026-06-07T06:12:40.1370943Z   
2026-06-07T06:12:40.1371108Z   Full diff:
2026-06-07T06:12:40.1371299Z     [
2026-06-07T06:12:40.1371478Z         'date_range',
2026-06-07T06:12:40.1371709Z   +     'input_completeness_status',
2026-06-07T06:12:40.1371967Z   +     'run_health_status',
2026-06-07T06:12:40.1372187Z     ]
```

```text
2026-06-07T06:12:40.1365044Z tests/test_p121_real_data_backtest_evidence_gate.py:122: AssertionError
2026-06-07T06:12:40.1365478Z =========================== short test summary info ============================
2026-06-07T06:12:40.1366292Z FAILED tests/test_p121_real_data_backtest_evidence_gate.py::test_p121_valid_real_data_backtest_evidence_passes - AssertionError: assert False is True
2026-06-07T06:12:40.1367884Z  +  where False = RealDataBacktestEvidenceGateReport(passed=False, artifact_path='/tmp/pytest-of-runner/pytest-0/test_p121_valid_real_da...cktest-evidence.json', missing_fields=['input_completeness_status', 'run_health_status'], invalid_fields=[], errors=[]).passed
2026-06-07T06:12:40.1369396Z FAILED tests/test_p121_real_data_backtest_evidence_gate.py::test_p121_missing_date_range_fails_schema - AssertionError: assert ['date_range'...ealth_status'] == ['date_range']
2026-06-07T06:12:40.1370108Z   
2026-06-07T06:12:40.1370415Z   Left contains 2 more items, first extra item: 'input_completeness_status'
2026-06-07T06:12:40.1370943Z   
2026-06-07T06:12:40.1371108Z   Full diff:
2026-06-07T06:12:40.1371299Z     [
2026-06-07T06:12:40.1371478Z         'date_range',
2026-06-07T06:12:40.1371709Z   +     'input_completeness_status',
2026-06-07T06:12:40.1371967Z   +     'run_health_status',
2026-06-07T06:12:40.1372187Z     ]
2026-06-07T06:12:40.1372392Z 2 failed, 1703 passed, 1 skipped in 14.52s
2026-06-07T06:12:40.4985510Z ##[error]Process completed with exit code 1.
```

```text
2026-06-07T06:12:40.1371709Z   +     'input_completeness_status',
2026-06-07T06:12:40.1371967Z   +     'run_health_status',
2026-06-07T06:12:40.1372187Z     ]
2026-06-07T06:12:40.1372392Z 2 failed, 1703 passed, 1 skipped in 14.52s
2026-06-07T06:12:40.4985510Z ##[error]Process completed with exit code 1.
2026-06-07T06:12:40.5101864Z Post job cleanup.
2026-06-07T06:12:40.6124009Z [command]/usr/bin/git version
2026-06-07T06:12:40.6163739Z git version 2.54.0
2026-06-07T06:12:40.6212449Z Temporarily overriding HOME='/home/runner/work/_temp/9a3e5771-8bfa-42fd-bd58-12bd1b31c498' before making global git config changes
2026-06-07T06:12:40.6213421Z Adding repository directory to the temporary git global config as a safe directory
2026-06-07T06:12:40.6221060Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-06-07T06:12:40.6260353Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-06-07T06:12:40.6294360Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-06-07T06:12:40.6532783Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-06-07T06:12:40.6559339Z http.https://github.com/.extraheader
2026-06-07T06:12:40.6572352Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

## CI

- Run ID: `27084626823`
- Branch: `main`
- Commit: `068124df8549`
- Title: P124 require backtest health fields in real-data evidence
- Created: 2026-06-07T06:12:04Z
- Updated: 2026-06-07T06:13:00Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27084626823

### Failed job: Pytest

- Job ID: `79936521034`
- Started: 2026-06-07T06:12:06Z
- Completed: 2026-06-07T06:12:59Z
- Failed steps: 53. Full regression suite residual tests

#### Error context

```text
2026-06-07T06:12:55.4037857Z ........................................................................ [ 86%]
2026-06-07T06:12:55.7664017Z ........................................................................ [ 91%]
2026-06-07T06:12:56.0106369Z ........................................................................ [ 97%]
2026-06-07T06:12:56.0631477Z .............................                                            [100%]
2026-06-07T06:12:56.0632050Z =================================== FAILURES ===================================
2026-06-07T06:12:56.0632594Z ______________ test_p121_valid_real_data_backtest_evidence_passes ______________
2026-06-07T06:12:56.0632934Z 
2026-06-07T06:12:56.0633162Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-33/test_p121_valid_real_data_back0')
2026-06-07T06:12:56.0633679Z 
2026-06-07T06:12:56.0633902Z     def test_p121_valid_real_data_backtest_evidence_passes(tmp_path: Path) -> None:
2026-06-07T06:12:56.0634285Z         artifact = tmp_path / "real-data-backtest-evidence.json"
2026-06-07T06:12:56.0634648Z         artifact.write_text(json.dumps(_valid_real_payload()), encoding="utf-8")
2026-06-07T06:12:56.0635260Z     
2026-06-07T06:12:56.0635589Z         gate = validate_real_data_backtest_evidence_artifact(artifact)
2026-06-07T06:12:56.0636023Z     
2026-06-07T06:12:56.0636279Z >       assert gate.passed is True
```

```text
2026-06-07T06:12:56.0635260Z     
2026-06-07T06:12:56.0635589Z         gate = validate_real_data_backtest_evidence_artifact(artifact)
2026-06-07T06:12:56.0636023Z     
2026-06-07T06:12:56.0636279Z >       assert gate.passed is True
2026-06-07T06:12:56.0636636Z E       AssertionError: assert False is True
2026-06-07T06:12:56.0637935Z E        +  where False = RealDataBacktestEvidenceGateReport(passed=False, artifact_path='/tmp/pytest-of-runner/pytest-33/test_p121_valid_real_d...cktest-evidence.json', missing_fields=['input_completeness_status', 'run_health_status'], invalid_fields=[], errors=[]).passed
2026-06-07T06:12:56.0638695Z 
2026-06-07T06:12:56.0638864Z tests/test_p121_real_data_backtest_evidence_gate.py:92: AssertionError
2026-06-07T06:12:56.0639288Z __________________ test_p121_missing_date_range_fails_schema ___________________
2026-06-07T06:12:56.0639563Z 
2026-06-07T06:12:56.0639757Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-33/test_p121_missing_date_range_f0')
2026-06-07T06:12:56.0640022Z 
2026-06-07T06:12:56.0640179Z     def test_p121_missing_date_range_fails_schema(tmp_path: Path) -> None:
2026-06-07T06:12:56.0640492Z         payload = _valid_real_payload()
2026-06-07T06:12:56.0640726Z         del payload["date_range"]
2026-06-07T06:12:56.0640984Z         artifact = tmp_path / "missing-date-range.json"
```

```text
2026-06-07T06:12:56.0636279Z >       assert gate.passed is True
2026-06-07T06:12:56.0636636Z E       AssertionError: assert False is True
2026-06-07T06:12:56.0637935Z E        +  where False = RealDataBacktestEvidenceGateReport(passed=False, artifact_path='/tmp/pytest-of-runner/pytest-33/test_p121_valid_real_d...cktest-evidence.json', missing_fields=['input_completeness_status', 'run_health_status'], invalid_fields=[], errors=[]).passed
2026-06-07T06:12:56.0638695Z 
2026-06-07T06:12:56.0638864Z tests/test_p121_real_data_backtest_evidence_gate.py:92: AssertionError
2026-06-07T06:12:56.0639288Z __________________ test_p121_missing_date_range_fails_schema ___________________
2026-06-07T06:12:56.0639563Z 
2026-06-07T06:12:56.0639757Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-33/test_p121_missing_date_range_f0')
2026-06-07T06:12:56.0640022Z 
2026-06-07T06:12:56.0640179Z     def test_p121_missing_date_range_fails_schema(tmp_path: Path) -> None:
2026-06-07T06:12:56.0640492Z         payload = _valid_real_payload()
2026-06-07T06:12:56.0640726Z         del payload["date_range"]
2026-06-07T06:12:56.0640984Z         artifact = tmp_path / "missing-date-range.json"
2026-06-07T06:12:56.0641302Z         artifact.write_text(json.dumps(payload), encoding="utf-8")
2026-06-07T06:12:56.0641567Z     
2026-06-07T06:12:56.0641788Z         gate = validate_real_data_backtest_evidence_artifact(artifact)
```

```text
2026-06-07T06:12:56.0641788Z         gate = validate_real_data_backtest_evidence_artifact(artifact)
2026-06-07T06:12:56.0642050Z     
2026-06-07T06:12:56.0642218Z         assert gate.passed is False
2026-06-07T06:12:56.0642457Z >       assert gate.missing_fields == ["date_range"]
2026-06-07T06:12:56.0642778Z E       AssertionError: assert ['date_range'...ealth_status'] == ['date_range']
2026-06-07T06:12:56.0643152Z E         
2026-06-07T06:12:56.0643431Z E         Left contains 2 more items, first extra item: 'input_completeness_status'
2026-06-07T06:12:56.0643759Z E         
2026-06-07T06:12:56.0643927Z E         Full diff:
2026-06-07T06:12:56.0644109Z E           [
2026-06-07T06:12:56.0644283Z E               'date_range',
2026-06-07T06:12:56.0644497Z E         +     'input_completeness_status',
2026-06-07T06:12:56.0644727Z E         +     'run_health_status',
2026-06-07T06:12:56.0645038Z E           ]
2026-06-07T06:12:56.0645127Z 
2026-06-07T06:12:56.0645542Z tests/test_p121_real_data_backtest_evidence_gate.py:122: AssertionError
```

```text
2026-06-07T06:12:56.0644497Z E         +     'input_completeness_status',
2026-06-07T06:12:56.0644727Z E         +     'run_health_status',
2026-06-07T06:12:56.0645038Z E           ]
2026-06-07T06:12:56.0645127Z 
2026-06-07T06:12:56.0645542Z tests/test_p121_real_data_backtest_evidence_gate.py:122: AssertionError
2026-06-07T06:12:56.0645898Z =========================== short test summary info ============================
2026-06-07T06:12:56.0646565Z FAILED tests/test_p121_real_data_backtest_evidence_gate.py::test_p121_valid_real_data_backtest_evidence_passes - AssertionError: assert False is True
2026-06-07T06:12:56.0647622Z  +  where False = RealDataBacktestEvidenceGateReport(passed=False, artifact_path='/tmp/pytest-of-runner/pytest-33/test_p121_valid_real_d...cktest-evidence.json', missing_fields=['input_completeness_status', 'run_health_status'], invalid_fields=[], errors=[]).passed
2026-06-07T06:12:56.0648715Z FAILED tests/test_p121_real_data_backtest_evidence_gate.py::test_p121_missing_date_range_fails_schema - AssertionError: assert ['date_range'...ealth_status'] == ['date_range']
2026-06-07T06:12:56.0649248Z   
2026-06-07T06:12:56.0649492Z   Left contains 2 more items, first extra item: 'input_completeness_status'
2026-06-07T06:12:56.0649779Z   
2026-06-07T06:12:56.0649955Z   Full diff:
2026-06-07T06:12:56.0650122Z     [
2026-06-07T06:12:56.0650280Z         'date_range',
2026-06-07T06:12:56.0650474Z   +     'input_completeness_status',
```

```text
2026-06-07T06:12:56.0645038Z E           ]
2026-06-07T06:12:56.0645127Z 
2026-06-07T06:12:56.0645542Z tests/test_p121_real_data_backtest_evidence_gate.py:122: AssertionError
2026-06-07T06:12:56.0645898Z =========================== short test summary info ============================
2026-06-07T06:12:56.0646565Z FAILED tests/test_p121_real_data_backtest_evidence_gate.py::test_p121_valid_real_data_backtest_evidence_passes - AssertionError: assert False is True
2026-06-07T06:12:56.0647622Z  +  where False = RealDataBacktestEvidenceGateReport(passed=False, artifact_path='/tmp/pytest-of-runner/pytest-33/test_p121_valid_real_d...cktest-evidence.json', missing_fields=['input_completeness_status', 'run_health_status'], invalid_fields=[], errors=[]).passed
2026-06-07T06:12:56.0648715Z FAILED tests/test_p121_real_data_backtest_evidence_gate.py::test_p121_missing_date_range_fails_schema - AssertionError: assert ['date_range'...ealth_status'] == ['date_range']
2026-06-07T06:12:56.0649248Z   
2026-06-07T06:12:56.0649492Z   Left contains 2 more items, first extra item: 'input_completeness_status'
2026-06-07T06:12:56.0649779Z   
2026-06-07T06:12:56.0649955Z   Full diff:
2026-06-07T06:12:56.0650122Z     [
2026-06-07T06:12:56.0650280Z         'date_range',
2026-06-07T06:12:56.0650474Z   +     'input_completeness_status',
2026-06-07T06:12:56.0650799Z   +     'run_health_status',
2026-06-07T06:12:56.0650989Z     ]
```

```text
2026-06-07T06:12:56.0645542Z tests/test_p121_real_data_backtest_evidence_gate.py:122: AssertionError
2026-06-07T06:12:56.0645898Z =========================== short test summary info ============================
2026-06-07T06:12:56.0646565Z FAILED tests/test_p121_real_data_backtest_evidence_gate.py::test_p121_valid_real_data_backtest_evidence_passes - AssertionError: assert False is True
2026-06-07T06:12:56.0647622Z  +  where False = RealDataBacktestEvidenceGateReport(passed=False, artifact_path='/tmp/pytest-of-runner/pytest-33/test_p121_valid_real_d...cktest-evidence.json', missing_fields=['input_completeness_status', 'run_health_status'], invalid_fields=[], errors=[]).passed
2026-06-07T06:12:56.0648715Z FAILED tests/test_p121_real_data_backtest_evidence_gate.py::test_p121_missing_date_range_fails_schema - AssertionError: assert ['date_range'...ealth_status'] == ['date_range']
2026-06-07T06:12:56.0649248Z   
2026-06-07T06:12:56.0649492Z   Left contains 2 more items, first extra item: 'input_completeness_status'
2026-06-07T06:12:56.0649779Z   
2026-06-07T06:12:56.0649955Z   Full diff:
2026-06-07T06:12:56.0650122Z     [
2026-06-07T06:12:56.0650280Z         'date_range',
2026-06-07T06:12:56.0650474Z   +     'input_completeness_status',
2026-06-07T06:12:56.0650799Z   +     'run_health_status',
2026-06-07T06:12:56.0650989Z     ]
2026-06-07T06:12:56.0651165Z 2 failed, 1250 passed, 1 skipped in 10.52s
2026-06-07T06:12:56.2939785Z ##[error]Process completed with exit code 1.
```

```text
2026-06-07T06:12:56.0650474Z   +     'input_completeness_status',
2026-06-07T06:12:56.0650799Z   +     'run_health_status',
2026-06-07T06:12:56.0650989Z     ]
2026-06-07T06:12:56.0651165Z 2 failed, 1250 passed, 1 skipped in 10.52s
2026-06-07T06:12:56.2939785Z ##[error]Process completed with exit code 1.
2026-06-07T06:12:56.2997629Z ##[group]Run actions/upload-artifact@v4
2026-06-07T06:12:56.2997873Z with:
2026-06-07T06:12:56.2998059Z   name: p109-residual-pytest-evidence
2026-06-07T06:12:56.2998319Z   path: artifacts/evidence/p109-residual-pytest/
2026-06-07T06:12:56.2998580Z   if-no-files-found: warn
2026-06-07T06:12:56.2998780Z   compression-level: 6
2026-06-07T06:12:56.2998970Z   overwrite: false
2026-06-07T06:12:56.2999157Z   include-hidden-files: false
2026-06-07T06:12:56.2999353Z env:
2026-06-07T06:12:56.2999567Z   pythonLocation: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-07T06:12:56.2999914Z   PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib/pkgconfig
```

## Report Quality Validation

- Run ID: `27084626819`
- Branch: `main`
- Commit: `068124df8549`
- Title: P124 require backtest health fields in real-data evidence
- Created: 2026-06-07T06:12:04Z
- Updated: 2026-06-07T06:13:12Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27084626819

### Failed job: validate-reports (premarket)

- Job ID: `79936521015`
- Started: 2026-06-07T06:12:06Z
- Completed: 2026-06-07T06:13:08Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-07T06:12:24.4524740Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-07T06:12:24.4525138Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-07T06:12:24.4525562Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-07T06:12:24.4525924Z ##[endgroup]
2026-06-07T06:13:05.7988667Z Traceback (most recent call last):
2026-06-07T06:13:05.7996566Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 491, in <module>
2026-06-07T06:13:05.7998188Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-03/2026-06-07?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-07T06:13:05.7999164Z     raise SystemExit(main())
2026-06-07T06:13:05.7999433Z                      ^^^^^^
2026-06-07T06:13:05.8000571Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 474, in main
2026-06-07T06:13:05.8001390Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-07T06:13:05.8001870Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-07T06:13:05.8002670Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 108, in write_report_text_guarded
2026-06-07T06:13:05.8003496Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-07T06:13:05.8004364Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-07T06:13:05.8005122Z     raise ReportOutputBoundaryError(
```

```text
2026-06-07T06:13:05.8005122Z     raise ReportOutputBoundaryError(
2026-06-07T06:13:05.8006500Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/premarket-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
2026-06-07T06:13:05.8008566Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-03/2026-06-07?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-07T06:13:05.8010125Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-03/2026-06-07?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-07T06:13:05.8537362Z ##[error]Process completed with exit code 1.
2026-06-07T06:13:05.8622635Z ##[group]Run actions/upload-artifact@v4
2026-06-07T06:13:05.8622942Z with:
2026-06-07T06:13:05.8623171Z   name: validated-premarket-report
2026-06-07T06:13:05.8623474Z   path: reports/premarket-report.md
2026-06-07T06:13:05.8623939Z   retention-days: 14
2026-06-07T06:13:05.8624180Z   if-no-files-found: warn
2026-06-07T06:13:05.8624425Z   compression-level: 6
2026-06-07T06:13:05.8624670Z   overwrite: false
2026-06-07T06:13:05.8624902Z   include-hidden-files: false
2026-06-07T06:13:05.8625144Z env:
2026-06-07T06:13:05.8625458Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (weekly)

- Job ID: `79936521025`
- Started: 2026-06-07T06:12:06Z
- Completed: 2026-06-07T06:12:24Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-07T06:12:21.8182824Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-07T06:12:21.8183211Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-07T06:12:21.8183624Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-07T06:12:21.8183958Z ##[endgroup]
2026-06-07T06:12:22.6034141Z Traceback (most recent call last):
2026-06-07T06:12:22.6041761Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 491, in <module>
2026-06-07T06:12:22.6042632Z     raise SystemExit(main())
2026-06-07T06:12:22.6042904Z                      ^^^^^^
2026-06-07T06:12:22.6043537Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 474, in main
2026-06-07T06:12:22.6044286Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-07T06:12:22.6044739Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-07T06:12:22.6045512Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 108, in write_report_text_guarded
2026-06-07T06:12:22.6057680Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-07T06:12:22.6058838Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-07T06:12:22.6059574Z     raise ReportOutputBoundaryError(
2026-06-07T06:12:22.6060889Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
```

```text
2026-06-07T06:12:22.6057680Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-07T06:12:22.6058838Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-07T06:12:22.6059574Z     raise ReportOutputBoundaryError(
2026-06-07T06:12:22.6060889Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
2026-06-07T06:12:22.6291566Z ##[error]Process completed with exit code 1.
2026-06-07T06:12:22.6376460Z ##[group]Run actions/upload-artifact@v4
2026-06-07T06:12:22.6376756Z with:
2026-06-07T06:12:22.6377146Z   name: validated-weekly-report
2026-06-07T06:12:22.6377419Z   path: reports/weekly-report.md
2026-06-07T06:12:22.6377681Z   retention-days: 14
2026-06-07T06:12:22.6377906Z   if-no-files-found: warn
2026-06-07T06:12:22.6378146Z   compression-level: 6
2026-06-07T06:12:22.6378378Z   overwrite: false
2026-06-07T06:12:22.6378599Z   include-hidden-files: false
2026-06-07T06:12:22.6378850Z env:
2026-06-07T06:12:22.6379224Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (postmarket)

- Job ID: `79936521026`
- Started: 2026-06-07T06:12:07Z
- Completed: 2026-06-07T06:13:11Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-07T06:12:27.7088523Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-07T06:12:27.7088912Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-07T06:12:27.7089354Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-07T06:12:27.7089687Z ##[endgroup]
2026-06-07T06:13:08.5804653Z Traceback (most recent call last):
2026-06-07T06:13:08.5806791Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-03/2026-06-07?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-07T06:13:08.5809901Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-03/2026-06-07?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-07T06:13:08.5812275Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-03/2026-06-07?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-07T06:13:08.5818964Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 491, in <module>
2026-06-07T06:13:08.5819718Z     raise SystemExit(main())
2026-06-07T06:13:08.5819983Z                      ^^^^^^
2026-06-07T06:13:08.5820625Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 474, in main
2026-06-07T06:13:08.5821405Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-07T06:13:08.5821867Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-07T06:13:08.5822659Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 108, in write_report_text_guarded
2026-06-07T06:13:08.5823811Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
```

```text
2026-06-07T06:13:08.5823811Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-07T06:13:08.5824696Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-07T06:13:08.5825473Z     raise ReportOutputBoundaryError(
2026-06-07T06:13:08.5826913Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/postmarket-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
2026-06-07T06:13:08.6348958Z ##[error]Process completed with exit code 1.
2026-06-07T06:13:08.6429906Z ##[group]Run actions/upload-artifact@v4
2026-06-07T06:13:08.6430211Z with:
2026-06-07T06:13:08.6430428Z   name: validated-postmarket-report
2026-06-07T06:13:08.6430723Z   path: reports/postmarket-report.md
2026-06-07T06:13:08.6431180Z   retention-days: 14
2026-06-07T06:13:08.6431409Z   if-no-files-found: warn
2026-06-07T06:13:08.6431648Z   compression-level: 6
2026-06-07T06:13:08.6431876Z   overwrite: false
2026-06-07T06:13:08.6432100Z   include-hidden-files: false
2026-06-07T06:13:08.6432331Z env:
2026-06-07T06:13:08.6432624Z   POLYGON_API_KEY: ***
```
