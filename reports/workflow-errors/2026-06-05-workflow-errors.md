# GitHub Actions Workflow Error Report

Generated: 2026-06-05 08:33 UTC
Repository: `yalcinkadir/institutional-trading-engine`
Filter since: 2026-06-04 08:33 UTC
Failed runs included: 7

## CI

- Run ID: `27004258306`
- Branch: `main`
- Commit: `fbef34dcead8`
- Title: P120 add paper observation evidence schema guard
- Created: 2026-06-05T08:27:09Z
- Updated: 2026-06-05T08:27:57Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27004258306

### Failed job: Pytest

- Job ID: `79691819711`
- Started: 2026-06-05T08:27:12Z
- Completed: 2026-06-05T08:27:56Z
- Failed steps: 53. Full regression suite residual tests

#### Error context

```text
2026-06-05T08:27:49.7689643Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-05T08:27:49.7690336Z   POLYGON_API_KEY: test-key
2026-06-05T08:27:49.7690859Z ##[endgroup]
2026-06-05T08:27:53.8221806Z 
2026-06-05T08:27:53.8222634Z ==================================== ERRORS ====================================
2026-06-05T08:27:53.8223440Z _____ ERROR collecting tests/test_p120_paper_observation_evidence_gate.py ______
2026-06-05T08:27:53.8224963Z ImportError while importing test module '/home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_p120_paper_observation_evidence_gate.py'.
2026-06-05T08:27:53.8225953Z Hint: make sure your test modules/packages have valid Python names.
2026-06-05T08:27:53.8226361Z Traceback:
2026-06-05T08:27:53.8226803Z /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/importlib/__init__.py:126: in import_module
2026-06-05T08:27:53.8227429Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-06-05T08:27:53.8227918Z tests/test_p120_paper_observation_evidence_gate.py:7: in <module>
2026-06-05T08:27:53.8228582Z     from src.operations.paper_observation_evidence_gate import validate_paper_observation_evidence_artifact
2026-06-05T08:27:53.8229584Z E   ModuleNotFoundError: No module named 'src.operations.paper_observation_evidence_gate'
2026-06-05T08:27:53.8230168Z =========================== short test summary info ============================
2026-06-05T08:27:53.8230623Z ERROR tests/test_p120_paper_observation_evidence_gate.py
```

```text
2026-06-05T08:27:49.7690336Z   POLYGON_API_KEY: test-key
2026-06-05T08:27:49.7690859Z ##[endgroup]
2026-06-05T08:27:53.8221806Z 
2026-06-05T08:27:53.8222634Z ==================================== ERRORS ====================================
2026-06-05T08:27:53.8223440Z _____ ERROR collecting tests/test_p120_paper_observation_evidence_gate.py ______
2026-06-05T08:27:53.8224963Z ImportError while importing test module '/home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_p120_paper_observation_evidence_gate.py'.
2026-06-05T08:27:53.8225953Z Hint: make sure your test modules/packages have valid Python names.
2026-06-05T08:27:53.8226361Z Traceback:
2026-06-05T08:27:53.8226803Z /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/importlib/__init__.py:126: in import_module
2026-06-05T08:27:53.8227429Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-06-05T08:27:53.8227918Z tests/test_p120_paper_observation_evidence_gate.py:7: in <module>
2026-06-05T08:27:53.8228582Z     from src.operations.paper_observation_evidence_gate import validate_paper_observation_evidence_artifact
2026-06-05T08:27:53.8229584Z E   ModuleNotFoundError: No module named 'src.operations.paper_observation_evidence_gate'
2026-06-05T08:27:53.8230168Z =========================== short test summary info ============================
2026-06-05T08:27:53.8230623Z ERROR tests/test_p120_paper_observation_evidence_gate.py
2026-06-05T08:27:53.8231083Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
```

```text
2026-06-05T08:27:49.7690859Z ##[endgroup]
2026-06-05T08:27:53.8221806Z 
2026-06-05T08:27:53.8222634Z ==================================== ERRORS ====================================
2026-06-05T08:27:53.8223440Z _____ ERROR collecting tests/test_p120_paper_observation_evidence_gate.py ______
2026-06-05T08:27:53.8224963Z ImportError while importing test module '/home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_p120_paper_observation_evidence_gate.py'.
2026-06-05T08:27:53.8225953Z Hint: make sure your test modules/packages have valid Python names.
2026-06-05T08:27:53.8226361Z Traceback:
2026-06-05T08:27:53.8226803Z /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/importlib/__init__.py:126: in import_module
2026-06-05T08:27:53.8227429Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-06-05T08:27:53.8227918Z tests/test_p120_paper_observation_evidence_gate.py:7: in <module>
2026-06-05T08:27:53.8228582Z     from src.operations.paper_observation_evidence_gate import validate_paper_observation_evidence_artifact
2026-06-05T08:27:53.8229584Z E   ModuleNotFoundError: No module named 'src.operations.paper_observation_evidence_gate'
2026-06-05T08:27:53.8230168Z =========================== short test summary info ============================
2026-06-05T08:27:53.8230623Z ERROR tests/test_p120_paper_observation_evidence_gate.py
2026-06-05T08:27:53.8231083Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-06-05T08:27:53.8231482Z 1 error in 3.84s
```

```text
2026-06-05T08:27:53.8222634Z ==================================== ERRORS ====================================
2026-06-05T08:27:53.8223440Z _____ ERROR collecting tests/test_p120_paper_observation_evidence_gate.py ______
2026-06-05T08:27:53.8224963Z ImportError while importing test module '/home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_p120_paper_observation_evidence_gate.py'.
2026-06-05T08:27:53.8225953Z Hint: make sure your test modules/packages have valid Python names.
2026-06-05T08:27:53.8226361Z Traceback:
2026-06-05T08:27:53.8226803Z /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/importlib/__init__.py:126: in import_module
2026-06-05T08:27:53.8227429Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-06-05T08:27:53.8227918Z tests/test_p120_paper_observation_evidence_gate.py:7: in <module>
2026-06-05T08:27:53.8228582Z     from src.operations.paper_observation_evidence_gate import validate_paper_observation_evidence_artifact
2026-06-05T08:27:53.8229584Z E   ModuleNotFoundError: No module named 'src.operations.paper_observation_evidence_gate'
2026-06-05T08:27:53.8230168Z =========================== short test summary info ============================
2026-06-05T08:27:53.8230623Z ERROR tests/test_p120_paper_observation_evidence_gate.py
2026-06-05T08:27:53.8231083Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-06-05T08:27:53.8231482Z 1 error in 3.84s
2026-06-05T08:27:53.9824537Z ##[error]Process completed with exit code 2.
2026-06-05T08:27:53.9897795Z ##[group]Run actions/upload-artifact@v4
```

