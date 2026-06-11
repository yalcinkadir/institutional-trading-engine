# GitHub Actions Workflow Error Report

Generated: 2026-06-11 08:52 UTC
Repository: `yalcinkadir/institutional-trading-engine`
Filter since: 2026-06-10 08:52 UTC
Failed runs included: 10

## Decision Engine Tests

- Run ID: `27335261595`
- Branch: `main`
- Commit: `2c4d4e9631de`
- Title: Update BT9 tests for #184 checksum coverage manifest
- Created: 2026-06-11T08:49:53Z
- Updated: 2026-06-11T08:50:42Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27335261595

### Failed job: tests

- Job ID: `80757641217`
- Started: 2026-06-11T08:49:56Z
- Completed: 2026-06-11T08:50:41Z
- Failed steps: 5. Run pytest

#### Error context

```text
2026-06-11T08:50:39.1858127Z ........................................................................ [ 90%]
2026-06-11T08:50:39.3961193Z ........................................................................ [ 94%]
2026-06-11T08:50:39.4415598Z ........................................................................ [ 97%]
2026-06-11T08:50:39.5345417Z .........................................                                [100%]
2026-06-11T08:50:39.5346098Z =================================== FAILURES ===================================
2026-06-11T08:50:39.5347124Z _________ test_bt130_real_data_runner_blocks_missing_coverage_manifest _________
2026-06-11T08:50:39.5347851Z 
2026-06-11T08:50:39.5348433Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-0/test_bt130_real_data_runner_bl0')
2026-06-11T08:50:39.5350012Z 
2026-06-11T08:50:39.5350787Z     def test_bt130_real_data_runner_blocks_missing_coverage_manifest(tmp_path: Path) -> None:
2026-06-11T08:50:39.5351759Z         plans = tmp_path / "plans.json"
2026-06-11T08:50:39.5352329Z         bars = tmp_path / "bars"
2026-06-11T08:50:39.5352919Z         universe = tmp_path / "universe.csv"
2026-06-11T08:50:39.5353536Z         out = tmp_path / "evidence.json"
2026-06-11T08:50:39.5353927Z         _write_plan(plans)
2026-06-11T08:50:39.5354235Z         _write_bars(bars)
```

```text
2026-06-11T08:50:39.5361509Z         payload = json.loads(out.read_text(encoding="utf-8"))
2026-06-11T08:50:39.5361866Z         assert payload["data_source"] == "real_data"
2026-06-11T08:50:39.5362183Z         assert payload["is_demo"] is False
2026-06-11T08:50:39.5362515Z >       assert payload["input_pack_gate_status"] == "PASSED"
2026-06-11T08:50:39.5362919Z E       AssertionError: assert 'FAILED' == 'PASSED'
2026-06-11T08:50:39.5363234Z E         
2026-06-11T08:50:39.5363435Z E         - PASSED
2026-06-11T08:50:39.5363641Z E         + FAILED
2026-06-11T08:50:39.5363756Z 
2026-06-11T08:50:39.5363969Z tests/test_bt130_real_historical_evidence_pack_gate.py:108: AssertionError
2026-06-11T08:50:39.5364471Z ___________ test_bt130_real_data_runner_blocks_fully_rejected_plans ____________
2026-06-11T08:50:39.5364771Z 
2026-06-11T08:50:39.5365012Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-0/test_bt130_real_data_runner_bl1')
2026-06-11T08:50:39.5365354Z 
2026-06-11T08:50:39.5365590Z     def test_bt130_real_data_runner_blocks_fully_rejected_plans(tmp_path: Path) -> None:
2026-06-11T08:50:39.5366027Z         plans = tmp_path / "plans.json"
```

```text
2026-06-11T08:50:39.5362515Z >       assert payload["input_pack_gate_status"] == "PASSED"
2026-06-11T08:50:39.5362919Z E       AssertionError: assert 'FAILED' == 'PASSED'
2026-06-11T08:50:39.5363234Z E         
2026-06-11T08:50:39.5363435Z E         - PASSED
2026-06-11T08:50:39.5363641Z E         + FAILED
2026-06-11T08:50:39.5363756Z 
2026-06-11T08:50:39.5363969Z tests/test_bt130_real_historical_evidence_pack_gate.py:108: AssertionError
2026-06-11T08:50:39.5364471Z ___________ test_bt130_real_data_runner_blocks_fully_rejected_plans ____________
2026-06-11T08:50:39.5364771Z 
2026-06-11T08:50:39.5365012Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-0/test_bt130_real_data_runner_bl1')
2026-06-11T08:50:39.5365354Z 
2026-06-11T08:50:39.5365590Z     def test_bt130_real_data_runner_blocks_fully_rejected_plans(tmp_path: Path) -> None:
2026-06-11T08:50:39.5366027Z         plans = tmp_path / "plans.json"
2026-06-11T08:50:39.5366311Z         bars = tmp_path / "bars"
2026-06-11T08:50:39.5366585Z         universe = tmp_path / "universe.csv"
2026-06-11T08:50:39.5366892Z         coverage = tmp_path / "coverage.json"
```

```text
2026-06-11T08:50:39.5363234Z E         
2026-06-11T08:50:39.5363435Z E         - PASSED
2026-06-11T08:50:39.5363641Z E         + FAILED
2026-06-11T08:50:39.5363756Z 
2026-06-11T08:50:39.5363969Z tests/test_bt130_real_historical_evidence_pack_gate.py:108: AssertionError
2026-06-11T08:50:39.5364471Z ___________ test_bt130_real_data_runner_blocks_fully_rejected_plans ____________
2026-06-11T08:50:39.5364771Z 
2026-06-11T08:50:39.5365012Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-0/test_bt130_real_data_runner_bl1')
2026-06-11T08:50:39.5365354Z 
2026-06-11T08:50:39.5365590Z     def test_bt130_real_data_runner_blocks_fully_rejected_plans(tmp_path: Path) -> None:
2026-06-11T08:50:39.5366027Z         plans = tmp_path / "plans.json"
2026-06-11T08:50:39.5366311Z         bars = tmp_path / "bars"
2026-06-11T08:50:39.5366585Z         universe = tmp_path / "universe.csv"
2026-06-11T08:50:39.5366892Z         coverage = tmp_path / "coverage.json"
2026-06-11T08:50:39.5367196Z         out = tmp_path / "evidence.json"
2026-06-11T08:50:39.5367500Z         _write_plan(plans, unsupported_action=True)
```

```text
2026-06-11T08:50:39.5372846Z         )
2026-06-11T08:50:39.5373025Z     
2026-06-11T08:50:39.5373226Z         assert result.returncode == 1
2026-06-11T08:50:39.5373541Z >       assert "accepted_plan_count=0" in result.stdout
2026-06-11T08:50:39.5374351Z E       AssertionError: assert 'accepted_plan_count=0' in 'BT9 real historical input pack gate status: FAIL\n- coverage_manifest_symbol_0_not_object\n- coverage_manifest_missing_symbol:SPY\n'
2026-06-11T08:50:39.5376300Z E        +  where 'BT9 real historical input pack gate status: FAIL\n- coverage_manifest_symbol_0_not_object\n- coverage_manifest_missing_symbol:SPY\n' = CompletedProcess(args=['/opt/hostedtoolcache/Python/3.11.15/x64/bin/python', 'scripts/run_historical_entry_exit_backte... pack gate status: FAIL\n- coverage_manifest_symbol_0_not_object\n- coverage_manifest_missing_symbol:SPY\n', stderr='').stdout
2026-06-11T08:50:39.5378476Z 
2026-06-11T08:50:39.5378789Z tests/test_bt130_real_historical_evidence_pack_gate.py:142: AssertionError
2026-06-11T08:50:39.5379566Z __________________ test_177_pipeline_export_is_bt9_compatible __________________
2026-06-11T08:50:39.5379865Z 
2026-06-11T08:50:39.5380122Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-0/test_177_pipeline_export_is_bt0')
2026-06-11T08:50:39.5380469Z 
2026-06-11T08:50:39.5380674Z     def test_177_pipeline_export_is_bt9_compatible(tmp_path: Path) -> None:
2026-06-11T08:50:39.5381074Z         source = tmp_path / "pipeline.json"
2026-06-11T08:50:39.5381440Z         output = tmp_path / "data/trade_plans/historical_trade_plans.json"
2026-06-11T08:50:39.5381946Z         manifest = tmp_path / "data/trade_plans/historical_trade_plans_manifest.json"
```

```text
2026-06-11T08:50:39.5373541Z >       assert "accepted_plan_count=0" in result.stdout
2026-06-11T08:50:39.5374351Z E       AssertionError: assert 'accepted_plan_count=0' in 'BT9 real historical input pack gate status: FAIL\n- coverage_manifest_symbol_0_not_object\n- coverage_manifest_missing_symbol:SPY\n'
2026-06-11T08:50:39.5376300Z E        +  where 'BT9 real historical input pack gate status: FAIL\n- coverage_manifest_symbol_0_not_object\n- coverage_manifest_missing_symbol:SPY\n' = CompletedProcess(args=['/opt/hostedtoolcache/Python/3.11.15/x64/bin/python', 'scripts/run_historical_entry_exit_backte... pack gate status: FAIL\n- coverage_manifest_symbol_0_not_object\n- coverage_manifest_missing_symbol:SPY\n', stderr='').stdout
2026-06-11T08:50:39.5378476Z 
2026-06-11T08:50:39.5378789Z tests/test_bt130_real_historical_evidence_pack_gate.py:142: AssertionError
2026-06-11T08:50:39.5379566Z __________________ test_177_pipeline_export_is_bt9_compatible __________________
2026-06-11T08:50:39.5379865Z 
2026-06-11T08:50:39.5380122Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-0/test_177_pipeline_export_is_bt0')
2026-06-11T08:50:39.5380469Z 
2026-06-11T08:50:39.5380674Z     def test_177_pipeline_export_is_bt9_compatible(tmp_path: Path) -> None:
2026-06-11T08:50:39.5381074Z         source = tmp_path / "pipeline.json"
2026-06-11T08:50:39.5381440Z         output = tmp_path / "data/trade_plans/historical_trade_plans.json"
2026-06-11T08:50:39.5381946Z         manifest = tmp_path / "data/trade_plans/historical_trade_plans_manifest.json"
2026-06-11T08:50:39.5382434Z         universe = tmp_path / "data/universe/survivorship_universe.csv"
2026-06-11T08:50:39.5382839Z         bars_root = tmp_path / "data/historical/bars/1day"
2026-06-11T08:50:39.5383165Z         _write_pipeline_source(source)
```

```text
2026-06-11T08:50:39.5389617Z     
2026-06-11T08:50:39.5389840Z         assert export_report.passed is True
2026-06-11T08:50:39.5390294Z         assert export_report.pipeline_generation_source == "scanner_signal_quality_validator"
2026-06-11T08:50:39.5390750Z >       assert bt9_report.passed is True
2026-06-11T08:50:39.5391043Z E       AssertionError: assert False is True
2026-06-11T08:50:39.5392275Z E        +  where False = BT9RealHistoricalInputPackReport(passed=False, universe_path='/tmp/pytest-of-runner/pytest-0/test_177_pipeline_export_...3e644908770ab592dbe5422a3513996f116f'}, failures=['missing_coverage_manifest', 'coverage_manifest_missing_symbol:SPY']).passed
2026-06-11T08:50:39.5393358Z 
2026-06-11T08:50:39.5393547Z tests/test_htp1_historical_trade_plan_export.py:288: AssertionError
2026-06-11T08:50:39.5394007Z ______________________ test_htp1_export_is_bt9_compatible ______________________
2026-06-11T08:50:39.5394286Z 
2026-06-11T08:50:39.5394531Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-0/test_htp1_export_is_bt9_compat0')
2026-06-11T08:50:39.5394867Z 
2026-06-11T08:50:39.5395042Z     def test_htp1_export_is_bt9_compatible(tmp_path: Path) -> None:
2026-06-11T08:50:39.5395430Z         source = tmp_path / "observations.json"
2026-06-11T08:50:39.5395823Z         output = tmp_path / "data/trade_plans/historical_trade_plans.json"
2026-06-11T08:50:39.5396306Z         manifest = tmp_path / "data/trade_plans/historical_trade_plans_manifest.json"
```

