# GitHub Actions Workflow Error Report

Generated: 2026-06-13 08:23 UTC
Repository: `yalcinkadir/institutional-trading-engine`
Filter since: 2026-06-12 08:23 UTC
Failed runs included: 8

## Daily Evidence Report

- Run ID: `27447969257`
- Branch: `main`
- Commit: `c3b112105a52`
- Title: Daily Evidence Report
- Created: 2026-06-12T23:00:59Z
- Updated: 2026-06-12T23:01:22Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27447969257

### Failed job: Build daily evidence report

- Job ID: `81137095457`
- Started: 2026-06-12T23:01:03Z
- Completed: 2026-06-12T23:01:21Z
- Failed steps: 7. Build scheduled paper observation incoming sources

#### Error context

```text
2026-06-12T23:01:18.0627091Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-12T23:01:18.0627676Z ##[endgroup]
2026-06-12T23:01:18.1088476Z Daily paper observation source status: FAIL
2026-06-12T23:01:18.1089248Z Built files: 0
2026-06-12T23:01:18.1089725Z ERROR: missing source file: paper_observations.json
2026-06-12T23:01:18.1090382Z ERROR: missing source file: backtest_results.json
2026-06-12T23:01:18.1091194Z ERROR: missing source file: regime_observations.json
2026-06-12T23:01:18.1091880Z ERROR: missing source file: position_snapshots.json
2026-06-12T23:01:18.1159696Z ##[error]Process completed with exit code 1.
2026-06-12T23:01:18.1297370Z ##[group]Run actions/upload-artifact@v4
2026-06-12T23:01:18.1297935Z with:
2026-06-12T23:01:18.1298173Z   name: daily-evidence-report-2026-06-12
2026-06-12T23:01:18.1298472Z   if-no-files-found: error
2026-06-12T23:01:18.1299725Z   path: reports/daily_evidence_source_bootstrap/
reports/daily_paper_observation_source/
reports/daily_observation_cadence/
```

```text
2026-06-12T23:01:18.0627676Z ##[endgroup]
2026-06-12T23:01:18.1088476Z Daily paper observation source status: FAIL
2026-06-12T23:01:18.1089248Z Built files: 0
2026-06-12T23:01:18.1089725Z ERROR: missing source file: paper_observations.json
2026-06-12T23:01:18.1090382Z ERROR: missing source file: backtest_results.json
2026-06-12T23:01:18.1091194Z ERROR: missing source file: regime_observations.json
2026-06-12T23:01:18.1091880Z ERROR: missing source file: position_snapshots.json
2026-06-12T23:01:18.1159696Z ##[error]Process completed with exit code 1.
2026-06-12T23:01:18.1297370Z ##[group]Run actions/upload-artifact@v4
2026-06-12T23:01:18.1297935Z with:
2026-06-12T23:01:18.1298173Z   name: daily-evidence-report-2026-06-12
2026-06-12T23:01:18.1298472Z   if-no-files-found: error
2026-06-12T23:01:18.1299725Z   path: reports/daily_evidence_source_bootstrap/
reports/daily_paper_observation_source/
reports/daily_observation_cadence/
reports/daily_observation_source_feed/
```

```text
2026-06-12T23:01:18.1088476Z Daily paper observation source status: FAIL
2026-06-12T23:01:18.1089248Z Built files: 0
2026-06-12T23:01:18.1089725Z ERROR: missing source file: paper_observations.json
2026-06-12T23:01:18.1090382Z ERROR: missing source file: backtest_results.json
2026-06-12T23:01:18.1091194Z ERROR: missing source file: regime_observations.json
2026-06-12T23:01:18.1091880Z ERROR: missing source file: position_snapshots.json
2026-06-12T23:01:18.1159696Z ##[error]Process completed with exit code 1.
2026-06-12T23:01:18.1297370Z ##[group]Run actions/upload-artifact@v4
2026-06-12T23:01:18.1297935Z with:
2026-06-12T23:01:18.1298173Z   name: daily-evidence-report-2026-06-12
2026-06-12T23:01:18.1298472Z   if-no-files-found: error
2026-06-12T23:01:18.1299725Z   path: reports/daily_evidence_source_bootstrap/
reports/daily_paper_observation_source/
reports/daily_observation_cadence/
reports/daily_observation_source_feed/
reports/daily_observation_feed/
```

```text
2026-06-12T23:01:18.1089248Z Built files: 0
2026-06-12T23:01:18.1089725Z ERROR: missing source file: paper_observations.json
2026-06-12T23:01:18.1090382Z ERROR: missing source file: backtest_results.json
2026-06-12T23:01:18.1091194Z ERROR: missing source file: regime_observations.json
2026-06-12T23:01:18.1091880Z ERROR: missing source file: position_snapshots.json
2026-06-12T23:01:18.1159696Z ##[error]Process completed with exit code 1.
2026-06-12T23:01:18.1297370Z ##[group]Run actions/upload-artifact@v4
2026-06-12T23:01:18.1297935Z with:
2026-06-12T23:01:18.1298173Z   name: daily-evidence-report-2026-06-12
2026-06-12T23:01:18.1298472Z   if-no-files-found: error
2026-06-12T23:01:18.1299725Z   path: reports/daily_evidence_source_bootstrap/
reports/daily_paper_observation_source/
reports/daily_observation_cadence/
reports/daily_observation_source_feed/
reports/daily_observation_feed/
reports/daily_evidence_input_build/
```

```text
2026-06-12T23:01:18.1089725Z ERROR: missing source file: paper_observations.json
2026-06-12T23:01:18.1090382Z ERROR: missing source file: backtest_results.json
2026-06-12T23:01:18.1091194Z ERROR: missing source file: regime_observations.json
2026-06-12T23:01:18.1091880Z ERROR: missing source file: position_snapshots.json
2026-06-12T23:01:18.1159696Z ##[error]Process completed with exit code 1.
2026-06-12T23:01:18.1297370Z ##[group]Run actions/upload-artifact@v4
2026-06-12T23:01:18.1297935Z with:
2026-06-12T23:01:18.1298173Z   name: daily-evidence-report-2026-06-12
2026-06-12T23:01:18.1298472Z   if-no-files-found: error
2026-06-12T23:01:18.1299725Z   path: reports/daily_evidence_source_bootstrap/
reports/daily_paper_observation_source/
reports/daily_observation_cadence/
reports/daily_observation_source_feed/
reports/daily_observation_feed/
reports/daily_evidence_input_build/
reports/daily_evidence_input_validation/
```

## Decision Engine Tests

- Run ID: `27445998992`
- Branch: `main`
- Commit: `c3b112105a52`
- Title: Add compact BT138 research analyzer script
- Created: 2026-06-12T22:11:21Z
- Updated: 2026-06-12T22:12:16Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27445998992

### Failed job: tests

- Job ID: `81130981397`
- Started: 2026-06-12T22:11:29Z
- Completed: 2026-06-12T22:12:15Z
- Failed steps: 5. Run pytest

#### Error context

```text
2026-06-12T22:12:13.5880480Z ........................................................................ [ 91%]
2026-06-12T22:12:13.7936628Z ........................................................................ [ 94%]
2026-06-12T22:12:13.8364463Z ........................................................................ [ 98%]
2026-06-12T22:12:13.9202239Z ...............................                                          [100%]
2026-06-12T22:12:13.9203398Z =================================== FAILURES ===================================
2026-06-12T22:12:13.9204857Z _______ test_198_market_regime_breadth_failure_contains_structured_audit _______
2026-06-12T22:12:13.9205662Z 
2026-06-12T22:12:13.9205925Z monkeypatch = <_pytest.monkeypatch.MonkeyPatch object at 0x7ff93a611e90>
2026-06-12T22:12:13.9206235Z 
2026-06-12T22:12:13.9206697Z     def test_198_market_regime_breadth_failure_contains_structured_audit(monkeypatch: pytest.MonkeyPatch) -> None:
2026-06-12T22:12:13.9207627Z         monkeypatch.setattr(market_regime, "_try_symbol_snapshot", lambda _client, ticker: ({"ticker": ticker, "close": 100, "above_sma50": True, "above_sma200": True}, None))
2026-06-12T22:12:13.9208272Z     
2026-06-12T22:12:13.9208475Z         def broken_breadth(_client):
2026-06-12T22:12:13.9208769Z             raise RuntimeError("breadth failed")
2026-06-12T22:12:13.9209375Z     
2026-06-12T22:12:13.9209684Z         monkeypatch.setattr(market_regime, "_calculate_breadth", broken_breadth)
```

