# GitHub Actions Workflow Error Report

Generated: 2026-05-31 08:20 UTC
Repository: `yalcinkadir/institutional-trading-engine`
Filter since: 2026-05-30 08:20 UTC
Failed runs included: 9

## IP9 IP10 Public Repository Governance

- Run ID: `26685335159`
- Branch: `main`
- Commit: `1b9ece5c2519`
- Title: Remove generated weekly report from public repository
- Created: 2026-05-30T13:43:19Z
- Updated: 2026-05-30T13:43:26Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26685335159

### Failed job: IP9/IP10 governance checks

- Job ID: `78652480857`
- Started: 2026-05-30T13:43:21Z
- Completed: 2026-05-30T13:43:25Z
- Failed steps: 2. Checkout repository

#### Error context

```text
2026-05-30T13:43:23.2885725Z   lfs: false
2026-05-30T13:43:23.2886437Z   submodules: false
2026-05-30T13:43:23.2887057Z   set-safe-directory: true
2026-05-30T13:43:23.2887999Z ##[endgroup]
2026-05-30T13:43:23.3501733Z ##[error]The runner has received a shutdown signal. This can happen when the runner service is stopped, or a manually started runner is canceled.
2026-05-30T13:43:23.3967043Z Cleaning up orphan processes
2026-05-30T13:43:23.5203878Z ##[warning]Node.js 20 actions are deprecated. The following actions are running on Node.js 20 and may not work as expected: actions/checkout@v4. Actions will be forced to run with Node.js 24 by default starting June 16th, 2026. Node.js 20 will be removed from the runner on September 16th, 2026. Please check if updated versions of these actions are available that support Node.js 24. To opt into Node.js 24 now, set the FORCE_JAVASCRIPT_ACTIONS_TO_NODE24=true environment variable on the runner or in your workflow file. Once Node.js 24 becomes the default, you can temporarily opt out by setting ACTIONS_ALLOW_USE_UNSECURE_NODE_VERSION=true. For more information see: https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/
```

## Decision Engine Tests

- Run ID: `26685335158`
- Branch: `main`
- Commit: `1b9ece5c2519`
- Title: Remove generated weekly report from public repository
- Created: 2026-05-30T13:43:19Z
- Updated: 2026-05-30T13:43:52Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26685335158

### Failed job: tests

- Job ID: `78652480860`
- Started: 2026-05-30T13:43:21Z
- Completed: 2026-05-30T13:43:51Z
- Failed steps: 5. Run pytest

#### Error context

```text
2026-05-30T13:43:49.0330102Z ........................................................................ [ 87%]
2026-05-30T13:43:49.2768309Z ........................................................................ [ 93%]
2026-05-30T13:43:49.3249493Z ........................................................................ [ 98%]
2026-05-30T13:43:49.7839863Z ................                                                         [100%]
2026-05-30T13:43:49.7841135Z =================================== FAILURES ===================================
2026-05-30T13:43:49.7842918Z _________ TestDataPersistence.test_decision_log_path_not_in_gitignore __________
2026-05-30T13:43:49.7843695Z 
2026-05-30T13:43:49.7844122Z self = <test_priority_fixes.TestDataPersistence object at 0x7fee90523f90>
2026-05-30T13:43:49.7844568Z 
2026-05-30T13:43:49.7844734Z     def test_decision_log_path_not_in_gitignore(self):
2026-05-30T13:43:49.7845133Z         gitignore = Path(".gitignore")
2026-05-30T13:43:49.7845473Z         if not gitignore.exists():
2026-05-30T13:43:49.7845777Z             return
2026-05-30T13:43:49.7846059Z         content = gitignore.read_text()
2026-05-30T13:43:49.7846420Z         # data/ should NOT be in gitignore
2026-05-30T13:43:49.7846776Z >       assert "data/" not in content, (
```

```text
2026-05-30T13:43:49.7846420Z         # data/ should NOT be in gitignore
2026-05-30T13:43:49.7846776Z >       assert "data/" not in content, (
2026-05-30T13:43:49.7847464Z             "data/ is in .gitignore â decision log will be lost on every run"
2026-05-30T13:43:49.7847902Z         )
2026-05-30T13:43:49.7848376Z E       AssertionError: data/ is in .gitignore â decision log will be lost on every run
2026-05-30T13:43:49.7848961Z E       assert 'data/' not in '# Python\n_...\n.vscode/\n'
2026-05-30T13:43:49.7849584Z E         
2026-05-30T13:43:49.7849832Z E         'data/' is contained here:
2026-05-30T13:43:49.7850140Z E           e/
2026-05-30T13:43:49.7850372Z E           cache/
2026-05-30T13:43:49.7850616Z E           data/raw/
2026-05-30T13:43:49.7850873Z E           data/live/
2026-05-30T13:43:49.7851135Z E           data/private/
2026-05-30T13:43:49.7851576Z E           data/vendor/
2026-05-30T13:43:49.7851946Z E           evidence/
2026-05-30T13:43:49.7852201Z E           lockbox/
```

```text
2026-05-30T13:43:49.7860664Z E           .DS_Store
2026-05-30T13:43:49.7860878Z E           .idea/
2026-05-30T13:43:49.7861086Z E           .vscode/
2026-05-30T13:43:49.7861225Z 
2026-05-30T13:43:49.7861363Z tests/test_priority_fixes.py:372: AssertionError
2026-05-30T13:43:49.7861895Z =============================== warnings summary ===============================
2026-05-30T13:43:49.7862461Z ../../../../../opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/fastapi/testclient.py:1
2026-05-30T13:43:49.7863591Z   /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
2026-05-30T13:43:49.7864912Z     from starlette.testclient import TestClient as TestClient  # noqa
2026-05-30T13:43:49.7865223Z 
2026-05-30T13:43:49.7865480Z tests/test_jwt_auth.py::test_create_and_validate_token
2026-05-30T13:43:49.7865894Z tests/test_security_layer.py::test_metrics_accepts_admin_token
2026-05-30T13:43:49.7866375Z tests/test_security_layer.py::test_viewer_cannot_access_metrics
2026-05-30T13:43:49.7867396Z   /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/jwt/api_jwt.py:147: InsecureKeyLengthWarning: The HMAC key is 18 bytes long, which is below the minimum recommended length of 32 bytes for SHA256. See RFC 7518 Section 3.2.
2026-05-30T13:43:49.7868362Z     return self._jws.encode(
2026-05-30T13:43:49.7868519Z
```

```text
2026-05-30T13:43:49.7871743Z     decoded = self.decode_complete(
2026-05-30T13:43:49.7871928Z 
2026-05-30T13:43:49.7872179Z -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2026-05-30T13:43:49.7872687Z =========================== short test summary info ============================
2026-05-30T13:43:49.7873688Z FAILED tests/test_priority_fixes.py::TestDataPersistence::test_decision_log_path_not_in_gitignore - AssertionError: data/ is in .gitignore â decision log will be lost on every run
2026-05-30T13:43:49.7874492Z assert 'data/' not in '# Python\n_...\n.vscode/\n'
2026-05-30T13:43:49.7874799Z   
2026-05-30T13:43:49.7875011Z   'data/' is contained here:
2026-05-30T13:43:49.7875246Z     e/
2026-05-30T13:43:49.7875432Z     cache/
2026-05-30T13:43:49.7875634Z     data/raw/
2026-05-30T13:43:49.7875833Z     data/live/
2026-05-30T13:43:49.7876037Z     data/private/
2026-05-30T13:43:49.7876244Z     data/vendor/
2026-05-30T13:43:49.7876447Z     evidence/
2026-05-30T13:43:49.7876653Z     lockbox/
```

