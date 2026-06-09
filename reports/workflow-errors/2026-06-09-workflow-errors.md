# GitHub Actions Workflow Error Report

Generated: 2026-06-09 08:26 UTC
Repository: `yalcinkadir/institutional-trading-engine`
Filter since: 2026-06-08 08:26 UTC
Failed runs included: 6

## Report Quality Validation

- Run ID: `27192864263`
- Branch: `main`
- Commit: `f8edb553f237`
- Title: docs: add p161 dataflow contract to roadmap
- Created: 2026-06-09T08:10:39Z
- Updated: 2026-06-09T08:11:56Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27192864263

### Failed job: validate-reports (premarket)

- Job ID: `80277076962`
- Started: 2026-06-09T08:10:42Z
- Completed: 2026-06-09T08:11:55Z
- Failed steps: 6. Validate report quality

#### Error context

```text
2026-06-09T08:11:51.4997126Z - Report used fallback data; content is structurally valid but not analytically strong
2026-06-09T08:11:51.4997535Z 
2026-06-09T08:11:51.4997624Z Errors:
2026-06-09T08:11:51.4997851Z - Missing analytical term: Risk Tier
2026-06-09T08:11:51.5079234Z ##[error]Process completed with exit code 1.
2026-06-09T08:11:51.5159268Z ##[group]Run actions/upload-artifact@v4
2026-06-09T08:11:51.5159579Z with:
2026-06-09T08:11:51.5159821Z   name: validated-premarket-report
2026-06-09T08:11:51.5160148Z   path: reports/generated/premarket-report.md
2026-06-09T08:11:51.5160462Z   retention-days: 14
2026-06-09T08:11:51.5160722Z   if-no-files-found: warn
2026-06-09T08:11:51.5160989Z   compression-level: 6
2026-06-09T08:11:51.5161500Z   overwrite: false
2026-06-09T08:11:51.5161750Z   include-hidden-files: false
2026-06-09T08:11:51.5162010Z env:
2026-06-09T08:11:51.5162352Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (postmarket)

- Job ID: `80277077012`
- Started: 2026-06-09T08:10:42Z
- Completed: 2026-06-09T08:11:42Z
- Failed steps: 6. Validate report quality

#### Error context

```text
2026-06-09T08:11:39.7504206Z - Report used fallback data; content is structurally valid but not analytically strong
2026-06-09T08:11:39.7504588Z 
2026-06-09T08:11:39.7504669Z Errors:
2026-06-09T08:11:39.7504878Z - Missing analytical term: Risk Tier
2026-06-09T08:11:39.7574785Z ##[error]Process completed with exit code 1.
2026-06-09T08:11:39.7651698Z ##[group]Run actions/upload-artifact@v4
2026-06-09T08:11:39.7651993Z with:
2026-06-09T08:11:39.7652217Z   name: validated-postmarket-report
2026-06-09T08:11:39.7652531Z   path: reports/generated/postmarket-report.md
2026-06-09T08:11:39.7652830Z   retention-days: 14
2026-06-09T08:11:39.7653056Z   if-no-files-found: warn
2026-06-09T08:11:39.7653302Z   compression-level: 6
2026-06-09T08:11:39.7653528Z   overwrite: false
2026-06-09T08:11:39.7653750Z   include-hidden-files: false
2026-06-09T08:11:39.7653988Z env:
2026-06-09T08:11:39.7654299Z   POLYGON_API_KEY: ***
```

## Report Quality Validation

- Run ID: `27192274966`
- Branch: `main`
- Commit: `ff154a1d878a`
- Title: docs: reference p161 dataflow contract matrix
- Created: 2026-06-09T07:58:55Z
- Updated: 2026-06-09T07:59:59Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27192274966

### Failed job: validate-reports (postmarket)

- Job ID: `80275121020`
- Started: 2026-06-09T07:58:57Z
- Completed: 2026-06-09T07:59:54Z
- Failed steps: 6. Validate report quality

#### Error context

```text
2026-06-09T07:59:52.2162893Z - Report used fallback data; content is structurally valid but not analytically strong
2026-06-09T07:59:52.2163300Z 
2026-06-09T07:59:52.2163396Z Errors:
2026-06-09T07:59:52.2163618Z - Missing analytical term: Risk Tier
2026-06-09T07:59:52.2246378Z ##[error]Process completed with exit code 1.
2026-06-09T07:59:52.2328838Z ##[group]Run actions/upload-artifact@v4
2026-06-09T07:59:52.2329145Z with:
2026-06-09T07:59:52.2329381Z   name: validated-postmarket-report
2026-06-09T07:59:52.2329715Z   path: reports/generated/postmarket-report.md
2026-06-09T07:59:52.2330029Z   retention-days: 14
2026-06-09T07:59:52.2330271Z   if-no-files-found: warn
2026-06-09T07:59:52.2330524Z   compression-level: 6
2026-06-09T07:59:52.2330757Z   overwrite: false
2026-06-09T07:59:52.2331004Z   include-hidden-files: false
2026-06-09T07:59:52.2331250Z env:
2026-06-09T07:59:52.2331592Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (premarket)

