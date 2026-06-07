# P125 Dataflow Integrity & Schema Validation Gate

P125 defines explicit data contracts between core runtime and evidence stages.

The goal is to prevent incomplete structures from silently moving from one module to the next.

## Covered contract stages

- Signal output contract
- Decision report contract
- Paper Observation artifact contract
- Historical backtest evidence contract

## Signal contract

Required fields:

- signal_id
- symbol
- action
- setup_type
- decision
- market_regime
- generated_at
- data_status
- source
- source_timestamp
- fallback_level

For BUY_WATCH signals, these fields are also required:

- entry_trigger
- stop_loss
- target_1

## Decision report contract

Required fields:

- market_state
- summary
- run_health
- scanner_data_quality
- signal_generation_status
- decisions

## Paper Observation contract

Required fields:

- timestamp_utc
- ready_for_review
- universe
- signal_ids
- decision_status
- data_quality_status
- provenance
- gates

The gates list must include:

- paper_observation_health

## Backtest evidence contract

Required fields:

- run_id
- data_source
- symbol_universe
- date_range
- strategy_version
- input_pack_gate_status
- input_completeness_status
- run_health_status
- input_plan_count
- accepted_plan_count
- rejected_plan_count
- metrics
- results

## Failure behavior

Missing or empty required fields raise a ContractViolation.

This prevents:

- empty dictionaries being treated as valid input
- None values for required decision fields
- BUY_WATCH signals without executable levels
- Paper Observation artifacts without health gates
- backtest evidence without run-health status

## Targeted test

```bash
pytest tests/test_p125_dataflow_contracts.py -q
```

## Safety boundary

P125 adds schema and contract validation only. It does not loosen trading thresholds, change signal generation logic or authorize live trading.
