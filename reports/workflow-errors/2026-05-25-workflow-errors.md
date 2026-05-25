# GitHub Actions Workflow Error Report

Generated: 2026-05-25 08:42 UTC
Repository: `yalcinkadir/institutional-trading-engine`
Filter since: 2026-05-24 08:42 UTC
Failed runs included: 4

## Decision Engine Tests

- Run ID: `26375625937`
- Branch: `main`
- Commit: `da5520129763`
- Title: Merge pull request #70 from yalcinkadir/p69
- Created: 2026-05-24T23:22:05Z
- Updated: 2026-05-24T23:22:30Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26375625937

### Failed job: tests

- Job ID: `77635266512`
- Started: 2026-05-24T23:22:08Z
- Completed: 2026-05-24T23:22:30Z
- Failed steps: 5. Run pytest

#### Error context

```text
2026-05-24T23:22:24.5653524Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-05-24T23:22:24.5653875Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-05-24T23:22:24.5654164Z ##[endgroup]
2026-05-24T23:22:28.8985687Z 
2026-05-24T23:22:28.8986213Z ==================================== ERRORS ====================================
2026-05-24T23:22:28.8987165Z ____ ERROR collecting tests/test_polygon_artifact_consolidation_workflow.py ____
2026-05-24T23:22:28.8988937Z ImportError while importing test module '/home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_polygon_artifact_consolidation_workflow.py'.
2026-05-24T23:22:28.8990252Z Hint: make sure your test modules/packages have valid Python names.
2026-05-24T23:22:28.8990763Z Traceback:
2026-05-24T23:22:28.8991384Z /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/importlib/__init__.py:126: in import_module
2026-05-24T23:22:28.8992181Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-05-24T23:22:28.8992677Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-05-24T23:22:28.8993261Z tests/test_polygon_artifact_consolidation_workflow.py:5: in <module>
2026-05-24T23:22:28.8993780Z     import yaml
2026-05-24T23:22:28.8994096Z E   ModuleNotFoundError: No module named 'yaml'
2026-05-24T23:22:28.8994605Z =========================== short test summary info ============================
```

```text
2026-05-24T23:22:24.5653875Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-05-24T23:22:24.5654164Z ##[endgroup]
2026-05-24T23:22:28.8985687Z 
2026-05-24T23:22:28.8986213Z ==================================== ERRORS ====================================
2026-05-24T23:22:28.8987165Z ____ ERROR collecting tests/test_polygon_artifact_consolidation_workflow.py ____
2026-05-24T23:22:28.8988937Z ImportError while importing test module '/home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_polygon_artifact_consolidation_workflow.py'.
2026-05-24T23:22:28.8990252Z Hint: make sure your test modules/packages have valid Python names.
2026-05-24T23:22:28.8990763Z Traceback:
2026-05-24T23:22:28.8991384Z /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/importlib/__init__.py:126: in import_module
2026-05-24T23:22:28.8992181Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-05-24T23:22:28.8992677Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-05-24T23:22:28.8993261Z tests/test_polygon_artifact_consolidation_workflow.py:5: in <module>
2026-05-24T23:22:28.8993780Z     import yaml
2026-05-24T23:22:28.8994096Z E   ModuleNotFoundError: No module named 'yaml'
2026-05-24T23:22:28.8994605Z =========================== short test summary info ============================
2026-05-24T23:22:28.8995200Z ERROR tests/test_polygon_artifact_consolidation_workflow.py
```

```text
2026-05-24T23:22:24.5654164Z ##[endgroup]
2026-05-24T23:22:28.8985687Z 
2026-05-24T23:22:28.8986213Z ==================================== ERRORS ====================================
2026-05-24T23:22:28.8987165Z ____ ERROR collecting tests/test_polygon_artifact_consolidation_workflow.py ____
2026-05-24T23:22:28.8988937Z ImportError while importing test module '/home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_polygon_artifact_consolidation_workflow.py'.
2026-05-24T23:22:28.8990252Z Hint: make sure your test modules/packages have valid Python names.
2026-05-24T23:22:28.8990763Z Traceback:
2026-05-24T23:22:28.8991384Z /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/importlib/__init__.py:126: in import_module
2026-05-24T23:22:28.8992181Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-05-24T23:22:28.8992677Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-05-24T23:22:28.8993261Z tests/test_polygon_artifact_consolidation_workflow.py:5: in <module>
2026-05-24T23:22:28.8993780Z     import yaml
2026-05-24T23:22:28.8994096Z E   ModuleNotFoundError: No module named 'yaml'
2026-05-24T23:22:28.8994605Z =========================== short test summary info ============================
2026-05-24T23:22:28.8995200Z ERROR tests/test_polygon_artifact_consolidation_workflow.py
2026-05-24T23:22:28.8995794Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
```

