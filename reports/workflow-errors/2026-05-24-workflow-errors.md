# GitHub Actions Workflow Error Report

Generated: 2026-05-24 08:05 UTC
Repository: `yalcinkadir/institutional-trading-engine`
Filter since: 2026-05-23 08:05 UTC
Failed runs included: 3

## Polygon Edge Data Pipeline

- Run ID: `26347619213`
- Branch: `main`
- Commit: `172f9b6c2894`
- Title: Polygon Edge Data Pipeline
- Created: 2026-05-24T00:37:04Z
- Updated: 2026-05-24T01:45:10Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26347619213

### Failed job: Build Polygon All-Assets Runtime Dataset

- Job ID: `77560083038`
- Started: 2026-05-24T00:37:07Z
- Completed: 2026-05-24T01:45:09Z

#### Error context

```text
Could not fetch job logs: HTTPError: 404 Client Error: The specified blob does not exist. for url: https://productionresultssa14.blob.core.windows.net/actions-results/ccd7e7ba-a6a9-4022-830c-93941da7ee44/workflow-job-run-f0bd1920-17fc-5ca0-93d6-ba662886bdbf/logs/job/job-logs.txt?rsct=text%2Fplain&se=2026-05-24T08%3A15%3A16Z&sig=zCj5A8VDYPa3lGHVjBlcyXqmFs1dudBBekCwghpzGKI%3D&ske=2026-05-24T09%3A31%3A52Z&skoid=ca7593d4-ee42-46cd-af88-8b886a2f84eb&sks=b&skt=2026-05-24T05%3A31%3A52Z&sktid=398a6654-997b-47e9-b12b-9515b896b4de&skv=2025-11-05&sp=r&spr=https&sr=b&st=2026-05-24T08%3A05%3A11Z&sv=2025-11-05
```

## Polygon Edge Data Pipeline

- Run ID: `26347559897`
- Branch: `main`
- Commit: `b25abdc548e5`
- Title: Polygon Edge Data Pipeline
- Created: 2026-05-24T00:33:47Z
- Updated: 2026-05-24T00:34:11Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26347559897

### Failed job: Build Polygon All-Assets Runtime Dataset

- Job ID: `77559924902`
- Started: 2026-05-24T00:33:49Z
- Completed: 2026-05-24T00:34:11Z
- Failed steps: 7. Validate minimum universe coverage

#### Error context

```text
2026-05-24T00:34:06.9334405Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-05-24T00:34:06.9334775Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-05-24T00:34:06.9335162Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-05-24T00:34:06.9335472Z ##[endgroup]
2026-05-24T00:34:07.0554430Z Traceback (most recent call last):
2026-05-24T00:34:07.0561592Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/validate_universe_coverage.py", line 48, in <module>
2026-05-24T00:34:07.0562425Z     sys.exit(main())
2026-05-24T00:34:07.0562667Z              ^^^^^^
2026-05-24T00:34:07.0563335Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/validate_universe_coverage.py", line 37, in main
2026-05-24T00:34:07.0564306Z     universe = load_survivorship_universe(args.universe)
2026-05-24T00:34:07.0564656Z                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-05-24T00:34:07.0565426Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/data/survivorship_universe.py", line 395, in load_survivorship_universe
2026-05-24T00:34:07.0566191Z     return SurvivorshipUniverse(lifecycles)
2026-05-24T00:34:07.0566505Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-05-24T00:34:07.0567441Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/data/survivorship_universe.py", line 220, in __init__
2026-05-24T00:34:07.0568233Z     raise ValueError(f"duplicate ticker in universe: {symbol}")
```

```text
2026-05-24T00:34:07.0566505Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-05-24T00:34:07.0567441Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/src/data/survivorship_universe.py", line 220, in __init__
2026-05-24T00:34:07.0568233Z     raise ValueError(f"duplicate ticker in universe: {symbol}")
2026-05-24T00:34:07.0568632Z ValueError: duplicate ticker in universe: BCPC
2026-05-24T00:34:07.0657184Z ##[error]Process completed with exit code 1.
2026-05-24T00:34:07.0733417Z ##[group]Run actions/upload-artifact@v4
2026-05-24T00:34:07.0733709Z with:
2026-05-24T00:34:07.0733903Z   name: polygon-edge-runtime-dataset
2026-05-24T00:34:07.0734364Z   path: data/universe/survivorship_universe.csv
data/historical_bars/
reports/edge_evidence_data/

2026-05-24T00:34:07.0734824Z   if-no-files-found: warn
2026-05-24T00:34:07.0735039Z   compression-level: 6
2026-05-24T00:34:07.0735241Z   overwrite: false
2026-05-24T00:34:07.0735446Z   include-hidden-files: false
```