- Job ID: `80275121028`
- Started: 2026-06-09T07:58:57Z
- Completed: 2026-06-09T07:59:58Z
- Failed steps: 6. Validate report quality

#### Error context

```text
2026-06-09T07:59:55.7509051Z - Report used fallback data; content is structurally valid but not analytically strong
2026-06-09T07:59:55.7509476Z 
2026-06-09T07:59:55.7509577Z Errors:
2026-06-09T07:59:55.7509810Z - Missing analytical term: Risk Tier
2026-06-09T07:59:55.7588294Z ##[error]Process completed with exit code 1.
2026-06-09T07:59:55.7672466Z ##[group]Run actions/upload-artifact@v4
2026-06-09T07:59:55.7672765Z with:
2026-06-09T07:59:55.7672995Z   name: validated-premarket-report
2026-06-09T07:59:55.7673306Z   path: reports/generated/premarket-report.md
2026-06-09T07:59:55.7673607Z   retention-days: 14
2026-06-09T07:59:55.7673841Z   if-no-files-found: warn
2026-06-09T07:59:55.7674091Z   compression-level: 6
2026-06-09T07:59:55.7674320Z   overwrite: false
2026-06-09T07:59:55.7674563Z   include-hidden-files: false
2026-06-09T07:59:55.7674808Z env:
2026-06-09T07:59:55.7675194Z   POLYGON_API_KEY: ***
```

## Report Quality Validation

- Run ID: `27191769439`
- Branch: `main`
- Commit: `7a9278b787c9`
- Title: test: enforce p161 dataflow contract semantics
- Created: 2026-06-09T07:48:21Z
- Updated: 2026-06-09T07:49:41Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27191769439

### Failed job: validate-reports (postmarket)

- Job ID: `80273505737`
- Started: 2026-06-09T07:48:39Z
- Completed: 2026-06-09T07:49:36Z
- Failed steps: 6. Validate report quality

#### Error context

