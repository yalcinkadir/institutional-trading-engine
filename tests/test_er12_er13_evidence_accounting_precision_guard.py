from __future__ import annotations

import json

from src.trading.risk_engine import calculate_position_risk
from src.validation.historical_edge_validation import (
    HistoricalEdgeValidationConfig,
    render_historical_edge_markdown,
    validate_historical_edge,
)


def test_er12_historical_edge_report_exposes_sharpe_caveats_in_json_and_markdown() -> None:
    report = validate_historical_edge(
        [{"result_r": 1.0}, {"result_r": -0.5}, {"result_r": 0.75}],
        config=HistoricalEdgeValidationConfig(
            min_total_trades=3,
            min_expectancy_r=0.0,
            min_profit_factor=1.0,
            max_drawdown_limit=1.0,
            min_sharpe_ratio=-10,
            min_deflated_sharpe_probability=0.0,
            bootstrap_iterations=100,
        ),
    )

    data = report.to_dict()
    markdown = render_historical_edge_markdown(report)

    assert data["metrics"]["sharpe_definition_version"] == "per-trade-sharpe-2026.05.29-v1"
    assert data["caveats"]["sharpe_std_method"] == "population_std"
    assert data["caveats"]["iid_assumption"] == "not_verified"
    assert data["caveats"]["small_sample_warning"] is True
    assert data["caveats"]["not_proof_of_edge"] is True
    assert "Sharpe caveats" in markdown
    assert "population standard deviation" in markdown
    assert "IID assumption is not verified" in markdown
    assert "not proof of live edge" in markdown


def test_er13_position_risk_uses_cent_stable_money_outputs() -> None:
    result = calculate_position_risk(
        account_size=10_000.10,
        risk_percent=1.25,
        entry_price=33.335,
        stop_price=31.115,
        buying_power=1_000.01,
        max_notional=999.99,
    )

    assert result["risk_amount"] == 125.00
    assert result["risk_per_share"] == 2.22
    assert result["notional_cap"] == 999.99
    assert result["shares"] == 29
    assert result["notional"] == 966.72
    json.dumps(result, allow_nan=False)


def test_er13_invalid_notional_caps_return_cent_stable_zeroes() -> None:
    result = calculate_position_risk(
        account_size=10_000.10,
        risk_percent=1.25,
        entry_price=33.335,
        stop_price=31.115,
        buying_power=0.0,
    )

    assert result == {
        "shares": 0,
        "risk_amount": 125.00,
        "risk_per_share": 2.22,
        "notional": 0.0,
        "notional_cap": 0.0,
    }
