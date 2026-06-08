from __future__ import annotations

from src.reporting.report_formatter import format_report


def test_market_data_failure_taxonomy_is_visible_in_report_health_section() -> None:
    payload = {
        "report_type": "premarket",
        "market_regime": {
            "data_status": "fallback",
            "regime": "Unknown",
            "market_health_score": "n/a",
            "symbols": {},
            "breadth": {},
            "focus_areas": [],
            "notes": [],
        },
        "cross_asset": {
            "data_status": "fallback",
            "regime": "Unknown",
            "risk_score": "n/a",
            "risk_on_score": "n/a",
            "risk_off_score": "n/a",
            "warnings": [],
            "confirmations": [],
        },
        "screener": {
            "title": "Scanner",
            "watchlist": [],
            "objectives": [],
            "warnings": [],
        },
        "decision_report": {
            "market_state": "Unknown",
            "portfolio_heat_limit": "n/a",
            "approved_count": 0,
            "blocked_count": 1,
            "summary": "Scanner data quality blocked signal generation.",
            "allowed_setups": [],
            "decisions": [
                {
                    "symbol": "SPY",
                    "decision": "blocked",
                    "risk_tier": "blocked",
                    "setup_type": "data_quality",
                    "position_size_multiplier": 0.0,
                    "setup_score": 0,
                    "regime_alignment": "blocked",
                    "data_confidence": "blocked",
                    "blocked_reasons": ["scanner_data_quality_blocked"],
                    "notes": [],
                }
            ],
            "signal_generation_status": "BLOCKED_DATA_QUALITY",
            "run_health": {
                "run_health_status": "FAILED",
                "success_status": "FAILED",
                "reasons": ["scanner_data_quality_blocked"],
            },
            "scanner_data_quality": {
                "data_quality_status": "BLOCKED",
                "total_symbols": 1,
                "valid_symbols": 0,
                "market_data_failures": {
                    "SPY": {
                        "kind": "AUTH_FORBIDDEN",
                        "message": "Polygon returned 403 Forbidden for daily bars",
                        "status_code": 403,
                    }
                },
            },
            "governance_state": {
                "governance_status": "PASSED",
                "stage": "active_report_path_governance",
                "active_path": "scripts/generate_report.py::_build_market_payload",
                "kill_switch_active": False,
                "approval_granted": True,
                "live_trading_authorized": False,
                "broker_execution_mode": "paper_only",
                "reasons": [],
            },
        },
    }

    report = format_report(payload)

    assert "## Run Health / Silent-Failure Gate" in report
    assert "- Scanner Data Quality: BLOCKED" in report
    assert "- Market Data Failures:" in report
    assert "SPY: AUTH_FORBIDDEN | status=403" in report
    assert "Polygon returned 403 Forbidden for daily bars" in report
    assert "BLOCKED_DATA_QUALITY" in report