```text
2026-06-12T22:12:13.9210696Z     
2026-06-12T22:12:13.9210907Z         assert summary["exception_audit"]
2026-06-12T22:12:13.9211212Z         audit = summary["exception_audit"][0]
2026-06-12T22:12:13.9211566Z >       assert audit["stage"] == "reporting.market_regime.breadth"
2026-06-12T22:12:13.9212079Z E       AssertionError: assert 'reporting.ma...PolygonClient' == 'reporting.ma...egime.breadth'
2026-06-12T22:12:13.9212518Z E         
2026-06-12T22:12:13.9212745Z E         - reporting.market_regime.breadth
2026-06-12T22:12:13.9213049Z E         ?                         ^^ ^^ -
2026-06-12T22:12:13.9213509Z E         + reporting.market_regime.PolygonClient
2026-06-12T22:12:13.9213816Z E         ?                         ^^^^^^^^^^ ^
2026-06-12T22:12:13.9213999Z 
2026-06-12T22:12:13.9214135Z tests/test_198_exception_audit.py:85: AssertionError
2026-06-12T22:12:13.9214492Z =============================== warnings summary ===============================
2026-06-12T22:12:13.9215019Z tests/test_screening_engine.py::test_asset_score_status_bands
2026-06-12T22:12:13.9216033Z   /home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_screening_engine.py:20: DeprecationWarning: src.scoring.asset_score.calculate_asset_score is deprecated; use src.reporting.decision_report
2026-06-12T22:12:13.9217016Z     strong = calculate_asset_score(25, 25, 20, 10, 10)
```

```text
2026-06-12T22:12:13.9213049Z E         ?                         ^^ ^^ -
2026-06-12T22:12:13.9213509Z E         + reporting.market_regime.PolygonClient
2026-06-12T22:12:13.9213816Z E         ?                         ^^^^^^^^^^ ^
2026-06-12T22:12:13.9213999Z 
2026-06-12T22:12:13.9214135Z tests/test_198_exception_audit.py:85: AssertionError
2026-06-12T22:12:13.9214492Z =============================== warnings summary ===============================
2026-06-12T22:12:13.9215019Z tests/test_screening_engine.py::test_asset_score_status_bands
2026-06-12T22:12:13.9216033Z   /home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_screening_engine.py:20: DeprecationWarning: src.scoring.asset_score.calculate_asset_score is deprecated; use src.reporting.decision_report
2026-06-12T22:12:13.9217016Z     strong = calculate_asset_score(25, 25, 20, 10, 10)
2026-06-12T22:12:13.9217228Z 
2026-06-12T22:12:13.9217396Z tests/test_screening_engine.py::test_asset_score_status_bands
2026-06-12T22:12:13.9218346Z   /home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_screening_engine.py:21: DeprecationWarning: src.scoring.asset_score.calculate_asset_score is deprecated; use src.reporting.decision_report
2026-06-12T22:12:13.9219504Z     ready = calculate_asset_score(20, 20, 15, 10, 10)
2026-06-12T22:12:13.9219715Z 
2026-06-12T22:12:13.9219872Z tests/test_screening_engine.py::test_asset_score_status_bands
2026-06-12T22:12:13.9220813Z   /home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_screening_engine.py:22: DeprecationWarning: src.scoring.asset_score.calculate_asset_score is deprecated; use src.reporting.decision_report
```

```text
2026-06-12T22:12:13.9224220Z     result = calculate_confidence_score(
2026-06-12T22:12:13.9224415Z 
2026-06-12T22:12:13.9224632Z -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2026-06-12T22:12:13.9225069Z =========================== short test summary info ============================
2026-06-12T22:12:13.9226113Z FAILED tests/test_198_exception_audit.py::test_198_market_regime_breadth_failure_contains_structured_audit - AssertionError: assert 'reporting.ma...PolygonClient' == 'reporting.ma...egime.breadth'
2026-06-12T22:12:13.9226995Z   
2026-06-12T22:12:13.9227204Z   - reporting.market_regime.breadth
2026-06-12T22:12:13.9227469Z   ?                         ^^ ^^ -
2026-06-12T22:12:13.9227731Z   + reporting.market_regime.PolygonClient
2026-06-12T22:12:13.9228000Z   ?                         ^^^^^^^^^^ ^
2026-06-12T22:12:13.9228299Z 1 failed, 2045 passed, 1 skipped, 4 warnings in 28.97s
2026-06-12T22:12:14.3746809Z ##[error]Process completed with exit code 1.
2026-06-12T22:12:14.3886000Z Post job cleanup.
2026-06-12T22:12:14.4870288Z [command]/usr/bin/git version
2026-06-12T22:12:14.4906829Z git version 2.54.0
2026-06-12T22:12:14.4950178Z Temporarily overriding HOME='/home/runner/work/_temp/98bd4f3a-d5bc-4bb7-b0b9-9fa4cff32ce5' before making global git config changes
```

