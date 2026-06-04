# GitHub Actions Workflow Error Report

Generated: 2026-06-04 08:39 UTC
Repository: `yalcinkadir/institutional-trading-engine`
Filter since: 2026-06-03 08:39 UTC
Failed runs included: 10

## CI

- Run ID: `26933810777`
- Branch: `main`
- Commit: `ce09f9bbbb0f`
- Title: .gitignore aktualisieren
- Created: 2026-06-04T05:57:43Z
- Updated: 2026-06-04T05:58:51Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26933810777

### Failed job: Pytest

- Job ID: `79458858922`
- Started: 2026-06-04T05:57:46Z
- Completed: 2026-06-04T05:58:50Z
- Failed steps: 53. Full regression suite residual tests

#### Error context

```text
2026-06-04T05:58:46.1802666Z ........................................................................ [ 86%]
2026-06-04T05:58:47.5762396Z ........................................................................ [ 92%]
2026-06-04T05:58:47.6490222Z ........................................................................ [ 99%]
2026-06-04T05:58:47.6874953Z ...........                                                              [100%]
2026-06-04T05:58:47.6876505Z =================================== FAILURES ===================================
2026-06-04T05:58:47.6877055Z ______ test_arch106_committed_inventory_artifact_matches_generator_output ______
2026-06-04T05:58:47.6877401Z 
2026-06-04T05:58:47.6877686Z     def test_arch106_committed_inventory_artifact_matches_generator_output() -> None:
2026-06-04T05:58:47.6878204Z         expected = build_inventory()
2026-06-04T05:58:47.6878679Z         actual = json.loads(INVENTORY_ARTIFACT_PATH.read_text(encoding="utf-8"))
2026-06-04T05:58:47.6879133Z     
2026-06-04T05:58:47.6879342Z >       assert actual == expected, (
2026-06-04T05:58:47.6879618Z             "ARCH106 inventory artifact is stale. Regenerate it with: "
2026-06-04T05:58:47.6879958Z             "python scripts/generate_module_inventory.py && "
2026-06-04T05:58:47.6880295Z             "git add docs/architecture/module_inventory.generated.json"
2026-06-04T05:58:47.6880573Z         )
```

```text
2026-06-04T05:58:47.6879618Z             "ARCH106 inventory artifact is stale. Regenerate it with: "
2026-06-04T05:58:47.6879958Z             "python scripts/generate_module_inventory.py && "
2026-06-04T05:58:47.6880295Z             "git add docs/architecture/module_inventory.generated.json"
2026-06-04T05:58:47.6880573Z         )
2026-06-04T05:58:47.6881121Z E       AssertionError: ARCH106 inventory artifact is stale. Regenerate it with: python scripts/generate_module_inventory.py && git add docs/architecture/module_inventory.generated.json
2026-06-04T05:58:47.6882043Z E       assert {'classificat....}, ...], ...} == {'classificat....}, ...], ...}
2026-06-04T05:58:47.6882331Z E         
2026-06-04T05:58:47.6882533Z E         Omitting 4 identical items, use -vv to show
2026-06-04T05:58:47.6882793Z E         Differing items:
2026-06-04T05:58:47.6884012Z E         {'modules': [{'classification': 'experimental', 'notes': 'ARCH106 Step 4a: adaptive expectancy research layer. Not mar... yet classified in ARCH106 Step 3.', 'path': 'src/analytics/explainability.py', 'runtime_entrypoint': None, ...}, ...]} != {'modules': [{'classification': 'experimental', 'notes': 'ARCH106 Step 4a: adaptive expectancy research layer. Not mar... yet classified in ARCH106 Step 3.', 'path': 'src/analytics/explainability.py', 'runtime_entrypoint': None, ...}, ...]}
2026-06-04T05:58:47.6885906Z E         {'counters': {'classified_modules': 7, 'connected_runtime': 5, 'experimental': 2, 'total_src_modules': 313, ...}} != {'counters': {'classified_modules': 11, 'connected_runtime': 5, 'experimental': 6, 'total_src_modules': 313, ...}}
2026-06-04T05:58:47.6886535Z E         
2026-06-04T05:58:47.6886702Z E         Full diff:
2026-06-04T05:58:47.6886878Z E           {
2026-06-04T05:58:47.6887147Z E               'classification_source': 'docs/architecture/module_classification.json',
2026-06-04T05:58:47.6887543Z E               'counters': {
```

```text
2026-06-04T05:58:47.7390702Z E               'schema_version': 1,
2026-06-04T05:58:47.7390820Z E               'source': 'scripts/generate_module_inventory.py',
2026-06-04T05:58:47.7390884Z E           }
2026-06-04T05:58:47.7390895Z 
2026-06-04T05:58:47.7391044Z tests/test_architecture_module_inventory.py:93: AssertionError
2026-06-04T05:58:47.7391163Z =============================== warnings summary ===============================
2026-06-04T05:58:47.7391416Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbol_writes_csv_and_metadata
2026-06-04T05:58:47.7391637Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbol_merges_without_duplicates
2026-06-04T05:58:47.7391839Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbols_batch_counts_results
2026-06-04T05:58:47.7392108Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbols_batch_counts_results
2026-06-04T05:58:47.7393136Z   /home/runner/work/institutional-trading-engine/institutional-trading-engine/src/historical/polygon_ingestion.py:125: FutureWarning: The behavior of DataFrame concatenation with empty or all-NA entries is deprecated. In a future version, this will no longer exclude empty or all-NA columns when determining the result dtypes. To retain the old behavior, exclude the relevant entries before the concat operation.
2026-06-04T05:58:47.7393274Z     combined = pd.concat([existing, df], ignore_index=True)
2026-06-04T05:58:47.7393279Z 
2026-06-04T05:58:47.7393473Z -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2026-06-04T05:58:47.7393594Z =========================== short test summary info ============================
2026-06-04T05:58:47.7394344Z FAILED tests/test_architecture_module_inventory.py::test_arch106_committed_inventory_artifact_matches_generator_output - AssertionError: ARCH106 inventory artifact is stale. Regenerate it with: python scripts/generate_module_inventory.py && git add docs/architecture/module_inventory.generated.json
```

```text
2026-06-04T05:58:47.7393274Z     combined = pd.concat([existing, df], ignore_index=True)
2026-06-04T05:58:47.7393279Z 
2026-06-04T05:58:47.7393473Z -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2026-06-04T05:58:47.7393594Z =========================== short test summary info ============================
2026-06-04T05:58:47.7394344Z FAILED tests/test_architecture_module_inventory.py::test_arch106_committed_inventory_artifact_matches_generator_output - AssertionError: ARCH106 inventory artifact is stale. Regenerate it with: python scripts/generate_module_inventory.py && git add docs/architecture/module_inventory.generated.json
2026-06-04T05:58:47.7394487Z assert {'classificat....}, ...], ...} == {'classificat....}, ...], ...}
2026-06-04T05:58:47.7394555Z   
2026-06-04T05:58:47.7394671Z   Omitting 4 identical items, use -vv to show
2026-06-04T05:58:47.7394823Z   Differing items:
2026-06-04T05:58:47.7396132Z   {'modules': [{'classification': 'experimental', 'notes': 'ARCH106 Step 4a: adaptive expectancy research layer. Not mar... yet classified in ARCH106 Step 3.', 'path': 'src/analytics/explainability.py', 'runtime_entrypoint': None, ...}, ...]} != {'modules': [{'classification': 'experimental', 'notes': 'ARCH106 Step 4a: adaptive expectancy research layer. Not mar... yet classified in ARCH106 Step 3.', 'path': 'src/analytics/explainability.py', 'runtime_entrypoint': None, ...}, ...]}
2026-06-04T05:58:47.7396632Z   {'counters': {'classified_modules': 7, 'connected_runtime': 5, 'experimental': 2, 'total_src_modules': 313, ...}} != {'counters': {'classified_modules': 11, 'connected_runtime': 5, 'experimental': 6, 'total_src_modules': 313, ...}}
2026-06-04T05:58:47.7396698Z   
2026-06-04T05:58:47.7396771Z   Full diff:
2026-06-04T05:58:47.7396836Z     {
2026-06-04T05:58:47.7397010Z         'classification_source': 'docs/architecture/module_classification.json',
2026-06-04T05:58:47.7397087Z         'counters': {
```