```text
2026-05-24T23:22:28.8986213Z ==================================== ERRORS ====================================
2026-05-24T23:22:28.8987165Z ____ ERROR collecting tests/test_polygon_artifact_consolidation_workflow.py ____
2026-05-24T23:22:28.8988937Z ImportError while importing test module '/home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_polygon_artifact_consolidation_workflow.py'.
2026-05-24T23:22:28.8990252Z Hint: make sure your test modules/packages have valid Python names.
2026-05-24T23:22:28.8990763Z Traceback:
2026-05-24T23:22:28.8991384Z /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/importlib/__init__.py:126: in import_module
2026-05-24T23:22:28.8992181Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-05-24T23:22:28.8992677Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-05-24T23:22:28.8993261Z tests/test_polygon_artifact_consolidation_workflow.py:5: in <module>
2026-05-24T23:22:28.8993780Z     import yaml
2026-05-24T23:22:28.8994096Z E   ModuleNotFoundError: No module named 'yaml'
2026-05-24T23:22:28.8994605Z =========================== short test summary info ============================
2026-05-24T23:22:28.8995200Z ERROR tests/test_polygon_artifact_consolidation_workflow.py
2026-05-24T23:22:28.8995794Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-05-24T23:22:28.8996273Z 1 error in 3.42s
2026-05-24T23:22:29.1732900Z ##[error]Process completed with exit code 2.
```

```text
2026-05-24T23:22:28.8992181Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-05-24T23:22:28.8992677Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-05-24T23:22:28.8993261Z tests/test_polygon_artifact_consolidation_workflow.py:5: in <module>
2026-05-24T23:22:28.8993780Z     import yaml
2026-05-24T23:22:28.8994096Z E   ModuleNotFoundError: No module named 'yaml'
2026-05-24T23:22:28.8994605Z =========================== short test summary info ============================
2026-05-24T23:22:28.8995200Z ERROR tests/test_polygon_artifact_consolidation_workflow.py
2026-05-24T23:22:28.8995794Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-05-24T23:22:28.8996273Z 1 error in 3.42s
2026-05-24T23:22:29.1732900Z ##[error]Process completed with exit code 2.
2026-05-24T23:22:29.1846481Z Post job cleanup.
2026-05-24T23:22:29.2864818Z [command]/usr/bin/git version
2026-05-24T23:22:29.2902575Z git version 2.54.0
2026-05-24T23:22:29.2946073Z Temporarily overriding HOME='/home/runner/work/_temp/c4c2e809-25ae-46a8-9fd8-37f0dc3e1fe4' before making global git config changes
2026-05-24T23:22:29.2947266Z Adding repository directory to the temporary git global config as a safe directory
2026-05-24T23:22:29.2962173Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
```

```text
2026-05-24T23:22:28.8993261Z tests/test_polygon_artifact_consolidation_workflow.py:5: in <module>
2026-05-24T23:22:28.8993780Z     import yaml
2026-05-24T23:22:28.8994096Z E   ModuleNotFoundError: No module named 'yaml'
2026-05-24T23:22:28.8994605Z =========================== short test summary info ============================
2026-05-24T23:22:28.8995200Z ERROR tests/test_polygon_artifact_consolidation_workflow.py
2026-05-24T23:22:28.8995794Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-05-24T23:22:28.8996273Z 1 error in 3.42s
2026-05-24T23:22:29.1732900Z ##[error]Process completed with exit code 2.
2026-05-24T23:22:29.1846481Z Post job cleanup.
2026-05-24T23:22:29.2864818Z [command]/usr/bin/git version
2026-05-24T23:22:29.2902575Z git version 2.54.0
2026-05-24T23:22:29.2946073Z Temporarily overriding HOME='/home/runner/work/_temp/c4c2e809-25ae-46a8-9fd8-37f0dc3e1fe4' before making global git config changes
2026-05-24T23:22:29.2947266Z Adding repository directory to the temporary git global config as a safe directory
2026-05-24T23:22:29.2962173Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-05-24T23:22:29.3002790Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-05-24T23:22:29.3040945Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
```

