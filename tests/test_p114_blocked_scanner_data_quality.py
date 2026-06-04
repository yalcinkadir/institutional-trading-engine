from __future__ import annotations

import pytest


class _BlockedDiagnostics:
    has_warnings = True
    data_quality_status = "BLOCKED"

    def warning_lines(self) -> list[str]:
        return ["scanner_metrics_missing:NVDA"]

    def as_summary(self) -> dict:
        return {
            "data_quality_status": "BLOCKED",
            "total_symbols": 1,
            "valid_symbols": 0,
            "missing_symbols": ["NVDA"],
            "missing_required_fields": {},
            "missing_provenance_fields": {},
            "stale_symbols": {},
        }


class _UnknownDiagnostics:
    has_warnings = True
    data_quality_status = "UNKNOWN"

    def warning_lines(self) -> list[str]:
        return ["scanner_metrics_status_unknown:NVDA"]

    def as_summary(self) -> dict:
        return {
            "data_quality_status": "UNKNOWN",
            "total_symbols": 1,
            "valid_symbols": 0,
            "missing_symbols": [],
            "missing_required_fields": {},
            "missing_provenance_fields": {},
            "stale_symbols": {},
        }


class _DegradedDiagnostics:
    has_warnings = True
    data_quality_status = "DEGRADED"

    def warning_lines(self) -> list[str]:
        return ["scanner_metrics_missing_provenance:NVDA:source_timestamp"]

    def as_summary(self) -> dict:
        return {
            "data_quality_status": "DEGRADED",
            "total_symbols": 1,
            "valid_symbols": 1,
            "missing_symbols": [],
            "missing_required_fields": {},
            "missing_provenance_fields": {"NVDA": ["source_timestamp"]},
            "stale_symbols": {},
        }


def _patch_market_report_dependencies(monkeypatch: pytest.MonkeyPatch) -> None:
    import scripts.generate_report as generate_report

    monkeypatch.setattr(
        generate_report,
        "build_market_regime_summary",
        lambda report_type: {
            "regime": "Bullish",
            "market_health_score": 78,
            "data_status": "LIVE",
            "symbols": {
                "SPY": {"close": 500.0},
                "QQQ": {"close": 420.0},
                "VIX": {"close": 16.0},
            },
            "breadth": {
                "universe_size": 100,
                "above_sma50": 68,
                "breadth_percent": 68.0,
            },
            "focus_areas": [],
            "notes": [],
            "errors": [],
        },
    )
    monkeypatch.setattr(
        generate_report,
        "build_screener_snapshot",
        lambda report_type: {"title": "P114", "watchlist": ["NVDA"], "objectives": [], "warnings": []},
    )
    monkeypatch.setattr(
        generate_report,
        "build_cross_asset_report",
        lambda: {
            "data_status": "OK",
            "regime": "risk_on",
            "risk_score": 10,
            "risk_on_score": 80,
            "risk_off_score": 20,
            "warnings": [],
            "confirmations": [],
        },
    )
    monkeypatch.setattr(
        generate_report,
        "_load_scanner_metrics",
        lambda decision_report: None,
    )


def test_p114_blocked_scanner_data_quality_fails_market_report_build(monkeypatch: pytest.MonkeyPatch) -> None:
    import scripts.generate_report as generate_report

    _patch_market_report_dependencies(monkeypatch)
    monkeypatch.setattr(
        generate_report,
        "normalize_scanner_metrics_map",
        lambda raw, symbols: ({}, _BlockedDiagnostics()),
    )

    with pytest.raises(generate_report.ReportDataQualityBlockedError) as exc_info:
        generate_report.build_report("premarket")

    assert "BLOCKED" in str(exc_info.value)
    assert "scanner_metrics_missing:NVDA" in str(exc_info.value)


def test_p114_unknown_scanner_data_quality_fails_market_report_build(monkeypatch: pytest.MonkeyPatch) -> None:
    import scripts.generate_report as generate_report

    _patch_market_report_dependencies(monkeypatch)
    monkeypatch.setattr(
        generate_report,
        "normalize_scanner_metrics_map",
        lambda raw, symbols: ({}, _UnknownDiagnostics()),
    )

    with pytest.raises(generate_report.ReportDataQualityBlockedError) as exc_info:
        generate_report.build_report("premarket")

    assert "UNKNOWN" in str(exc_info.value)


def test_p114_degraded_scanner_data_quality_allows_report_build(monkeypatch: pytest.MonkeyPatch) -> None:
    import scripts.generate_report as generate_report

    _patch_market_report_dependencies(monkeypatch)
    monkeypatch.setattr(
        generate_report,
        "normalize_scanner_metrics_map",
        lambda raw, symbols: (
            {
                "NVDA": {
                    "close": 100.0,
                    "atr14": 4.0,
                    "source": "polygon",
                    "fallback_level": "primary",
                    "data_status": "DEGRADED",
                }
            },
            _DegradedDiagnostics(),
        ),
    )

    report, decision_payload = generate_report.build_report("premarket")

    assert "Institutional Trading Engine" in report
    assert decision_payload is not None
    assert decision_payload["scanner_data_quality"]["data_quality_status"] == "DEGRADED"
