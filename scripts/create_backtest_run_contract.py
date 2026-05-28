from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.backtesting.backtest_run_contract import (
    BacktestExecutionAssumptions,
    BacktestRunContract,
    BacktestUniverse,
    validate_backtest_run_contract,
    write_backtest_run_contract,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a deterministic BT1 backtest run contract")
    parser.add_argument("--strategy-id", required=True)
    parser.add_argument("--strategy-version", required=True)
    parser.add_argument("--universe-id", required=True)
    parser.add_argument("--symbols", required=True)
    parser.add_argument("--start-date", required=True)
    parser.add_argument("--end-date", required=True)
    parser.add_argument("--data-source", required=True)
    parser.add_argument("--data-source-version", required=True)
    parser.add_argument("--threshold-version", required=True)
    parser.add_argument("--setup-config-version", required=True)
    parser.add_argument("--slippage-model", required=True)
    parser.add_argument("--commission-model", required=True)
    parser.add_argument("--output-file", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    contract = BacktestRunContract(
        strategy_id=args.strategy_id,
        strategy_version=args.strategy_version,
        universe=BacktestUniverse(
            universe_id=args.universe_id,
            symbols=tuple(symbol.strip() for symbol in args.symbols.split(",") if symbol.strip()),
        ),
        start_date=args.start_date,
        end_date=args.end_date,
        data_source=args.data_source,
        data_source_version=args.data_source_version,
        threshold_version=args.threshold_version,
        setup_config_version=args.setup_config_version,
        execution_assumptions=BacktestExecutionAssumptions(
            slippage_model=args.slippage_model,
            commission_model=args.commission_model,
        ),
    )
    validated = validate_backtest_run_contract(contract)
    payload = write_backtest_run_contract(validated.with_created_at(), Path(args.output_file))
    print(json.dumps({"status": "PASS", "contract_id": payload["contract_id"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
