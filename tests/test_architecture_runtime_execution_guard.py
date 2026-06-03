from __future__ import annotations

from pathlib import Path

import scripts.generate_report as generate_report


RUNTIME_ENTRYPOINT = Path("scripts/generate_report.py")

CRITICAL_RUNTIME_IMPORTS = [
    "from src.reporting.market_regime import build_market_regime_summary",
    "from src.reporting.screener_engine import build_screener_snapshot",
    "from src.reporting.decision_report import build_decision_report",
    "from src.signals.scanner_metrics_pipeline import normalize_scanner_metrics_map",
    "from src.signals.signal_generator import build_signals, save_signals",
]

CRITICAL_RUNTIME_CALLS = [
    "market_regime_called",
    "screener_called",
    "decision_report_called",
    "scanner_metrics_normalized",
    "signals_built",
    "signals_saved",
]


def test_arch106_report_signal_runtime_entrypoint_declares_critical_imports() -> None:
    source = RUNTIME_ENTRYPOINT.read_text(encoding="utf-8")

    for import_line in CRITICAL_RUNTIME_IMPORTS:
        assert import_line in source


def test_arch106_report_signal_path_has_runtime_execution_proof(monkeypatch, tmp_path) -> None:
    execution_trace: list[str] = []

    class FakeDiagnostics:
        has_warnings = False

        def warning_lines(self) -> list[str]:
            return []

        def as_summary(self) -> dict:
            return {
                "data_quality_status": "OK",
                "total_symbols": 1,
                "valid_symbols": 1,
                "missing_symbols": [],
                "missing_required_fields": {},
                "missing_provenance_fields": {},
                "stale_symbols": {},
            }

    class FakeSignal:
        symbol = "NVDA"
        action = "BUY_WATCH"
        signal_id = "sig_NVDA_arch106"
        close = 100.0
        entry_trigger = 101.0
        entry_type = "breakout"
        entry_reason = "runtime proof"
        stop_loss = 95.0
        stop_model = "atr_stop"
        stop_reason = "runtime proof"
        target_1 = 110.0
        target_2 = 120.0
        exit_model = "momentum_targets"
        exit_reason = "runtime proof"
        risk_reward = 1.8
        atr_pct = 4.0
        valid_until = "2026-06-06"

    def fake_market_regime(report_type: str) -> dict:
        execution_trace.append("market_regime_called")
        assert report_type == "premarket"
        return {"regime": "Bullish", "market_health_score": 75, "data_status": "OK"}

    def fake_screener(report_type: str) -> dict:
        execution_trace.append("screener_called")
        assert report_type == "premarket"
        return {"watchlist": ["NVDA"]}

    def fake_cross_asset() -> dict:
        return {"status": "ok"}

    def fake_decision_report(market_regime: dict, screener: dict) -> dict:
        execution_trace.append("decision_report_called")
        assert market_regime["regime"] == "Bullish"
        assert screener["watchlist"] == ["NVDA"]
        return {
            "decisions": [
                {
                    "symbol": "NVDA",
                    "decision": "approved",
                    "setup_type": "momentum_breakout",
                    "risk_tier": "tier_1",
                    "position_size_multiplier": 1.0,
                    "setup_score": 91.0,
                    "regime_alignment": 0.8,
                    "blocked_reasons": [],
                    "notes": [],
                }
            ]
        }

    def fake_load_scanner_metrics(decision_report: dict) -> dict:
        return {
            "NVDA": {
                "close": 100.0,
                "atr14": 4.0,
                "source": "polygon",
                "source_timestamp": "2026-06-03T14:30:00+00:00",
                "fallback_level": "primary",
                "data_status": "OK",
            }
        }

    def fake_normalize_scanner_metrics_map(raw_metrics: dict, symbols: list[str]):
        execution_trace.append("scanner_metrics_normalized")
        assert symbols == ["NVDA"]
        assert raw_metrics["NVDA"]["close"] == 100.0
        return raw_metrics, FakeDiagnostics()

    def fake_build_signals(decision_report: dict, scanner_metrics_map: dict, market_regime: str):
        execution_trace.append("signals_built")
        assert market_regime == "Bullish"
        assert scanner_metrics_map["NVDA"]["data_status"] == "OK"
        return [FakeSignal()]

    def fake_save_signals(signals, date_str=None, data_quality=None):
        execution_trace.append("signals_saved")
        assert signals[0].action == "BUY_WATCH"
        assert data_quality["data_quality_status"] == "OK"
        json_path = tmp_path / "signals.json"
        md_path = tmp_path / "signals.md"
        json_path.write_text("{}", encoding="utf-8")
        md_path.write_text("# signals", encoding="utf-8")
        return json_path, md_path

    monkeypatch.setattr(generate_report, "build_market_regime_summary", fake_market_regime)
    monkeypatch.setattr(generate_report, "build_screener_snapshot", fake_screener)
    monkeypatch.setattr(generate_report, "build_cross_asset_report", fake_cross_asset)
    monkeypatch.setattr(generate_report, "build_decision_report", fake_decision_report)
    monkeypatch.setattr(generate_report, "_load_scanner_metrics", fake_load_scanner_metrics)
    monkeypatch.setattr(generate_report, "normalize_scanner_metrics_map", fake_normalize_scanner_metrics_map)

    import src.signals.signal_generator as signal_generator

    monkeypatch.setattr(signal_generator, "build_signals", fake_build_signals)
    monkeypatch.setattr(signal_generator, "save_signals", fake_save_signals)

    report, decision_payload = generate_report.build_report("premarket")
    assert decision_payload is not None
    generate_report.generate_signals(decision_payload)

    for required_call in CRITICAL_RUNTIME_CALLS:
        assert required_call in execution_trace

    assert execution_trace.index("market_regime_called") < execution_trace.index("decision_report_called")
    assert execution_trace.index("scanner_metrics_normalized") < execution_trace.index("signals_built")
    assert execution_trace.index("signals_built") < execution_trace.index("signals_saved")
