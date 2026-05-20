"""
Tests for src/bridge/scanner_to_orchestrator.py

Covers:
- Full translation with healthy live data
- Translation with missing VIX (fallback path)
- Translation with empty/minimal universe
- Individual derivation functions
- Output validity: all floats in expected ranges
- Auditability: all fields have derivation notes
"""

from __future__ import annotations

import math

import pandas as pd
import pytest

from src.bridge.scanner_to_orchestrator import (
    BridgeTranslation,
    _clamp,
    _derive_equity_strength,
    _derive_feature_alpha_score,
    _derive_gap_risk,
    _derive_gold_strength,
    _derive_market_regime_score,
    _safe_float,
    translate,
)


# ── Fixtures ────────────────────────────────────────────────────────────────

def _make_spy_metrics(
    close: float = 500.0,
    trend: str = "Strong Uptrend",
    rsi14: float = 58.0,
    atr_pct: float = 1.2,
    ret_20d: float = 4.0,
    rs_spread: float = 0.0,
    rs_label: str = "Neutral",
    rvol: float = 1.1,
    volume: int = 80_000_000,
    vol20: float = 75_000_000,
    setup_readiness: str = "Trend Strong, Entry Unclear",
) -> dict:
    return {
        "symbol": "SPY",
        "close": close,
        "high": close * 1.005,
        "low": close * 0.995,
        "volume": volume,
        "sma20": close * 0.98,
        "sma50": close * 0.95,
        "sma200": close * 0.90,
        "rsi14": rsi14,
        "atr14": close * (atr_pct / 100),
        "atr_pct": atr_pct,
        "vol20": vol20,
        "rvol": rvol,
        "ret_20d": ret_20d,
        "benchmark": "SPY",
        "benchmark_ret_20d": ret_20d,
        "rs_spread": rs_spread,
        "rs_label": rs_label,
        "trend": trend,
        "momentum": "Strong",
        "volatility": "Normal",
        "rvol_label": "Normal",
        "setup_readiness": setup_readiness,
        "warnings": [],
        "entry": pd.NA,
        "stop_loss": pd.NA,
        "exit_1": pd.NA,
        "exit_2": pd.NA,
    }


def _make_qqq_metrics(**kwargs) -> dict:
    m = _make_spy_metrics(**kwargs)
    m["symbol"] = "QQQ"
    m["benchmark"] = "QQQ"
    return m


def _make_nvda_metrics(
    trend: str = "Strong Uptrend",
    rs_label: str = "Leader",
    setup_readiness: str = "Breakout Watch",
    rs_spread: float = 8.0,
    rvol: float = 1.3,
    rsi14: float = 58.0,
    ret_20d: float = 12.0,
) -> dict:
    m = _make_spy_metrics()
    m["symbol"] = "NVDA"
    m["benchmark"] = "QQQ"
    m["trend"] = trend
    m["rs_label"] = rs_label
    m["rs_spread"] = rs_spread
    m["setup_readiness"] = setup_readiness
    m["rvol"] = rvol
    m["rsi14"] = rsi14
    m["ret_20d"] = ret_20d
    return m


def _make_gld_metrics(trend: str = "Uptrend", rsi14: float = 52.0, ret_20d: float = 2.0) -> dict:
    m = _make_spy_metrics()
    m["symbol"] = "GLD"
    m["benchmark"] = "GLD"
    m["trend"] = trend
    m["rsi14"] = rsi14
    m["ret_20d"] = ret_20d
    m["rs_label"] = "Neutral"
    m["setup_readiness"] = "Not Ready"
    return m


def _make_vix_data(close: float = 16.5, direction: str = "Falling") -> dict:
    return {"close": close, "direction": direction}


def _make_full_metrics_map() -> dict:
    return {
        "SPY": _make_spy_metrics(),
        "QQQ": _make_qqq_metrics(),
        "NVDA": _make_nvda_metrics(),
        "GLD": _make_gld_metrics(),
    }


# ── _safe_float ─────────────────────────────────────────────────────────────