```text
2026-06-11T08:50:39.5390750Z >       assert bt9_report.passed is True
2026-06-11T08:50:39.5391043Z E       AssertionError: assert False is True
2026-06-11T08:50:39.5392275Z E        +  where False = BT9RealHistoricalInputPackReport(passed=False, universe_path='/tmp/pytest-of-runner/pytest-0/test_177_pipeline_export_...3e644908770ab592dbe5422a3513996f116f'}, failures=['missing_coverage_manifest', 'coverage_manifest_missing_symbol:SPY']).passed
2026-06-11T08:50:39.5393358Z 
2026-06-11T08:50:39.5393547Z tests/test_htp1_historical_trade_plan_export.py:288: AssertionError
2026-06-11T08:50:39.5394007Z ______________________ test_htp1_export_is_bt9_compatible ______________________
2026-06-11T08:50:39.5394286Z 
2026-06-11T08:50:39.5394531Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-0/test_htp1_export_is_bt9_compat0')
2026-06-11T08:50:39.5394867Z 
2026-06-11T08:50:39.5395042Z     def test_htp1_export_is_bt9_compatible(tmp_path: Path) -> None:
2026-06-11T08:50:39.5395430Z         source = tmp_path / "observations.json"
2026-06-11T08:50:39.5395823Z         output = tmp_path / "data/trade_plans/historical_trade_plans.json"
2026-06-11T08:50:39.5396306Z         manifest = tmp_path / "data/trade_plans/historical_trade_plans_manifest.json"
2026-06-11T08:50:39.5396788Z         universe = tmp_path / "data/universe/survivorship_universe.csv"
2026-06-11T08:50:39.5397190Z         bars_root = tmp_path / "data/historical/bars/1day"
2026-06-11T08:50:39.5397531Z         _write_source(source, [_valid_record()])
```

## CI

- Run ID: `27335261027`
- Branch: `main`
- Commit: `2c4d4e9631de`
- Title: Update BT9 tests for #184 checksum coverage manifest
- Created: 2026-06-11T08:49:53Z
- Updated: 2026-06-11T08:51:06Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27335261027

### Failed job: Pytest

- Job ID: `80757639387`
- Started: 2026-06-11T08:49:56Z
- Completed: 2026-06-11T08:51:05Z
- Failed steps: 53. Full regression suite residual tests

#### Error context

```text
2026-06-11T08:51:01.8480391Z ........................................................................ [ 88%]
2026-06-11T08:51:02.0651684Z ........................................................................ [ 93%]
2026-06-11T08:51:02.1154634Z ........................................................................ [ 98%]
2026-06-11T08:51:02.1851668Z ....................                                                     [100%]
2026-06-11T08:51:02.1852857Z =================================== FAILURES ===================================
2026-06-11T08:51:02.1853623Z _________ test_bt130_real_data_runner_blocks_missing_coverage_manifest _________
2026-06-11T08:51:02.1854146Z 
2026-06-11T08:51:02.1854564Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-33/test_bt130_real_data_runner_bl0')
2026-06-11T08:51:02.1855714Z 
2026-06-11T08:51:02.1856316Z     def test_bt130_real_data_runner_blocks_missing_coverage_manifest(tmp_path: Path) -> None:
2026-06-11T08:51:02.1857321Z         plans = tmp_path / "plans.json"
2026-06-11T08:51:02.1857994Z         bars = tmp_path / "bars"
2026-06-11T08:51:02.1858658Z         universe = tmp_path / "universe.csv"
2026-06-11T08:51:02.1859412Z         out = tmp_path / "evidence.json"
2026-06-11T08:51:02.1860003Z         _write_plan(plans)
2026-06-11T08:51:02.1860391Z         _write_bars(bars)
```

```text
2026-06-11T08:51:02.1868022Z         payload = json.loads(out.read_text(encoding="utf-8"))
2026-06-11T08:51:02.1868426Z         assert payload["data_source"] == "real_data"
2026-06-11T08:51:02.1868781Z         assert payload["is_demo"] is False
2026-06-11T08:51:02.1869159Z >       assert payload["input_pack_gate_status"] == "PASSED"
2026-06-11T08:51:02.1869572Z E       AssertionError: assert 'FAILED' == 'PASSED'
2026-06-11T08:51:02.1869903Z E         
2026-06-11T08:51:02.1870119Z E         - PASSED
2026-06-11T08:51:02.1870347Z E         + FAILED
2026-06-11T08:51:02.1870487Z 
2026-06-11T08:51:02.1870964Z tests/test_bt130_real_historical_evidence_pack_gate.py:108: AssertionError
2026-06-11T08:51:02.1871554Z ___________ test_bt130_real_data_runner_blocks_fully_rejected_plans ____________
2026-06-11T08:51:02.1871925Z 
2026-06-11T08:51:02.1872212Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-33/test_bt130_real_data_runner_bl1')
2026-06-11T08:51:02.1872606Z 
2026-06-11T08:51:02.1872877Z     def test_bt130_real_data_runner_blocks_fully_rejected_plans(tmp_path: Path) -> None:
2026-06-11T08:51:02.1873383Z         plans = tmp_path / "plans.json"
```

```text
2026-06-11T08:51:02.1869159Z >       assert payload["input_pack_gate_status"] == "PASSED"
2026-06-11T08:51:02.1869572Z E       AssertionError: assert 'FAILED' == 'PASSED'
2026-06-11T08:51:02.1869903Z E         
2026-06-11T08:51:02.1870119Z E         - PASSED
2026-06-11T08:51:02.1870347Z E         + FAILED
2026-06-11T08:51:02.1870487Z 
2026-06-11T08:51:02.1870964Z tests/test_bt130_real_historical_evidence_pack_gate.py:108: AssertionError
2026-06-11T08:51:02.1871554Z ___________ test_bt130_real_data_runner_blocks_fully_rejected_plans ____________
2026-06-11T08:51:02.1871925Z 
2026-06-11T08:51:02.1872212Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-33/test_bt130_real_data_runner_bl1')
2026-06-11T08:51:02.1872606Z 
2026-06-11T08:51:02.1872877Z     def test_bt130_real_data_runner_blocks_fully_rejected_plans(tmp_path: Path) -> None:
2026-06-11T08:51:02.1873383Z         plans = tmp_path / "plans.json"
2026-06-11T08:51:02.1873691Z         bars = tmp_path / "bars"
2026-06-11T08:51:02.1873965Z         universe = tmp_path / "universe.csv"
2026-06-11T08:51:02.1874263Z         coverage = tmp_path / "coverage.json"
```

```text
2026-06-11T08:51:02.1869903Z E         
2026-06-11T08:51:02.1870119Z E         - PASSED
2026-06-11T08:51:02.1870347Z E         + FAILED
2026-06-11T08:51:02.1870487Z 
2026-06-11T08:51:02.1870964Z tests/test_bt130_real_historical_evidence_pack_gate.py:108: AssertionError
2026-06-11T08:51:02.1871554Z ___________ test_bt130_real_data_runner_blocks_fully_rejected_plans ____________
2026-06-11T08:51:02.1871925Z 
2026-06-11T08:51:02.1872212Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-33/test_bt130_real_data_runner_bl1')
2026-06-11T08:51:02.1872606Z 
2026-06-11T08:51:02.1872877Z     def test_bt130_real_data_runner_blocks_fully_rejected_plans(tmp_path: Path) -> None:
2026-06-11T08:51:02.1873383Z         plans = tmp_path / "plans.json"
2026-06-11T08:51:02.1873691Z         bars = tmp_path / "bars"
2026-06-11T08:51:02.1873965Z         universe = tmp_path / "universe.csv"
2026-06-11T08:51:02.1874263Z         coverage = tmp_path / "coverage.json"
2026-06-11T08:51:02.1874567Z         out = tmp_path / "evidence.json"
2026-06-11T08:51:02.1875150Z         _write_plan(plans, unsupported_action=True)
```

```text
2026-06-11T08:51:02.1881037Z         )
2026-06-11T08:51:02.1881215Z     
2026-06-11T08:51:02.1881431Z         assert result.returncode == 1
2026-06-11T08:51:02.1881743Z >       assert "accepted_plan_count=0" in result.stdout
2026-06-11T08:51:02.1882543Z E       AssertionError: assert 'accepted_plan_count=0' in 'BT9 real historical input pack gate status: FAIL\n- coverage_manifest_symbol_0_not_object\n- coverage_manifest_missing_symbol:SPY\n'
2026-06-11T08:51:02.1884478Z E        +  where 'BT9 real historical input pack gate status: FAIL\n- coverage_manifest_symbol_0_not_object\n- coverage_manifest_missing_symbol:SPY\n' = CompletedProcess(args=['/opt/hostedtoolcache/Python/3.11.15/x64/bin/python', 'scripts/run_historical_entry_exit_backte... pack gate status: FAIL\n- coverage_manifest_symbol_0_not_object\n- coverage_manifest_missing_symbol:SPY\n', stderr='').stdout
2026-06-11T08:51:02.1886070Z 
2026-06-11T08:51:02.1886281Z tests/test_bt130_real_historical_evidence_pack_gate.py:142: AssertionError
2026-06-11T08:51:02.1886784Z __________________ test_177_pipeline_export_is_bt9_compatible __________________
2026-06-11T08:51:02.1887081Z 
2026-06-11T08:51:02.1887327Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-33/test_177_pipeline_export_is_bt0')
2026-06-11T08:51:02.1887683Z 
2026-06-11T08:51:02.1887890Z     def test_177_pipeline_export_is_bt9_compatible(tmp_path: Path) -> None:
2026-06-11T08:51:02.1888292Z         source = tmp_path / "pipeline.json"
2026-06-11T08:51:02.1888657Z         output = tmp_path / "data/trade_plans/historical_trade_plans.json"
2026-06-11T08:51:02.1889145Z         manifest = tmp_path / "data/trade_plans/historical_trade_plans_manifest.json"
```

```text
2026-06-11T08:51:02.1881743Z >       assert "accepted_plan_count=0" in result.stdout
2026-06-11T08:51:02.1882543Z E       AssertionError: assert 'accepted_plan_count=0' in 'BT9 real historical input pack gate status: FAIL\n- coverage_manifest_symbol_0_not_object\n- coverage_manifest_missing_symbol:SPY\n'
2026-06-11T08:51:02.1884478Z E        +  where 'BT9 real historical input pack gate status: FAIL\n- coverage_manifest_symbol_0_not_object\n- coverage_manifest_missing_symbol:SPY\n' = CompletedProcess(args=['/opt/hostedtoolcache/Python/3.11.15/x64/bin/python', 'scripts/run_historical_entry_exit_backte... pack gate status: FAIL\n- coverage_manifest_symbol_0_not_object\n- coverage_manifest_missing_symbol:SPY\n', stderr='').stdout
2026-06-11T08:51:02.1886070Z 
2026-06-11T08:51:02.1886281Z tests/test_bt130_real_historical_evidence_pack_gate.py:142: AssertionError
2026-06-11T08:51:02.1886784Z __________________ test_177_pipeline_export_is_bt9_compatible __________________
2026-06-11T08:51:02.1887081Z 
2026-06-11T08:51:02.1887327Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-33/test_177_pipeline_export_is_bt0')
2026-06-11T08:51:02.1887683Z 
2026-06-11T08:51:02.1887890Z     def test_177_pipeline_export_is_bt9_compatible(tmp_path: Path) -> None:
2026-06-11T08:51:02.1888292Z         source = tmp_path / "pipeline.json"
2026-06-11T08:51:02.1888657Z         output = tmp_path / "data/trade_plans/historical_trade_plans.json"
2026-06-11T08:51:02.1889145Z         manifest = tmp_path / "data/trade_plans/historical_trade_plans_manifest.json"
2026-06-11T08:51:02.1889632Z         universe = tmp_path / "data/universe/survivorship_universe.csv"
2026-06-11T08:51:02.1890035Z         bars_root = tmp_path / "data/historical/bars/1day"
2026-06-11T08:51:02.1890364Z         _write_pipeline_source(source)
```

```text
2026-06-11T08:51:02.1897055Z     
2026-06-11T08:51:02.1897268Z         assert export_report.passed is True
2026-06-11T08:51:02.1897971Z         assert export_report.pipeline_generation_source == "scanner_signal_quality_validator"
2026-06-11T08:51:02.1898434Z >       assert bt9_report.passed is True
2026-06-11T08:51:02.1898733Z E       AssertionError: assert False is True
2026-06-11T08:51:02.1899816Z E        +  where False = BT9RealHistoricalInputPackReport(passed=False, universe_path='/tmp/pytest-of-runner/pytest-33/test_177_pipeline_export...3e644908770ab592dbe5422a3513996f116f'}, failures=['missing_coverage_manifest', 'coverage_manifest_missing_symbol:SPY']).passed
2026-06-11T08:51:02.1900798Z 
2026-06-11T08:51:02.1900982Z tests/test_htp1_historical_trade_plan_export.py:288: AssertionError
2026-06-11T08:51:02.1901448Z ______________________ test_htp1_export_is_bt9_compatible ______________________
2026-06-11T08:51:02.1901744Z 
2026-06-11T08:51:02.1901984Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-33/test_htp1_export_is_bt9_compat0')
2026-06-11T08:51:02.1902434Z 
2026-06-11T08:51:02.1902757Z     def test_htp1_export_is_bt9_compatible(tmp_path: Path) -> None:
2026-06-11T08:51:02.1903414Z         source = tmp_path / "observations.json"
2026-06-11T08:51:02.1904018Z         output = tmp_path / "data/trade_plans/historical_trade_plans.json"
2026-06-11T08:51:02.1904509Z         manifest = tmp_path / "data/trade_plans/historical_trade_plans_manifest.json"
```