```text
2026-06-05T08:27:53.8226803Z /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/importlib/__init__.py:126: in import_module
2026-06-05T08:27:53.8227429Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-06-05T08:27:53.8227918Z tests/test_p120_paper_observation_evidence_gate.py:7: in <module>
2026-06-05T08:27:53.8228582Z     from src.operations.paper_observation_evidence_gate import validate_paper_observation_evidence_artifact
2026-06-05T08:27:53.8229584Z E   ModuleNotFoundError: No module named 'src.operations.paper_observation_evidence_gate'
2026-06-05T08:27:53.8230168Z =========================== short test summary info ============================
2026-06-05T08:27:53.8230623Z ERROR tests/test_p120_paper_observation_evidence_gate.py
2026-06-05T08:27:53.8231083Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-06-05T08:27:53.8231482Z 1 error in 3.84s
2026-06-05T08:27:53.9824537Z ##[error]Process completed with exit code 2.
2026-06-05T08:27:53.9897795Z ##[group]Run actions/upload-artifact@v4
2026-06-05T08:27:53.9898099Z with:
2026-06-05T08:27:53.9898321Z   name: p109-residual-pytest-evidence
2026-06-05T08:27:53.9898647Z   path: artifacts/evidence/p109-residual-pytest/
2026-06-05T08:27:53.9898963Z   if-no-files-found: warn
2026-06-05T08:27:53.9899205Z   compression-level: 6
```

```text
2026-06-05T08:27:53.8227918Z tests/test_p120_paper_observation_evidence_gate.py:7: in <module>
2026-06-05T08:27:53.8228582Z     from src.operations.paper_observation_evidence_gate import validate_paper_observation_evidence_artifact
2026-06-05T08:27:53.8229584Z E   ModuleNotFoundError: No module named 'src.operations.paper_observation_evidence_gate'
2026-06-05T08:27:53.8230168Z =========================== short test summary info ============================
2026-06-05T08:27:53.8230623Z ERROR tests/test_p120_paper_observation_evidence_gate.py
2026-06-05T08:27:53.8231083Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-06-05T08:27:53.8231482Z 1 error in 3.84s
2026-06-05T08:27:53.9824537Z ##[error]Process completed with exit code 2.
2026-06-05T08:27:53.9897795Z ##[group]Run actions/upload-artifact@v4
2026-06-05T08:27:53.9898099Z with:
2026-06-05T08:27:53.9898321Z   name: p109-residual-pytest-evidence
2026-06-05T08:27:53.9898647Z   path: artifacts/evidence/p109-residual-pytest/
2026-06-05T08:27:53.9898963Z   if-no-files-found: warn
2026-06-05T08:27:53.9899205Z   compression-level: 6
2026-06-05T08:27:53.9899428Z   overwrite: false
2026-06-05T08:27:53.9899651Z   include-hidden-files: false
```

```text
2026-06-05T08:27:53.8230168Z =========================== short test summary info ============================
2026-06-05T08:27:53.8230623Z ERROR tests/test_p120_paper_observation_evidence_gate.py
2026-06-05T08:27:53.8231083Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-06-05T08:27:53.8231482Z 1 error in 3.84s
2026-06-05T08:27:53.9824537Z ##[error]Process completed with exit code 2.
2026-06-05T08:27:53.9897795Z ##[group]Run actions/upload-artifact@v4
2026-06-05T08:27:53.9898099Z with:
2026-06-05T08:27:53.9898321Z   name: p109-residual-pytest-evidence
2026-06-05T08:27:53.9898647Z   path: artifacts/evidence/p109-residual-pytest/
2026-06-05T08:27:53.9898963Z   if-no-files-found: warn
2026-06-05T08:27:53.9899205Z   compression-level: 6
2026-06-05T08:27:53.9899428Z   overwrite: false
2026-06-05T08:27:53.9899651Z   include-hidden-files: false
2026-06-05T08:27:53.9899889Z env:
2026-06-05T08:27:53.9900152Z   pythonLocation: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-05T08:27:53.9900603Z   PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib/pkgconfig
```

## Decision Engine Tests

- Run ID: `27004258291`
- Branch: `main`
- Commit: `fbef34dcead8`
- Title: P120 add paper observation evidence schema guard
- Created: 2026-06-05T08:27:09Z
- Updated: 2026-06-05T08:27:41Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27004258291

### Failed job: tests

- Job ID: `79691819688`
- Started: 2026-06-05T08:27:12Z
- Completed: 2026-06-05T08:27:40Z
- Failed steps: 5. Run pytest

#### Error context

```text
2026-06-05T08:27:31.1665599Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-05T08:27:31.1666027Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-05T08:27:31.1666384Z ##[endgroup]
2026-06-05T08:27:37.5532306Z 
2026-06-05T08:27:37.5532928Z ==================================== ERRORS ====================================
2026-06-05T08:27:37.5533799Z _____ ERROR collecting tests/test_p120_paper_observation_evidence_gate.py ______
2026-06-05T08:27:37.5535210Z ImportError while importing test module '/home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_p120_paper_observation_evidence_gate.py'.
2026-06-05T08:27:37.5536517Z Hint: make sure your test modules/packages have valid Python names.
2026-06-05T08:27:37.5537036Z Traceback:
2026-06-05T08:27:37.5537626Z /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/importlib/__init__.py:126: in import_module
2026-06-05T08:27:37.5539014Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-06-05T08:27:37.5539664Z tests/test_p120_paper_observation_evidence_gate.py:7: in <module>
2026-06-05T08:27:37.5540535Z     from src.operations.paper_observation_evidence_gate import validate_paper_observation_evidence_artifact
2026-06-05T08:27:37.5541538Z E   ModuleNotFoundError: No module named 'src.operations.paper_observation_evidence_gate'
2026-06-05T08:27:37.5542314Z =========================== short test summary info ============================
2026-06-05T08:27:37.5542903Z ERROR tests/test_p120_paper_observation_evidence_gate.py
```

```text
2026-06-05T08:27:31.1666027Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-05T08:27:31.1666384Z ##[endgroup]
2026-06-05T08:27:37.5532306Z 
2026-06-05T08:27:37.5532928Z ==================================== ERRORS ====================================
2026-06-05T08:27:37.5533799Z _____ ERROR collecting tests/test_p120_paper_observation_evidence_gate.py ______
2026-06-05T08:27:37.5535210Z ImportError while importing test module '/home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_p120_paper_observation_evidence_gate.py'.
2026-06-05T08:27:37.5536517Z Hint: make sure your test modules/packages have valid Python names.
2026-06-05T08:27:37.5537036Z Traceback:
2026-06-05T08:27:37.5537626Z /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/importlib/__init__.py:126: in import_module
2026-06-05T08:27:37.5539014Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-06-05T08:27:37.5539664Z tests/test_p120_paper_observation_evidence_gate.py:7: in <module>
2026-06-05T08:27:37.5540535Z     from src.operations.paper_observation_evidence_gate import validate_paper_observation_evidence_artifact
2026-06-05T08:27:37.5541538Z E   ModuleNotFoundError: No module named 'src.operations.paper_observation_evidence_gate'
2026-06-05T08:27:37.5542314Z =========================== short test summary info ============================
2026-06-05T08:27:37.5542903Z ERROR tests/test_p120_paper_observation_evidence_gate.py
2026-06-05T08:27:37.5543510Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
```