```text
2026-05-24T23:22:28.8994605Z =========================== short test summary info ============================
2026-05-24T23:22:28.8995200Z ERROR tests/test_polygon_artifact_consolidation_workflow.py
2026-05-24T23:22:28.8995794Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-05-24T23:22:28.8996273Z 1 error in 3.42s
2026-05-24T23:22:29.1732900Z ##[error]Process completed with exit code 2.
2026-05-24T23:22:29.1846481Z Post job cleanup.
2026-05-24T23:22:29.2864818Z [command]/usr/bin/git version
2026-05-24T23:22:29.2902575Z git version 2.54.0
2026-05-24T23:22:29.2946073Z Temporarily overriding HOME='/home/runner/work/_temp/c4c2e809-25ae-46a8-9fd8-37f0dc3e1fe4' before making global git config changes
2026-05-24T23:22:29.2947266Z Adding repository directory to the temporary git global config as a safe directory
2026-05-24T23:22:29.2962173Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-05-24T23:22:29.3002790Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-05-24T23:22:29.3040945Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-05-24T23:22:29.3294274Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-05-24T23:22:29.3321063Z http.https://github.com/.extraheader
2026-05-24T23:22:29.3334051Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

## CI

- Run ID: `26375625949`
- Branch: `main`
- Commit: `da5520129763`
- Title: Merge pull request #70 from yalcinkadir/p69
- Created: 2026-05-24T23:22:05Z
- Updated: 2026-05-24T23:22:30Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26375625949

### Failed job: Pytest

- Job ID: `77635266518`
- Started: 2026-05-24T23:22:08Z
- Completed: 2026-05-24T23:22:30Z
- Failed steps: 5. Run tests

#### Error context

```text
2026-05-24T23:22:28.5804787Z rootdir: /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-05-24T23:22:28.5807177Z plugins: anyio-4.13.0
2026-05-24T23:22:28.5807806Z collected 826 items / 1 error
2026-05-24T23:22:28.5808188Z 
2026-05-24T23:22:28.5808374Z ==================================== ERRORS ====================================
2026-05-24T23:22:28.5809002Z ____ ERROR collecting tests/test_polygon_artifact_consolidation_workflow.py ____
2026-05-24T23:22:28.5810221Z ImportError while importing test module '/home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_polygon_artifact_consolidation_workflow.py'.
2026-05-24T23:22:28.5811369Z Hint: make sure your test modules/packages have valid Python names.
2026-05-24T23:22:28.5811826Z Traceback:
2026-05-24T23:22:28.5812340Z /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/importlib/__init__.py:126: in import_module
2026-05-24T23:22:28.5813076Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-05-24T23:22:28.5813542Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-05-24T23:22:28.5814059Z tests/test_polygon_artifact_consolidation_workflow.py:5: in <module>
2026-05-24T23:22:28.5814539Z     import yaml
2026-05-24T23:22:28.5814842Z E   ModuleNotFoundError: No module named 'yaml'
2026-05-24T23:22:28.5815302Z =========================== short test summary info ============================
```

```text
2026-05-24T23:22:28.5807177Z plugins: anyio-4.13.0
2026-05-24T23:22:28.5807806Z collected 826 items / 1 error
2026-05-24T23:22:28.5808188Z 
2026-05-24T23:22:28.5808374Z ==================================== ERRORS ====================================
2026-05-24T23:22:28.5809002Z ____ ERROR collecting tests/test_polygon_artifact_consolidation_workflow.py ____
2026-05-24T23:22:28.5810221Z ImportError while importing test module '/home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_polygon_artifact_consolidation_workflow.py'.
2026-05-24T23:22:28.5811369Z Hint: make sure your test modules/packages have valid Python names.
2026-05-24T23:22:28.5811826Z Traceback:
2026-05-24T23:22:28.5812340Z /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/importlib/__init__.py:126: in import_module
2026-05-24T23:22:28.5813076Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-05-24T23:22:28.5813542Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-05-24T23:22:28.5814059Z tests/test_polygon_artifact_consolidation_workflow.py:5: in <module>
2026-05-24T23:22:28.5814539Z     import yaml
2026-05-24T23:22:28.5814842Z E   ModuleNotFoundError: No module named 'yaml'
2026-05-24T23:22:28.5815302Z =========================== short test summary info ============================
2026-05-24T23:22:28.5815988Z ERROR tests/test_polygon_artifact_consolidation_workflow.py
```

```text
2026-05-24T23:22:28.5807806Z collected 826 items / 1 error
2026-05-24T23:22:28.5808188Z 
2026-05-24T23:22:28.5808374Z ==================================== ERRORS ====================================
2026-05-24T23:22:28.5809002Z ____ ERROR collecting tests/test_polygon_artifact_consolidation_workflow.py ____
2026-05-24T23:22:28.5810221Z ImportError while importing test module '/home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_polygon_artifact_consolidation_workflow.py'.
2026-05-24T23:22:28.5811369Z Hint: make sure your test modules/packages have valid Python names.
2026-05-24T23:22:28.5811826Z Traceback:
2026-05-24T23:22:28.5812340Z /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/importlib/__init__.py:126: in import_module
2026-05-24T23:22:28.5813076Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-05-24T23:22:28.5813542Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-05-24T23:22:28.5814059Z tests/test_polygon_artifact_consolidation_workflow.py:5: in <module>
2026-05-24T23:22:28.5814539Z     import yaml
2026-05-24T23:22:28.5814842Z E   ModuleNotFoundError: No module named 'yaml'
2026-05-24T23:22:28.5815302Z =========================== short test summary info ============================
2026-05-24T23:22:28.5815988Z ERROR tests/test_polygon_artifact_consolidation_workflow.py
2026-05-24T23:22:28.5816523Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
```

```text
2026-05-24T23:22:28.5808374Z ==================================== ERRORS ====================================
2026-05-24T23:22:28.5809002Z ____ ERROR collecting tests/test_polygon_artifact_consolidation_workflow.py ____
2026-05-24T23:22:28.5810221Z ImportError while importing test module '/home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_polygon_artifact_consolidation_workflow.py'.
2026-05-24T23:22:28.5811369Z Hint: make sure your test modules/packages have valid Python names.
2026-05-24T23:22:28.5811826Z Traceback:
2026-05-24T23:22:28.5812340Z /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/importlib/__init__.py:126: in import_module
2026-05-24T23:22:28.5813076Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-05-24T23:22:28.5813542Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-05-24T23:22:28.5814059Z tests/test_polygon_artifact_consolidation_workflow.py:5: in <module>
2026-05-24T23:22:28.5814539Z     import yaml
2026-05-24T23:22:28.5814842Z E   ModuleNotFoundError: No module named 'yaml'
2026-05-24T23:22:28.5815302Z =========================== short test summary info ============================
2026-05-24T23:22:28.5815988Z ERROR tests/test_polygon_artifact_consolidation_workflow.py
2026-05-24T23:22:28.5816523Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-05-24T23:22:28.5817036Z =============================== 1 error in 3.61s ===============================
2026-05-24T23:22:28.8059137Z ##[error]Process completed with exit code 2.
```

```text
2026-05-24T23:22:28.5813076Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-05-24T23:22:28.5813542Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-05-24T23:22:28.5814059Z tests/test_polygon_artifact_consolidation_workflow.py:5: in <module>
2026-05-24T23:22:28.5814539Z     import yaml
2026-05-24T23:22:28.5814842Z E   ModuleNotFoundError: No module named 'yaml'
2026-05-24T23:22:28.5815302Z =========================== short test summary info ============================
2026-05-24T23:22:28.5815988Z ERROR tests/test_polygon_artifact_consolidation_workflow.py
2026-05-24T23:22:28.5816523Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-05-24T23:22:28.5817036Z =============================== 1 error in 3.61s ===============================
2026-05-24T23:22:28.8059137Z ##[error]Process completed with exit code 2.
2026-05-24T23:22:28.8179042Z Post job cleanup.
2026-05-24T23:22:28.9166123Z [command]/usr/bin/git version
2026-05-24T23:22:28.9203769Z git version 2.54.0
2026-05-24T23:22:28.9249123Z Temporarily overriding HOME='/home/runner/work/_temp/9374dc2a-5f6b-4d90-93f0-dbde7187206d' before making global git config changes
2026-05-24T23:22:28.9250560Z Adding repository directory to the temporary git global config as a safe directory
2026-05-24T23:22:28.9263282Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
```

```text
2026-05-24T23:22:28.5814059Z tests/test_polygon_artifact_consolidation_workflow.py:5: in <module>
2026-05-24T23:22:28.5814539Z     import yaml
2026-05-24T23:22:28.5814842Z E   ModuleNotFoundError: No module named 'yaml'
2026-05-24T23:22:28.5815302Z =========================== short test summary info ============================
2026-05-24T23:22:28.5815988Z ERROR tests/test_polygon_artifact_consolidation_workflow.py
2026-05-24T23:22:28.5816523Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-05-24T23:22:28.5817036Z =============================== 1 error in 3.61s ===============================
2026-05-24T23:22:28.8059137Z ##[error]Process completed with exit code 2.
2026-05-24T23:22:28.8179042Z Post job cleanup.
2026-05-24T23:22:28.9166123Z [command]/usr/bin/git version
2026-05-24T23:22:28.9203769Z git version 2.54.0
2026-05-24T23:22:28.9249123Z Temporarily overriding HOME='/home/runner/work/_temp/9374dc2a-5f6b-4d90-93f0-dbde7187206d' before making global git config changes
2026-05-24T23:22:28.9250560Z Adding repository directory to the temporary git global config as a safe directory
2026-05-24T23:22:28.9263282Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-05-24T23:22:28.9301273Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-05-24T23:22:28.9334796Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
```

```text
2026-05-24T23:22:28.5815302Z =========================== short test summary info ============================
2026-05-24T23:22:28.5815988Z ERROR tests/test_polygon_artifact_consolidation_workflow.py
2026-05-24T23:22:28.5816523Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-05-24T23:22:28.5817036Z =============================== 1 error in 3.61s ===============================
2026-05-24T23:22:28.8059137Z ##[error]Process completed with exit code 2.
2026-05-24T23:22:28.8179042Z Post job cleanup.
2026-05-24T23:22:28.9166123Z [command]/usr/bin/git version
2026-05-24T23:22:28.9203769Z git version 2.54.0
2026-05-24T23:22:28.9249123Z Temporarily overriding HOME='/home/runner/work/_temp/9374dc2a-5f6b-4d90-93f0-dbde7187206d' before making global git config changes
2026-05-24T23:22:28.9250560Z Adding repository directory to the temporary git global config as a safe directory
2026-05-24T23:22:28.9263282Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-05-24T23:22:28.9301273Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-05-24T23:22:28.9334796Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-05-24T23:22:28.9567724Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-05-24T23:22:28.9595313Z http.https://github.com/.extraheader
2026-05-24T23:22:28.9608137Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

