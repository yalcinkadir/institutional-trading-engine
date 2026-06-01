from __future__ import annotations

from pathlib import Path

from src.runtime.portfolio_state import PortfolioState, PortfolioStateStore


def test_er4_corrupt_portfolio_state_loads_fail_closed(tmp_path: Path) -> None:
    path = tmp_path / "portfolio_state.json"
    path.write_text("not-json", encoding="utf-8")

    state = PortfolioStateStore(path).load()

    assert state.governance_valid is False
    assert state.source == "invalid_portfolio_state_fail_closed"
    assert any("Invalid portfolio state JSON" in warning for warning in state.warnings)


def test_er4_non_object_portfolio_state_loads_fail_closed(tmp_path: Path) -> None:
    path = tmp_path / "portfolio_state.json"
    path.write_text("[]", encoding="utf-8")

    state = PortfolioStateStore(path).load()

    assert state.governance_valid is False
    assert state.source == "invalid_portfolio_state_fail_closed"
    assert any("JSON object" in warning for warning in state.warnings)


def test_er4_portfolio_state_save_does_not_leave_tmp_file(tmp_path: Path) -> None:
    path = tmp_path / "portfolio_state.json"
    store = PortfolioStateStore(path)

    store.save(
        PortfolioState(
            equity_start=10_000,
            equity_current=9_900,
            drawdown_percent=-1.0,
            daily_loss_percent=-0.5,
            open_positions=[],
            updated_at="2026-06-01T00:00:00+00:00",
        )
    )

    assert path.exists()
    assert not list(tmp_path.glob("*.tmp"))
    assert store.load().governance_valid is True
