from __future__ import annotations

from datetime import UTC, datetime
from types import SimpleNamespace
import importlib

import pytest


def _decision_report() -> dict:
    return {
        "decisions": [
            {
                "symbol": "AAPL",
                "decision": "approved",
                "setup_type": "breakout",
                "risk_tier": "A",
                "position_size_multiplier": 1.0,
                "setup_score": 82.0,
                "regime_alignment": 1.0,
            }
        ]
    }


def _fresh_source_timestamp() -> str:
    return datetime.now(UTC).isoformat()


def _patch_market_report_builders(monkeypatch, generate_report) -> None:
    monkeypatch.setattr(
        generate_report,
        "build_market_regime_summary",
        lambda report_type: {"regime": "Bullish"},
    )
    monkeypatch.setattr(generate_report, "build_screener_snapshot", lambda report_type: {})
    monkeypatch.setattr(generate_report, "build_cross_asset_report", lambda: {})
    monkeypatch.setattr(
        generate_report,
        "build_decision_report",
        lambda *, market_regime, screener: _decision_report(),
    )


def test_market_payload_passes_non_empty_scanner_metrics_to_signal_generation(monkeypatch) -> None:
    generate_report = importlib.import_module("scripts.generate_report")
    signal_generator = importlib.import_module("src.signals.signal_generator")

    _patch_market_report_builders(monkeypatch, generate_report)
    monkeypatch.setattr(
        generate_report,
        "_merge_signal_levels_into_decisions",
        lambda decision_report, signals: None,
    )

    loaded_metrics = {
        "AAPL": {
            "close": 123.45,
            "atr14": 2.5,
            "atr_pct": 2.02,
            "source": "polygon",
            "source_timestamp": _fresh_source_timestamp(),
            "fallback_level": "primary",
            "data_status": "OK",
        }
    }
    monkeypatch.setattr(generate_report, "_load_scanner_metrics", lambda decision_report: loaded_metrics)

    captured: dict[str, object] = {}

    def fake_build_signals(*, decision_report, scanner_metrics_map, market_regime):
        captured["scanner_metrics_map"] = scanner_metrics_map
        captured["market_regime"] = market_regime
        return [SimpleNamespace(symbol="AAPL", action="BUY_WATCH", fallback_level="primary")]

    monkeypatch.setattr(signal_generator, "build_signals", fake_build_signals)

    _, decision_payload = generate_report._build_market_payload("premarket")

    scanner_metrics_map = captured["scanner_metrics_map"]
    assert isinstance(scanner_metrics_map, dict)
    assert scanner_metrics_map["AAPL"]["close"] == 123.45
    assert scanner_metrics_map["AAPL"]["atr14"] == 2.5
    assert scanner_metrics_map["AAPL"]["source"] == "polygon"
    assert captured["market_regime"] == "Bullish"
    assert decision_payload["scanner_data_quality"]["data_quality_status"] == "OK"
    assert decision_payload["signals"][0].action == "BUY_WATCH"


def test_market_payload_blocks_when_scanner_metrics_loader_returns_none(monkeypatch) -> None:
    generate_report = importlib.import_module("scripts.generate_report")

    _patch_market_report_builders(monkeypatch, generate_report)
    monkeypatch.setattr(generate_report, "_load_scanner_metrics", lambda decision_report: None)

    with pytest.raises(generate_report.ReportDataQualityBlockedError) as exc:
        generate_report._build_market_payload("premarket")

    assert "Scanner data quality status BLOCKED blocks report generation" in str(exc.value)
    assert "scanner_metrics_missing:AAPL" in str(exc.value)


def test_market_payload_blocks_all_close_null_scanner_metrics(monkeypatch) -> None:
    generate_report = importlib.import_module("scripts.generate_report")

    _patch_market_report_builders(monkeypatch, generate_report)
    monkeypatch.setattr(
        generate_report,
        "_load_scanner_metrics",
        lambda decision_report: {
            "AAPL": {
                "close": None,
                "atr14": 2.5,
                "source": "polygon",
                "source_timestamp": _fresh_source_timestamp(),
                "fallback_level": "primary",
                "data_status": "OK",
            }
        },
    )

    with pytest.raises(generate_report.ReportDataQualityBlockedError) as exc:
        generate_report._build_market_payload("premarket")

    assert "scanner_metrics_incomplete:AAPL:close" in str(exc.value)


def test_build_signals_fails_closed_for_actionable_decisions_without_scanner_metrics() -> None:
    signal_generator = importlib.import_module("src.signals.signal_generator")

    with pytest.raises(ValueError, match="scanner_metrics_map is required"):
        signal_generator.build_signals(
            decision_report=_decision_report(),
            scanner_metrics_map=None,
            market_regime="Bullish",
        )


def test_generate_signals_fallback_cannot_silently_rebuild_actionable_signals_without_metrics(
    monkeypatch,
    tmp_path,
) -> None:
    generate_report = importlib.import_module("scripts.generate_report")
    signal_generator = importlib.import_module("src.signals.signal_generator")

    monkeypatch.setattr(signal_generator, "SIGNALS_DIR", tmp_path)

    decision_payload = {
        "decision_report": _decision_report(),
        "market_regime": "Bullish",
        "scanner_data_quality": {
            "data_quality_status": "UNKNOWN",
            "total_symbols": 1,
            "valid_symbols": 0,
        },
    }

    with pytest.raises(generate_report.SignalGenerationFailedError) as exc:
        generate_report.generate_signals(decision_payload)

    assert "scanner_metrics_map is required" in str(exc.value)
    assert exc.value.evidence["status"] == generate_report.SIGNAL_GENERATION_STATUS_FAILED