```text
2026-06-12T22:12:13.9227469Z   ?                         ^^ ^^ -
2026-06-12T22:12:13.9227731Z   + reporting.market_regime.PolygonClient
2026-06-12T22:12:13.9228000Z   ?                         ^^^^^^^^^^ ^
2026-06-12T22:12:13.9228299Z 1 failed, 2045 passed, 1 skipped, 4 warnings in 28.97s
2026-06-12T22:12:14.3746809Z ##[error]Process completed with exit code 1.
2026-06-12T22:12:14.3886000Z Post job cleanup.
2026-06-12T22:12:14.4870288Z [command]/usr/bin/git version
2026-06-12T22:12:14.4906829Z git version 2.54.0
2026-06-12T22:12:14.4950178Z Temporarily overriding HOME='/home/runner/work/_temp/98bd4f3a-d5bc-4bb7-b0b9-9fa4cff32ce5' before making global git config changes
2026-06-12T22:12:14.4951471Z Adding repository directory to the temporary git global config as a safe directory
2026-06-12T22:12:14.4964857Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-06-12T22:12:14.5003927Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-06-12T22:12:14.5038620Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-06-12T22:12:14.5281892Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-06-12T22:12:14.5307440Z http.https://github.com/.extraheader
2026-06-12T22:12:14.5319750Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

## Decision Engine Tests

- Run ID: `27445964957`
- Branch: `main`
- Commit: `a2b2fe971762`
- Title: Add BT138 partial T1 trailing exit guard tests
- Created: 2026-06-12T22:10:30Z
- Updated: 2026-06-12T22:10:58Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27445964957

### Failed job: tests

- Job ID: `81130871044`
- Started: 2026-06-12T22:10:33Z
- Completed: 2026-06-12T22:10:57Z
- Failed steps: 5. Run pytest

#### Error context

```text
2026-06-12T22:10:48.4395810Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-12T22:10:48.4396172Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-12T22:10:48.4396488Z ##[endgroup]
2026-06-12T22:10:54.7735673Z 
2026-06-12T22:10:54.7736308Z ==================================== ERRORS ====================================
2026-06-12T22:10:54.7736846Z ________ ERROR collecting tests/test_bt138_partial_t1_trailing_exit.py _________
2026-06-12T22:10:54.7737637Z ImportError while importing test module '/home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_bt138_partial_t1_trailing_exit.py'.
2026-06-12T22:10:54.7738709Z Hint: make sure your test modules/packages have valid Python names.
2026-06-12T22:10:54.7739039Z Traceback:
2026-06-12T22:10:54.7739420Z /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/importlib/__init__.py:126: in import_module
2026-06-12T22:10:54.7739933Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-06-12T22:10:54.7740319Z tests/test_bt138_partial_t1_trailing_exit.py:6: in <module>
2026-06-12T22:10:54.7740790Z     from scripts.bt138_partial_t1_trailing_exit import build_bt138_report, persist_bt138_report
2026-06-12T22:10:54.7741331Z E   ModuleNotFoundError: No module named 'scripts.bt138_partial_t1_trailing_exit'
2026-06-12T22:10:54.7741770Z =========================== short test summary info ============================
2026-06-12T22:10:54.7742142Z ERROR tests/test_bt138_partial_t1_trailing_exit.py
```

```text
2026-06-12T22:10:48.4396172Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-12T22:10:48.4396488Z ##[endgroup]
2026-06-12T22:10:54.7735673Z 
2026-06-12T22:10:54.7736308Z ==================================== ERRORS ====================================
2026-06-12T22:10:54.7736846Z ________ ERROR collecting tests/test_bt138_partial_t1_trailing_exit.py _________
2026-06-12T22:10:54.7737637Z ImportError while importing test module '/home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_bt138_partial_t1_trailing_exit.py'.
2026-06-12T22:10:54.7738709Z Hint: make sure your test modules/packages have valid Python names.
2026-06-12T22:10:54.7739039Z Traceback:
2026-06-12T22:10:54.7739420Z /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/importlib/__init__.py:126: in import_module
2026-06-12T22:10:54.7739933Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-06-12T22:10:54.7740319Z tests/test_bt138_partial_t1_trailing_exit.py:6: in <module>
2026-06-12T22:10:54.7740790Z     from scripts.bt138_partial_t1_trailing_exit import build_bt138_report, persist_bt138_report
2026-06-12T22:10:54.7741331Z E   ModuleNotFoundError: No module named 'scripts.bt138_partial_t1_trailing_exit'
2026-06-12T22:10:54.7741770Z =========================== short test summary info ============================
2026-06-12T22:10:54.7742142Z ERROR tests/test_bt138_partial_t1_trailing_exit.py
2026-06-12T22:10:54.7742512Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
```

```text
2026-06-12T22:10:48.4396488Z ##[endgroup]
2026-06-12T22:10:54.7735673Z 
2026-06-12T22:10:54.7736308Z ==================================== ERRORS ====================================
2026-06-12T22:10:54.7736846Z ________ ERROR collecting tests/test_bt138_partial_t1_trailing_exit.py _________
2026-06-12T22:10:54.7737637Z ImportError while importing test module '/home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_bt138_partial_t1_trailing_exit.py'.
2026-06-12T22:10:54.7738709Z Hint: make sure your test modules/packages have valid Python names.
2026-06-12T22:10:54.7739039Z Traceback:
2026-06-12T22:10:54.7739420Z /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/importlib/__init__.py:126: in import_module
2026-06-12T22:10:54.7739933Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-06-12T22:10:54.7740319Z tests/test_bt138_partial_t1_trailing_exit.py:6: in <module>
2026-06-12T22:10:54.7740790Z     from scripts.bt138_partial_t1_trailing_exit import build_bt138_report, persist_bt138_report
2026-06-12T22:10:54.7741331Z E   ModuleNotFoundError: No module named 'scripts.bt138_partial_t1_trailing_exit'
2026-06-12T22:10:54.7741770Z =========================== short test summary info ============================
2026-06-12T22:10:54.7742142Z ERROR tests/test_bt138_partial_t1_trailing_exit.py
2026-06-12T22:10:54.7742512Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-06-12T22:10:54.7742833Z 1 error in 5.80s
```

```text
2026-06-12T22:10:54.7736308Z ==================================== ERRORS ====================================
2026-06-12T22:10:54.7736846Z ________ ERROR collecting tests/test_bt138_partial_t1_trailing_exit.py _________
2026-06-12T22:10:54.7737637Z ImportError while importing test module '/home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_bt138_partial_t1_trailing_exit.py'.
2026-06-12T22:10:54.7738709Z Hint: make sure your test modules/packages have valid Python names.
2026-06-12T22:10:54.7739039Z Traceback:
2026-06-12T22:10:54.7739420Z /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/importlib/__init__.py:126: in import_module
2026-06-12T22:10:54.7739933Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-06-12T22:10:54.7740319Z tests/test_bt138_partial_t1_trailing_exit.py:6: in <module>
2026-06-12T22:10:54.7740790Z     from scripts.bt138_partial_t1_trailing_exit import build_bt138_report, persist_bt138_report
2026-06-12T22:10:54.7741331Z E   ModuleNotFoundError: No module named 'scripts.bt138_partial_t1_trailing_exit'
2026-06-12T22:10:54.7741770Z =========================== short test summary info ============================
2026-06-12T22:10:54.7742142Z ERROR tests/test_bt138_partial_t1_trailing_exit.py
2026-06-12T22:10:54.7742512Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-06-12T22:10:54.7742833Z 1 error in 5.80s
2026-06-12T22:10:55.0569451Z ##[error]Process completed with exit code 2.
2026-06-12T22:10:55.0706094Z Post job cleanup.
```

```text
2026-06-12T22:10:54.7739420Z /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/importlib/__init__.py:126: in import_module
2026-06-12T22:10:54.7739933Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-06-12T22:10:54.7740319Z tests/test_bt138_partial_t1_trailing_exit.py:6: in <module>
2026-06-12T22:10:54.7740790Z     from scripts.bt138_partial_t1_trailing_exit import build_bt138_report, persist_bt138_report
2026-06-12T22:10:54.7741331Z E   ModuleNotFoundError: No module named 'scripts.bt138_partial_t1_trailing_exit'
2026-06-12T22:10:54.7741770Z =========================== short test summary info ============================
2026-06-12T22:10:54.7742142Z ERROR tests/test_bt138_partial_t1_trailing_exit.py
2026-06-12T22:10:54.7742512Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-06-12T22:10:54.7742833Z 1 error in 5.80s
2026-06-12T22:10:55.0569451Z ##[error]Process completed with exit code 2.
2026-06-12T22:10:55.0706094Z Post job cleanup.
2026-06-12T22:10:55.1639938Z [command]/usr/bin/git version
2026-06-12T22:10:55.1673240Z git version 2.54.0
2026-06-12T22:10:55.1712216Z Temporarily overriding HOME='/home/runner/work/_temp/af10b556-a6d9-4f2f-b6e0-ed95843e3548' before making global git config changes
2026-06-12T22:10:55.1713374Z Adding repository directory to the temporary git global config as a safe directory
2026-06-12T22:10:55.1725793Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
```

```text
2026-06-12T22:10:54.7740319Z tests/test_bt138_partial_t1_trailing_exit.py:6: in <module>
2026-06-12T22:10:54.7740790Z     from scripts.bt138_partial_t1_trailing_exit import build_bt138_report, persist_bt138_report
2026-06-12T22:10:54.7741331Z E   ModuleNotFoundError: No module named 'scripts.bt138_partial_t1_trailing_exit'
2026-06-12T22:10:54.7741770Z =========================== short test summary info ============================
2026-06-12T22:10:54.7742142Z ERROR tests/test_bt138_partial_t1_trailing_exit.py
2026-06-12T22:10:54.7742512Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-06-12T22:10:54.7742833Z 1 error in 5.80s
2026-06-12T22:10:55.0569451Z ##[error]Process completed with exit code 2.
2026-06-12T22:10:55.0706094Z Post job cleanup.
2026-06-12T22:10:55.1639938Z [command]/usr/bin/git version
2026-06-12T22:10:55.1673240Z git version 2.54.0
2026-06-12T22:10:55.1712216Z Temporarily overriding HOME='/home/runner/work/_temp/af10b556-a6d9-4f2f-b6e0-ed95843e3548' before making global git config changes
2026-06-12T22:10:55.1713374Z Adding repository directory to the temporary git global config as a safe directory
2026-06-12T22:10:55.1725793Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-06-12T22:10:55.1757278Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-06-12T22:10:55.1786033Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
```

```text
2026-06-12T22:10:54.7741770Z =========================== short test summary info ============================
2026-06-12T22:10:54.7742142Z ERROR tests/test_bt138_partial_t1_trailing_exit.py
2026-06-12T22:10:54.7742512Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-06-12T22:10:54.7742833Z 1 error in 5.80s
2026-06-12T22:10:55.0569451Z ##[error]Process completed with exit code 2.
2026-06-12T22:10:55.0706094Z Post job cleanup.
2026-06-12T22:10:55.1639938Z [command]/usr/bin/git version
2026-06-12T22:10:55.1673240Z git version 2.54.0
2026-06-12T22:10:55.1712216Z Temporarily overriding HOME='/home/runner/work/_temp/af10b556-a6d9-4f2f-b6e0-ed95843e3548' before making global git config changes
2026-06-12T22:10:55.1713374Z Adding repository directory to the temporary git global config as a safe directory
2026-06-12T22:10:55.1725793Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-06-12T22:10:55.1757278Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-06-12T22:10:55.1786033Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-06-12T22:10:55.1965334Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-06-12T22:10:55.1986425Z http.https://github.com/.extraheader
2026-06-12T22:10:55.1996848Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

