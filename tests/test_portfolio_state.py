from __future__ import annotations

import json
from pathlib import Path

from src.runtime.portfolio_state import (
    PortfolioState,
    PortfolioStateStore,
)


def test_load_missing_file_returns_fail_closed_default(tmp_path: Path) -> None:
    store = PortfolioStateStore(tmp_path / "missing.json")

    state = store.load()

    assert state.drawdown_percent == 0.0
    assert state.daily_loss_percent == 0.0
    assert state.source == "missing_portfolio_state_fail_closed"
    assert state.governance_valid is False
    assert any("fail closed" in warning for warning in state.warnings)


def test_load_valid_portfolio_state(tmp_path: Path) -> None:
    path = tmp_path / "portfolio_state.json"
    path.write_text(
        json.dumps(
            {
                "equity_start": 10000.0,
                "equity_current": 9720.0,
                "drawdown_percent": -2.8,
                "daily_loss_percent": -0.9,
                "open_positions": [
                    {
                        "symbol": "NDQ100",
                        "side": "long",
                        "entry": 29464.38,
                        "current": 29572.0,
                        "risk_amount": 1108.97,
                        "unrealized_pnl": 80.71,
                    }
                ],
                "updated_at": "2026-05-20T22:00:00+02:00",
            }
        ),
        encoding="utf-8",
    )

    state = PortfolioStateStore(path).load()

    assert state.equity_start == 10000.0
    assert state.equity_current == 9720.0
    assert state.drawdown_percent == -2.8
    assert state.daily_loss_percent == -0.9
    assert state.governance_valid is True
    assert len(state.open_positions) == 1
    assert state.open_positions[0].symbol == "NDQ100"


def test_load_explicit_invalid_governance_state(tmp_path: Path) -> None:
    path = tmp_path / "portfolio_state.json"
    path.write_text(
        json.dumps(
            {
                "equity_start": 10000.0,
                "equity_current": 10000.0,
                "drawdown_percent": 0.0,
                "daily_loss_percent": 0.0,
                "open_positions": [],
                "governance_valid": False,
            }
        ),
        encoding="utf-8",
    )

    state = PortfolioStateStore(path).load()

    assert state.governance_valid is False


def test_load_invalid_json_returns_fail_closed_state(tmp_path: Path) -> None:
    path = tmp_path / "portfolio_state.json"
    path.write_text("not-json", encoding="utf-8")

    state = PortfolioStateStore(path).load()

    assert state.source == "invalid_portfolio_state_fail_closed"
    assert state.governance_valid is False
    assert any("Invalid portfolio state JSON" in warning for warning in state.warnings)


def test_load_non_object_returns_fail_closed_state(tmp_path: Path) -> None:
    path = tmp_path / "portfolio_state.json"
    path.write_text("[]", encoding="utf-8")

    state = PortfolioStateStore(path).load()

    assert state.source == "invalid_portfolio_state_fail_closed"
    assert state.governance_valid is False
    assert any("JSON object" in warning for warning in state.warnings)


def test_load_missing_required_field_returns_fail_closed_state(tmp_path: Path) -> None:
    path = tmp_path / "portfolio_state.json"
    path.write_text(
        json.dumps(
            {
                "equity_start": 10000.0,
                "equity_current": 9900.0,
                "drawdown_percent": -1.0,
                "open_positions": [],
            }
        ),
        encoding="utf-8",
    )

    state = PortfolioStateStore(path).load()

    assert state.source == "invalid_portfolio_state_fail_closed"
    assert state.governance_valid is False
    assert any("daily_loss_percent" in warning for warning in state.warnings)


def test_load_non_finite_number_returns_fail_closed_state(tmp_path: Path) -> None:
    path = tmp_path / "portfolio_state.json"
    path.write_text(
        json.dumps(
            {
                "equity_start": 10000.0,
                "equity_current": 9900.0,
                "drawdown_percent": "NaN",
                "daily_loss_percent": 0.0,
                "open_positions": [],
            }
        ),
        encoding="utf-8",
    )

    state = PortfolioStateStore(path).load()

    assert state.source == "invalid_portfolio_state_fail_closed"
    assert state.governance_valid is False
    assert any("Non-finite" in warning for warning in state.warnings)


def test_save_and_reload_roundtrip(tmp_path: Path) -> None:
    path = tmp_path / "portfolio_state.json"
    store = PortfolioStateStore(path)
    state = PortfolioState(
        equity_start=10000.0,
        equity_current=9800.0,
        drawdown_percent=-2.0,
        daily_loss_percent=-0.5,
        open_positions=[],
        updated_at="2026-05-20T22:00:00+02:00",
    )

    saved_path = store.save(state)
    reloaded = store.load()

    assert saved_path == path
    assert reloaded.drawdown_percent == -2.0
    assert reloaded.daily_loss_percent == -0.5
    assert reloaded.governance_valid is True