```text
2026-06-05T08:27:31.1666384Z ##[endgroup]
2026-06-05T08:27:37.5532306Z 
2026-06-05T08:27:37.5532928Z ==================================== ERRORS ====================================
2026-06-05T08:27:37.5533799Z _____ ERROR collecting tests/test_p120_paper_observation_evidence_gate.py ______
2026-06-05T08:27:37.5535210Z ImportError while importing test module '/home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_p120_paper_observation_evidence_gate.py'.
2026-06-05T08:27:37.5536517Z Hint: make sure your test modules/packages have valid Python names.
2026-06-05T08:27:37.5537036Z Traceback:
2026-06-05T08:27:37.5537626Z /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/importlib/__init__.py:126: in import_module
2026-06-05T08:27:37.5539014Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-06-05T08:27:37.5539664Z tests/test_p120_paper_observation_evidence_gate.py:7: in <module>
2026-06-05T08:27:37.5540535Z     from src.operations.paper_observation_evidence_gate import validate_paper_observation_evidence_artifact
2026-06-05T08:27:37.5541538Z E   ModuleNotFoundError: No module named 'src.operations.paper_observation_evidence_gate'
2026-06-05T08:27:37.5542314Z =========================== short test summary info ============================
2026-06-05T08:27:37.5542903Z ERROR tests/test_p120_paper_observation_evidence_gate.py
2026-06-05T08:27:37.5543510Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-06-05T08:27:37.5544039Z 1 error in 5.80s
```

```text
2026-06-05T08:27:37.5532928Z ==================================== ERRORS ====================================
2026-06-05T08:27:37.5533799Z _____ ERROR collecting tests/test_p120_paper_observation_evidence_gate.py ______
2026-06-05T08:27:37.5535210Z ImportError while importing test module '/home/runner/work/institutional-trading-engine/institutional-trading-engine/tests/test_p120_paper_observation_evidence_gate.py'.
2026-06-05T08:27:37.5536517Z Hint: make sure your test modules/packages have valid Python names.
2026-06-05T08:27:37.5537036Z Traceback:
2026-06-05T08:27:37.5537626Z /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/importlib/__init__.py:126: in import_module
2026-06-05T08:27:37.5539014Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-06-05T08:27:37.5539664Z tests/test_p120_paper_observation_evidence_gate.py:7: in <module>
2026-06-05T08:27:37.5540535Z     from src.operations.paper_observation_evidence_gate import validate_paper_observation_evidence_artifact
2026-06-05T08:27:37.5541538Z E   ModuleNotFoundError: No module named 'src.operations.paper_observation_evidence_gate'
2026-06-05T08:27:37.5542314Z =========================== short test summary info ============================
2026-06-05T08:27:37.5542903Z ERROR tests/test_p120_paper_observation_evidence_gate.py
2026-06-05T08:27:37.5543510Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-06-05T08:27:37.5544039Z 1 error in 5.80s
2026-06-05T08:27:37.8924945Z ##[error]Process completed with exit code 2.
2026-06-05T08:27:37.9047292Z Post job cleanup.
```

```text
2026-06-05T08:27:37.5537626Z /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/importlib/__init__.py:126: in import_module
2026-06-05T08:27:37.5539014Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-06-05T08:27:37.5539664Z tests/test_p120_paper_observation_evidence_gate.py:7: in <module>
2026-06-05T08:27:37.5540535Z     from src.operations.paper_observation_evidence_gate import validate_paper_observation_evidence_artifact
2026-06-05T08:27:37.5541538Z E   ModuleNotFoundError: No module named 'src.operations.paper_observation_evidence_gate'
2026-06-05T08:27:37.5542314Z =========================== short test summary info ============================
2026-06-05T08:27:37.5542903Z ERROR tests/test_p120_paper_observation_evidence_gate.py
2026-06-05T08:27:37.5543510Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-06-05T08:27:37.5544039Z 1 error in 5.80s
2026-06-05T08:27:37.8924945Z ##[error]Process completed with exit code 2.
2026-06-05T08:27:37.9047292Z Post job cleanup.
2026-06-05T08:27:38.0064651Z [command]/usr/bin/git version
2026-06-05T08:27:38.0102946Z git version 2.54.0
2026-06-05T08:27:38.0147756Z Temporarily overriding HOME='/home/runner/work/_temp/55429fbe-4dd3-4bde-b970-7e019f6643b5' before making global git config changes
2026-06-05T08:27:38.0149388Z Adding repository directory to the temporary git global config as a safe directory
2026-06-05T08:27:38.0164104Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
```

```text
2026-06-05T08:27:37.5539664Z tests/test_p120_paper_observation_evidence_gate.py:7: in <module>
2026-06-05T08:27:37.5540535Z     from src.operations.paper_observation_evidence_gate import validate_paper_observation_evidence_artifact
2026-06-05T08:27:37.5541538Z E   ModuleNotFoundError: No module named 'src.operations.paper_observation_evidence_gate'
2026-06-05T08:27:37.5542314Z =========================== short test summary info ============================
2026-06-05T08:27:37.5542903Z ERROR tests/test_p120_paper_observation_evidence_gate.py
2026-06-05T08:27:37.5543510Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-06-05T08:27:37.5544039Z 1 error in 5.80s
2026-06-05T08:27:37.8924945Z ##[error]Process completed with exit code 2.
2026-06-05T08:27:37.9047292Z Post job cleanup.
2026-06-05T08:27:38.0064651Z [command]/usr/bin/git version
2026-06-05T08:27:38.0102946Z git version 2.54.0
2026-06-05T08:27:38.0147756Z Temporarily overriding HOME='/home/runner/work/_temp/55429fbe-4dd3-4bde-b970-7e019f6643b5' before making global git config changes
2026-06-05T08:27:38.0149388Z Adding repository directory to the temporary git global config as a safe directory
2026-06-05T08:27:38.0164104Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-06-05T08:27:38.0204874Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-06-05T08:27:38.0242743Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
```