```text
2026-06-11T08:51:02.1898434Z >       assert bt9_report.passed is True
2026-06-11T08:51:02.1898733Z E       AssertionError: assert False is True
2026-06-11T08:51:02.1899816Z E        +  where False = BT9RealHistoricalInputPackReport(passed=False, universe_path='/tmp/pytest-of-runner/pytest-33/test_177_pipeline_export...3e644908770ab592dbe5422a3513996f116f'}, failures=['missing_coverage_manifest', 'coverage_manifest_missing_symbol:SPY']).passed
2026-06-11T08:51:02.1900798Z 
2026-06-11T08:51:02.1900982Z tests/test_htp1_historical_trade_plan_export.py:288: AssertionError
2026-06-11T08:51:02.1901448Z ______________________ test_htp1_export_is_bt9_compatible ______________________
2026-06-11T08:51:02.1901744Z 
2026-06-11T08:51:02.1901984Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-33/test_htp1_export_is_bt9_compat0')
2026-06-11T08:51:02.1902434Z 
2026-06-11T08:51:02.1902757Z     def test_htp1_export_is_bt9_compatible(tmp_path: Path) -> None:
2026-06-11T08:51:02.1903414Z         source = tmp_path / "observations.json"
2026-06-11T08:51:02.1904018Z         output = tmp_path / "data/trade_plans/historical_trade_plans.json"
2026-06-11T08:51:02.1904509Z         manifest = tmp_path / "data/trade_plans/historical_trade_plans_manifest.json"
2026-06-11T08:51:02.1905260Z         universe = tmp_path / "data/universe/survivorship_universe.csv"
2026-06-11T08:51:02.1905667Z         bars_root = tmp_path / "data/historical/bars/1day"
2026-06-11T08:51:02.1906004Z         _write_source(source, [_valid_record()])
```

## Report Quality Validation

- Run ID: `27335260981`
- Branch: `main`
- Commit: `2c4d4e9631de`
- Title: Update BT9 tests for #184 checksum coverage manifest
- Created: 2026-06-11T08:49:52Z
- Updated: 2026-06-11T08:51:10Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27335260981

### Failed job: validate-reports (postmarket)

- Job ID: `80757639685`
- Started: 2026-06-11T08:49:56Z
- Completed: 2026-06-11T08:51:09Z
- Failed steps: 6. Validate report quality

#### Error context

