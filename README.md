# Institutional Trading Engine

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![CI](https://img.shields.io/badge/CI-pytest-brightgreen.svg)
![Status](https://img.shields.io/badge/status-research--evidence--platform-orange.svg)

Institutional Trading Engine is a production-oriented market intelligence, screening, reporting, runtime orchestration, observability, historical validation and decision-support platform.

The system is designed for research and decision support. It does not place live trades.

## Current Validation Status

```text
P36-P47 validation roadmap: implemented
Phase A Evidence Hygiene A3-A10: implemented
Phase A CI stabilization: green
Full regression suite: green
Phase B1-B14 evidence pipeline: implemented, CI-green and workflow-green
Phase B15 observation cadence review: implemented and CI-green
Phase B1.1: active 3-6 month observation-only evidence collection
Phase C3/C4/C5/C6/C7: paper-only execution planning, reconciliation, drift, fill-quality and kill-switch governance infrastructure
Phase IP1: public/private edge boundary guardrail implemented
Phase IP2: public repository hygiene policy implemented
TG1: Telegram research-only report dispatcher implemented
BT1: deterministic backtest run contract implemented
Live trading authorization: not granted by code
Broker execution: paper-only infrastructure; live execution is not implemented
```

Code quality is not trading edge. The system is promising enough to test seriously, but real capital still requires forward evidence, drift detection, regime-change monitoring, position-level risk attribution and manual review.

## Public / Private Edge Boundary

The public repository is intended to expose the framework, validation discipline, paper-execution controls, auditability, tests and documentation. It is not intended to expose proprietary production edge configuration.

IP1 adds a conservative repository hygiene scanner:

```bash
python scripts/check_ip_boundary.py --root . --no-write
```

IP2 adds the operational public repository hygiene policy:

```bash
python scripts/validate_public_repo_policy.py --no-write
```

Policy files:

```text
.ip-boundary.yml
docs/operations/public_repo_hygiene_policy.md
```

Operational documentation:

```text
docs/operations/ip_boundary.md
docs/operations/public_repo_hygiene_policy.md
```

Public-safe content may include architecture, interfaces, demo defaults, synthetic examples, tests, documentation and paper-observation infrastructure. Private edge should stay outside the public repository, including real thresholds, real scoring weights, proprietary setup rankings, non-public entry/exit profiles and private evidence artifacts.

## Telegram Research-Only Reports

TG1 can dispatch Telegram reports in research-only mode. It blocks live-trading language, order-action phrases and private-edge terms before sending.

Dry-run mode:

```bash
python scripts/send_telegram_report.py \
  --report-file reports/daily_evidence/latest.md \
  --title "Daily Evidence" \
  --dry-run
```

Actual Telegram delivery requires explicit `--send` plus secrets in the environment:

```bash
TELEGRAM_BOT_TOKEN=...
TELEGRAM_CHAT_ID=...
python scripts/send_telegram_report.py \
  --report-file reports/daily_evidence/latest.md \
  --title "Daily Evidence" \
  --send
```

Every Telegram report must remain compatible with:

```text
Research / Paper Observation Only. No live trading authorization.
```

Operational documentation:

```text
docs/operations/telegram_report_dispatcher.md
```

## Backtesting Contracts

BT1 creates deterministic backtest run contracts before strategy scenario testing starts.

```bash
python scripts/create_backtest_run_contract.py --help
```

Each contract records strategy version, universe, date range, data-source version, config-version labels and execution assumptions. It emits a stable `contract_id` so later results can be traced back to the exact run assumptions.

Operational documentation:

```text
docs/operations/backtest_run_contract.md
```

BT1 does not add strategy edge. It only makes later backtests reproducible and auditable.

## Phase B Daily Evidence Pipeline

The Daily Evidence workflow now runs as an auditable evidence chain. It no longer builds green reports from placeholder component JSONs.

```text
Observation source selection
→ optional real paper observation source builder
→ optional Day-0 observation-only bootstrap
→ persisted daily observation feed
→ daily evidence input builder
→ daily evidence input validator
→ B1-B6 component report generation
→ daily evidence report generation
→ optional real paper observation cadence review
→ artifact upload
```

Manual bootstrap workflow path:

```text
Actions → Daily Evidence Report → Run workflow
bootstrap_observation_only_sources=true
use_real_paper_observation_source=false
```

Manual real paper observation workflow path:

```text
Actions → Daily Evidence Report → Run workflow
bootstrap_observation_only_sources=false
use_real_paper_observation_source=true
real_paper_observation_source_dir=reports/daily_paper_observation_raw
```

The bootstrap mode is only a Day-0 observation-only seed. Records are marked as `observation_only_bootstrap` and are not statistically meaningful 3-6 month forward evidence.

The real paper observation mode is still observation-only. It proves capture discipline and artifact completeness, not live trading readiness.

Operational documentation:

```text
docs/operations/generated_daily_evidence_components.md
docs/operations/daily_evidence_input_pipeline.md
docs/operations/daily_evidence_input_builder.md
docs/operations/daily_evidence_source_bootstrap.md
docs/operations/daily_paper_observation_source.md
docs/operations/daily_observation_cadence.md
docs/operations/vwap_twap_slicing.md
docs/operations/order_reconciliation.md
docs/operations/daily_execution_reconciliation.md
docs/operations/fill_quality_report.md
docs/operations/execution_kill_switch.md
docs/operations/ip_boundary.md
docs/operations/public_repo_hygiene_policy.md
docs/operations/telegram_report_dispatcher.md
docs/operations/backtest_run_contract.md
```

Core CLI commands:

```bash
python scripts/bootstrap_daily_evidence_sources.py \
  --output-dir reports/daily_observation_incoming \
  --report-dir reports/daily_evidence_source_bootstrap \
  --report-date 2026-05-26

python scripts/build_daily_paper_observation_sources.py \
  --source-dir reports/daily_paper_observation_raw \
  --output-dir reports/daily_observation_incoming \
  --report-dir reports/daily_paper_observation_source

python scripts/persist_daily_observation_sources.py \
  --incoming-dir reports/daily_observation_incoming \
  --feed-dir reports/daily_observation_feed \
  --report-dir reports/daily_observation_source_feed \
  --report-date 2026-05-26

python scripts/build_daily_evidence_inputs.py \
  --source-dir reports/daily_observation_feed \
  --output-dir reports/daily_evidence_inputs \
  --report-dir reports/daily_evidence_input_build

python scripts/validate_daily_evidence_inputs.py \
  --input-dir reports/daily_evidence_inputs \
  --output-dir reports/daily_evidence_input_validation

python scripts/generate_daily_evidence_components.py \
  --input-dir reports/daily_evidence_inputs \
  --output-dir reports/daily_evidence_components \
  --report-date 2026-05-26 \
  --observation-only

python scripts/run_daily_evidence_report.py \
  --input-dir reports/daily_evidence_components \
  --output-dir reports/daily_evidence \
  --report-date 2026-05-26 \
  --max-failed-components 3

python scripts/review_daily_observation_cadence.py \
  --report-date 2026-05-26 \
  --raw-source-dir reports/daily_paper_observation_raw \
  --artifact-root reports \
  --output-dir reports/daily_observation_cadence

python scripts/reconcile_daily_execution.py \
  --expected-file reports/daily_expected_execution/expected.json \
  --observed-file reports/daily_observed_execution/observed.json \
  --output-dir reports/daily_execution_reconciliation

python scripts/generate_fill_quality_report.py \
  --input-file reports/fill_quality_input/fills.json \
  --output-dir reports/fill_quality

python scripts/evaluate_execution_kill_switch.py \
  --input-file reports/execution_kill_switch_input/input.json \
  --output-dir reports/execution_kill_switch

python scripts/check_ip_boundary.py \
  --root . \
  --no-write

python scripts/validate_public_repo_policy.py \
  --no-write
```