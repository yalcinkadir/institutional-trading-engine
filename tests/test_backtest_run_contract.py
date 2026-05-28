import json

import pytest

from src.backtesting.backtest_run_contract import (
    BacktestContractError,
    BacktestExecutionAssumptions,
    BacktestRunContract,
    BacktestUniverse,
    load_backtest_run_contract,
    validate_backtest_run_contract,
    write_backtest_run_contract,
)


def _contract() -> BacktestRunContract:
    return BacktestRunContract(
        strategy_id="demo_momentum",
        strategy_version="v1",
        universe=BacktestUniverse(universe_id="demo_universe", symbols=("msft", "AAPL", "AAPL")),
        start_date="2023-01-01",
        end_date="2023-12-31",
        data_source="polygon_demo",
        data_source_version="v2026_05",
        threshold_version="demo_thresholds_v1",
        setup_config_version="demo_setup_v1",
        execution_assumptions=BacktestExecutionAssumptions(
            slippage_model="demo_bps_5",
            commission_model="zero_commission_demo",
        ),
        metadata={"b": 2, "a": 1},
    )


def test_contract_id_is_stable_after_normalization() -> None:
    first = validate_backtest_run_contract(_contract())
    second = validate_backtest_run_contract(_contract())

    assert first.contract_id() == second.contract_id()
    assert first.universe.symbols == ("AAPL", "MSFT")


def test_created_at_does_not_change_contract_id() -> None:
    contract = validate_backtest_run_contract(_contract())

    assert contract.contract_id() == contract.with_created_at().contract_id()


def test_rejects_invalid_date_window() -> None:
    contract = _contract()
    invalid = BacktestRunContract(
        **{**contract.__dict__, "start_date": "2024-01-01", "end_date": "2023-01-01"}
    )

    with pytest.raises(BacktestContractError):
        validate_backtest_run_contract(invalid)


def test_rejects_empty_universe() -> None:
    contract = _contract()
    invalid = BacktestRunContract(**{**contract.__dict__, "universe": BacktestUniverse("empty", ())})

    with pytest.raises(BacktestContractError):
        validate_backtest_run_contract(invalid)


def test_write_and_load_contract_round_trip(tmp_path) -> None:
    path = tmp_path / "contract.json"
    payload = write_backtest_run_contract(_contract().with_created_at(), path)

    loaded = load_backtest_run_contract(path)
    reloaded_payload = json.loads(path.read_text(encoding="utf-8"))

    assert payload["contract_id"] == loaded.contract_id()
    assert reloaded_payload["schema_version"] == "bt1.backtest_run_contract.v1"
    assert reloaded_payload["contract_id"] == payload["contract_id"]