## CI

- Run ID: `27445964966`
- Branch: `main`
- Commit: `a2b2fe971762`
- Title: Add BT138 partial T1 trailing exit guard tests
- Created: 2026-06-12T22:10:30Z
- Updated: 2026-06-12T22:11:23Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27445964966

### Failed job: Pytest

- Job ID: `81130871087`
- Started: 2026-06-12T22:10:33Z
- Completed: 2026-06-12T22:11:22Z
- Failed steps: 53. Full regression suite residual tests

#### Error context

```text
2026-06-12T22:11:14.3220285Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-12T22:11:14.3220625Z   POLYGON_API_KEY: test-key
2026-06-12T22:11:14.3220877Z ##[endgroup]
2026-06-12T22:11:19.3590240Z 
2026-06-12T22:11:19.3590942Z ==================================== ERRORS ====================================
2026-06-12T22:11:19.3592236Z ________ ERROR collecting tests/test_bt138_partial_t1_trailing_exit.py _________
2026-06-12T22:11:19.3594896Z ImportError while importing test module '/home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_bt138_partial_t1_trailing_exit.py'.
2026-06-12T22:11:19.3597273Z Hint: make sure your test modules/packages have valid Python names.
2026-06-12T22:11:19.3598221Z Traceback:
2026-06-12T22:11:19.3599286Z /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/importlib/__init__.py:126: in import_module
2026-06-12T22:11:19.3600774Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-06-12T22:11:19.3601865Z tests/test_bt138_partial_t1_trailing_exit.py:6: in <module>
2026-06-12T22:11:19.3603310Z     from scripts.bt138_partial_t1_trailing_exit import build_bt138_report, persist_bt138_report
2026-06-12T22:11:19.3605365Z E   ModuleNotFoundError: No module named 'scripts.bt138_partial_t1_trailing_exit'
2026-06-12T22:11:19.3606649Z =========================== short test summary info ============================
2026-06-12T22:11:19.3607672Z ERROR tests/test_bt138_partial_t1_trailing_exit.py
```

```text
2026-06-12T22:11:14.3220625Z   POLYGON_API_KEY: test-key
2026-06-12T22:11:14.3220877Z ##[endgroup]
2026-06-12T22:11:19.3590240Z 
2026-06-12T22:11:19.3590942Z ==================================== ERRORS ====================================
2026-06-12T22:11:19.3592236Z ________ ERROR collecting tests/test_bt138_partial_t1_trailing_exit.py _________
2026-06-12T22:11:19.3594896Z ImportError while importing test module '/home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_bt138_partial_t1_trailing_exit.py'.
2026-06-12T22:11:19.3597273Z Hint: make sure your test modules/packages have valid Python names.
2026-06-12T22:11:19.3598221Z Traceback:
2026-06-12T22:11:19.3599286Z /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/importlib/__init__.py:126: in import_module
2026-06-12T22:11:19.3600774Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-06-12T22:11:19.3601865Z tests/test_bt138_partial_t1_trailing_exit.py:6: in <module>
2026-06-12T22:11:19.3603310Z     from scripts.bt138_partial_t1_trailing_exit import build_bt138_report, persist_bt138_report
2026-06-12T22:11:19.3605365Z E   ModuleNotFoundError: No module named 'scripts.bt138_partial_t1_trailing_exit'
2026-06-12T22:11:19.3606649Z =========================== short test summary info ============================
2026-06-12T22:11:19.3607672Z ERROR tests/test_bt138_partial_t1_trailing_exit.py
2026-06-12T22:11:19.3608750Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
```

```text
2026-06-12T22:11:14.3220877Z ##[endgroup]
2026-06-12T22:11:19.3590240Z 
2026-06-12T22:11:19.3590942Z ==================================== ERRORS ====================================
2026-06-12T22:11:19.3592236Z ________ ERROR collecting tests/test_bt138_partial_t1_trailing_exit.py _________
2026-06-12T22:11:19.3594896Z ImportError while importing test module '/home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_bt138_partial_t1_trailing_exit.py'.
2026-06-12T22:11:19.3597273Z Hint: make sure your test modules/packages have valid Python names.
2026-06-12T22:11:19.3598221Z Traceback:
2026-06-12T22:11:19.3599286Z /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/importlib/__init__.py:126: in import_module
2026-06-12T22:11:19.3600774Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-06-12T22:11:19.3601865Z tests/test_bt138_partial_t1_trailing_exit.py:6: in <module>
2026-06-12T22:11:19.3603310Z     from scripts.bt138_partial_t1_trailing_exit import build_bt138_report, persist_bt138_report
2026-06-12T22:11:19.3605365Z E   ModuleNotFoundError: No module named 'scripts.bt138_partial_t1_trailing_exit'
2026-06-12T22:11:19.3606649Z =========================== short test summary info ============================
2026-06-12T22:11:19.3607672Z ERROR tests/test_bt138_partial_t1_trailing_exit.py
2026-06-12T22:11:19.3608750Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-06-12T22:11:19.3609706Z 1 error in 4.85s
```

```text
2026-06-12T22:11:19.3590942Z ==================================== ERRORS ====================================
2026-06-12T22:11:19.3592236Z ________ ERROR collecting tests/test_bt138_partial_t1_trailing_exit.py _________
2026-06-12T22:11:19.3594896Z ImportError while importing test module '/home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_bt138_partial_t1_trailing_exit.py'.
2026-06-12T22:11:19.3597273Z Hint: make sure your test modules/packages have valid Python names.
2026-06-12T22:11:19.3598221Z Traceback:
2026-06-12T22:11:19.3599286Z /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/importlib/__init__.py:126: in import_module
2026-06-12T22:11:19.3600774Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-06-12T22:11:19.3601865Z tests/test_bt138_partial_t1_trailing_exit.py:6: in <module>
2026-06-12T22:11:19.3603310Z     from scripts.bt138_partial_t1_trailing_exit import build_bt138_report, persist_bt138_report
2026-06-12T22:11:19.3605365Z E   ModuleNotFoundError: No module named 'scripts.bt138_partial_t1_trailing_exit'
2026-06-12T22:11:19.3606649Z =========================== short test summary info ============================
2026-06-12T22:11:19.3607672Z ERROR tests/test_bt138_partial_t1_trailing_exit.py
2026-06-12T22:11:19.3608750Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-06-12T22:11:19.3609706Z 1 error in 4.85s
2026-06-12T22:11:19.5721810Z ##[error]Process completed with exit code 2.
2026-06-12T22:11:19.5790832Z ##[group]Run actions/upload-artifact@v4
```

```text
2026-06-12T22:11:19.3599286Z /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/importlib/__init__.py:126: in import_module
2026-06-12T22:11:19.3600774Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-06-12T22:11:19.3601865Z tests/test_bt138_partial_t1_trailing_exit.py:6: in <module>
2026-06-12T22:11:19.3603310Z     from scripts.bt138_partial_t1_trailing_exit import build_bt138_report, persist_bt138_report
2026-06-12T22:11:19.3605365Z E   ModuleNotFoundError: No module named 'scripts.bt138_partial_t1_trailing_exit'
2026-06-12T22:11:19.3606649Z =========================== short test summary info ============================
2026-06-12T22:11:19.3607672Z ERROR tests/test_bt138_partial_t1_trailing_exit.py
2026-06-12T22:11:19.3608750Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-06-12T22:11:19.3609706Z 1 error in 4.85s
2026-06-12T22:11:19.5721810Z ##[error]Process completed with exit code 2.
2026-06-12T22:11:19.5790832Z ##[group]Run actions/upload-artifact@v4
2026-06-12T22:11:19.5791110Z with:
2026-06-12T22:11:19.5791319Z   name: p109-residual-pytest-evidence
2026-06-12T22:11:19.5791624Z   path: artifacts/evidence/p109-residual-pytest/
2026-06-12T22:11:19.5791921Z   if-no-files-found: warn
2026-06-12T22:11:19.5792154Z   compression-level: 6
```

