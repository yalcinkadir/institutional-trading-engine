# GitHub Actions Workflow Error Report

Generated: 2026-06-12 08:43 UTC
Repository: `yalcinkadir/institutional-trading-engine`
Filter since: 2026-06-11 08:43 UTC
Failed runs included: 8

## Decision Engine Tests

- Run ID: `27403781697`
- Branch: `main`
- Commit: `d99bb93d78c9`
- Title: Keep decision consistency adapter in tests (#200)
- Created: 2026-06-12T08:19:08Z
- Updated: 2026-06-12T08:19:58Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27403781697

### Failed job: tests

- Job ID: `80987764449`
- Started: 2026-06-12T08:19:10Z
- Completed: 2026-06-12T08:19:57Z
- Failed steps: 5. Run pytest

#### Error context

```text
2026-06-12T08:19:54.9762983Z ........................................................................ [ 90%]
2026-06-12T08:19:55.1896184Z ........................................................................ [ 94%]
2026-06-12T08:19:55.2310710Z ........................................................................ [ 97%]
2026-06-12T08:19:55.3208329Z ............................................                             [100%]
2026-06-12T08:19:55.3209231Z =================================== FAILURES ===================================
2026-06-12T08:19:55.3209852Z _______________ test_arch106_current_inventory_satisfies_ratchet _______________
2026-06-12T08:19:55.3210262Z 
2026-06-12T08:19:55.3210960Z     def test_arch106_current_inventory_satisfies_ratchet() -> None:
2026-06-12T08:19:55.3212011Z         inventory, classification = _inventory_and_classification()
2026-06-12T08:19:55.3212481Z     
2026-06-12T08:19:55.3212837Z         result = validate_ratchet(inventory, classification)
2026-06-12T08:19:55.3213281Z     
2026-06-12T08:19:55.3213600Z >       assert result.ok, result.as_text()
2026-06-12T08:19:55.3214095Z E       AssertionError: ARCH106 ratchet guard failed:
2026-06-12T08:19:55.3214682Z E         - unclassified legacy baseline grew: current=267, allowed=266; classify new modules before merge
2026-06-12T08:19:55.3215156Z E
```

```text
2026-06-12T08:19:55.3212481Z     
2026-06-12T08:19:55.3212837Z         result = validate_ratchet(inventory, classification)
2026-06-12T08:19:55.3213281Z     
2026-06-12T08:19:55.3213600Z >       assert result.ok, result.as_text()
2026-06-12T08:19:55.3214095Z E       AssertionError: ARCH106 ratchet guard failed:
2026-06-12T08:19:55.3214682Z E         - unclassified legacy baseline grew: current=267, allowed=266; classify new modules before merge
2026-06-12T08:19:55.3215156Z E         
2026-06-12T08:19:55.3215360Z E       assert False
2026-06-12T08:19:55.3215960Z E        +  where False = RatchetResult(ok=False, messages=('unclassified legacy baseline grew: current=267, allowed=266; classify new modules before merge',)).ok
2026-06-12T08:19:55.3216505Z 
2026-06-12T08:19:55.3216668Z tests/test_arch106_ratchet_guard.py:23: AssertionError
2026-06-12T08:19:55.3217118Z ______ test_arch106_committed_inventory_artifact_matches_generator_output ______
2026-06-12T08:19:55.3217432Z 
2026-06-12T08:19:55.3217662Z     def test_arch106_committed_inventory_artifact_matches_generator_output() -> None:
2026-06-12T08:19:55.3218152Z         is_current, message = check_inventory(INVENTORY_ARTIFACT_PATH)
2026-06-12T08:19:55.3218495Z
```

```text
2026-06-12T08:19:55.3215156Z E         
2026-06-12T08:19:55.3215360Z E       assert False
2026-06-12T08:19:55.3215960Z E        +  where False = RatchetResult(ok=False, messages=('unclassified legacy baseline grew: current=267, allowed=266; classify new modules before merge',)).ok
2026-06-12T08:19:55.3216505Z 
2026-06-12T08:19:55.3216668Z tests/test_arch106_ratchet_guard.py:23: AssertionError
2026-06-12T08:19:55.3217118Z ______ test_arch106_committed_inventory_artifact_matches_generator_output ______
2026-06-12T08:19:55.3217432Z 
2026-06-12T08:19:55.3217662Z     def test_arch106_committed_inventory_artifact_matches_generator_output() -> None:
2026-06-12T08:19:55.3218152Z         is_current, message = check_inventory(INVENTORY_ARTIFACT_PATH)
2026-06-12T08:19:55.3218495Z     
2026-06-12T08:19:55.3218705Z >       assert is_current, message
2026-06-12T08:19:55.3219063Z E       AssertionError: ARCH106 unclassified legacy baseline exceeded.
2026-06-12T08:19:55.3219474Z E         Current unclassified legacy modules: 267
2026-06-12T08:19:55.3219793Z E         Allowed baseline: 266
2026-06-12T08:19:55.3220514Z E         New production modules under src/ must be explicitly classified as connected_runtime, runtime_entrypoint, test_only, experimental, quarantine or delete_candidate before merge.
2026-06-12T08:19:55.3221214Z E
```

```text
2026-06-12T08:19:55.3217662Z     def test_arch106_committed_inventory_artifact_matches_generator_output() -> None:
2026-06-12T08:19:55.3218152Z         is_current, message = check_inventory(INVENTORY_ARTIFACT_PATH)
2026-06-12T08:19:55.3218495Z     
2026-06-12T08:19:55.3218705Z >       assert is_current, message
2026-06-12T08:19:55.3219063Z E       AssertionError: ARCH106 unclassified legacy baseline exceeded.
2026-06-12T08:19:55.3219474Z E         Current unclassified legacy modules: 267
2026-06-12T08:19:55.3219793Z E         Allowed baseline: 266
2026-06-12T08:19:55.3220514Z E         New production modules under src/ must be explicitly classified as connected_runtime, runtime_entrypoint, test_only, experimental, quarantine or delete_candidate before merge.
2026-06-12T08:19:55.3221214Z E         
2026-06-12T08:19:55.3221633Z E       assert False
2026-06-12T08:19:55.3221775Z 
2026-06-12T08:19:55.3221959Z tests/test_architecture_module_inventory.py:99: AssertionError
2026-06-12T08:19:55.3222436Z _____________ test_arch106_inventory_check_reports_stale_artifact ______________
2026-06-12T08:19:55.3222730Z 
2026-06-12T08:19:55.3222984Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-0/test_arch106_inventory_check_r1')
2026-06-12T08:19:55.3223313Z
```

```text
2026-06-12T08:19:55.3220514Z E         New production modules under src/ must be explicitly classified as connected_runtime, runtime_entrypoint, test_only, experimental, quarantine or delete_candidate before merge.
2026-06-12T08:19:55.3221214Z E         
2026-06-12T08:19:55.3221633Z E       assert False
2026-06-12T08:19:55.3221775Z 
2026-06-12T08:19:55.3221959Z tests/test_architecture_module_inventory.py:99: AssertionError
2026-06-12T08:19:55.3222436Z _____________ test_arch106_inventory_check_reports_stale_artifact ______________
2026-06-12T08:19:55.3222730Z 
2026-06-12T08:19:55.3222984Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-0/test_arch106_inventory_check_r1')
2026-06-12T08:19:55.3223313Z 
2026-06-12T08:19:55.3223530Z     def test_arch106_inventory_check_reports_stale_artifact(tmp_path) -> None:
2026-06-12T08:19:55.3223997Z         stale_path = tmp_path / "module_inventory.generated.json"
2026-06-12T08:19:55.3224348Z         stale_path.write_text(
2026-06-12T08:19:55.3224603Z             json.dumps(
2026-06-12T08:19:55.3224832Z                 {
2026-06-12T08:19:55.3225069Z                     "schema_version": 1,
2026-06-12T08:19:55.3225423Z                     "source": "scripts/generate_module_inventory.py",
```

```text
2026-06-12T08:19:55.3229026Z         is_current, message = check_inventory(stale_path)
2026-06-12T08:19:55.3229325Z     
2026-06-12T08:19:55.3229535Z         assert is_current is False
2026-06-12T08:19:55.3229878Z >       assert "ARCH106 module inventory artifact is stale" in message
2026-06-12T08:19:55.3231530Z E       AssertionError: assert 'ARCH106 module inventory artifact is stale' in 'ARCH106 unclassified legacy baseline exceeded.\nCurrent unclassified legacy modules: 267\nAllowed baseline: 266\nNew ...fied as connected_runtime, runtime_entrypoint, test_only, experimental, quarantine or delete_candidate before merge.\n'
2026-06-12T08:19:55.3232720Z 
2026-06-12T08:19:55.3232898Z tests/test_architecture_module_inventory.py:185: AssertionError
2026-06-12T08:19:55.3233315Z =============================== warnings summary ===============================
2026-06-12T08:19:55.3233860Z tests/test_screening_engine.py::test_asset_score_status_bands
2026-06-12T08:19:55.3234858Z   /home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_screening_engine.py:20: DeprecationWarning: src.scoring.asset_score.calculate_asset_score is deprecated; use src.reporting.decision_report
2026-06-12T08:19:55.3235811Z     strong = calculate_asset_score(25, 25, 20, 10, 10)
2026-06-12T08:19:55.3236026Z 
2026-06-12T08:19:55.3236209Z tests/test_screening_engine.py::test_asset_score_status_bands
2026-06-12T08:19:55.3237171Z   /home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_screening_engine.py:21: DeprecationWarning: src.scoring.asset_score.calculate_asset_score is deprecated; use src.reporting.decision_report
2026-06-12T08:19:55.3238083Z     ready = calculate_asset_score(20, 20, 15, 10, 10)
2026-06-12T08:19:55.3238298Z
```

```text
2026-06-12T08:19:55.3229535Z         assert is_current is False
2026-06-12T08:19:55.3229878Z >       assert "ARCH106 module inventory artifact is stale" in message
2026-06-12T08:19:55.3231530Z E       AssertionError: assert 'ARCH106 module inventory artifact is stale' in 'ARCH106 unclassified legacy baseline exceeded.\nCurrent unclassified legacy modules: 267\nAllowed baseline: 266\nNew ...fied as connected_runtime, runtime_entrypoint, test_only, experimental, quarantine or delete_candidate before merge.\n'
2026-06-12T08:19:55.3232720Z 
2026-06-12T08:19:55.3232898Z tests/test_architecture_module_inventory.py:185: AssertionError
2026-06-12T08:19:55.3233315Z =============================== warnings summary ===============================
2026-06-12T08:19:55.3233860Z tests/test_screening_engine.py::test_asset_score_status_bands
2026-06-12T08:19:55.3234858Z   /home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_screening_engine.py:20: DeprecationWarning: src.scoring.asset_score.calculate_asset_score is deprecated; use src.reporting.decision_report
2026-06-12T08:19:55.3235811Z     strong = calculate_asset_score(25, 25, 20, 10, 10)
2026-06-12T08:19:55.3236026Z 
2026-06-12T08:19:55.3236209Z tests/test_screening_engine.py::test_asset_score_status_bands
2026-06-12T08:19:55.3237171Z   /home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_screening_engine.py:21: DeprecationWarning: src.scoring.asset_score.calculate_asset_score is deprecated; use src.reporting.decision_report
2026-06-12T08:19:55.3238083Z     ready = calculate_asset_score(20, 20, 15, 10, 10)
2026-06-12T08:19:55.3238298Z 
2026-06-12T08:19:55.3238457Z tests/test_screening_engine.py::test_asset_score_status_bands
2026-06-12T08:19:55.3239391Z   /home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_screening_engine.py:22: DeprecationWarning: src.scoring.asset_score.calculate_asset_score is deprecated; use src.reporting.decision_report
```

```text
2026-06-12T08:19:55.3243162Z     result = calculate_confidence_score(
2026-06-12T08:19:55.3243364Z 
2026-06-12T08:19:55.3243604Z -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2026-06-12T08:19:55.3244125Z =========================== short test summary info ============================
2026-06-12T08:19:55.3244805Z FAILED tests/test_arch106_ratchet_guard.py::test_arch106_current_inventory_satisfies_ratchet - AssertionError: ARCH106 ratchet guard failed:
2026-06-12T08:19:55.3245581Z   - unclassified legacy baseline grew: current=267, allowed=266; classify new modules before merge
2026-06-12T08:19:55.3246038Z   
2026-06-12T08:19:55.3246235Z assert False
2026-06-12T08:19:55.3246799Z  +  where False = RatchetResult(ok=False, messages=('unclassified legacy baseline grew: current=267, allowed=266; classify new modules before merge',)).ok
2026-06-12T08:19:55.3247882Z FAILED tests/test_architecture_module_inventory.py::test_arch106_committed_inventory_artifact_matches_generator_output - AssertionError: ARCH106 unclassified legacy baseline exceeded.
2026-06-12T08:19:55.3248638Z   Current unclassified legacy modules: 267
2026-06-12T08:19:55.3248937Z   Allowed baseline: 266
2026-06-12T08:19:55.3249616Z   New production modules under src/ must be explicitly classified as connected_runtime, runtime_entrypoint, test_only, experimental, quarantine or delete_candidate before merge.
2026-06-12T08:19:55.3250294Z   
2026-06-12T08:19:55.3250481Z assert False
2026-06-12T08:19:55.3252205Z FAILED tests/test_architecture_module_inventory.py::test_arch106_inventory_check_reports_stale_artifact - AssertionError: assert 'ARCH106 module inventory artifact is stale' in 'ARCH106 unclassified legacy baseline exceeded.\nCurrent unclassified legacy modules: 267\nAllowed baseline: 266\nNew ...fied as connected_runtime, runtime_entrypoint, test_only, experimental, quarantine or delete_candidate before merge.\n'
```

## CI

- Run ID: `27403781652`
- Branch: `main`
- Commit: `d99bb93d78c9`
- Title: Keep decision consistency adapter in tests (#200)
- Created: 2026-06-12T08:19:07Z
- Updated: 2026-06-12T08:20:18Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27403781652

### Failed job: Pytest

- Job ID: `80987764455`
- Started: 2026-06-12T08:19:10Z
- Completed: 2026-06-12T08:20:17Z
- Failed steps: 53. Full regression suite residual tests

#### Error context

```text
2026-06-12T08:20:14.9232897Z ........................................................................ [ 89%]
2026-06-12T08:20:15.0736452Z ........................................................................ [ 93%]
2026-06-12T08:20:15.1727276Z ........................................................................ [ 98%]
2026-06-12T08:20:15.2410058Z .......................                                                  [100%]
2026-06-12T08:20:15.2411928Z =================================== FAILURES ===================================
2026-06-12T08:20:15.2412688Z _______________ test_arch106_current_inventory_satisfies_ratchet _______________
2026-06-12T08:20:15.2413130Z 
2026-06-12T08:20:15.2413409Z     def test_arch106_current_inventory_satisfies_ratchet() -> None:
2026-06-12T08:20:15.2414128Z         inventory, classification = _inventory_and_classification()
2026-06-12T08:20:15.2414684Z     
2026-06-12T08:20:15.2415070Z         result = validate_ratchet(inventory, classification)
2026-06-12T08:20:15.2415907Z     
2026-06-12T08:20:15.2416223Z >       assert result.ok, result.as_text()
2026-06-12T08:20:15.2416738Z E       AssertionError: ARCH106 ratchet guard failed:
2026-06-12T08:20:15.2417562Z E         - unclassified legacy baseline grew: current=267, allowed=266; classify new modules before merge
2026-06-12T08:20:15.2418131Z E
```

```text
2026-06-12T08:20:15.2414684Z     
2026-06-12T08:20:15.2415070Z         result = validate_ratchet(inventory, classification)
2026-06-12T08:20:15.2415907Z     
2026-06-12T08:20:15.2416223Z >       assert result.ok, result.as_text()
2026-06-12T08:20:15.2416738Z E       AssertionError: ARCH106 ratchet guard failed:
2026-06-12T08:20:15.2417562Z E         - unclassified legacy baseline grew: current=267, allowed=266; classify new modules before merge
2026-06-12T08:20:15.2418131Z E         
2026-06-12T08:20:15.2418336Z E       assert False
2026-06-12T08:20:15.2418924Z E        +  where False = RatchetResult(ok=False, messages=('unclassified legacy baseline grew: current=267, allowed=266; classify new modules before merge',)).ok
2026-06-12T08:20:15.2419482Z 
2026-06-12T08:20:15.2419631Z tests/test_arch106_ratchet_guard.py:23: AssertionError
2026-06-12T08:20:15.2420466Z ______ test_arch106_committed_inventory_artifact_matches_generator_output ______
2026-06-12T08:20:15.2420930Z 
2026-06-12T08:20:15.2421271Z     def test_arch106_committed_inventory_artifact_matches_generator_output() -> None:
2026-06-12T08:20:15.2421987Z         is_current, message = check_inventory(INVENTORY_ARTIFACT_PATH)
2026-06-12T08:20:15.2422463Z
```

```text
2026-06-12T08:20:15.2418131Z E         
2026-06-12T08:20:15.2418336Z E       assert False
2026-06-12T08:20:15.2418924Z E        +  where False = RatchetResult(ok=False, messages=('unclassified legacy baseline grew: current=267, allowed=266; classify new modules before merge',)).ok
2026-06-12T08:20:15.2419482Z 
2026-06-12T08:20:15.2419631Z tests/test_arch106_ratchet_guard.py:23: AssertionError
2026-06-12T08:20:15.2420466Z ______ test_arch106_committed_inventory_artifact_matches_generator_output ______
2026-06-12T08:20:15.2420930Z 
2026-06-12T08:20:15.2421271Z     def test_arch106_committed_inventory_artifact_matches_generator_output() -> None:
2026-06-12T08:20:15.2421987Z         is_current, message = check_inventory(INVENTORY_ARTIFACT_PATH)
2026-06-12T08:20:15.2422463Z     
2026-06-12T08:20:15.2422738Z >       assert is_current, message
2026-06-12T08:20:15.2423230Z E       AssertionError: ARCH106 unclassified legacy baseline exceeded.
2026-06-12T08:20:15.2423785Z E         Current unclassified legacy modules: 267
2026-06-12T08:20:15.2424183Z E         Allowed baseline: 266
2026-06-12T08:20:15.2424931Z E         New production modules under src/ must be explicitly classified as connected_runtime, runtime_entrypoint, test_only, experimental, quarantine or delete_candidate before merge.
2026-06-12T08:20:15.2425675Z E
```

```text
2026-06-12T08:20:15.2421271Z     def test_arch106_committed_inventory_artifact_matches_generator_output() -> None:
2026-06-12T08:20:15.2421987Z         is_current, message = check_inventory(INVENTORY_ARTIFACT_PATH)
2026-06-12T08:20:15.2422463Z     
2026-06-12T08:20:15.2422738Z >       assert is_current, message
2026-06-12T08:20:15.2423230Z E       AssertionError: ARCH106 unclassified legacy baseline exceeded.
2026-06-12T08:20:15.2423785Z E         Current unclassified legacy modules: 267
2026-06-12T08:20:15.2424183Z E         Allowed baseline: 266
2026-06-12T08:20:15.2424931Z E         New production modules under src/ must be explicitly classified as connected_runtime, runtime_entrypoint, test_only, experimental, quarantine or delete_candidate before merge.
2026-06-12T08:20:15.2425675Z E         
2026-06-12T08:20:15.2425883Z E       assert False
2026-06-12T08:20:15.2426023Z 
2026-06-12T08:20:15.2426208Z tests/test_architecture_module_inventory.py:99: AssertionError
2026-06-12T08:20:15.2426686Z _____________ test_arch106_inventory_check_reports_stale_artifact ______________
2026-06-12T08:20:15.2426986Z 
2026-06-12T08:20:15.2427237Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-33/test_arch106_inventory_check_r1')
2026-06-12T08:20:15.2427583Z
```

```text
2026-06-12T08:20:15.2424931Z E         New production modules under src/ must be explicitly classified as connected_runtime, runtime_entrypoint, test_only, experimental, quarantine or delete_candidate before merge.
2026-06-12T08:20:15.2425675Z E         
2026-06-12T08:20:15.2425883Z E       assert False
2026-06-12T08:20:15.2426023Z 
2026-06-12T08:20:15.2426208Z tests/test_architecture_module_inventory.py:99: AssertionError
2026-06-12T08:20:15.2426686Z _____________ test_arch106_inventory_check_reports_stale_artifact ______________
2026-06-12T08:20:15.2426986Z 
2026-06-12T08:20:15.2427237Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-33/test_arch106_inventory_check_r1')
2026-06-12T08:20:15.2427583Z 
2026-06-12T08:20:15.2428044Z     def test_arch106_inventory_check_reports_stale_artifact(tmp_path) -> None:
2026-06-12T08:20:15.2428530Z         stale_path = tmp_path / "module_inventory.generated.json"
2026-06-12T08:20:15.2428880Z         stale_path.write_text(
2026-06-12T08:20:15.2429138Z             json.dumps(
2026-06-12T08:20:15.2429374Z                 {
2026-06-12T08:20:15.2429603Z                     "schema_version": 1,
2026-06-12T08:20:15.2430218Z                     "source": "scripts/generate_module_inventory.py",
```

```text
2026-06-12T08:20:15.2433835Z         is_current, message = check_inventory(stale_path)
2026-06-12T08:20:15.2434140Z     
2026-06-12T08:20:15.2434339Z         assert is_current is False
2026-06-12T08:20:15.2434692Z >       assert "ARCH106 module inventory artifact is stale" in message
2026-06-12T08:20:15.2435941Z E       AssertionError: assert 'ARCH106 module inventory artifact is stale' in 'ARCH106 unclassified legacy baseline exceeded.\nCurrent unclassified legacy modules: 267\nAllowed baseline: 266\nNew ...fied as connected_runtime, runtime_entrypoint, test_only, experimental, quarantine or delete_candidate before merge.\n'
2026-06-12T08:20:15.2436987Z 
2026-06-12T08:20:15.2437320Z tests/test_architecture_module_inventory.py:185: AssertionError
2026-06-12T08:20:15.2437743Z =============================== warnings summary ===============================
2026-06-12T08:20:15.2438265Z tests/test_screening_engine.py::test_asset_score_status_bands
2026-06-12T08:20:15.2439273Z   /home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_screening_engine.py:20: DeprecationWarning: src.scoring.asset_score.calculate_asset_score is deprecated; use src.reporting.decision_report
2026-06-12T08:20:15.2440442Z     strong = calculate_asset_score(25, 25, 20, 10, 10)
2026-06-12T08:20:15.2440715Z 
2026-06-12T08:20:15.2440896Z tests/test_screening_engine.py::test_asset_score_status_bands
2026-06-12T08:20:15.2441849Z   /home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_screening_engine.py:21: DeprecationWarning: src.scoring.asset_score.calculate_asset_score is deprecated; use src.reporting.decision_report
2026-06-12T08:20:15.2442795Z     ready = calculate_asset_score(20, 20, 15, 10, 10)
2026-06-12T08:20:15.2443008Z
```

```text
2026-06-12T08:20:15.2434339Z         assert is_current is False
2026-06-12T08:20:15.2434692Z >       assert "ARCH106 module inventory artifact is stale" in message
2026-06-12T08:20:15.2435941Z E       AssertionError: assert 'ARCH106 module inventory artifact is stale' in 'ARCH106 unclassified legacy baseline exceeded.\nCurrent unclassified legacy modules: 267\nAllowed baseline: 266\nNew ...fied as connected_runtime, runtime_entrypoint, test_only, experimental, quarantine or delete_candidate before merge.\n'
2026-06-12T08:20:15.2436987Z 
2026-06-12T08:20:15.2437320Z tests/test_architecture_module_inventory.py:185: AssertionError
2026-06-12T08:20:15.2437743Z =============================== warnings summary ===============================
2026-06-12T08:20:15.2438265Z tests/test_screening_engine.py::test_asset_score_status_bands
2026-06-12T08:20:15.2439273Z   /home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_screening_engine.py:20: DeprecationWarning: src.scoring.asset_score.calculate_asset_score is deprecated; use src.reporting.decision_report
2026-06-12T08:20:15.2440442Z     strong = calculate_asset_score(25, 25, 20, 10, 10)
2026-06-12T08:20:15.2440715Z 
2026-06-12T08:20:15.2440896Z tests/test_screening_engine.py::test_asset_score_status_bands
2026-06-12T08:20:15.2441849Z   /home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_screening_engine.py:21: DeprecationWarning: src.scoring.asset_score.calculate_asset_score is deprecated; use src.reporting.decision_report
2026-06-12T08:20:15.2442795Z     ready = calculate_asset_score(20, 20, 15, 10, 10)
2026-06-12T08:20:15.2443008Z 
2026-06-12T08:20:15.2443176Z tests/test_screening_engine.py::test_asset_score_status_bands
2026-06-12T08:20:15.2444143Z   /home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_screening_engine.py:22: DeprecationWarning: src.scoring.asset_score.calculate_asset_score is deprecated; use src.reporting.decision_report
```

```text
2026-06-12T08:20:15.2447565Z     result = calculate_confidence_score(
2026-06-12T08:20:15.2447766Z 
2026-06-12T08:20:15.2447989Z -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2026-06-12T08:20:15.2448587Z =========================== short test summary info ============================
2026-06-12T08:20:15.2449269Z FAILED tests/test_arch106_ratchet_guard.py::test_arch106_current_inventory_satisfies_ratchet - AssertionError: ARCH106 ratchet guard failed:
2026-06-12T08:20:15.2450220Z   - unclassified legacy baseline grew: current=267, allowed=266; classify new modules before merge
2026-06-12T08:20:15.2450688Z   
2026-06-12T08:20:15.2450886Z assert False
2026-06-12T08:20:15.2451454Z  +  where False = RatchetResult(ok=False, messages=('unclassified legacy baseline grew: current=267, allowed=266; classify new modules before merge',)).ok
2026-06-12T08:20:15.2452543Z FAILED tests/test_architecture_module_inventory.py::test_arch106_committed_inventory_artifact_matches_generator_output - AssertionError: ARCH106 unclassified legacy baseline exceeded.
2026-06-12T08:20:15.2453303Z   Current unclassified legacy modules: 267
2026-06-12T08:20:15.2453595Z   Allowed baseline: 266
2026-06-12T08:20:15.2454278Z   New production modules under src/ must be explicitly classified as connected_runtime, runtime_entrypoint, test_only, experimental, quarantine or delete_candidate before merge.
2026-06-12T08:20:15.2454963Z   
2026-06-12T08:20:15.2455149Z assert False
2026-06-12T08:20:15.2456551Z FAILED tests/test_architecture_module_inventory.py::test_arch106_inventory_check_reports_stale_artifact - AssertionError: assert 'ARCH106 module inventory artifact is stale' in 'ARCH106 unclassified legacy baseline exceeded.\nCurrent unclassified legacy modules: 267\nAllowed baseline: 266\nNew ...fied as connected_runtime, runtime_entrypoint, test_only, experimental, quarantine or delete_candidate before merge.\n'
```

## Decision Engine Tests

- Run ID: `27403336786`
- Branch: `main`
- Commit: `80d76cfbf51a`
- Title: Update changelog for decision engine consistency (#200)
- Created: 2026-06-12T08:09:43Z
- Updated: 2026-06-12T08:10:32Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27403336786

### Failed job: tests

- Job ID: `80986323833`
- Started: 2026-06-12T08:09:45Z
- Completed: 2026-06-12T08:10:31Z
- Failed steps: 5. Run pytest

#### Error context

```text
2026-06-12T08:10:29.6409618Z ........................................................................ [ 90%]
2026-06-12T08:10:29.8556518Z ........................................................................ [ 94%]
2026-06-12T08:10:29.8981683Z ........................................................................ [ 97%]
2026-06-12T08:10:29.9871232Z ............................................                             [100%]
2026-06-12T08:10:29.9872454Z =================================== FAILURES ===================================
2026-06-12T08:10:29.9873174Z _______________ test_arch106_current_inventory_satisfies_ratchet _______________
2026-06-12T08:10:29.9873662Z 
2026-06-12T08:10:29.9874389Z     def test_arch106_current_inventory_satisfies_ratchet() -> None:
2026-06-12T08:10:29.9875351Z         inventory, classification = _inventory_and_classification()
2026-06-12T08:10:29.9875884Z     
2026-06-12T08:10:29.9876247Z         result = validate_ratchet(inventory, classification)
2026-06-12T08:10:29.9876713Z     
2026-06-12T08:10:29.9877029Z >       assert result.ok, result.as_text()
2026-06-12T08:10:29.9877493Z E       AssertionError: ARCH106 ratchet guard failed:
2026-06-12T08:10:29.9878260Z E         - unclassified legacy baseline grew: current=267, allowed=266; classify new modules before merge
2026-06-12T08:10:29.9878948Z E
```

```text
2026-06-12T08:10:29.9875884Z     
2026-06-12T08:10:29.9876247Z         result = validate_ratchet(inventory, classification)
2026-06-12T08:10:29.9876713Z     
2026-06-12T08:10:29.9877029Z >       assert result.ok, result.as_text()
2026-06-12T08:10:29.9877493Z E       AssertionError: ARCH106 ratchet guard failed:
2026-06-12T08:10:29.9878260Z E         - unclassified legacy baseline grew: current=267, allowed=266; classify new modules before merge
2026-06-12T08:10:29.9878948Z E         
2026-06-12T08:10:29.9879229Z E       assert False
2026-06-12T08:10:29.9880111Z E        +  where False = RatchetResult(ok=False, messages=('unclassified legacy baseline grew: current=267, allowed=266; classify new modules before merge',)).ok
2026-06-12T08:10:29.9880972Z 
2026-06-12T08:10:29.9881178Z tests/test_arch106_ratchet_guard.py:23: AssertionError
2026-06-12T08:10:29.9881834Z ______ test_arch106_committed_inventory_artifact_matches_generator_output ______
2026-06-12T08:10:29.9882531Z 
2026-06-12T08:10:29.9882875Z     def test_arch106_committed_inventory_artifact_matches_generator_output() -> None:
2026-06-12T08:10:29.9883619Z         is_current, message = check_inventory(INVENTORY_ARTIFACT_PATH)
2026-06-12T08:10:29.9884119Z
```

```text
2026-06-12T08:10:29.9878948Z E         
2026-06-12T08:10:29.9879229Z E       assert False
2026-06-12T08:10:29.9880111Z E        +  where False = RatchetResult(ok=False, messages=('unclassified legacy baseline grew: current=267, allowed=266; classify new modules before merge',)).ok
2026-06-12T08:10:29.9880972Z 
2026-06-12T08:10:29.9881178Z tests/test_arch106_ratchet_guard.py:23: AssertionError
2026-06-12T08:10:29.9881834Z ______ test_arch106_committed_inventory_artifact_matches_generator_output ______
2026-06-12T08:10:29.9882531Z 
2026-06-12T08:10:29.9882875Z     def test_arch106_committed_inventory_artifact_matches_generator_output() -> None:
2026-06-12T08:10:29.9883619Z         is_current, message = check_inventory(INVENTORY_ARTIFACT_PATH)
2026-06-12T08:10:29.9884119Z     
2026-06-12T08:10:29.9884395Z >       assert is_current, message
2026-06-12T08:10:29.9884906Z E       AssertionError: ARCH106 unclassified legacy baseline exceeded.
2026-06-12T08:10:29.9885464Z E         Current unclassified legacy modules: 267
2026-06-12T08:10:29.9885905Z E         Allowed baseline: 266
2026-06-12T08:10:29.9886968Z E         New production modules under src/ must be explicitly classified as connected_runtime, runtime_entrypoint, test_only, experimental, quarantine or delete_candidate before merge.
2026-06-12T08:10:29.9888086Z E
```

```text
2026-06-12T08:10:29.9882875Z     def test_arch106_committed_inventory_artifact_matches_generator_output() -> None:
2026-06-12T08:10:29.9883619Z         is_current, message = check_inventory(INVENTORY_ARTIFACT_PATH)
2026-06-12T08:10:29.9884119Z     
2026-06-12T08:10:29.9884395Z >       assert is_current, message
2026-06-12T08:10:29.9884906Z E       AssertionError: ARCH106 unclassified legacy baseline exceeded.
2026-06-12T08:10:29.9885464Z E         Current unclassified legacy modules: 267
2026-06-12T08:10:29.9885905Z E         Allowed baseline: 266
2026-06-12T08:10:29.9886968Z E         New production modules under src/ must be explicitly classified as connected_runtime, runtime_entrypoint, test_only, experimental, quarantine or delete_candidate before merge.
2026-06-12T08:10:29.9888086Z E         
2026-06-12T08:10:29.9888359Z E       assert False
2026-06-12T08:10:29.9888560Z 
2026-06-12T08:10:29.9888807Z tests/test_architecture_module_inventory.py:99: AssertionError
2026-06-12T08:10:29.9889492Z _____________ test_arch106_inventory_check_reports_stale_artifact ______________
2026-06-12T08:10:29.9889927Z 
2026-06-12T08:10:29.9890280Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-0/test_arch106_inventory_check_r1')
2026-06-12T08:10:29.9890765Z
```

```text
2026-06-12T08:10:29.9886968Z E         New production modules under src/ must be explicitly classified as connected_runtime, runtime_entrypoint, test_only, experimental, quarantine or delete_candidate before merge.
2026-06-12T08:10:29.9888086Z E         
2026-06-12T08:10:29.9888359Z E       assert False
2026-06-12T08:10:29.9888560Z 
2026-06-12T08:10:29.9888807Z tests/test_architecture_module_inventory.py:99: AssertionError
2026-06-12T08:10:29.9889492Z _____________ test_arch106_inventory_check_reports_stale_artifact ______________
2026-06-12T08:10:29.9889927Z 
2026-06-12T08:10:29.9890280Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-0/test_arch106_inventory_check_r1')
2026-06-12T08:10:29.9890765Z 
2026-06-12T08:10:29.9891075Z     def test_arch106_inventory_check_reports_stale_artifact(tmp_path) -> None:
2026-06-12T08:10:29.9891748Z         stale_path = tmp_path / "module_inventory.generated.json"
2026-06-12T08:10:29.9892395Z         stale_path.write_text(
2026-06-12T08:10:29.9892751Z             json.dumps(
2026-06-12T08:10:29.9893053Z                 {
2026-06-12T08:10:29.9893352Z                     "schema_version": 1,
2026-06-12T08:10:29.9893818Z                     "source": "scripts/generate_module_inventory.py",
```

```text
2026-06-12T08:10:29.9898781Z         is_current, message = check_inventory(stale_path)
2026-06-12T08:10:29.9899210Z     
2026-06-12T08:10:29.9899478Z         assert is_current is False
2026-06-12T08:10:29.9899959Z >       assert "ARCH106 module inventory artifact is stale" in message
2026-06-12T08:10:29.9902180Z E       AssertionError: assert 'ARCH106 module inventory artifact is stale' in 'ARCH106 unclassified legacy baseline exceeded.\nCurrent unclassified legacy modules: 267\nAllowed baseline: 266\nNew ...fied as connected_runtime, runtime_entrypoint, test_only, experimental, quarantine or delete_candidate before merge.\n'
2026-06-12T08:10:29.9903995Z 
2026-06-12T08:10:29.9904245Z tests/test_architecture_module_inventory.py:185: AssertionError
2026-06-12T08:10:29.9904838Z =============================== warnings summary ===============================
2026-06-12T08:10:29.9905561Z tests/test_screening_engine.py::test_asset_score_status_bands
2026-06-12T08:10:29.9907051Z   /home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_screening_engine.py:20: DeprecationWarning: src.scoring.asset_score.calculate_asset_score is deprecated; use src.reporting.decision_report
2026-06-12T08:10:29.9908461Z     strong = calculate_asset_score(25, 25, 20, 10, 10)
2026-06-12T08:10:29.9908759Z 
2026-06-12T08:10:29.9909013Z tests/test_screening_engine.py::test_asset_score_status_bands
2026-06-12T08:10:29.9910464Z   /home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_screening_engine.py:21: DeprecationWarning: src.scoring.asset_score.calculate_asset_score is deprecated; use src.reporting.decision_report
2026-06-12T08:10:29.9911875Z     ready = calculate_asset_score(20, 20, 15, 10, 10)
2026-06-12T08:10:29.9912329Z
```

```text
2026-06-12T08:10:29.9899478Z         assert is_current is False
2026-06-12T08:10:29.9899959Z >       assert "ARCH106 module inventory artifact is stale" in message
2026-06-12T08:10:29.9902180Z E       AssertionError: assert 'ARCH106 module inventory artifact is stale' in 'ARCH106 unclassified legacy baseline exceeded.\nCurrent unclassified legacy modules: 267\nAllowed baseline: 266\nNew ...fied as connected_runtime, runtime_entrypoint, test_only, experimental, quarantine or delete_candidate before merge.\n'
2026-06-12T08:10:29.9903995Z 
2026-06-12T08:10:29.9904245Z tests/test_architecture_module_inventory.py:185: AssertionError
2026-06-12T08:10:29.9904838Z =============================== warnings summary ===============================
2026-06-12T08:10:29.9905561Z tests/test_screening_engine.py::test_asset_score_status_bands
2026-06-12T08:10:29.9907051Z   /home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_screening_engine.py:20: DeprecationWarning: src.scoring.asset_score.calculate_asset_score is deprecated; use src.reporting.decision_report
2026-06-12T08:10:29.9908461Z     strong = calculate_asset_score(25, 25, 20, 10, 10)
2026-06-12T08:10:29.9908759Z 
2026-06-12T08:10:29.9909013Z tests/test_screening_engine.py::test_asset_score_status_bands
2026-06-12T08:10:29.9910464Z   /home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_screening_engine.py:21: DeprecationWarning: src.scoring.asset_score.calculate_asset_score is deprecated; use src.reporting.decision_report
2026-06-12T08:10:29.9911875Z     ready = calculate_asset_score(20, 20, 15, 10, 10)
2026-06-12T08:10:29.9912329Z 
2026-06-12T08:10:29.9912561Z tests/test_screening_engine.py::test_asset_score_status_bands
2026-06-12T08:10:29.9914031Z   /home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_screening_engine.py:22: DeprecationWarning: src.scoring.asset_score.calculate_asset_score is deprecated; use src.reporting.decision_report
```

```text
2026-06-12T08:10:29.9919319Z     result = calculate_confidence_score(
2026-06-12T08:10:29.9919597Z 
2026-06-12T08:10:29.9919919Z -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2026-06-12T08:10:29.9920585Z =========================== short test summary info ============================
2026-06-12T08:10:29.9921606Z FAILED tests/test_arch106_ratchet_guard.py::test_arch106_current_inventory_satisfies_ratchet - AssertionError: ARCH106 ratchet guard failed:
2026-06-12T08:10:29.9922961Z   - unclassified legacy baseline grew: current=267, allowed=266; classify new modules before merge
2026-06-12T08:10:29.9923631Z   
2026-06-12T08:10:29.9923895Z assert False
2026-06-12T08:10:29.9924733Z  +  where False = RatchetResult(ok=False, messages=('unclassified legacy baseline grew: current=267, allowed=266; classify new modules before merge',)).ok
2026-06-12T08:10:29.9926406Z FAILED tests/test_architecture_module_inventory.py::test_arch106_committed_inventory_artifact_matches_generator_output - AssertionError: ARCH106 unclassified legacy baseline exceeded.
2026-06-12T08:10:29.9927567Z   Current unclassified legacy modules: 267
2026-06-12T08:10:29.9927967Z   Allowed baseline: 266
2026-06-12T08:10:29.9928970Z   New production modules under src/ must be explicitly classified as connected_runtime, runtime_entrypoint, test_only, experimental, quarantine or delete_candidate before merge.
2026-06-12T08:10:29.9930087Z   
2026-06-12T08:10:29.9930356Z assert False
2026-06-12T08:10:29.9932974Z FAILED tests/test_architecture_module_inventory.py::test_arch106_inventory_check_reports_stale_artifact - AssertionError: assert 'ARCH106 module inventory artifact is stale' in 'ARCH106 unclassified legacy baseline exceeded.\nCurrent unclassified legacy modules: 267\nAllowed baseline: 266\nNew ...fied as connected_runtime, runtime_entrypoint, test_only, experimental, quarantine or delete_candidate before merge.\n'
```

## CI

- Run ID: `27403336869`
- Branch: `main`
- Commit: `80d76cfbf51a`
- Title: Update changelog for decision engine consistency (#200)
- Created: 2026-06-12T08:09:43Z
- Updated: 2026-06-12T08:10:56Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27403336869

### Failed job: Pytest

- Job ID: `80986324061`
- Started: 2026-06-12T08:09:45Z
- Completed: 2026-06-12T08:10:56Z
- Failed steps: 53. Full regression suite residual tests

#### Error context

```text
2026-06-12T08:10:52.9561661Z ........................................................................ [ 89%]
2026-06-12T08:10:53.1208857Z ........................................................................ [ 93%]
2026-06-12T08:10:53.2199919Z ........................................................................ [ 98%]
2026-06-12T08:10:53.2926895Z .......................                                                  [100%]
2026-06-12T08:10:53.2927759Z =================================== FAILURES ===================================
2026-06-12T08:10:53.2928958Z _______________ test_arch106_current_inventory_satisfies_ratchet _______________
2026-06-12T08:10:53.2929525Z 
2026-06-12T08:10:53.2929887Z     def test_arch106_current_inventory_satisfies_ratchet() -> None:
2026-06-12T08:10:53.2930698Z         inventory, classification = _inventory_and_classification()
2026-06-12T08:10:53.2931407Z     
2026-06-12T08:10:53.2931860Z         result = validate_ratchet(inventory, classification)
2026-06-12T08:10:53.2932838Z     
2026-06-12T08:10:53.2933232Z >       assert result.ok, result.as_text()
2026-06-12T08:10:53.2933844Z E       AssertionError: ARCH106 ratchet guard failed:
2026-06-12T08:10:53.2934776Z E         - unclassified legacy baseline grew: current=267, allowed=266; classify new modules before merge
2026-06-12T08:10:53.2935627Z E
```

```text
2026-06-12T08:10:53.2931407Z     
2026-06-12T08:10:53.2931860Z         result = validate_ratchet(inventory, classification)
2026-06-12T08:10:53.2932838Z     
2026-06-12T08:10:53.2933232Z >       assert result.ok, result.as_text()
2026-06-12T08:10:53.2933844Z E       AssertionError: ARCH106 ratchet guard failed:
2026-06-12T08:10:53.2934776Z E         - unclassified legacy baseline grew: current=267, allowed=266; classify new modules before merge
2026-06-12T08:10:53.2935627Z E         
2026-06-12T08:10:53.2935975Z E       assert False
2026-06-12T08:10:53.2937071Z E        +  where False = RatchetResult(ok=False, messages=('unclassified legacy baseline grew: current=267, allowed=266; classify new modules before merge',)).ok
2026-06-12T08:10:53.2938117Z 
2026-06-12T08:10:53.2938666Z tests/test_arch106_ratchet_guard.py:23: AssertionError
2026-06-12T08:10:53.2939506Z ______ test_arch106_committed_inventory_artifact_matches_generator_output ______
2026-06-12T08:10:53.2940117Z 
2026-06-12T08:10:53.2940551Z     def test_arch106_committed_inventory_artifact_matches_generator_output() -> None:
2026-06-12T08:10:53.2941520Z         is_current, message = check_inventory(INVENTORY_ARTIFACT_PATH)
2026-06-12T08:10:53.2942162Z
```

```text
2026-06-12T08:10:53.2935627Z E         
2026-06-12T08:10:53.2935975Z E       assert False
2026-06-12T08:10:53.2937071Z E        +  where False = RatchetResult(ok=False, messages=('unclassified legacy baseline grew: current=267, allowed=266; classify new modules before merge',)).ok
2026-06-12T08:10:53.2938117Z 
2026-06-12T08:10:53.2938666Z tests/test_arch106_ratchet_guard.py:23: AssertionError
2026-06-12T08:10:53.2939506Z ______ test_arch106_committed_inventory_artifact_matches_generator_output ______
2026-06-12T08:10:53.2940117Z 
2026-06-12T08:10:53.2940551Z     def test_arch106_committed_inventory_artifact_matches_generator_output() -> None:
2026-06-12T08:10:53.2941520Z         is_current, message = check_inventory(INVENTORY_ARTIFACT_PATH)
2026-06-12T08:10:53.2942162Z     
2026-06-12T08:10:53.2942508Z >       assert is_current, message
2026-06-12T08:10:53.2943084Z E       AssertionError: ARCH106 unclassified legacy baseline exceeded.
2026-06-12T08:10:53.2943726Z E         Current unclassified legacy modules: 267
2026-06-12T08:10:53.2944211Z E         Allowed baseline: 266
2026-06-12T08:10:53.2945403Z E         New production modules under src/ must be explicitly classified as connected_runtime, runtime_entrypoint, test_only, experimental, quarantine or delete_candidate before merge.
2026-06-12T08:10:53.2946618Z E
```

```text
2026-06-12T08:10:53.2940551Z     def test_arch106_committed_inventory_artifact_matches_generator_output() -> None:
2026-06-12T08:10:53.2941520Z         is_current, message = check_inventory(INVENTORY_ARTIFACT_PATH)
2026-06-12T08:10:53.2942162Z     
2026-06-12T08:10:53.2942508Z >       assert is_current, message
2026-06-12T08:10:53.2943084Z E       AssertionError: ARCH106 unclassified legacy baseline exceeded.
2026-06-12T08:10:53.2943726Z E         Current unclassified legacy modules: 267
2026-06-12T08:10:53.2944211Z E         Allowed baseline: 266
2026-06-12T08:10:53.2945403Z E         New production modules under src/ must be explicitly classified as connected_runtime, runtime_entrypoint, test_only, experimental, quarantine or delete_candidate before merge.
2026-06-12T08:10:53.2946618Z E         
2026-06-12T08:10:53.2946916Z E       assert False
2026-06-12T08:10:53.2947130Z 
2026-06-12T08:10:53.2947403Z tests/test_architecture_module_inventory.py:99: AssertionError
2026-06-12T08:10:53.2948154Z _____________ test_arch106_inventory_check_reports_stale_artifact ______________
2026-06-12T08:10:53.2949063Z 
2026-06-12T08:10:53.2949456Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-33/test_arch106_inventory_check_r1')
2026-06-12T08:10:53.2950027Z
```

```text
2026-06-12T08:10:53.2945403Z E         New production modules under src/ must be explicitly classified as connected_runtime, runtime_entrypoint, test_only, experimental, quarantine or delete_candidate before merge.
2026-06-12T08:10:53.2946618Z E         
2026-06-12T08:10:53.2946916Z E       assert False
2026-06-12T08:10:53.2947130Z 
2026-06-12T08:10:53.2947403Z tests/test_architecture_module_inventory.py:99: AssertionError
2026-06-12T08:10:53.2948154Z _____________ test_arch106_inventory_check_reports_stale_artifact ______________
2026-06-12T08:10:53.2949063Z 
2026-06-12T08:10:53.2949456Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-33/test_arch106_inventory_check_r1')
2026-06-12T08:10:53.2950027Z 
2026-06-12T08:10:53.2950623Z     def test_arch106_inventory_check_reports_stale_artifact(tmp_path) -> None:
2026-06-12T08:10:53.2951391Z         stale_path = tmp_path / "module_inventory.generated.json"
2026-06-12T08:10:53.2951946Z         stale_path.write_text(
2026-06-12T08:10:53.2952325Z             json.dumps(
2026-06-12T08:10:53.2952659Z                 {
2026-06-12T08:10:53.2952994Z                     "schema_version": 1,
2026-06-12T08:10:53.2953502Z                     "source": "scripts/generate_module_inventory.py",
```

```text
2026-06-12T08:10:53.2959106Z         is_current, message = check_inventory(stale_path)
2026-06-12T08:10:53.2959565Z     
2026-06-12T08:10:53.2959856Z         assert is_current is False
2026-06-12T08:10:53.2960393Z >       assert "ARCH106 module inventory artifact is stale" in message
2026-06-12T08:10:53.2962451Z E       AssertionError: assert 'ARCH106 module inventory artifact is stale' in 'ARCH106 unclassified legacy baseline exceeded.\nCurrent unclassified legacy modules: 267\nAllowed baseline: 266\nNew ...fied as connected_runtime, runtime_entrypoint, test_only, experimental, quarantine or delete_candidate before merge.\n'
2026-06-12T08:10:53.2964545Z 
2026-06-12T08:10:53.2964824Z tests/test_architecture_module_inventory.py:185: AssertionError
2026-06-12T08:10:53.2965476Z =============================== warnings summary ===============================
2026-06-12T08:10:53.2966233Z tests/test_screening_engine.py::test_asset_score_status_bands
2026-06-12T08:10:53.2967854Z   /home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_screening_engine.py:20: DeprecationWarning: src.scoring.asset_score.calculate_asset_score is deprecated; use src.reporting.decision_report
2026-06-12T08:10:53.2969653Z     strong = calculate_asset_score(25, 25, 20, 10, 10)
2026-06-12T08:10:53.2969996Z 
2026-06-12T08:10:53.2970268Z tests/test_screening_engine.py::test_asset_score_status_bands
2026-06-12T08:10:53.2971889Z   /home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_screening_engine.py:21: DeprecationWarning: src.scoring.asset_score.calculate_asset_score is deprecated; use src.reporting.decision_report
2026-06-12T08:10:53.2973483Z     ready = calculate_asset_score(20, 20, 15, 10, 10)
2026-06-12T08:10:53.2973820Z
```

```text
2026-06-12T08:10:53.2959856Z         assert is_current is False
2026-06-12T08:10:53.2960393Z >       assert "ARCH106 module inventory artifact is stale" in message
2026-06-12T08:10:53.2962451Z E       AssertionError: assert 'ARCH106 module inventory artifact is stale' in 'ARCH106 unclassified legacy baseline exceeded.\nCurrent unclassified legacy modules: 267\nAllowed baseline: 266\nNew ...fied as connected_runtime, runtime_entrypoint, test_only, experimental, quarantine or delete_candidate before merge.\n'
2026-06-12T08:10:53.2964545Z 
2026-06-12T08:10:53.2964824Z tests/test_architecture_module_inventory.py:185: AssertionError
2026-06-12T08:10:53.2965476Z =============================== warnings summary ===============================
2026-06-12T08:10:53.2966233Z tests/test_screening_engine.py::test_asset_score_status_bands
2026-06-12T08:10:53.2967854Z   /home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_screening_engine.py:20: DeprecationWarning: src.scoring.asset_score.calculate_asset_score is deprecated; use src.reporting.decision_report
2026-06-12T08:10:53.2969653Z     strong = calculate_asset_score(25, 25, 20, 10, 10)
2026-06-12T08:10:53.2969996Z 
2026-06-12T08:10:53.2970268Z tests/test_screening_engine.py::test_asset_score_status_bands
2026-06-12T08:10:53.2971889Z   /home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_screening_engine.py:21: DeprecationWarning: src.scoring.asset_score.calculate_asset_score is deprecated; use src.reporting.decision_report
2026-06-12T08:10:53.2973483Z     ready = calculate_asset_score(20, 20, 15, 10, 10)
2026-06-12T08:10:53.2973820Z 
2026-06-12T08:10:53.2974092Z tests/test_screening_engine.py::test_asset_score_status_bands
2026-06-12T08:10:53.2975683Z   /home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_screening_engine.py:22: DeprecationWarning: src.scoring.asset_score.calculate_asset_score is deprecated; use src.reporting.decision_report
```

```text
2026-06-12T08:10:53.2981579Z     result = calculate_confidence_score(
2026-06-12T08:10:53.2981883Z 
2026-06-12T08:10:53.2982229Z -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2026-06-12T08:10:53.2983161Z =========================== short test summary info ============================
2026-06-12T08:10:53.2984296Z FAILED tests/test_arch106_ratchet_guard.py::test_arch106_current_inventory_satisfies_ratchet - AssertionError: ARCH106 ratchet guard failed:
2026-06-12T08:10:53.2985616Z   - unclassified legacy baseline grew: current=267, allowed=266; classify new modules before merge
2026-06-12T08:10:53.2986358Z   
2026-06-12T08:10:53.2986625Z assert False
2026-06-12T08:10:53.2987555Z  +  where False = RatchetResult(ok=False, messages=('unclassified legacy baseline grew: current=267, allowed=266; classify new modules before merge',)).ok
2026-06-12T08:10:53.2989657Z FAILED tests/test_architecture_module_inventory.py::test_arch106_committed_inventory_artifact_matches_generator_output - AssertionError: ARCH106 unclassified legacy baseline exceeded.
2026-06-12T08:10:53.2990984Z   Current unclassified legacy modules: 267
2026-06-12T08:10:53.2991428Z   Allowed baseline: 266
2026-06-12T08:10:53.2992561Z   New production modules under src/ must be explicitly classified as connected_runtime, runtime_entrypoint, test_only, experimental, quarantine or delete_candidate before merge.
2026-06-12T08:10:53.2993768Z   
2026-06-12T08:10:53.2994043Z assert False
2026-06-12T08:10:53.2996566Z FAILED tests/test_architecture_module_inventory.py::test_arch106_inventory_check_reports_stale_artifact - AssertionError: assert 'ARCH106 module inventory artifact is stale' in 'ARCH106 unclassified legacy baseline exceeded.\nCurrent unclassified legacy modules: 267\nAllowed baseline: 266\nNew ...fied as connected_runtime, runtime_entrypoint, test_only, experimental, quarantine or delete_candidate before merge.\n'
```

## Decision Engine Tests

- Run ID: `27403310091`
- Branch: `main`
- Commit: `07d38fd0bb4b`
- Title: Document decision engine consistency contract (#200)
- Created: 2026-06-12T08:09:11Z
- Updated: 2026-06-12T08:09:59Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27403310091

### Failed job: tests

- Job ID: `80986238872`
- Started: 2026-06-12T08:09:14Z
- Completed: 2026-06-12T08:09:58Z
- Failed steps: 5. Run pytest

#### Error context

```text
2026-06-12T08:09:55.2681508Z ........................................................................ [ 90%]
2026-06-12T08:09:55.5084437Z ........................................................................ [ 94%]
2026-06-12T08:09:55.5546928Z ........................................................................ [ 97%]
2026-06-12T08:09:55.6486792Z ............................................                             [100%]
2026-06-12T08:09:55.6487881Z =================================== FAILURES ===================================
2026-06-12T08:09:55.6488713Z _______________ test_arch106_current_inventory_satisfies_ratchet _______________
2026-06-12T08:09:55.6489281Z 
2026-06-12T08:09:55.6489965Z     def test_arch106_current_inventory_satisfies_ratchet() -> None:
2026-06-12T08:09:55.6490978Z         inventory, classification = _inventory_and_classification()
2026-06-12T08:09:55.6491520Z     
2026-06-12T08:09:55.6491898Z         result = validate_ratchet(inventory, classification)
2026-06-12T08:09:55.6492361Z     
2026-06-12T08:09:55.6493458Z >       assert result.ok, result.as_text()
2026-06-12T08:09:55.6493944Z E       AssertionError: ARCH106 ratchet guard failed:
2026-06-12T08:09:55.6494738Z E         - unclassified legacy baseline grew: current=267, allowed=266; classify new modules before merge
2026-06-12T08:09:55.6495473Z E
```

```text
2026-06-12T08:09:55.6491520Z     
2026-06-12T08:09:55.6491898Z         result = validate_ratchet(inventory, classification)
2026-06-12T08:09:55.6492361Z     
2026-06-12T08:09:55.6493458Z >       assert result.ok, result.as_text()
2026-06-12T08:09:55.6493944Z E       AssertionError: ARCH106 ratchet guard failed:
2026-06-12T08:09:55.6494738Z E         - unclassified legacy baseline grew: current=267, allowed=266; classify new modules before merge
2026-06-12T08:09:55.6495473Z E         
2026-06-12T08:09:55.6495755Z E       assert False
2026-06-12T08:09:55.6496703Z E        +  where False = RatchetResult(ok=False, messages=('unclassified legacy baseline grew: current=267, allowed=266; classify new modules before merge',)).ok
2026-06-12T08:09:55.6497636Z 
2026-06-12T08:09:55.6497875Z tests/test_arch106_ratchet_guard.py:23: AssertionError
2026-06-12T08:09:55.6498558Z ______ test_arch106_committed_inventory_artifact_matches_generator_output ______
2026-06-12T08:09:55.6499059Z 
2026-06-12T08:09:55.6499417Z     def test_arch106_committed_inventory_artifact_matches_generator_output() -> None:
2026-06-12T08:09:55.6500192Z         is_current, message = check_inventory(INVENTORY_ARTIFACT_PATH)
2026-06-12T08:09:55.6500707Z
```

```text
2026-06-12T08:09:55.6495473Z E         
2026-06-12T08:09:55.6495755Z E       assert False
2026-06-12T08:09:55.6496703Z E        +  where False = RatchetResult(ok=False, messages=('unclassified legacy baseline grew: current=267, allowed=266; classify new modules before merge',)).ok
2026-06-12T08:09:55.6497636Z 
2026-06-12T08:09:55.6497875Z tests/test_arch106_ratchet_guard.py:23: AssertionError
2026-06-12T08:09:55.6498558Z ______ test_arch106_committed_inventory_artifact_matches_generator_output ______
2026-06-12T08:09:55.6499059Z 
2026-06-12T08:09:55.6499417Z     def test_arch106_committed_inventory_artifact_matches_generator_output() -> None:
2026-06-12T08:09:55.6500192Z         is_current, message = check_inventory(INVENTORY_ARTIFACT_PATH)
2026-06-12T08:09:55.6500707Z     
2026-06-12T08:09:55.6500989Z >       assert is_current, message
2026-06-12T08:09:55.6501509Z E       AssertionError: ARCH106 unclassified legacy baseline exceeded.
2026-06-12T08:09:55.6502098Z E         Current unclassified legacy modules: 267
2026-06-12T08:09:55.6502733Z E         Allowed baseline: 266
2026-06-12T08:09:55.6503858Z E         New production modules under src/ must be explicitly classified as connected_runtime, runtime_entrypoint, test_only, experimental, quarantine or delete_candidate before merge.
2026-06-12T08:09:55.6505014Z E
```

```text
2026-06-12T08:09:55.6499417Z     def test_arch106_committed_inventory_artifact_matches_generator_output() -> None:
2026-06-12T08:09:55.6500192Z         is_current, message = check_inventory(INVENTORY_ARTIFACT_PATH)
2026-06-12T08:09:55.6500707Z     
2026-06-12T08:09:55.6500989Z >       assert is_current, message
2026-06-12T08:09:55.6501509Z E       AssertionError: ARCH106 unclassified legacy baseline exceeded.
2026-06-12T08:09:55.6502098Z E         Current unclassified legacy modules: 267
2026-06-12T08:09:55.6502733Z E         Allowed baseline: 266
2026-06-12T08:09:55.6503858Z E         New production modules under src/ must be explicitly classified as connected_runtime, runtime_entrypoint, test_only, experimental, quarantine or delete_candidate before merge.
2026-06-12T08:09:55.6505014Z E         
2026-06-12T08:09:55.6505293Z E       assert False
2026-06-12T08:09:55.6505496Z 
2026-06-12T08:09:55.6505767Z tests/test_architecture_module_inventory.py:99: AssertionError
2026-06-12T08:09:55.6506470Z _____________ test_arch106_inventory_check_reports_stale_artifact ______________
2026-06-12T08:09:55.6506931Z 
2026-06-12T08:09:55.6507289Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-0/test_arch106_inventory_check_r1')
2026-06-12T08:09:55.6507805Z
```

```text
2026-06-12T08:09:55.6503858Z E         New production modules under src/ must be explicitly classified as connected_runtime, runtime_entrypoint, test_only, experimental, quarantine or delete_candidate before merge.
2026-06-12T08:09:55.6505014Z E         
2026-06-12T08:09:55.6505293Z E       assert False
2026-06-12T08:09:55.6505496Z 
2026-06-12T08:09:55.6505767Z tests/test_architecture_module_inventory.py:99: AssertionError
2026-06-12T08:09:55.6506470Z _____________ test_arch106_inventory_check_reports_stale_artifact ______________
2026-06-12T08:09:55.6506931Z 
2026-06-12T08:09:55.6507289Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-0/test_arch106_inventory_check_r1')
2026-06-12T08:09:55.6507805Z 
2026-06-12T08:09:55.6508127Z     def test_arch106_inventory_check_reports_stale_artifact(tmp_path) -> None:
2026-06-12T08:09:55.6508824Z         stale_path = tmp_path / "module_inventory.generated.json"
2026-06-12T08:09:55.6509342Z         stale_path.write_text(
2026-06-12T08:09:55.6509707Z             json.dumps(
2026-06-12T08:09:55.6510013Z                 {
2026-06-12T08:09:55.6510320Z                     "schema_version": 1,
2026-06-12T08:09:55.6510798Z                     "source": "scripts/generate_module_inventory.py",
```

```text
2026-06-12T08:09:55.6516114Z         is_current, message = check_inventory(stale_path)
2026-06-12T08:09:55.6516540Z     
2026-06-12T08:09:55.6516809Z         assert is_current is False
2026-06-12T08:09:55.6517299Z >       assert "ARCH106 module inventory artifact is stale" in message
2026-06-12T08:09:55.6519566Z E       AssertionError: assert 'ARCH106 module inventory artifact is stale' in 'ARCH106 unclassified legacy baseline exceeded.\nCurrent unclassified legacy modules: 267\nAllowed baseline: 266\nNew ...fied as connected_runtime, runtime_entrypoint, test_only, experimental, quarantine or delete_candidate before merge.\n'
2026-06-12T08:09:55.6521624Z 
2026-06-12T08:09:55.6521898Z tests/test_architecture_module_inventory.py:185: AssertionError
2026-06-12T08:09:55.6522689Z =============================== warnings summary ===============================
2026-06-12T08:09:55.6523449Z tests/test_screening_engine.py::test_asset_score_status_bands
2026-06-12T08:09:55.6525032Z   /home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_screening_engine.py:20: DeprecationWarning: src.scoring.asset_score.calculate_asset_score is deprecated; use src.reporting.decision_report
2026-06-12T08:09:55.6526604Z     strong = calculate_asset_score(25, 25, 20, 10, 10)
2026-06-12T08:09:55.6526940Z 
2026-06-12T08:09:55.6527198Z tests/test_screening_engine.py::test_asset_score_status_bands
2026-06-12T08:09:55.6528820Z   /home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_screening_engine.py:21: DeprecationWarning: src.scoring.asset_score.calculate_asset_score is deprecated; use src.reporting.decision_report
2026-06-12T08:09:55.6530403Z     ready = calculate_asset_score(20, 20, 15, 10, 10)
2026-06-12T08:09:55.6530710Z
```

```text
2026-06-12T08:09:55.6516809Z         assert is_current is False
2026-06-12T08:09:55.6517299Z >       assert "ARCH106 module inventory artifact is stale" in message
2026-06-12T08:09:55.6519566Z E       AssertionError: assert 'ARCH106 module inventory artifact is stale' in 'ARCH106 unclassified legacy baseline exceeded.\nCurrent unclassified legacy modules: 267\nAllowed baseline: 266\nNew ...fied as connected_runtime, runtime_entrypoint, test_only, experimental, quarantine or delete_candidate before merge.\n'
2026-06-12T08:09:55.6521624Z 
2026-06-12T08:09:55.6521898Z tests/test_architecture_module_inventory.py:185: AssertionError
2026-06-12T08:09:55.6522689Z =============================== warnings summary ===============================
2026-06-12T08:09:55.6523449Z tests/test_screening_engine.py::test_asset_score_status_bands
2026-06-12T08:09:55.6525032Z   /home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_screening_engine.py:20: DeprecationWarning: src.scoring.asset_score.calculate_asset_score is deprecated; use src.reporting.decision_report
2026-06-12T08:09:55.6526604Z     strong = calculate_asset_score(25, 25, 20, 10, 10)
2026-06-12T08:09:55.6526940Z 
2026-06-12T08:09:55.6527198Z tests/test_screening_engine.py::test_asset_score_status_bands
2026-06-12T08:09:55.6528820Z   /home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_screening_engine.py:21: DeprecationWarning: src.scoring.asset_score.calculate_asset_score is deprecated; use src.reporting.decision_report
2026-06-12T08:09:55.6530403Z     ready = calculate_asset_score(20, 20, 15, 10, 10)
2026-06-12T08:09:55.6530710Z 
2026-06-12T08:09:55.6530957Z tests/test_screening_engine.py::test_asset_score_status_bands
2026-06-12T08:09:55.6532729Z   /home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_screening_engine.py:22: DeprecationWarning: src.scoring.asset_score.calculate_asset_score is deprecated; use src.reporting.decision_report
```

```text
2026-06-12T08:09:55.6538732Z     result = calculate_confidence_score(
2026-06-12T08:09:55.6539024Z 
2026-06-12T08:09:55.6539349Z -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2026-06-12T08:09:55.6540048Z =========================== short test summary info ============================
2026-06-12T08:09:55.6541140Z FAILED tests/test_arch106_ratchet_guard.py::test_arch106_current_inventory_satisfies_ratchet - AssertionError: ARCH106 ratchet guard failed:
2026-06-12T08:09:55.6542596Z   - unclassified legacy baseline grew: current=267, allowed=266; classify new modules before merge
2026-06-12T08:09:55.6543306Z   
2026-06-12T08:09:55.6543576Z assert False
2026-06-12T08:09:55.6544458Z  +  where False = RatchetResult(ok=False, messages=('unclassified legacy baseline grew: current=267, allowed=266; classify new modules before merge',)).ok
2026-06-12T08:09:55.6546311Z FAILED tests/test_architecture_module_inventory.py::test_arch106_committed_inventory_artifact_matches_generator_output - AssertionError: ARCH106 unclassified legacy baseline exceeded.
2026-06-12T08:09:55.6547599Z   Current unclassified legacy modules: 267
2026-06-12T08:09:55.6548017Z   Allowed baseline: 266
2026-06-12T08:09:55.6549110Z   New production modules under src/ must be explicitly classified as connected_runtime, runtime_entrypoint, test_only, experimental, quarantine or delete_candidate before merge.
2026-06-12T08:09:55.6550223Z   
2026-06-12T08:09:55.6550474Z assert False
2026-06-12T08:09:55.6553161Z FAILED tests/test_architecture_module_inventory.py::test_arch106_inventory_check_reports_stale_artifact - AssertionError: assert 'ARCH106 module inventory artifact is stale' in 'ARCH106 unclassified legacy baseline exceeded.\nCurrent unclassified legacy modules: 267\nAllowed baseline: 266\nNew ...fied as connected_runtime, runtime_entrypoint, test_only, experimental, quarantine or delete_candidate before merge.\n'
```

## CI

- Run ID: `27403310128`
- Branch: `main`
- Commit: `07d38fd0bb4b`
- Title: Document decision engine consistency contract (#200)
- Created: 2026-06-12T08:09:11Z
- Updated: 2026-06-12T08:10:16Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27403310128

### Failed job: Pytest

- Job ID: `80986239255`
- Started: 2026-06-12T08:09:13Z
- Completed: 2026-06-12T08:10:15Z
- Failed steps: 53. Full regression suite residual tests

#### Error context

```text
2026-06-12T08:10:10.1627107Z ........................................................................ [ 89%]
2026-06-12T08:10:11.0351389Z ........................................................................ [ 93%]
2026-06-12T08:10:11.1109545Z ........................................................................ [ 98%]
2026-06-12T08:10:11.1642701Z .......................                                                  [100%]
2026-06-12T08:10:11.1643233Z =================================== FAILURES ===================================
2026-06-12T08:10:11.1643756Z _______________ test_arch106_current_inventory_satisfies_ratchet _______________
2026-06-12T08:10:11.1644114Z 
2026-06-12T08:10:11.1644364Z     def test_arch106_current_inventory_satisfies_ratchet() -> None:
2026-06-12T08:10:11.1644889Z         inventory, classification = _inventory_and_classification()
2026-06-12T08:10:11.1645294Z     
2026-06-12T08:10:11.1645761Z         result = validate_ratchet(inventory, classification)
2026-06-12T08:10:11.1646396Z     
2026-06-12T08:10:11.1646655Z >       assert result.ok, result.as_text()
2026-06-12T08:10:11.1647064Z E       AssertionError: ARCH106 ratchet guard failed:
2026-06-12T08:10:11.1647694Z E         - unclassified legacy baseline grew: current=267, allowed=266; classify new modules before merge
2026-06-12T08:10:11.1648249Z E
```

```text
2026-06-12T08:10:11.1645294Z     
2026-06-12T08:10:11.1645761Z         result = validate_ratchet(inventory, classification)
2026-06-12T08:10:11.1646396Z     
2026-06-12T08:10:11.1646655Z >       assert result.ok, result.as_text()
2026-06-12T08:10:11.1647064Z E       AssertionError: ARCH106 ratchet guard failed:
2026-06-12T08:10:11.1647694Z E         - unclassified legacy baseline grew: current=267, allowed=266; classify new modules before merge
2026-06-12T08:10:11.1648249Z E         
2026-06-12T08:10:11.1648485Z E       assert False
2026-06-12T08:10:11.1649212Z E        +  where False = RatchetResult(ok=False, messages=('unclassified legacy baseline grew: current=267, allowed=266; classify new modules before merge',)).ok
2026-06-12T08:10:11.1649897Z 
2026-06-12T08:10:11.1650079Z tests/test_arch106_ratchet_guard.py:23: AssertionError
2026-06-12T08:10:11.1650628Z ______ test_arch106_committed_inventory_artifact_matches_generator_output ______
2026-06-12T08:10:11.1651015Z 
2026-06-12T08:10:11.1651283Z     def test_arch106_committed_inventory_artifact_matches_generator_output() -> None:
2026-06-12T08:10:11.1651905Z         is_current, message = check_inventory(INVENTORY_ARTIFACT_PATH)
2026-06-12T08:10:11.1652322Z
```

```text
2026-06-12T08:10:11.1648249Z E         
2026-06-12T08:10:11.1648485Z E       assert False
2026-06-12T08:10:11.1649212Z E        +  where False = RatchetResult(ok=False, messages=('unclassified legacy baseline grew: current=267, allowed=266; classify new modules before merge',)).ok
2026-06-12T08:10:11.1649897Z 
2026-06-12T08:10:11.1650079Z tests/test_arch106_ratchet_guard.py:23: AssertionError
2026-06-12T08:10:11.1650628Z ______ test_arch106_committed_inventory_artifact_matches_generator_output ______
2026-06-12T08:10:11.1651015Z 
2026-06-12T08:10:11.1651283Z     def test_arch106_committed_inventory_artifact_matches_generator_output() -> None:
2026-06-12T08:10:11.1651905Z         is_current, message = check_inventory(INVENTORY_ARTIFACT_PATH)
2026-06-12T08:10:11.1652322Z     
2026-06-12T08:10:11.1652577Z >       assert is_current, message
2026-06-12T08:10:11.1653016Z E       AssertionError: ARCH106 unclassified legacy baseline exceeded.
2026-06-12T08:10:11.1653502Z E         Current unclassified legacy modules: 267
2026-06-12T08:10:11.1653867Z E         Allowed baseline: 266
2026-06-12T08:10:11.1654756Z E         New production modules under src/ must be explicitly classified as connected_runtime, runtime_entrypoint, test_only, experimental, quarantine or delete_candidate before merge.
2026-06-12T08:10:11.1655785Z E
```

```text
2026-06-12T08:10:11.1651283Z     def test_arch106_committed_inventory_artifact_matches_generator_output() -> None:
2026-06-12T08:10:11.1651905Z         is_current, message = check_inventory(INVENTORY_ARTIFACT_PATH)
2026-06-12T08:10:11.1652322Z     
2026-06-12T08:10:11.1652577Z >       assert is_current, message
2026-06-12T08:10:11.1653016Z E       AssertionError: ARCH106 unclassified legacy baseline exceeded.
2026-06-12T08:10:11.1653502Z E         Current unclassified legacy modules: 267
2026-06-12T08:10:11.1653867Z E         Allowed baseline: 266
2026-06-12T08:10:11.1654756Z E         New production modules under src/ must be explicitly classified as connected_runtime, runtime_entrypoint, test_only, experimental, quarantine or delete_candidate before merge.
2026-06-12T08:10:11.1655785Z E         
2026-06-12T08:10:11.1655999Z E       assert False
2026-06-12T08:10:11.1656147Z 
2026-06-12T08:10:11.1656336Z tests/test_architecture_module_inventory.py:99: AssertionError
2026-06-12T08:10:11.1656866Z _____________ test_arch106_inventory_check_reports_stale_artifact ______________
2026-06-12T08:10:11.1657202Z 
2026-06-12T08:10:11.1657483Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-33/test_arch106_inventory_check_r1')
2026-06-12T08:10:11.1657896Z
```

```text
2026-06-12T08:10:11.1654756Z E         New production modules under src/ must be explicitly classified as connected_runtime, runtime_entrypoint, test_only, experimental, quarantine or delete_candidate before merge.
2026-06-12T08:10:11.1655785Z E         
2026-06-12T08:10:11.1655999Z E       assert False
2026-06-12T08:10:11.1656147Z 
2026-06-12T08:10:11.1656336Z tests/test_architecture_module_inventory.py:99: AssertionError
2026-06-12T08:10:11.1656866Z _____________ test_arch106_inventory_check_reports_stale_artifact ______________
2026-06-12T08:10:11.1657202Z 
2026-06-12T08:10:11.1657483Z tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-33/test_arch106_inventory_check_r1')
2026-06-12T08:10:11.1657896Z 
2026-06-12T08:10:11.1658322Z     def test_arch106_inventory_check_reports_stale_artifact(tmp_path) -> None:
2026-06-12T08:10:11.1658865Z         stale_path = tmp_path / "module_inventory.generated.json"
2026-06-12T08:10:11.1659256Z         stale_path.write_text(
2026-06-12T08:10:11.1659524Z             json.dumps(
2026-06-12T08:10:11.1659758Z                 {
2026-06-12T08:10:11.1659989Z                     "schema_version": 1,
2026-06-12T08:10:11.1660355Z                     "source": "scripts/generate_module_inventory.py",
```

```text
2026-06-12T08:10:11.1664277Z         is_current, message = check_inventory(stale_path)
2026-06-12T08:10:11.1664607Z     
2026-06-12T08:10:11.1664818Z         assert is_current is False
2026-06-12T08:10:11.1665200Z >       assert "ARCH106 module inventory artifact is stale" in message
2026-06-12T08:10:11.1666803Z E       AssertionError: assert 'ARCH106 module inventory artifact is stale' in 'ARCH106 unclassified legacy baseline exceeded.\nCurrent unclassified legacy modules: 267\nAllowed baseline: 266\nNew ...fied as connected_runtime, runtime_entrypoint, test_only, experimental, quarantine or delete_candidate before merge.\n'
2026-06-12T08:10:11.1668408Z 
2026-06-12T08:10:11.1668605Z tests/test_architecture_module_inventory.py:185: AssertionError
2026-06-12T08:10:11.1669081Z =============================== warnings summary ===============================
2026-06-12T08:10:11.1669587Z tests/test_screening_engine.py::test_asset_score_status_bands
2026-06-12T08:10:11.1670775Z   /home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_screening_engine.py:20: DeprecationWarning: src.scoring.asset_score.calculate_asset_score is deprecated; use src.reporting.decision_report
2026-06-12T08:10:11.1671890Z     strong = calculate_asset_score(25, 25, 20, 10, 10)
2026-06-12T08:10:11.1672121Z 
2026-06-12T08:10:11.1672298Z tests/test_screening_engine.py::test_asset_score_status_bands
2026-06-12T08:10:11.1673412Z   /home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_screening_engine.py:21: DeprecationWarning: src.scoring.asset_score.calculate_asset_score is deprecated; use src.reporting.decision_report
2026-06-12T08:10:11.1674497Z     ready = calculate_asset_score(20, 20, 15, 10, 10)
2026-06-12T08:10:11.1674741Z
```

```text
2026-06-12T08:10:11.1664818Z         assert is_current is False
2026-06-12T08:10:11.1665200Z >       assert "ARCH106 module inventory artifact is stale" in message
2026-06-12T08:10:11.1666803Z E       AssertionError: assert 'ARCH106 module inventory artifact is stale' in 'ARCH106 unclassified legacy baseline exceeded.\nCurrent unclassified legacy modules: 267\nAllowed baseline: 266\nNew ...fied as connected_runtime, runtime_entrypoint, test_only, experimental, quarantine or delete_candidate before merge.\n'
2026-06-12T08:10:11.1668408Z 
2026-06-12T08:10:11.1668605Z tests/test_architecture_module_inventory.py:185: AssertionError
2026-06-12T08:10:11.1669081Z =============================== warnings summary ===============================
2026-06-12T08:10:11.1669587Z tests/test_screening_engine.py::test_asset_score_status_bands
2026-06-12T08:10:11.1670775Z   /home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_screening_engine.py:20: DeprecationWarning: src.scoring.asset_score.calculate_asset_score is deprecated; use src.reporting.decision_report
2026-06-12T08:10:11.1671890Z     strong = calculate_asset_score(25, 25, 20, 10, 10)
2026-06-12T08:10:11.1672121Z 
2026-06-12T08:10:11.1672298Z tests/test_screening_engine.py::test_asset_score_status_bands
2026-06-12T08:10:11.1673412Z   /home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_screening_engine.py:21: DeprecationWarning: src.scoring.asset_score.calculate_asset_score is deprecated; use src.reporting.decision_report
2026-06-12T08:10:11.1674497Z     ready = calculate_asset_score(20, 20, 15, 10, 10)
2026-06-12T08:10:11.1674741Z 
2026-06-12T08:10:11.1674922Z tests/test_screening_engine.py::test_asset_score_status_bands
2026-06-12T08:10:11.1676175Z   /home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_screening_engine.py:22: DeprecationWarning: src.scoring.asset_score.calculate_asset_score is deprecated; use src.reporting.decision_report
```

```text
2026-06-12T08:10:11.1680345Z     result = calculate_confidence_score(
2026-06-12T08:10:11.1680566Z 
2026-06-12T08:10:11.1680802Z -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2026-06-12T08:10:11.1681419Z =========================== short test summary info ============================
2026-06-12T08:10:11.1682175Z FAILED tests/test_arch106_ratchet_guard.py::test_arch106_current_inventory_satisfies_ratchet - AssertionError: ARCH106 ratchet guard failed:
2026-06-12T08:10:11.1683061Z   - unclassified legacy baseline grew: current=267, allowed=266; classify new modules before merge
2026-06-12T08:10:11.1683558Z   
2026-06-12T08:10:11.1683749Z assert False
2026-06-12T08:10:11.1684386Z  +  where False = RatchetResult(ok=False, messages=('unclassified legacy baseline grew: current=267, allowed=266; classify new modules before merge',)).ok
2026-06-12T08:10:11.1685786Z FAILED tests/test_architecture_module_inventory.py::test_arch106_committed_inventory_artifact_matches_generator_output - AssertionError: ARCH106 unclassified legacy baseline exceeded.
2026-06-12T08:10:11.1686747Z   Current unclassified legacy modules: 267
2026-06-12T08:10:11.1687061Z   Allowed baseline: 266
2026-06-12T08:10:11.1687841Z   New production modules under src/ must be explicitly classified as connected_runtime, runtime_entrypoint, test_only, experimental, quarantine or delete_candidate before merge.
2026-06-12T08:10:11.1688650Z   
2026-06-12T08:10:11.1688845Z assert False
2026-06-12T08:10:11.1690523Z FAILED tests/test_architecture_module_inventory.py::test_arch106_inventory_check_reports_stale_artifact - AssertionError: assert 'ARCH106 module inventory artifact is stale' in 'ARCH106 unclassified legacy baseline exceeded.\nCurrent unclassified legacy modules: 267\nAllowed baseline: 266\nNew ...fied as connected_runtime, runtime_entrypoint, test_only, experimental, quarantine or delete_candidate before merge.\n'
```

## Module Inventory Freshness

- Run ID: `27403296071`
- Branch: `main`
- Commit: `ac1d12881163`
- Title: Add decision engine consistency adapter (#200)
- Created: 2026-06-12T08:08:54Z
- Updated: 2026-06-12T08:09:04Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27403296071

### Failed job: Check ARCH106 module inventory freshness

- Job ID: `80986195812`
- Started: 2026-06-12T08:08:57Z
- Completed: 2026-06-12T08:09:03Z
- Failed steps: 4. Check committed module inventory

#### Error context

```text
2026-06-12T08:09:00.3558835Z ARCH106 unclassified legacy baseline exceeded.
2026-06-12T08:09:00.3560893Z Current unclassified legacy modules: 267
2026-06-12T08:09:00.3562873Z Allowed baseline: 266
2026-06-12T08:09:00.3614031Z New production modules under src/ must be explicitly classified as connected_runtime, runtime_entrypoint, test_only, experimental, quarantine or delete_candidate before merge.
2026-06-12T08:09:00.3631167Z ##[error]Process completed with exit code 1.
2026-06-12T08:09:00.3923298Z Post job cleanup.
2026-06-12T08:09:00.4928046Z [command]/usr/bin/git version
2026-06-12T08:09:00.4964654Z git version 2.54.0
2026-06-12T08:09:00.5014827Z Temporarily overriding HOME='/home/runner/work/_temp/6075a8c9-4ec2-4ee9-b087-a7719642a90f' before making global git config changes
2026-06-12T08:09:00.5017568Z Adding repository directory to the temporary git global config as a safe directory
2026-06-12T08:09:00.5020218Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-06-12T08:09:00.5068308Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-06-12T08:09:00.5100018Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-06-12T08:09:00.5307517Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-06-12T08:09:00.5330499Z http.https://github.com/.extraheader
2026-06-12T08:09:00.5341785Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

## ARCH106 Module Inventory Guard

- Run ID: `27403296232`
- Branch: `main`
- Commit: `ac1d12881163`
- Title: Add decision engine consistency adapter (#200)
- Created: 2026-06-12T08:08:54Z
- Updated: 2026-06-12T08:09:18Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27403296232

### Failed job: ARCH106 module inventory and runtime reachability guard

- Job ID: `80986196664`
- Started: 2026-06-12T08:08:57Z
- Completed: 2026-06-12T08:09:17Z
- Failed steps: 5. ARCH106 inventory artifact freshness and baseline guard

#### Error context

```text
2026-06-12T08:09:15.7059456Z ARCH106 unclassified legacy baseline exceeded.
2026-06-12T08:09:15.7060057Z Current unclassified legacy modules: 267
2026-06-12T08:09:15.7060479Z Allowed baseline: 266
2026-06-12T08:09:15.7061289Z New production modules under src/ must be explicitly classified as connected_runtime, runtime_entrypoint, test_only, experimental, quarantine or delete_candidate before merge.
2026-06-12T08:09:15.7125004Z ##[error]Process completed with exit code 1.
2026-06-12T08:09:15.7306164Z Post job cleanup.
2026-06-12T08:09:15.8222675Z [command]/usr/bin/git version
2026-06-12T08:09:15.8255935Z git version 2.54.0
2026-06-12T08:09:15.8295987Z Temporarily overriding HOME='/home/runner/work/_temp/182c6697-ab3b-4db1-81e0-d5f15d216720' before making global git config changes
2026-06-12T08:09:15.8297478Z Adding repository directory to the temporary git global config as a safe directory
2026-06-12T08:09:15.8312089Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-06-12T08:09:15.8344270Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-06-12T08:09:15.8373868Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-06-12T08:09:15.8557548Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-06-12T08:09:15.8578017Z http.https://github.com/.extraheader
2026-06-12T08:09:15.8589856Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```