class TestSafeFloat:
    def test_valid_float(self):
        assert _safe_float(3.14, 0.0) == pytest.approx(3.14)

    def test_none_returns_fallback(self):
        assert _safe_float(None, 99.0) == pytest.approx(99.0)

    def test_nan_returns_fallback(self):
        assert _safe_float(float("nan"), 42.0) == pytest.approx(42.0)

    def test_inf_returns_fallback(self):
        assert _safe_float(float("inf"), 5.0) == pytest.approx(5.0)

    def test_string_float(self):
        assert _safe_float("12.5", 0.0) == pytest.approx(12.5)

    def test_invalid_string_returns_fallback(self):
        assert _safe_float("not_a_number", 7.0) == pytest.approx(7.0)

    def test_pandas_na_returns_fallback(self):
        assert _safe_float(pd.NA, 3.0) == pytest.approx(3.0)


# ── _clamp ───────────────────────────────────────────────────────────────────

class TestClamp:
    def test_within_range(self):
        assert _clamp(50.0, 0.0, 100.0) == pytest.approx(50.0)

    def test_below_min(self):
        assert _clamp(-10.0, 0.0, 100.0) == pytest.approx(0.0)

    def test_above_max(self):
        assert _clamp(120.0, 0.0, 100.0) == pytest.approx(100.0)


# ── _derive_equity_strength ──────────────────────────────────────────────────

class TestDeriveEquityStrength:
    def test_strong_uptrend_returns_high_score(self):
        m = {"SPY": _make_spy_metrics(trend="Strong Uptrend", rsi14=58.0, ret_20d=6.0)}
        score, note = _derive_equity_strength(m)
        assert score > 60.0
        assert "SPY" in note

    def test_downtrend_returns_low_score(self):
        m = {"SPY": _make_spy_metrics(trend="Downtrend", rsi14=35.0, ret_20d=-10.0)}
        score, note = _derive_equity_strength(m)
        assert score < 40.0

    def test_missing_spy_qqq_returns_fallback(self):
        score, note = _derive_equity_strength({})
        assert score == pytest.approx(50.0)
        assert "fallback" in note

    def test_overbought_rsi_penalized(self):
        strong = _make_spy_metrics(rsi14=58.0, trend="Strong Uptrend")
        extended = _make_spy_metrics(rsi14=80.0, trend="Strong Uptrend")
        score_strong, _ = _derive_equity_strength({"SPY": strong})
        score_extended, _ = _derive_equity_strength({"SPY": extended})
        assert score_strong > score_extended

    def test_output_in_valid_range(self):
        for trend in ["Strong Uptrend", "Uptrend", "Mixed", "Downtrend"]:
            m = {"SPY": _make_spy_metrics(trend=trend)}
            score, _ = _derive_equity_strength(m)
            assert 0.0 <= score <= 100.0, f"Score {score} out of range for trend={trend}"


# ── _derive_gold_strength ────────────────────────────────────────────────────

class TestDeriveGoldStrength:
    def test_strong_gold_returns_high_score(self):
        m = {"GLD": _make_gld_metrics(trend="Strong Uptrend", rsi14=62.0, ret_20d=8.0)}
        score, _ = _derive_gold_strength(m)
        assert score > 60.0

    def test_missing_gld_returns_fallback(self):
        score, note = _derive_gold_strength({})
        assert score == pytest.approx(50.0)
        assert "fallback" in note

    def test_output_in_valid_range(self):
        for ret in [-15, -5, 0, 5, 15]:
            m = {"GLD": _make_gld_metrics(ret_20d=float(ret))}
            score, _ = _derive_gold_strength(m)
            assert 0.0 <= score <= 100.0


# ── _derive_market_regime_score ───────────────────────────────────────────────