```text
2026-06-12T22:11:19.3601865Z tests/test_bt138_partial_t1_trailing_exit.py:6: in <module>
2026-06-12T22:11:19.3603310Z     from scripts.bt138_partial_t1_trailing_exit import build_bt138_report, persist_bt138_report
2026-06-12T22:11:19.3605365Z E   ModuleNotFoundError: No module named 'scripts.bt138_partial_t1_trailing_exit'
2026-06-12T22:11:19.3606649Z =========================== short test summary info ============================
2026-06-12T22:11:19.3607672Z ERROR tests/test_bt138_partial_t1_trailing_exit.py
2026-06-12T22:11:19.3608750Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-06-12T22:11:19.3609706Z 1 error in 4.85s
2026-06-12T22:11:19.5721810Z ##[error]Process completed with exit code 2.
2026-06-12T22:11:19.5790832Z ##[group]Run actions/upload-artifact@v4
2026-06-12T22:11:19.5791110Z with:
2026-06-12T22:11:19.5791319Z   name: p109-residual-pytest-evidence
2026-06-12T22:11:19.5791624Z   path: artifacts/evidence/p109-residual-pytest/
2026-06-12T22:11:19.5791921Z   if-no-files-found: warn
2026-06-12T22:11:19.5792154Z   compression-level: 6
2026-06-12T22:11:19.5792383Z   overwrite: false
2026-06-12T22:11:19.5792594Z   include-hidden-files: false
```

```text
2026-06-12T22:11:19.3606649Z =========================== short test summary info ============================
2026-06-12T22:11:19.3607672Z ERROR tests/test_bt138_partial_t1_trailing_exit.py
2026-06-12T22:11:19.3608750Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-06-12T22:11:19.3609706Z 1 error in 4.85s
2026-06-12T22:11:19.5721810Z ##[error]Process completed with exit code 2.
2026-06-12T22:11:19.5790832Z ##[group]Run actions/upload-artifact@v4
2026-06-12T22:11:19.5791110Z with:
2026-06-12T22:11:19.5791319Z   name: p109-residual-pytest-evidence
2026-06-12T22:11:19.5791624Z   path: artifacts/evidence/p109-residual-pytest/
2026-06-12T22:11:19.5791921Z   if-no-files-found: warn
2026-06-12T22:11:19.5792154Z   compression-level: 6
2026-06-12T22:11:19.5792383Z   overwrite: false
2026-06-12T22:11:19.5792594Z   include-hidden-files: false
2026-06-12T22:11:19.5792824Z env:
2026-06-12T22:11:19.5793074Z   pythonLocation: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-12T22:11:19.5793482Z   PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib/pkgconfig
```

## Institutional Reports

- Run ID: `27444608495`
- Branch: `main`
- Commit: `91bc88ab532d`
- Title: Institutional Reports
- Created: 2026-06-12T21:39:41Z
- Updated: 2026-06-12T21:40:55Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27444608495

### Failed job: Generate scheduled report

- Job ID: `81126560106`
- Started: 2026-06-12T21:39:44Z
- Completed: 2026-06-12T21:40:54Z
- Failed steps: 17. Enforce scheduled report liveness gate

#### Error context