```text
2026-06-05T08:27:37.5542314Z =========================== short test summary info ============================
2026-06-05T08:27:37.5542903Z ERROR tests/test_p120_paper_observation_evidence_gate.py
2026-06-05T08:27:37.5543510Z !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2026-06-05T08:27:37.5544039Z 1 error in 5.80s
2026-06-05T08:27:37.8924945Z ##[error]Process completed with exit code 2.
2026-06-05T08:27:37.9047292Z Post job cleanup.
2026-06-05T08:27:38.0064651Z [command]/usr/bin/git version
2026-06-05T08:27:38.0102946Z git version 2.54.0
2026-06-05T08:27:38.0147756Z Temporarily overriding HOME='/home/runner/work/_temp/55429fbe-4dd3-4bde-b970-7e019f6643b5' before making global git config changes
2026-06-05T08:27:38.0149388Z Adding repository directory to the temporary git global config as a safe directory
2026-06-05T08:27:38.0164104Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-06-05T08:27:38.0204874Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-06-05T08:27:38.0242743Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-06-05T08:27:38.0484467Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-06-05T08:27:38.0512133Z http.https://github.com/.extraheader
2026-06-05T08:27:38.0527676Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

## Report Quality Validation

- Run ID: `27004258283`
- Branch: `main`
- Commit: `fbef34dcead8`
- Title: P120 add paper observation evidence schema guard
- Created: 2026-06-05T08:27:09Z
- Updated: 2026-06-05T08:28:25Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27004258283

### Failed job: validate-reports (premarket)

- Job ID: `79691819898`
- Started: 2026-06-05T08:27:12Z
- Completed: 2026-06-05T08:28:24Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-05T08:27:28.8040993Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-05T08:27:28.8041394Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-05T08:27:28.8041849Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-05T08:27:28.8042202Z ##[endgroup]
2026-06-05T08:28:20.0790666Z Traceback (most recent call last):
2026-06-05T08:28:20.0793204Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-01/2026-06-05?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-05T08:28:20.0801224Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 295, in <module>
2026-06-05T08:28:20.0802085Z     raise SystemExit(main())
2026-06-05T08:28:20.0802377Z                      ^^^^^^
2026-06-05T08:28:20.0803155Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 282, in main
2026-06-05T08:28:20.0804076Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-05T08:28:20.0804545Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-05T08:28:20.0805304Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 108, in write_report_text_guarded
2026-06-05T08:28:20.0806444Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-05T08:28:20.0807299Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-05T08:28:20.0808040Z     raise ReportOutputBoundaryError(
```

```text
2026-06-05T08:28:20.0808040Z     raise ReportOutputBoundaryError(
2026-06-05T08:28:20.0809414Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/premarket-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
2026-06-05T08:28:20.0811520Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-01/2026-06-05?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-05T08:28:20.0812990Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-01/2026-06-05?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-05T08:28:20.1468083Z ##[error]Process completed with exit code 1.
2026-06-05T08:28:20.1552967Z ##[group]Run actions/upload-artifact@v4
2026-06-05T08:28:20.1553280Z with:
2026-06-05T08:28:20.1553498Z   name: validated-premarket-report
2026-06-05T08:28:20.1553786Z   path: reports/premarket-report.md
2026-06-05T08:28:20.1554051Z   retention-days: 14
2026-06-05T08:28:20.1554467Z   if-no-files-found: warn
2026-06-05T08:28:20.1554703Z   compression-level: 6
2026-06-05T08:28:20.1554925Z   overwrite: false
2026-06-05T08:28:20.1555145Z   include-hidden-files: false
2026-06-05T08:28:20.1555656Z env:
2026-06-05T08:28:20.1556001Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (weekly)

- Job ID: `79691819952`
- Started: 2026-06-05T08:27:12Z
- Completed: 2026-06-05T08:27:34Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-05T08:27:31.5785977Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-05T08:27:31.5786405Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-05T08:27:31.5786890Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-05T08:27:31.5787257Z ##[endgroup]
2026-06-05T08:27:32.7457101Z Traceback (most recent call last):
2026-06-05T08:27:32.7466864Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 295, in <module>
2026-06-05T08:27:32.7467996Z     raise SystemExit(main())
2026-06-05T08:27:32.7468390Z                      ^^^^^^
2026-06-05T08:27:32.7469390Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 282, in main
2026-06-05T08:27:32.7470649Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-05T08:27:32.7472056Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-05T08:27:32.7473873Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 108, in write_report_text_guarded
2026-06-05T08:27:32.7475220Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-05T08:27:32.7476245Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-05T08:27:32.7477054Z     raise ReportOutputBoundaryError(
2026-06-05T08:27:32.7478549Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
```

```text
2026-06-05T08:27:32.7475220Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-05T08:27:32.7476245Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-05T08:27:32.7477054Z     raise ReportOutputBoundaryError(
2026-06-05T08:27:32.7478549Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
2026-06-05T08:27:32.7699435Z ##[error]Process completed with exit code 1.
2026-06-05T08:27:32.7783926Z ##[group]Run actions/upload-artifact@v4
2026-06-05T08:27:32.7784225Z with:
2026-06-05T08:27:32.7784430Z   name: validated-weekly-report
2026-06-05T08:27:32.7784695Z   path: reports/weekly-report.md
2026-06-05T08:27:32.7784949Z   retention-days: 14
2026-06-05T08:27:32.7785170Z   if-no-files-found: warn
2026-06-05T08:27:32.7785399Z   compression-level: 6
2026-06-05T08:27:32.7785616Z   overwrite: false
2026-06-05T08:27:32.7785830Z   include-hidden-files: false
2026-06-05T08:27:32.7786064Z env:
2026-06-05T08:27:32.7786418Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (postmarket)

- Job ID: `79691819961`
- Started: 2026-06-05T08:27:12Z
- Completed: 2026-06-05T08:28:23Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-05T08:27:28.4860497Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-05T08:27:28.4860919Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-05T08:27:28.4861369Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-05T08:27:28.4861714Z ##[endgroup]
2026-06-05T08:28:19.1807888Z Traceback (most recent call last):
2026-06-05T08:28:19.1809984Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-01/2026-06-05?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-05T08:28:19.1820375Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 295, in <module>
2026-06-05T08:28:19.1821457Z     raise SystemExit(main())
2026-06-05T08:28:19.1821836Z                      ^^^^^^
2026-06-05T08:28:19.1822804Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 282, in main
2026-06-05T08:28:19.1823992Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-05T08:28:19.1824707Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-05T08:28:19.1825900Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 108, in write_report_text_guarded
2026-06-05T08:28:19.1827378Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-05T08:28:19.1828772Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-05T08:28:19.1831043Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-01/2026-06-05?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
```