```text
2026-06-09T07:49:34.6020144Z - Report used fallback data; content is structurally valid but not analytically strong
2026-06-09T07:49:34.6020540Z 
2026-06-09T07:49:34.6020627Z Errors:
2026-06-09T07:49:34.6020848Z - Missing analytical term: Risk Tier
2026-06-09T07:49:34.6093094Z ##[error]Process completed with exit code 1.
2026-06-09T07:49:34.6174296Z ##[group]Run actions/upload-artifact@v4
2026-06-09T07:49:34.6174600Z with:
2026-06-09T07:49:34.6174834Z   name: validated-postmarket-report
2026-06-09T07:49:34.6175147Z   path: reports/generated/postmarket-report.md
2026-06-09T07:49:34.6175455Z   retention-days: 14
2026-06-09T07:49:34.6175694Z   if-no-files-found: warn
2026-06-09T07:49:34.6175950Z   compression-level: 6
2026-06-09T07:49:34.6176183Z   overwrite: false
2026-06-09T07:49:34.6176429Z   include-hidden-files: false
2026-06-09T07:49:34.6176678Z env:
2026-06-09T07:49:34.6177054Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (premarket)

- Job ID: `80273505753`
- Started: 2026-06-09T07:48:39Z
- Completed: 2026-06-09T07:49:41Z
- Failed steps: 6. Validate report quality

#### Error context

```text
2026-06-09T07:49:37.9875150Z - Report used fallback data; content is structurally valid but not analytically strong
2026-06-09T07:49:37.9875561Z 
2026-06-09T07:49:37.9875644Z Errors:
2026-06-09T07:49:37.9875859Z - Missing analytical term: Risk Tier
2026-06-09T07:49:37.9959639Z ##[error]Process completed with exit code 1.
2026-06-09T07:49:38.0043313Z ##[group]Run actions/upload-artifact@v4
2026-06-09T07:49:38.0043622Z with:
2026-06-09T07:49:38.0043851Z   name: validated-premarket-report
2026-06-09T07:49:38.0044163Z   path: reports/generated/premarket-report.md
2026-06-09T07:49:38.0044470Z   retention-days: 14
2026-06-09T07:49:38.0044714Z   if-no-files-found: warn
2026-06-09T07:49:38.0044990Z   compression-level: 6
2026-06-09T07:49:38.0045220Z   overwrite: false
2026-06-09T07:49:38.0045450Z   include-hidden-files: false
2026-06-09T07:49:38.0045701Z env:
2026-06-09T07:49:38.0046066Z   POLYGON_API_KEY: ***
```

## Report Quality Validation

- Run ID: `27191735242`
- Branch: `main`
- Commit: `94cf0fcec1df`
- Title: docs: expand p161 dataflow contract matrix
- Created: 2026-06-09T07:47:38Z
- Updated: 2026-06-09T07:48:37Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27191735242

### Failed job: validate-reports (postmarket)

- Job ID: `80273355706`
- Started: 2026-06-09T07:47:41Z
- Completed: 2026-06-09T07:48:36Z
- Failed steps: 6. Validate report quality

#### Error context

```text
2026-06-09T07:48:34.5916641Z - Report used fallback data; content is structurally valid but not analytically strong
2026-06-09T07:48:34.5917039Z 
2026-06-09T07:48:34.5917121Z Errors:
2026-06-09T07:48:34.5917334Z - Missing analytical term: Risk Tier
2026-06-09T07:48:34.5990495Z ##[error]Process completed with exit code 1.
2026-06-09T07:48:34.6071146Z ##[group]Run actions/upload-artifact@v4
2026-06-09T07:48:34.6071444Z with:
2026-06-09T07:48:34.6071667Z   name: validated-postmarket-report
2026-06-09T07:48:34.6071974Z   path: reports/generated/postmarket-report.md
2026-06-09T07:48:34.6072280Z   retention-days: 14
2026-06-09T07:48:34.6072518Z   if-no-files-found: warn
2026-06-09T07:48:34.6072767Z   compression-level: 6
2026-06-09T07:48:34.6072995Z   overwrite: false
2026-06-09T07:48:34.6073230Z   include-hidden-files: false
2026-06-09T07:48:34.6073474Z env:
2026-06-09T07:48:34.6073828Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (premarket)

- Job ID: `80273355958`
- Started: 2026-06-09T07:47:40Z
- Completed: 2026-06-09T07:48:36Z
- Failed steps: 6. Validate report quality

#### Error context