```text
2026-06-12T21:40:52.5969787Z   REPORT_LIVENESS_HEALTH: reports/health/report-liveness-latest.json
2026-06-12T21:40:52.5970253Z   SCHEDULED_REPORT_LIVENESS_EXIT_CODE: 1
2026-06-12T21:40:52.5970581Z ##[endgroup]
2026-06-12T21:40:52.6026788Z Scheduled report liveness gate blocked. Evidence was written before failing the workflow.
2026-06-12T21:40:52.6038227Z ##[error]Process completed with exit code 1.
2026-06-12T21:40:52.6162563Z Post job cleanup.
2026-06-12T21:40:52.7154423Z [command]/usr/bin/git version
2026-06-12T21:40:52.7191517Z git version 2.54.0
2026-06-12T21:40:52.7237933Z Temporarily overriding HOME='/home/runner/work/_temp/c566ecdc-87fe-4f66-8407-2dc87e47caf9' before making global git config changes
2026-06-12T21:40:52.7238966Z Adding repository directory to the temporary git global config as a safe directory
2026-06-12T21:40:52.7246125Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-06-12T21:40:52.7282512Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-06-12T21:40:52.7316242Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-06-12T21:40:52.7559014Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-06-12T21:40:52.7572491Z http.https://github.com/.extraheader
2026-06-12T21:40:52.7586038Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

## Decision Engine Tests

- Run ID: `27444456460`
- Branch: `main`
- Commit: `91bc88ab532d`
- Title: Add BT137 research analyzer script
- Created: 2026-06-12T21:36:13Z
- Updated: 2026-06-12T21:37:07Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27444456460

### Failed job: tests

- Job ID: `81126060495`
- Started: 2026-06-12T21:36:16Z
- Completed: 2026-06-12T21:37:06Z
- Failed steps: 5. Run pytest

#### Error context

```text
2026-06-12T21:37:02.9573929Z ........................................................................ [ 91%]
2026-06-12T21:37:03.1814251Z ........................................................................ [ 95%]
2026-06-12T21:37:03.2362822Z ........................................................................ [ 98%]
2026-06-12T21:37:03.3188740Z ...........................                                              [100%]
2026-06-12T21:37:03.3189460Z =================================== FAILURES ===================================
2026-06-12T21:37:03.3190327Z _______ test_198_market_regime_breadth_failure_contains_structured_audit _______
2026-06-12T21:37:03.3190838Z 
2026-06-12T21:37:03.3191059Z monkeypatch = <_pytest.monkeypatch.MonkeyPatch object at 0x7f56798516d0>
2026-06-12T21:37:03.3191379Z 
2026-06-12T21:37:03.3191799Z     def test_198_market_regime_breadth_failure_contains_structured_audit(monkeypatch: pytest.MonkeyPatch) -> None:
2026-06-12T21:37:03.3192783Z         monkeypatch.setattr(market_regime, "_try_symbol_snapshot", lambda _client, ticker: ({"ticker": ticker, "close": 100, "above_sma50": True, "above_sma200": True}, None))
2026-06-12T21:37:03.3193482Z     
2026-06-12T21:37:03.3193677Z         def broken_breadth(_client):
2026-06-12T21:37:03.3193973Z             raise RuntimeError("breadth failed")
2026-06-12T21:37:03.3194249Z     
2026-06-12T21:37:03.3194550Z         monkeypatch.setattr(market_regime, "_calculate_breadth", broken_breadth)
```

```text
2026-06-12T21:37:03.3195583Z     
2026-06-12T21:37:03.3195778Z         assert summary["exception_audit"]
2026-06-12T21:37:03.3196074Z         audit = summary["exception_audit"][0]
2026-06-12T21:37:03.3196428Z >       assert audit["stage"] == "reporting.market_regime.breadth"
2026-06-12T21:37:03.3197421Z E       AssertionError: assert 'reporting.ma...PolygonClient' == 'reporting.ma...egime.breadth'
2026-06-12T21:37:03.3197893Z E         
2026-06-12T21:37:03.3198108Z E         - reporting.market_regime.breadth
2026-06-12T21:37:03.3198423Z E         ?                         ^^ ^^ -
2026-06-12T21:37:03.3198743Z E         + reporting.market_regime.PolygonClient
2026-06-12T21:37:03.3199051Z E         ?                         ^^^^^^^^^^ ^
2026-06-12T21:37:03.3199236Z 
2026-06-12T21:37:03.3199377Z tests/test_198_exception_audit.py:85: AssertionError
2026-06-12T21:37:03.3199750Z =============================== warnings summary ===============================
2026-06-12T21:37:03.3200281Z tests/test_screening_engine.py::test_asset_score_status_bands
2026-06-12T21:37:03.3201367Z   /home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_screening_engine.py:20: DeprecationWarning: src.scoring.asset_score.calculate_asset_score is deprecated; use src.reporting.decision_report
2026-06-12T21:37:03.3202447Z     strong = calculate_asset_score(25, 25, 20, 10, 10)
```

```text
2026-06-12T21:37:03.3198423Z E         ?                         ^^ ^^ -
2026-06-12T21:37:03.3198743Z E         + reporting.market_regime.PolygonClient
2026-06-12T21:37:03.3199051Z E         ?                         ^^^^^^^^^^ ^
2026-06-12T21:37:03.3199236Z 
2026-06-12T21:37:03.3199377Z tests/test_198_exception_audit.py:85: AssertionError
2026-06-12T21:37:03.3199750Z =============================== warnings summary ===============================
2026-06-12T21:37:03.3200281Z tests/test_screening_engine.py::test_asset_score_status_bands
2026-06-12T21:37:03.3201367Z   /home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_screening_engine.py:20: DeprecationWarning: src.scoring.asset_score.calculate_asset_score is deprecated; use src.reporting.decision_report
2026-06-12T21:37:03.3202447Z     strong = calculate_asset_score(25, 25, 20, 10, 10)
2026-06-12T21:37:03.3202671Z 
2026-06-12T21:37:03.3202836Z tests/test_screening_engine.py::test_asset_score_status_bands
2026-06-12T21:37:03.3203939Z   /home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_screening_engine.py:21: DeprecationWarning: src.scoring.asset_score.calculate_asset_score is deprecated; use src.reporting.decision_report
2026-06-12T21:37:03.3204975Z     ready = calculate_asset_score(20, 20, 15, 10, 10)
2026-06-12T21:37:03.3205192Z 
2026-06-12T21:37:03.3205362Z tests/test_screening_engine.py::test_asset_score_status_bands
2026-06-12T21:37:03.3206424Z   /home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_screening_engine.py:22: DeprecationWarning: src.scoring.asset_score.calculate_asset_score is deprecated; use src.reporting.decision_report
```

```text
2026-06-12T21:37:03.3210332Z     result = calculate_confidence_score(
2026-06-12T21:37:03.3210528Z 
2026-06-12T21:37:03.3210752Z -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2026-06-12T21:37:03.3211213Z =========================== short test summary info ============================
2026-06-12T21:37:03.3212305Z FAILED tests/test_198_exception_audit.py::test_198_market_regime_breadth_failure_contains_structured_audit - AssertionError: assert 'reporting.ma...PolygonClient' == 'reporting.ma...egime.breadth'
2026-06-12T21:37:03.3213262Z   
2026-06-12T21:37:03.3213471Z   - reporting.market_regime.breadth
2026-06-12T21:37:03.3213737Z   ?                         ^^ ^^ -
2026-06-12T21:37:03.3214008Z   + reporting.market_regime.PolygonClient
2026-06-12T21:37:03.3214287Z   ?                         ^^^^^^^^^^ ^
2026-06-12T21:37:03.3214595Z 1 failed, 2041 passed, 1 skipped, 4 warnings in 28.88s
2026-06-12T21:37:03.7029569Z ##[error]Process completed with exit code 1.
2026-06-12T21:37:03.7174254Z Post job cleanup.
2026-06-12T21:37:03.8185718Z [command]/usr/bin/git version
2026-06-12T21:37:03.8222858Z git version 2.54.0
2026-06-12T21:37:03.8266879Z Temporarily overriding HOME='/home/runner/work/_temp/d491cd7f-b62c-425d-997c-3300461a9efd' before making global git config changes
```

```text
2026-06-12T21:37:03.3213737Z   ?                         ^^ ^^ -
2026-06-12T21:37:03.3214008Z   + reporting.market_regime.PolygonClient
2026-06-12T21:37:03.3214287Z   ?                         ^^^^^^^^^^ ^
2026-06-12T21:37:03.3214595Z 1 failed, 2041 passed, 1 skipped, 4 warnings in 28.88s
2026-06-12T21:37:03.7029569Z ##[error]Process completed with exit code 1.
2026-06-12T21:37:03.7174254Z Post job cleanup.
2026-06-12T21:37:03.8185718Z [command]/usr/bin/git version
2026-06-12T21:37:03.8222858Z git version 2.54.0
2026-06-12T21:37:03.8266879Z Temporarily overriding HOME='/home/runner/work/_temp/d491cd7f-b62c-425d-997c-3300461a9efd' before making global git config changes
2026-06-12T21:37:03.8268151Z Adding repository directory to the temporary git global config as a safe directory
2026-06-12T21:37:03.8273081Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-06-12T21:37:03.8308535Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-06-12T21:37:03.8340298Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-06-12T21:37:03.8565447Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-06-12T21:37:03.8590369Z http.https://github.com/.extraheader
2026-06-12T21:37:03.8603859Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

## Decision Engine Tests

- Run ID: `27444267018`
- Branch: `main`
- Commit: `50f20c978c8e`
- Title: test_bt137_regime_breadth_entry_gate.py erstellen
- Created: 2026-06-12T21:32:06Z
- Updated: 2026-06-12T21:32:38Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27444267018

### Failed job: tests

- Job ID: `81125458670`
- Started: 2026-06-12T21:32:15Z
- Completed: 2026-06-12T21:32:37Z
- Failed steps: 5. Run pytest

#### Error context

```text
2026-06-12T21:32:29.1655595Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-12T21:32:29.1655985Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-12T21:32:29.1656311Z ##[endgroup]
2026-06-12T21:32:35.5548118Z 
2026-06-12T21:32:35.5548762Z ==================================== ERRORS ====================================
2026-06-12T21:32:35.5550213Z ________ ERROR collecting tests/test_bt137_regime_breadth_entry_gate.py ________
2026-06-12T21:32:35.5551642Z ImportError while importing test module '/home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_bt137_regime_breadth_entry_gate.py'.
2026-06-12T21:32:35.5552971Z Hint: make sure your test modules/packages have valid Python names.
2026-06-12T21:32:35.5553519Z Traceback:
2026-06-12T21:32:35.5554138Z /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/importlib/__init__.py:126: in import_module
2026-06-12T21:32:35.5554990Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-06-12T21:32:35.5555636Z tests/test_bt137_regime_breadth_entry_gate.py:6: in <module>
2026-06-12T21:32:35.5556179Z     from scripts.bt137_regime_breadth_entry_gate import (
2026-06-12T21:32:35.5556651Z E   ModuleNotFoundError: No module named 'scripts.bt137_regime_breadth_entry_gate'
2026-06-12T21:32:35.5557136Z =========================== short test summary info ============================
2026-06-12T21:32:35.5557517Z ERROR tests/test_bt137_regime_breadth_entry_gate.py
```

```text
2026-06-12T21:32:29.1655985Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-12T21:32:29.1656311Z ##[endgroup]
2026-06-12T21:32:35.5548118Z 
2026-06-12T21:32:35.5548762Z ==================================== ERRORS ====================================
2026-06-12T21:32:35.5550213Z ________ ERROR collecting tests/test_bt137_regime_breadth_entry_gate.py ________
2026-06-12T21:32:35.5551642Z ImportError while importing test module '/home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_bt137_regime_breadth_entry_gate.py'.
2026-06-12T21:32:35.5552971Z Hint: make sure your test modules/packages have valid Python names.
2026-06-12T21:32:35.5553519Z Traceback:
2026-06-12T21:32:35.5554138Z /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/importlib/__init__.py:126: in import_module
2026-06-12T21:32:35.5554990Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-06-12T21:32:35.5555636Z tests/test_bt137_regime_breadth_entry_gate.py:6: in <module>
2026-06-12T21:32:35.5556179Z     from scripts.bt137_regime_breadth_entry_gate import (
2026-06-12T21:32:35.5556651Z E   ModuleNotFoundError: No module named 'scripts.bt137_regime_breadth_entry_gate'
2026-06-12T21:32:35.5557136Z =========================== short test summary info ============================
2026-06-12T21:32:35.5557517Z ERROR tests/test_bt137_regime_breadth_entry_gate.py
2026-06-12T21:32:35.5557911Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
```

```text
2026-06-12T21:32:29.1656311Z ##[endgroup]
2026-06-12T21:32:35.5548118Z 
2026-06-12T21:32:35.5548762Z ==================================== ERRORS ====================================
2026-06-12T21:32:35.5550213Z ________ ERROR collecting tests/test_bt137_regime_breadth_entry_gate.py ________
2026-06-12T21:32:35.5551642Z ImportError while importing test module '/home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_bt137_regime_breadth_entry_gate.py'.
2026-06-12T21:32:35.5552971Z Hint: make sure your test modules/packages have valid Python names.
2026-06-12T21:32:35.5553519Z Traceback:
2026-06-12T21:32:35.5554138Z /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/importlib/__init__.py:126: in import_module
2026-06-12T21:32:35.5554990Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-06-12T21:32:35.5555636Z tests/test_bt137_regime_breadth_entry_gate.py:6: in <module>
2026-06-12T21:32:35.5556179Z     from scripts.bt137_regime_breadth_entry_gate import (
2026-06-12T21:32:35.5556651Z E   ModuleNotFoundError: No module named 'scripts.bt137_regime_breadth_entry_gate'
2026-06-12T21:32:35.5557136Z =========================== short test summary info ============================
2026-06-12T21:32:35.5557517Z ERROR tests/test_bt137_regime_breadth_entry_gate.py
2026-06-12T21:32:35.5557911Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-06-12T21:32:35.5558255Z 1 error in 5.89s
```

```text
2026-06-12T21:32:35.5548762Z ==================================== ERRORS ====================================
2026-06-12T21:32:35.5550213Z ________ ERROR collecting tests/test_bt137_regime_breadth_entry_gate.py ________
2026-06-12T21:32:35.5551642Z ImportError while importing test module '/home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_bt137_regime_breadth_entry_gate.py'.
2026-06-12T21:32:35.5552971Z Hint: make sure your test modules/packages have valid Python names.
2026-06-12T21:32:35.5553519Z Traceback:
2026-06-12T21:32:35.5554138Z /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/importlib/__init__.py:126: in import_module
2026-06-12T21:32:35.5554990Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-06-12T21:32:35.5555636Z tests/test_bt137_regime_breadth_entry_gate.py:6: in <module>
2026-06-12T21:32:35.5556179Z     from scripts.bt137_regime_breadth_entry_gate import (
2026-06-12T21:32:35.5556651Z E   ModuleNotFoundError: No module named 'scripts.bt137_regime_breadth_entry_gate'
2026-06-12T21:32:35.5557136Z =========================== short test summary info ============================
2026-06-12T21:32:35.5557517Z ERROR tests/test_bt137_regime_breadth_entry_gate.py
2026-06-12T21:32:35.5557911Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-06-12T21:32:35.5558255Z 1 error in 5.89s
2026-06-12T21:32:35.7697402Z ##[error]Process completed with exit code 2.
2026-06-12T21:32:35.7835913Z Post job cleanup.
```

```text
2026-06-12T21:32:35.5554138Z /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/importlib/__init__.py:126: in import_module
2026-06-12T21:32:35.5554990Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-06-12T21:32:35.5555636Z tests/test_bt137_regime_breadth_entry_gate.py:6: in <module>
2026-06-12T21:32:35.5556179Z     from scripts.bt137_regime_breadth_entry_gate import (
2026-06-12T21:32:35.5556651Z E   ModuleNotFoundError: No module named 'scripts.bt137_regime_breadth_entry_gate'
2026-06-12T21:32:35.5557136Z =========================== short test summary info ============================
2026-06-12T21:32:35.5557517Z ERROR tests/test_bt137_regime_breadth_entry_gate.py
2026-06-12T21:32:35.5557911Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-06-12T21:32:35.5558255Z 1 error in 5.89s
2026-06-12T21:32:35.7697402Z ##[error]Process completed with exit code 2.
2026-06-12T21:32:35.7835913Z Post job cleanup.
2026-06-12T21:32:35.8807178Z [command]/usr/bin/git version
2026-06-12T21:32:35.8843366Z git version 2.54.0
2026-06-12T21:32:35.8885031Z Temporarily overriding HOME='/home/runner/work/_temp/7a8d3ed0-e680-4532-a12e-c3f27452a2e9' before making global git config changes
2026-06-12T21:32:35.8886299Z Adding repository directory to the temporary git global config as a safe directory
2026-06-12T21:32:35.8891943Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
```

```text
2026-06-12T21:32:35.5555636Z tests/test_bt137_regime_breadth_entry_gate.py:6: in <module>
2026-06-12T21:32:35.5556179Z     from scripts.bt137_regime_breadth_entry_gate import (
2026-06-12T21:32:35.5556651Z E   ModuleNotFoundError: No module named 'scripts.bt137_regime_breadth_entry_gate'
2026-06-12T21:32:35.5557136Z =========================== short test summary info ============================
2026-06-12T21:32:35.5557517Z ERROR tests/test_bt137_regime_breadth_entry_gate.py
2026-06-12T21:32:35.5557911Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-06-12T21:32:35.5558255Z 1 error in 5.89s
2026-06-12T21:32:35.7697402Z ##[error]Process completed with exit code 2.
2026-06-12T21:32:35.7835913Z Post job cleanup.
2026-06-12T21:32:35.8807178Z [command]/usr/bin/git version
2026-06-12T21:32:35.8843366Z git version 2.54.0
2026-06-12T21:32:35.8885031Z Temporarily overriding HOME='/home/runner/work/_temp/7a8d3ed0-e680-4532-a12e-c3f27452a2e9' before making global git config changes
2026-06-12T21:32:35.8886299Z Adding repository directory to the temporary git global config as a safe directory
2026-06-12T21:32:35.8891943Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-06-12T21:32:35.8933879Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-06-12T21:32:35.8966800Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
```

```text
2026-06-12T21:32:35.5557136Z =========================== short test summary info ============================
2026-06-12T21:32:35.5557517Z ERROR tests/test_bt137_regime_breadth_entry_gate.py
2026-06-12T21:32:35.5557911Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-06-12T21:32:35.5558255Z 1 error in 5.89s
2026-06-12T21:32:35.7697402Z ##[error]Process completed with exit code 2.
2026-06-12T21:32:35.7835913Z Post job cleanup.
2026-06-12T21:32:35.8807178Z [command]/usr/bin/git version
2026-06-12T21:32:35.8843366Z git version 2.54.0
2026-06-12T21:32:35.8885031Z Temporarily overriding HOME='/home/runner/work/_temp/7a8d3ed0-e680-4532-a12e-c3f27452a2e9' before making global git config changes
2026-06-12T21:32:35.8886299Z Adding repository directory to the temporary git global config as a safe directory
2026-06-12T21:32:35.8891943Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-06-12T21:32:35.8933879Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-06-12T21:32:35.8966800Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-06-12T21:32:35.9207001Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-06-12T21:32:35.9232641Z http.https://github.com/.extraheader
2026-06-12T21:32:35.9245913Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

## CI

- Run ID: `27444267084`
- Branch: `main`
- Commit: `50f20c978c8e`
- Title: test_bt137_regime_breadth_entry_gate.py erstellen
- Created: 2026-06-12T21:32:06Z
- Updated: 2026-06-12T21:33:01Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27444267084

### Failed job: Pytest

- Job ID: `81125458959`
- Started: 2026-06-12T21:32:15Z
- Completed: 2026-06-12T21:33:00Z
- Failed steps: 53. Full regression suite residual tests

#### Error context

```text
2026-06-12T21:32:52.6737382Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-12T21:32:52.6737730Z   POLYGON_API_KEY: test-key
2026-06-12T21:32:52.6737968Z ##[endgroup]
2026-06-12T21:32:58.1744443Z 
2026-06-12T21:32:58.1745023Z ==================================== ERRORS ====================================
2026-06-12T21:32:58.1745563Z ________ ERROR collecting tests/test_bt137_regime_breadth_entry_gate.py ________
2026-06-12T21:32:58.1746423Z ImportError while importing test module '/home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_bt137_regime_breadth_entry_gate.py'.
2026-06-12T21:32:58.1747225Z Hint: make sure your test modules/packages have valid Python names.
2026-06-12T21:32:58.1747581Z Traceback:
2026-06-12T21:32:58.1747981Z /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/importlib/__init__.py:126: in import_module
2026-06-12T21:32:58.1748783Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-06-12T21:32:58.1749190Z tests/test_bt137_regime_breadth_entry_gate.py:6: in <module>
2026-06-12T21:32:58.1749600Z     from scripts.bt137_regime_breadth_entry_gate import (
2026-06-12T21:32:58.1750313Z E   ModuleNotFoundError: No module named 'scripts.bt137_regime_breadth_entry_gate'
2026-06-12T21:32:58.1750807Z =========================== short test summary info ============================
2026-06-12T21:32:58.1751182Z ERROR tests/test_bt137_regime_breadth_entry_gate.py
```

```text
2026-06-12T21:32:52.6737730Z   POLYGON_API_KEY: test-key
2026-06-12T21:32:52.6737968Z ##[endgroup]
2026-06-12T21:32:58.1744443Z 
2026-06-12T21:32:58.1745023Z ==================================== ERRORS ====================================
2026-06-12T21:32:58.1745563Z ________ ERROR collecting tests/test_bt137_regime_breadth_entry_gate.py ________
2026-06-12T21:32:58.1746423Z ImportError while importing test module '/home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_bt137_regime_breadth_entry_gate.py'.
2026-06-12T21:32:58.1747225Z Hint: make sure your test modules/packages have valid Python names.
2026-06-12T21:32:58.1747581Z Traceback:
2026-06-12T21:32:58.1747981Z /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/importlib/__init__.py:126: in import_module
2026-06-12T21:32:58.1748783Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-06-12T21:32:58.1749190Z tests/test_bt137_regime_breadth_entry_gate.py:6: in <module>
2026-06-12T21:32:58.1749600Z     from scripts.bt137_regime_breadth_entry_gate import (
2026-06-12T21:32:58.1750313Z E   ModuleNotFoundError: No module named 'scripts.bt137_regime_breadth_entry_gate'
2026-06-12T21:32:58.1750807Z =========================== short test summary info ============================
2026-06-12T21:32:58.1751182Z ERROR tests/test_bt137_regime_breadth_entry_gate.py
2026-06-12T21:32:58.1751565Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
```

```text
2026-06-12T21:32:52.6737968Z ##[endgroup]
2026-06-12T21:32:58.1744443Z 
2026-06-12T21:32:58.1745023Z ==================================== ERRORS ====================================
2026-06-12T21:32:58.1745563Z ________ ERROR collecting tests/test_bt137_regime_breadth_entry_gate.py ________
2026-06-12T21:32:58.1746423Z ImportError while importing test module '/home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_bt137_regime_breadth_entry_gate.py'.
2026-06-12T21:32:58.1747225Z Hint: make sure your test modules/packages have valid Python names.
2026-06-12T21:32:58.1747581Z Traceback:
2026-06-12T21:32:58.1747981Z /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/importlib/__init__.py:126: in import_module
2026-06-12T21:32:58.1748783Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-06-12T21:32:58.1749190Z tests/test_bt137_regime_breadth_entry_gate.py:6: in <module>
2026-06-12T21:32:58.1749600Z     from scripts.bt137_regime_breadth_entry_gate import (
2026-06-12T21:32:58.1750313Z E   ModuleNotFoundError: No module named 'scripts.bt137_regime_breadth_entry_gate'
2026-06-12T21:32:58.1750807Z =========================== short test summary info ============================
2026-06-12T21:32:58.1751182Z ERROR tests/test_bt137_regime_breadth_entry_gate.py
2026-06-12T21:32:58.1751565Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-06-12T21:32:58.1751896Z 1 error in 5.30s
```

```text
2026-06-12T21:32:58.1745023Z ==================================== ERRORS ====================================
2026-06-12T21:32:58.1745563Z ________ ERROR collecting tests/test_bt137_regime_breadth_entry_gate.py ________
2026-06-12T21:32:58.1746423Z ImportError while importing test module '/home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_bt137_regime_breadth_entry_gate.py'.
2026-06-12T21:32:58.1747225Z Hint: make sure your test modules/packages have valid Python names.
2026-06-12T21:32:58.1747581Z Traceback:
2026-06-12T21:32:58.1747981Z /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/importlib/__init__.py:126: in import_module
2026-06-12T21:32:58.1748783Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-06-12T21:32:58.1749190Z tests/test_bt137_regime_breadth_entry_gate.py:6: in <module>
2026-06-12T21:32:58.1749600Z     from scripts.bt137_regime_breadth_entry_gate import (
2026-06-12T21:32:58.1750313Z E   ModuleNotFoundError: No module named 'scripts.bt137_regime_breadth_entry_gate'
2026-06-12T21:32:58.1750807Z =========================== short test summary info ============================
2026-06-12T21:32:58.1751182Z ERROR tests/test_bt137_regime_breadth_entry_gate.py
2026-06-12T21:32:58.1751565Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-06-12T21:32:58.1751896Z 1 error in 5.30s
2026-06-12T21:32:58.3939691Z ##[error]Process completed with exit code 2.
2026-06-12T21:32:58.4014676Z ##[group]Run actions/upload-artifact@v4
```

```text
2026-06-12T21:32:58.1747981Z /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/importlib/__init__.py:126: in import_module
2026-06-12T21:32:58.1748783Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-06-12T21:32:58.1749190Z tests/test_bt137_regime_breadth_entry_gate.py:6: in <module>
2026-06-12T21:32:58.1749600Z     from scripts.bt137_regime_breadth_entry_gate import (
2026-06-12T21:32:58.1750313Z E   ModuleNotFoundError: No module named 'scripts.bt137_regime_breadth_entry_gate'
2026-06-12T21:32:58.1750807Z =========================== short test summary info ============================
2026-06-12T21:32:58.1751182Z ERROR tests/test_bt137_regime_breadth_entry_gate.py
2026-06-12T21:32:58.1751565Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-06-12T21:32:58.1751896Z 1 error in 5.30s
2026-06-12T21:32:58.3939691Z ##[error]Process completed with exit code 2.
2026-06-12T21:32:58.4014676Z ##[group]Run actions/upload-artifact@v4
2026-06-12T21:32:58.4014957Z with:
2026-06-12T21:32:58.4015177Z   name: p109-residual-pytest-evidence
2026-06-12T21:32:58.4015484Z   path: artifacts/evidence/p109-residual-pytest/
2026-06-12T21:32:58.4015785Z   if-no-files-found: warn
2026-06-12T21:32:58.4016022Z   compression-level: 6
```

```text
2026-06-12T21:32:58.1749190Z tests/test_bt137_regime_breadth_entry_gate.py:6: in <module>
2026-06-12T21:32:58.1749600Z     from scripts.bt137_regime_breadth_entry_gate import (
2026-06-12T21:32:58.1750313Z E   ModuleNotFoundError: No module named 'scripts.bt137_regime_breadth_entry_gate'
2026-06-12T21:32:58.1750807Z =========================== short test summary info ============================
2026-06-12T21:32:58.1751182Z ERROR tests/test_bt137_regime_breadth_entry_gate.py
2026-06-12T21:32:58.1751565Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-06-12T21:32:58.1751896Z 1 error in 5.30s
2026-06-12T21:32:58.3939691Z ##[error]Process completed with exit code 2.
2026-06-12T21:32:58.4014676Z ##[group]Run actions/upload-artifact@v4
2026-06-12T21:32:58.4014957Z with:
2026-06-12T21:32:58.4015177Z   name: p109-residual-pytest-evidence
2026-06-12T21:32:58.4015484Z   path: artifacts/evidence/p109-residual-pytest/
2026-06-12T21:32:58.4015785Z   if-no-files-found: warn
2026-06-12T21:32:58.4016022Z   compression-level: 6
2026-06-12T21:32:58.4016246Z   overwrite: false
2026-06-12T21:32:58.4016495Z   include-hidden-files: false
```

```text
2026-06-12T21:32:58.1750807Z =========================== short test summary info ============================
2026-06-12T21:32:58.1751182Z ERROR tests/test_bt137_regime_breadth_entry_gate.py
2026-06-12T21:32:58.1751565Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-06-12T21:32:58.1751896Z 1 error in 5.30s
2026-06-12T21:32:58.3939691Z ##[error]Process completed with exit code 2.
2026-06-12T21:32:58.4014676Z ##[group]Run actions/upload-artifact@v4
2026-06-12T21:32:58.4014957Z with:
2026-06-12T21:32:58.4015177Z   name: p109-residual-pytest-evidence
2026-06-12T21:32:58.4015484Z   path: artifacts/evidence/p109-residual-pytest/
2026-06-12T21:32:58.4015785Z   if-no-files-found: warn
2026-06-12T21:32:58.4016022Z   compression-level: 6
2026-06-12T21:32:58.4016246Z   overwrite: false
2026-06-12T21:32:58.4016495Z   include-hidden-files: false
2026-06-12T21:32:58.4016738Z env:
2026-06-12T21:32:58.4016996Z   pythonLocation: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-12T21:32:58.4017427Z   PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib/pkgconfig
```