```text
2026-06-05T08:28:19.1831043Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-01/2026-06-05?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-05T08:28:19.1833383Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-01/2026-06-05?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-05T08:28:19.1834725Z     raise ReportOutputBoundaryError(
2026-06-05T08:28:19.1837218Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/postmarket-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
2026-06-05T08:28:19.2428878Z ##[error]Process completed with exit code 1.
2026-06-05T08:28:19.2514151Z ##[group]Run actions/upload-artifact@v4
2026-06-05T08:28:19.2514485Z with:
2026-06-05T08:28:19.2514719Z   name: validated-postmarket-report
2026-06-05T08:28:19.2515035Z   path: reports/postmarket-report.md
2026-06-05T08:28:19.2515506Z   retention-days: 14
2026-06-05T08:28:19.2515755Z   if-no-files-found: warn
2026-06-05T08:28:19.2516011Z   compression-level: 6
2026-06-05T08:28:19.2516257Z   overwrite: false
2026-06-05T08:28:19.2516494Z   include-hidden-files: false
2026-06-05T08:28:19.2516754Z env:
2026-06-05T08:28:19.2517301Z   POLYGON_API_KEY: ***
```

## Report Quality Validation

- Run ID: `27001516525`
- Branch: `main`
- Commit: `7562e3287d19`
- Title: P119 document module inventory regeneration
- Created: 2026-06-05T07:24:01Z
- Updated: 2026-06-05T07:25:16Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27001516525

### Failed job: validate-reports (postmarket)

