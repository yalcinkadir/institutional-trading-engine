from __future__ import annotations

import importlib
import sys
from types import ModuleType

import pytest


def _load_generate_report():
    return importlib.import_module("scripts.generate_report")


def test_signal_generation_failure_evidence_is_structured() -> None:
    generate_report = _load_generate_report()
    exc = RuntimeError("boom")

    evidence = generate_report._signal_generation_failure_evidence(exc)

    assert evidence == {
        "stage": "signal_generation",
        "status": "FAILED",
        "exception_type": "RuntimeError",
        "exception_message": "boom",
        "live_trading_authorized": False,
        "broker_execution_mode": "paper_only",
    }


def test_generate_signals_raises_on_signal_generator_exception(monkeypatch) -> None:
    generate_report = _load_generate_report()
    fake_module = ModuleType("src.signals.signal_generator")

    def failing_build_signals(**_: object) -> list[object]:
        raise RuntimeError("signal generator exploded")

    fake_module.build_signals = failing_build_signals  # type: ignore[attr-defined]
    fake_module.save_signals = lambda *args, **kwargs: ("signals.json", "signals.md")  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "src.signals.signal_generator", fake_module)

    decision_payload = {
        "decision_report": {"decisions": []},
        "market_regime": "Bullish",
        "signals": None,
    }

    with pytest.raises(generate_report.SignalGenerationFailedError) as exc_info:
        generate_report.generate_signals(decision_payload)

    assert "signal_generation failed" in str(exc_info.value)
    assert exc_info.value.evidence["stage"] == "signal_generation"
    assert exc_info.value.evidence["status"] == "FAILED"
    assert exc_info.value.evidence["exception_type"] == "RuntimeError"
    assert exc_info.value.evidence["exception_message"] == "signal generator exploded"
    assert exc_info.value.evidence["live_trading_authorized"] is False
    assert exc_info.value.evidence["broker_execution_mode"] == "paper_only"


def test_generate_signals_allows_valid_empty_no_trade_signals(monkeypatch) -> None:
    generate_report = _load_generate_report()
    fake_module = ModuleType("src.signals.signal_generator")
    save_calls: dict[str, object] = {}

    def build_empty_signals(**_: object) -> list[object]:
        return []

    def fake_save_signals(signals: list[object], **kwargs: object) -> tuple[str, str]:
        save_calls["signals"] = signals
        save_calls["kwargs"] = kwargs
        return "signals.json", "signals.md"

    fake_module.build_signals = build_empty_signals  # type: ignore[attr-defined]
    fake_module.save_signals = fake_save_signals  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "src.signals.signal_generator", fake_module)

    decision_payload = {
        "decision_report": {"decisions": []},
        "market_regime": "Bullish",
        "signals": None,
    }

    generate_report.generate_signals(decision_payload)

    assert save_calls["signals"] == []
    assert decision_payload["signal_generation_status"] == "PASSED"
    assert decision_payload["signal_generation_health"] == {
        "stage": "signal_generation",
        "status": "PASSED",
        "live_trading_authorized": False,
        "broker_execution_mode": "paper_only",
    }


def test_main_returns_non_green_exit_code_on_signal_generation_failure(monkeypatch, capsys) -> None:
    generate_report = _load_generate_report()

    monkeypatch.setattr(
        generate_report,
        "parse_args",
        lambda: type("Args", (), {"type": "premarket", "output": None})(),
    )
    monkeypatch.setattr(
        generate_report,
        "build_report",
        lambda report_type: ("demo report", {"decision_report": {}, "market_regime": "Bullish"}),
    )

    def failing_generate_signals(_: dict[str, object]) -> None:
        exc = RuntimeError("broken signal stage")
        evidence = generate_report._signal_generation_failure_evidence(exc)
        raise generate_report.SignalGenerationFailedError(
            "signal_generation failed: RuntimeError: broken signal stage",
            evidence=evidence,
        )

    monkeypatch.setattr(generate_report, "generate_signals", failing_generate_signals)

    assert generate_report.main() == 3
    captured = capsys.readouterr()
    assert "signal_generation failed" in captured.err
    assert '"status": "FAILED"' in captured.err
    assert '"exception_type": "RuntimeError"' in captured.err
