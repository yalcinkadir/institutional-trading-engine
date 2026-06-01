from __future__ import annotations

from src.trading.risk_engine import calculate_position_risk


def test_position_risk_without_notional_cap_preserves_risk_based_sizing() -> None:
    result = calculate_position_risk(
        account_size=10_000,
        risk_percent=1,
        entry_price=100,
        stop_price=95,
    )

    assert result["shares"] == 20
    assert result["risk_amount"] == 100
    assert result["risk_per_share"] == 5
    assert result["notional"] == 2_000
    assert result["notional_cap"] is None


def test_position_risk_caps_shares_by_buying_power() -> None:
    result = calculate_position_risk(
        account_size=10_000,
        risk_percent=1,
        entry_price=100,
        stop_price=99,
        buying_power=2_500,
    )

    assert result["shares"] == 25
    assert result["risk_amount"] == 100
    assert result["risk_per_share"] == 1
    assert result["notional"] == 2_500
    assert result["notional_cap"] == 2_500


def test_position_risk_uses_stricter_of_buying_power_and_max_notional() -> None:
    result = calculate_position_risk(
        account_size=10_000,
        risk_percent=2,
        entry_price=50,
        stop_price=49,
        buying_power=5_000,
        max_notional=1_200,
    )

    assert result["shares"] == 24
    assert result["notional"] == 1_200
    assert result["notional_cap"] == 1_200


def test_position_risk_zero_or_negative_notional_cap_produces_zero_shares() -> None:
    result = calculate_position_risk(
        account_size=10_000,
        risk_percent=1,
        entry_price=100,
        stop_price=99,
        buying_power=0,
    )

    assert result["shares"] == 0
    assert result["notional"] == 0
    assert result["notional_cap"] == 0


def test_position_risk_rejects_non_positive_entry_price() -> None:
    result = calculate_position_risk(
        account_size=10_000,
        risk_percent=1,
        entry_price=0,
        stop_price=99,
        buying_power=10_000,
    )

    assert result["shares"] == 0
    assert result["risk_per_share"] == 0
    assert result["notional"] == 0
    assert result["notional_cap"] == 0