```text
2026-06-11T08:51:06.0027056Z - Report used fallback data; content is structurally valid but not analytically strong
2026-06-11T08:51:06.0027659Z 
2026-06-11T08:51:06.0027770Z Errors:
2026-06-11T08:51:06.0028073Z - Missing analytical term: Risk Tier
2026-06-11T08:51:06.0097423Z ##[error]Process completed with exit code 1.
2026-06-11T08:51:06.0178140Z ##[group]Run actions/upload-artifact@v4
2026-06-11T08:51:06.0178451Z with:
2026-06-11T08:51:06.0178680Z   name: validated-postmarket-report
2026-06-11T08:51:06.0179004Z   path: reports/generated/postmarket-report.md
2026-06-11T08:51:06.0179470Z   retention-days: 14
2026-06-11T08:51:06.0179749Z   if-no-files-found: warn
2026-06-11T08:51:06.0180000Z   compression-level: 6
2026-06-11T08:51:06.0180228Z   overwrite: false
2026-06-11T08:51:06.0180462Z   include-hidden-files: false
2026-06-11T08:51:06.0180715Z env:
2026-06-11T08:51:06.0181074Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (premarket)

- Job ID: `80757639745`
- Started: 2026-06-11T08:49:55Z
- Completed: 2026-06-11T08:50:54Z
- Failed steps: 6. Validate report quality

#### Error context

```text
2026-06-11T08:50:52.1629639Z - Report used fallback data; content is structurally valid but not analytically strong
2026-06-11T08:50:52.1630027Z 
2026-06-11T08:50:52.1630115Z Errors:
2026-06-11T08:50:52.1630345Z - Missing analytical term: Risk Tier
2026-06-11T08:50:52.1699336Z ##[error]Process completed with exit code 1.
2026-06-11T08:50:52.1778058Z ##[group]Run actions/upload-artifact@v4
2026-06-11T08:50:52.1778360Z with:
2026-06-11T08:50:52.1778594Z   name: validated-premarket-report
2026-06-11T08:50:52.1778910Z   path: reports/generated/premarket-report.md
2026-06-11T08:50:52.1779218Z   retention-days: 14
2026-06-11T08:50:52.1779458Z   if-no-files-found: warn
2026-06-11T08:50:52.1779713Z   compression-level: 6
2026-06-11T08:50:52.1779957Z   overwrite: false
2026-06-11T08:50:52.1780190Z   include-hidden-files: false
2026-06-11T08:50:52.1780445Z env:
2026-06-11T08:50:52.1780774Z   POLYGON_API_KEY: ***
```

## Decision Engine Tests

- Run ID: `27334660619`
- Branch: `main`
- Commit: `7ce082458246`
- Title: Document #184 historical input persistence and checksum requirements
- Created: 2026-06-11T08:38:31Z
- Updated: 2026-06-11T08:39:24Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27334660619

### Failed job: tests

- Job ID: `80755571440`
- Started: 2026-06-11T08:38:35Z
- Completed: 2026-06-11T08:39:23Z
- Failed steps: 5. Run pytest

#### Error context

```text
2026-06-11T08:39:20.8825090Z ........................................................................ [ 90%]
2026-06-11T08:39:21.0989219Z ........................................................................ [ 94%]
2026-06-11T08:39:21.1451447Z ........................................................................ [ 97%]
2026-06-11T08:39:21.2357645Z .........................................                                [100%]
2026-06-11T08:39:21.2358655Z =================================== FAILURES ===================================
2026-06-11T08:39:21.2359432Z _________ test_bt130_real_data_runner_blocks_missing_coverage_manifest _________
2026-06-11T08:39:21.2359952Z 
2026-06-11T08:39:21.2360397Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-0/test_bt130_real_data_runner_bl0')
2026-06-11T08:39:21.2361391Z 
2026-06-11T08:39:21.2361898Z     def test_bt130_real_data_runner_blocks_missing_coverage_manifest(tmp_path: Path) -> None:
2026-06-11T08:39:21.2363081Z         plans = tmp_path / "plans.json"
2026-06-11T08:39:21.2363582Z         bars = tmp_path / "bars"
2026-06-11T08:39:21.2364048Z         universe = tmp_path / "universe.csv"
2026-06-11T08:39:21.2364571Z         out = tmp_path / "evidence.json"
2026-06-11T08:39:21.2365047Z         _write_plan(plans)
2026-06-11T08:39:21.2365487Z         _write_bars(bars)
```

```text
2026-06-11T08:39:21.2375493Z         payload = json.loads(out.read_text(encoding="utf-8"))
2026-06-11T08:39:21.2376127Z         assert payload["data_source"] == "real_data"
2026-06-11T08:39:21.2376721Z         assert payload["is_demo"] is False
2026-06-11T08:39:21.2377360Z >       assert payload["input_pack_gate_status"] == "PASSED"
2026-06-11T08:39:21.2378025Z E       AssertionError: assert 'FAILED' == 'PASSED'
2026-06-11T08:39:21.2378520Z E         
2026-06-11T08:39:21.2378839Z E         - PASSED
2026-06-11T08:39:21.2379174Z E         + FAILED
2026-06-11T08:39:21.2379377Z 
2026-06-11T08:39:21.2379732Z tests/test_bt130_real_historical_evidence_pack_gate.py:108: AssertionError
2026-06-11T08:39:21.2380589Z ___________ test_bt130_real_data_runner_blocks_fully_rejected_plans ____________
2026-06-11T08:39:21.2381107Z 
2026-06-11T08:39:21.2381533Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-0/test_bt130_real_data_runner_bl1')
2026-06-11T08:39:21.2382365Z 
2026-06-11T08:39:21.2382802Z     def test_bt130_real_data_runner_blocks_fully_rejected_plans(tmp_path: Path) -> None:
2026-06-11T08:39:21.2383581Z         plans = tmp_path / "plans.json"
```

```text
2026-06-11T08:39:21.2377360Z >       assert payload["input_pack_gate_status"] == "PASSED"
2026-06-11T08:39:21.2378025Z E       AssertionError: assert 'FAILED' == 'PASSED'
2026-06-11T08:39:21.2378520Z E         
2026-06-11T08:39:21.2378839Z E         - PASSED
2026-06-11T08:39:21.2379174Z E         + FAILED
2026-06-11T08:39:21.2379377Z 
2026-06-11T08:39:21.2379732Z tests/test_bt130_real_historical_evidence_pack_gate.py:108: AssertionError
2026-06-11T08:39:21.2380589Z ___________ test_bt130_real_data_runner_blocks_fully_rejected_plans ____________
2026-06-11T08:39:21.2381107Z 
2026-06-11T08:39:21.2381533Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-0/test_bt130_real_data_runner_bl1')
2026-06-11T08:39:21.2382365Z 
2026-06-11T08:39:21.2382802Z     def test_bt130_real_data_runner_blocks_fully_rejected_plans(tmp_path: Path) -> None:
2026-06-11T08:39:21.2383581Z         plans = tmp_path / "plans.json"
2026-06-11T08:39:21.2384067Z         bars = tmp_path / "bars"
2026-06-11T08:39:21.2384541Z         universe = tmp_path / "universe.csv"
2026-06-11T08:39:21.2385062Z         coverage = tmp_path / "coverage.json"
```

```text
2026-06-11T08:39:21.2378520Z E         
2026-06-11T08:39:21.2378839Z E         - PASSED
2026-06-11T08:39:21.2379174Z E         + FAILED
2026-06-11T08:39:21.2379377Z 
2026-06-11T08:39:21.2379732Z tests/test_bt130_real_historical_evidence_pack_gate.py:108: AssertionError
2026-06-11T08:39:21.2380589Z ___________ test_bt130_real_data_runner_blocks_fully_rejected_plans ____________
2026-06-11T08:39:21.2381107Z 
2026-06-11T08:39:21.2381533Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-0/test_bt130_real_data_runner_bl1')
2026-06-11T08:39:21.2382365Z 
2026-06-11T08:39:21.2382802Z     def test_bt130_real_data_runner_blocks_fully_rejected_plans(tmp_path: Path) -> None:
2026-06-11T08:39:21.2383581Z         plans = tmp_path / "plans.json"
2026-06-11T08:39:21.2384067Z         bars = tmp_path / "bars"
2026-06-11T08:39:21.2384541Z         universe = tmp_path / "universe.csv"
2026-06-11T08:39:21.2385062Z         coverage = tmp_path / "coverage.json"
2026-06-11T08:39:21.2385577Z         out = tmp_path / "evidence.json"
2026-06-11T08:39:21.2386108Z         _write_plan(plans, unsupported_action=True)
```

```text
2026-06-11T08:39:21.2395255Z         )
2026-06-11T08:39:21.2395569Z     
2026-06-11T08:39:21.2395914Z         assert result.returncode == 1
2026-06-11T08:39:21.2396454Z >       assert "accepted_plan_count=0" in result.stdout
2026-06-11T08:39:21.2397941Z E       AssertionError: assert 'accepted_plan_count=0' in 'BT9 real historical input pack gate status: FAIL\n- coverage_manifest_symbol_0_not_object\n- coverage_manifest_missing_symbol:SPY\n'
2026-06-11T08:39:21.2401557Z E        +  where 'BT9 real historical input pack gate status: FAIL\n- coverage_manifest_symbol_0_not_object\n- coverage_manifest_missing_symbol:SPY\n' = CompletedProcess(args=['/opt/hostedtoolcache/Python/3.11.15/x64/bin/python', 'scripts/run_historical_entry_exit_backte... pack gate status: FAIL\n- coverage_manifest_symbol_0_not_object\n- coverage_manifest_missing_symbol:SPY\n', stderr='').stdout
2026-06-11T08:39:21.2404155Z 
2026-06-11T08:39:21.2404516Z tests/test_bt130_real_historical_evidence_pack_gate.py:142: AssertionError
2026-06-11T08:39:21.2405404Z _________________ test_bt9_input_pack_passes_with_valid_files __________________
2026-06-11T08:39:21.2405930Z 
2026-06-11T08:39:21.2406361Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-0/test_bt9_input_pack_passes_wit0')
2026-06-11T08:39:21.2406981Z 
2026-06-11T08:39:21.2407342Z     def test_bt9_input_pack_passes_with_valid_files(tmp_path: Path) -> None:
2026-06-11T08:39:21.2408053Z         universe = tmp_path / "universe.csv"
2026-06-11T08:39:21.2408568Z         bars = tmp_path / "bars"
2026-06-11T08:39:21.2409025Z         plans = tmp_path / "plans.json"
```

```text
2026-06-11T08:39:21.2396454Z >       assert "accepted_plan_count=0" in result.stdout
2026-06-11T08:39:21.2397941Z E       AssertionError: assert 'accepted_plan_count=0' in 'BT9 real historical input pack gate status: FAIL\n- coverage_manifest_symbol_0_not_object\n- coverage_manifest_missing_symbol:SPY\n'
2026-06-11T08:39:21.2401557Z E        +  where 'BT9 real historical input pack gate status: FAIL\n- coverage_manifest_symbol_0_not_object\n- coverage_manifest_missing_symbol:SPY\n' = CompletedProcess(args=['/opt/hostedtoolcache/Python/3.11.15/x64/bin/python', 'scripts/run_historical_entry_exit_backte... pack gate status: FAIL\n- coverage_manifest_symbol_0_not_object\n- coverage_manifest_missing_symbol:SPY\n', stderr='').stdout
2026-06-11T08:39:21.2404155Z 
2026-06-11T08:39:21.2404516Z tests/test_bt130_real_historical_evidence_pack_gate.py:142: AssertionError
2026-06-11T08:39:21.2405404Z _________________ test_bt9_input_pack_passes_with_valid_files __________________
2026-06-11T08:39:21.2405930Z 
2026-06-11T08:39:21.2406361Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-0/test_bt9_input_pack_passes_wit0')
2026-06-11T08:39:21.2406981Z 
2026-06-11T08:39:21.2407342Z     def test_bt9_input_pack_passes_with_valid_files(tmp_path: Path) -> None:
2026-06-11T08:39:21.2408053Z         universe = tmp_path / "universe.csv"
2026-06-11T08:39:21.2408568Z         bars = tmp_path / "bars"
2026-06-11T08:39:21.2409025Z         plans = tmp_path / "plans.json"
2026-06-11T08:39:21.2409542Z         _write_universe(universe)
2026-06-11T08:39:21.2410023Z         _write_bars(bars)
2026-06-11T08:39:21.2410457Z         _write_trade_plans(plans)
```

```text
2026-06-11T08:39:21.2410899Z     
2026-06-11T08:39:21.2411619Z         report = validate_bt9_input_pack(universe_path=universe, bars_root=bars, trade_plans_path=plans)
2026-06-11T08:39:21.2412784Z     
2026-06-11T08:39:21.2413214Z >       assert report.passed is True
2026-06-11T08:39:21.2413710Z E       AssertionError: assert False is True
2026-06-11T08:39:21.2415655Z E        +  where False = BT9RealHistoricalInputPackReport(passed=False, universe_path='/tmp/pytest-of-runner/pytest-0/test_bt9_input_pack_passe...2e768d3e61c37f54fed585974d3cdda614de'}, failures=['missing_coverage_manifest', 'coverage_manifest_missing_symbol:SPY']).passed
2026-06-11T08:39:21.2417403Z 
2026-06-11T08:39:21.2417735Z tests/test_bt9_real_historical_input_pack_gate.py:95: AssertionError
2026-06-11T08:39:21.2418612Z __ test_real_data_runner_blocks_trade_plans_not_generated_by_runtime_pipeline __
2026-06-11T08:39:21.2419180Z 
2026-06-11T08:39:21.2419611Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-0/test_real_data_runner_blocks_t0')
2026-06-11T08:39:21.2420256Z 
2026-06-11T08:39:21.2420807Z     def test_real_data_runner_blocks_trade_plans_not_generated_by_runtime_pipeline(tmp_path: Path) -> None:
2026-06-11T08:39:21.2421740Z         universe = tmp_path / "universe.csv"
2026-06-11T08:39:21.2422504Z         bars = tmp_path / "bars"
2026-06-11T08:39:21.2423205Z         plans = tmp_path / "plans.json"
```

```text
2026-06-11T08:39:21.2413214Z >       assert report.passed is True
2026-06-11T08:39:21.2413710Z E       AssertionError: assert False is True
2026-06-11T08:39:21.2415655Z E        +  where False = BT9RealHistoricalInputPackReport(passed=False, universe_path='/tmp/pytest-of-runner/pytest-0/test_bt9_input_pack_passe...2e768d3e61c37f54fed585974d3cdda614de'}, failures=['missing_coverage_manifest', 'coverage_manifest_missing_symbol:SPY']).passed
2026-06-11T08:39:21.2417403Z 
2026-06-11T08:39:21.2417735Z tests/test_bt9_real_historical_input_pack_gate.py:95: AssertionError
2026-06-11T08:39:21.2418612Z __ test_real_data_runner_blocks_trade_plans_not_generated_by_runtime_pipeline __
2026-06-11T08:39:21.2419180Z 
2026-06-11T08:39:21.2419611Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-0/test_real_data_runner_blocks_t0')
2026-06-11T08:39:21.2420256Z 
2026-06-11T08:39:21.2420807Z     def test_real_data_runner_blocks_trade_plans_not_generated_by_runtime_pipeline(tmp_path: Path) -> None:
2026-06-11T08:39:21.2421740Z         universe = tmp_path / "universe.csv"
2026-06-11T08:39:21.2422504Z         bars = tmp_path / "bars"
2026-06-11T08:39:21.2423205Z         plans = tmp_path / "plans.json"
2026-06-11T08:39:21.2423792Z         coverage_manifest = tmp_path / "coverage_manifest.json"
2026-06-11T08:39:21.2424481Z         json_output = tmp_path / "blocked-evidence.json"
2026-06-11T08:39:21.2425099Z         markdown_output = tmp_path / "blocked-evidence.md"
```

## CI

- Run ID: `27334660759`
- Branch: `main`
- Commit: `7ce082458246`
- Title: Document #184 historical input persistence and checksum requirements
- Created: 2026-06-11T08:38:31Z
- Updated: 2026-06-11T08:39:43Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27334660759

### Failed job: Pytest

- Job ID: `80755572862`
- Started: 2026-06-11T08:38:34Z
- Completed: 2026-06-11T08:39:42Z
- Failed steps: 53. Full regression suite residual tests

#### Error context

```text
2026-06-11T08:39:39.0885172Z ........................................................................ [ 88%]
2026-06-11T08:39:39.2969984Z ........................................................................ [ 93%]
2026-06-11T08:39:39.3399810Z ........................................................................ [ 98%]
2026-06-11T08:39:39.4071006Z ....................                                                     [100%]
2026-06-11T08:39:39.4071720Z =================================== FAILURES ===================================
2026-06-11T08:39:39.4072456Z _________ test_bt130_real_data_runner_blocks_missing_coverage_manifest _________
2026-06-11T08:39:39.4072962Z 
2026-06-11T08:39:39.4073369Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-33/test_bt130_real_data_runner_bl0')
2026-06-11T08:39:39.4073953Z 
2026-06-11T08:39:39.4074426Z     def test_bt130_real_data_runner_blocks_missing_coverage_manifest(tmp_path: Path) -> None:
2026-06-11T08:39:39.4075185Z         plans = tmp_path / "plans.json"
2026-06-11T08:39:39.4075643Z         bars = tmp_path / "bars"
2026-06-11T08:39:39.4076420Z         universe = tmp_path / "universe.csv"
2026-06-11T08:39:39.4076923Z         out = tmp_path / "evidence.json"
2026-06-11T08:39:39.4077390Z         _write_plan(plans)
2026-06-11T08:39:39.4077766Z         _write_bars(bars)
```

```text
2026-06-11T08:39:39.4087189Z         payload = json.loads(out.read_text(encoding="utf-8"))
2026-06-11T08:39:39.4087765Z         assert payload["data_source"] == "real_data"
2026-06-11T08:39:39.4088263Z         assert payload["is_demo"] is False
2026-06-11T08:39:39.4088982Z >       assert payload["input_pack_gate_status"] == "PASSED"
2026-06-11T08:39:39.4089566Z E       AssertionError: assert 'FAILED' == 'PASSED'
2026-06-11T08:39:39.4090029Z E         
2026-06-11T08:39:39.4090325Z E         - PASSED
2026-06-11T08:39:39.4090657Z E         + FAILED
2026-06-11T08:39:39.4090837Z 
2026-06-11T08:39:39.4091441Z tests/test_bt130_real_historical_evidence_pack_gate.py:108: AssertionError
2026-06-11T08:39:39.4092265Z ___________ test_bt130_real_data_runner_blocks_fully_rejected_plans ____________
2026-06-11T08:39:39.4092760Z 
2026-06-11T08:39:39.4093156Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-33/test_bt130_real_data_runner_bl1')
2026-06-11T08:39:39.4093727Z 
2026-06-11T08:39:39.4094117Z     def test_bt130_real_data_runner_blocks_fully_rejected_plans(tmp_path: Path) -> None:
2026-06-11T08:39:39.4094841Z         plans = tmp_path / "plans.json"
```

```text
2026-06-11T08:39:39.4088982Z >       assert payload["input_pack_gate_status"] == "PASSED"
2026-06-11T08:39:39.4089566Z E       AssertionError: assert 'FAILED' == 'PASSED'
2026-06-11T08:39:39.4090029Z E         
2026-06-11T08:39:39.4090325Z E         - PASSED
2026-06-11T08:39:39.4090657Z E         + FAILED
2026-06-11T08:39:39.4090837Z 
2026-06-11T08:39:39.4091441Z tests/test_bt130_real_historical_evidence_pack_gate.py:108: AssertionError
2026-06-11T08:39:39.4092265Z ___________ test_bt130_real_data_runner_blocks_fully_rejected_plans ____________
2026-06-11T08:39:39.4092760Z 
2026-06-11T08:39:39.4093156Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-33/test_bt130_real_data_runner_bl1')
2026-06-11T08:39:39.4093727Z 
2026-06-11T08:39:39.4094117Z     def test_bt130_real_data_runner_blocks_fully_rejected_plans(tmp_path: Path) -> None:
2026-06-11T08:39:39.4094841Z         plans = tmp_path / "plans.json"
2026-06-11T08:39:39.4095290Z         bars = tmp_path / "bars"
2026-06-11T08:39:39.4095726Z         universe = tmp_path / "universe.csv"
2026-06-11T08:39:39.4096218Z         coverage = tmp_path / "coverage.json"
```

```text
2026-06-11T08:39:39.4090029Z E         
2026-06-11T08:39:39.4090325Z E         - PASSED
2026-06-11T08:39:39.4090657Z E         + FAILED
2026-06-11T08:39:39.4090837Z 
2026-06-11T08:39:39.4091441Z tests/test_bt130_real_historical_evidence_pack_gate.py:108: AssertionError
2026-06-11T08:39:39.4092265Z ___________ test_bt130_real_data_runner_blocks_fully_rejected_plans ____________
2026-06-11T08:39:39.4092760Z 
2026-06-11T08:39:39.4093156Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-33/test_bt130_real_data_runner_bl1')
2026-06-11T08:39:39.4093727Z 
2026-06-11T08:39:39.4094117Z     def test_bt130_real_data_runner_blocks_fully_rejected_plans(tmp_path: Path) -> None:
2026-06-11T08:39:39.4094841Z         plans = tmp_path / "plans.json"
2026-06-11T08:39:39.4095290Z         bars = tmp_path / "bars"
2026-06-11T08:39:39.4095726Z         universe = tmp_path / "universe.csv"
2026-06-11T08:39:39.4096218Z         coverage = tmp_path / "coverage.json"
2026-06-11T08:39:39.4096691Z         out = tmp_path / "evidence.json"
2026-06-11T08:39:39.4097184Z         _write_plan(plans, unsupported_action=True)
```

```text
2026-06-11T08:39:39.4105241Z         )
2026-06-11T08:39:39.4105522Z     
2026-06-11T08:39:39.4105841Z         assert result.returncode == 1
2026-06-11T08:39:39.4106336Z >       assert "accepted_plan_count=0" in result.stdout
2026-06-11T08:39:39.4107658Z E       AssertionError: assert 'accepted_plan_count=0' in 'BT9 real historical input pack gate status: FAIL\n- coverage_manifest_symbol_0_not_object\n- coverage_manifest_missing_symbol:SPY\n'
2026-06-11T08:39:39.4111057Z E        +  where 'BT9 real historical input pack gate status: FAIL\n- coverage_manifest_symbol_0_not_object\n- coverage_manifest_missing_symbol:SPY\n' = CompletedProcess(args=['/opt/hostedtoolcache/Python/3.11.15/x64/bin/python', 'scripts/run_historical_entry_exit_backte... pack gate status: FAIL\n- coverage_manifest_symbol_0_not_object\n- coverage_manifest_missing_symbol:SPY\n', stderr='').stdout
2026-06-11T08:39:39.4113347Z 
2026-06-11T08:39:39.4113700Z tests/test_bt130_real_historical_evidence_pack_gate.py:142: AssertionError
2026-06-11T08:39:39.4114535Z _________________ test_bt9_input_pack_passes_with_valid_files __________________
2026-06-11T08:39:39.4115019Z 
2026-06-11T08:39:39.4115427Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-33/test_bt9_input_pack_passes_wit0')
2026-06-11T08:39:39.4115986Z 
2026-06-11T08:39:39.4116302Z     def test_bt9_input_pack_passes_with_valid_files(tmp_path: Path) -> None:
2026-06-11T08:39:39.4116966Z         universe = tmp_path / "universe.csv"
2026-06-11T08:39:39.4117422Z         bars = tmp_path / "bars"
2026-06-11T08:39:39.4117848Z         plans = tmp_path / "plans.json"
```

```text
2026-06-11T08:39:39.4106336Z >       assert "accepted_plan_count=0" in result.stdout
2026-06-11T08:39:39.4107658Z E       AssertionError: assert 'accepted_plan_count=0' in 'BT9 real historical input pack gate status: FAIL\n- coverage_manifest_symbol_0_not_object\n- coverage_manifest_missing_symbol:SPY\n'
2026-06-11T08:39:39.4111057Z E        +  where 'BT9 real historical input pack gate status: FAIL\n- coverage_manifest_symbol_0_not_object\n- coverage_manifest_missing_symbol:SPY\n' = CompletedProcess(args=['/opt/hostedtoolcache/Python/3.11.15/x64/bin/python', 'scripts/run_historical_entry_exit_backte... pack gate status: FAIL\n- coverage_manifest_symbol_0_not_object\n- coverage_manifest_missing_symbol:SPY\n', stderr='').stdout
2026-06-11T08:39:39.4113347Z 
2026-06-11T08:39:39.4113700Z tests/test_bt130_real_historical_evidence_pack_gate.py:142: AssertionError
2026-06-11T08:39:39.4114535Z _________________ test_bt9_input_pack_passes_with_valid_files __________________
2026-06-11T08:39:39.4115019Z 
2026-06-11T08:39:39.4115427Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-33/test_bt9_input_pack_passes_wit0')
2026-06-11T08:39:39.4115986Z 
2026-06-11T08:39:39.4116302Z     def test_bt9_input_pack_passes_with_valid_files(tmp_path: Path) -> None:
2026-06-11T08:39:39.4116966Z         universe = tmp_path / "universe.csv"
2026-06-11T08:39:39.4117422Z         bars = tmp_path / "bars"
2026-06-11T08:39:39.4117848Z         plans = tmp_path / "plans.json"
2026-06-11T08:39:39.4118292Z         _write_universe(universe)
2026-06-11T08:39:39.4118863Z         _write_bars(bars)
2026-06-11T08:39:39.4119253Z         _write_trade_plans(plans)
```

```text
2026-06-11T08:39:39.4119639Z     
2026-06-11T08:39:39.4120261Z         report = validate_bt9_input_pack(universe_path=universe, bars_root=bars, trade_plans_path=plans)
2026-06-11T08:39:39.4121009Z     
2026-06-11T08:39:39.4121335Z >       assert report.passed is True
2026-06-11T08:39:39.4121807Z E       AssertionError: assert False is True
2026-06-11T08:39:39.4123826Z E        +  where False = BT9RealHistoricalInputPackReport(passed=False, universe_path='/tmp/pytest-of-runner/pytest-33/test_bt9_input_pack_pass...2e768d3e61c37f54fed585974d3cdda614de'}, failures=['missing_coverage_manifest', 'coverage_manifest_missing_symbol:SPY']).passed
2026-06-11T08:39:39.4125486Z 
2026-06-11T08:39:39.4125785Z tests/test_bt9_real_historical_input_pack_gate.py:95: AssertionError
2026-06-11T08:39:39.4126587Z __ test_real_data_runner_blocks_trade_plans_not_generated_by_runtime_pipeline __
2026-06-11T08:39:39.4127111Z 
2026-06-11T08:39:39.4127513Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-33/test_real_data_runner_blocks_t0')
2026-06-11T08:39:39.4128053Z 
2026-06-11T08:39:39.4128573Z     def test_real_data_runner_blocks_trade_plans_not_generated_by_runtime_pipeline(tmp_path: Path) -> None:
2026-06-11T08:39:39.4129621Z         universe = tmp_path / "universe.csv"
2026-06-11T08:39:39.4130100Z         bars = tmp_path / "bars"
2026-06-11T08:39:39.4130525Z         plans = tmp_path / "plans.json"
```

```text
2026-06-11T08:39:39.4121335Z >       assert report.passed is True
2026-06-11T08:39:39.4121807Z E       AssertionError: assert False is True
2026-06-11T08:39:39.4123826Z E        +  where False = BT9RealHistoricalInputPackReport(passed=False, universe_path='/tmp/pytest-of-runner/pytest-33/test_bt9_input_pack_pass...2e768d3e61c37f54fed585974d3cdda614de'}, failures=['missing_coverage_manifest', 'coverage_manifest_missing_symbol:SPY']).passed
2026-06-11T08:39:39.4125486Z 
2026-06-11T08:39:39.4125785Z tests/test_bt9_real_historical_input_pack_gate.py:95: AssertionError
2026-06-11T08:39:39.4126587Z __ test_real_data_runner_blocks_trade_plans_not_generated_by_runtime_pipeline __
2026-06-11T08:39:39.4127111Z 
2026-06-11T08:39:39.4127513Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-33/test_real_data_runner_blocks_t0')
2026-06-11T08:39:39.4128053Z 
2026-06-11T08:39:39.4128573Z     def test_real_data_runner_blocks_trade_plans_not_generated_by_runtime_pipeline(tmp_path: Path) -> None:
2026-06-11T08:39:39.4129621Z         universe = tmp_path / "universe.csv"
2026-06-11T08:39:39.4130100Z         bars = tmp_path / "bars"
2026-06-11T08:39:39.4130525Z         plans = tmp_path / "plans.json"
2026-06-11T08:39:39.4131061Z         coverage_manifest = tmp_path / "coverage_manifest.json"
2026-06-11T08:39:39.4131689Z         json_output = tmp_path / "blocked-evidence.json"
2026-06-11T08:39:39.4132268Z         markdown_output = tmp_path / "blocked-evidence.md"
```

## Report Quality Validation

- Run ID: `27334660698`
- Branch: `main`
- Commit: `7ce082458246`
- Title: Document #184 historical input persistence and checksum requirements
- Created: 2026-06-11T08:38:31Z
- Updated: 2026-06-11T08:39:57Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27334660698

### Failed job: validate-reports (postmarket)

- Job ID: `80755610248`
- Started: 2026-06-11T08:38:47Z
- Completed: 2026-06-11T08:39:54Z
- Failed steps: 6. Validate report quality

#### Error context

```text
2026-06-11T08:39:42.1593489Z - Report used fallback data; content is structurally valid but not analytically strong
2026-06-11T08:39:42.1594089Z 
2026-06-11T08:39:42.1594221Z Errors:
2026-06-11T08:39:42.1594563Z - Missing analytical term: Risk Tier
2026-06-11T08:39:42.1664886Z ##[error]Process completed with exit code 1.
2026-06-11T08:39:42.1746850Z ##[group]Run actions/upload-artifact@v4
2026-06-11T08:39:42.1747388Z with:
2026-06-11T08:39:42.1747623Z   name: validated-postmarket-report
2026-06-11T08:39:42.1747962Z   path: reports/generated/postmarket-report.md
2026-06-11T08:39:42.1748279Z   retention-days: 14
2026-06-11T08:39:42.1748518Z   if-no-files-found: warn
2026-06-11T08:39:42.1748777Z   compression-level: 6
2026-06-11T08:39:42.1749011Z   overwrite: false
2026-06-11T08:39:42.1749259Z   include-hidden-files: false
2026-06-11T08:39:42.1749510Z env:
2026-06-11T08:39:42.1749838Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (premarket)

