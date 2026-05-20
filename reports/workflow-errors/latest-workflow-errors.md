# GitHub Actions Workflow Error Report

Generated: 2026-05-20 20:52 UTC
Repository: `yalcinkadir/institutional-trading-engine`
Failed runs included: 9

## .github/workflows/entry-exit-watcher.yml

- Run ID: `26189143246`
- Branch: `main`
- Commit: `85bc5d865486`
- Title: Initialize workflow error reports directory
- Created: 2026-05-20T20:49:35Z
- Updated: 2026-05-20T20:49:35Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26189143246

- No failed jobs returned by API, although run concluded as failure.

## .github/workflows/entry-exit-watcher.yml

- Run ID: `26189058499`
- Branch: `main`
- Commit: `c91b6a909ac1`
- Title: Commit generated workflow error reports reliably
- Created: 2026-05-20T20:47:54Z
- Updated: 2026-05-20T20:47:54Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26189058499

- No failed jobs returned by API, although run concluded as failure.

## .github/workflows/entry-exit-watcher.yml

- Run ID: `26188808905`
- Branch: `main`
- Commit: `16426c335a63`
- Title: Fix workflow error report commit rebase handling
- Created: 2026-05-20T20:42:58Z
- Updated: 2026-05-20T20:42:58Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26188808905

- No failed jobs returned by API, although run concluded as failure.

## Workflow Error Report

- Run ID: `26188749416`
- Branch: `main`
- Commit: `996a346322e4`
- Title: Workflow Error Report
- Created: 2026-05-20T20:41:47Z
- Updated: 2026-05-20T20:42:05Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26188749416

### Failed job: Generate workflow error report

- Job ID: `77051237897`
- Started: 2026-05-20T20:41:51Z
- Completed: 2026-05-20T20:42:04Z
- Failed steps: 6. Commit workflow error report

#### Error context

