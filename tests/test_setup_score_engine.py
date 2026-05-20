"""
Tests for Phase 3 — Setup Score Engine.

Covers:
- Score components individually
- Full score with strong/weak/mixed setups
- Deductions: warnings, downtrend, overbought RSI
- Label assignment at all thresholds
- rank_universe ordering and filtering
- None/missing metrics handled gracefully
- All scores clamped to [0, 100]
- Determinism: same inputs → same output
"""

from __future__ import annotations

import pytest

from src.scoring.setup_score_engine import (
    SetupScoreResult,
    calculate_setup_score,
    rank_universe,
)


# ── Metric builder ────────────────────────────────────────────────────────────

def _m(
    trend: str = "Strong Uptrend",
    rsi14: float = 58.0,
    rs_spread: float = 5.0,
    rs_label: str = "Leader",
    rvol: float = 1.3,
    atr_pct: float = 1.5,
    warnings: list | None = None,
) -> dict:
    return {
        "trend": trend,
        "rsi14": rsi14,
        "rs_spread": rs_spread,
        "rs_label": rs_label,
        "rvol": rvol,
        "atr_pct": atr_pct,
        "warnings": warnings or [],
    }


# ── Return type ───────────────────────────────────────────────────────────────

class TestSetupScoreResultType:
    def test_returns_dataclass(self):
        result = calculate_setup_score("NVDA", _m())
        assert isinstance(result, SetupScoreResult)

    def test_symbol_preserved(self):
        result = calculate_setup_score("AAPL", _m())
        assert result.symbol == "AAPL"

    def test_score_is_float(self):
        result = calculate_setup_score("NVDA", _m())
        assert isinstance(result.score, float)

    def test_label_is_string(self):
        result = calculate_setup_score("NVDA", _m())
        assert isinstance(result.label, str)

    def test_notes_is_tuple(self):
        result = calculate_setup_score("NVDA", _m())
        assert isinstance(result.notes, tuple)
        assert len(result.notes) == 5  # one per component

    def test_contributions_has_five_keys(self):
        result = calculate_setup_score("NVDA", _m())
        assert set(result.contributions.keys()) == {
            "trend_quality",
            "relative_strength",
            "momentum_quality",
            "volume_confirmation",
            "risk_reward_profile",
        }


# ── Score range ───────────────────────────────────────────────────────────────

class TestScoreRange:
    def test_max_score_scenario(self):
        result = calculate_setup_score("NVDA", _m(
            trend="Strong Uptrend", rsi14=58, rs_spread=15, rs_label="Leader",
            rvol=2.0, atr_pct=1.5, warnings=[],
        ))
        assert result.score <= 100.0

    def test_min_score_scenario(self):
        result = calculate_setup_score("NVDA", _m(
            trend="Downtrend", rsi14=30, rs_spread=-15, rs_label="Weak",
            rvol=0.3, atr_pct=9.0, warnings=["w1", "w2", "w3"],
        ))
        assert result.score >= 0.0

    def test_all_scenarios_in_range(self):
        scenarios = [
            _m(), _m(trend="Downtrend", rsi14=30), _m(trend="Mixed", rsi14=75),
            _m(rvol=0.1, atr_pct=15.0), _m(warnings=["a", "b", "c", "d"]),
        ]
        for m in scenarios:
            result = calculate_setup_score("X", m)
            assert 0.0 <= result.score <= 100.0, f"score={result.score} out of range"


# ── Component scoring ─────────────────────────────────────────────────────────

class TestTrendComponent:
    def test_strong_uptrend_max_points(self):
        r = calculate_setup_score("X", _m(trend="Strong Uptrend"))
        assert r.contributions["trend_quality"] == 25.0

    def test_uptrend_mid_points(self):
        r = calculate_setup_score("X", _m(trend="Uptrend"))
        assert r.contributions["trend_quality"] == 17.0

    def test_mixed_low_points(self):
        r = calculate_setup_score("X", _m(trend="Mixed"))
        assert r.contributions["trend_quality"] == 8.0

    def test_downtrend_zero_points(self):
        r = calculate_setup_score("X", _m(trend="Downtrend"))
        assert r.contributions["trend_quality"] == 0.0


