# BT2 Strategy Test Matrix

BT2 adds a deterministic Strategy Test Matrix for public-safe strategy coverage validation.

## Purpose

The matrix answers one institutional question:

```text
Do we have explicit, testable coverage for each strategy sleeve across regimes, setup families, validation stages and data modes?
```

BT2 is not a signal generator. It does not prove edge, authorize live trading or define production thresholds.

## Public-safe boundary

The public matrix may include:

- demo strategy identifiers
- synthetic cases
- paper-observation case labels
- regime labels
- setup-family labels
- validation-stage labels
- expected governance gates
- documentation and tests

The public matrix must not include:

- proprietary thresholds
- production scoring weights
- private setup rankings
- private entry/exit profiles
- real ranked opportunities
- real-money trade instructions
- broker execution authorization

## Core dimensions

Each case contains:

| Field | Meaning |
|---|---|
| `case_id` | Deterministic matrix case identifier |
| `strategy_id` | Public-safe strategy identifier |
| `sleeve` | Strategy sleeve / portfolio bucket |
| `regime` | Regime bucket, for example `risk_on`, `neutral`, `risk_off` |
| `setup_family` | Setup family, for example `breakout`, `pullback`, `mean_reversion_demo` |
| `asset_class` | Public-safe asset-class label |
| `data_mode` | `synthetic` or `paper_observation` |
| `validation_stage` | `backtest`, `paper_observation` or `execution_quality` |
| `expected_gate` | Governance output expected for this case |
| `risk_state` | Must remain paper/research oriented in the public repo |
| `evidence_source` | Synthetic or paper-observation source label |
| `tags` | Must include `demo` and `public_safe` by default |

## Gates

BT2 validates:

- required fields are complete
- each strategy has enough cases
- required regime coverage exists
- required setup-family coverage exists
- required validation-stage coverage exists
- required data-mode coverage exists
- public cases are demo/public-safe by default
- live-trading authorization terms are blocked
- private-edge terms are blocked
- research-only footer is present

## Demo matrix

The demo file lives at:

```text
data/demo_strategy_test_matrix.json
```

It is intentionally synthetic/demo-only.

## CLI

Generate the built-in demo report:

```bash
python scripts/generate_strategy_test_matrix.py --demo
```

Generate from the demo JSON file:

```bash
python scripts/generate_strategy_test_matrix.py \
  --input-json data/demo_strategy_test_matrix.json \
  --output-json reports/strategy_test_matrix/strategy_test_matrix.json \
  --output-md reports/strategy_test_matrix/strategy_test_matrix.md
```

## Tests

```bash
pytest tests/test_strategy_test_matrix.py -q
```

CI includes BT2 as a dedicated test step before the full regression suite.

## Output

BT2 writes:

```text
reports/strategy_test_matrix/strategy_test_matrix.json
reports/strategy_test_matrix/strategy_test_matrix.md
```

Generated reports must include:

```text
Research / Paper Observation Only. No live trading authorization.
```

## Non-goals

BT2 does not:

- produce trading signals
- optimize strategy parameters
- place orders
- connect to broker execution
- approve live trading
- expose private edge
- replace forward paper observation

## Current status

BT2 model, demo matrix, CLI, documentation, tests and CI step are implemented on the `bt2-strategy-test-matrix` branch.
