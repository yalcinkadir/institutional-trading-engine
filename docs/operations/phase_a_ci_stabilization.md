# Phase A CI Stabilization Plan

Phase A is not complete until the new tests are part of CI and the full regression suite is green.

## Required Phase A test set

```bash
pytest tests/test_decision_engine.py -q
pytest tests/test_out_of_sample_lockbox.py -q
pytest tests/test_slippage_model.py -q
pytest tests/test_execution_realism.py -q
pytest tests/test_statistical_robustness.py -q
pytest tests/test_historical_edge_validation.py -q
pytest tests/test_polygon_structured_logging.py -q
pytest tests/test_polygon_data_pipeline.py -q
pytest tests/test_polygon_cache.py -q
```

## Full regression

```bash
pytest -q
```

## CI gate before Phase B

Phase B must not start until:

1. all Phase A tests are included in GitHub Actions
2. the CI workflow has been executed
3. failed tests are fixed
4. `pytest -q` is green
5. README, CHANGELOG, SETUP_NOTES and ROADMAP are current

## Failure handling

If a Phase A test fails:

1. stop feature development
2. identify the failing module
3. fix the implementation or the test expectation
4. rerun the targeted test
5. rerun full regression

## Operational rule

No live capital. No broker execution. No Phase B evidence collection until the stabilization pass is green.