- Job ID: `80755610286`
- Started: 2026-06-11T08:38:47Z
- Completed: 2026-06-11T08:39:56Z
- Failed steps: 6. Validate report quality

#### Error context

```text
2026-06-11T08:39:54.1955339Z - Report used fallback data; content is structurally valid but not analytically strong
2026-06-11T08:39:54.1955955Z 
2026-06-11T08:39:54.1956081Z Errors:
2026-06-11T08:39:54.1956412Z - Missing analytical term: Risk Tier
2026-06-11T08:39:54.2035515Z ##[error]Process completed with exit code 1.
2026-06-11T08:39:54.2118585Z ##[group]Run actions/upload-artifact@v4
2026-06-11T08:39:54.2118897Z with:
2026-06-11T08:39:54.2119137Z   name: validated-premarket-report
2026-06-11T08:39:54.2119766Z   path: reports/generated/premarket-report.md
2026-06-11T08:39:54.2120275Z   retention-days: 14
2026-06-11T08:39:54.2120547Z   if-no-files-found: warn
2026-06-11T08:39:54.2120822Z   compression-level: 6
2026-06-11T08:39:54.2121058Z   overwrite: false
2026-06-11T08:39:54.2121295Z   include-hidden-files: false
2026-06-11T08:39:54.2121549Z env:
2026-06-11T08:39:54.2121919Z   POLYGON_API_KEY: ***
```

## CI

- Run ID: `27334604467`
- Branch: `main`
- Commit: `5ba2d0f749f0`
- Title: Align BT131 real-data text guard with evidence validator output
- Created: 2026-06-11T08:37:32Z
- Updated: 2026-06-11T08:38:42Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27334604467

### Failed job: Pytest

- Job ID: `80755380382`
- Started: 2026-06-11T08:37:34Z
- Completed: 2026-06-11T08:38:41Z
- Failed steps: 53. Full regression suite residual tests

#### Error context

```text
2026-06-11T08:38:38.0868353Z ........................................................................ [ 88%]
2026-06-11T08:38:38.3053860Z ........................................................................ [ 93%]
2026-06-11T08:38:38.3550390Z ........................................................................ [ 98%]
2026-06-11T08:38:38.4257681Z ....................                                                     [100%]
2026-06-11T08:38:38.4258453Z =================================== FAILURES ===================================
2026-06-11T08:38:38.4259213Z _________ test_bt130_real_data_runner_blocks_missing_coverage_manifest _________
2026-06-11T08:38:38.4259711Z 
2026-06-11T08:38:38.4260110Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-33/test_bt130_real_data_runner_bl0')
2026-06-11T08:38:38.4260680Z 
2026-06-11T08:38:38.4261116Z     def test_bt130_real_data_runner_blocks_missing_coverage_manifest(tmp_path: Path) -> None:
2026-06-11T08:38:38.4261871Z         plans = tmp_path / "plans.json"
2026-06-11T08:38:38.4262231Z         bars = tmp_path / "bars"
2026-06-11T08:38:38.4262840Z         universe = tmp_path / "universe.csv"
2026-06-11T08:38:38.4263202Z         out = tmp_path / "evidence.json"
2026-06-11T08:38:38.4263547Z         _write_plan(plans)
2026-06-11T08:38:38.4263860Z         _write_bars(bars)
```

```text
2026-06-11T08:38:38.4271016Z         payload = json.loads(out.read_text(encoding="utf-8"))
2026-06-11T08:38:38.4271444Z         assert payload["data_source"] == "real_data"
2026-06-11T08:38:38.4271817Z         assert payload["is_demo"] is False
2026-06-11T08:38:38.4272221Z >       assert payload["input_pack_gate_status"] == "PASSED"
2026-06-11T08:38:38.4272647Z E       AssertionError: assert 'FAILED' == 'PASSED'
2026-06-11T08:38:38.4272945Z E         
2026-06-11T08:38:38.4273141Z E         - PASSED
2026-06-11T08:38:38.4273352Z E         + FAILED
2026-06-11T08:38:38.4273476Z 
2026-06-11T08:38:38.4273853Z tests/test_bt130_real_historical_evidence_pack_gate.py:108: AssertionError
2026-06-11T08:38:38.4274387Z ___________ test_bt130_real_data_runner_blocks_fully_rejected_plans ____________
2026-06-11T08:38:38.4274692Z 
2026-06-11T08:38:38.4275166Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-33/test_bt130_real_data_runner_bl1')
2026-06-11T08:38:38.4275525Z 
2026-06-11T08:38:38.4275771Z     def test_bt130_real_data_runner_blocks_fully_rejected_plans(tmp_path: Path) -> None:
2026-06-11T08:38:38.4276219Z         plans = tmp_path / "plans.json"
```

```text
2026-06-11T08:38:38.4272221Z >       assert payload["input_pack_gate_status"] == "PASSED"
2026-06-11T08:38:38.4272647Z E       AssertionError: assert 'FAILED' == 'PASSED'
2026-06-11T08:38:38.4272945Z E         
2026-06-11T08:38:38.4273141Z E         - PASSED
2026-06-11T08:38:38.4273352Z E         + FAILED
2026-06-11T08:38:38.4273476Z 
2026-06-11T08:38:38.4273853Z tests/test_bt130_real_historical_evidence_pack_gate.py:108: AssertionError
2026-06-11T08:38:38.4274387Z ___________ test_bt130_real_data_runner_blocks_fully_rejected_plans ____________
2026-06-11T08:38:38.4274692Z 
2026-06-11T08:38:38.4275166Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-33/test_bt130_real_data_runner_bl1')
2026-06-11T08:38:38.4275525Z 
2026-06-11T08:38:38.4275771Z     def test_bt130_real_data_runner_blocks_fully_rejected_plans(tmp_path: Path) -> None:
2026-06-11T08:38:38.4276219Z         plans = tmp_path / "plans.json"
2026-06-11T08:38:38.4276503Z         bars = tmp_path / "bars"
2026-06-11T08:38:38.4276770Z         universe = tmp_path / "universe.csv"
2026-06-11T08:38:38.4277075Z         coverage = tmp_path / "coverage.json"
```