## Decision Engine Tests

- Run ID: `26375567411`
- Branch: `p69`
- Commit: `21260ff77b66`
- Title: Add Polygon artifact consolidation workflow
- Created: 2026-05-24T23:19:17Z
- Updated: 2026-05-24T23:19:39Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26375567411

### Failed job: tests

- Job ID: `77635109905`
- Started: 2026-05-24T23:19:19Z
- Completed: 2026-05-24T23:19:39Z
- Failed steps: 5. Run pytest

#### Error context

```text
2026-05-24T23:19:34.2937006Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-05-24T23:19:34.2937357Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-05-24T23:19:34.2937657Z ##[endgroup]
2026-05-24T23:19:37.7836542Z 
2026-05-24T23:19:37.7837072Z ==================================== ERRORS ====================================
2026-05-24T23:19:37.7837687Z ____ ERROR collecting tests/test_polygon_artifact_consolidation_workflow.py ____
2026-05-24T23:19:37.7838544Z ImportError while importing test module '/home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_polygon_artifact_consolidation_workflow.py'.
2026-05-24T23:19:37.7839342Z Hint: make sure your test modules/packages have valid Python names.
2026-05-24T23:19:37.7839700Z Traceback:
2026-05-24T23:19:37.7840070Z /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/importlib/__init__.py:126: in import_module
2026-05-24T23:19:37.7840579Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-05-24T23:19:37.7840903Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-05-24T23:19:37.7841267Z tests/test_polygon_artifact_consolidation_workflow.py:5: in <module>
2026-05-24T23:19:37.7841597Z     import yaml
2026-05-24T23:19:37.7841805Z E   ModuleNotFoundError: No module named 'yaml'
2026-05-24T23:19:37.7842125Z =========================== short test summary info ============================
```