```text
2026-06-09T07:48:34.5351592Z - Report used fallback data; content is structurally valid but not analytically strong
2026-06-09T07:48:34.5351982Z 
2026-06-09T07:48:34.5352068Z Errors:
2026-06-09T07:48:34.5352297Z - Missing analytical term: Risk Tier
2026-06-09T07:48:34.5424474Z ##[error]Process completed with exit code 1.
2026-06-09T07:48:34.5503819Z ##[group]Run actions/upload-artifact@v4
2026-06-09T07:48:34.5504355Z with:
2026-06-09T07:48:34.5504593Z   name: validated-premarket-report
2026-06-09T07:48:34.5504914Z   path: reports/generated/premarket-report.md
2026-06-09T07:48:34.5505225Z   retention-days: 14
2026-06-09T07:48:34.5505469Z   if-no-files-found: warn
2026-06-09T07:48:34.5505729Z   compression-level: 6
2026-06-09T07:48:34.5505967Z   overwrite: false
2026-06-09T07:48:34.5506211Z   include-hidden-files: false
2026-06-09T07:48:34.5506463Z env:
2026-06-09T07:48:34.5506804Z   POLYGON_API_KEY: ***
```

## Report Quality Validation

- Run ID: `27189838986`
- Branch: `main`
- Commit: `a640a04c4c31`
- Title: test: remove obsolete p160 hard-coded baseline expectation
- Created: 2026-06-09T07:07:13Z
- Updated: 2026-06-09T07:08:27Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27189838986

### Failed job: validate-reports (premarket)

- Job ID: `80267137819`
- Started: 2026-06-09T07:07:16Z
- Completed: 2026-06-09T07:08:26Z
- Failed steps: 6. Validate report quality

#### Error context

```text
2026-06-09T07:08:22.5695669Z - Report used fallback data; content is structurally valid but not analytically strong
2026-06-09T07:08:22.5695883Z 
2026-06-09T07:08:22.5695928Z Errors:
2026-06-09T07:08:22.5696050Z - Missing analytical term: Risk Tier
2026-06-09T07:08:22.5742465Z ##[error]Process completed with exit code 1.
2026-06-09T07:08:22.5792141Z ##[group]Run actions/upload-artifact@v4
2026-06-09T07:08:22.5792297Z with:
2026-06-09T07:08:22.5792424Z   name: validated-premarket-report
2026-06-09T07:08:22.5792594Z   path: reports/generated/premarket-report.md
2026-06-09T07:08:22.5792756Z   retention-days: 14
2026-06-09T07:08:22.5792880Z   if-no-files-found: warn
2026-06-09T07:08:22.5793012Z   compression-level: 6
2026-06-09T07:08:22.5793133Z   overwrite: false
2026-06-09T07:08:22.5793259Z   include-hidden-files: false
2026-06-09T07:08:22.5793390Z env:
2026-06-09T07:08:22.5793604Z   POLYGON_API_KEY: ***
```

### Failed job: validate-reports (postmarket)

- Job ID: `80267137821`
- Started: 2026-06-09T07:07:16Z
- Completed: 2026-06-09T07:08:15Z
- Failed steps: 6. Validate report quality

#### Error context

```text
2026-06-09T07:08:13.3773204Z - Report used fallback data; content is structurally valid but not analytically strong
2026-06-09T07:08:13.3773700Z 
2026-06-09T07:08:13.3773803Z Errors:
2026-06-09T07:08:13.3774083Z - Missing analytical term: Risk Tier
2026-06-09T07:08:13.3847700Z ##[error]Process completed with exit code 1.
2026-06-09T07:08:13.3929718Z ##[group]Run actions/upload-artifact@v4
2026-06-09T07:08:13.3930034Z with:
2026-06-09T07:08:13.3930267Z   name: validated-postmarket-report
2026-06-09T07:08:13.3930584Z   path: reports/generated/postmarket-report.md
2026-06-09T07:08:13.3930898Z   retention-days: 14
2026-06-09T07:08:13.3931133Z   if-no-files-found: warn
2026-06-09T07:08:13.3931384Z   compression-level: 6
2026-06-09T07:08:13.3931614Z   overwrite: false
2026-06-09T07:08:13.3931848Z   include-hidden-files: false
2026-06-09T07:08:13.3932085Z env:
2026-06-09T07:08:13.3932406Z   POLYGON_API_KEY: ***
```