```text
2026-05-20T20:42:01.5144341Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-05-20T20:42:01.5144656Z ##[endgroup]
2026-05-20T20:42:01.5369459Z error: cannot pull with rebase: Your index contains uncommitted changes.
2026-05-20T20:42:01.5370174Z error: Please commit or stash them.
2026-05-20T20:42:01.5385149Z ##[error]Process completed with exit code 128.
2026-05-20T20:42:01.5503462Z Post job cleanup.
2026-05-20T20:42:01.6501164Z [command]/usr/bin/git version
2026-05-20T20:42:01.6537987Z git version 2.54.0
2026-05-20T20:42:01.6584261Z Temporarily overriding HOME='/home/runner/work/_temp/cc0b4d02-ae92-477a-8a6f-9158d3b156ee' before making global git config changes
2026-05-20T20:42:01.6586038Z Adding repository directory to the temporary git global config as a safe directory
2026-05-20T20:42:01.6598257Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-05-20T20:42:01.6632505Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-05-20T20:42:01.6665866Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-05-20T20:42:01.6890940Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-05-20T20:42:01.6915447Z http.https://github.com/.extraheader
2026-05-20T20:42:01.6928653Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

## .github/workflows/entry-exit-watcher.yml

- Run ID: `26188609435`
- Branch: `main`
- Commit: `8c1ca422e266`
- Title: Align macro risk-on threshold with scoring model
- Created: 2026-05-20T20:39:06Z
- Updated: 2026-05-20T20:39:06Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26188609435

- No failed jobs returned by API, although run concluded as failure.

## Report Quality Validation

- Run ID: `26188522826`
- Branch: `main`
- Commit: `996a346322e4`
- Title: Raise alpha weight for high conviction fusion confidence
- Created: 2026-05-20T20:37:22Z
- Updated: 2026-05-20T20:41:30Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26188522826

### Failed job: validate-reports (premarket)

- Job ID: `77050450268`
- Started: 2026-05-20T20:37:24Z
- Completed: 2026-05-20T20:41:29Z
- Failed steps: 6. Validate report quality

#### Error context

```text
2026-05-20T20:41:26.9822907Z - Report used fallback data; content is structurally valid but not analytically strong
2026-05-20T20:41:26.9823281Z 
2026-05-20T20:41:26.9823354Z Errors:
2026-05-20T20:41:26.9823534Z - Missing analytical term: SPY
2026-05-20T20:41:26.9893615Z ##[error]Process completed with exit code 1.
2026-05-20T20:41:27.0003621Z Post job cleanup.
2026-05-20T20:41:27.0994336Z [command]/usr/bin/git version
2026-05-20T20:41:27.1031228Z git version 2.54.0
2026-05-20T20:41:27.1072831Z Temporarily overriding HOME='/home/runner/work/_temp/78b53e4f-4128-4be2-a5e3-a82c13b0811e' before making global git config changes
2026-05-20T20:41:27.1074050Z Adding repository directory to the temporary git global config as a safe directory
2026-05-20T20:41:27.1087019Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/institutional-trading-engine/institutional-trading-engine
2026-05-20T20:41:27.1123309Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-05-20T20:41:27.1157329Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-05-20T20:41:27.1408767Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-05-20T20:41:27.1433886Z http.https://github.com/.extraheader
2026-05-20T20:41:27.1447181Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
```

## .github/workflows/entry-exit-watcher.yml

- Run ID: `26188522147`
- Branch: `main`
- Commit: `996a346322e4`
- Title: Raise alpha weight for high conviction fusion confidence
- Created: 2026-05-20T20:37:21Z
- Updated: 2026-05-20T20:37:21Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26188522147

- No failed jobs returned by API, although run concluded as failure.

## Decision Engine Tests

- Run ID: `26188512563`
- Branch: `main`
- Commit: `8c1ca422e266`
- Title: Align macro risk-on threshold with scoring model
- Created: 2026-05-20T20:37:09Z
- Updated: 2026-05-20T20:39:38Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26188512563

### Failed job: tests

- Job ID: `77050756283`
- Started: 2026-05-20T20:39:11Z
- Completed: 2026-05-20T20:39:37Z
- Failed steps: 5. Run pytest

#### Error context

```text
2026-05-20T20:39:32.1964380Z ........................................................................ [ 53%]
2026-05-20T20:39:34.2809345Z .........s.............................................................. [ 71%]
2026-05-20T20:39:34.3336461Z ........................................................................ [ 88%]
2026-05-20T20:39:34.6135545Z .............................................                            [100%]
2026-05-20T20:39:34.6136509Z =================================== FAILURES ===================================
2026-05-20T20:39:34.6137084Z ______________________ test_multi_factor_high_conviction _______________________
2026-05-20T20:39:34.6137422Z 
2026-05-20T20:39:34.6137543Z     def test_multi_factor_high_conviction():
2026-05-20T20:39:34.6137870Z         engine = MultiFactorFusionEngine()
2026-05-20T20:39:34.6138158Z     
2026-05-20T20:39:34.6138349Z         result = engine.evaluate(
2026-05-20T20:39:34.6138618Z             FusionInputs(
2026-05-20T20:39:34.6138860Z                 regime_score=90,
2026-05-20T20:39:34.6139114Z                 tail_risk_score=15,
2026-05-20T20:39:34.6139387Z                 liquidity_score=85,
2026-05-20T20:39:34.6139658Z                 feature_alpha_score=88,
```

```text
2026-05-20T20:39:34.6140702Z         )
2026-05-20T20:39:34.6140882Z     
2026-05-20T20:39:34.6141124Z         assert result.classification == "high_conviction"
2026-05-20T20:39:34.6141484Z >       assert result.confidence >= 75
2026-05-20T20:39:34.6141784Z E       AssertionError: assert 73.15 >= 75
2026-05-20T20:39:34.6142553Z E        +  where 73.15 = FusionDecision(fusion_score=73.15, confidence=73.15, classification='high_conviction', reasoning='strong multi-factor alignment').confidence
2026-05-20T20:39:34.6143511Z 
2026-05-20T20:39:34.6143658Z tests/test_multi_factor_fusion.py:22: AssertionError
2026-05-20T20:39:34.6144055Z =============================== warnings summary ===============================
2026-05-20T20:39:34.6144576Z tests/test_jwt_auth.py::test_create_and_validate_token
2026-05-20T20:39:34.6145017Z tests/test_security_layer.py::test_metrics_accepts_admin_token
2026-05-20T20:39:34.6145486Z tests/test_security_layer.py::test_viewer_cannot_access_metrics
2026-05-20T20:39:34.6147039Z   /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/jwt/api_jwt.py:147: InsecureKeyLengthWarning: The HMAC key is 18 bytes long, which is below the minimum recommended length of 32 bytes for SHA256. See RFC 7518 Section 3.2.
2026-05-20T20:39:34.6148239Z     return self._jws.encode(
2026-05-20T20:39:34.6148411Z 
2026-05-20T20:39:34.6148572Z tests/test_jwt_auth.py::test_create_and_validate_token
```

```text
2026-05-20T20:39:34.6141484Z >       assert result.confidence >= 75
2026-05-20T20:39:34.6141784Z E       AssertionError: assert 73.15 >= 75
2026-05-20T20:39:34.6142553Z E        +  where 73.15 = FusionDecision(fusion_score=73.15, confidence=73.15, classification='high_conviction', reasoning='strong multi-factor alignment').confidence
2026-05-20T20:39:34.6143511Z 
2026-05-20T20:39:34.6143658Z tests/test_multi_factor_fusion.py:22: AssertionError
2026-05-20T20:39:34.6144055Z =============================== warnings summary ===============================
2026-05-20T20:39:34.6144576Z tests/test_jwt_auth.py::test_create_and_validate_token
2026-05-20T20:39:34.6145017Z tests/test_security_layer.py::test_metrics_accepts_admin_token
2026-05-20T20:39:34.6145486Z tests/test_security_layer.py::test_viewer_cannot_access_metrics
2026-05-20T20:39:34.6147039Z   /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/jwt/api_jwt.py:147: InsecureKeyLengthWarning: The HMAC key is 18 bytes long, which is below the minimum recommended length of 32 bytes for SHA256. See RFC 7518 Section 3.2.
2026-05-20T20:39:34.6148239Z     return self._jws.encode(
2026-05-20T20:39:34.6148411Z 
2026-05-20T20:39:34.6148572Z tests/test_jwt_auth.py::test_create_and_validate_token
2026-05-20T20:39:34.6149009Z tests/test_security_layer.py::test_metrics_accepts_admin_token
2026-05-20T20:39:34.6149437Z tests/test_security_layer.py::test_viewer_cannot_access_metrics
2026-05-20T20:39:34.6150398Z   /opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/site-packages/jwt/api_jwt.py:365: InsecureKeyLengthWarning: The HMAC key is 18 bytes long, which is below the minimum recommended length of 32 bytes for SHA256. See RFC 7518 Section 3.2.
```

```text
2026-05-20T20:39:34.6151426Z     decoded = self.decode_complete(
2026-05-20T20:39:34.6151597Z 
2026-05-20T20:39:34.6151795Z -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2026-05-20T20:39:34.6152234Z =========================== short test summary info ============================
2026-05-20T20:39:34.6152768Z FAILED tests/test_multi_factor_fusion.py::test_multi_factor_high_conviction - AssertionError: assert 73.15 >= 75
2026-05-20T20:39:34.6153770Z  +  where 73.15 = FusionDecision(fusion_score=73.15, confidence=73.15, classification='high_conviction', reasoning='strong multi-factor alignment').confidence
2026-05-20T20:39:34.6154411Z 1 failed, 403 passed, 1 skipped, 6 warnings in 6.17s
2026-05-20T20:39:34.8513306Z ##[error]Process completed with exit code 1.
2026-05-20T20:39:34.8525803Z ##[debug]Finishing: Run pytest
2026-05-20T20:39:34.8545949Z ##[debug]Evaluating condition for step: 'Post Setup Python'
2026-05-20T20:39:34.8547944Z ##[debug]Evaluating: success()
2026-05-20T20:39:34.8548315Z ##[debug]Evaluating success:
2026-05-20T20:39:34.8548725Z ##[debug]=> false
2026-05-20T20:39:34.8549072Z ##[debug]Result: false
2026-05-20T20:39:34.8555949Z ##[debug]Evaluating condition for step: 'Post Checkout repository'
2026-05-20T20:39:34.8558675Z ##[debug]Evaluating: always()
```

```text
2026-05-20T20:39:34.6152234Z =========================== short test summary info ============================
2026-05-20T20:39:34.6152768Z FAILED tests/test_multi_factor_fusion.py::test_multi_factor_high_conviction - AssertionError: assert 73.15 >= 75
2026-05-20T20:39:34.6153770Z  +  where 73.15 = FusionDecision(fusion_score=73.15, confidence=73.15, classification='high_conviction', reasoning='strong multi-factor alignment').confidence
2026-05-20T20:39:34.6154411Z 1 failed, 403 passed, 1 skipped, 6 warnings in 6.17s
2026-05-20T20:39:34.8513306Z ##[error]Process completed with exit code 1.
2026-05-20T20:39:34.8525803Z ##[debug]Finishing: Run pytest
2026-05-20T20:39:34.8545949Z ##[debug]Evaluating condition for step: 'Post Setup Python'
2026-05-20T20:39:34.8547944Z ##[debug]Evaluating: success()
2026-05-20T20:39:34.8548315Z ##[debug]Evaluating success:
2026-05-20T20:39:34.8548725Z ##[debug]=> false
2026-05-20T20:39:34.8549072Z ##[debug]Result: false
2026-05-20T20:39:34.8555949Z ##[debug]Evaluating condition for step: 'Post Checkout repository'
2026-05-20T20:39:34.8558675Z ##[debug]Evaluating: always()
2026-05-20T20:39:34.8559012Z ##[debug]Evaluating always:
2026-05-20T20:39:34.8559766Z ##[debug]=> true
2026-05-20T20:39:34.8560092Z ##[debug]Result: true
```

## .github/workflows/entry-exit-watcher.yml

- Run ID: `26188510892`
- Branch: `main`
- Commit: `8c1ca422e266`
- Title: Align macro risk-on threshold with scoring model
- Created: 2026-05-20T20:37:07Z
- Updated: 2026-05-20T20:37:07Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26188510892

- No failed jobs returned by API, although run concluded as failure.