```text
2026-05-24T23:19:34.2937357Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-05-24T23:19:34.2937657Z ##[endgroup]
2026-05-24T23:19:37.7836542Z 
2026-05-24T23:19:37.7837072Z ==================================== ERRORS ====================================
2026-05-24T23:19:37.7837687Z ____ ERROR collecting tests/test_polygon_artifact_consolidation_workflow.py ____
2026-05-24T23:19:37.7838544Z ImportError while importing test module '/home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_polygon_artifact_consolidation_workflow.py'.
2026-05-24T23:19:37.7839342Z Hint: make sure your test modules/packages have valid Python names.
2026-05-24T23:19:37.7839700Z Traceback:
2026-05-24T23:19:37.7840070Z /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/importlib/__init__.py:126: in import_module
2026-05-24T23:19:37.7840579Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-05-24T23:19:37.7840903Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-05-24T23:19:37.7841267Z tests/test_polygon_artifact_consolidation_workflow.py:5: in <module>
2026-05-24T23:19:37.7841597Z     import yaml
2026-05-24T23:19:37.7841805Z E   ModuleNotFoundError: No module named 'yaml'
2026-05-24T23:19:37.7842125Z =========================== short test summary info ============================
2026-05-24T23:19:37.7842493Z ERROR tests/test_polygon_artifact_consolidation_workflow.py
```

```text
2026-05-24T23:19:34.2937657Z ##[endgroup]
2026-05-24T23:19:37.7836542Z 
2026-05-24T23:19:37.7837072Z ==================================== ERRORS ====================================
2026-05-24T23:19:37.7837687Z ____ ERROR collecting tests/test_polygon_artifact_consolidation_workflow.py ____
2026-05-24T23:19:37.7838544Z ImportError while importing test module '/home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_polygon_artifact_consolidation_workflow.py'.
2026-05-24T23:19:37.7839342Z Hint: make sure your test modules/packages have valid Python names.
2026-05-24T23:19:37.7839700Z Traceback:
2026-05-24T23:19:37.7840070Z /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/importlib/__init__.py:126: in import_module
2026-05-24T23:19:37.7840579Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-05-24T23:19:37.7840903Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-05-24T23:19:37.7841267Z tests/test_polygon_artifact_consolidation_workflow.py:5: in <module>
2026-05-24T23:19:37.7841597Z     import yaml
2026-05-24T23:19:37.7841805Z E   ModuleNotFoundError: No module named 'yaml'
2026-05-24T23:19:37.7842125Z =========================== short test summary info ============================
2026-05-24T23:19:37.7842493Z ERROR tests/test_polygon_artifact_consolidation_workflow.py
2026-05-24T23:19:37.7843079Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
```

