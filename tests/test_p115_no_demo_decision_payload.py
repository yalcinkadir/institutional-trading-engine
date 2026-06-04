from __future__ import annotations


def _market_regime() -> dict:
    return {
        "regime": "Bullish",
        "market_health_score": 78,
        "data_status": "LIVE",
        "symbols": {"VIX": {"close": 16.0}},
        "breadth": {
            "universe_size": 100,
            "above_sma50": 68,
            "breadth_percent": 68.0,
        },
        "focus_areas": [],
        "notes": [],
        "errors": [],
    }


def _screener() -> dict:
    return {
        "title": "P115 Production Screener",
        "watchlist": ["MSFT", "NVDA", "META", "AAPL", "MU", "QQQ", "GLD", "SLV"],
        "objectives": [],
        "warnings": [],
    }


def _score_sequence(report: dict) -> list[float]:
    return [float(item["setup_score"]) for item in report["decisions"]]


def _alignment_sequence(report: dict) -> list[float]:
    return [float(item["regime_alignment"]) for item in report["decisions"]]


def test_p115_scheduled_decision_report_rejects_known_demo_score_sequence() -> None:
    from src.reporting.decision_report import build_decision_report

    report = build_decision_report(_market_regime(), _screener())

    assert report.get("data_source") != "demo"
    assert report.get("score_source") != "demo_arithmetic_sequence"
    assert _score_sequence(report) != [82.0, 79.0, 76.0, 73.0, 70.0, 67.0, 64.0, 61.0]
    assert _alignment_sequence(report) != [0.82, 0.78, 0.74, 0.7, 0.66, 0.62, 0.58, 0.54]


def test_p115_decision_records_include_non_demo_score_provenance() -> None:
    from src.reporting.decision_report import build_decision_report

    report = build_decision_report(_market_regime(), _screener())

    assert report.get("score_source") in {"scanner_derived", "evidence_adjusted"}
    assert report.get("data_source") in {"live", "scanner_metrics"}
    for decision in report["decisions"]:
        assert decision.get("score_source") in {"scanner_derived", "evidence_adjusted"}
        assert decision.get("data_source") in {"live", "scanner_metrics"}
        assert decision.get("thresholds_version") != "public_demo"
