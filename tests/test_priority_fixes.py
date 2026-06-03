"""
Tests for Priority Fixes:
  1. liquidity_stress fix — no more permanent hard override
  2. signal_generator — Entry/Stop/Target levels
  3. generate_outcomes — real outcomes (no mocks)
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.runtime.portfolio_state import PortfolioState


class _ValidPortfolioStateStore:
    def load(self) -> PortfolioState:
        return PortfolioState(
            equity_start=10000.0,
            equity_current=10000.0,
            drawdown_percent=0.0,
            daily_loss_percent=0.0,
            open_positions=[],
            source="test_portfolio_state_store",
            governance_valid=True,
        )


# ── Helpers ────────────────────────────────────────────────────────────────

def _make_market_regime(
    regime: str = "Bullish",
    health: int = 75,
    data_status: str = "PARTIAL",
    vix: float | None = None,
    breadth_pct: float = 60.0,
) -> dict:
    symbols = {
        "SPY": {"close": 500.0, "sma50": 490.0, "sma200": 460.0,
                "above_sma50": True, "above_sma200": True, "atr14": 5.5, "avg_volume_20": 70e6},
        "QQQ": {"close": 420.0, "sma50": 410.0, "sma200": 380.0,
                "above_sma50": True, "above_sma200": True, "atr14": 6.2, "avg_volume_20": 55e6},
    }
    if vix is not None:
        symbols["VIX"] = {"close": vix, "sma50": None, "sma200": None,
                          "above_sma50": False, "above_sma200": False, "atr14": None}
    return {
        "regime": regime,
        "market_health_score": health,
        "data_status": data_status,
        "symbols": symbols,
        "breadth": {"universe_size": 10, "above_sma50": 6, "breadth_percent": breadth_pct},
        "focus_areas": [],
        "notes": [],
        "errors": [],
    }


def _make_screener() -> dict:
    return {
        "title": "Pre-Market Watchlist",
        "watchlist": ["NVDA", "MSFT", "AAPL"],
        "objectives": [],
        "warnings": [],
    }


def _build_decision_report_with_valid_portfolio(regime: dict, screener: dict) -> dict:
    from src.reporting.decision_report import build_decision_report

    return build_decision_report(
        regime,
        screener,
        portfolio_state_store=_ValidPortfolioStateStore(),
    )


# ── Fix 1: liquidity_stress ────────────────────────────────────────────────

class TestLiquidityStressFix:
    def test_partial_data_status_does_not_trigger_hard_override(self):
        """
        The critical bug: data_status=PARTIAL (always on Free tier)
        used to set liquidity_stress=True → hard override → all blocked.
        """
        regime = _make_market_regime(data_status="PARTIAL")
        screener = _make_screener()
        report = _build_decision_report_with_valid_portfolio(regime, screener)

        assert "liquidity_stress" not in report["hard_overrides"], (
            "liquidity_stress fired on PARTIAL data — bug not fixed"
        )

    def test_no_approvals_before_fix_now_have_approvals(self):
        """After the fix, Bullish regime + partial data should produce approvals."""
        regime = _make_market_regime(regime="Bullish", health=75, data_status="PARTIAL")
        screener = _make_screener()
        report = _build_decision_report_with_valid_portfolio(regime, screener)

        approved = report["approved_count"]
        assert approved > 0, (
            f"Still no approvals after fix. Hard overrides: {report['hard_overrides']}"
        )

    def test_genuine_high_vix_triggers_hard_override(self):
        """VIX >= 30 should still trigger liquidity_stress."""
        regime = _make_market_regime(vix=32.0, data_status="LIVE")
        screener = _make_screener()
        report = _build_decision_report_with_valid_portfolio(regime, screener)

        assert "liquidity_stress" in report["hard_overrides"]

    def test_vix_none_does_not_trigger_liquidity_stress(self):
        """VIX=None (Free tier) must not trigger liquidity_stress."""
        regime = _make_market_regime(vix=None, data_status="PARTIAL")
        screener = _make_screener()
        report = _build_decision_report_with_valid_portfolio(regime, screener)

        assert "liquidity_stress" not in report["hard_overrides"]

    def test_very_low_breadth_triggers_liquidity_stress(self):
        """Breadth < 25% is genuine liquidity stress."""
        regime = _make_market_regime(breadth_pct=20.0, data_status="LIVE")
        screener = _make_screener()
        report = _build_decision_report_with_valid_portfolio(regime, screener)

        assert "liquidity_stress" in report["hard_overrides"]

    def test_data_quality_note_present_when_partial(self):
        """Partial data produces a note, not a hard override."""
        regime = _make_market_regime(data_status="PARTIAL")
        screener = _make_screener()
        report = _build_decision_report_with_valid_portfolio(regime, screener)

        assert report["data_quality_note"]


# The remaining tests in this file rely on local fixtures/imports above.