```text
2026-06-11T08:38:38.4272945Z E         
2026-06-11T08:38:38.4273141Z E         - PASSED
2026-06-11T08:38:38.4273352Z E         + FAILED
2026-06-11T08:38:38.4273476Z 
2026-06-11T08:38:38.4273853Z tests/test_bt130_real_historical_evidence_pack_gate.py:108: AssertionError
2026-06-11T08:38:38.4274387Z ___________ test_bt130_real_data_runner_blocks_fully_rejected_plans ____________
2026-06-11T08:38:38.4274692Z 
2026-06-11T08:38:38.4275166Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-33/test_bt130_real_data_runner_bl1')
2026-06-11T08:38:38.4275525Z 
2026-06-11T08:38:38.4275771Z     def test_bt130_real_data_runner_blocks_fully_rejected_plans(tmp_path: Path) -> None:
2026-06-11T08:38:38.4276219Z         plans = tmp_path / "plans.json"
2026-06-11T08:38:38.4276503Z         bars = tmp_path / "bars"
2026-06-11T08:38:38.4276770Z         universe = tmp_path / "universe.csv"
2026-06-11T08:38:38.4277075Z         coverage = tmp_path / "coverage.json"
2026-06-11T08:38:38.4277366Z         out = tmp_path / "evidence.json"
2026-06-11T08:38:38.4277666Z         _write_plan(plans, unsupported_action=True)
```

```text
2026-06-11T08:38:38.4283735Z         )
2026-06-11T08:38:38.4284090Z     
2026-06-11T08:38:38.4284391Z         assert result.returncode == 1
2026-06-11T08:38:38.4284728Z >       assert "accepted_plan_count=0" in result.stdout
2026-06-11T08:38:38.4285756Z E       AssertionError: assert 'accepted_plan_count=0' in 'BT9 real historical input pack gate status: FAIL\n- coverage_manifest_symbol_0_not_object\n- coverage_manifest_missing_symbol:SPY\n'
2026-06-11T08:38:38.4287792Z E        +  where 'BT9 real historical input pack gate status: FAIL\n- coverage_manifest_symbol_0_not_object\n- coverage_manifest_missing_symbol:SPY\n' = CompletedProcess(args=['/opt/hostedtoolcache/Python/3.11.15/x64/bin/python', 'scripts/run_historical_entry_exit_backte... pack gate status: FAIL\n- coverage_manifest_symbol_0_not_object\n- coverage_manifest_missing_symbol:SPY\n', stderr='').stdout
2026-06-11T08:38:38.4289159Z 
2026-06-11T08:38:38.4289370Z tests/test_bt130_real_historical_evidence_pack_gate.py:142: AssertionError
2026-06-11T08:38:38.4289873Z _________________ test_bt9_input_pack_passes_with_valid_files __________________
2026-06-11T08:38:38.4290169Z 
2026-06-11T08:38:38.4290418Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-33/test_bt9_input_pack_passes_wit0')
2026-06-11T08:38:38.4290769Z 
2026-06-11T08:38:38.4290970Z     def test_bt9_input_pack_passes_with_valid_files(tmp_path: Path) -> None:
2026-06-11T08:38:38.4291383Z         universe = tmp_path / "universe.csv"
2026-06-11T08:38:38.4291669Z         bars = tmp_path / "bars"
2026-06-11T08:38:38.4291934Z         plans = tmp_path / "plans.json"
```

```text
2026-06-11T08:38:38.4284728Z >       assert "accepted_plan_count=0" in result.stdout
2026-06-11T08:38:38.4285756Z E       AssertionError: assert 'accepted_plan_count=0' in 'BT9 real historical input pack gate status: FAIL\n- coverage_manifest_symbol_0_not_object\n- coverage_manifest_missing_symbol:SPY\n'
2026-06-11T08:38:38.4287792Z E        +  where 'BT9 real historical input pack gate status: FAIL\n- coverage_manifest_symbol_0_not_object\n- coverage_manifest_missing_symbol:SPY\n' = CompletedProcess(args=['/opt/hostedtoolcache/Python/3.11.15/x64/bin/python', 'scripts/run_historical_entry_exit_backte... pack gate status: FAIL\n- coverage_manifest_symbol_0_not_object\n- coverage_manifest_missing_symbol:SPY\n', stderr='').stdout
2026-06-11T08:38:38.4289159Z 
2026-06-11T08:38:38.4289370Z tests/test_bt130_real_historical_evidence_pack_gate.py:142: AssertionError
2026-06-11T08:38:38.4289873Z _________________ test_bt9_input_pack_passes_with_valid_files __________________
2026-06-11T08:38:38.4290169Z 
2026-06-11T08:38:38.4290418Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-33/test_bt9_input_pack_passes_wit0')
2026-06-11T08:38:38.4290769Z 
2026-06-11T08:38:38.4290970Z     def test_bt9_input_pack_passes_with_valid_files(tmp_path: Path) -> None:
2026-06-11T08:38:38.4291383Z         universe = tmp_path / "universe.csv"
2026-06-11T08:38:38.4291669Z         bars = tmp_path / "bars"
2026-06-11T08:38:38.4291934Z         plans = tmp_path / "plans.json"
2026-06-11T08:38:38.4292209Z         _write_universe(universe)
2026-06-11T08:38:38.4292464Z         _write_bars(bars)
2026-06-11T08:38:38.4292701Z         _write_trade_plans(plans)
```

```text
2026-06-11T08:38:38.4292939Z     
2026-06-11T08:38:38.4293327Z         report = validate_bt9_input_pack(universe_path=universe, bars_root=bars, trade_plans_path=plans)
2026-06-11T08:38:38.4293791Z     
2026-06-11T08:38:38.4293996Z >       assert report.passed is True
2026-06-11T08:38:38.4294285Z E       AssertionError: assert False is True
2026-06-11T08:38:38.4295672Z E        +  where False = BT9RealHistoricalInputPackReport(passed=False, universe_path='/tmp/pytest-of-runner/pytest-33/test_bt9_input_pack_pass...2e768d3e61c37f54fed585974d3cdda614de'}, failures=['missing_coverage_manifest', 'coverage_manifest_missing_symbol:SPY']).passed
2026-06-11T08:38:38.4296693Z 
2026-06-11T08:38:38.4296893Z tests/test_bt9_real_historical_input_pack_gate.py:95: AssertionError
2026-06-11T08:38:38.4297399Z __ test_real_data_runner_blocks_trade_plans_not_generated_by_runtime_pipeline __
2026-06-11T08:38:38.4297715Z 
2026-06-11T08:38:38.4297967Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-33/test_real_data_runner_blocks_t0')
2026-06-11T08:38:38.4298309Z 
2026-06-11T08:38:38.4298623Z     def test_real_data_runner_blocks_trade_plans_not_generated_by_runtime_pipeline(tmp_path: Path) -> None:
2026-06-11T08:38:38.4299136Z         universe = tmp_path / "universe.csv"
2026-06-11T08:38:38.4299437Z         bars = tmp_path / "bars"
2026-06-11T08:38:38.4299707Z         plans = tmp_path / "plans.json"
```

```text
2026-06-11T08:38:38.4293996Z >       assert report.passed is True
2026-06-11T08:38:38.4294285Z E       AssertionError: assert False is True
2026-06-11T08:38:38.4295672Z E        +  where False = BT9RealHistoricalInputPackReport(passed=False, universe_path='/tmp/pytest-of-runner/pytest-33/test_bt9_input_pack_pass...2e768d3e61c37f54fed585974d3cdda614de'}, failures=['missing_coverage_manifest', 'coverage_manifest_missing_symbol:SPY']).passed
2026-06-11T08:38:38.4296693Z 
2026-06-11T08:38:38.4296893Z tests/test_bt9_real_historical_input_pack_gate.py:95: AssertionError
2026-06-11T08:38:38.4297399Z __ test_real_data_runner_blocks_trade_plans_not_generated_by_runtime_pipeline __
2026-06-11T08:38:38.4297715Z 
2026-06-11T08:38:38.4297967Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-33/test_real_data_runner_blocks_t0')
2026-06-11T08:38:38.4298309Z 
2026-06-11T08:38:38.4298623Z     def test_real_data_runner_blocks_trade_plans_not_generated_by_runtime_pipeline(tmp_path: Path) -> None:
2026-06-11T08:38:38.4299136Z         universe = tmp_path / "universe.csv"
2026-06-11T08:38:38.4299437Z         bars = tmp_path / "bars"
2026-06-11T08:38:38.4299707Z         plans = tmp_path / "plans.json"
2026-06-11T08:38:38.4300046Z         coverage_manifest = tmp_path / "coverage_manifest.json"
2026-06-11T08:38:38.4300440Z         json_output = tmp_path / "blocked-evidence.json"
2026-06-11T08:38:38.4300805Z         markdown_output = tmp_path / "blocked-evidence.md"
```

## Decision Engine Tests

- Run ID: `27334604550`
- Branch: `main`
- Commit: `5ba2d0f749f0`
- Title: Align BT131 real-data text guard with evidence validator output
- Created: 2026-06-11T08:37:32Z
- Updated: 2026-06-11T08:38:22Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27334604550

### Failed job: tests

- Job ID: `80755380965`
- Started: 2026-06-11T08:37:34Z
- Completed: 2026-06-11T08:38:21Z
- Failed steps: 5. Run pytest

#### Error context

```text
2026-06-11T08:38:19.5236606Z ........................................................................ [ 90%]
2026-06-11T08:38:19.7442962Z ........................................................................ [ 94%]
2026-06-11T08:38:19.7927380Z ........................................................................ [ 97%]
2026-06-11T08:38:19.8862194Z .........................................                                [100%]
2026-06-11T08:38:19.8863360Z =================================== FAILURES ===================================
2026-06-11T08:38:19.8864251Z _________ test_bt130_real_data_runner_blocks_missing_coverage_manifest _________
2026-06-11T08:38:19.8864803Z 
2026-06-11T08:38:19.8865248Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-0/test_bt130_real_data_runner_bl0')
2026-06-11T08:38:19.8866183Z 
2026-06-11T08:38:19.8866923Z     def test_bt130_real_data_runner_blocks_missing_coverage_manifest(tmp_path: Path) -> None:
2026-06-11T08:38:19.8867743Z         plans = tmp_path / "plans.json"
2026-06-11T08:38:19.8868221Z         bars = tmp_path / "bars"
2026-06-11T08:38:19.8868677Z         universe = tmp_path / "universe.csv"
2026-06-11T08:38:19.8869174Z         out = tmp_path / "evidence.json"
2026-06-11T08:38:19.8869908Z         _write_plan(plans)
2026-06-11T08:38:19.8870318Z         _write_bars(bars)
```

```text
2026-06-11T08:38:19.8878529Z         payload = json.loads(out.read_text(encoding="utf-8"))
2026-06-11T08:38:19.8878888Z         assert payload["data_source"] == "real_data"
2026-06-11T08:38:19.8879205Z         assert payload["is_demo"] is False
2026-06-11T08:38:19.8879772Z >       assert payload["input_pack_gate_status"] == "PASSED"
2026-06-11T08:38:19.8880165Z E       AssertionError: assert 'FAILED' == 'PASSED'
2026-06-11T08:38:19.8880460Z E         
2026-06-11T08:38:19.8880673Z E         - PASSED
2026-06-11T08:38:19.8880888Z E         + FAILED
2026-06-11T08:38:19.8881048Z 
2026-06-11T08:38:19.8881264Z tests/test_bt130_real_historical_evidence_pack_gate.py:108: AssertionError
2026-06-11T08:38:19.8881776Z ___________ test_bt130_real_data_runner_blocks_fully_rejected_plans ____________
2026-06-11T08:38:19.8882081Z 
2026-06-11T08:38:19.8882323Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-0/test_bt130_real_data_runner_bl1')
2026-06-11T08:38:19.8882671Z 
2026-06-11T08:38:19.8882911Z     def test_bt130_real_data_runner_blocks_fully_rejected_plans(tmp_path: Path) -> None:
2026-06-11T08:38:19.8883348Z         plans = tmp_path / "plans.json"
```