## Polygon Edge Data Pipeline

- Run ID: `26347510876`
- Branch: `main`
- Commit: `dcdad9ea8333`
- Title: Polygon Edge Data Pipeline
- Created: 2026-05-24T00:31:07Z
- Updated: 2026-05-24T00:31:30Z
- URL: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/26347510876

### Failed job: Build Polygon All-Assets Runtime Dataset

- Job ID: `77559792496`
- Started: 2026-05-24T00:31:09Z
- Completed: 2026-05-24T00:31:29Z
- Failed steps: 7. Validate minimum universe coverage

#### Error context

```text
2026-05-24T00:31:27.4235798Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-05-24T00:31:27.4236159Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.15/x64
2026-05-24T00:31:27.4236544Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.15/x64/lib
2026-05-24T00:31:27.4236839Z ##[endgroup]
2026-05-24T00:31:27.4539404Z Traceback (most recent call last):
2026-05-24T00:31:27.4546199Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/validate_universe_coverage.py", line 20, in <module>
2026-05-24T00:31:27.4547196Z     from src.data.survivorship_universe import load_survivorship_universe, validate_universe_coverage
2026-05-24T00:31:27.4547691Z ModuleNotFoundError: No module named 'src'
2026-05-24T00:31:27.4593036Z ##[error]Process completed with exit code 1.
2026-05-24T00:31:27.4673666Z ##[group]Run actions/upload-artifact@v4
2026-05-24T00:31:27.4673939Z with:
2026-05-24T00:31:27.4674134Z   name: polygon-edge-runtime-dataset
2026-05-24T00:31:27.4674586Z   path: data/universe/survivorship_universe.csv
data/historical_bars/
reports/edge_evidence_data/
```

```text
2026-05-24T00:31:27.4236839Z ##[endgroup]
2026-05-24T00:31:27.4539404Z Traceback (most recent call last):
2026-05-24T00:31:27.4546199Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/validate_universe_coverage.py", line 20, in <module>
2026-05-24T00:31:27.4547196Z     from src.data.survivorship_universe import load_survivorship_universe, validate_universe_coverage
2026-05-24T00:31:27.4547691Z ModuleNotFoundError: No module named 'src'
2026-05-24T00:31:27.4593036Z ##[error]Process completed with exit code 1.
2026-05-24T00:31:27.4673666Z ##[group]Run actions/upload-artifact@v4
2026-05-24T00:31:27.4673939Z with:
2026-05-24T00:31:27.4674134Z   name: polygon-edge-runtime-dataset
2026-05-24T00:31:27.4674586Z   path: data/universe/survivorship_universe.csv
data/historical_bars/
reports/edge_evidence_data/

2026-05-24T00:31:27.4675034Z   if-no-files-found: warn
2026-05-24T00:31:27.4675246Z   compression-level: 6
2026-05-24T00:31:27.4675454Z   overwrite: false
```

```text
2026-05-24T00:31:27.4539404Z Traceback (most recent call last):
2026-05-24T00:31:27.4546199Z   File "/home/runner/work/institutional-trading-engine/institutional-trading-engine/scripts/validate_universe_coverage.py", line 20, in <module>
2026-05-24T00:31:27.4547196Z     from src.data.survivorship_universe import load_survivorship_universe, validate_universe_coverage
2026-05-24T00:31:27.4547691Z ModuleNotFoundError: No module named 'src'
2026-05-24T00:31:27.4593036Z ##[error]Process completed with exit code 1.
2026-05-24T00:31:27.4673666Z ##[group]Run actions/upload-artifact@v4
2026-05-24T00:31:27.4673939Z with:
2026-05-24T00:31:27.4674134Z   name: polygon-edge-runtime-dataset
2026-05-24T00:31:27.4674586Z   path: data/universe/survivorship_universe.csv
data/historical_bars/
reports/edge_evidence_data/

2026-05-24T00:31:27.4675034Z   if-no-files-found: warn
2026-05-24T00:31:27.4675246Z   compression-level: 6
2026-05-24T00:31:27.4675454Z   overwrite: false
2026-05-24T00:31:27.4675658Z   include-hidden-files: false
```
