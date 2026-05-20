"""
Setup Score Engine — Phase 3.

Produces a deterministic 0–100 institutional setup score for any symbol
from live scanner metrics. This is the central ranking layer that turns
raw scanner data into actionable institutional priority.

Design principles:
- Deterministic: same inputs always produce same score.
- Explainable: every point contribution is documented.
- No external I/O: pure function, fully testable.
- Conservative scoring: partial credit is given; bonuses require evidence.

Score composition:

  Trend Quality       (0–25 pts)  — structure and momentum direction
  Relative Strength   (0–25 pts)  — leadership vs benchmark
  Momentum Quality    (0–20 pts)  — RSI zone, not overbought
  Volume Confirmation (0–15 pts)  — institutional participation
  Risk-Reward Profile (0–15 pts)  — ATR% appropriateness

  Deductions:
    -10 per warning (max -30)
    -15 if Downtrend
    -10 if RSI > 72 (extended, chase risk)

Final score is clamped to [0, 100].

Labels:
  80–100 → High Conviction
  65–79  → Watchlist
  50–64  → Early Stage
  35–49  → Risky
  0–34   → Avoid
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class SetupScoreResult:
    """
    Result of a single symbol's setup score calculation.

    Attributes:
        symbol:       Ticker symbol.
        score:        0–100 composite score.
        label:        Human-readable quality label.
        contributions: Breakdown of each scoring component.
        deductions:   Applied penalties with reasons.
        notes:        Ordered list of scoring notes (for reports).
    """

    symbol: str
    score: float
    label: str
    contributions: dict[str, float]
    deductions: list[str]
    notes: tuple[str, ...]


def _safe(value: Any, fallback: float) -> float:
    if value is None:
        return fallback
    try:
        f = float(value)
        return fallback if math.isnan(f) or math.isinf(f) else f
    except (TypeError, ValueError):
        return fallback


def _clamp(v: float, lo: float = 0.0, hi: float = 100.0) -> float:
    return max(lo, min(hi, v))


def _trend_score(trend: str | None) -> tuple[float, str]:
    """0–25 pts for trend structure quality."""
    mapping = {
        "Strong Uptrend": (25.0, "Strong Uptrend confirmed (+25)"),
        "Uptrend":        (17.0, "Uptrend confirmed (+17)"),
        "Mixed":          (8.0,  "Mixed trend structure (+8)"),
        "Downtrend":      (0.0,  "Downtrend — no structural support (+0)"),
    }
    pts, note = mapping.get(trend or "", (5.0, f"Trend unknown: {trend!r} (+5)"))
    return pts, note


def _rs_score(rs_spread: float, rs_label: str | None) -> tuple[float, str]:
    """
    0–25 pts for relative strength.

    rs_spread is the 20-day return delta vs benchmark (percentage points).
    Leader label adds a quality bonus.
    """
    # Base: map rs_spread [-15, +15] → [0, 20]
    base = _clamp((rs_spread + 15.0) / 30.0 * 20.0, 0.0, 20.0)

    # Label bonus: confirmed leadership adds 5 pts
    label_bonus = 5.0 if rs_label == "Leader" else 0.0

    pts = _clamp(base + label_bonus, 0.0, 25.0)
    note = (
        f"RS spread={rs_spread:+.1f}pp, label={rs_label or 'N/A'} (+{pts:.0f})"
    )
    return round(pts, 2), note


def _rsi_score(rsi: float) -> tuple[float, str]:
    """
    0–20 pts for RSI zone quality.

    50–65: ideal momentum zone.
    45–50 or 65–70: acceptable.
    <45: weak.
    >70: extended (deduction applied separately).
    """
    if 50.0 <= rsi <= 65.0:
        pts, zone = 20.0, "ideal momentum zone 50–65"
    elif (45.0 <= rsi < 50.0) or (65.0 < rsi <= 70.0):
        pts, zone = 12.0, "acceptable momentum zone"
    elif rsi < 45.0:
        pts, zone = 4.0, "weak momentum (<45)"
    else:
        pts, zone = 8.0, "extended (>70) — see deductions"
    return pts, f"RSI={rsi:.1f} ({zone}) (+{pts:.0f})"


def _rvol_score(rvol: float) -> tuple[float, str]:
    """0–15 pts for relative volume (institutional participation)."""
    if rvol >= 1.5:
        pts, desc = 15.0, "strong institutional participation"
    elif rvol >= 1.2:
        pts, desc = 11.0, "above-average participation"
    elif rvol >= 0.8:
        pts, desc = 6.0, "average participation"
    else:
        pts, desc = 1.0, "weak participation"
    return pts, f"RVOL={rvol:.2f} ({desc}) (+{pts:.0f})"


def _atr_score(atr_pct: float) -> tuple[float, str]:
    """
    0–15 pts for ATR% appropriateness.

    Ideal: 0.8–3.5% — tight enough to size, volatile enough to move.
    Too tight (<0.8%): won't move.
    Too wide (>5%): position sizing becomes punitive.
    """
    if 0.8 <= atr_pct <= 3.5:
        pts, desc = 15.0, "ideal volatility range"
    elif 3.5 < atr_pct <= 5.0:
        pts, desc = 8.0, "elevated but manageable"
    elif atr_pct < 0.8:
        pts, desc = 5.0, "too low — limited movement potential"
    else:
        pts, desc = 2.0, "too high — sizing punitive"
    return pts, f"ATR%={atr_pct:.2f}% ({desc}) (+{pts:.0f})"


def calculate_setup_score(
    symbol: str,
    metrics: dict[str, Any],
) -> SetupScoreResult:
    """
    Calculate institutional setup score for one symbol.

    Args:
        symbol:  Ticker symbol (for labeling only).
        metrics: Scanner metrics dict from scanner.build_symbol_metrics().
                 None values are handled with conservative fallbacks.

    Returns:
        SetupScoreResult with score, label, and full breakdown.
    """
    trend     = metrics.get("trend")
    rs_spread = _safe(metrics.get("rs_spread"), 0.0)
    rs_label  = metrics.get("rs_label")
    rsi       = _safe(metrics.get("rsi14"), 50.0)
    rvol      = _safe(metrics.get("rvol"), 1.0)
    atr_pct   = _safe(metrics.get("atr_pct"), 2.0)
    warnings  = metrics.get("warnings") or []

    contributions: dict[str, float] = {}
    notes: list[str] = []
    deductions: list[str] = []

    # ── Positive contributions ─────────────────────────────────────────────
    trend_pts, trend_note = _trend_score(trend)
    contributions["trend_quality"] = trend_pts
    notes.append(trend_note)

    rs_pts, rs_note = _rs_score(rs_spread, rs_label)
    contributions["relative_strength"] = rs_pts
    notes.append(rs_note)

    rsi_pts, rsi_note = _rsi_score(rsi)
    contributions["momentum_quality"] = rsi_pts
    notes.append(rsi_note)

    rvol_pts, rvol_note = _rvol_score(rvol)
    contributions["volume_confirmation"] = rvol_pts
    notes.append(rvol_note)

    atr_pts, atr_note = _atr_score(atr_pct)
    contributions["risk_reward_profile"] = atr_pts
    notes.append(atr_note)

    raw_score = sum(contributions.values())

    # ── Deductions ────────────────────────────────────────────────────────
    # Warnings from scanner (data quality, structural issues)
    warning_penalty = min(len(warnings), 3) * 10.0
    if warning_penalty > 0:
        raw_score -= warning_penalty
        deductions.append(f"scanner warnings ×{min(len(warnings), 3)}: -{warning_penalty:.0f}")

    # Downtrend structural deduction
    if trend == "Downtrend":
        raw_score -= 15.0
        deductions.append("Downtrend structural deduction: -15")

    # Overbought / chase risk
    if rsi > 72.0:
        raw_score -= 10.0
        deductions.append(f"RSI={rsi:.1f} chase-risk deduction: -10")

    final_score = round(_clamp(raw_score, 0.0, 100.0), 1)

    # ── Label ──────────────────────────────────────────────────────────────
    if final_score >= 80:
        label = "High Conviction"
    elif final_score >= 65:
        label = "Watchlist"
    elif final_score >= 50:
        label = "Early Stage"
    elif final_score >= 35:
        label = "Risky"
    else:
        label = "Avoid"

    return SetupScoreResult(
        symbol=symbol,
        score=final_score,
        label=label,
        contributions=contributions,
        deductions=deductions,
        notes=tuple(notes),
    )


def rank_universe(
    metrics_map: dict[str, Any],
    min_score: float = 0.0,
) -> list[SetupScoreResult]:
    """
    Score and rank all symbols in the metrics_map.

    Args:
        metrics_map: Full scanner output (symbol → metrics dict or None).
        min_score:   Minimum score to include in results (default 0).

    Returns:
        List of SetupScoreResult sorted descending by score.
        Symbols with None metrics are excluded.
    """
    results: list[SetupScoreResult] = []

    for symbol, metrics in metrics_map.items():
        if not metrics:
            continue
        result = calculate_setup_score(symbol, metrics)
        if result.score >= min_score:
            results.append(result)

    return sorted(results, key=lambda r: r.score, reverse=True)