- Job ID: `79682854993`
- Started: 2026-06-05T07:24:04Z
- Completed: 2026-06-05T07:25:15Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-05T07:24:23.3881992Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-05T07:24:23.3882375Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-05T07:24:23.3882789Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-05T07:24:23.3883132Z ##[endgroup]
2026-06-05T07:25:11.8859031Z Traceback (most recent call last):
2026-06-05T07:25:11.8861133Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-01/2026-06-05?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-05T07:25:11.8870202Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 295, in <module>
2026-06-05T07:25:11.8871287Z     raise SystemExit(main())
2026-06-05T07:25:11.8871648Z                      ^^^^^^
2026-06-05T07:25:11.8872606Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 282, in main
2026-06-05T07:25:11.8873803Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-05T07:25:11.8874514Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-05T07:25:11.8876089Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-01/2026-06-05?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-05T07:25:11.8878597Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-01/2026-06-05?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-05T07:25:11.8888643Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 108, in write_report_text_guarded
2026-06-05T07:25:11.8908058Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
```

```text
2026-06-05T07:25:11.8908058Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-05T07:25:11.8909300Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-05T07:25:11.8910194Z     raise ReportOutputBoundaryError(
2026-06-05T07:25:11.8911833Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/postmarket-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
2026-06-05T07:25:11.9541099Z ##[error]Process completed with exit code 1.
2026-06-05T07:25:11.9626214Z ##[group]Run actions/upload-artifact@v4
2026-06-05T07:25:11.9626531Z with:
2026-06-05T07:25:11.9626748Z   name: validated-postmarket-report
2026-06-05T07:25:11.9627302Z   path: reports/postmarket-report.md
2026-06-05T07:25:11.9627761Z   retention-days: 14
2026-06-05T07:25:11.9627985Z   if-no-files-found: warn
2026-06-05T07:25:11.9628218Z   compression-level: 6
2026-06-05T07:25:11.9628437Z   overwrite: false
2026-06-05T07:25:11.9628649Z   include-hidden-files: false
2026-06-05T07:25:11.9628878Z env:
2026-06-05T07:25:11.9629211Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (premarket)

- Job ID: `79682854995`
- Started: 2026-06-05T07:24:03Z
- Completed: 2026-06-05T07:25:05Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-05T07:24:20.2387217Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-05T07:24:20.2387604Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-05T07:24:20.2388019Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-05T07:24:20.2388343Z ##[endgroup]
2026-06-05T07:25:02.5391879Z Traceback (most recent call last):
2026-06-05T07:25:02.5394116Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-01/2026-06-05?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-05T07:25:02.5397509Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-01/2026-06-05?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-05T07:25:02.5399468Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-01/2026-06-05?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-05T07:25:02.5407195Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 295, in <module>
2026-06-05T07:25:02.5407918Z     raise SystemExit(main())
2026-06-05T07:25:02.5408169Z                      ^^^^^^
2026-06-05T07:25:02.5408815Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 282, in main
2026-06-05T07:25:02.5409646Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-05T07:25:02.5410101Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-05T07:25:02.5410879Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 108, in write_report_text_guarded
2026-06-05T07:25:02.5411670Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
```

```text
2026-06-05T07:25:02.5411670Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-05T07:25:02.5412532Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-05T07:25:02.5413269Z     raise ReportOutputBoundaryError(
2026-06-05T07:25:02.5414656Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/premarket-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
2026-06-05T07:25:02.6082446Z ##[error]Process completed with exit code 1.
2026-06-05T07:25:02.6168654Z ##[group]Run actions/upload-artifact@v4
2026-06-05T07:25:02.6168962Z with:
2026-06-05T07:25:02.6169179Z   name: validated-premarket-report
2026-06-05T07:25:02.6169468Z   path: reports/premarket-report.md
2026-06-05T07:25:02.6169932Z   retention-days: 14
2026-06-05T07:25:02.6170155Z   if-no-files-found: warn
2026-06-05T07:25:02.6170386Z   compression-level: 6
2026-06-05T07:25:02.6170605Z   overwrite: false
2026-06-05T07:25:02.6170819Z   include-hidden-files: false
2026-06-05T07:25:02.6171052Z env:
2026-06-05T07:25:02.6171399Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (weekly)

- Job ID: `79682855040`
- Started: 2026-06-05T07:24:04Z
- Completed: 2026-06-05T07:24:23Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-05T07:24:20.4998593Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-05T07:24:20.4998963Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-05T07:24:20.4999395Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-05T07:24:20.4999716Z ##[endgroup]
2026-06-05T07:24:20.7972729Z Traceback (most recent call last):
2026-06-05T07:24:20.7984416Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 295, in <module>
2026-06-05T07:24:20.7986545Z     raise SystemExit(main())
2026-06-05T07:24:20.7987078Z                      ^^^^^^
2026-06-05T07:24:20.7988144Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 282, in main
2026-06-05T07:24:20.7989429Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-05T07:24:20.7990372Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-05T07:24:20.7991680Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 108, in write_report_text_guarded
2026-06-05T07:24:20.7992982Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-05T07:24:20.7994370Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-05T07:24:20.7995668Z     raise ReportOutputBoundaryError(
2026-06-05T07:24:20.7997807Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
```

```text
2026-06-05T07:24:20.7992982Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-05T07:24:20.7994370Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-05T07:24:20.7995668Z     raise ReportOutputBoundaryError(
2026-06-05T07:24:20.7997807Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
2026-06-05T07:24:20.8195197Z ##[error]Process completed with exit code 1.
2026-06-05T07:24:20.8270898Z ##[group]Run actions/upload-artifact@v4
2026-06-05T07:24:20.8271188Z with:
2026-06-05T07:24:20.8271402Z   name: validated-weekly-report
2026-06-05T07:24:20.8271667Z   path: reports/weekly-report.md
2026-06-05T07:24:20.8271919Z   retention-days: 14
2026-06-05T07:24:20.8272143Z   if-no-files-found: warn
2026-06-05T07:24:20.8272375Z   compression-level: 6
2026-06-05T07:24:20.8272605Z   overwrite: false
2026-06-05T07:24:20.8272825Z   include-hidden-files: false
2026-06-05T07:24:20.8273057Z env:
2026-06-05T07:24:20.8273426Z   POLYGON_API_KEY: ***
```

## Report Quality Validation

- Run ID: `27001355037`
- Branch: `main`
- Commit: `59f644235466`
- Title: P119 add module inventory freshness workflow
- Created: 2026-06-05T07:20:07Z
- Updated: 2026-06-05T07:21:23Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27001355037

### Failed job: validate-reports (postmarket)

- Job ID: `79682349992`
- Started: 2026-06-05T07:20:10Z
- Completed: 2026-06-05T07:21:08Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-05T07:20:26.7790256Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-05T07:20:26.7790678Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-05T07:20:26.7791148Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-05T07:20:26.7791500Z ##[endgroup]
2026-06-05T07:21:06.2099116Z Traceback (most recent call last):
2026-06-05T07:21:06.2101393Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-01/2026-06-05?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-05T07:21:06.2114638Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 295, in <module>
2026-06-05T07:21:06.2115716Z     raise SystemExit(main())
2026-06-05T07:21:06.2116099Z                      ^^^^^^
2026-06-05T07:21:06.2117068Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 282, in main
2026-06-05T07:21:06.2118554Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-05T07:21:06.2120341Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-01/2026-06-05?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-05T07:21:06.2122658Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-01/2026-06-05?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-05T07:21:06.2124002Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-05T07:21:06.2129769Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 108, in write_report_text_guarded
2026-06-05T07:21:06.2139409Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
```

```text
2026-06-05T07:21:06.2139409Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-05T07:21:06.2141211Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-05T07:21:06.2142503Z     raise ReportOutputBoundaryError(
2026-06-05T07:21:06.2144885Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/postmarket-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
2026-06-05T07:21:06.2900256Z ##[error]Process completed with exit code 1.
2026-06-05T07:21:06.2989032Z ##[group]Run actions/upload-artifact@v4
2026-06-05T07:21:06.2989365Z with:
2026-06-05T07:21:06.2989601Z   name: validated-postmarket-report
2026-06-05T07:21:06.2989908Z   path: reports/postmarket-report.md
2026-06-05T07:21:06.2990396Z   retention-days: 14
2026-06-05T07:21:06.2990637Z   if-no-files-found: warn
2026-06-05T07:21:06.2990886Z   compression-level: 6
2026-06-05T07:21:06.2991120Z   overwrite: false
2026-06-05T07:21:06.2991349Z   include-hidden-files: false
2026-06-05T07:21:06.2991593Z env:
2026-06-05T07:21:06.2991908Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (premarket)

- Job ID: `79682350023`
- Started: 2026-06-05T07:20:10Z
- Completed: 2026-06-05T07:21:22Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-05T07:20:29.5131530Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-05T07:20:29.5131930Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-05T07:20:29.5132347Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-05T07:20:29.5132672Z ##[endgroup]
2026-06-05T07:21:11.9447940Z Traceback (most recent call last):
2026-06-05T07:21:11.9455885Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 295, in <module>
2026-06-05T07:21:11.9457939Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-01/2026-06-05?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-05T07:21:11.9459000Z     raise SystemExit(main())
2026-06-05T07:21:11.9459294Z                      ^^^^^^
2026-06-05T07:21:11.9460011Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 282, in main
2026-06-05T07:21:11.9460889Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-05T07:21:11.9461429Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-05T07:21:11.9462291Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 108, in write_report_text_guarded
2026-06-05T07:21:11.9463185Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-05T07:21:11.9464124Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-05T07:21:11.9464969Z     raise ReportOutputBoundaryError(
```

```text
2026-06-05T07:21:11.9464969Z     raise ReportOutputBoundaryError(
2026-06-05T07:21:11.9466708Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/premarket-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
2026-06-05T07:21:11.9468984Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-01/2026-06-05?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-05T07:21:11.9470533Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-01/2026-06-05?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-05T07:21:12.0083662Z ##[error]Process completed with exit code 1.
2026-06-05T07:21:12.0162096Z ##[group]Run actions/upload-artifact@v4
2026-06-05T07:21:12.0162386Z with:
2026-06-05T07:21:12.0162614Z   name: validated-premarket-report
2026-06-05T07:21:12.0162899Z   path: reports/premarket-report.md
2026-06-05T07:21:12.0163322Z   retention-days: 14
2026-06-05T07:21:12.0163552Z   if-no-files-found: warn
2026-06-05T07:21:12.0163796Z   compression-level: 6
2026-06-05T07:21:12.0164018Z   overwrite: false
2026-06-05T07:21:12.0164239Z   include-hidden-files: false
2026-06-05T07:21:12.0164473Z env:
2026-06-05T07:21:12.0164769Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (weekly)

- Job ID: `79682350042`
- Started: 2026-06-05T07:20:11Z
- Completed: 2026-06-05T07:20:33Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-05T07:20:30.0523298Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-05T07:20:30.0523696Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-05T07:20:30.0524121Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-05T07:20:30.0524458Z ##[endgroup]
2026-06-05T07:20:31.2337091Z Traceback (most recent call last):
2026-06-05T07:20:31.2345271Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 295, in <module>
2026-06-05T07:20:31.2346537Z     raise SystemExit(main())
2026-06-05T07:20:31.2346877Z                      ^^^^^^
2026-06-05T07:20:31.2347758Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 282, in main
2026-06-05T07:20:31.2348860Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-05T07:20:31.2349467Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-05T07:20:31.2350546Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 108, in write_report_text_guarded
2026-06-05T07:20:31.2351658Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-05T07:20:31.2352816Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-05T07:20:31.2353845Z     raise ReportOutputBoundaryError(
2026-06-05T07:20:31.2355766Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
```

```text
2026-06-05T07:20:31.2351658Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-05T07:20:31.2352816Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-05T07:20:31.2353845Z     raise ReportOutputBoundaryError(
2026-06-05T07:20:31.2355766Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
2026-06-05T07:20:31.2572046Z ##[error]Process completed with exit code 1.
2026-06-05T07:20:31.2657099Z ##[group]Run actions/upload-artifact@v4
2026-06-05T07:20:31.2657408Z with:
2026-06-05T07:20:31.2657623Z   name: validated-weekly-report
2026-06-05T07:20:31.2657894Z   path: reports/weekly-report.md
2026-06-05T07:20:31.2658153Z   retention-days: 14
2026-06-05T07:20:31.2658377Z   if-no-files-found: warn
2026-06-05T07:20:31.2658611Z   compression-level: 6
2026-06-05T07:20:31.2658840Z   overwrite: false
2026-06-05T07:20:31.2659064Z   include-hidden-files: false
2026-06-05T07:20:31.2659307Z env:
2026-06-05T07:20:31.2659641Z   POLYGON_API_KEY: ***
```

## Report Quality Validation

- Run ID: `27001204692`
- Branch: `main`
- Commit: `aa74b63bd9a3`
- Title: P119 add deterministic inventory check tests
- Created: 2026-06-05T07:16:14Z
- Updated: 2026-06-05T07:17:25Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27001204692

### Failed job: validate-reports (premarket)

- Job ID: `79681847289`
- Started: 2026-06-05T07:16:17Z
- Completed: 2026-06-05T07:17:20Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-05T07:16:37.0397664Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-05T07:16:37.0398058Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-05T07:16:37.0398531Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-05T07:16:37.0398868Z ##[endgroup]
2026-06-05T07:17:18.0782569Z Traceback (most recent call last):
2026-06-05T07:17:18.0784569Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-01/2026-06-05?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-05T07:17:18.0786304Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-01/2026-06-05?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-05T07:17:18.0787665Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-01/2026-06-05?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-05T07:17:18.0794798Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 295, in <module>
2026-06-05T07:17:18.0795558Z     raise SystemExit(main())
2026-06-05T07:17:18.0795839Z                      ^^^^^^
2026-06-05T07:17:18.0796485Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 282, in main
2026-06-05T07:17:18.0797245Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-05T07:17:18.0803123Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-05T07:17:18.0804379Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 108, in write_report_text_guarded
2026-06-05T07:17:18.0805391Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
```

```text
2026-06-05T07:17:18.0805391Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-05T07:17:18.0806911Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-05T07:17:18.0808155Z     raise ReportOutputBoundaryError(
2026-06-05T07:17:18.0810366Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/premarket-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
2026-06-05T07:17:18.1534986Z ##[error]Process completed with exit code 1.
2026-06-05T07:17:18.1623035Z ##[group]Run actions/upload-artifact@v4
2026-06-05T07:17:18.1623370Z with:
2026-06-05T07:17:18.1623608Z   name: validated-premarket-report
2026-06-05T07:17:18.1623912Z   path: reports/premarket-report.md
2026-06-05T07:17:18.1624191Z   retention-days: 14
2026-06-05T07:17:18.1624650Z   if-no-files-found: warn
2026-06-05T07:17:18.1624912Z   compression-level: 6
2026-06-05T07:17:18.1625152Z   overwrite: false
2026-06-05T07:17:18.1625392Z   include-hidden-files: false
2026-06-05T07:17:18.1625646Z env:
2026-06-05T07:17:18.1625996Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (postmarket)

- Job ID: `79681847302`
- Started: 2026-06-05T07:16:17Z
- Completed: 2026-06-05T07:17:24Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-05T07:16:36.3060028Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-05T07:16:36.3060401Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-05T07:16:36.3060839Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-05T07:16:36.3061166Z ##[endgroup]
2026-06-05T07:17:22.0355985Z Traceback (most recent call last):
2026-06-05T07:17:22.0358033Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-01/2026-06-05?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-05T07:17:22.0369941Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 295, in <module>
2026-06-05T07:17:22.0372122Z     raise SystemExit(main())
2026-06-05T07:17:22.0372786Z                      ^^^^^^
2026-06-05T07:17:22.0374493Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 282, in main
2026-06-05T07:17:22.0376649Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-05T07:17:22.0377853Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-05T07:17:22.0379989Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 108, in write_report_text_guarded
2026-06-05T07:17:22.0382417Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-05T07:17:22.0384829Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-05T07:17:22.0386968Z     raise ReportOutputBoundaryError(
```

```text
2026-06-05T07:17:22.0386968Z     raise ReportOutputBoundaryError(
2026-06-05T07:17:22.0389264Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/postmarket-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
2026-06-05T07:17:22.0392572Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-01/2026-06-05?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-05T07:17:22.0394675Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-01/2026-06-05?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-05T07:17:22.1070321Z ##[error]Process completed with exit code 1.
2026-06-05T07:17:22.1149458Z ##[group]Run actions/upload-artifact@v4
2026-06-05T07:17:22.1149742Z with:
2026-06-05T07:17:22.1149967Z   name: validated-postmarket-report
2026-06-05T07:17:22.1150254Z   path: reports/postmarket-report.md
2026-06-05T07:17:22.1150518Z   retention-days: 14
2026-06-05T07:17:22.1150864Z   if-no-files-found: warn
2026-06-05T07:17:22.1151095Z   compression-level: 6
2026-06-05T07:17:22.1151493Z   overwrite: false
2026-06-05T07:17:22.1151723Z   include-hidden-files: false
2026-06-05T07:17:22.1151962Z env:
2026-06-05T07:17:22.1152276Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (weekly)

- Job ID: `79681847304`
- Started: 2026-06-05T07:16:17Z
- Completed: 2026-06-05T07:16:38Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-05T07:16:35.7287578Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-05T07:16:35.7287976Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-05T07:16:35.7288398Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-05T07:16:35.7288739Z ##[endgroup]
2026-06-05T07:16:36.4347314Z Traceback (most recent call last):
2026-06-05T07:16:36.4355152Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 295, in <module>
2026-06-05T07:16:36.4355960Z     raise SystemExit(main())
2026-06-05T07:16:36.4356227Z                      ^^^^^^
2026-06-05T07:16:36.4356874Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 282, in main
2026-06-05T07:16:36.4357640Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-05T07:16:36.4358101Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-05T07:16:36.4358923Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 108, in write_report_text_guarded
2026-06-05T07:16:36.4359740Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-05T07:16:36.4360907Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-05T07:16:36.4361671Z     raise ReportOutputBoundaryError(
2026-06-05T07:16:36.4363062Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
```

```text
2026-06-05T07:16:36.4359740Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-05T07:16:36.4360907Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-05T07:16:36.4361671Z     raise ReportOutputBoundaryError(
2026-06-05T07:16:36.4363062Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
2026-06-05T07:16:36.4570086Z ##[error]Process completed with exit code 1.
2026-06-05T07:16:36.4650932Z ##[group]Run actions/upload-artifact@v4
2026-06-05T07:16:36.4651272Z with:
2026-06-05T07:16:36.4651495Z   name: validated-weekly-report
2026-06-05T07:16:36.4651777Z   path: reports/weekly-report.md
2026-06-05T07:16:36.4652051Z   retention-days: 14
2026-06-05T07:16:36.4652279Z   if-no-files-found: warn
2026-06-05T07:16:36.4652521Z   compression-level: 6
2026-06-05T07:16:36.4652760Z   overwrite: false
2026-06-05T07:16:36.4652992Z   include-hidden-files: false
2026-06-05T07:16:36.4653233Z env:
2026-06-05T07:16:36.4653603Z   POLYGON_API_KEY: ***
```

## Report Quality Validation

- Run ID: `27000827237`
- Branch: `main`
- Commit: `891c95c17483`
- Title: P119 add module inventory check mode
- Created: 2026-06-05T07:06:53Z
- Updated: 2026-06-05T07:08:08Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27000827237

### Failed job: validate-reports (postmarket)

- Job ID: `79680643356`
- Started: 2026-06-05T07:06:56Z
- Completed: 2026-06-05T07:07:55Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-05T07:07:12.3559433Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-05T07:07:12.3559842Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-05T07:07:12.3560269Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-05T07:07:12.3560624Z ##[endgroup]
2026-06-05T07:07:53.0434019Z Traceback (most recent call last):
2026-06-05T07:07:53.0438157Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-01/2026-06-05?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-05T07:07:53.0447584Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 295, in <module>
2026-06-05T07:07:53.0448317Z     raise SystemExit(main())
2026-06-05T07:07:53.0448594Z                      ^^^^^^
2026-06-05T07:07:53.0449239Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 282, in main
2026-06-05T07:07:53.0450020Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-05T07:07:53.0450481Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-05T07:07:53.0451256Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 108, in write_report_text_guarded
2026-06-05T07:07:53.0452041Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-05T07:07:53.0452880Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-05T07:07:53.0453617Z     raise ReportOutputBoundaryError(
```

```text
2026-06-05T07:07:53.0453617Z     raise ReportOutputBoundaryError(
2026-06-05T07:07:53.0455236Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/postmarket-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
2026-06-05T07:07:53.0457439Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-01/2026-06-05?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-05T07:07:53.0458791Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-01/2026-06-05?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-05T07:07:53.1050578Z ##[error]Process completed with exit code 1.
2026-06-05T07:07:53.1137119Z ##[group]Run actions/upload-artifact@v4
2026-06-05T07:07:53.1137423Z with:
2026-06-05T07:07:53.1137663Z   name: validated-postmarket-report
2026-06-05T07:07:53.1137975Z   path: reports/postmarket-report.md
2026-06-05T07:07:53.1138439Z   retention-days: 14
2026-06-05T07:07:53.1138675Z   if-no-files-found: warn
2026-06-05T07:07:53.1138928Z   compression-level: 6
2026-06-05T07:07:53.1139170Z   overwrite: false
2026-06-05T07:07:53.1139402Z   include-hidden-files: false
2026-06-05T07:07:53.1139656Z env:
2026-06-05T07:07:53.1139990Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (premarket)

- Job ID: `79680643380`
- Started: 2026-06-05T07:06:56Z
- Completed: 2026-06-05T07:08:07Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-05T07:07:14.4342948Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-05T07:07:14.4343339Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-05T07:07:14.4343760Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-05T07:07:14.4344088Z ##[endgroup]
2026-06-05T07:08:03.4430652Z Traceback (most recent call last):
2026-06-05T07:08:03.4433926Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-01/2026-06-05?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-06-05T07:08:03.4437287Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-01/2026-06-05?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-06-05T07:08:03.4439713Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2025-01-01/2026-06-05?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-06-05T07:08:03.4448237Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 295, in <module>
2026-06-05T07:08:03.4449493Z     raise SystemExit(main())
2026-06-05T07:08:03.4450123Z                      ^^^^^^
2026-06-05T07:08:03.4451122Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 282, in main
2026-06-05T07:08:03.4452261Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-05T07:08:03.4452771Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-05T07:08:03.4453670Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 108, in write_report_text_guarded
2026-06-05T07:08:03.4454535Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
```

```text
2026-06-05T07:08:03.4454535Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-05T07:08:03.4455412Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-05T07:08:03.4456188Z     raise ReportOutputBoundaryError(
2026-06-05T07:08:03.4457621Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/premarket-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
2026-06-05T07:08:03.4973709Z ##[error]Process completed with exit code 1.
2026-06-05T07:08:03.5057177Z ##[group]Run actions/upload-artifact@v4
2026-06-05T07:08:03.5057473Z with:
2026-06-05T07:08:03.5057742Z   name: validated-premarket-report
2026-06-05T07:08:03.5058026Z   path: reports/premarket-report.md
2026-06-05T07:08:03.5058284Z   retention-days: 14
2026-06-05T07:08:03.5058696Z   if-no-files-found: warn
2026-06-05T07:08:03.5058921Z   compression-level: 6
2026-06-05T07:08:03.5059133Z   overwrite: false
2026-06-05T07:08:03.5059340Z   include-hidden-files: false
2026-06-05T07:08:03.5059565Z env:
2026-06-05T07:08:03.5059886Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (weekly)

- Job ID: `79680643418`
- Started: 2026-06-05T07:06:56Z
- Completed: 2026-06-05T07:07:12Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-06-05T07:07:10.4172456Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-05T07:07:10.4172833Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-05T07:07:10.4173279Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-06-05T07:07:10.4173599Z ##[endgroup]
2026-06-05T07:07:10.7895894Z Traceback (most recent call last):
2026-06-05T07:07:10.7908502Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 295, in <module>
2026-06-05T07:07:10.7910629Z     raise SystemExit(main())
2026-06-05T07:07:10.7911492Z                      ^^^^^^
2026-06-05T07:07:10.7936388Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 282, in main
2026-06-05T07:07:10.7937517Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-06-05T07:07:10.7938237Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-06-05T07:07:10.7939619Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 108, in write_report_text_guarded
2026-06-05T07:07:10.7940885Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-05T07:07:10.7942254Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-05T07:07:10.7943439Z     raise ReportOutputBoundaryError(
2026-06-05T07:07:10.7945635Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
```

```text
2026-06-05T07:07:10.7940885Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-06-05T07:07:10.7942254Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 86, in assert_report_output_path_allowed
2026-06-05T07:07:10.7943439Z     raise ReportOutputBoundaryError(
2026-06-05T07:07:10.7945635Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Allowed generated report roots: ['reports/generated', 'reports/intraday', 'reports/postmarket', 'reports/premarket', 'reports/signals', 'reports/validation', 'reports/weekly']. Boundary=report-output-boundary-v2.
2026-06-05T07:07:10.8165820Z ##[error]Process completed with exit code 1.
2026-06-05T07:07:10.8251410Z ##[group]Run actions/upload-artifact@v4
2026-06-05T07:07:10.8251712Z with:
2026-06-05T07:07:10.8252057Z   name: validated-weekly-report
2026-06-05T07:07:10.8252349Z   path: reports/weekly-report.md
2026-06-05T07:07:10.8252605Z   retention-days: 14
2026-06-05T07:07:10.8252835Z   if-no-files-found: warn
2026-06-05T07:07:10.8253075Z   compression-level: 6
2026-06-05T07:07:10.8253311Z   overwrite: false
2026-06-05T07:07:10.8253537Z   include-hidden-files: false
2026-06-05T07:07:10.8253780Z env:
2026-06-05T07:07:10.8254159Z   POLYGON_API_KEY: ***
```