class TestDeriveMarketRegimeScore:
    def test_risk_on_conditions_yield_high_score(self):
        m = {
            "SPY": _make_spy_metrics(trend="Strong Uptrend", rsi14=62.0),
            "QQQ": _make_qqq_metrics(trend="Strong Uptrend", rsi14=60.0),
            "NVDA": _make_nvda_metrics(rs_label="Leader"),
        }
        score, _ = _derive_market_regime_score(m, vix_level=14.0)
        assert score > 65.0

    def test_risk_off_conditions_yield_low_score(self):
        m = {
            "SPY": _make_spy_metrics(trend="Downtrend", rsi14=38.0),
            "QQQ": _make_qqq_metrics(trend="Downtrend", rsi14=35.0),
        }
        score, _ = _derive_market_regime_score(m, vix_level=38.0)
        assert score < 35.0

    def test_vix_35_penalty_applied(self):
        m = {"SPY": _make_spy_metrics(), "QQQ": _make_qqq_metrics()}
        low_vix, _ = _derive_market_regime_score(m, vix_level=14.0)
        high_vix, _ = _derive_market_regime_score(m, vix_level=38.0)
        assert low_vix > high_vix

    def test_output_in_valid_range(self):
        m = _make_full_metrics_map()
        for vix in [10.0, 20.0, 30.0, 45.0]:
            score, _ = _derive_market_regime_score(m, vix_level=vix)
            assert 0.0 <= score <= 100.0, f"Score {score} out of range for vix={vix}"


# ── _derive_gap_risk ──────────────────────────────────────────────────────────

class TestDeriveGapRisk:
    def test_high_vix_increases_gap_risk(self):
        m = _make_full_metrics_map()
        low_risk, _ = _derive_gap_risk(m, vix_level=14.0)
        high_risk, _ = _derive_gap_risk(m, vix_level=40.0)
        assert high_risk > low_risk

    def test_output_in_valid_range(self):
        m = _make_full_metrics_map()
        for vix in [12.0, 20.0, 30.0, 45.0]:
            score, _ = _derive_gap_risk(m, vix_level=vix)
            assert 0.0 <= score <= 50.0


# ── _derive_feature_alpha_score ───────────────────────────────────────────────

class TestDeriveFeatureAlphaScore:
    def test_many_actionable_setups_yield_high_score(self):
        m = {
            "NVDA": _make_nvda_metrics(setup_readiness="Breakout Watch"),
            "AMD": _make_nvda_metrics(setup_readiness="Pullback Candidate"),
            "MSFT": _make_nvda_metrics(setup_readiness="Breakout Watch"),
        }
        score, note = _derive_feature_alpha_score(m)
        assert score > 70.0

    def test_all_weak_setups_yield_low_score(self):
        m = {}
        for sym in ["NVDA", "AMD", "MSFT", "META"]:
            entry = _make_nvda_metrics(setup_readiness="Weak - Avoid")
            entry["symbol"] = sym
            m[sym] = entry
        score, _ = _derive_feature_alpha_score(m)
        assert score < 40.0

    def test_empty_universe_returns_fallback(self):
        # Only index symbols — filtered out
        score, note = _derive_feature_alpha_score(
            {"SPY": _make_spy_metrics(), "QQQ": _make_qqq_metrics()}
        )
        assert score == pytest.approx(50.0)
        assert "fallback" in note


# ── translate (full integration) ─────────────────────────────────────────────

