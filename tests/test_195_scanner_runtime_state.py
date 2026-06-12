from __future__ import annotations

import os

import pytest

import src.scanner as scanner


def test_195_api_key_is_read_from_runtime_context_not_import_time(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("POLYGON_API_KEY", raising=False)
    context_without_key = scanner.MarketDataRunContext.from_env(run_id="run-without-key")
    assert context_without_key.api_key is None

    monkeypatch.setenv("POLYGON_API_KEY", "runtime-key-after-import")
    context_with_key = scanner.MarketDataRunContext.from_env(run_id="run-with-key")
    assert context_with_key.api_key == "runtime-key-after-import"

    # Backwards-compatible module attribute may exist, but runtime context must not
    # be frozen to its import-time value.
    assert getattr(scanner, "API_KEY", None) != context_with_key.api_key or scanner.API_KEY is None


def test_195_failure_context_is_isolated_between_runs() -> None:
    run_one = scanner.MarketDataRunContext(run_id="run-1", api_key=None)
    run_two = scanner.MarketDataRunContext(run_id="run-2", api_key=None)

    scanner.get_daily_bars("AAPL", retries=1, context=run_one)

    assert run_one.get_failure("AAPL") is not None
    assert run_one.get_failure("AAPL").run_id == "run-1"
    assert run_two.get_failure("AAPL") is None

    scanner.get_daily_bars("MSFT", retries=1, context=run_two)

    assert run_two.get_failure("MSFT") is not None
    assert run_two.get_failure("MSFT").run_id == "run-2"
    assert run_one.get_failure("MSFT") is None


def test_195_failure_stub_uses_explicit_context_not_global_leakage() -> None:
    run_one = scanner.MarketDataRunContext(run_id="run-1", api_key=None)
    run_two = scanner.MarketDataRunContext(run_id="run-2", api_key=None)

    scanner.get_daily_bars("AAPL", retries=1, context=run_one)

    leaked_stub = scanner._failure_stub_metrics("AAPL", context=run_two)

    assert leaked_stub["data_failure_kind"] == scanner.MarketDataFailureKind.EMPTY_BARS.value
    assert leaked_stub["data_failure_message"] == "scanner returned no bars without a provider-level failure detail"
    assert leaked_stub["run_id"] == "run-2"


def test_195_context_can_export_structured_failure_evidence() -> None:
    context = scanner.MarketDataRunContext(run_id="scheduled-2026-06-12", api_key=None)

    scanner.get_daily_bars("AAPL", retries=1, context=context)
    evidence = context.failure_evidence()

    assert evidence["run_id"] == "scheduled-2026-06-12"
    assert evidence["failure_count"] == 1
    assert evidence["failures"][0]["symbol"] == "AAPL"
    assert evidence["failures"][0]["kind"] == "MISSING_API_KEY"
    assert evidence["failures"][0]["run_id"] == "scheduled-2026-06-12"
    assert "recorded_at" in evidence["failures"][0]