```text
2026-05-24T23:19:37.7837072Z ==================================== ERRORS ====================================
2026-05-24T23:19:37.7837687Z ____ ERROR collecting tests/test_polygon_artifact_consolidation_workflow.py ____
2026-05-24T23:19:37.7838544Z ImportError while importing test module '/home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_polygon_artifact_consolidation_workflow.py'.
2026-05-24T23:19:37.7839342Z Hint: make sure your test modules/packages have valid Python names.
2026-05-24T23:19:37.7839700Z Traceback:
2026-05-24T23:19:37.7840070Z /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/importlib/__init__.py:126: in import_module
2026-05-24T23:19:37.7840579Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-05-24T23:19:37.7840903Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-05-24T23:19:37.7841267Z tests/test_polygon_artifact_consolidation_workflow.py:5: in <module>
2026-05-24T23:19:37.7841597Z     import yaml
2026-05-24T23:19:37.7841805Z E   ModuleNotFoundError: No module named 'yaml'
2026-05-24T23:19:37.7842125Z =========================== short test summary info ============================
2026-05-24T23:19:37.7842493Z ERROR tests/test_polygon_artifact_consolidation_workflow.py
2026-05-24T23:19:37.7843079Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-05-24T23:19:37.7843385Z 1 error in 2.73s
2026-05-24T23:19:37.9411438Z ##[error]Process completed with exit code 2.
```

```text
2026-05-24T23:19:37.7840579Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-05-24T23:19:37.7840903Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-05-24T23:19:37.7841267Z tests/test_polygon_artifact_consolidation_workflow.py:5: in <module>
2026-05-24T23:19:37.7841597Z     import yaml
2026-05-24T23:19:37.7841805Z E   ModuleNotFoundError: No module named 'yaml'
2026-05-24T23:19:37.7842125Z =========================== short test summary info ============================
2026-05-24T23:19:37.7842493Z ERROR tests/test_polygon_artifact_consolidation_workflow.py
2026-05-24T23:19:37.7843079Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-05-24T23:19:37.7843385Z 1 error in 2.73s
2026-05-24T23:19:37.9411438Z ##[error]Process completed with exit code 2.
2026-05-24T23:19:37.9517177Z Post job cleanup.
2026-05-24T23:19:38.0503605Z [command]/usr/bin/git version
2026-05-24T23:19:38.0539245Z git version 2.54.0
2026-05-24T23:19:38.0586562Z Temporarily overriding HOME='/home/runner/work/_temp/a2b9613b-a313-4e02-95e6-dd7587963708' before making global git config changes
2026-05-24T23:19:38.0587658Z Adding repository directory to the temporary git global config as a safe directory
2026-05-24T23:19:38.0592072Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
```

```text
2026-05-24T23:19:37.7841267Z tests/test_polygon_artifact_consolidation_workflow.py:5: in <module>
2026-05-24T23:19:37.7841597Z     import yaml
2026-05-24T23:19:37.7841805Z E   ModuleNotFoundError: No module named 'yaml'
2026-05-24T23:19:37.7842125Z =========================== short test summary info ============================
2026-05-24T23:19:37.7842493Z ERROR tests/test_polygon_artifact_consolidation_workflow.py
2026-05-24T23:19:37.7843079Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-05-24T23:19:37.7843385Z 1 error in 2.73s
2026-05-24T23:19:37.9411438Z ##[error]Process completed with exit code 2.
2026-05-24T23:19:37.9517177Z Post job cleanup.
2026-05-24T23:19:38.0503605Z [command]/usr/bin/git version
2026-05-24T23:19:38.0539245Z git version 2.54.0
2026-05-24T23:19:38.0586562Z Temporarily overriding HOME='/home/runner/work/_temp/a2b9613b-a313-4e02-95e6-dd7587963708' before making global git config changes
2026-05-24T23:19:38.0587658Z Adding repository directory to the temporary git global config as a safe directory
2026-05-24T23:19:38.0592072Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-05-24T23:19:38.0627862Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-05-24T23:19:38.0661166Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
```