## CI

- Run ID: `27189631836`
- Branch: `main`
- Commit: `15504f6315be`
- Title: CI
- Created: 2026-06-09T07:02:48Z
- Updated: 2026-06-09T07:04:07Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27189631836

### Failed job: Pytest

- Job ID: `80266489048`
- Started: 2026-06-09T07:02:56Z
- Completed: 2026-06-09T07:04:06Z
- Failed steps: 53. Full regression suite residual tests

#### Error context

```text
2026-06-09T07:04:01.8515888Z ........................................................................ [ 85%]
2026-06-09T07:04:01.9087692Z ........................................................................ [ 91%]
2026-06-09T07:04:02.1388724Z ........................................................................ [ 96%]
2026-06-09T07:04:02.2227581Z .............................................                            [100%]
2026-06-09T07:04:02.2228414Z =================================== FAILURES ===================================
2026-06-09T07:04:02.2229243Z ____________ test_p160_script_declares_expected_counts_and_baseline ____________
2026-06-09T07:04:02.2230173Z 
2026-06-09T07:04:02.2230575Z     def test_p160_script_declares_expected_counts_and_baseline() -> None:
2026-06-09T07:04:02.2231318Z         text = SCRIPT.read_text(encoding="utf-8")
2026-06-09T07:04:02.2231841Z     
2026-06-09T07:04:02.2232218Z         assert "EXPECTED_NEW_COUNT = 88" in text
2026-06-09T07:04:02.2232899Z >       assert "EXPECTED_RESULTING_UNCLASSIFIED_BASELINE = 196" in text
2026-06-09T07:04:02.2235503Z E       assert 'EXPECTED_RESULTING_UNCLASSIFIED_BASELINE = 196' in '#!/usr/bin/env python3\n"""One-shot script: classify pipeline-relevant modules for issue #160.\n\nRun once, then disc...fied legacy baseline set to {baseline}")\n    return 0\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
2026-06-09T07:04:02.2237465Z 
2026-06-09T07:04:02.2237884Z tests/test_p160_pipeline_classification_script.py:14: AssertionError
2026-06-09T07:04:02.2238694Z =========================== short test summary info ============================
```

```text
2026-06-09T07:04:02.2232218Z         assert "EXPECTED_NEW_COUNT = 88" in text
2026-06-09T07:04:02.2232899Z >       assert "EXPECTED_RESULTING_UNCLASSIFIED_BASELINE = 196" in text
2026-06-09T07:04:02.2235503Z E       assert 'EXPECTED_RESULTING_UNCLASSIFIED_BASELINE = 196' in '#!/usr/bin/env python3\n"""One-shot script: classify pipeline-relevant modules for issue #160.\n\nRun once, then disc...fied legacy baseline set to {baseline}")\n    return 0\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
2026-06-09T07:04:02.2237465Z 
2026-06-09T07:04:02.2237884Z tests/test_p160_pipeline_classification_script.py:14: AssertionError
2026-06-09T07:04:02.2238694Z =========================== short test summary info ============================
2026-06-09T07:04:02.2241743Z FAILED tests/test_p160_pipeline_classification_script.py::test_p160_script_declares_expected_counts_and_baseline - assert 'EXPECTED_RESULTING_UNCLASSIFIED_BASELINE = 196' in '#!/usr/bin/env python3\n"""One-shot script: classify pipeline-relevant modules for issue #160.\n\nRun once, then disc...fied legacy baseline set to {baseline}")\n    return 0\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
2026-06-09T07:04:02.2244514Z 1 failed, 1339 passed, 1 skipped in 21.80s
2026-06-09T07:04:02.5558470Z ##[error]Process completed with exit code 1.
2026-06-09T07:04:02.5632209Z ##[group]Run actions/upload-artifact@v4
2026-06-09T07:04:02.5632515Z with:
2026-06-09T07:04:02.5632725Z   name: p109-residual-pytest-evidence
2026-06-09T07:04:02.5633037Z   path: artifacts/evidence/p109-residual-pytest/
2026-06-09T07:04:02.5633340Z   if-no-files-found: warn
2026-06-09T07:04:02.5633571Z   compression-level: 6
2026-06-09T07:04:02.5633785Z   overwrite: false
```

