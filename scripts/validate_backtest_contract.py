from __future__ import annotations

import json
import sys
from pathlib import Path

from src.backtesting.backtest_run_contract import (
    backtest_run_contract_from_dict,
    validate_backtest_run_contract,
    write_backtest_run_contract,
)


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: python scripts/validate_backtest_contract.py input.json output.json")
        return 2
    source = Path(sys.argv[1])
    target = Path(sys.argv[2])
    payload = json.loads(source.read_text(encoding="utf-8"))
    contract = validate_backtest_run_contract(backtest_run_contract_from_dict(payload))
    written = write_backtest_run_contract(contract.with_created_at(), target)
    print(json.dumps({"status": "PASS", "contract_id": written["contract_id"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