```text
2026-06-04T05:58:47.7668376Z         'schema_version': 1,
2026-06-04T05:58:47.7668487Z         'source': 'scripts/generate_module_inventory.py',
2026-06-04T05:58:47.7668550Z     }
2026-06-04T05:58:47.7668703Z 1 failed, 1161 passed, 1 skipped, 1 deselected, 4 warnings in 10.68s
2026-06-04T05:58:47.9138884Z ##[error]Process completed with exit code 1.
2026-06-04T05:58:47.9224749Z Post job cleanup.
2026-06-04T05:58:47.9989376Z [command]/usr/bin/git version
2026-06-04T05:58:48.0018359Z git version 2.54.0
2026-06-04T05:58:48.0049436Z Temporarily overriding HOME='/home/runner/work/_temp/d92d1692-63ba-4c9f-b781-d189ed0dfc0f' before making global git config changes
2026-06-04T05:58:48.0050339Z Adding repository directory to the temporary git global config as a safe directory
2026-06-04T05:58:48.0053934Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-06-04T05:58:48.0082590Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-06-04T05:58:48.0108486Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-06-04T05:58:48.0297898Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-06-04T05:58:48.0314864Z http.https://github.com/.extraheader
2026-06-04T05:58:48.0324018Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

## Decision Engine Tests

- Run ID: `26933810803`
- Branch: `main`
- Commit: `ce09f9bbbb0f`
- Title: .gitignore aktualisieren
- Created: 2026-06-04T05:57:43Z
- Updated: 2026-06-04T05:58:22Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26933810803

### Failed job: tests

- Job ID: `79458858850`
- Started: 2026-06-04T05:57:46Z
- Completed: 2026-06-04T05:58:21Z
- Failed steps: 5. Run pytest

#### Error context

```text
2026-06-04T05:58:17.4124294Z ........................................................................ [ 89%]
2026-06-04T05:58:17.6291786Z ........................................................................ [ 94%]
2026-06-04T05:58:17.6678612Z ........................................................................ [ 98%]
2026-06-04T05:58:17.7292819Z ........................                                                 [100%]
2026-06-04T05:58:17.7293827Z =================================== FAILURES ===================================
2026-06-04T05:58:17.7294628Z ______ test_arch106_committed_inventory_artifact_matches_generator_output ______
2026-06-04T05:58:17.7295486Z 
2026-06-04T05:58:17.7295918Z     def test_arch106_committed_inventory_artifact_matches_generator_output() -> None:
2026-06-04T05:58:17.7296659Z         expected = build_inventory()
2026-06-04T05:58:17.7297310Z         actual = json.loads(INVENTORY_ARTIFACT_PATH.read_text(encoding="utf-8"))
2026-06-04T05:58:17.7297938Z     
2026-06-04T05:58:17.7298255Z >       assert actual == expected, (
2026-06-04T05:58:17.7298826Z             "ARCH106 inventory artifact is stale. Regenerate it with: "
2026-06-04T05:58:17.7299796Z             "python scripts/generate_module_inventory.py && "
2026-06-04T05:58:17.7300798Z             "git add docs/architecture/module_inventory.generated.json"
2026-06-04T05:58:17.7301360Z         )
```

```text
2026-06-04T05:58:17.7298826Z             "ARCH106 inventory artifact is stale. Regenerate it with: "
2026-06-04T05:58:17.7299796Z             "python scripts/generate_module_inventory.py && "
2026-06-04T05:58:17.7300798Z             "git add docs/architecture/module_inventory.generated.json"
2026-06-04T05:58:17.7301360Z         )
2026-06-04T05:58:17.7302521Z E       AssertionError: ARCH106 inventory artifact is stale. Regenerate it with: python scripts/generate_module_inventory.py && git add docs/architecture/module_inventory.generated.json
2026-06-04T05:58:17.7303958Z E       assert {'classificat....}, ...], ...} == {'classificat....}, ...], ...}
2026-06-04T05:58:17.7304573Z E         
2026-06-04T05:58:17.7304958Z E         Omitting 4 identical items, use -vv to show
2026-06-04T05:58:17.7305467Z E         Differing items:
2026-06-04T05:58:17.7308281Z E         {'modules': [{'classification': 'experimental', 'notes': 'ARCH106 Step 4a: adaptive expectancy research layer. Not mar... yet classified in ARCH106 Step 3.', 'path': 'src/analytics/explainability.py', 'runtime_entrypoint': None, ...}, ...]} != {'modules': [{'classification': 'experimental', 'notes': 'ARCH106 Step 4a: adaptive expectancy research layer. Not mar... yet classified in ARCH106 Step 3.', 'path': 'src/analytics/explainability.py', 'runtime_entrypoint': None, ...}, ...]}
2026-06-04T05:58:17.7312266Z E         {'counters': {'classified_modules': 7, 'connected_runtime': 5, 'experimental': 2, 'total_src_modules': 313, ...}} != {'counters': {'classified_modules': 11, 'connected_runtime': 5, 'experimental': 6, 'total_src_modules': 313, ...}}
2026-06-04T05:58:17.7313701Z E         
2026-06-04T05:58:17.7314010Z E         Full diff:
2026-06-04T05:58:17.7314350Z E           {
2026-06-04T05:58:17.7314915Z E               'classification_source': 'docs/architecture/module_classification.json',
2026-06-04T05:58:17.7315614Z E               'counters': {
```

```text
2026-06-04T05:58:17.7969464Z E               'schema_version': 1,
2026-06-04T05:58:17.7969610Z E               'source': 'scripts/generate_module_inventory.py',
2026-06-04T05:58:17.7969690Z E           }
2026-06-04T05:58:17.7969702Z 
2026-06-04T05:58:17.7969895Z tests/test_architecture_module_inventory.py:93: AssertionError
2026-06-04T05:58:17.7970038Z =============================== warnings summary ===============================
2026-06-04T05:58:17.7970483Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbol_writes_csv_and_metadata
2026-06-04T05:58:17.7970777Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbol_merges_without_duplicates
2026-06-04T05:58:17.7971073Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbols_batch_counts_results
2026-06-04T05:58:17.7971334Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbols_batch_counts_results
2026-06-04T05:58:17.7972643Z   /home/runner/work/institutional-trading-engine/institutional-trading-engine/src/historical/polygon_ingestion.py:125: FutureWarning: The behavior of DataFrame concatenation with empty or all-NA entries is deprecated. In a future version, this will no longer exclude empty or all-NA columns when determining the result dtypes. To retain the old behavior, exclude the relevant entries before the concat operation.
2026-06-04T05:58:17.7972944Z     combined = pd.concat([existing, df], ignore_index=True)
2026-06-04T05:58:17.7972950Z 
2026-06-04T05:58:17.7973189Z -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2026-06-04T05:58:17.7973346Z =========================== short test summary info ============================
2026-06-04T05:58:17.7974411Z FAILED tests/test_architecture_module_inventory.py::test_arch106_committed_inventory_artifact_matches_generator_output - AssertionError: ARCH106 inventory artifact is stale. Regenerate it with: python scripts/generate_module_inventory.py && git add docs/architecture/module_inventory.generated.json
```

```text
2026-06-04T05:58:17.7972944Z     combined = pd.concat([existing, df], ignore_index=True)
2026-06-04T05:58:17.7972950Z 
2026-06-04T05:58:17.7973189Z -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2026-06-04T05:58:17.7973346Z =========================== short test summary info ============================
2026-06-04T05:58:17.7974411Z FAILED tests/test_architecture_module_inventory.py::test_arch106_committed_inventory_artifact_matches_generator_output - AssertionError: ARCH106 inventory artifact is stale. Regenerate it with: python scripts/generate_module_inventory.py && git add docs/architecture/module_inventory.generated.json
2026-06-04T05:58:17.7974587Z assert {'classificat....}, ...], ...} == {'classificat....}, ...], ...}
2026-06-04T05:58:17.7974679Z   
2026-06-04T05:58:17.7974807Z   Omitting 4 identical items, use -vv to show
2026-06-04T05:58:17.7974892Z   Differing items:
2026-06-04T05:58:17.7976275Z   {'modules': [{'classification': 'experimental', 'notes': 'ARCH106 Step 4a: adaptive expectancy research layer. Not mar... yet classified in ARCH106 Step 3.', 'path': 'src/analytics/explainability.py', 'runtime_entrypoint': None, ...}, ...]} != {'modules': [{'classification': 'experimental', 'notes': 'ARCH106 Step 4a: adaptive expectancy research layer. Not mar... yet classified in ARCH106 Step 3.', 'path': 'src/analytics/explainability.py', 'runtime_entrypoint': None, ...}, ...]}
2026-06-04T05:58:17.7976903Z   {'counters': {'classified_modules': 7, 'connected_runtime': 5, 'experimental': 2, 'total_src_modules': 313, ...}} != {'counters': {'classified_modules': 11, 'connected_runtime': 5, 'experimental': 6, 'total_src_modules': 313, ...}}
2026-06-04T05:58:17.7976988Z   
2026-06-04T05:58:17.7977073Z   Full diff:
2026-06-04T05:58:17.7977150Z     {
2026-06-04T05:58:17.7977362Z         'classification_source': 'docs/architecture/module_classification.json',
2026-06-04T05:58:17.7977449Z         'counters': {
```

```text
2026-06-04T05:58:17.8352365Z         'schema_version': 1,
2026-06-04T05:58:17.8352505Z         'source': 'scripts/generate_module_inventory.py',
2026-06-04T05:58:17.8352590Z     }
2026-06-04T05:58:17.8352740Z 1 failed, 1606 passed, 1 skipped, 4 warnings in 12.13s
2026-06-04T05:58:18.1239752Z ##[error]Process completed with exit code 1.
2026-06-04T05:58:18.1355744Z Post job cleanup.
2026-06-04T05:58:18.2344634Z [command]/usr/bin/git version
2026-06-04T05:58:18.2381300Z git version 2.54.0
2026-06-04T05:58:18.2424531Z Temporarily overriding HOME='/home/runner/work/_temp/32efe3e9-c174-4e82-8b42-341ba80e9382' before making global git config changes
2026-06-04T05:58:18.2430916Z Adding repository directory to the temporary git global config as a safe directory
2026-06-04T05:58:18.2438206Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-06-04T05:58:18.2469134Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-06-04T05:58:18.2504999Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-06-04T05:58:18.2750555Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-06-04T05:58:18.2776048Z http.https://github.com/.extraheader
2026-06-04T05:58:18.2789686Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

## Report Quality Validation

- Run ID: `26933810772`
- Branch: `main`
- Commit: `ce09f9bbbb0f`
- Title: .gitignore aktualisieren
- Created: 2026-06-04T05:57:43Z
- Updated: 2026-06-04T05:58:47Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26933810772

### Failed job: validate-reports (postmarket)

- Job ID: `79458858947`
- Started: 2026-06-04T05:57:47Z
- Completed: 2026-06-04T05:58:46Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-04T05:58:02.9157590Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-04T05:58:02.9157969Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-04T05:58:02.9158582Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-04T05:58:02.9158928Z ##[endgroup]
2026-06-04T05:58:44.5932102Z Traceback (most recent call last):
2026-06-04T05:58:44.5944410Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 264, in <module>
2026-06-04T05:58:44.5946708Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-31/2026-06-04?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-04T05:58:44.5948089Z     raise SystemExit(main())
2026-06-04T05:58:44.5948673Z                      ^^^^^^
2026-06-04T05:58:44.5949598Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 254, in main
2026-06-04T05:58:44.5950752Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-04T05:58:44.5951424Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-04T05:58:44.5952525Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 68, in write_report_text_guarded
2026-06-04T05:58:44.5953651Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-04T05:58:44.5954911Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-06-04T05:58:44.5956028Z     raise ReportOutputBoundaryError(
```

```text
2026-06-04T05:58:44.5956028Z     raise ReportOutputBoundaryError(
2026-06-04T05:58:44.5957506Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/postmarket-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-06-04T05:58:44.5960597Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-31/2026-06-04?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-04T05:58:44.5962715Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-31/2026-06-04?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-04T05:58:44.6631247Z ##[error]Process completed with exit code 1.
2026-06-04T05:58:44.6717646Z ##[group]Run actions/upload-artifact@v4
2026-06-04T05:58:44.6717940Z with:
2026-06-04T05:58:44.6718165Z   name: validated-postmarket-report
2026-06-04T05:58:44.6718736Z   path: reports/postmarket-report.md
2026-06-04T05:58:44.6719011Z   retention-days: 14
2026-06-04T05:58:44.6719241Z   if-no-files-found: warn
2026-06-04T05:58:44.6719481Z   compression-level: 6
2026-06-04T05:58:44.6719928Z   overwrite: false
2026-06-04T05:58:44.6720155Z   include-hidden-files: false
2026-06-04T05:58:44.6720398Z env:
2026-06-04T05:58:44.6720773Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (weekly)

- Job ID: `79458858959`
- Started: 2026-06-04T05:57:46Z
- Completed: 2026-06-04T05:58:07Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-04T05:58:04.6312306Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-04T05:58:04.6312726Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-04T05:58:04.6313182Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-04T05:58:04.6313542Z ##[endgroup]
2026-06-04T05:58:04.9690636Z Traceback (most recent call last):
2026-06-04T05:58:04.9700681Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 264, in <module>
2026-06-04T05:58:04.9701847Z     raise SystemExit(main())
2026-06-04T05:58:04.9702277Z                      ^^^^^^
2026-06-04T05:58:04.9718823Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 254, in main
2026-06-04T05:58:04.9720118Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-04T05:58:04.9720871Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-04T05:58:04.9722138Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 68, in write_report_text_guarded
2026-06-04T05:58:04.9723394Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-04T05:58:04.9724755Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-06-04T05:58:04.9725963Z     raise ReportOutputBoundaryError(
2026-06-04T05:58:04.9727639Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
```

```text
2026-06-04T05:58:04.9723394Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-04T05:58:04.9724755Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-06-04T05:58:04.9725963Z     raise ReportOutputBoundaryError(
2026-06-04T05:58:04.9727639Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-06-04T05:58:04.9953799Z ##[error]Process completed with exit code 1.
2026-06-04T05:58:05.0038946Z ##[group]Run actions/upload-artifact@v4
2026-06-04T05:58:05.0039288Z with:
2026-06-04T05:58:05.0039530Z   name: validated-weekly-report
2026-06-04T05:58:05.0039823Z   path: reports/weekly-report.md
2026-06-04T05:58:05.0040103Z   retention-days: 14
2026-06-04T05:58:05.0040349Z   if-no-files-found: warn
2026-06-04T05:58:05.0040608Z   compression-level: 6
2026-06-04T05:58:05.0040858Z   overwrite: false
2026-06-04T05:58:05.0041102Z   include-hidden-files: false
2026-06-04T05:58:05.0041359Z env:
2026-06-04T05:58:05.0041707Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (premarket)

- Job ID: `79458858968`
- Started: 2026-06-04T05:57:46Z
- Completed: 2026-06-04T05:58:46Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-04T05:58:02.8220788Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-04T05:58:02.8221194Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-04T05:58:02.8221640Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-04T05:58:02.8221989Z ##[endgroup]
2026-06-04T05:58:43.7986450Z Traceback (most recent call last):
2026-06-04T05:58:43.7988419Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-31/2026-06-04?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-04T05:58:43.7997640Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 264, in <module>
2026-06-04T05:58:43.7999028Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-31/2026-06-04?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-04T05:58:43.8000512Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-31/2026-06-04?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-04T05:58:43.8001414Z     raise SystemExit(main())
2026-06-04T05:58:43.8001687Z                      ^^^^^^
2026-06-04T05:58:43.8002331Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 254, in main
2026-06-04T05:58:43.8003095Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-04T05:58:43.8003564Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-04T05:58:43.8004598Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 68, in write_report_text_guarded
2026-06-04T05:58:43.8005381Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
```

```text
2026-06-04T05:58:43.8005381Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-04T05:58:43.8006221Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-06-04T05:58:43.8006959Z     raise ReportOutputBoundaryError(
2026-06-04T05:58:43.8007937Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/premarket-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-06-04T05:58:43.8794687Z ##[error]Process completed with exit code 1.
2026-06-04T05:58:43.8881426Z ##[group]Run actions/upload-artifact@v4
2026-06-04T05:58:43.8881743Z with:
2026-06-04T05:58:43.8881984Z   name: validated-premarket-report
2026-06-04T05:58:43.8882291Z   path: reports/premarket-report.md
2026-06-04T05:58:43.8882568Z   retention-days: 14
2026-06-04T05:58:43.8882810Z   if-no-files-found: warn
2026-06-04T05:58:43.8883071Z   compression-level: 6
2026-06-04T05:58:43.8883523Z   overwrite: false
2026-06-04T05:58:43.8883976Z   include-hidden-files: false
2026-06-04T05:58:43.8884235Z env:
2026-06-04T05:58:43.8884595Z   POLYGON_API_KEY: ***
```

## Decision Engine Tests

- Run ID: `26933751452`
- Branch: `main`
- Commit: `fcb8f38f6b33`
- Title: test_priority_fixes.py aktualisieren
- Created: 2026-06-04T05:56:01Z
- Updated: 2026-06-04T05:56:40Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26933751452

### Failed job: tests

- Job ID: `79458678385`
- Started: 2026-06-04T05:56:05Z
- Completed: 2026-06-04T05:56:39Z
- Failed steps: 5. Run pytest

#### Error context

```text
2026-06-04T05:56:36.1316451Z ........................................................................ [ 89%]
2026-06-04T05:56:36.3462720Z ........................................................................ [ 94%]
2026-06-04T05:56:36.3919104Z ........................................................................ [ 98%]
2026-06-04T05:56:36.4568830Z ........................                                                 [100%]
2026-06-04T05:56:36.4569481Z =================================== FAILURES ===================================
2026-06-04T05:56:36.4570645Z ______ test_arch106_committed_inventory_artifact_matches_generator_output ______
2026-06-04T05:56:36.4571492Z 
2026-06-04T05:56:36.4572142Z     def test_arch106_committed_inventory_artifact_matches_generator_output() -> None:
2026-06-04T05:56:36.4573211Z         expected = build_inventory()
2026-06-04T05:56:36.4573834Z         actual = json.loads(INVENTORY_ARTIFACT_PATH.read_text(encoding="utf-8"))
2026-06-04T05:56:36.4574421Z     
2026-06-04T05:56:36.4574666Z >       assert actual == expected, (
2026-06-04T05:56:36.4575102Z             "ARCH106 inventory artifact is stale. Regenerate it with: "
2026-06-04T05:56:36.4576070Z             "python scripts/generate_module_inventory.py && "
2026-06-04T05:56:36.4576633Z             "git add docs/architecture/module_inventory.generated.json"
2026-06-04T05:56:36.4577069Z         )
```

```text
2026-06-04T05:56:36.4575102Z             "ARCH106 inventory artifact is stale. Regenerate it with: "
2026-06-04T05:56:36.4576070Z             "python scripts/generate_module_inventory.py && "
2026-06-04T05:56:36.4576633Z             "git add docs/architecture/module_inventory.generated.json"
2026-06-04T05:56:36.4577069Z         )
2026-06-04T05:56:36.4577978Z E       AssertionError: ARCH106 inventory artifact is stale. Regenerate it with: python scripts/generate_module_inventory.py && git add docs/architecture/module_inventory.generated.json
2026-06-04T05:56:36.4579165Z E       assert {'classificat....}, ...], ...} == {'classificat....}, ...], ...}
2026-06-04T05:56:36.4580084Z E         
2026-06-04T05:56:36.4580380Z E         Omitting 4 identical items, use -vv to show
2026-06-04T05:56:36.4580766Z E         Differing items:
2026-06-04T05:56:36.4583070Z E         {'modules': [{'classification': 'experimental', 'notes': 'ARCH106 Step 4a: adaptive expectancy research layer. Not mar... yet classified in ARCH106 Step 3.', 'path': 'src/analytics/explainability.py', 'runtime_entrypoint': None, ...}, ...]} != {'modules': [{'classification': 'experimental', 'notes': 'ARCH106 Step 4a: adaptive expectancy research layer. Not mar... yet classified in ARCH106 Step 3.', 'path': 'src/analytics/explainability.py', 'runtime_entrypoint': None, ...}, ...]}
2026-06-04T05:56:36.4586023Z E         {'counters': {'classified_modules': 7, 'connected_runtime': 5, 'experimental': 2, 'total_src_modules': 313, ...}} != {'counters': {'classified_modules': 11, 'connected_runtime': 5, 'experimental': 6, 'total_src_modules': 313, ...}}
2026-06-04T05:56:36.4587163Z E         
2026-06-04T05:56:36.4587347Z E         Full diff:
2026-06-04T05:56:36.4587542Z E           {
2026-06-04T05:56:36.4587864Z E               'classification_source': 'docs/architecture/module_classification.json',
2026-06-04T05:56:36.4588264Z E               'counters': {
```

```text
2026-06-04T05:56:36.5287449Z E               'schema_version': 1,
2026-06-04T05:56:36.5287585Z E               'source': 'scripts/generate_module_inventory.py',
2026-06-04T05:56:36.5287666Z E           }
2026-06-04T05:56:36.5287675Z 
2026-06-04T05:56:36.5287852Z tests/test_architecture_module_inventory.py:93: AssertionError
2026-06-04T05:56:36.5288066Z __________ test_gitignore_blocks_private_edge_and_generated_artifacts __________
2026-06-04T05:56:36.5288077Z 
2026-06-04T05:56:36.5288293Z     def test_gitignore_blocks_private_edge_and_generated_artifacts() -> None:
2026-06-04T05:56:36.5288428Z         content = GITIGNORE.read_text(encoding="utf-8")
2026-06-04T05:56:36.5288505Z     
2026-06-04T05:56:36.5288762Z         missing = [pattern for pattern in REQUIRED_GITIGNORE_PATTERNS if pattern not in content]
2026-06-04T05:56:36.5288838Z     
2026-06-04T05:56:36.5288927Z >       assert missing == []
2026-06-04T05:56:36.5289104Z E       AssertionError: assert ['data/raw/',...ata/private/'] == []
2026-06-04T05:56:36.5289178Z E         
2026-06-04T05:56:36.5289335Z E         Left contains 3 more items, first extra item: 'data/raw/'
```

```text
2026-06-04T05:56:36.5288505Z     
2026-06-04T05:56:36.5288762Z         missing = [pattern for pattern in REQUIRED_GITIGNORE_PATTERNS if pattern not in content]
2026-06-04T05:56:36.5288838Z     
2026-06-04T05:56:36.5288927Z >       assert missing == []
2026-06-04T05:56:36.5289104Z E       AssertionError: assert ['data/raw/',...ata/private/'] == []
2026-06-04T05:56:36.5289178Z E         
2026-06-04T05:56:36.5289335Z E         Left contains 3 more items, first extra item: 'data/raw/'
2026-06-04T05:56:36.5289412Z E         
2026-06-04T05:56:36.5289490Z E         Full diff:
2026-06-04T05:56:36.5289572Z E         - []
2026-06-04T05:56:36.5289644Z E         + [
2026-06-04T05:56:36.5289731Z E         +     'data/raw/',
2026-06-04T05:56:36.5290145Z E         +     'data/live/',
2026-06-04T05:56:36.5290282Z E         +     'data/private/',
2026-06-04T05:56:36.5290355Z E         + ]
2026-06-04T05:56:36.5290361Z
```

```text
2026-06-04T05:56:36.5290145Z E         +     'data/live/',
2026-06-04T05:56:36.5290282Z E         +     'data/private/',
2026-06-04T05:56:36.5290355Z E         + ]
2026-06-04T05:56:36.5290361Z 
2026-06-04T05:56:36.5290496Z tests/test_artifact_hygiene.py:76: AssertionError
2026-06-04T05:56:36.5290641Z =============================== warnings summary ===============================
2026-06-04T05:56:36.5290948Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbol_writes_csv_and_metadata
2026-06-04T05:56:36.5291364Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbol_merges_without_duplicates
2026-06-04T05:56:36.5291635Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbols_batch_counts_results
2026-06-04T05:56:36.5291899Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbols_batch_counts_results
2026-06-04T05:56:36.5293273Z   /home/runner/work/institutional-trading-engine/institutional-trading-engine/src/historical/polygon_ingestion.py:125: FutureWarning: The behavior of DataFrame concatenation with empty or all-NA entries is deprecated. In a future version, this will no longer exclude empty or all-NA columns when determining the result dtypes. To retain the old behavior, exclude the relevant entries before the concat operation.
2026-06-04T05:56:36.5293433Z     combined = pd.concat([existing, df], ignore_index=True)
2026-06-04T05:56:36.5293439Z 
2026-06-04T05:56:36.5293656Z -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2026-06-04T05:56:36.5293809Z =========================== short test summary info ============================
2026-06-04T05:56:36.5294802Z FAILED tests/test_architecture_module_inventory.py::test_arch106_committed_inventory_artifact_matches_generator_output - AssertionError: ARCH106 inventory artifact is stale. Regenerate it with: python scripts/generate_module_inventory.py && git add docs/architecture/module_inventory.generated.json
```

```text
2026-06-04T05:56:36.5293433Z     combined = pd.concat([existing, df], ignore_index=True)
2026-06-04T05:56:36.5293439Z 
2026-06-04T05:56:36.5293656Z -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2026-06-04T05:56:36.5293809Z =========================== short test summary info ============================
2026-06-04T05:56:36.5294802Z FAILED tests/test_architecture_module_inventory.py::test_arch106_committed_inventory_artifact_matches_generator_output - AssertionError: ARCH106 inventory artifact is stale. Regenerate it with: python scripts/generate_module_inventory.py && git add docs/architecture/module_inventory.generated.json
2026-06-04T05:56:36.5294978Z assert {'classificat....}, ...], ...} == {'classificat....}, ...], ...}
2026-06-04T05:56:36.5295057Z   
2026-06-04T05:56:36.5295177Z   Omitting 4 identical items, use -vv to show
2026-06-04T05:56:36.5295257Z   Differing items:
2026-06-04T05:56:36.5296737Z   {'modules': [{'classification': 'experimental', 'notes': 'ARCH106 Step 4a: adaptive expectancy research layer. Not mar... yet classified in ARCH106 Step 3.', 'path': 'src/analytics/explainability.py', 'runtime_entrypoint': None, ...}, ...]} != {'modules': [{'classification': 'experimental', 'notes': 'ARCH106 Step 4a: adaptive expectancy research layer. Not mar... yet classified in ARCH106 Step 3.', 'path': 'src/analytics/explainability.py', 'runtime_entrypoint': None, ...}, ...]}
2026-06-04T05:56:36.5297390Z   {'counters': {'classified_modules': 7, 'connected_runtime': 5, 'experimental': 2, 'total_src_modules': 313, ...}} != {'counters': {'classified_modules': 11, 'connected_runtime': 5, 'experimental': 6, 'total_src_modules': 313, ...}}
2026-06-04T05:56:36.5297459Z   
2026-06-04T05:56:36.5297537Z   Full diff:
2026-06-04T05:56:36.5297611Z     {
2026-06-04T05:56:36.5297823Z         'classification_source': 'docs/architecture/module_classification.json',
2026-06-04T05:56:36.5297903Z         'counters': {
```

```text
2026-06-04T05:56:36.5600917Z         ],
2026-06-04T05:56:36.5601010Z         'schema_version': 1,
2026-06-04T05:56:36.5601146Z         'source': 'scripts/generate_module_inventory.py',
2026-06-04T05:56:36.5601220Z     }
2026-06-04T05:56:36.5601745Z FAILED tests/test_artifact_hygiene.py::test_gitignore_blocks_private_edge_and_generated_artifacts - AssertionError: assert ['data/raw/',...ata/private/'] == []
2026-06-04T05:56:36.5601820Z   
2026-06-04T05:56:36.5601981Z   Left contains 3 more items, first extra item: 'data/raw/'
2026-06-04T05:56:36.5602173Z   
2026-06-04T05:56:36.5602256Z   Full diff:
2026-06-04T05:56:36.5602331Z   - []
2026-06-04T05:56:36.5602399Z   + [
2026-06-04T05:56:36.5602482Z   +     'data/raw/',
2026-06-04T05:56:36.5602562Z   +     'data/live/',
2026-06-04T05:56:36.5602653Z   +     'data/private/',
2026-06-04T05:56:36.5602722Z   + ]
2026-06-04T05:56:36.5602870Z 2 failed, 1605 passed, 1 skipped, 4 warnings in 12.80s
```

```text
2026-06-04T05:56:36.5602562Z   +     'data/live/',
2026-06-04T05:56:36.5602653Z   +     'data/private/',
2026-06-04T05:56:36.5602722Z   + ]
2026-06-04T05:56:36.5602870Z 2 failed, 1605 passed, 1 skipped, 4 warnings in 12.80s
2026-06-04T05:56:36.7253264Z ##[error]Process completed with exit code 1.
2026-06-04T05:56:36.7377239Z Post job cleanup.
2026-06-04T05:56:36.8352179Z [command]/usr/bin/git version
2026-06-04T05:56:36.8387289Z git version 2.54.0
2026-06-04T05:56:36.8429732Z Temporarily overriding HOME='/home/runner/work/_temp/016c72b9-91e1-4ebb-9e0b-e945fa2f3f96' before making global git config changes
2026-06-04T05:56:36.8431298Z Adding repository directory to the temporary git global config as a safe directory
2026-06-04T05:56:36.8442393Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-06-04T05:56:36.8475459Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-06-04T05:56:36.8506838Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-06-04T05:56:36.8737054Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-06-04T05:56:36.8761476Z http.https://github.com/.extraheader
2026-06-04T05:56:36.8773566Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

## CI

- Run ID: `26933751435`
- Branch: `main`
- Commit: `fcb8f38f6b33`
- Title: test_priority_fixes.py aktualisieren
- Created: 2026-06-04T05:56:01Z
- Updated: 2026-06-04T05:56:44Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26933751435

### Failed job: Pytest

- Job ID: `79458678392`
- Started: 2026-06-04T05:56:03Z
- Completed: 2026-06-04T05:56:44Z
- Failed steps: 46. IP5/IP6 artifact hygiene tests

#### Error context

```text
2026-06-04T05:56:42.0083913Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-04T05:56:42.0084257Z   POLYGON_API_KEY: test-key
2026-06-04T05:56:42.0084502Z ##[endgroup]
2026-06-04T05:56:42.2596809Z F.                                                                       [100%]
2026-06-04T05:56:42.2597520Z =================================== FAILURES ===================================
2026-06-04T05:56:42.2598138Z __________ test_gitignore_blocks_private_edge_and_generated_artifacts __________
2026-06-04T05:56:42.2598442Z 
2026-06-04T05:56:42.2598713Z     def test_gitignore_blocks_private_edge_and_generated_artifacts() -> None:
2026-06-04T05:56:42.2599172Z         content = GITIGNORE.read_text(encoding="utf-8")
2026-06-04T05:56:42.2599475Z     
2026-06-04T05:56:42.2599842Z         missing = [pattern for pattern in REQUIRED_GITIGNORE_PATTERNS if pattern not in content]
2026-06-04T05:56:42.2600539Z     
2026-06-04T05:56:42.2600751Z >       assert missing == []
2026-06-04T05:56:42.2601361Z E       AssertionError: assert ['data/raw/',...ata/private/'] == []
2026-06-04T05:56:42.2601720Z E         
2026-06-04T05:56:42.2601996Z E         Left contains 3 more items, first extra item: 'data/raw/'
```

```text
2026-06-04T05:56:42.2599475Z     
2026-06-04T05:56:42.2599842Z         missing = [pattern for pattern in REQUIRED_GITIGNORE_PATTERNS if pattern not in content]
2026-06-04T05:56:42.2600539Z     
2026-06-04T05:56:42.2600751Z >       assert missing == []
2026-06-04T05:56:42.2601361Z E       AssertionError: assert ['data/raw/',...ata/private/'] == []
2026-06-04T05:56:42.2601720Z E         
2026-06-04T05:56:42.2601996Z E         Left contains 3 more items, first extra item: 'data/raw/'
2026-06-04T05:56:42.2602315Z E         
2026-06-04T05:56:42.2602516Z E         Full diff:
2026-06-04T05:56:42.2602750Z E         - []
2026-06-04T05:56:42.2602971Z E         + [
2026-06-04T05:56:42.2603194Z E         +     'data/raw/',
2026-06-04T05:56:42.2603447Z E         +     'data/live/',
2026-06-04T05:56:42.2603701Z E         +     'data/private/',
2026-06-04T05:56:42.2603952Z E         + ]
2026-06-04T05:56:42.2604076Z
```

```text
2026-06-04T05:56:42.2603447Z E         +     'data/live/',
2026-06-04T05:56:42.2603701Z E         +     'data/private/',
2026-06-04T05:56:42.2603952Z E         + ]
2026-06-04T05:56:42.2604076Z 
2026-06-04T05:56:42.2604216Z tests/test_artifact_hygiene.py:76: AssertionError
2026-06-04T05:56:42.2604600Z =========================== short test summary info ============================
2026-06-04T05:56:42.2605473Z FAILED tests/test_artifact_hygiene.py::test_gitignore_blocks_private_edge_and_generated_artifacts - AssertionError: assert ['data/raw/',...ata/private/'] == []
2026-06-04T05:56:42.2606124Z   
2026-06-04T05:56:42.2606397Z   Left contains 3 more items, first extra item: 'data/raw/'
2026-06-04T05:56:42.2606741Z   
2026-06-04T05:56:42.2606931Z   Full diff:
2026-06-04T05:56:42.2607129Z   - []
2026-06-04T05:56:42.2607320Z   + [
2026-06-04T05:56:42.2607514Z   +     'data/raw/',
2026-06-04T05:56:42.2607747Z   +     'data/live/',
2026-06-04T05:56:42.2607978Z   +     'data/private/',
```

```text
2026-06-04T05:56:42.2603952Z E         + ]
2026-06-04T05:56:42.2604076Z 
2026-06-04T05:56:42.2604216Z tests/test_artifact_hygiene.py:76: AssertionError
2026-06-04T05:56:42.2604600Z =========================== short test summary info ============================
2026-06-04T05:56:42.2605473Z FAILED tests/test_artifact_hygiene.py::test_gitignore_blocks_private_edge_and_generated_artifacts - AssertionError: assert ['data/raw/',...ata/private/'] == []
2026-06-04T05:56:42.2606124Z   
2026-06-04T05:56:42.2606397Z   Left contains 3 more items, first extra item: 'data/raw/'
2026-06-04T05:56:42.2606741Z   
2026-06-04T05:56:42.2606931Z   Full diff:
2026-06-04T05:56:42.2607129Z   - []
2026-06-04T05:56:42.2607320Z   + [
2026-06-04T05:56:42.2607514Z   +     'data/raw/',
2026-06-04T05:56:42.2607747Z   +     'data/live/',
2026-06-04T05:56:42.2607978Z   +     'data/private/',
2026-06-04T05:56:42.2608210Z   + ]
2026-06-04T05:56:42.2608415Z 1 failed, 1 passed in 0.05s
```

```text
2026-06-04T05:56:42.2607747Z   +     'data/live/',
2026-06-04T05:56:42.2607978Z   +     'data/private/',
2026-06-04T05:56:42.2608210Z   + ]
2026-06-04T05:56:42.2608415Z 1 failed, 1 passed in 0.05s
2026-06-04T05:56:42.2932288Z ##[error]Process completed with exit code 1.
2026-06-04T05:56:42.3060270Z Post job cleanup.
2026-06-04T05:56:42.4063146Z [command]/usr/bin/git version
2026-06-04T05:56:42.4099821Z git version 2.54.0
2026-06-04T05:56:42.4140308Z Temporarily overriding HOME='/home/runner/work/_temp/0f54bb0e-5ec0-4552-aa04-bb303aeeedb2' before making global git config changes
2026-06-04T05:56:42.4141612Z Adding repository directory to the temporary git global config as a safe directory
2026-06-04T05:56:42.4153682Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-06-04T05:56:42.4189074Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-06-04T05:56:42.4222309Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-06-04T05:56:42.4463828Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-06-04T05:56:42.4491412Z http.https://github.com/.extraheader
2026-06-04T05:56:42.4504022Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

## Report Quality Validation

- Run ID: `26933751433`
- Branch: `main`
- Commit: `fcb8f38f6b33`
- Title: test_priority_fixes.py aktualisieren
- Created: 2026-06-04T05:56:01Z
- Updated: 2026-06-04T05:57:12Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26933751433

### Failed job: validate-reports (weekly)

- Job ID: `79458678693`
- Started: 2026-06-04T05:56:04Z
- Completed: 2026-06-04T05:56:29Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-04T05:56:25.7123709Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-04T05:56:25.7124012Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-04T05:56:25.7124358Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-04T05:56:25.7124619Z ##[endgroup]
2026-06-04T05:56:26.3536594Z Traceback (most recent call last):
2026-06-04T05:56:26.3542742Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 264, in <module>
2026-06-04T05:56:26.3543670Z     raise SystemExit(main())
2026-06-04T05:56:26.3543895Z                      ^^^^^^
2026-06-04T05:56:26.3544396Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 254, in main
2026-06-04T05:56:26.3544997Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-04T05:56:26.3545358Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-04T05:56:26.3545969Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 68, in write_report_text_guarded
2026-06-04T05:56:26.3546590Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-04T05:56:26.3547253Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-06-04T05:56:26.3547831Z     raise ReportOutputBoundaryError(
2026-06-04T05:56:26.3548551Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
```

```text
2026-06-04T05:56:26.3546590Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-04T05:56:26.3547253Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-06-04T05:56:26.3547831Z     raise ReportOutputBoundaryError(
2026-06-04T05:56:26.3548551Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-06-04T05:56:26.3734413Z ##[error]Process completed with exit code 1.
2026-06-04T05:56:26.3799240Z ##[group]Run actions/upload-artifact@v4
2026-06-04T05:56:26.3799500Z with:
2026-06-04T05:56:26.3799691Z   name: validated-weekly-report
2026-06-04T05:56:26.3799919Z   path: reports/weekly-report.md
2026-06-04T05:56:26.3800136Z   retention-days: 14
2026-06-04T05:56:26.3800326Z   if-no-files-found: warn
2026-06-04T05:56:26.3800523Z   compression-level: 6
2026-06-04T05:56:26.3800720Z   overwrite: false
2026-06-04T05:56:26.3800908Z   include-hidden-files: false
2026-06-04T05:56:26.3801119Z env:
2026-06-04T05:56:26.3801441Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (postmarket)

- Job ID: `79458678697`
- Started: 2026-06-04T05:56:04Z
- Completed: 2026-06-04T05:57:10Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-04T05:56:25.4233258Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-04T05:56:25.4233650Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-04T05:56:25.4234106Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-04T05:56:25.4234446Z ##[endgroup]
2026-06-04T05:57:07.9188441Z Traceback (most recent call last):
2026-06-04T05:57:07.9190662Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-31/2026-06-04?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-04T05:57:07.9193812Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-31/2026-06-04?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-04T05:57:07.9195646Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-31/2026-06-04?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-04T05:57:07.9203632Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 264, in <module>
2026-06-04T05:57:07.9204485Z     raise SystemExit(main())
2026-06-04T05:57:07.9204773Z                      ^^^^^^
2026-06-04T05:57:07.9205495Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 254, in main
2026-06-04T05:57:07.9206379Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-04T05:57:07.9206899Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-04T05:57:07.9207809Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 68, in write_report_text_guarded
2026-06-04T05:57:07.9208686Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
```

```text
2026-06-04T05:57:07.9208686Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-04T05:57:07.9209547Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-06-04T05:57:07.9210295Z     raise ReportOutputBoundaryError(
2026-06-04T05:57:07.9211608Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/postmarket-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-06-04T05:57:08.0090746Z ##[error]Process completed with exit code 1.
2026-06-04T05:57:08.0177080Z ##[group]Run actions/upload-artifact@v4
2026-06-04T05:57:08.0177397Z with:
2026-06-04T05:57:08.0177623Z   name: validated-postmarket-report
2026-06-04T05:57:08.0177918Z   path: reports/postmarket-report.md
2026-06-04T05:57:08.0178189Z   retention-days: 14
2026-06-04T05:57:08.0178419Z   if-no-files-found: warn
2026-06-04T05:57:08.0178661Z   compression-level: 6
2026-06-04T05:57:08.0179074Z   overwrite: false
2026-06-04T05:57:08.0179301Z   include-hidden-files: false
2026-06-04T05:57:08.0179540Z env:
2026-06-04T05:57:08.0179855Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (premarket)

- Job ID: `79458678706`
- Started: 2026-06-04T05:56:04Z
- Completed: 2026-06-04T05:57:02Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-04T05:56:20.1520257Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-04T05:56:20.1520668Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-04T05:56:20.1521134Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-04T05:56:20.1521478Z ##[endgroup]
2026-06-04T05:57:00.6050110Z Traceback (most recent call last):
2026-06-04T05:57:00.6051974Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-31/2026-06-04?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-04T05:57:00.6054447Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-31/2026-06-04?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-04T05:57:00.6055957Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-31/2026-06-04?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-04T05:57:00.6063701Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 264, in <module>
2026-06-04T05:57:00.6064437Z     raise SystemExit(main())
2026-06-04T05:57:00.6064718Z                      ^^^^^^
2026-06-04T05:57:00.6065361Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 254, in main
2026-06-04T05:57:00.6066107Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-04T05:57:00.6066565Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-04T05:57:00.6067326Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 68, in write_report_text_guarded
2026-06-04T05:57:00.6068101Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
```

```text
2026-06-04T05:57:00.6068101Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-04T05:57:00.6080306Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-06-04T05:57:00.6090005Z     raise ReportOutputBoundaryError(
2026-06-04T05:57:00.6091240Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/premarket-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-06-04T05:57:00.6819637Z ##[error]Process completed with exit code 1.
2026-06-04T05:57:00.6906818Z ##[group]Run actions/upload-artifact@v4
2026-06-04T05:57:00.6907138Z with:
2026-06-04T05:57:00.6907376Z   name: validated-premarket-report
2026-06-04T05:57:00.6907677Z   path: reports/premarket-report.md
2026-06-04T05:57:00.6907957Z   retention-days: 14
2026-06-04T05:57:00.6908213Z   if-no-files-found: warn
2026-06-04T05:57:00.6908470Z   compression-level: 6
2026-06-04T05:57:00.6908930Z   overwrite: false
2026-06-04T05:57:00.6909417Z   include-hidden-files: false
2026-06-04T05:57:00.6909687Z env:
2026-06-04T05:57:00.6910040Z   POLYGON_API_KEY: ***
```

## Decision Engine Tests

- Run ID: `26933327983`
- Branch: `main`
- Commit: `ba1be4297628`
- Title: P109 keep data subdir ignores without hiding decision log root
- Created: 2026-06-04T05:44:16Z
- Updated: 2026-06-04T05:44:54Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26933327983

### Failed job: tests

- Job ID: `79457399552`
- Started: 2026-06-04T05:44:19Z
- Completed: 2026-06-04T05:44:54Z
- Failed steps: 5. Run pytest

#### Error context

```text
2026-06-04T05:44:50.6020389Z ........................................................................ [ 89%]
2026-06-04T05:44:50.8062334Z ........................................................................ [ 94%]
2026-06-04T05:44:50.8448870Z ........................................................................ [ 98%]
2026-06-04T05:44:50.9055842Z ........................                                                 [100%]
2026-06-04T05:44:50.9056628Z =================================== FAILURES ===================================
2026-06-04T05:44:50.9057426Z ______ test_arch106_committed_inventory_artifact_matches_generator_output ______
2026-06-04T05:44:50.9058305Z 
2026-06-04T05:44:50.9058749Z     def test_arch106_committed_inventory_artifact_matches_generator_output() -> None:
2026-06-04T05:44:50.9059486Z         expected = build_inventory()
2026-06-04T05:44:50.9060133Z         actual = json.loads(INVENTORY_ARTIFACT_PATH.read_text(encoding="utf-8"))
2026-06-04T05:44:50.9060771Z     
2026-06-04T05:44:50.9061085Z >       assert actual == expected, (
2026-06-04T05:44:50.9061658Z             "ARCH106 inventory artifact is stale. Regenerate it with: "
2026-06-04T05:44:50.9062620Z             "python scripts/generate_module_inventory.py && "
2026-06-04T05:44:50.9063308Z             "git add docs/architecture/module_inventory.generated.json"
2026-06-04T05:44:50.9063861Z         )
```

```text
2026-06-04T05:44:50.9061658Z             "ARCH106 inventory artifact is stale. Regenerate it with: "
2026-06-04T05:44:50.9062620Z             "python scripts/generate_module_inventory.py && "
2026-06-04T05:44:50.9063308Z             "git add docs/architecture/module_inventory.generated.json"
2026-06-04T05:44:50.9063861Z         )
2026-06-04T05:44:50.9065026Z E       AssertionError: ARCH106 inventory artifact is stale. Regenerate it with: python scripts/generate_module_inventory.py && git add docs/architecture/module_inventory.generated.json
2026-06-04T05:44:50.9066637Z E       assert {'classificat....}, ...], ...} == {'classificat....}, ...], ...}
2026-06-04T05:44:50.9067258Z E         
2026-06-04T05:44:50.9067646Z E         Omitting 4 identical items, use -vv to show
2026-06-04T05:44:50.9068157Z E         Differing items:
2026-06-04T05:44:50.9070993Z E         {'modules': [{'classification': 'experimental', 'notes': 'ARCH106 Step 4a: adaptive expectancy research layer. Not mar... yet classified in ARCH106 Step 3.', 'path': 'src/analytics/explainability.py', 'runtime_entrypoint': None, ...}, ...]} != {'modules': [{'classification': 'experimental', 'notes': 'ARCH106 Step 4a: adaptive expectancy research layer. Not mar... yet classified in ARCH106 Step 3.', 'path': 'src/analytics/explainability.py', 'runtime_entrypoint': None, ...}, ...]}
2026-06-04T05:44:50.9074904Z E         {'counters': {'classified_modules': 7, 'connected_runtime': 5, 'experimental': 2, 'total_src_modules': 313, ...}} != {'counters': {'classified_modules': 11, 'connected_runtime': 5, 'experimental': 6, 'total_src_modules': 313, ...}}
2026-06-04T05:44:50.9076465Z E         
2026-06-04T05:44:50.9076765Z E         Full diff:
2026-06-04T05:44:50.9077099Z E           {
2026-06-04T05:44:50.9077665Z E               'classification_source': 'docs/architecture/module_classification.json',
2026-06-04T05:44:50.9078371Z E               'counters': {
```

```text
2026-06-04T05:44:50.9789608Z E               'schema_version': 1,
2026-06-04T05:44:50.9789750Z E               'source': 'scripts/generate_module_inventory.py',
2026-06-04T05:44:50.9789829Z E           }
2026-06-04T05:44:50.9789850Z 
2026-06-04T05:44:50.9790034Z tests/test_architecture_module_inventory.py:93: AssertionError
2026-06-04T05:44:50.9790260Z __________ test_gitignore_blocks_private_edge_and_generated_artifacts __________
2026-06-04T05:44:50.9790270Z 
2026-06-04T05:44:50.9790475Z     def test_gitignore_blocks_private_edge_and_generated_artifacts() -> None:
2026-06-04T05:44:50.9790617Z         content = GITIGNORE.read_text(encoding="utf-8")
2026-06-04T05:44:50.9790693Z     
2026-06-04T05:44:50.9790955Z         missing = [pattern for pattern in REQUIRED_GITIGNORE_PATTERNS if pattern not in content]
2026-06-04T05:44:50.9791029Z     
2026-06-04T05:44:50.9791125Z >       assert missing == []
2026-06-04T05:44:50.9791306Z E       AssertionError: assert ['data/raw/',...ata/private/'] == []
2026-06-04T05:44:50.9791383Z E         
2026-06-04T05:44:50.9791541Z E         Left contains 3 more items, first extra item: 'data/raw/'
```

```text
2026-06-04T05:44:50.9790693Z     
2026-06-04T05:44:50.9790955Z         missing = [pattern for pattern in REQUIRED_GITIGNORE_PATTERNS if pattern not in content]
2026-06-04T05:44:50.9791029Z     
2026-06-04T05:44:50.9791125Z >       assert missing == []
2026-06-04T05:44:50.9791306Z E       AssertionError: assert ['data/raw/',...ata/private/'] == []
2026-06-04T05:44:50.9791383Z E         
2026-06-04T05:44:50.9791541Z E         Left contains 3 more items, first extra item: 'data/raw/'
2026-06-04T05:44:50.9791616Z E         
2026-06-04T05:44:50.9791705Z E         Full diff:
2026-06-04T05:44:50.9791787Z E         - []
2026-06-04T05:44:50.9791869Z E         + [
2026-06-04T05:44:50.9791955Z E         +     'data/raw/',
2026-06-04T05:44:50.9792178Z E         +     'data/live/',
2026-06-04T05:44:50.9792272Z E         +     'data/private/',
2026-06-04T05:44:50.9792356Z E         + ]
2026-06-04T05:44:50.9792362Z
```

```text
2026-06-04T05:44:50.9792178Z E         +     'data/live/',
2026-06-04T05:44:50.9792272Z E         +     'data/private/',
2026-06-04T05:44:50.9792356Z E         + ]
2026-06-04T05:44:50.9792362Z 
2026-06-04T05:44:50.9792499Z tests/test_artifact_hygiene.py:76: AssertionError
2026-06-04T05:44:50.9792641Z =============================== warnings summary ===============================
2026-06-04T05:44:50.9792964Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbol_writes_csv_and_metadata
2026-06-04T05:44:50.9793320Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbol_merges_without_duplicates
2026-06-04T05:44:50.9793590Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbols_batch_counts_results
2026-06-04T05:44:50.9793845Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbols_batch_counts_results
2026-06-04T05:44:50.9795142Z   /home/runner/work/institutional-trading-engine/institutional-trading-engine/src/historical/polygon_ingestion.py:125: FutureWarning: The behavior of DataFrame concatenation with empty or all-NA entries is deprecated. In a future version, this will no longer exclude empty or all-NA columns when determining the result dtypes. To retain the old behavior, exclude the relevant entries before the concat operation.
2026-06-04T05:44:50.9795316Z     combined = pd.concat([existing, df], ignore_index=True)
2026-06-04T05:44:50.9795322Z 
2026-06-04T05:44:50.9795540Z -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2026-06-04T05:44:50.9795975Z =========================== short test summary info ============================
2026-06-04T05:44:50.9796927Z FAILED tests/test_architecture_module_inventory.py::test_arch106_committed_inventory_artifact_matches_generator_output - AssertionError: ARCH106 inventory artifact is stale. Regenerate it with: python scripts/generate_module_inventory.py && git add docs/architecture/module_inventory.generated.json
```

```text
2026-06-04T05:44:50.9795316Z     combined = pd.concat([existing, df], ignore_index=True)
2026-06-04T05:44:50.9795322Z 
2026-06-04T05:44:50.9795540Z -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2026-06-04T05:44:50.9795975Z =========================== short test summary info ============================
2026-06-04T05:44:50.9796927Z FAILED tests/test_architecture_module_inventory.py::test_arch106_committed_inventory_artifact_matches_generator_output - AssertionError: ARCH106 inventory artifact is stale. Regenerate it with: python scripts/generate_module_inventory.py && git add docs/architecture/module_inventory.generated.json
2026-06-04T05:44:50.9797100Z assert {'classificat....}, ...], ...} == {'classificat....}, ...], ...}
2026-06-04T05:44:50.9797193Z   
2026-06-04T05:44:50.9797311Z   Omitting 4 identical items, use -vv to show
2026-06-04T05:44:50.9797401Z   Differing items:
2026-06-04T05:44:50.9798800Z   {'modules': [{'classification': 'experimental', 'notes': 'ARCH106 Step 4a: adaptive expectancy research layer. Not mar... yet classified in ARCH106 Step 3.', 'path': 'src/analytics/explainability.py', 'runtime_entrypoint': None, ...}, ...]} != {'modules': [{'classification': 'experimental', 'notes': 'ARCH106 Step 4a: adaptive expectancy research layer. Not mar... yet classified in ARCH106 Step 3.', 'path': 'src/analytics/explainability.py', 'runtime_entrypoint': None, ...}, ...]}
2026-06-04T05:44:50.9799422Z   {'counters': {'classified_modules': 7, 'connected_runtime': 5, 'experimental': 2, 'total_src_modules': 313, ...}} != {'counters': {'classified_modules': 11, 'connected_runtime': 5, 'experimental': 6, 'total_src_modules': 313, ...}}
2026-06-04T05:44:50.9799503Z   
2026-06-04T05:44:50.9799581Z   Full diff:
2026-06-04T05:44:50.9799664Z     {
2026-06-04T05:44:50.9799866Z         'classification_source': 'docs/architecture/module_classification.json',
2026-06-04T05:44:50.9799959Z         'counters': {
```

```text
2026-06-04T05:44:51.0136170Z         ],
2026-06-04T05:44:51.0136277Z         'schema_version': 1,
2026-06-04T05:44:51.0136410Z         'source': 'scripts/generate_module_inventory.py',
2026-06-04T05:44:51.0136495Z     }
2026-06-04T05:44:51.0137014Z FAILED tests/test_artifact_hygiene.py::test_gitignore_blocks_private_edge_and_generated_artifacts - AssertionError: assert ['data/raw/',...ata/private/'] == []
2026-06-04T05:44:51.0137100Z   
2026-06-04T05:44:51.0137259Z   Left contains 3 more items, first extra item: 'data/raw/'
2026-06-04T05:44:51.0137469Z   
2026-06-04T05:44:51.0137549Z   Full diff:
2026-06-04T05:44:51.0137636Z   - []
2026-06-04T05:44:51.0137709Z   + [
2026-06-04T05:44:51.0137802Z   +     'data/raw/',
2026-06-04T05:44:51.0137896Z   +     'data/live/',
2026-06-04T05:44:51.0137985Z   +     'data/private/',
2026-06-04T05:44:51.0138066Z   + ]
2026-06-04T05:44:51.0138215Z 2 failed, 1605 passed, 1 skipped, 4 warnings in 12.44s
```

```text
2026-06-04T05:44:51.0137896Z   +     'data/live/',
2026-06-04T05:44:51.0137985Z   +     'data/private/',
2026-06-04T05:44:51.0138066Z   + ]
2026-06-04T05:44:51.0138215Z 2 failed, 1605 passed, 1 skipped, 4 warnings in 12.44s
2026-06-04T05:44:51.2801201Z ##[error]Process completed with exit code 1.
2026-06-04T05:44:51.2916229Z Post job cleanup.
2026-06-04T05:44:51.3929679Z [command]/usr/bin/git version
2026-06-04T05:44:51.3966816Z git version 2.54.0
2026-06-04T05:44:51.4007722Z Temporarily overriding HOME='/home/runner/work/_temp/6ac1b7f1-4eef-44d9-bacb-0bb1ec782db8' before making global git config changes
2026-06-04T05:44:51.4008842Z Adding repository directory to the temporary git global config as a safe directory
2026-06-04T05:44:51.4020932Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-06-04T05:44:51.4058105Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-06-04T05:44:51.4091431Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-06-04T05:44:51.4334829Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-06-04T05:44:51.4359331Z http.https://github.com/.extraheader
2026-06-04T05:44:51.4373014Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

## CI

- Run ID: `26933327975`
- Branch: `main`
- Commit: `ba1be4297628`
- Title: P109 keep data subdir ignores without hiding decision log root
- Created: 2026-06-04T05:44:16Z
- Updated: 2026-06-04T05:45:01Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26933327975

### Failed job: Pytest

- Job ID: `79457399543`
- Started: 2026-06-04T05:44:19Z
- Completed: 2026-06-04T05:45:00Z
- Failed steps: 46. IP5/IP6 artifact hygiene tests

#### Error context

```text
2026-06-04T05:44:57.7490683Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-04T05:44:57.7491024Z   POLYGON_API_KEY: test-key
2026-06-04T05:44:57.7491256Z ##[endgroup]
2026-06-04T05:44:58.0041991Z F.                                                                       [100%]
2026-06-04T05:44:58.0042921Z =================================== FAILURES ===================================
2026-06-04T05:44:58.0043913Z __________ test_gitignore_blocks_private_edge_and_generated_artifacts __________
2026-06-04T05:44:58.0044880Z 
2026-06-04T05:44:58.0045371Z     def test_gitignore_blocks_private_edge_and_generated_artifacts() -> None:
2026-06-04T05:44:58.0046329Z         content = GITIGNORE.read_text(encoding="utf-8")
2026-06-04T05:44:58.0046880Z     
2026-06-04T05:44:58.0047399Z         missing = [pattern for pattern in REQUIRED_GITIGNORE_PATTERNS if pattern not in content]
2026-06-04T05:44:58.0048293Z     
2026-06-04T05:44:58.0048533Z >       assert missing == []
2026-06-04T05:44:58.0048960Z E       AssertionError: assert ['data/raw/',...ata/private/'] == []
2026-06-04T05:44:58.0049404Z E         
2026-06-04T05:44:58.0049742Z E         Left contains 3 more items, first extra item: 'data/raw/'
```

```text
2026-06-04T05:44:58.0046880Z     
2026-06-04T05:44:58.0047399Z         missing = [pattern for pattern in REQUIRED_GITIGNORE_PATTERNS if pattern not in content]
2026-06-04T05:44:58.0048293Z     
2026-06-04T05:44:58.0048533Z >       assert missing == []
2026-06-04T05:44:58.0048960Z E       AssertionError: assert ['data/raw/',...ata/private/'] == []
2026-06-04T05:44:58.0049404Z E         
2026-06-04T05:44:58.0049742Z E         Left contains 3 more items, first extra item: 'data/raw/'
2026-06-04T05:44:58.0050163Z E         
2026-06-04T05:44:58.0050397Z E         Full diff:
2026-06-04T05:44:58.0050667Z E         - []
2026-06-04T05:44:58.0050914Z E         + [
2026-06-04T05:44:58.0051163Z E         +     'data/raw/',
2026-06-04T05:44:58.0051465Z E         +     'data/live/',
2026-06-04T05:44:58.0051772Z E         +     'data/private/',
2026-06-04T05:44:58.0052076Z E         + ]
2026-06-04T05:44:58.0052222Z
```

```text
2026-06-04T05:44:58.0051465Z E         +     'data/live/',
2026-06-04T05:44:58.0051772Z E         +     'data/private/',
2026-06-04T05:44:58.0052076Z E         + ]
2026-06-04T05:44:58.0052222Z 
2026-06-04T05:44:58.0052387Z tests/test_artifact_hygiene.py:76: AssertionError
2026-06-04T05:44:58.0052866Z =========================== short test summary info ============================
2026-06-04T05:44:58.0053952Z FAILED tests/test_artifact_hygiene.py::test_gitignore_blocks_private_edge_and_generated_artifacts - AssertionError: assert ['data/raw/',...ata/private/'] == []
2026-06-04T05:44:58.0055147Z   
2026-06-04T05:44:58.0055470Z   Left contains 3 more items, first extra item: 'data/raw/'
2026-06-04T05:44:58.0055883Z   
2026-06-04T05:44:58.0056103Z   Full diff:
2026-06-04T05:44:58.0056340Z   - []
2026-06-04T05:44:58.0056574Z   + [
2026-06-04T05:44:58.0056806Z   +     'data/raw/',
2026-06-04T05:44:58.0057082Z   +     'data/live/',
2026-06-04T05:44:58.0057359Z   +     'data/private/',
```

```text
2026-06-04T05:44:58.0052076Z E         + ]
2026-06-04T05:44:58.0052222Z 
2026-06-04T05:44:58.0052387Z tests/test_artifact_hygiene.py:76: AssertionError
2026-06-04T05:44:58.0052866Z =========================== short test summary info ============================
2026-06-04T05:44:58.0053952Z FAILED tests/test_artifact_hygiene.py::test_gitignore_blocks_private_edge_and_generated_artifacts - AssertionError: assert ['data/raw/',...ata/private/'] == []
2026-06-04T05:44:58.0055147Z   
2026-06-04T05:44:58.0055470Z   Left contains 3 more items, first extra item: 'data/raw/'
2026-06-04T05:44:58.0055883Z   
2026-06-04T05:44:58.0056103Z   Full diff:
2026-06-04T05:44:58.0056340Z   - []
2026-06-04T05:44:58.0056574Z   + [
2026-06-04T05:44:58.0056806Z   +     'data/raw/',
2026-06-04T05:44:58.0057082Z   +     'data/live/',
2026-06-04T05:44:58.0057359Z   +     'data/private/',
2026-06-04T05:44:58.0057632Z   + ]
2026-06-04T05:44:58.0057880Z 1 failed, 1 passed in 0.06s
```

```text
2026-06-04T05:44:58.0057082Z   +     'data/live/',
2026-06-04T05:44:58.0057359Z   +     'data/private/',
2026-06-04T05:44:58.0057632Z   + ]
2026-06-04T05:44:58.0057880Z 1 failed, 1 passed in 0.06s
2026-06-04T05:44:58.0307677Z ##[error]Process completed with exit code 1.
2026-06-04T05:44:58.1012271Z Post job cleanup.
2026-06-04T05:44:58.1977684Z [command]/usr/bin/git version
2026-06-04T05:44:58.2012937Z git version 2.54.0
2026-06-04T05:44:58.2055519Z Temporarily overriding HOME='/home/runner/work/_temp/2cd135a0-265c-497c-b9fe-155e1aba8094' before making global git config changes
2026-06-04T05:44:58.2056758Z Adding repository directory to the temporary git global config as a safe directory
2026-06-04T05:44:58.2068747Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-06-04T05:44:58.2102007Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-06-04T05:44:58.2133227Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-06-04T05:44:58.2361879Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-06-04T05:44:58.2384679Z http.https://github.com/.extraheader
2026-06-04T05:44:58.2396777Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

## Report Quality Validation

- Run ID: `26933327982`
- Branch: `main`
- Commit: `ba1be4297628`
- Title: P109 keep data subdir ignores without hiding decision log root
- Created: 2026-06-04T05:44:16Z
- Updated: 2026-06-04T05:45:28Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26933327982

### Failed job: validate-reports (postmarket)

- Job ID: `79457399627`
- Started: 2026-06-04T05:44:19Z
- Completed: 2026-06-04T05:45:21Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-04T05:44:37.5833119Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-04T05:44:37.5833521Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-04T05:44:37.5833929Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-04T05:44:37.5834260Z ##[endgroup]
2026-06-04T05:45:19.4498517Z Traceback (most recent call last):
2026-06-04T05:45:19.4500121Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-31/2026-06-04?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-04T05:45:19.4510058Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 264, in <module>
2026-06-04T05:45:19.4512735Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-31/2026-06-04?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-04T05:45:19.4514576Z     raise SystemExit(main())
2026-06-04T05:45:19.4515243Z                      ^^^^^^
2026-06-04T05:45:19.4516075Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 254, in main
2026-06-04T05:45:19.4517082Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-04T05:45:19.4517655Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-04T05:45:19.4518430Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 68, in write_report_text_guarded
2026-06-04T05:45:19.4519205Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-04T05:45:19.4520034Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
```

```text
2026-06-04T05:45:19.4520034Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-06-04T05:45:19.4520762Z     raise ReportOutputBoundaryError(
2026-06-04T05:45:19.4521708Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/postmarket-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-06-04T05:45:19.4523328Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-31/2026-06-04?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-04T05:45:19.5097512Z ##[error]Process completed with exit code 1.
2026-06-04T05:45:19.5179408Z ##[group]Run actions/upload-artifact@v4
2026-06-04T05:45:19.5179706Z with:
2026-06-04T05:45:19.5179922Z   name: validated-postmarket-report
2026-06-04T05:45:19.5180208Z   path: reports/postmarket-report.md
2026-06-04T05:45:19.5180472Z   retention-days: 14
2026-06-04T05:45:19.5180695Z   if-no-files-found: warn
2026-06-04T05:45:19.5180922Z   compression-level: 6
2026-06-04T05:45:19.5181330Z   overwrite: false
2026-06-04T05:45:19.5181546Z   include-hidden-files: false
2026-06-04T05:45:19.5181780Z env:
2026-06-04T05:45:19.5182114Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (weekly)

- Job ID: `79457399639`
- Started: 2026-06-04T05:44:19Z
- Completed: 2026-06-04T05:44:39Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-04T05:44:37.6167215Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-04T05:44:37.6167619Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-04T05:44:37.6168045Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-04T05:44:37.6168393Z ##[endgroup]
2026-06-04T05:44:37.9328869Z Traceback (most recent call last):
2026-06-04T05:44:37.9337538Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 264, in <module>
2026-06-04T05:44:37.9338635Z     raise SystemExit(main())
2026-06-04T05:44:37.9339017Z                      ^^^^^^
2026-06-04T05:44:37.9339953Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 254, in main
2026-06-04T05:44:37.9341128Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-04T05:44:37.9341796Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-04T05:44:37.9343183Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 68, in write_report_text_guarded
2026-06-04T05:44:37.9344388Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-04T05:44:37.9345716Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-06-04T05:44:37.9346868Z     raise ReportOutputBoundaryError(
2026-06-04T05:44:37.9348325Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
```

```text
2026-06-04T05:44:37.9344388Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-04T05:44:37.9345716Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-06-04T05:44:37.9346868Z     raise ReportOutputBoundaryError(
2026-06-04T05:44:37.9348325Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-06-04T05:44:37.9596653Z ##[error]Process completed with exit code 1.
2026-06-04T05:44:37.9681979Z ##[group]Run actions/upload-artifact@v4
2026-06-04T05:44:37.9682303Z with:
2026-06-04T05:44:37.9682535Z   name: validated-weekly-report
2026-06-04T05:44:37.9682823Z   path: reports/weekly-report.md
2026-06-04T05:44:37.9683361Z   retention-days: 14
2026-06-04T05:44:37.9683607Z   if-no-files-found: warn
2026-06-04T05:44:37.9683864Z   compression-level: 6
2026-06-04T05:44:37.9684109Z   overwrite: false
2026-06-04T05:44:37.9684346Z   include-hidden-files: false
2026-06-04T05:44:37.9684600Z env:
2026-06-04T05:44:37.9684983Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (premarket)

- Job ID: `79457399651`
- Started: 2026-06-04T05:44:19Z
- Completed: 2026-06-04T05:45:27Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-04T05:44:35.4004675Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-04T05:44:35.4005054Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-04T05:44:35.4005493Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-04T05:44:35.4005819Z ##[endgroup]
2026-06-04T05:45:23.7694401Z Traceback (most recent call last):
2026-06-04T05:45:23.7703028Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 264, in <module>
2026-06-04T05:45:23.7704730Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-31/2026-06-04?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-04T05:45:23.7706307Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-31/2026-06-04?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-04T05:45:23.7708142Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-31/2026-06-04?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-04T05:45:23.7709116Z     raise SystemExit(main())
2026-06-04T05:45:23.7709416Z                      ^^^^^^
2026-06-04T05:45:23.7710119Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 254, in main
2026-06-04T05:45:23.7710966Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-04T05:45:23.7711450Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-04T05:45:23.7712167Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 68, in write_report_text_guarded
2026-06-04T05:45:23.7712899Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
```

```text
2026-06-04T05:45:23.7712899Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-04T05:45:23.7713693Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-06-04T05:45:23.7714404Z     raise ReportOutputBoundaryError(
2026-06-04T05:45:23.7715303Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/premarket-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-06-04T05:45:23.8302993Z ##[error]Process completed with exit code 1.
2026-06-04T05:45:23.8379106Z ##[group]Run actions/upload-artifact@v4
2026-06-04T05:45:23.8379403Z with:
2026-06-04T05:45:23.8379635Z   name: validated-premarket-report
2026-06-04T05:45:23.8379925Z   path: reports/premarket-report.md
2026-06-04T05:45:23.8380192Z   retention-days: 14
2026-06-04T05:45:23.8380423Z   if-no-files-found: warn
2026-06-04T05:45:23.8380661Z   compression-level: 6
2026-06-04T05:45:23.8381129Z   overwrite: false
2026-06-04T05:45:23.8381360Z   include-hidden-files: false
2026-06-04T05:45:23.8381605Z env:
2026-06-04T05:45:23.8381920Z   POLYGON_API_KEY: ***
```

## Decision Engine Tests

- Run ID: `26933242467`
- Branch: `main`
- Commit: `22eff9e7b642`
- Title: P109 fix scanner config import for CI runtime
- Created: 2026-06-04T05:41:56Z
- Updated: 2026-06-04T05:42:32Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26933242467

### Failed job: tests

- Job ID: `79457143288`
- Started: 2026-06-04T05:41:59Z
- Completed: 2026-06-04T05:42:31Z
- Failed steps: 5. Run pytest

#### Error context

```text
2026-06-04T05:42:29.4327423Z ........................................................................ [ 89%]
2026-06-04T05:42:29.6542558Z ........................................................................ [ 94%]
2026-06-04T05:42:29.6999584Z ........................................................................ [ 98%]
2026-06-04T05:42:29.7642532Z ........................                                                 [100%]
2026-06-04T05:42:29.7643343Z =================================== FAILURES ===================================
2026-06-04T05:42:29.7644171Z ______ test_arch106_committed_inventory_artifact_matches_generator_output ______
2026-06-04T05:42:29.7645203Z 
2026-06-04T05:42:29.7645795Z     def test_arch106_committed_inventory_artifact_matches_generator_output() -> None:
2026-06-04T05:42:29.7646674Z         expected = build_inventory()
2026-06-04T05:42:29.7647449Z         actual = json.loads(INVENTORY_ARTIFACT_PATH.read_text(encoding="utf-8"))
2026-06-04T05:42:29.7648516Z     
2026-06-04T05:42:29.7649160Z >       assert actual == expected, (
2026-06-04T05:42:29.7649830Z             "ARCH106 inventory artifact is stale. Regenerate it with: "
2026-06-04T05:42:29.7651045Z             "python scripts/generate_module_inventory.py && "
2026-06-04T05:42:29.7651903Z             "git add docs/architecture/module_inventory.generated.json"
2026-06-04T05:42:29.7652623Z         )
```

```text
2026-06-04T05:42:29.7649830Z             "ARCH106 inventory artifact is stale. Regenerate it with: "
2026-06-04T05:42:29.7651045Z             "python scripts/generate_module_inventory.py && "
2026-06-04T05:42:29.7651903Z             "git add docs/architecture/module_inventory.generated.json"
2026-06-04T05:42:29.7652623Z         )
2026-06-04T05:42:29.7654125Z E       AssertionError: ARCH106 inventory artifact is stale. Regenerate it with: python scripts/generate_module_inventory.py && git add docs/architecture/module_inventory.generated.json
2026-06-04T05:42:29.7655628Z E       assert {'classificat....}, ...], ...} == {'classificat....}, ...], ...}
2026-06-04T05:42:29.7656243Z E         
2026-06-04T05:42:29.7656635Z E         Omitting 4 identical items, use -vv to show
2026-06-04T05:42:29.7657152Z E         Differing items:
2026-06-04T05:42:29.7658772Z E         {'counters': {'classified_modules': 7, 'connected_runtime': 5, 'experimental': 2, 'total_src_modules': 313, ...}} != {'counters': {'classified_modules': 11, 'connected_runtime': 5, 'experimental': 6, 'total_src_modules': 313, ...}}
2026-06-04T05:42:29.7662707Z E         {'modules': [{'classification': 'experimental', 'notes': 'ARCH106 Step 4a: adaptive expectancy research layer. Not mar... yet classified in ARCH106 Step 3.', 'path': 'src/analytics/explainability.py', 'runtime_entrypoint': None, ...}, ...]} != {'modules': [{'classification': 'experimental', 'notes': 'ARCH106 Step 4a: adaptive expectancy research layer. Not mar... yet classified in ARCH106 Step 3.', 'path': 'src/analytics/explainability.py', 'runtime_entrypoint': None, ...}, ...]}
2026-06-04T05:42:29.7664381Z E         
2026-06-04T05:42:29.7664569Z E         Full diff:
2026-06-04T05:42:29.7664769Z E           {
2026-06-04T05:42:29.7665113Z E               'classification_source': 'docs/architecture/module_classification.json',
2026-06-04T05:42:29.7665535Z E               'counters': {
```

```text
2026-06-04T05:42:29.8304833Z E               'schema_version': 1,
2026-06-04T05:42:29.8304976Z E               'source': 'scripts/generate_module_inventory.py',
2026-06-04T05:42:29.8305055Z E           }
2026-06-04T05:42:29.8305063Z 
2026-06-04T05:42:29.8305243Z tests/test_architecture_module_inventory.py:93: AssertionError
2026-06-04T05:42:29.8305471Z _________ TestDataPersistence.test_decision_log_path_not_in_gitignore __________
2026-06-04T05:42:29.8305479Z 
2026-06-04T05:42:29.8305683Z self = <test_priority_fixes.TestDataPersistence object at 0x7faae99b4590>
2026-06-04T05:42:29.8305688Z 
2026-06-04T05:42:29.8305818Z     def test_decision_log_path_not_in_gitignore(self):
2026-06-04T05:42:29.8305923Z         gitignore = Path(".gitignore")
2026-06-04T05:42:29.8306016Z         if not gitignore.exists():
2026-06-04T05:42:29.8306092Z             return
2026-06-04T05:42:29.8306189Z         content = gitignore.read_text()
2026-06-04T05:42:29.8306290Z >       assert "data/" not in content, (
2026-06-04T05:42:29.8306690Z             "data/ is in .gitignore â decision log will be lost on every run"
```

```text
2026-06-04T05:42:29.8306189Z         content = gitignore.read_text()
2026-06-04T05:42:29.8306290Z >       assert "data/" not in content, (
2026-06-04T05:42:29.8306690Z             "data/ is in .gitignore â decision log will be lost on every run"
2026-06-04T05:42:29.8306770Z         )
2026-06-04T05:42:29.8307057Z E       AssertionError: data/ is in .gitignore â decision log will be lost on every run
2026-06-04T05:42:29.8307190Z E       assert 'data/' not in '# Python\n_...\n.vscode/\n'
2026-06-04T05:42:29.8307271Z E         
2026-06-04T05:42:29.8307451Z E         'data/' is contained here:
2026-06-04T05:42:29.8307831Z E           e/
2026-06-04T05:42:29.8307915Z E           cache/
2026-06-04T05:42:29.8307996Z E           data/raw/
2026-06-04T05:42:29.8308073Z E           data/live/
2026-06-04T05:42:29.8308162Z E           data/private/
2026-06-04T05:42:29.8308245Z E           data/vendor/
2026-06-04T05:42:29.8308319Z E           evidence/
2026-06-04T05:42:29.8308399Z E           lockbox/
```

```text
2026-06-04T05:42:29.8311503Z E           .DS_Store
2026-06-04T05:42:29.8311580Z E           .idea/
2026-06-04T05:42:29.8311653Z E           .vscode/
2026-06-04T05:42:29.8311659Z 
2026-06-04T05:42:29.8311789Z tests/test_priority_fixes.py:383: AssertionError
2026-06-04T05:42:29.8311940Z =============================== warnings summary ===============================
2026-06-04T05:42:29.8312250Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbol_writes_csv_and_metadata
2026-06-04T05:42:29.8312566Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbol_merges_without_duplicates
2026-06-04T05:42:29.8312838Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbols_batch_counts_results
2026-06-04T05:42:29.8313109Z tests/test_polygon_historical_ingestion.py::test_ingest_historical_symbols_batch_counts_results
2026-06-04T05:42:29.8314476Z   /home/runner/work/institutional-trading-engine/institutional-trading-engine/src/historical/polygon_ingestion.py:125: FutureWarning: The behavior of DataFrame concatenation with empty or all-NA entries is deprecated. In a future version, this will no longer exclude empty or all-NA columns when determining the result dtypes. To retain the old behavior, exclude the relevant entries before the concat operation.
2026-06-04T05:42:29.8314642Z     combined = pd.concat([existing, df], ignore_index=True)
2026-06-04T05:42:29.8314648Z 
2026-06-04T05:42:29.8314869Z -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2026-06-04T05:42:29.8315024Z =========================== short test summary info ============================
2026-06-04T05:42:29.8316025Z FAILED tests/test_architecture_module_inventory.py::test_arch106_committed_inventory_artifact_matches_generator_output - AssertionError: ARCH106 inventory artifact is stale. Regenerate it with: python scripts/generate_module_inventory.py && git add docs/architecture/module_inventory.generated.json
```

```text
2026-06-04T05:42:29.8314642Z     combined = pd.concat([existing, df], ignore_index=True)
2026-06-04T05:42:29.8314648Z 
2026-06-04T05:42:29.8314869Z -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2026-06-04T05:42:29.8315024Z =========================== short test summary info ============================
2026-06-04T05:42:29.8316025Z FAILED tests/test_architecture_module_inventory.py::test_arch106_committed_inventory_artifact_matches_generator_output - AssertionError: ARCH106 inventory artifact is stale. Regenerate it with: python scripts/generate_module_inventory.py && git add docs/architecture/module_inventory.generated.json
2026-06-04T05:42:29.8316323Z assert {'classificat....}, ...], ...} == {'classificat....}, ...], ...}
2026-06-04T05:42:29.8316398Z   
2026-06-04T05:42:29.8316524Z   Omitting 4 identical items, use -vv to show
2026-06-04T05:42:29.8316603Z   Differing items:
2026-06-04T05:42:29.8317345Z   {'counters': {'classified_modules': 7, 'connected_runtime': 5, 'experimental': 2, 'total_src_modules': 313, ...}} != {'counters': {'classified_modules': 11, 'connected_runtime': 5, 'experimental': 6, 'total_src_modules': 313, ...}}
2026-06-04T05:42:29.8319059Z   {'modules': [{'classification': 'experimental', 'notes': 'ARCH106 Step 4a: adaptive expectancy research layer. Not mar... yet classified in ARCH106 Step 3.', 'path': 'src/analytics/explainability.py', 'runtime_entrypoint': None, ...}, ...]} != {'modules': [{'classification': 'experimental', 'notes': 'ARCH106 Step 4a: adaptive expectancy research layer. Not mar... yet classified in ARCH106 Step 3.', 'path': 'src/analytics/explainability.py', 'runtime_entrypoint': None, ...}, ...]}
2026-06-04T05:42:29.8319144Z   
2026-06-04T05:42:29.8319225Z   Full diff:
2026-06-04T05:42:29.8319296Z     {
2026-06-04T05:42:29.8319515Z         'classification_source': 'docs/architecture/module_classification.json',
2026-06-04T05:42:29.8319595Z         'counters': {
```

```text
2026-06-04T05:42:29.8647897Z         ],
2026-06-04T05:42:29.8647991Z         'schema_version': 1,
2026-06-04T05:42:29.8648126Z         'source': 'scripts/generate_module_inventory.py',
2026-06-04T05:42:29.8648255Z     }
2026-06-04T05:42:29.8649143Z FAILED tests/test_priority_fixes.py::TestDataPersistence::test_decision_log_path_not_in_gitignore - AssertionError: data/ is in .gitignore â decision log will be lost on every run
2026-06-04T05:42:29.8649287Z assert 'data/' not in '# Python\n_...\n.vscode/\n'
2026-06-04T05:42:29.8649365Z   
2026-06-04T05:42:29.8649461Z   'data/' is contained here:
2026-06-04T05:42:29.8649532Z     e/
2026-06-04T05:42:29.8649608Z     cache/
2026-06-04T05:42:29.8649681Z     data/raw/
2026-06-04T05:42:29.8649762Z     data/live/
2026-06-04T05:42:29.8649850Z     data/private/
2026-06-04T05:42:29.8649932Z     data/vendor/
2026-06-04T05:42:29.8650005Z     evidence/
2026-06-04T05:42:29.8650081Z     lockbox/
```

```text
2026-06-04T05:42:29.8653174Z     .DS_Store
2026-06-04T05:42:29.8653252Z     .idea/
2026-06-04T05:42:29.8653323Z     .vscode/
2026-06-04T05:42:29.8653473Z 2 failed, 1605 passed, 1 skipped, 4 warnings in 12.10s
2026-06-04T05:42:30.0243028Z ##[error]Process completed with exit code 1.
2026-06-04T05:42:30.0359919Z Post job cleanup.
2026-06-04T05:42:30.1358157Z [command]/usr/bin/git version
2026-06-04T05:42:30.1394616Z git version 2.54.0
2026-06-04T05:42:30.1437316Z Temporarily overriding HOME='/home/runner/work/_temp/e1a51157-5694-4ea0-aa78-0c95826baccb' before making global git config changes
2026-06-04T05:42:30.1438688Z Adding repository directory to the temporary git global config as a safe directory
2026-06-04T05:42:30.1450970Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-06-04T05:42:30.1485721Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-06-04T05:42:30.1518746Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-06-04T05:42:30.1742703Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-06-04T05:42:30.1766057Z http.https://github.com/.extraheader
2026-06-04T05:42:30.1778424Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```