```text
2026-06-11T08:38:19.8879772Z >       assert payload["input_pack_gate_status"] == "PASSED"
2026-06-11T08:38:19.8880165Z E       AssertionError: assert 'FAILED' == 'PASSED'
2026-06-11T08:38:19.8880460Z E         
2026-06-11T08:38:19.8880673Z E         - PASSED
2026-06-11T08:38:19.8880888Z E         + FAILED
2026-06-11T08:38:19.8881048Z 
2026-06-11T08:38:19.8881264Z tests/test_bt130_real_historical_evidence_pack_gate.py:108: AssertionError
2026-06-11T08:38:19.8881776Z ___________ test_bt130_real_data_runner_blocks_fully_rejected_plans ____________
2026-06-11T08:38:19.8882081Z 
2026-06-11T08:38:19.8882323Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-0/test_bt130_real_data_runner_bl1')
2026-06-11T08:38:19.8882671Z 
2026-06-11T08:38:19.8882911Z     def test_bt130_real_data_runner_blocks_fully_rejected_plans(tmp_path: Path) -> None:
2026-06-11T08:38:19.8883348Z         plans = tmp_path / "plans.json"
2026-06-11T08:38:19.8883629Z         bars = tmp_path / "bars"
2026-06-11T08:38:19.8883916Z         universe = tmp_path / "universe.csv"
2026-06-11T08:38:19.8884228Z         coverage = tmp_path / "coverage.json"
```

```text
2026-06-11T08:38:19.8880460Z E         
2026-06-11T08:38:19.8880673Z E         - PASSED
2026-06-11T08:38:19.8880888Z E         + FAILED
2026-06-11T08:38:19.8881048Z 
2026-06-11T08:38:19.8881264Z tests/test_bt130_real_historical_evidence_pack_gate.py:108: AssertionError
2026-06-11T08:38:19.8881776Z ___________ test_bt130_real_data_runner_blocks_fully_rejected_plans ____________
2026-06-11T08:38:19.8882081Z 
2026-06-11T08:38:19.8882323Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-0/test_bt130_real_data_runner_bl1')
2026-06-11T08:38:19.8882671Z 
2026-06-11T08:38:19.8882911Z     def test_bt130_real_data_runner_blocks_fully_rejected_plans(tmp_path: Path) -> None:
2026-06-11T08:38:19.8883348Z         plans = tmp_path / "plans.json"
2026-06-11T08:38:19.8883629Z         bars = tmp_path / "bars"
2026-06-11T08:38:19.8883916Z         universe = tmp_path / "universe.csv"
2026-06-11T08:38:19.8884228Z         coverage = tmp_path / "coverage.json"
2026-06-11T08:38:19.8884519Z         out = tmp_path / "evidence.json"
2026-06-11T08:38:19.8884818Z         _write_plan(plans, unsupported_action=True)
```

```text
2026-06-11T08:38:19.8890189Z         )
2026-06-11T08:38:19.8890367Z     
2026-06-11T08:38:19.8890570Z         assert result.returncode == 1
2026-06-11T08:38:19.8890886Z >       assert "accepted_plan_count=0" in result.stdout
2026-06-11T08:38:19.8891699Z E       AssertionError: assert 'accepted_plan_count=0' in 'BT9 real historical input pack gate status: FAIL\n- coverage_manifest_symbol_0_not_object\n- coverage_manifest_missing_symbol:SPY\n'
2026-06-11T08:38:19.8893624Z E        +  where 'BT9 real historical input pack gate status: FAIL\n- coverage_manifest_symbol_0_not_object\n- coverage_manifest_missing_symbol:SPY\n' = CompletedProcess(args=['/opt/hostedtoolcache/Python/3.11.15/x64/bin/python', 'scripts/run_historical_entry_exit_backte... pack gate status: FAIL\n- coverage_manifest_symbol_0_not_object\n- coverage_manifest_missing_symbol:SPY\n', stderr='').stdout
2026-06-11T08:38:19.8895793Z 
2026-06-11T08:38:19.8896151Z tests/test_bt130_real_historical_evidence_pack_gate.py:142: AssertionError
2026-06-11T08:38:19.8897005Z _________________ test_bt9_input_pack_passes_with_valid_files __________________
2026-06-11T08:38:19.8897516Z 
2026-06-11T08:38:19.8897928Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-0/test_bt9_input_pack_passes_wit0')
2026-06-11T08:38:19.8898523Z 
2026-06-11T08:38:19.8898835Z     def test_bt9_input_pack_passes_with_valid_files(tmp_path: Path) -> None:
2026-06-11T08:38:19.8899250Z         universe = tmp_path / "universe.csv"
2026-06-11T08:38:19.8899756Z         bars = tmp_path / "bars"
2026-06-11T08:38:19.8900061Z         plans = tmp_path / "plans.json"
```

```text
2026-06-11T08:38:19.8890886Z >       assert "accepted_plan_count=0" in result.stdout
2026-06-11T08:38:19.8891699Z E       AssertionError: assert 'accepted_plan_count=0' in 'BT9 real historical input pack gate status: FAIL\n- coverage_manifest_symbol_0_not_object\n- coverage_manifest_missing_symbol:SPY\n'
2026-06-11T08:38:19.8893624Z E        +  where 'BT9 real historical input pack gate status: FAIL\n- coverage_manifest_symbol_0_not_object\n- coverage_manifest_missing_symbol:SPY\n' = CompletedProcess(args=['/opt/hostedtoolcache/Python/3.11.15/x64/bin/python', 'scripts/run_historical_entry_exit_backte... pack gate status: FAIL\n- coverage_manifest_symbol_0_not_object\n- coverage_manifest_missing_symbol:SPY\n', stderr='').stdout
2026-06-11T08:38:19.8895793Z 
2026-06-11T08:38:19.8896151Z tests/test_bt130_real_historical_evidence_pack_gate.py:142: AssertionError
2026-06-11T08:38:19.8897005Z _________________ test_bt9_input_pack_passes_with_valid_files __________________
2026-06-11T08:38:19.8897516Z 
2026-06-11T08:38:19.8897928Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-0/test_bt9_input_pack_passes_wit0')
2026-06-11T08:38:19.8898523Z 
2026-06-11T08:38:19.8898835Z     def test_bt9_input_pack_passes_with_valid_files(tmp_path: Path) -> None:
2026-06-11T08:38:19.8899250Z         universe = tmp_path / "universe.csv"
2026-06-11T08:38:19.8899756Z         bars = tmp_path / "bars"
2026-06-11T08:38:19.8900061Z         plans = tmp_path / "plans.json"
2026-06-11T08:38:19.8900356Z         _write_universe(universe)
2026-06-11T08:38:19.8900646Z         _write_bars(bars)
2026-06-11T08:38:19.8900888Z         _write_trade_plans(plans)
```

```text
2026-06-11T08:38:19.8901131Z     
2026-06-11T08:38:19.8901538Z         report = validate_bt9_input_pack(universe_path=universe, bars_root=bars, trade_plans_path=plans)
2026-06-11T08:38:19.8901996Z     
2026-06-11T08:38:19.8902192Z >       assert report.passed is True
2026-06-11T08:38:19.8902474Z E       AssertionError: assert False is True
2026-06-11T08:38:19.8903591Z E        +  where False = BT9RealHistoricalInputPackReport(passed=False, universe_path='/tmp/pytest-of-runner/pytest-0/test_bt9_input_pack_passe...2e768d3e61c37f54fed585974d3cdda614de'}, failures=['missing_coverage_manifest', 'coverage_manifest_missing_symbol:SPY']).passed
2026-06-11T08:38:19.8904580Z 
2026-06-11T08:38:19.8904770Z tests/test_bt9_real_historical_input_pack_gate.py:95: AssertionError
2026-06-11T08:38:19.8905266Z __ test_real_data_runner_blocks_trade_plans_not_generated_by_runtime_pipeline __
2026-06-11T08:38:19.8905581Z 
2026-06-11T08:38:19.8905832Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-0/test_real_data_runner_blocks_t0')
2026-06-11T08:38:19.8906179Z 
2026-06-11T08:38:19.8906486Z     def test_real_data_runner_blocks_trade_plans_not_generated_by_runtime_pipeline(tmp_path: Path) -> None:
2026-06-11T08:38:19.8906998Z         universe = tmp_path / "universe.csv"
2026-06-11T08:38:19.8907286Z         bars = tmp_path / "bars"
2026-06-11T08:38:19.8907546Z         plans = tmp_path / "plans.json"
```

```text
2026-06-11T08:38:19.8902192Z >       assert report.passed is True
2026-06-11T08:38:19.8902474Z E       AssertionError: assert False is True
2026-06-11T08:38:19.8903591Z E        +  where False = BT9RealHistoricalInputPackReport(passed=False, universe_path='/tmp/pytest-of-runner/pytest-0/test_bt9_input_pack_passe...2e768d3e61c37f54fed585974d3cdda614de'}, failures=['missing_coverage_manifest', 'coverage_manifest_missing_symbol:SPY']).passed
2026-06-11T08:38:19.8904580Z 
2026-06-11T08:38:19.8904770Z tests/test_bt9_real_historical_input_pack_gate.py:95: AssertionError
2026-06-11T08:38:19.8905266Z __ test_real_data_runner_blocks_trade_plans_not_generated_by_runtime_pipeline __
2026-06-11T08:38:19.8905581Z 
2026-06-11T08:38:19.8905832Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-0/test_real_data_runner_blocks_t0')
2026-06-11T08:38:19.8906179Z 
2026-06-11T08:38:19.8906486Z     def test_real_data_runner_blocks_trade_plans_not_generated_by_runtime_pipeline(tmp_path: Path) -> None:
2026-06-11T08:38:19.8906998Z         universe = tmp_path / "universe.csv"
2026-06-11T08:38:19.8907286Z         bars = tmp_path / "bars"
2026-06-11T08:38:19.8907546Z         plans = tmp_path / "plans.json"
2026-06-11T08:38:19.8907879Z         coverage_manifest = tmp_path / "coverage_manifest.json"
2026-06-11T08:38:19.8908267Z         json_output = tmp_path / "blocked-evidence.json"
2026-06-11T08:38:19.8908639Z         markdown_output = tmp_path / "blocked-evidence.md"
```

## Report Quality Validation

- Run ID: `27334603752`
- Branch: `main`
- Commit: `5ba2d0f749f0`
- Title: Align BT131 real-data text guard with evidence validator output
- Created: 2026-06-11T08:37:31Z
- Updated: 2026-06-11T08:38:45Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27334603752

### Failed job: validate-reports (premarket)

- Job ID: `80755379007`
- Started: 2026-06-11T08:37:34Z
- Completed: 2026-06-11T08:38:44Z
- Failed steps: 6. Validate report quality

#### Error context