class TestRelativeStrengthComponent:
    def test_leader_with_strong_spread_high_score(self):
        r = calculate_setup_score("X", _m(rs_spread=12.0, rs_label="Leader"))
        assert r.contributions["relative_strength"] >= 22.0

    def test_weak_with_negative_spread_low_score(self):
        r = calculate_setup_score("X", _m(rs_spread=-12.0, rs_label="Weak"))
        assert r.contributions["relative_strength"] < 8.0

    def test_leader_bonus_applied(self):
        r_leader = calculate_setup_score("X", _m(rs_spread=5.0, rs_label="Leader"))
        r_neutral = calculate_setup_score("X", _m(rs_spread=5.0, rs_label="Neutral"))
        assert r_leader.contributions["relative_strength"] > r_neutral.contributions["relative_strength"]


class TestMomentumComponent:
    def test_ideal_zone_max_points(self):
        for rsi in [50.0, 58.0, 65.0]:
            r = calculate_setup_score("X", _m(rsi14=rsi))
            assert r.contributions["momentum_quality"] == 20.0

    def test_weak_zone_low_points(self):
        r = calculate_setup_score("X", _m(rsi14=38.0))
        assert r.contributions["momentum_quality"] == 4.0


class TestVolumeComponent:
    def test_strong_rvol_max_points(self):
        r = calculate_setup_score("X", _m(rvol=1.8))
        assert r.contributions["volume_confirmation"] == 15.0

    def test_weak_rvol_low_points(self):
        r = calculate_setup_score("X", _m(rvol=0.4))
        assert r.contributions["volume_confirmation"] == 1.0


class TestAtrComponent:
    def test_ideal_atr_max_points(self):
        for atr in [0.8, 2.0, 3.5]:
            r = calculate_setup_score("X", _m(atr_pct=atr))
            assert r.contributions["risk_reward_profile"] == 15.0

    def test_extreme_atr_low_points(self):
        r = calculate_setup_score("X", _m(atr_pct=10.0))
        assert r.contributions["risk_reward_profile"] == 2.0


# ── Deductions ────────────────────────────────────────────────────────────────

class TestDeductions:
    def test_one_warning_deducted(self):
        no_warn = calculate_setup_score("X", _m(warnings=[]))
        with_warn = calculate_setup_score("X", _m(warnings=["issue1"]))
        assert with_warn.score == pytest.approx(no_warn.score - 10.0, abs=0.1)
        assert len(with_warn.deductions) == 1

    def test_max_three_warnings_capped(self):
        r4 = calculate_setup_score("X", _m(warnings=["a", "b", "c", "d"]))
        r3 = calculate_setup_score("X", _m(warnings=["a", "b", "c"]))
        # 4 warnings should cap at 3×10=30 deduction, same as 3
        assert r4.score == pytest.approx(r3.score, abs=0.1)

    def test_downtrend_deduction_applied(self):
        uptrend = calculate_setup_score("X", _m(trend="Strong Uptrend"))
        downtrend = calculate_setup_score("X", _m(trend="Downtrend"))
        # Downtrend: 0 pts trend + 15 deduction vs 25 pts trend
        assert downtrend.score < uptrend.score
        assert any("Downtrend" in d for d in downtrend.deductions)

    def test_overbought_rsi_deduction(self):
        normal = calculate_setup_score("X", _m(rsi14=58.0))
        overbought = calculate_setup_score("X", _m(rsi14=75.0))
        assert overbought.score < normal.score
        assert any("chase" in d for d in overbought.deductions)

    def test_no_deductions_when_clean(self):
        r = calculate_setup_score("X", _m())
        assert r.deductions == []


# ── Label assignment ──────────────────────────────────────────────────────────

