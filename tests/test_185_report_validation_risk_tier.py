from __future__ import annotations

from src.reporting.report_quality import validate_report_quality


BASE_MARKET_REPORT = """# Institutional Trading Engine — POSTMARKET REPORT

Generated: 2026-06-11 21:00 UTC

## Market Regime

- Data Status: LIVE
- Regime: bullish
- Market Health Score: 82

### Core Market Metrics

#### SPY
- Close: 620
- SMA50: 610 ✅
- SMA200: 580 ✅
- ATR14: 5.1

#### QQQ
- Close: 540
- SMA50: 530 ✅
- SMA200: 500 ✅
- ATR14: 6.1

#### VIX
- Close: 16
- SMA50: 18 ❌
- SMA200: 19 ❌
- ATR14: 1.2

### Market Breadth
- Universe Size: 120
- Above SMA50: 88
- Breadth %: 73%

### Focus Areas
- Monitor institutional risk conditions and trend quality.

## Run Health / Silent-Failure Gate

- Run Health: OK
- Success Status: SUCCESS
- Signal Generation: PASSED
- Scanner Data Quality: PASSED
- Reasons: actionable_signals_generated

## Decision Engine

- Market State: low_vol_bull
- Portfolio Heat Limit: 1.0
- Approved / Reduced Size: 1
- Blocked / No Trade: 1

### Active Strategy Types
- momentum_breakout
- pullback_continuation

### Decision Summary
- Decision context allows selective risk-taking in regime-aligned setups.

### Ranked Opportunities

{ranked_opportunities}

## Post-Market Review

### Watchlist
- MSFT
- QQQ

### Objectives
- Preserve capital first.
- Monitor Relative Strength before risk expansion.
- Track Trade Summary and Hard Overrides.

### Warnings
- No live trading authorization.

### Notes
- Research and paper-observation only.
- Regime Alignment, No-Trade and Risk Tier validation remain evidence-gated.
"""


def _report(ranked_opportunities: str) -> str:
    return BASE_MARKET_REPORT.format(ranked_opportunities=ranked_opportunities)


def test_185_accepts_structured_decision_risk_tier_rows() -> None:
    report = _report(
        """#### MSFT
- Decision: **approved** | Risk Tier: tier_1
- Setup Score: 84 | Regime Alignment: 0.81 | Asymmetry Score: 0.72 | Data Confidence: 0.85

### 🚫 Blocked / No Trade

- **QQQ**: no_trade — insufficient_quality_threshold | Asymmetry Score: 0.62
"""
    )

    result = validate_report_quality(report, "postmarket")

    assert result.passed is True
    assert result.risk_tier_evidence["issue"] == "#185"
    assert result.risk_tier_evidence["status"] == "PASS"
    assert result.risk_tier_evidence["decision_risk_tier_rows"] == [
        {"decision": "approved", "risk_tier": "tier_1"}
    ]


def test_185_blocks_prose_only_risk_tier_mentions_without_machine_readable_row() -> None:
    report = _report(
        """#### MSFT
- Decision context says this candidate has a Risk Tier somewhere in prose.
- Setup Score: 84 | Regime Alignment: 0.81 | Asymmetry Score: 0.72 | Data Confidence: 0.85
"""
    )

    result = validate_report_quality(report, "postmarket")

    assert result.passed is False
    assert result.risk_tier_evidence["status"] == "BLOCKED"
    assert "Risk Tier evidence is present only as prose; expected machine-readable decision/risk-tier rows." in result.errors


def test_185_accepts_explicit_no_active_risk_report_without_ranked_risk_tier_row() -> None:
    report = _report(
        """- No ranked opportunities qualified for active risk. Decision remains No-Trade / watch mode until setup quality improves.
- Asymmetry Score: n/a — no approved asymmetric setup available.
"""
    )

    result = validate_report_quality(report, "postmarket")

    assert result.passed is True
    assert result.risk_tier_evidence["status"] == "PASS_NO_ACTIVE_RISK"
    assert result.risk_tier_evidence["decision_risk_tier_row_count"] == 0
    assert result.risk_tier_evidence["explicit_no_active_risk"] is True


def test_185_blocks_actionable_decision_with_no_trade_risk_tier() -> None:
    report = _report(
        """#### MSFT
- Decision: **approved** | Risk Tier: no_trade
- Setup Score: 84 | Regime Alignment: 0.81 | Asymmetry Score: 0.72 | Data Confidence: 0.85
"""
    )

    result = validate_report_quality(report, "postmarket")

    assert result.passed is False
    assert "Actionable decision `approved` cannot carry `no_trade` risk tier." in result.errors


def test_185_blocks_invalid_risk_tier_values() -> None:
    report = _report(
        """#### MSFT
- Decision: **watch** | Risk Tier: maybe_later
- Setup Score: 74 | Regime Alignment: 0.71 | Asymmetry Score: 0.67 | Data Confidence: 0.80
"""
    )

    result = validate_report_quality(report, "postmarket")

    assert result.passed is False
    assert "Invalid risk tier values: ['maybe_later']" in result.errors