```text
2026-06-11T08:38:40.5849882Z - Report used fallback data; content is structurally valid but not analytically strong
2026-06-11T08:38:40.5850618Z 
2026-06-11T08:38:40.5850767Z Errors:
2026-06-11T08:38:40.5851136Z - Missing analytical term: Risk Tier
2026-06-11T08:38:40.5925013Z ##[error]Process completed with exit code 1.
2026-06-11T08:38:40.6005666Z ##[group]Run actions/upload-artifact@v4
2026-06-11T08:38:40.6005965Z with:
2026-06-11T08:38:40.6006175Z   name: validated-premarket-report
2026-06-11T08:38:40.6006773Z   path: reports/generated/premarket-report.md
2026-06-11T08:38:40.6007174Z   retention-days: 14
2026-06-11T08:38:40.6007394Z   if-no-files-found: warn
2026-06-11T08:38:40.6007632Z   compression-level: 6
2026-06-11T08:38:40.6007844Z   overwrite: false
2026-06-11T08:38:40.6008059Z   include-hidden-files: false
2026-06-11T08:38:40.6008286Z env:
2026-06-11T08:38:40.6008616Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (postmarket)

- Job ID: `80755379111`
- Started: 2026-06-11T08:37:34Z
- Completed: 2026-06-11T08:38:33Z
- Failed steps: 6. Validate report quality

#### Error context

```text
2026-06-11T08:38:31.6732834Z - Report used fallback data; content is structurally valid but not analytically strong
2026-06-11T08:38:31.6733251Z 
2026-06-11T08:38:31.6733335Z Errors:
2026-06-11T08:38:31.6733552Z - Missing analytical term: Risk Tier
2026-06-11T08:38:31.6799153Z ##[error]Process completed with exit code 1.
2026-06-11T08:38:31.6879084Z ##[group]Run actions/upload-artifact@v4
2026-06-11T08:38:31.6879385Z with:
2026-06-11T08:38:31.6879601Z   name: validated-postmarket-report
2026-06-11T08:38:31.6879914Z   path: reports/generated/postmarket-report.md
2026-06-11T08:38:31.6880214Z   retention-days: 14
2026-06-11T08:38:31.6880433Z   if-no-files-found: warn
2026-06-11T08:38:31.6880666Z   compression-level: 6
2026-06-11T08:38:31.6880879Z   overwrite: false
2026-06-11T08:38:31.6881103Z   include-hidden-files: false
2026-06-11T08:38:31.6881345Z env:
2026-06-11T08:38:31.6881672Z   POLYGON_API_KEY: ***
```

## Decision Engine Tests

- Run ID: `27333839154`
- Branch: `main`
- Commit: `fab3a1d54a79`
- Title: Add #184 historical input persistence guard tests
- Created: 2026-06-11T08:22:52Z
- Updated: 2026-06-11T08:23:39Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27333839154

### Failed job: tests

- Job ID: `80752738863`
- Started: 2026-06-11T08:22:55Z
- Completed: 2026-06-11T08:23:38Z
- Failed steps: 5. Run pytest

#### Error context

```text
2026-06-11T08:23:35.5489040Z ........................................................................ [ 90%]
2026-06-11T08:23:35.8030254Z ........................................................................ [ 94%]
2026-06-11T08:23:35.8351849Z ........................................................................ [ 97%]
2026-06-11T08:23:35.9033979Z .........................................                                [100%]
2026-06-11T08:23:35.9034519Z =================================== FAILURES ===================================
2026-06-11T08:23:35.9035087Z _________ test_bt130_real_data_runner_blocks_missing_coverage_manifest _________
2026-06-11T08:23:35.9035737Z 
2026-06-11T08:23:35.9036162Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-0/test_bt130_real_data_runner_bl0')
2026-06-11T08:23:35.9037157Z 
2026-06-11T08:23:35.9037603Z     def test_bt130_real_data_runner_blocks_missing_coverage_manifest(tmp_path: Path) -> None:
2026-06-11T08:23:35.9038017Z         plans = tmp_path / "plans.json"
2026-06-11T08:23:35.9038263Z         bars = tmp_path / "bars"
2026-06-11T08:23:35.9038494Z         universe = tmp_path / "universe.csv"
2026-06-11T08:23:35.9038736Z         out = tmp_path / "evidence.json"
2026-06-11T08:23:35.9038960Z         _write_plan(plans)
2026-06-11T08:23:35.9039159Z         _write_bars(bars)
```

```text
2026-06-11T08:23:35.9043804Z         payload = json.loads(out.read_text(encoding="utf-8"))
2026-06-11T08:23:35.9044086Z         assert payload["data_source"] == "real_data"
2026-06-11T08:23:35.9044364Z         assert payload["is_demo"] is False
2026-06-11T08:23:35.9044642Z >       assert payload["input_pack_gate_status"] == "PASSED"
2026-06-11T08:23:35.9044944Z E       AssertionError: assert 'FAILED' == 'PASSED'
2026-06-11T08:23:35.9045186Z E         
2026-06-11T08:23:35.9045350Z E         - PASSED
2026-06-11T08:23:35.9045517Z E         + FAILED
2026-06-11T08:23:35.9045608Z 
2026-06-11T08:23:35.9045778Z tests/test_bt130_real_historical_evidence_pack_gate.py:108: AssertionError
2026-06-11T08:23:35.9046175Z ___________ test_bt130_real_data_runner_blocks_fully_rejected_plans ____________
2026-06-11T08:23:35.9046408Z 
2026-06-11T08:23:35.9046778Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-0/test_bt130_real_data_runner_bl1')
2026-06-11T08:23:35.9047053Z 
2026-06-11T08:23:35.9047242Z     def test_bt130_real_data_runner_blocks_fully_rejected_plans(tmp_path: Path) -> None:
2026-06-11T08:23:35.9047590Z         plans = tmp_path / "plans.json"
```

```text
2026-06-11T08:23:35.9044642Z >       assert payload["input_pack_gate_status"] == "PASSED"
2026-06-11T08:23:35.9044944Z E       AssertionError: assert 'FAILED' == 'PASSED'
2026-06-11T08:23:35.9045186Z E         
2026-06-11T08:23:35.9045350Z E         - PASSED
2026-06-11T08:23:35.9045517Z E         + FAILED
2026-06-11T08:23:35.9045608Z 
2026-06-11T08:23:35.9045778Z tests/test_bt130_real_historical_evidence_pack_gate.py:108: AssertionError
2026-06-11T08:23:35.9046175Z ___________ test_bt130_real_data_runner_blocks_fully_rejected_plans ____________
2026-06-11T08:23:35.9046408Z 
2026-06-11T08:23:35.9046778Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-0/test_bt130_real_data_runner_bl1')
2026-06-11T08:23:35.9047053Z 
2026-06-11T08:23:35.9047242Z     def test_bt130_real_data_runner_blocks_fully_rejected_plans(tmp_path: Path) -> None:
2026-06-11T08:23:35.9047590Z         plans = tmp_path / "plans.json"
2026-06-11T08:23:35.9047823Z         bars = tmp_path / "bars"
2026-06-11T08:23:35.9048050Z         universe = tmp_path / "universe.csv"
2026-06-11T08:23:35.9048304Z         coverage = tmp_path / "coverage.json"
```

```text
2026-06-11T08:23:35.9045186Z E         
2026-06-11T08:23:35.9045350Z E         - PASSED
2026-06-11T08:23:35.9045517Z E         + FAILED
2026-06-11T08:23:35.9045608Z 
2026-06-11T08:23:35.9045778Z tests/test_bt130_real_historical_evidence_pack_gate.py:108: AssertionError
2026-06-11T08:23:35.9046175Z ___________ test_bt130_real_data_runner_blocks_fully_rejected_plans ____________
2026-06-11T08:23:35.9046408Z 
2026-06-11T08:23:35.9046778Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-0/test_bt130_real_data_runner_bl1')
2026-06-11T08:23:35.9047053Z 
2026-06-11T08:23:35.9047242Z     def test_bt130_real_data_runner_blocks_fully_rejected_plans(tmp_path: Path) -> None:
2026-06-11T08:23:35.9047590Z         plans = tmp_path / "plans.json"
2026-06-11T08:23:35.9047823Z         bars = tmp_path / "bars"
2026-06-11T08:23:35.9048050Z         universe = tmp_path / "universe.csv"
2026-06-11T08:23:35.9048304Z         coverage = tmp_path / "coverage.json"
2026-06-11T08:23:35.9048539Z         out = tmp_path / "evidence.json"
2026-06-11T08:23:35.9048783Z         _write_plan(plans, unsupported_action=True)
```

```text
2026-06-11T08:23:35.9053111Z         )
2026-06-11T08:23:35.9053266Z     
2026-06-11T08:23:35.9053439Z         assert result.returncode == 1
2026-06-11T08:23:35.9053702Z >       assert "accepted_plan_count=0" in result.stdout
2026-06-11T08:23:35.9054331Z E       AssertionError: assert 'accepted_plan_count=0' in 'BT9 real historical input pack gate status: FAIL\n- coverage_manifest_symbol_0_not_object\n- coverage_manifest_missing_symbol:SPY\n'
2026-06-11T08:23:35.9056228Z E        +  where 'BT9 real historical input pack gate status: FAIL\n- coverage_manifest_symbol_0_not_object\n- coverage_manifest_missing_symbol:SPY\n' = CompletedProcess(args=['/opt/hostedtoolcache/Python/3.11.15/x64/bin/python', 'scripts/run_historical_entry_exit_backte... pack gate status: FAIL\n- coverage_manifest_symbol_0_not_object\n- coverage_manifest_missing_symbol:SPY\n', stderr='').stdout
2026-06-11T08:23:35.9058256Z 
2026-06-11T08:23:35.9065183Z tests/test_bt130_real_historical_evidence_pack_gate.py:142: AssertionError
2026-06-11T08:23:35.9065623Z _________________ test_bt9_input_pack_passes_with_valid_files __________________
2026-06-11T08:23:35.9065868Z 
2026-06-11T08:23:35.9066077Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-0/test_bt9_input_pack_passes_wit0')
2026-06-11T08:23:35.9066349Z 
2026-06-11T08:23:35.9066711Z     def test_bt9_input_pack_passes_with_valid_files(tmp_path: Path) -> None:
2026-06-11T08:23:35.9067099Z         universe = tmp_path / "universe.csv"
2026-06-11T08:23:35.9067337Z         bars = tmp_path / "bars"
2026-06-11T08:23:35.9067566Z         plans = tmp_path / "plans.json"
```

```text
2026-06-11T08:23:35.9053702Z >       assert "accepted_plan_count=0" in result.stdout
2026-06-11T08:23:35.9054331Z E       AssertionError: assert 'accepted_plan_count=0' in 'BT9 real historical input pack gate status: FAIL\n- coverage_manifest_symbol_0_not_object\n- coverage_manifest_missing_symbol:SPY\n'
2026-06-11T08:23:35.9056228Z E        +  where 'BT9 real historical input pack gate status: FAIL\n- coverage_manifest_symbol_0_not_object\n- coverage_manifest_missing_symbol:SPY\n' = CompletedProcess(args=['/opt/hostedtoolcache/Python/3.11.15/x64/bin/python', 'scripts/run_historical_entry_exit_backte... pack gate status: FAIL\n- coverage_manifest_symbol_0_not_object\n- coverage_manifest_missing_symbol:SPY\n', stderr='').stdout
2026-06-11T08:23:35.9058256Z 
2026-06-11T08:23:35.9065183Z tests/test_bt130_real_historical_evidence_pack_gate.py:142: AssertionError
2026-06-11T08:23:35.9065623Z _________________ test_bt9_input_pack_passes_with_valid_files __________________
2026-06-11T08:23:35.9065868Z 
2026-06-11T08:23:35.9066077Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-0/test_bt9_input_pack_passes_wit0')
2026-06-11T08:23:35.9066349Z 
2026-06-11T08:23:35.9066711Z     def test_bt9_input_pack_passes_with_valid_files(tmp_path: Path) -> None:
2026-06-11T08:23:35.9067099Z         universe = tmp_path / "universe.csv"
2026-06-11T08:23:35.9067337Z         bars = tmp_path / "bars"
2026-06-11T08:23:35.9067566Z         plans = tmp_path / "plans.json"
2026-06-11T08:23:35.9067809Z         _write_universe(universe)
2026-06-11T08:23:35.9068033Z         _write_bars(bars)
2026-06-11T08:23:35.9068241Z         _write_trade_plans(plans)
```

```text
2026-06-11T08:23:35.9068437Z     
2026-06-11T08:23:35.9068755Z         report = validate_bt9_input_pack(universe_path=universe, bars_root=bars, trade_plans_path=plans)
2026-06-11T08:23:35.9069111Z     
2026-06-11T08:23:35.9069277Z >       assert report.passed is True
2026-06-11T08:23:35.9069518Z E       AssertionError: assert False is True
2026-06-11T08:23:35.9070375Z E        +  where False = BT9RealHistoricalInputPackReport(passed=False, universe_path='/tmp/pytest-of-runner/pytest-0/test_bt9_input_pack_passe...2e768d3e61c37f54fed585974d3cdda614de'}, failures=['missing_coverage_manifest', 'coverage_manifest_missing_symbol:SPY']).passed
2026-06-11T08:23:35.9071143Z 
2026-06-11T08:23:35.9071310Z tests/test_bt9_real_historical_input_pack_gate.py:95: AssertionError
2026-06-11T08:23:35.9071707Z __ test_real_data_runner_blocks_trade_plans_not_generated_by_runtime_pipeline __
2026-06-11T08:23:35.9072041Z 
2026-06-11T08:23:35.9072269Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-0/test_real_data_runner_blocks_t0')
2026-06-11T08:23:35.9072538Z 
2026-06-11T08:23:35.9072777Z     def test_real_data_runner_blocks_trade_plans_not_generated_by_runtime_pipeline(tmp_path: Path) -> None:
2026-06-11T08:23:35.9073173Z         universe = tmp_path / "universe.csv"
2026-06-11T08:23:35.9073415Z         bars = tmp_path / "bars"
2026-06-11T08:23:35.9073636Z         plans = tmp_path / "plans.json"
```

```text
2026-06-11T08:23:35.9069277Z >       assert report.passed is True
2026-06-11T08:23:35.9069518Z E       AssertionError: assert False is True
2026-06-11T08:23:35.9070375Z E        +  where False = BT9RealHistoricalInputPackReport(passed=False, universe_path='/tmp/pytest-of-runner/pytest-0/test_bt9_input_pack_passe...2e768d3e61c37f54fed585974d3cdda614de'}, failures=['missing_coverage_manifest', 'coverage_manifest_missing_symbol:SPY']).passed
2026-06-11T08:23:35.9071143Z 
2026-06-11T08:23:35.9071310Z tests/test_bt9_real_historical_input_pack_gate.py:95: AssertionError
2026-06-11T08:23:35.9071707Z __ test_real_data_runner_blocks_trade_plans_not_generated_by_runtime_pipeline __
2026-06-11T08:23:35.9072041Z 
2026-06-11T08:23:35.9072269Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-0/test_real_data_runner_blocks_t0')
2026-06-11T08:23:35.9072538Z 
2026-06-11T08:23:35.9072777Z     def test_real_data_runner_blocks_trade_plans_not_generated_by_runtime_pipeline(tmp_path: Path) -> None:
2026-06-11T08:23:35.9073173Z         universe = tmp_path / "universe.csv"
2026-06-11T08:23:35.9073415Z         bars = tmp_path / "bars"
2026-06-11T08:23:35.9073636Z         plans = tmp_path / "plans.json"
2026-06-11T08:23:35.9073912Z         coverage_manifest = tmp_path / "coverage_manifest.json"
2026-06-11T08:23:35.9074237Z         json_output = tmp_path / "blocked-evidence.json"
2026-06-11T08:23:35.9074536Z         markdown_output = tmp_path / "blocked-evidence.md"
```