```text
2026-06-09T07:04:02.2235503Z E       assert 'EXPECTED_RESULTING_UNCLASSIFIED_BASELINE = 196' in '#!/usr/bin/env python3\n"""One-shot script: classify pipeline-relevant modules for issue #160.\n\nRun once, then disc...fied legacy baseline set to {baseline}")\n    return 0\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
2026-06-09T07:04:02.2237465Z 
2026-06-09T07:04:02.2237884Z tests/test_p160_pipeline_classification_script.py:14: AssertionError
2026-06-09T07:04:02.2238694Z =========================== short test summary info ============================
2026-06-09T07:04:02.2241743Z FAILED tests/test_p160_pipeline_classification_script.py::test_p160_script_declares_expected_counts_and_baseline - assert 'EXPECTED_RESULTING_UNCLASSIFIED_BASELINE = 196' in '#!/usr/bin/env python3\n"""One-shot script: classify pipeline-relevant modules for issue #160.\n\nRun once, then disc...fied legacy baseline set to {baseline}")\n    return 0\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
2026-06-09T07:04:02.2244514Z 1 failed, 1339 passed, 1 skipped in 21.80s
2026-06-09T07:04:02.5558470Z ##[error]Process completed with exit code 1.
2026-06-09T07:04:02.5632209Z ##[group]Run actions/upload-artifact@v4
2026-06-09T07:04:02.5632515Z with:
2026-06-09T07:04:02.5632725Z   name: p109-residual-pytest-evidence
2026-06-09T07:04:02.5633037Z   path: artifacts/evidence/p109-residual-pytest/
2026-06-09T07:04:02.5633340Z   if-no-files-found: warn
2026-06-09T07:04:02.5633571Z   compression-level: 6
2026-06-09T07:04:02.5633785Z   overwrite: false
2026-06-09T07:04:02.5634026Z   include-hidden-files: false
2026-06-09T07:04:02.5634259Z env:
```

```text
2026-06-09T07:04:02.2237884Z tests/test_p160_pipeline_classification_script.py:14: AssertionError
2026-06-09T07:04:02.2238694Z =========================== short test summary info ============================
2026-06-09T07:04:02.2241743Z FAILED tests/test_p160_pipeline_classification_script.py::test_p160_script_declares_expected_counts_and_baseline - assert 'EXPECTED_RESULTING_UNCLASSIFIED_BASELINE = 196' in '#!/usr/bin/env python3\n"""One-shot script: classify pipeline-relevant modules for issue #160.\n\nRun once, then disc...fied legacy baseline set to {baseline}")\n    return 0\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
2026-06-09T07:04:02.2244514Z 1 failed, 1339 passed, 1 skipped in 21.80s
2026-06-09T07:04:02.5558470Z ##[error]Process completed with exit code 1.
2026-06-09T07:04:02.5632209Z ##[group]Run actions/upload-artifact@v4
2026-06-09T07:04:02.5632515Z with:
2026-06-09T07:04:02.5632725Z   name: p109-residual-pytest-evidence
2026-06-09T07:04:02.5633037Z   path: artifacts/evidence/p109-residual-pytest/
2026-06-09T07:04:02.5633340Z   if-no-files-found: warn
2026-06-09T07:04:02.5633571Z   compression-level: 6
2026-06-09T07:04:02.5633785Z   overwrite: false
2026-06-09T07:04:02.5634026Z   include-hidden-files: false
2026-06-09T07:04:02.5634259Z env:
2026-06-09T07:04:02.5634502Z   pythonLocation: /opt/hostedtoolcache/Python/3.11.15/x64
2026-06-09T07:04:02.5635238Z   PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib/pkgconfig
```