```text
2026-05-30T13:43:49.7884217Z     .DS_Store
2026-05-30T13:43:49.7884409Z     .idea/
2026-05-30T13:43:49.7884747Z     .vscode/
2026-05-30T13:43:49.7885002Z 1 failed, 1310 passed, 1 skipped, 7 warnings in 11.79s
2026-05-30T13:43:50.2077581Z ##[error]Process completed with exit code 1.
2026-05-30T13:43:50.2196691Z Post job cleanup.
2026-05-30T13:43:50.3231063Z [command]/usr/bin/git version
2026-05-30T13:43:50.3271978Z git version 2.54.0
2026-05-30T13:43:50.3320135Z Temporarily overriding HOME='/home/runner/work/_temp/d377e108-7140-48c1-9cd7-adf2c90f4f5e' before making global git config changes
2026-05-30T13:43:50.3321874Z Adding repository directory to the temporary git global config as a safe directory
2026-05-30T13:43:50.3336573Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-05-30T13:43:50.3379445Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-05-30T13:43:50.3417107Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-05-30T13:43:50.3665343Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-05-30T13:43:50.3693896Z http.https://github.com/.extraheader
2026-05-30T13:43:50.3709450Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

## Decision Engine Tests

- Run ID: `26680160673`
- Branch: `main`
- Commit: `9eab20956193`
- Title: Ignore generated weekly report artifact
- Created: 2026-05-30T09:16:10Z
- Updated: 2026-05-30T09:16:44Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26680160673

### Failed job: tests

- Job ID: `78639045565`
- Started: 2026-05-30T09:16:12Z
- Completed: 2026-05-30T09:16:43Z
- Failed steps: 5. Run pytest

#### Error context

```text
2026-05-30T09:16:41.1794639Z ........................................................................ [ 87%]
2026-05-30T09:16:41.3829569Z ........................................................................ [ 93%]
2026-05-30T09:16:41.4207388Z ........................................................................ [ 98%]
2026-05-30T09:16:41.7119286Z ................                                                         [100%]
2026-05-30T09:16:41.7120259Z =================================== FAILURES ===================================
2026-05-30T09:16:41.7121675Z _________ TestDataPersistence.test_decision_log_path_not_in_gitignore __________
2026-05-30T09:16:41.7122188Z 
2026-05-30T09:16:41.7122523Z self = <test_priority_fixes.TestDataPersistence object at 0x7f434d427850>
2026-05-30T09:16:41.7122970Z 
2026-05-30T09:16:41.7123184Z     def test_decision_log_path_not_in_gitignore(self):
2026-05-30T09:16:41.7123683Z         gitignore = Path(".gitignore")
2026-05-30T09:16:41.7124124Z         if not gitignore.exists():
2026-05-30T09:16:41.7124472Z             return
2026-05-30T09:16:41.7124784Z         content = gitignore.read_text()
2026-05-30T09:16:41.7125195Z         # data/ should NOT be in gitignore
2026-05-30T09:16:41.7125598Z >       assert "data/" not in content, (
```

```text
2026-05-30T09:16:41.7125195Z         # data/ should NOT be in gitignore
2026-05-30T09:16:41.7125598Z >       assert "data/" not in content, (
2026-05-30T09:16:41.7126429Z             "data/ is in .gitignore â decision log will be lost on every run"
2026-05-30T09:16:41.7126954Z         )
2026-05-30T09:16:41.7127525Z E       AssertionError: data/ is in .gitignore â decision log will be lost on every run
2026-05-30T09:16:41.7128210Z E       assert 'data/' not in '# Python\n_...\n.vscode/\n'
2026-05-30T09:16:41.7128965Z E         
2026-05-30T09:16:41.7129238Z E         'data/' is contained here:
2026-05-30T09:16:41.7129581Z E           e/
2026-05-30T09:16:41.7129833Z E           cache/
2026-05-30T09:16:41.7130104Z E           data/raw/
2026-05-30T09:16:41.7130394Z E           data/live/
2026-05-30T09:16:41.7130695Z E           data/private/
2026-05-30T09:16:41.7131009Z E           data/vendor/
2026-05-30T09:16:41.7131519Z E           evidence/
2026-05-30T09:16:41.7131799Z E           lockbox/
```

```text
2026-05-30T09:16:41.7142480Z E           .DS_Store
2026-05-30T09:16:41.7142758Z E           .idea/
2026-05-30T09:16:41.7143061Z E           .vscode/
2026-05-30T09:16:41.7143243Z 
2026-05-30T09:16:41.7143419Z tests/test_priority_fixes.py:372: AssertionError
2026-05-30T09:16:41.7143939Z =============================== warnings summary ===============================
2026-05-30T09:16:41.7144766Z ../../../../../opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/fastapi/testclient.py:1
2026-05-30T09:16:41.7146487Z   /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
2026-05-30T09:16:41.7148366Z     from starlette.testclient import TestClient as TestClient  # noqa
2026-05-30T09:16:41.7148802Z 
2026-05-30T09:16:41.7149142Z tests/test_jwt_auth.py::test_create_and_validate_token
2026-05-30T09:16:41.7149722Z tests/test_security_layer.py::test_metrics_accepts_admin_token
2026-05-30T09:16:41.7150334Z tests/test_security_layer.py::test_viewer_cannot_access_metrics
2026-05-30T09:16:41.7151989Z   /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/jwt/api_jwt.py:147: InsecureKeyLengthWarning: The HMAC key is 18 bytes long, which is below the minimum recommended length of 32 bytes for SHA256. See RFC 7518 Section 3.2.
2026-05-30T09:16:41.7153435Z     return self._jws.encode(
2026-05-30T09:16:41.7153654Z
```

```text
2026-05-30T09:16:41.7158200Z     decoded = self.decode_complete(
2026-05-30T09:16:41.7158453Z 
2026-05-30T09:16:41.7158795Z -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2026-05-30T09:16:41.7159487Z =========================== short test summary info ============================
2026-05-30T09:16:41.7160964Z FAILED tests/test_priority_fixes.py::TestDataPersistence::test_decision_log_path_not_in_gitignore - AssertionError: data/ is in .gitignore â decision log will be lost on every run
2026-05-30T09:16:41.7162294Z assert 'data/' not in '# Python\n_...\n.vscode/\n'
2026-05-30T09:16:41.7162701Z   
2026-05-30T09:16:41.7162968Z   'data/' is contained here:
2026-05-30T09:16:41.7163280Z     e/
2026-05-30T09:16:41.7163515Z     cache/
2026-05-30T09:16:41.7163768Z     data/raw/
2026-05-30T09:16:41.7164027Z     data/live/
2026-05-30T09:16:41.7164290Z     data/private/
2026-05-30T09:16:41.7164564Z     data/vendor/
2026-05-30T09:16:41.7164831Z     evidence/
2026-05-30T09:16:41.7165085Z     lockbox/
```

```text
2026-05-30T09:16:41.7174817Z     .DS_Store
2026-05-30T09:16:41.7175064Z     .idea/
2026-05-30T09:16:41.7175507Z     .vscode/
2026-05-30T09:16:41.7175840Z 1 failed, 1310 passed, 1 skipped, 7 warnings in 11.44s
2026-05-30T09:16:41.9396500Z ##[error]Process completed with exit code 1.
2026-05-30T09:16:41.9512604Z Post job cleanup.
2026-05-30T09:16:42.0524639Z [command]/usr/bin/git version
2026-05-30T09:16:42.0560185Z git version 2.54.0
2026-05-30T09:16:42.0602287Z Temporarily overriding HOME='/home/runner/work/_temp/49775142-f6ac-425e-aab5-00d4bf90e637' before making global git config changes
2026-05-30T09:16:42.0603566Z Adding repository directory to the temporary git global config as a safe directory
2026-05-30T09:16:42.0608962Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-05-30T09:16:42.0645664Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-05-30T09:16:42.0679276Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-05-30T09:16:42.0922724Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-05-30T09:16:42.0946857Z http.https://github.com/.extraheader
2026-05-30T09:16:42.0958989Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

## Report Quality Validation

- Run ID: `26680160649`
- Branch: `main`
- Commit: `9eab20956193`
- Title: Ignore generated weekly report artifact
- Created: 2026-05-30T09:16:10Z
- Updated: 2026-05-30T09:16:46Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26680160649

### Failed job: validate-reports (weekly)

- Job ID: `78639045502`
- Started: 2026-05-30T09:16:13Z
- Completed: 2026-05-30T09:16:33Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-05-30T09:16:31.0424941Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-05-30T09:16:31.0425330Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-05-30T09:16:31.0425739Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-05-30T09:16:31.0426070Z ##[endgroup]
2026-05-30T09:16:31.3343490Z Traceback (most recent call last):
2026-05-30T09:16:31.3352604Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 247, in <module>
2026-05-30T09:16:31.3353368Z     raise SystemExit(main())
2026-05-30T09:16:31.3353638Z                      ^^^^^^
2026-05-30T09:16:31.3354297Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 236, in main
2026-05-30T09:16:31.3355064Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-05-30T09:16:31.3355514Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-05-30T09:16:31.3356307Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 68, in write_report_text_guarded
2026-05-30T09:16:31.3357449Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-05-30T09:16:31.3358350Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-05-30T09:16:31.3359131Z     raise ReportOutputBoundaryError(
2026-05-30T09:16:31.3360109Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
```

```text
2026-05-30T09:16:31.3357449Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-05-30T09:16:31.3358350Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-05-30T09:16:31.3359131Z     raise ReportOutputBoundaryError(
2026-05-30T09:16:31.3360109Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-05-30T09:16:31.3550358Z ##[error]Process completed with exit code 1.
2026-05-30T09:16:31.3679672Z Post job cleanup.
2026-05-30T09:16:31.4839763Z [command]/usr/bin/git version
2026-05-30T09:16:31.4875820Z git version 2.54.0
2026-05-30T09:16:31.4919273Z Temporarily overriding HOME='/home/runner/work/_temp/732e165e-1fc4-444b-9393-514d2b7d3513' before making global git config changes
2026-05-30T09:16:31.4920624Z Adding repository directory to the temporary git global config as a safe directory
2026-05-30T09:16:31.4925118Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-05-30T09:16:31.4960630Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-05-30T09:16:31.4992624Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-05-30T09:16:31.5221112Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-05-30T09:16:31.5245218Z http.https://github.com/.extraheader
2026-05-30T09:16:31.5259330Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

### Failed job: validate-reports (premarket)

- Job ID: `78639045508`
- Started: 2026-05-30T09:16:12Z
- Completed: 2026-05-30T09:16:45Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-05-30T09:16:27.6835955Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-05-30T09:16:27.6836379Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-05-30T09:16:27.6836817Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-05-30T09:16:27.6837163Z ##[endgroup]
2026-05-30T09:16:43.6851622Z Traceback (most recent call last):
2026-05-30T09:16:43.6860208Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 247, in <module>
2026-05-30T09:16:43.6862180Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-05-30T09:16:43.6864196Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-05-30T09:16:43.6865921Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-05-30T09:16:43.6867040Z WARNING: scanner metric loading failed: ModuleNotFoundError: No module named 'config'
2026-05-30T09:16:43.6867557Z WARNING: scanner_metrics_missing:MSFT
2026-05-30T09:16:43.6867895Z WARNING: scanner_metrics_missing:NVDA
2026-05-30T09:16:43.6868209Z WARNING: scanner_metrics_missing:META
2026-05-30T09:16:43.6868523Z WARNING: scanner_metrics_missing:AAPL
2026-05-30T09:16:43.6868837Z WARNING: scanner_metrics_missing:MU
2026-05-30T09:16:43.6869147Z WARNING: scanner_metrics_missing:QQQ
```

```text
2026-05-30T09:16:43.6860208Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 247, in <module>
2026-05-30T09:16:43.6862180Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-05-30T09:16:43.6864196Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-05-30T09:16:43.6865921Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-05-30T09:16:43.6867040Z WARNING: scanner metric loading failed: ModuleNotFoundError: No module named 'config'
2026-05-30T09:16:43.6867557Z WARNING: scanner_metrics_missing:MSFT
2026-05-30T09:16:43.6867895Z WARNING: scanner_metrics_missing:NVDA
2026-05-30T09:16:43.6868209Z WARNING: scanner_metrics_missing:META
2026-05-30T09:16:43.6868523Z WARNING: scanner_metrics_missing:AAPL
2026-05-30T09:16:43.6868837Z WARNING: scanner_metrics_missing:MU
2026-05-30T09:16:43.6869147Z WARNING: scanner_metrics_missing:QQQ
2026-05-30T09:16:43.6869458Z WARNING: scanner_metrics_missing:GLD
2026-05-30T09:16:43.6869765Z WARNING: scanner_metrics_missing:SLV
2026-05-30T09:16:43.6870205Z     raise SystemExit(main())
2026-05-30T09:16:43.6870485Z                      ^^^^^^
2026-05-30T09:16:43.6871200Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 236, in main
```

```text
2026-05-30T09:16:43.6874686Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-05-30T09:16:43.6875574Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-05-30T09:16:43.6876342Z     raise ReportOutputBoundaryError(
2026-05-30T09:16:43.6877323Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/premarket-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-05-30T09:16:43.7443571Z ##[error]Process completed with exit code 1.
2026-05-30T09:16:43.7568274Z Post job cleanup.
2026-05-30T09:16:43.8553386Z [command]/usr/bin/git version
2026-05-30T09:16:43.8590252Z git version 2.54.0
2026-05-30T09:16:43.8633043Z Temporarily overriding HOME='/home/runner/work/_temp/33576154-2197-4235-9b6c-36309385fedc' before making global git config changes
2026-05-30T09:16:43.8634253Z Adding repository directory to the temporary git global config as a safe directory
2026-05-30T09:16:43.8648142Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-05-30T09:16:43.8682409Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-05-30T09:16:43.8715454Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-05-30T09:16:43.8957074Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-05-30T09:16:43.8982632Z http.https://github.com/.extraheader
2026-05-30T09:16:43.8996393Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

### Failed job: validate-reports (postmarket)

- Job ID: `78639045516`
- Started: 2026-05-30T09:16:12Z
- Completed: 2026-05-30T09:16:44Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-05-30T09:16:28.1991006Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-05-30T09:16:28.1991394Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-05-30T09:16:28.1991802Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-05-30T09:16:28.1992139Z ##[endgroup]
2026-05-30T09:16:43.0995763Z Traceback (most recent call last):
2026-05-30T09:16:43.0997681Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-05-30T09:16:43.1005652Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 247, in <module>
2026-05-30T09:16:43.1006389Z     raise SystemExit(main())
2026-05-30T09:16:43.1006651Z                      ^^^^^^
2026-05-30T09:16:43.1007283Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 236, in main
2026-05-30T09:16:43.1008021Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-05-30T09:16:43.1008478Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-05-30T09:16:43.1009217Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 68, in write_report_text_guarded
2026-05-30T09:16:43.1009987Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-05-30T09:16:43.1010802Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-05-30T09:16:43.1012145Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
```

```text
2026-05-30T09:16:43.1009987Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-05-30T09:16:43.1010802Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-05-30T09:16:43.1012145Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-05-30T09:16:43.1013651Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-05-30T09:16:43.1014539Z WARNING: scanner metric loading failed: ModuleNotFoundError: No module named 'config'
2026-05-30T09:16:43.1014986Z WARNING: scanner_metrics_missing:MSFT
2026-05-30T09:16:43.1015267Z WARNING: scanner_metrics_missing:NVDA
2026-05-30T09:16:43.1015769Z WARNING: scanner_metrics_missing:META
2026-05-30T09:16:43.1016029Z WARNING: scanner_metrics_missing:AAPL
2026-05-30T09:16:43.1016290Z WARNING: scanner_metrics_missing:MU
2026-05-30T09:16:43.1016559Z WARNING: scanner_metrics_missing:QQQ
2026-05-30T09:16:43.1016823Z WARNING: scanner_metrics_missing:GLD
2026-05-30T09:16:43.1017083Z WARNING: scanner_metrics_missing:SLV
2026-05-30T09:16:43.1017380Z     raise ReportOutputBoundaryError(
2026-05-30T09:16:43.1018285Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/postmarket-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-05-30T09:16:43.1623479Z ##[error]Process completed with exit code 1.
```

```text
2026-05-30T09:16:43.1016823Z WARNING: scanner_metrics_missing:GLD
2026-05-30T09:16:43.1017083Z WARNING: scanner_metrics_missing:SLV
2026-05-30T09:16:43.1017380Z     raise ReportOutputBoundaryError(
2026-05-30T09:16:43.1018285Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/postmarket-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-05-30T09:16:43.1623479Z ##[error]Process completed with exit code 1.
2026-05-30T09:16:43.1747767Z Post job cleanup.
2026-05-30T09:16:43.2756763Z [command]/usr/bin/git version
2026-05-30T09:16:43.2793352Z git version 2.54.0
2026-05-30T09:16:43.2833934Z Temporarily overriding HOME='/home/runner/work/_temp/d2300cde-3220-43ac-bc99-410db08dca07' before making global git config changes
2026-05-30T09:16:43.2835179Z Adding repository directory to the temporary git global config as a safe directory
2026-05-30T09:16:43.2839958Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-05-30T09:16:43.2884998Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-05-30T09:16:43.2918352Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-05-30T09:16:43.3177244Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-05-30T09:16:43.3209067Z http.https://github.com/.extraheader
2026-05-30T09:16:43.3221912Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

## CI

- Run ID: `26680108564`
- Branch: `main`
- Commit: `f1a6a0de2c10`
- Title: CI
- Created: 2026-05-30T09:13:27Z
- Updated: 2026-05-30T09:14:16Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26680108564

### Failed job: Pytest

- Job ID: `78638908422`
- Started: 2026-05-30T09:13:30Z
- Completed: 2026-05-30T09:14:15Z
- Failed steps: 45. IP5/IP6 artifact hygiene tests

#### Error context

```text
2026-05-30T09:14:12.4072480Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-05-30T09:14:12.4072823Z   POLYGON_API_KEY: test-key
2026-05-30T09:14:12.4073064Z ##[endgroup]
2026-05-30T09:14:12.6947181Z F.                                                                       [100%]
2026-05-30T09:14:12.6947867Z =================================== FAILURES ===================================
2026-05-30T09:14:12.6948540Z __________ test_gitignore_blocks_private_edge_and_generated_artifacts __________
2026-05-30T09:14:12.6948999Z 
2026-05-30T09:14:12.6949325Z     def test_gitignore_blocks_private_edge_and_generated_artifacts() -> None:
2026-05-30T09:14:12.6949945Z         content = GITIGNORE.read_text(encoding="utf-8")
2026-05-30T09:14:12.6950359Z     
2026-05-30T09:14:12.6950852Z         missing = [pattern for pattern in REQUIRED_GITIGNORE_PATTERNS if pattern not in content]
2026-05-30T09:14:12.6951521Z     
2026-05-30T09:14:12.6951823Z >       assert missing == []
2026-05-30T09:14:12.6952278Z E       AssertionError: assert ['reports/weekly-report.md'] == []
2026-05-30T09:14:12.6952651Z E         
2026-05-30T09:14:12.6952948Z E         Left contains one more item: 'reports/weekly-report.md'
```

```text
2026-05-30T09:14:12.6950359Z     
2026-05-30T09:14:12.6950852Z         missing = [pattern for pattern in REQUIRED_GITIGNORE_PATTERNS if pattern not in content]
2026-05-30T09:14:12.6951521Z     
2026-05-30T09:14:12.6951823Z >       assert missing == []
2026-05-30T09:14:12.6952278Z E       AssertionError: assert ['reports/weekly-report.md'] == []
2026-05-30T09:14:12.6952651Z E         
2026-05-30T09:14:12.6952948Z E         Left contains one more item: 'reports/weekly-report.md'
2026-05-30T09:14:12.6953282Z E         
2026-05-30T09:14:12.6953489Z E         Full diff:
2026-05-30T09:14:12.6953730Z E         - []
2026-05-30T09:14:12.6954326Z E         + [
2026-05-30T09:14:12.6954557Z E         +     'reports/weekly-report.md',
2026-05-30T09:14:12.6954838Z E         + ]
2026-05-30T09:14:12.6954957Z 
2026-05-30T09:14:12.6955095Z tests/test_artifact_hygiene.py:76: AssertionError
2026-05-30T09:14:12.6955668Z =========================== short test summary info ============================
```

```text
2026-05-30T09:14:12.6954326Z E         + [
2026-05-30T09:14:12.6954557Z E         +     'reports/weekly-report.md',
2026-05-30T09:14:12.6954838Z E         + ]
2026-05-30T09:14:12.6954957Z 
2026-05-30T09:14:12.6955095Z tests/test_artifact_hygiene.py:76: AssertionError
2026-05-30T09:14:12.6955668Z =========================== short test summary info ============================
2026-05-30T09:14:12.6956555Z FAILED tests/test_artifact_hygiene.py::test_gitignore_blocks_private_edge_and_generated_artifacts - AssertionError: assert ['reports/weekly-report.md'] == []
2026-05-30T09:14:12.6957206Z   
2026-05-30T09:14:12.6957484Z   Left contains one more item: 'reports/weekly-report.md'
2026-05-30T09:14:12.6957806Z   
2026-05-30T09:14:12.6957994Z   Full diff:
2026-05-30T09:14:12.6958200Z   - []
2026-05-30T09:14:12.6958395Z   + [
2026-05-30T09:14:12.6958613Z   +     'reports/weekly-report.md',
2026-05-30T09:14:12.6958871Z   + ]
2026-05-30T09:14:12.6959081Z 1 failed, 1 passed in 0.05s
```

```text
2026-05-30T09:14:12.6954838Z E         + ]
2026-05-30T09:14:12.6954957Z 
2026-05-30T09:14:12.6955095Z tests/test_artifact_hygiene.py:76: AssertionError
2026-05-30T09:14:12.6955668Z =========================== short test summary info ============================
2026-05-30T09:14:12.6956555Z FAILED tests/test_artifact_hygiene.py::test_gitignore_blocks_private_edge_and_generated_artifacts - AssertionError: assert ['reports/weekly-report.md'] == []
2026-05-30T09:14:12.6957206Z   
2026-05-30T09:14:12.6957484Z   Left contains one more item: 'reports/weekly-report.md'
2026-05-30T09:14:12.6957806Z   
2026-05-30T09:14:12.6957994Z   Full diff:
2026-05-30T09:14:12.6958200Z   - []
2026-05-30T09:14:12.6958395Z   + [
2026-05-30T09:14:12.6958613Z   +     'reports/weekly-report.md',
2026-05-30T09:14:12.6958871Z   + ]
2026-05-30T09:14:12.6959081Z 1 failed, 1 passed in 0.05s
2026-05-30T09:14:12.7266554Z ##[error]Process completed with exit code 1.
2026-05-30T09:14:12.7395182Z Post job cleanup.
```

```text
2026-05-30T09:14:12.6958395Z   + [
2026-05-30T09:14:12.6958613Z   +     'reports/weekly-report.md',
2026-05-30T09:14:12.6958871Z   + ]
2026-05-30T09:14:12.6959081Z 1 failed, 1 passed in 0.05s
2026-05-30T09:14:12.7266554Z ##[error]Process completed with exit code 1.
2026-05-30T09:14:12.7395182Z Post job cleanup.
2026-05-30T09:14:12.8373559Z [command]/usr/bin/git version
2026-05-30T09:14:12.8410779Z git version 2.54.0
2026-05-30T09:14:12.8452910Z Temporarily overriding HOME='/home/runner/work/_temp/bb17723b-7473-40ea-aac9-a7e5e641c887' before making global git config changes
2026-05-30T09:14:12.8454205Z Adding repository directory to the temporary git global config as a safe directory
2026-05-30T09:14:12.8459836Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-05-30T09:14:12.8497580Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-05-30T09:14:12.8530929Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-05-30T09:14:12.8771737Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-05-30T09:14:12.8795989Z http.https://github.com/.extraheader
2026-05-30T09:14:12.8808439Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

## CI

- Run ID: `26680060527`
- Branch: `main`
- Commit: `f1a6a0de2c10`
- Title: Treat weekly report as generated artifact in hygiene guard
- Created: 2026-05-30T09:10:57Z
- Updated: 2026-05-30T09:11:41Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26680060527

### Failed job: Pytest

- Job ID: `78638781796`
- Started: 2026-05-30T09:10:59Z
- Completed: 2026-05-30T09:11:40Z
- Failed steps: 45. IP5/IP6 artifact hygiene tests

#### Error context

```text
2026-05-30T09:11:36.7855203Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-05-30T09:11:36.7855533Z   POLYGON_API_KEY: test-key
2026-05-30T09:11:36.7855754Z ##[endgroup]
2026-05-30T09:11:37.0669142Z F.                                                                       [100%]
2026-05-30T09:11:37.0670040Z =================================== FAILURES ===================================
2026-05-30T09:11:37.0671368Z __________ test_gitignore_blocks_private_edge_and_generated_artifacts __________
2026-05-30T09:11:37.0672060Z 
2026-05-30T09:11:37.0672483Z     def test_gitignore_blocks_private_edge_and_generated_artifacts() -> None:
2026-05-30T09:11:37.0673022Z         content = GITIGNORE.read_text(encoding="utf-8")
2026-05-30T09:11:37.0673328Z     
2026-05-30T09:11:37.0673689Z         missing = [pattern for pattern in REQUIRED_GITIGNORE_PATTERNS if pattern not in content]
2026-05-30T09:11:37.0674131Z     
2026-05-30T09:11:37.0674315Z >       assert missing == []
2026-05-30T09:11:37.0674643Z E       AssertionError: assert ['reports/weekly-report.md'] == []
2026-05-30T09:11:37.0674993Z E         
2026-05-30T09:11:37.0675255Z E         Left contains one more item: 'reports/weekly-report.md'
```

```text
2026-05-30T09:11:37.0673328Z     
2026-05-30T09:11:37.0673689Z         missing = [pattern for pattern in REQUIRED_GITIGNORE_PATTERNS if pattern not in content]
2026-05-30T09:11:37.0674131Z     
2026-05-30T09:11:37.0674315Z >       assert missing == []
2026-05-30T09:11:37.0674643Z E       AssertionError: assert ['reports/weekly-report.md'] == []
2026-05-30T09:11:37.0674993Z E         
2026-05-30T09:11:37.0675255Z E         Left contains one more item: 'reports/weekly-report.md'
2026-05-30T09:11:37.0675575Z E         
2026-05-30T09:11:37.0675749Z E         Full diff:
2026-05-30T09:11:37.0675958Z E         - []
2026-05-30T09:11:37.0676420Z E         + [
2026-05-30T09:11:37.0676630Z E         +     'reports/weekly-report.md',
2026-05-30T09:11:37.0676893Z E         + ]
2026-05-30T09:11:37.0677005Z 
2026-05-30T09:11:37.0677132Z tests/test_artifact_hygiene.py:76: AssertionError
2026-05-30T09:11:37.0677496Z =========================== short test summary info ============================
```

```text
2026-05-30T09:11:37.0676420Z E         + [
2026-05-30T09:11:37.0676630Z E         +     'reports/weekly-report.md',
2026-05-30T09:11:37.0676893Z E         + ]
2026-05-30T09:11:37.0677005Z 
2026-05-30T09:11:37.0677132Z tests/test_artifact_hygiene.py:76: AssertionError
2026-05-30T09:11:37.0677496Z =========================== short test summary info ============================
2026-05-30T09:11:37.0678345Z FAILED tests/test_artifact_hygiene.py::test_gitignore_blocks_private_edge_and_generated_artifacts - AssertionError: assert ['reports/weekly-report.md'] == []
2026-05-30T09:11:37.0679018Z   
2026-05-30T09:11:37.0679258Z   Left contains one more item: 'reports/weekly-report.md'
2026-05-30T09:11:37.0679569Z   
2026-05-30T09:11:37.0679732Z   Full diff:
2026-05-30T09:11:37.0679907Z   - []
2026-05-30T09:11:37.0680076Z   + [
2026-05-30T09:11:37.0680265Z   +     'reports/weekly-report.md',
2026-05-30T09:11:37.0680508Z   + ]
2026-05-30T09:11:37.0680694Z 1 failed, 1 passed in 0.05s
```

```text
2026-05-30T09:11:37.0676893Z E         + ]
2026-05-30T09:11:37.0677005Z 
2026-05-30T09:11:37.0677132Z tests/test_artifact_hygiene.py:76: AssertionError
2026-05-30T09:11:37.0677496Z =========================== short test summary info ============================
2026-05-30T09:11:37.0678345Z FAILED tests/test_artifact_hygiene.py::test_gitignore_blocks_private_edge_and_generated_artifacts - AssertionError: assert ['reports/weekly-report.md'] == []
2026-05-30T09:11:37.0679018Z   
2026-05-30T09:11:37.0679258Z   Left contains one more item: 'reports/weekly-report.md'
2026-05-30T09:11:37.0679569Z   
2026-05-30T09:11:37.0679732Z   Full diff:
2026-05-30T09:11:37.0679907Z   - []
2026-05-30T09:11:37.0680076Z   + [
2026-05-30T09:11:37.0680265Z   +     'reports/weekly-report.md',
2026-05-30T09:11:37.0680508Z   + ]
2026-05-30T09:11:37.0680694Z 1 failed, 1 passed in 0.05s
2026-05-30T09:11:37.0929247Z ##[error]Process completed with exit code 1.
2026-05-30T09:11:37.1057274Z Post job cleanup.
```

```text
2026-05-30T09:11:37.0680076Z   + [
2026-05-30T09:11:37.0680265Z   +     'reports/weekly-report.md',
2026-05-30T09:11:37.0680508Z   + ]
2026-05-30T09:11:37.0680694Z 1 failed, 1 passed in 0.05s
2026-05-30T09:11:37.0929247Z ##[error]Process completed with exit code 1.
2026-05-30T09:11:37.1057274Z Post job cleanup.
2026-05-30T09:11:37.2022750Z [command]/usr/bin/git version
2026-05-30T09:11:37.2058270Z git version 2.54.0
2026-05-30T09:11:37.2103774Z Temporarily overriding HOME='/home/runner/work/_temp/0877f984-74ae-407f-9c79-c1231ca7fca0' before making global git config changes
2026-05-30T09:11:37.2105204Z Adding repository directory to the temporary git global config as a safe directory
2026-05-30T09:11:37.2118623Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-05-30T09:11:37.2152177Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-05-30T09:11:37.2183913Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-05-30T09:11:37.2410174Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-05-30T09:11:37.2434165Z http.https://github.com/.extraheader
2026-05-30T09:11:37.2448574Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

## Report Quality Validation

- Run ID: `26680060538`
- Branch: `main`
- Commit: `f1a6a0de2c10`
- Title: Treat weekly report as generated artifact in hygiene guard
- Created: 2026-05-30T09:10:57Z
- Updated: 2026-05-30T09:11:34Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26680060538

### Failed job: validate-reports (postmarket)

- Job ID: `78638781786`
- Started: 2026-05-30T09:10:59Z
- Completed: 2026-05-30T09:11:33Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-05-30T09:11:15.5281746Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-05-30T09:11:15.5282131Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-05-30T09:11:15.5282559Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-05-30T09:11:15.5282907Z ##[endgroup]
2026-05-30T09:11:31.6983210Z Traceback (most recent call last):
2026-05-30T09:11:31.6991333Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 247, in <module>
2026-05-30T09:11:31.6993918Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-05-30T09:11:31.6995176Z     raise SystemExit(main())
2026-05-30T09:11:31.6995432Z                      ^^^^^^
2026-05-30T09:11:31.6996106Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 236, in main
2026-05-30T09:11:31.6996845Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-05-30T09:11:31.6997324Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-05-30T09:11:31.6998068Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 68, in write_report_text_guarded
2026-05-30T09:11:31.6998852Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-05-30T09:11:31.6999688Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-05-30T09:11:31.7000409Z     raise ReportOutputBoundaryError(
```

```text
2026-05-30T09:11:31.7000409Z     raise ReportOutputBoundaryError(
2026-05-30T09:11:31.7001343Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/postmarket-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-05-30T09:11:31.7002904Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-05-30T09:11:31.7004505Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-05-30T09:11:31.7005697Z WARNING: scanner metric loading failed: ModuleNotFoundError: No module named 'config'
2026-05-30T09:11:31.7006127Z WARNING: scanner_metrics_missing:MSFT
2026-05-30T09:11:31.7006403Z WARNING: scanner_metrics_missing:NVDA
2026-05-30T09:11:31.7006666Z WARNING: scanner_metrics_missing:META
2026-05-30T09:11:31.7006932Z WARNING: scanner_metrics_missing:AAPL
2026-05-30T09:11:31.7007212Z WARNING: scanner_metrics_missing:MU
2026-05-30T09:11:31.7007478Z WARNING: scanner_metrics_missing:QQQ
2026-05-30T09:11:31.7007743Z WARNING: scanner_metrics_missing:GLD
2026-05-30T09:11:31.7008003Z WARNING: scanner_metrics_missing:SLV
2026-05-30T09:11:31.7640866Z ##[error]Process completed with exit code 1.
2026-05-30T09:11:31.7763494Z Post job cleanup.
2026-05-30T09:11:31.8772699Z [command]/usr/bin/git version
```

```text
2026-05-30T09:11:31.7007212Z WARNING: scanner_metrics_missing:MU
2026-05-30T09:11:31.7007478Z WARNING: scanner_metrics_missing:QQQ
2026-05-30T09:11:31.7007743Z WARNING: scanner_metrics_missing:GLD
2026-05-30T09:11:31.7008003Z WARNING: scanner_metrics_missing:SLV
2026-05-30T09:11:31.7640866Z ##[error]Process completed with exit code 1.
2026-05-30T09:11:31.7763494Z Post job cleanup.
2026-05-30T09:11:31.8772699Z [command]/usr/bin/git version
2026-05-30T09:11:31.8810762Z git version 2.54.0
2026-05-30T09:11:31.8853096Z Temporarily overriding HOME='/home/runner/work/_temp/107e11d7-744a-4b3f-a6d9-214fd436d719' before making global git config changes
2026-05-30T09:11:31.8854504Z Adding repository directory to the temporary git global config as a safe directory
2026-05-30T09:11:31.8867724Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-05-30T09:11:31.8906835Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-05-30T09:11:31.8942516Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-05-30T09:11:31.9209517Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-05-30T09:11:31.9240471Z http.https://github.com/.extraheader
2026-05-30T09:11:31.9254876Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

### Failed job: validate-reports (weekly)

- Job ID: `78638781792`
- Started: 2026-05-30T09:10:59Z
- Completed: 2026-05-30T09:11:18Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-05-30T09:11:15.6853314Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-05-30T09:11:15.6853705Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-05-30T09:11:15.6854138Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-05-30T09:11:15.6854467Z ##[endgroup]
2026-05-30T09:11:16.2796080Z Traceback (most recent call last):
2026-05-30T09:11:16.2805873Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 247, in <module>
2026-05-30T09:11:16.2807171Z     raise SystemExit(main())
2026-05-30T09:11:16.2807544Z                      ^^^^^^
2026-05-30T09:11:16.2808514Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 236, in main
2026-05-30T09:11:16.2809704Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-05-30T09:11:16.2810393Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-05-30T09:11:16.2811621Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 68, in write_report_text_guarded
2026-05-30T09:11:16.2813174Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-05-30T09:11:16.2814569Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-05-30T09:11:16.2815765Z     raise ReportOutputBoundaryError(
2026-05-30T09:11:16.2817246Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
```

```text
2026-05-30T09:11:16.2813174Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-05-30T09:11:16.2814569Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-05-30T09:11:16.2815765Z     raise ReportOutputBoundaryError(
2026-05-30T09:11:16.2817246Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/weekly-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-05-30T09:11:16.3041363Z ##[error]Process completed with exit code 1.
2026-05-30T09:11:16.3167899Z Post job cleanup.
2026-05-30T09:11:16.4144491Z [command]/usr/bin/git version
2026-05-30T09:11:16.4180992Z git version 2.54.0
2026-05-30T09:11:16.4224492Z Temporarily overriding HOME='/home/runner/work/_temp/fc89bba3-93ac-46f9-bcb4-bc7e6cd6de9c' before making global git config changes
2026-05-30T09:11:16.4225756Z Adding repository directory to the temporary git global config as a safe directory
2026-05-30T09:11:16.4230485Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-05-30T09:11:16.4267654Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-05-30T09:11:16.4300992Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-05-30T09:11:16.4538328Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-05-30T09:11:16.4565424Z http.https://github.com/.extraheader
2026-05-30T09:11:16.4578110Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

### Failed job: validate-reports (premarket)

- Job ID: `78638781795`
- Started: 2026-05-30T09:10:59Z
- Completed: 2026-05-30T09:11:31Z
- Failed steps: 5. Generate report

#### Error context

```text
2026-05-30T09:11:14.0943777Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-05-30T09:11:14.0944180Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-05-30T09:11:14.0944606Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-05-30T09:11:14.0944965Z ##[endgroup]
2026-05-30T09:11:29.7894039Z Traceback (most recent call last):
2026-05-30T09:11:29.7896158Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 1/3 in 2.0s
2026-05-30T09:11:29.7905715Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 247, in <module>
2026-05-30T09:11:29.7906777Z     raise SystemExit(main())
2026-05-30T09:11:29.7907145Z                      ^^^^^^
2026-05-30T09:11:29.7908052Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/generate_report.py", line 236, in main
2026-05-30T09:11:29.7909167Z     output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
2026-05-30T09:11:29.7909875Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-05-30T09:11:29.7911031Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 68, in write_report_text_guarded
2026-05-30T09:11:29.7912213Z     assert_report_output_path_allowed(output_path, repo_root=repo_root)
2026-05-30T09:11:29.7913692Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/report_output_boundary.py", line 54, in assert_report_output_path_allowed
2026-05-30T09:11:29.7914869Z     raise ReportOutputBoundaryError(
```

```text
2026-05-30T09:11:29.7914869Z     raise ReportOutputBoundaryError(
2026-05-30T09:11:29.7916329Z src.report_output_boundary.ReportOutputBoundaryError: Refusing generated report write to protected public artifact: reports/premarket-report.md. Use a non-committed output directory instead. Boundary=report-output-boundary-v1.
2026-05-30T09:11:29.7918848Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 2/3 in 4.0s
2026-05-30T09:11:29.7920994Z Polygon request failed: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-26/2026-05-30?adjusted=true&sort=asc&limit=260&apiKey=***. Retry 3/3 in 6.0s
2026-05-30T09:11:29.7922765Z WARNING: scanner metric loading failed: ModuleNotFoundError: No module named 'config'
2026-05-30T09:11:29.7923584Z WARNING: scanner_metrics_missing:MSFT
2026-05-30T09:11:29.7924003Z WARNING: scanner_metrics_missing:NVDA
2026-05-30T09:11:29.7924416Z WARNING: scanner_metrics_missing:META
2026-05-30T09:11:29.7924815Z WARNING: scanner_metrics_missing:AAPL
2026-05-30T09:11:29.7925217Z WARNING: scanner_metrics_missing:MU
2026-05-30T09:11:29.7925624Z WARNING: scanner_metrics_missing:QQQ
2026-05-30T09:11:29.7926020Z WARNING: scanner_metrics_missing:GLD
2026-05-30T09:11:29.7926425Z WARNING: scanner_metrics_missing:SLV
2026-05-30T09:11:29.8458722Z ##[error]Process completed with exit code 1.
2026-05-30T09:11:29.8581556Z Post job cleanup.
2026-05-30T09:11:29.9552985Z [command]/usr/bin/git version
```

```text
2026-05-30T09:11:29.7925217Z WARNING: scanner_metrics_missing:MU
2026-05-30T09:11:29.7925624Z WARNING: scanner_metrics_missing:QQQ
2026-05-30T09:11:29.7926020Z WARNING: scanner_metrics_missing:GLD
2026-05-30T09:11:29.7926425Z WARNING: scanner_metrics_missing:SLV
2026-05-30T09:11:29.8458722Z ##[error]Process completed with exit code 1.
2026-05-30T09:11:29.8581556Z Post job cleanup.
2026-05-30T09:11:29.9552985Z [command]/usr/bin/git version
2026-05-30T09:11:29.9588933Z git version 2.54.0
2026-05-30T09:11:29.9631069Z Temporarily overriding HOME='/home/runner/work/_temp/5b94aafa-fec5-473a-8792-58670547b6bf' before making global git config changes
2026-05-30T09:11:29.9632374Z Adding repository directory to the temporary git global config as a safe directory
2026-05-30T09:11:29.9644891Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-05-30T09:11:29.9681331Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-05-30T09:11:29.9714269Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-05-30T09:11:29.9960703Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-05-30T09:11:29.9986931Z http.https://github.com/.extraheader
2026-05-30T09:11:30.0003318Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

## Decision Engine Tests

- Run ID: `26680060539`
- Branch: `main`
- Commit: `f1a6a0de2c10`
- Title: Treat weekly report as generated artifact in hygiene guard
- Created: 2026-05-30T09:10:57Z
- Updated: 2026-05-30T09:11:29Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26680060539

### Failed job: tests

- Job ID: `78638781738`
- Started: 2026-05-30T09:10:59Z
- Completed: 2026-05-30T09:11:28Z
- Failed steps: 5. Run pytest

#### Error context

```text
2026-05-30T09:11:26.0170913Z ........................................................................ [ 87%]
2026-05-30T09:11:26.2243835Z ........................................................................ [ 93%]
2026-05-30T09:11:26.2622795Z ........................................................................ [ 98%]
2026-05-30T09:11:26.6917083Z ................                                                         [100%]
2026-05-30T09:11:26.6918159Z =================================== FAILURES ===================================
2026-05-30T09:11:26.6919305Z __________ test_gitignore_blocks_private_edge_and_generated_artifacts __________
2026-05-30T09:11:26.6919752Z 
2026-05-30T09:11:26.6920112Z     def test_gitignore_blocks_private_edge_and_generated_artifacts() -> None:
2026-05-30T09:11:26.6920778Z         content = GITIGNORE.read_text(encoding="utf-8")
2026-05-30T09:11:26.6921226Z     
2026-05-30T09:11:26.6921770Z         missing = [pattern for pattern in REQUIRED_GITIGNORE_PATTERNS if pattern not in content]
2026-05-30T09:11:26.6922457Z     
2026-05-30T09:11:26.6922747Z >       assert missing == []
2026-05-30T09:11:26.6923245Z E       AssertionError: assert ['reports/weekly-report.md'] == []
2026-05-30T09:11:26.6923764Z E         
2026-05-30T09:11:26.6924166Z E         Left contains one more item: 'reports/weekly-report.md'
```

```text
2026-05-30T09:11:26.6921226Z     
2026-05-30T09:11:26.6921770Z         missing = [pattern for pattern in REQUIRED_GITIGNORE_PATTERNS if pattern not in content]
2026-05-30T09:11:26.6922457Z     
2026-05-30T09:11:26.6922747Z >       assert missing == []
2026-05-30T09:11:26.6923245Z E       AssertionError: assert ['reports/weekly-report.md'] == []
2026-05-30T09:11:26.6923764Z E         
2026-05-30T09:11:26.6924166Z E         Left contains one more item: 'reports/weekly-report.md'
2026-05-30T09:11:26.6924671Z E         
2026-05-30T09:11:26.6925202Z E         Full diff:
2026-05-30T09:11:26.6925521Z E         - []
2026-05-30T09:11:26.6925814Z E         + [
2026-05-30T09:11:26.6926154Z E         +     'reports/weekly-report.md',
2026-05-30T09:11:26.6926556Z E         + ]
2026-05-30T09:11:26.6927051Z 
2026-05-30T09:11:26.6927258Z tests/test_artifact_hygiene.py:76: AssertionError
2026-05-30T09:11:26.6927941Z _________ TestDataPersistence.test_decision_log_path_not_in_gitignore __________
```

```text
2026-05-30T09:11:26.6925814Z E         + [
2026-05-30T09:11:26.6926154Z E         +     'reports/weekly-report.md',
2026-05-30T09:11:26.6926556Z E         + ]
2026-05-30T09:11:26.6927051Z 
2026-05-30T09:11:26.6927258Z tests/test_artifact_hygiene.py:76: AssertionError
2026-05-30T09:11:26.6927941Z _________ TestDataPersistence.test_decision_log_path_not_in_gitignore __________
2026-05-30T09:11:26.6928446Z 
2026-05-30T09:11:26.6928689Z self = <test_priority_fixes.TestDataPersistence object at 0x7fcf9c2fec10>
2026-05-30T09:11:26.6928996Z 
2026-05-30T09:11:26.6929134Z     def test_decision_log_path_not_in_gitignore(self):
2026-05-30T09:11:26.6929464Z         gitignore = Path(".gitignore")
2026-05-30T09:11:26.6929743Z         if not gitignore.exists():
2026-05-30T09:11:26.6929997Z             return
2026-05-30T09:11:26.6930220Z         content = gitignore.read_text()
2026-05-30T09:11:26.6930497Z         # data/ should NOT be in gitignore
2026-05-30T09:11:26.6930772Z >       assert "data/" not in content, (
```

```text
2026-05-30T09:11:26.6930497Z         # data/ should NOT be in gitignore
2026-05-30T09:11:26.6930772Z >       assert "data/" not in content, (
2026-05-30T09:11:26.6931402Z             "data/ is in .gitignore â decision log will be lost on every run"
2026-05-30T09:11:26.6931760Z         )
2026-05-30T09:11:26.6932164Z E       AssertionError: data/ is in .gitignore â decision log will be lost on every run
2026-05-30T09:11:26.6932622Z E       assert 'data/' not in '# Python\n_...\n.vscode/\n'
2026-05-30T09:11:26.6932918Z E         
2026-05-30T09:11:26.6933118Z E         'data/' is contained here:
2026-05-30T09:11:26.6933365Z E           e/
2026-05-30T09:11:26.6933565Z E           cache/
2026-05-30T09:11:26.6933772Z E           data/raw/
2026-05-30T09:11:26.6933998Z E           data/live/
2026-05-30T09:11:26.6934226Z E           data/private/
2026-05-30T09:11:26.6934468Z E           data/vendor/
2026-05-30T09:11:26.6934687Z E           evidence/
2026-05-30T09:11:26.6934894Z E           lockbox/
```

```text
2026-05-30T09:11:26.6942949Z E           .DS_Store
2026-05-30T09:11:26.6943149Z E           .idea/
2026-05-30T09:11:26.6943360Z E           .vscode/
2026-05-30T09:11:26.6943481Z 
2026-05-30T09:11:26.6943611Z tests/test_priority_fixes.py:372: AssertionError
2026-05-30T09:11:26.6943956Z =============================== warnings summary ===============================
2026-05-30T09:11:26.6944524Z ../../../../../opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/fastapi/testclient.py:1
2026-05-30T09:11:26.6945984Z   /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
2026-05-30T09:11:26.6946926Z     from starlette.testclient import TestClient as TestClient  # noqa
2026-05-30T09:11:26.6947206Z 
2026-05-30T09:11:26.6947495Z tests/test_jwt_auth.py::test_create_and_validate_token
2026-05-30T09:11:26.6947900Z tests/test_security_layer.py::test_metrics_accepts_admin_token
2026-05-30T09:11:26.6948320Z tests/test_security_layer.py::test_viewer_cannot_access_metrics
2026-05-30T09:11:26.6949298Z   /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/jwt/api_jwt.py:147: InsecureKeyLengthWarning: The HMAC key is 18 bytes long, which is below the minimum recommended length of 32 bytes for SHA256. See RFC 7518 Section 3.2.
2026-05-30T09:11:26.6950216Z     return self._jws.encode(
2026-05-30T09:11:26.6950369Z
```

```text
2026-05-30T09:11:26.6953124Z     decoded = self.decode_complete(
2026-05-30T09:11:26.6953310Z 
2026-05-30T09:11:26.6953528Z -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2026-05-30T09:11:26.6953982Z =========================== short test summary info ============================
2026-05-30T09:11:26.6954711Z FAILED tests/test_artifact_hygiene.py::test_gitignore_blocks_private_edge_and_generated_artifacts - AssertionError: assert ['reports/weekly-report.md'] == []
2026-05-30T09:11:26.6955555Z   
2026-05-30T09:11:26.6955820Z   Left contains one more item: 'reports/weekly-report.md'
2026-05-30T09:11:26.6956131Z   
2026-05-30T09:11:26.6956315Z   Full diff:
2026-05-30T09:11:26.6956511Z   - []
2026-05-30T09:11:26.6956691Z   + [
2026-05-30T09:11:26.6956890Z   +     'reports/weekly-report.md',
2026-05-30T09:11:26.6957148Z   + ]
2026-05-30T09:11:26.6957951Z FAILED tests/test_priority_fixes.py::TestDataPersistence::test_decision_log_path_not_in_gitignore - AssertionError: data/ is in .gitignore â decision log will be lost on every run
2026-05-30T09:11:26.6958692Z assert 'data/' not in '# Python\n_...\n.vscode/\n'
2026-05-30T09:11:26.6958978Z
```

```text
2026-05-30T09:11:26.6956511Z   - []
2026-05-30T09:11:26.6956691Z   + [
2026-05-30T09:11:26.6956890Z   +     'reports/weekly-report.md',
2026-05-30T09:11:26.6957148Z   + ]
2026-05-30T09:11:26.6957951Z FAILED tests/test_priority_fixes.py::TestDataPersistence::test_decision_log_path_not_in_gitignore - AssertionError: data/ is in .gitignore â decision log will be lost on every run
2026-05-30T09:11:26.6958692Z assert 'data/' not in '# Python\n_...\n.vscode/\n'
2026-05-30T09:11:26.6958978Z   
2026-05-30T09:11:26.6959187Z   'data/' is contained here:
2026-05-30T09:11:26.6959422Z     e/
2026-05-30T09:11:26.6959603Z     cache/
2026-05-30T09:11:26.6959793Z     data/raw/
2026-05-30T09:11:26.6959986Z     data/live/
2026-05-30T09:11:26.6960180Z     data/private/
2026-05-30T09:11:26.6960379Z     data/vendor/
2026-05-30T09:11:26.6960589Z     evidence/
2026-05-30T09:11:26.6960934Z     lockbox/
```

```text
2026-05-30T09:11:26.6968173Z     .DS_Store
2026-05-30T09:11:26.6968355Z     .idea/
2026-05-30T09:11:26.6968539Z     .vscode/
2026-05-30T09:11:26.6968785Z 2 failed, 1309 passed, 1 skipped, 7 warnings in 11.40s
2026-05-30T09:11:26.9741844Z ##[error]Process completed with exit code 1.
2026-05-30T09:11:26.9855811Z Post job cleanup.
2026-05-30T09:11:27.0820068Z [command]/usr/bin/git version
2026-05-30T09:11:27.0861037Z git version 2.54.0
2026-05-30T09:11:27.0901381Z Temporarily overriding HOME='/home/runner/work/_temp/526227df-0321-4f0e-95d6-6ed1f1b68257' before making global git config changes
2026-05-30T09:11:27.0902406Z Adding repository directory to the temporary git global config as a safe directory
2026-05-30T09:11:27.0908973Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-05-30T09:11:27.0946310Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-05-30T09:11:27.0979402Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-05-30T09:11:27.1227879Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-05-30T09:11:27.1251956Z http.https://github.com/.extraheader
2026-05-30T09:11:27.1266494Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

## CI

- Run ID: `26679770706`
- Branch: `main`
- Commit: `111b1b5293ae`
- Title: CI
- Created: 2026-05-30T08:55:58Z
- Updated: 2026-05-30T08:56:40Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26679770706

### Failed job: Pytest

- Job ID: `78638014629`
- Started: 2026-05-30T08:56:01Z
- Completed: 2026-05-30T08:56:39Z
- Failed steps: 45. IP5/IP6 artifact hygiene tests

#### Error context

```text
2026-05-30T08:56:37.1198153Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-05-30T08:56:37.1198490Z   POLYGON_API_KEY: test-key
2026-05-30T08:56:37.1198723Z ##[endgroup]
2026-05-30T08:56:37.4118957Z .F                                                                       [100%]
2026-05-30T08:56:37.4119829Z =================================== FAILURES ===================================
2026-05-30T08:56:37.4120768Z _______________ test_public_reports_are_synthetic_examples_only ________________
2026-05-30T08:56:37.4121697Z 
2026-05-30T08:56:37.4122109Z     def test_public_reports_are_synthetic_examples_only() -> None:
2026-05-30T08:56:37.4122867Z         for report_path in PUBLIC_REPORTS:
2026-05-30T08:56:37.4123521Z             content = report_path.read_text(encoding="utf-8")
2026-05-30T08:56:37.4123968Z     
2026-05-30T08:56:37.4124218Z >           assert "Synthetic example: yes" in content
2026-05-30T08:56:37.4125952Z E           AssertionError: assert 'Synthetic example: yes' in '# Institutional Trading Engine â WEEKLY REPORT\n\nGenerated: 2026-05-30 08:51 UTC\n\n## Weekly Summary\n\nThis report...s share the same sector or factor risk.\n- Treat all outputs as research and decision support, not financial advice.\n'
2026-05-30T08:56:37.4127182Z 
2026-05-30T08:56:37.4127341Z tests/test_artifact_hygiene.py:83: AssertionError
2026-05-30T08:56:37.4128094Z =========================== short test summary info ============================
```

```text
2026-05-30T08:56:37.4122867Z         for report_path in PUBLIC_REPORTS:
2026-05-30T08:56:37.4123521Z             content = report_path.read_text(encoding="utf-8")
2026-05-30T08:56:37.4123968Z     
2026-05-30T08:56:37.4124218Z >           assert "Synthetic example: yes" in content
2026-05-30T08:56:37.4125952Z E           AssertionError: assert 'Synthetic example: yes' in '# Institutional Trading Engine â WEEKLY REPORT\n\nGenerated: 2026-05-30 08:51 UTC\n\n## Weekly Summary\n\nThis report...s share the same sector or factor risk.\n- Treat all outputs as research and decision support, not financial advice.\n'
2026-05-30T08:56:37.4127182Z 
2026-05-30T08:56:37.4127341Z tests/test_artifact_hygiene.py:83: AssertionError
2026-05-30T08:56:37.4128094Z =========================== short test summary info ============================
2026-05-30T08:56:37.4130174Z FAILED tests/test_artifact_hygiene.py::test_public_reports_are_synthetic_examples_only - AssertionError: assert 'Synthetic example: yes' in '# Institutional Trading Engine â WEEKLY REPORT\n\nGenerated: 2026-05-30 08:51 UTC\n\n## Weekly Summary\n\nThis report...s share the same sector or factor risk.\n- Treat all outputs as research and decision support, not financial advice.\n'
2026-05-30T08:56:37.4132119Z 1 failed, 1 passed in 0.05s
2026-05-30T08:56:37.4435901Z ##[error]Process completed with exit code 1.
2026-05-30T08:56:37.4563502Z Post job cleanup.
2026-05-30T08:56:37.5549510Z [command]/usr/bin/git version
2026-05-30T08:56:37.5587913Z git version 2.54.0
2026-05-30T08:56:37.5635041Z Temporarily overriding HOME='/home/runner/work/_temp/a5ab2b42-7e64-4b97-9b1e-61b0ca3b39e1' before making global git config changes
2026-05-30T08:56:37.5636496Z Adding repository directory to the temporary git global config as a safe directory
```

```text
2026-05-30T08:56:37.4123968Z     
2026-05-30T08:56:37.4124218Z >           assert "Synthetic example: yes" in content
2026-05-30T08:56:37.4125952Z E           AssertionError: assert 'Synthetic example: yes' in '# Institutional Trading Engine â WEEKLY REPORT\n\nGenerated: 2026-05-30 08:51 UTC\n\n## Weekly Summary\n\nThis report...s share the same sector or factor risk.\n- Treat all outputs as research and decision support, not financial advice.\n'
2026-05-30T08:56:37.4127182Z 
2026-05-30T08:56:37.4127341Z tests/test_artifact_hygiene.py:83: AssertionError
2026-05-30T08:56:37.4128094Z =========================== short test summary info ============================
2026-05-30T08:56:37.4130174Z FAILED tests/test_artifact_hygiene.py::test_public_reports_are_synthetic_examples_only - AssertionError: assert 'Synthetic example: yes' in '# Institutional Trading Engine â WEEKLY REPORT\n\nGenerated: 2026-05-30 08:51 UTC\n\n## Weekly Summary\n\nThis report...s share the same sector or factor risk.\n- Treat all outputs as research and decision support, not financial advice.\n'
2026-05-30T08:56:37.4132119Z 1 failed, 1 passed in 0.05s
2026-05-30T08:56:37.4435901Z ##[error]Process completed with exit code 1.
2026-05-30T08:56:37.4563502Z Post job cleanup.
2026-05-30T08:56:37.5549510Z [command]/usr/bin/git version
2026-05-30T08:56:37.5587913Z git version 2.54.0
2026-05-30T08:56:37.5635041Z Temporarily overriding HOME='/home/runner/work/_temp/a5ab2b42-7e64-4b97-9b1e-61b0ca3b39e1' before making global git config changes
2026-05-30T08:56:37.5636496Z Adding repository directory to the temporary git global config as a safe directory
2026-05-30T08:56:37.5642588Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-05-30T08:56:37.5680655Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
```

```text
2026-05-30T08:56:37.4125952Z E           AssertionError: assert 'Synthetic example: yes' in '# Institutional Trading Engine â WEEKLY REPORT\n\nGenerated: 2026-05-30 08:51 UTC\n\n## Weekly Summary\n\nThis report...s share the same sector or factor risk.\n- Treat all outputs as research and decision support, not financial advice.\n'
2026-05-30T08:56:37.4127182Z 
2026-05-30T08:56:37.4127341Z tests/test_artifact_hygiene.py:83: AssertionError
2026-05-30T08:56:37.4128094Z =========================== short test summary info ============================
2026-05-30T08:56:37.4130174Z FAILED tests/test_artifact_hygiene.py::test_public_reports_are_synthetic_examples_only - AssertionError: assert 'Synthetic example: yes' in '# Institutional Trading Engine â WEEKLY REPORT\n\nGenerated: 2026-05-30 08:51 UTC\n\n## Weekly Summary\n\nThis report...s share the same sector or factor risk.\n- Treat all outputs as research and decision support, not financial advice.\n'
2026-05-30T08:56:37.4132119Z 1 failed, 1 passed in 0.05s
2026-05-30T08:56:37.4435901Z ##[error]Process completed with exit code 1.
2026-05-30T08:56:37.4563502Z Post job cleanup.
2026-05-30T08:56:37.5549510Z [command]/usr/bin/git version
2026-05-30T08:56:37.5587913Z git version 2.54.0
2026-05-30T08:56:37.5635041Z Temporarily overriding HOME='/home/runner/work/_temp/a5ab2b42-7e64-4b97-9b1e-61b0ca3b39e1' before making global git config changes
2026-05-30T08:56:37.5636496Z Adding repository directory to the temporary git global config as a safe directory
2026-05-30T08:56:37.5642588Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-05-30T08:56:37.5680655Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-05-30T08:56:37.5715220Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-05-30T08:56:37.5945448Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
```

```text
2026-05-30T08:56:37.4127341Z tests/test_artifact_hygiene.py:83: AssertionError
2026-05-30T08:56:37.4128094Z =========================== short test summary info ============================
2026-05-30T08:56:37.4130174Z FAILED tests/test_artifact_hygiene.py::test_public_reports_are_synthetic_examples_only - AssertionError: assert 'Synthetic example: yes' in '# Institutional Trading Engine â WEEKLY REPORT\n\nGenerated: 2026-05-30 08:51 UTC\n\n## Weekly Summary\n\nThis report...s share the same sector or factor risk.\n- Treat all outputs as research and decision support, not financial advice.\n'
2026-05-30T08:56:37.4132119Z 1 failed, 1 passed in 0.05s
2026-05-30T08:56:37.4435901Z ##[error]Process completed with exit code 1.
2026-05-30T08:56:37.4563502Z Post job cleanup.
2026-05-30T08:56:37.5549510Z [command]/usr/bin/git version
2026-05-30T08:56:37.5587913Z git version 2.54.0
2026-05-30T08:56:37.5635041Z Temporarily overriding HOME='/home/runner/work/_temp/a5ab2b42-7e64-4b97-9b1e-61b0ca3b39e1' before making global git config changes
2026-05-30T08:56:37.5636496Z Adding repository directory to the temporary git global config as a safe directory
2026-05-30T08:56:37.5642588Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-05-30T08:56:37.5680655Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-05-30T08:56:37.5715220Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-05-30T08:56:37.5945448Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-05-30T08:56:37.5970946Z http.https://github.com/.extraheader
2026-05-30T08:56:37.5983555Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```