class TestLabelAssignment:
    def test_high_conviction_label(self):
        # Best possible setup
        r = calculate_setup_score("X", _m(
            trend="Strong Uptrend", rsi14=60, rs_spread=15, rs_label="Leader",
            rvol=2.0, atr_pct=1.5,
        ))
        assert r.label == "High Conviction"
        assert r.score >= 80.0

    def test_avoid_label_on_weak_setup(self):
        r = calculate_setup_score("X", _m(
            trend="Downtrend", rsi14=28, rs_spread=-15, rs_label="Weak",
            rvol=0.2, atr_pct=12.0, warnings=["w1", "w2", "w3"],
        ))
        assert r.label == "Avoid"

    def test_all_labels_reachable(self):
        """Each label must be achievable — none are dead code."""
        labels_seen = set()

        configs = [
            _m(trend="Strong Uptrend", rsi14=60, rs_spread=15, rs_label="Leader", rvol=2.0, atr_pct=1.5),
            _m(trend="Uptrend", rsi14=55, rs_spread=4, rs_label="Neutral", rvol=1.1, atr_pct=2.0),
            _m(trend="Mixed", rsi14=50, rs_spread=0, rs_label="Neutral", rvol=0.9, atr_pct=2.5),
            _m(trend="Mixed", rsi14=42, rs_spread=-5, rs_label="Weak", rvol=0.7, atr_pct=4.0),
            _m(trend="Downtrend", rsi14=28, rs_spread=-15, rs_label="Weak", rvol=0.2, atr_pct=12.0,
               warnings=["w1", "w2", "w3"]),
        ]
        for m in configs:
            r = calculate_setup_score("X", m)
            labels_seen.add(r.label)

        expected = {"High Conviction", "Watchlist", "Early Stage", "Risky", "Avoid"}
        assert labels_seen == expected


# ── Determinism ───────────────────────────────────────────────────────────────

class TestDeterminism:
    def test_same_inputs_same_score(self):
        m = _m(trend="Uptrend", rsi14=55, rs_spread=3.5, rs_label="Neutral", rvol=1.2)
        r1 = calculate_setup_score("NVDA", m)
        r2 = calculate_setup_score("NVDA", m)
        assert r1.score == r2.score
        assert r1.label == r2.label

    def test_different_symbols_same_metrics_same_score(self):
        m = _m()
        assert calculate_setup_score("NVDA", m).score == calculate_setup_score("AMD", m).score


# ── Edge cases ────────────────────────────────────────────────────────────────

class TestEdgeCases:
    def test_none_trend_handled(self):
        m = {**_m(), "trend": None}
        r = calculate_setup_score("X", m)
        assert 0.0 <= r.score <= 100.0

    def test_none_rsi_handled(self):
        m = {**_m(), "rsi14": None}
        r = calculate_setup_score("X", m)
        assert 0.0 <= r.score <= 100.0

    def test_missing_warnings_key_handled(self):
        m = {k: v for k, v in _m().items() if k != "warnings"}
        r = calculate_setup_score("X", m)
        assert 0.0 <= r.score <= 100.0


# ── rank_universe ─────────────────────────────────────────────────────────────

class TestRankUniverse:
    def _make_universe(self) -> dict:
        return {
            "NVDA": _m(trend="Strong Uptrend", rs_spread=12, rs_label="Leader", rvol=1.8),
            "MSFT": _m(trend="Uptrend", rs_spread=3, rs_label="Neutral"),
            "CSCO": _m(trend="Downtrend", rs_spread=-8, rs_label="Weak", warnings=["w1"]),
            "BAD":  None,
        }

    def test_returns_list(self):
        results = rank_universe(self._make_universe())
        assert isinstance(results, list)

    def test_none_symbols_excluded(self):
        results = rank_universe(self._make_universe())
        symbols = [r.symbol for r in results]
        assert "BAD" not in symbols

    def test_sorted_descending_by_score(self):
        results = rank_universe(self._make_universe())
        scores = [r.score for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_min_score_filter(self):
        results = rank_universe(self._make_universe(), min_score=60.0)
        for r in results:
            assert r.score >= 60.0

    def test_empty_map_returns_empty_list(self):
        assert rank_universe({}) == []

    def test_all_none_returns_empty_list(self):
        assert rank_universe({"A": None, "B": None}) == []

    def test_best_symbol_is_first(self):
        results = rank_universe(self._make_universe())
        assert results[0].symbol == "NVDA"
