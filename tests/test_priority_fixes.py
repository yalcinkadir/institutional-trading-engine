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
from unittest.mock import MagicMock

import pytest

from src.data_path_policy import (
    REQUIRED_IGNORED_DATA_PATTERNS,
    TRACKABLE_AUDIT_DATA_PATHS,
    missing_required_ignored_data_patterns,
    normalize_gitignore_lines,
    prohibited_global_data_ignore_patterns,
)
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

        assert report.get("data_quality_note") != ""

    def test_risk_off_regime_keeps_low_heat(self):
        regime = _make_market_regime(regime="risk_off", health=30)
        screener = _make_screener()
        report = _build_decision_report_with_valid_portfolio(regime, screener)

        assert report["portfolio_heat_limit"] <= 0.5

    def test_bullish_vix_missing_regime_parsed_correctly(self):
        """'Bullish (VIX missing)' must be parsed as LOW_VOL_BULL."""
        regime = _make_market_regime(regime="Bullish (VIX missing)", health=75)
        screener = _make_screener()
        report = _build_decision_report_with_valid_portfolio(regime, screener)

        assert report["market_state"] == "low_vol_bull"


# ── Fix 2: signal_generator ───────────────────────────────────────────────

class TestSignalGenerator:
    def _make_decision_report(self, decision: str = "approved") -> dict:
        return {
            "market_state": "low_vol_bull",
            "decisions": [
                {
                    "symbol": "NVDA",
                    "decision": decision,
                    "setup_type": "momentum_breakout",
                    "risk_tier": "tier_1",
                    "position_size_multiplier": 1.0,
                    "setup_score": 80,
                    "regime_alignment": 0.82,
                    "asymmetry_score": 0.72,
                    "data_confidence": 0.85,
                    "score_source": "scanner_derived",
                    "data_source": "live",
                    "thresholds_version": "report_scoring_v2",
                    "blocked_reasons": [],
                    "notes": [],
                }
            ],
        }

    def _make_metrics_map(self) -> dict:
        return {
            "NVDA": {
                "close": 225.0,
                "atr14": 8.0,
                "atr_pct": 3.6,
                "entry": None,
                "stop_loss": None,
                "exit_1": None,
                "exit_2": None,
                "source": "polygon",
                "source_timestamp": "2026-06-03T14:30:00+00:00",
                "fallback_level": "primary",
                "data_status": "OK",
            }
        }

    def test_approved_produces_buy_watch(self):
        from src.signals.signal_generator import build_signals
        signals = build_signals(self._make_decision_report("approved"),
                                self._make_metrics_map(), "Bullish")
        assert len(signals) == 1
        assert signals[0].action == "BUY_WATCH"

    def test_blocked_produces_no_trade(self):
        from src.signals.signal_generator import build_signals
        signals = build_signals(self._make_decision_report("blocked"),
                                self._make_metrics_map(), "Bullish")
        assert signals[0].action == "NO_TRADE"

    def test_entry_stop_target_derived_for_buy_watch(self):
        from src.signals.signal_generator import build_signals
        signals = build_signals(self._make_decision_report("approved"),
                                self._make_metrics_map(), "Bullish")
        s = signals[0]
        assert s.entry_trigger is not None
        assert s.stop_loss is not None
        assert s.target_1 is not None
        assert s.entry_trigger > s.stop_loss

    def test_risk_reward_calculated(self):
        from src.signals.signal_generator import build_signals
        signals = build_signals(self._make_decision_report("approved"),
                                self._make_metrics_map(), "Bullish")
        assert signals[0].risk_reward is not None
        assert signals[0].risk_reward > 0

    def test_no_trade_has_no_entry_levels(self):
        from src.signals.signal_generator import build_signals
        signals = build_signals(self._make_decision_report("no_trade"),
                                self._make_metrics_map(), "Bullish")
        assert signals[0].entry_trigger is None

    def test_valid_until_is_future_date(self):
        from datetime import date
        from src.signals.signal_generator import build_signals
        signals = build_signals(self._make_decision_report(), {}, "Bullish")
        today = date.today().isoformat()
        assert signals[0].valid_until > today

    def test_save_signals_writes_json_and_md(self, tmp_path):
        from src.signals.signal_generator import build_signals, save_signals
        signals = build_signals(self._make_decision_report(),
                                self._make_metrics_map(), "Bullish")
        json_path, md_path = save_signals(signals, date_str="2026-05-20",
                                          signals_dir=tmp_path)
        assert json_path.exists()
        assert md_path.exists()
        payload = json.loads(json_path.read_text())
        assert "signals" in payload
        assert payload["total_signals"] == 1

    def test_json_payload_is_valid(self, tmp_path):
        from src.signals.signal_generator import build_signals, save_signals
        signals = build_signals(self._make_decision_report(),
                                self._make_metrics_map(), "Bullish")
        json_path, _ = save_signals(signals, date_str="2026-05-20",
                                    signals_dir=tmp_path)
        payload = json.loads(json_path.read_text())
        for sig in payload["signals"]:
            assert "symbol" in sig
            assert "action" in sig
            assert "generated_at" in sig

    def test_no_signals_still_produces_files(self, tmp_path):
        from src.signals.signal_generator import build_signals, save_signals
        signals = build_signals({"decisions": []}, {}, "Unknown")
        json_path, md_path = save_signals(signals, date_str="2026-05-20",
                                          signals_dir=tmp_path)
        assert json_path.exists()

    def test_momentum_breakout_entry_above_close(self):
        from src.signals.signal_generator import build_signals
        signals = build_signals(self._make_decision_report("approved"),
                                self._make_metrics_map(), "Bullish")
        s = signals[0]
        close = self._make_metrics_map()["NVDA"]["close"]
        assert s.entry_trigger > close

    def test_all_numeric_fields_are_finite(self):
        from src.signals.signal_generator import build_signals
        import dataclasses
        signals = build_signals(self._make_decision_report(),
                                self._make_metrics_map(), "Bullish")
        s = signals[0]
        for f in dataclasses.fields(s):
            v = getattr(s, f.name)
            if isinstance(v, float):
                assert not math.isnan(v), f"{f.name} is NaN"