class TestTranslate:
    def test_returns_bridge_translation(self):
        result = translate(_make_full_metrics_map(), _make_vix_data())
        assert isinstance(result, BridgeTranslation)

    def test_all_inputs_are_floats(self):
        result = translate(_make_full_metrics_map(), _make_vix_data())
        inputs = result.inputs
        for field_name in inputs.__dataclass_fields__:
            val = getattr(inputs, field_name)
            assert isinstance(val, float), f"{field_name}={val!r} is not float"

    def test_all_inputs_in_valid_ranges(self):
        result = translate(_make_full_metrics_map(), _make_vix_data())
        i = result.inputs

        assert 0.0 <= i.market_regime_score <= 100.0
        assert 0.0 <= i.equity_strength <= 100.0
        assert 0.0 <= i.bond_strength <= 100.0
        assert 0.0 <= i.dollar_strength <= 100.0
        assert 0.0 <= i.gold_strength <= 100.0
        assert i.volatility_level > 0.0
        assert 0.0 <= i.gap_risk_percent <= 50.0
        assert 0.0 <= i.liquidity_stress_percent <= 100.0
        assert 0.0 <= i.feature_alpha_score <= 100.0
        assert i.average_daily_volume_millions > 0.0
        assert i.bid_ask_spread_percent > 0.0
        assert i.order_size_percent_adv > 0.0

    def test_missing_vix_uses_fallback(self):
        result = translate(_make_full_metrics_map(), vix_data=None)
        assert result.inputs.volatility_level == pytest.approx(25.0)
        assert len(result.data_quality_warnings) >= 1
        assert any("VIX" in w for w in result.data_quality_warnings)

    def test_live_vix_is_used_when_available(self):
        result = translate(_make_full_metrics_map(), _make_vix_data(close=18.5))
        assert result.inputs.volatility_level == pytest.approx(18.5)
        assert not any("VIX" in w for w in result.data_quality_warnings)

    def test_all_derivation_notes_present(self):
        result = translate(_make_full_metrics_map(), _make_vix_data())
        expected_keys = {
            "volatility_level",
            "equity_strength",
            "gold_strength",
            "dollar_strength",
            "bond_strength",
            "market_regime_score",
            "gap_risk_percent",
            "liquidity_stress_percent",
            "feature_alpha_score",
            "average_daily_volume_millions",
            "bid_ask_spread_percent",
            "order_size_percent_adv",
            "portfolio_inputs",
        }
        for key in expected_keys:
            assert key in result.derivation_notes, f"Missing derivation note: {key}"

    def test_symbols_used_populated(self):
        result = translate(_make_full_metrics_map(), _make_vix_data())
        assert len(result.symbols_used) >= 3
        assert "SPY" in result.symbols_used
        assert "QQQ" in result.symbols_used

    def test_no_nan_in_outputs(self):
        result = translate(_make_full_metrics_map(), _make_vix_data())
        inputs = result.inputs
        for field_name in inputs.__dataclass_fields__:
            val = getattr(inputs, field_name)
            assert not math.isnan(val), f"{field_name} is NaN"
            assert not math.isinf(val), f"{field_name} is infinite"

    def test_risk_off_conditions_produce_conservative_regime(self):
        m = {
            "SPY": _make_spy_metrics(trend="Downtrend", rsi14=35.0, ret_20d=-8.0),
            "QQQ": _make_qqq_metrics(trend="Downtrend", rsi14=33.0, ret_20d=-10.0),
            "GLD": _make_gld_metrics(trend="Strong Uptrend", rsi14=65.0, ret_20d=8.0),
        }
        result = translate(m, _make_vix_data(close=34.0))
        # Under stress conditions, regime score should be below 50
        assert result.inputs.market_regime_score < 50.0

    def test_risk_on_conditions_produce_high_equity_strength(self):
        m = {
            "SPY": _make_spy_metrics(trend="Strong Uptrend", rsi14=60.0, ret_20d=8.0),
            "QQQ": _make_qqq_metrics(trend="Strong Uptrend", rsi14=62.0, ret_20d=9.0),
        }
        result = translate(m, _make_vix_data(close=13.5))
        assert result.inputs.equity_strength > 70.0

    def test_empty_metrics_map_uses_fallbacks(self):
        result = translate({}, vix_data=None)
        i = result.inputs
        # Should not crash and all values should be valid floats in range
        for field_name in i.__dataclass_fields__:
            val = getattr(i, field_name)
            assert isinstance(val, float)
            assert not math.isnan(val)

    def test_none_values_in_metrics_map_handled_gracefully(self):
        m = {"SPY": None, "QQQ": None, "NVDA": _make_nvda_metrics()}
        result = translate(m, _make_vix_data())
        # Should not crash
        assert isinstance(result, BridgeTranslation)