```text
2026-05-24T23:19:37.7842125Z =========================== short test summary info ============================
2026-05-24T23:19:37.7842493Z ERROR tests/test_polygon_artifact_consolidation_workflow.py
2026-05-24T23:19:37.7843079Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-05-24T23:19:37.7843385Z 1 error in 2.73s
2026-05-24T23:19:37.9411438Z ##[error]Process completed with exit code 2.
2026-05-24T23:19:37.9517177Z Post job cleanup.
2026-05-24T23:19:38.0503605Z [command]/usr/bin/git version
2026-05-24T23:19:38.0539245Z git version 2.54.0
2026-05-24T23:19:38.0586562Z Temporarily overriding HOME='/home/runner/work/_temp/a2b9613b-a313-4e02-95e6-dd7587963708' before making global git config changes
2026-05-24T23:19:38.0587658Z Adding repository directory to the temporary git global config as a safe directory
2026-05-24T23:19:38.0592072Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-05-24T23:19:38.0627862Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-05-24T23:19:38.0661166Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-05-24T23:19:38.0900195Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-05-24T23:19:38.0925802Z http.https://github.com/.extraheader
2026-05-24T23:19:38.0938024Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

## CI

- Run ID: `26375567402`
- Branch: `p69`
- Commit: `21260ff77b66`
- Title: Add Polygon artifact consolidation workflow
- Created: 2026-05-24T23:19:17Z
- Updated: 2026-05-24T23:19:42Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26375567402

### Failed job: Pytest

- Job ID: `77635109863`
- Started: 2026-05-24T23:19:19Z
- Completed: 2026-05-24T23:19:41Z
- Failed steps: 5. Run tests

#### Error context

```text
2026-05-24T23:19:40.3693695Z rootdir: /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-05-24T23:19:40.3694384Z plugins: anyio-4.13.0
2026-05-24T23:19:40.3694709Z collected 826 items / 1 error
2026-05-24T23:19:40.3694939Z 
2026-05-24T23:19:40.3695117Z ==================================== ERRORS ====================================
2026-05-24T23:19:40.3695763Z ____ ERROR collecting tests/test_polygon_artifact_consolidation_workflow.py ____
2026-05-24T23:19:40.3697115Z ImportError while importing test module '/home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_polygon_artifact_consolidation_workflow.py'.
2026-05-24T23:19:40.3698434Z Hint: make sure your test modules/packages have valid Python names.
2026-05-24T23:19:40.3698947Z Traceback:
2026-05-24T23:19:40.3699497Z /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/importlib/__init__.py:126: in import_module
2026-05-24T23:19:40.3700303Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-05-24T23:19:40.3700816Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-05-24T23:19:40.3701381Z tests/test_polygon_artifact_consolidation_workflow.py:5: in <module>
2026-05-24T23:19:40.3702142Z     import yaml
2026-05-24T23:19:40.3702463Z E   ModuleNotFoundError: No module named 'yaml'
2026-05-24T23:19:40.3702974Z =========================== short test summary info ============================
```

```text
2026-05-24T23:19:40.3694384Z plugins: anyio-4.13.0
2026-05-24T23:19:40.3694709Z collected 826 items / 1 error
2026-05-24T23:19:40.3694939Z 
2026-05-24T23:19:40.3695117Z ==================================== ERRORS ====================================
2026-05-24T23:19:40.3695763Z ____ ERROR collecting tests/test_polygon_artifact_consolidation_workflow.py ____
2026-05-24T23:19:40.3697115Z ImportError while importing test module '/home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_polygon_artifact_consolidation_workflow.py'.
2026-05-24T23:19:40.3698434Z Hint: make sure your test modules/packages have valid Python names.
2026-05-24T23:19:40.3698947Z Traceback:
2026-05-24T23:19:40.3699497Z /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/importlib/__init__.py:126: in import_module
2026-05-24T23:19:40.3700303Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-05-24T23:19:40.3700816Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-05-24T23:19:40.3701381Z tests/test_polygon_artifact_consolidation_workflow.py:5: in <module>
2026-05-24T23:19:40.3702142Z     import yaml
2026-05-24T23:19:40.3702463Z E   ModuleNotFoundError: No module named 'yaml'
2026-05-24T23:19:40.3702974Z =========================== short test summary info ============================
2026-05-24T23:19:40.3703559Z ERROR tests/test_polygon_artifact_consolidation_workflow.py
```

```text
2026-05-24T23:19:40.3694709Z collected 826 items / 1 error
2026-05-24T23:19:40.3694939Z 
2026-05-24T23:19:40.3695117Z ==================================== ERRORS ====================================
2026-05-24T23:19:40.3695763Z ____ ERROR collecting tests/test_polygon_artifact_consolidation_workflow.py ____
2026-05-24T23:19:40.3697115Z ImportError while importing test module '/home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_polygon_artifact_consolidation_workflow.py'.
2026-05-24T23:19:40.3698434Z Hint: make sure your test modules/packages have valid Python names.
2026-05-24T23:19:40.3698947Z Traceback:
2026-05-24T23:19:40.3699497Z /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/importlib/__init__.py:126: in import_module
2026-05-24T23:19:40.3700303Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-05-24T23:19:40.3700816Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-05-24T23:19:40.3701381Z tests/test_polygon_artifact_consolidation_workflow.py:5: in <module>
2026-05-24T23:19:40.3702142Z     import yaml
2026-05-24T23:19:40.3702463Z E   ModuleNotFoundError: No module named 'yaml'
2026-05-24T23:19:40.3702974Z =========================== short test summary info ============================
2026-05-24T23:19:40.3703559Z ERROR tests/test_polygon_artifact_consolidation_workflow.py
2026-05-24T23:19:40.3704162Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
```

```text
2026-05-24T23:19:40.3695117Z ==================================== ERRORS ====================================
2026-05-24T23:19:40.3695763Z ____ ERROR collecting tests/test_polygon_artifact_consolidation_workflow.py ____
2026-05-24T23:19:40.3697115Z ImportError while importing test module '/home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_polygon_artifact_consolidation_workflow.py'.
2026-05-24T23:19:40.3698434Z Hint: make sure your test modules/packages have valid Python names.
2026-05-24T23:19:40.3698947Z Traceback:
2026-05-24T23:19:40.3699497Z /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/importlib/__init__.py:126: in import_module
2026-05-24T23:19:40.3700303Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-05-24T23:19:40.3700816Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-05-24T23:19:40.3701381Z tests/test_polygon_artifact_consolidation_workflow.py:5: in <module>
2026-05-24T23:19:40.3702142Z     import yaml
2026-05-24T23:19:40.3702463Z E   ModuleNotFoundError: No module named 'yaml'
2026-05-24T23:19:40.3702974Z =========================== short test summary info ============================
2026-05-24T23:19:40.3703559Z ERROR tests/test_polygon_artifact_consolidation_workflow.py
2026-05-24T23:19:40.3704162Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-05-24T23:19:40.3704741Z =============================== 1 error in 3.40s ===============================
2026-05-24T23:19:40.5284746Z ##[error]Process completed with exit code 2.
```

```text
2026-05-24T23:19:40.3700303Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-05-24T23:19:40.3700816Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-05-24T23:19:40.3701381Z tests/test_polygon_artifact_consolidation_workflow.py:5: in <module>
2026-05-24T23:19:40.3702142Z     import yaml
2026-05-24T23:19:40.3702463Z E   ModuleNotFoundError: No module named 'yaml'
2026-05-24T23:19:40.3702974Z =========================== short test summary info ============================
2026-05-24T23:19:40.3703559Z ERROR tests/test_polygon_artifact_consolidation_workflow.py
2026-05-24T23:19:40.3704162Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-05-24T23:19:40.3704741Z =============================== 1 error in 3.40s ===============================
2026-05-24T23:19:40.5284746Z ##[error]Process completed with exit code 2.
2026-05-24T23:19:40.5401930Z Post job cleanup.
2026-05-24T23:19:40.6381867Z [command]/usr/bin/git version
2026-05-24T23:19:40.6425435Z git version 2.54.0
2026-05-24T23:19:40.6470414Z Temporarily overriding HOME='/home/runner/work/_temp/2ceae7f0-56df-4699-b88e-991a4520a29b' before making global git config changes
2026-05-24T23:19:40.6472358Z Adding repository directory to the temporary git global config as a safe directory
2026-05-24T23:19:40.6477514Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
```

```text
2026-05-24T23:19:40.3701381Z tests/test_polygon_artifact_consolidation_workflow.py:5: in <module>
2026-05-24T23:19:40.3702142Z     import yaml
2026-05-24T23:19:40.3702463Z E   ModuleNotFoundError: No module named 'yaml'
2026-05-24T23:19:40.3702974Z =========================== short test summary info ============================
2026-05-24T23:19:40.3703559Z ERROR tests/test_polygon_artifact_consolidation_workflow.py
2026-05-24T23:19:40.3704162Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-05-24T23:19:40.3704741Z =============================== 1 error in 3.40s ===============================
2026-05-24T23:19:40.5284746Z ##[error]Process completed with exit code 2.
2026-05-24T23:19:40.5401930Z Post job cleanup.
2026-05-24T23:19:40.6381867Z [command]/usr/bin/git version
2026-05-24T23:19:40.6425435Z git version 2.54.0
2026-05-24T23:19:40.6470414Z Temporarily overriding HOME='/home/runner/work/_temp/2ceae7f0-56df-4699-b88e-991a4520a29b' before making global git config changes
2026-05-24T23:19:40.6472358Z Adding repository directory to the temporary git global config as a safe directory
2026-05-24T23:19:40.6477514Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-05-24T23:19:40.6513163Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-05-24T23:19:40.6545524Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
```

```text
2026-05-24T23:19:40.3702974Z =========================== short test summary info ============================
2026-05-24T23:19:40.3703559Z ERROR tests/test_polygon_artifact_consolidation_workflow.py
2026-05-24T23:19:40.3704162Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-05-24T23:19:40.3704741Z =============================== 1 error in 3.40s ===============================
2026-05-24T23:19:40.5284746Z ##[error]Process completed with exit code 2.
2026-05-24T23:19:40.5401930Z Post job cleanup.
2026-05-24T23:19:40.6381867Z [command]/usr/bin/git version
2026-05-24T23:19:40.6425435Z git version 2.54.0
2026-05-24T23:19:40.6470414Z Temporarily overriding HOME='/home/runner/work/_temp/2ceae7f0-56df-4699-b88e-991a4520a29b' before making global git config changes
2026-05-24T23:19:40.6472358Z Adding repository directory to the temporary git global config as a safe directory
2026-05-24T23:19:40.6477514Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-05-24T23:19:40.6513163Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-05-24T23:19:40.6545524Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-05-24T23:19:40.6769195Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-05-24T23:19:40.6793054Z http.https://github.com/.extraheader
2026-05-24T23:19:40.6805939Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```