# ── Fix 3: generate_outcomes real EOD ─────────────────────────────────────

class TestGenerateOutcomesReal:
    def _make_bars(self, closes: list[float]) -> list[dict]:
        """Make fake Polygon bars with timestamps."""
        from datetime import datetime, timedelta
        base = datetime(2026, 5, 15)
        bars = []
        for i, c in enumerate(closes):
            ts = int((base + timedelta(days=i)).timestamp() * 1000)
            bars.append({"t": ts, "c": c, "o": c, "h": c + 1, "l": c - 1, "v": 1e6})
        return bars

    def test_real_outcome_win(self):
        from scripts.generate_outcomes import fetch_real_outcomes
        client = MagicMock()
        client.get_daily_bars.return_value = self._make_bars(
            [100.0] * 2 + [103.0] + [100.0] * 3 + [105.0] + [100.0] * 14 + [108.0]
        )
        result = fetch_real_outcomes("2026-05-15", "NVDA", 100.0, client)
        assert result["result_5d"] is not None
        assert result["classification"] in {"WIN", "NEUTRAL", "LOSS", "PENDING"}

    def test_real_outcome_pending_when_no_api_key(self):
        from scripts.generate_outcomes import fetch_real_outcomes
        client = MagicMock()
        client.get_daily_bars.side_effect = Exception("no key")
        result = fetch_real_outcomes("2026-05-15", "NVDA", 100.0, client)
        assert result["classification"] == "PENDING"
        assert result["result_5d"] is None
        assert "reason" in result

    def test_no_mock_performance_in_script(self):
        """Ensure build_mock_outcomes is no longer called in main()."""
        import inspect
        import scripts.generate_outcomes as mod
        source = inspect.getsource(mod.main)
        assert "build_mock_outcomes" not in source, (
            "build_mock_outcomes still called in main() — mock not removed"
        )

    def test_pct_calculation(self):
        from scripts.generate_outcomes import _pct
        assert _pct(100.0, 105.0) == pytest.approx(5.0)
        assert _pct(100.0, 95.0) == pytest.approx(-5.0)
        assert _pct(0.0, 100.0) == 0.0

    def test_win_classification(self):
        from scripts.generate_outcomes import fetch_real_outcomes
        client = MagicMock()
        bars = self._make_bars([100.0] * 6 + [103.0] + [100.0] * 15)
        client.get_daily_bars.return_value = bars
        result = fetch_real_outcomes("2026-05-15", "NVDA", 100.0, client)
        if result["result_5d"] is not None and result["result_5d"] >= 1.0:
            assert result["classification"] == "WIN"

    def test_outcome_files_written(self, tmp_path):
        from scripts.generate_outcomes import write_outcome_reports
        outcomes = [
            {"symbol": "NVDA", "signal_date": "2026-05-15", "action": "BUY_WATCH",
             "setup_type": "momentum_breakout", "entry_trigger": 226.0,
             "close_at_signal": 225.0, "market_regime": "Bullish",
             "result_1d": 1.5, "result_5d": 2.3, "result_20d": None,
             "classification": "WIN"},
        ]

        import scripts.generate_outcomes as mod
        orig = mod.OUTCOMES_DIR
        mod.OUTCOMES_DIR = tmp_path / "outcomes"

        try:
            write_outcome_reports(outcomes, "2026-05-15")
        finally:
            mod.OUTCOMES_DIR = orig

        md_files = list((tmp_path / "outcomes").glob("*.md"))
        json_files = list((tmp_path / "outcomes").glob("*.json"))
        assert len(md_files) >= 1
        assert len(json_files) >= 1


# ── data/ persistence ──────────────────────────────────────────────────────

class TestDataPersistence:
    def test_data_gitkeep_exists(self):
        gitkeep = Path("data/.gitkeep")
        if not gitkeep.exists():
            pytest.skip("data/.gitkeep not yet committed — add it")

    def test_data_path_policy_does_not_ignore_audit_root(self):
        gitignore = Path(".gitignore")
        if not gitignore.exists():
            return
        content = gitignore.read_text(encoding="utf-8")
        assert prohibited_global_data_ignore_patterns(content) == [], (
            "root-level data/ is in .gitignore — decision logs/evidence would be lost"
        )

    def test_data_path_policy_ignores_sensitive_operational_feeds(self):
        gitignore = Path(".gitignore")
        if not gitignore.exists():
            return
        content = gitignore.read_text(encoding="utf-8")
        assert missing_required_ignored_data_patterns(content) == []
        entries = normalize_gitignore_lines(content)
        for pattern in REQUIRED_IGNORED_DATA_PATTERNS:
            assert pattern in entries

    def test_trackable_audit_data_paths_are_not_explicitly_ignored(self):
        gitignore = Path(".gitignore")
        if not gitignore.exists():
            return
        entries = normalize_gitignore_lines(gitignore.read_text(encoding="utf-8"))
        for path in TRACKABLE_AUDIT_DATA_PATHS:
            assert path not in entries
