#!/usr/bin/env python3
"""Generate Institutional Trading Engine reports + signals."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.report_output_boundary import write_report_text_guarded
from src.reporting.cross_asset_report import build_cross_asset_report
from src.reporting.decision_report import build_decision_report
from src.reporting.market_regime import build_market_regime_summary
from src.reporting.report_formatter import format_report
from src.reporting.screener_engine import build_screener_snapshot
from src.reporting.weekly_summary import build_weekly_summary
from src.signals.intraday_vwap import enrich_metrics_with_vwap
from src.signals.scanner_metrics_pipeline import normalize_scanner_metrics_map
from src.signals.structure_levels import latest_confirmed_swing_low_3bar

VALID_REPORT_TYPES = {"premarket", "intraday", "postmarket", "weekly"}
MARKET_REPORT_TYPES = {"premarket", "intraday", "postmarket"}
BLOCKING_SCANNER_DATA_QUALITY_STATUSES = {"BLOCKED", "UNKNOWN"}
SIGNAL_GENERATION_STATUS_PASSED = "PASSED"
SIGNAL_GENERATION_STATUS_FAILED = "FAILED"
SIGNAL_GENERATION_STATUS_BLOCKED_DATA_QUALITY = "BLOCKED_DATA_QUALITY"
RUN_HEALTH_OK = "OK"
RUN_HEALTH_NO_TRADE_VALID = "NO_TRADE_VALID"
RUN_HEALTH_DEGRADED_DATA = "DEGRADED_DATA"
RUN_HEALTH_EMPTY_INPUT = "EMPTY_INPUT"
RUN_HEALTH_FALLBACK_ACTIVE = "FALLBACK_ACTIVE"
RUN_HEALTH_FAILED = "FAILED"


class ReportDataQualityBlockedError(RuntimeError):
    """Raised when scanner data quality is too poor for a green report run."""


class SignalGenerationFailedError(RuntimeError):
    """Raised when signal generation fails and must not be treated as no-trade."""

    def __init__(self, message: str, *, evidence: dict[str, Any]) -> None:
        super().__init__(message)
        self.evidence = evidence


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a market report.")
    parser.add_argument("--type", required=True, choices=sorted(VALID_REPORT_TYPES))
    parser.add_argument("--output", default=None)
    return parser.parse_args()


def _decision_symbols(decision_report: dict) -> list[str]:
    return [
        item["symbol"]
        for item in decision_report.get("decisions", [])
        if item.get("symbol")
    ]


def _signal_generation_failure_evidence(
    exc: Exception,
    *,
    stage: str = "signal_generation",
) -> dict[str, Any]:
    return {
        "stage": stage,
        "status": SIGNAL_GENERATION_STATUS_FAILED,
        "exception_type": type(exc).__name__,
        "exception_message": str(exc),
        "live_trading_authorized": False,
        "broker_execution_mode": "paper_only",
    }


def _raise_signal_generation_failed(
    exc: Exception,
    *,
    stage: str = "signal_generation",
) -> None:
    evidence = _signal_generation_failure_evidence(exc, stage=stage)
    raise SignalGenerationFailedError(
        f"{stage} failed: {type(exc).__name__}: {exc}",
        evidence=evidence,
    ) from exc


def _signal_generation_success_evidence(stage: str = "signal_generation") -> dict[str, Any]:
    return {
        "stage": stage,
        "status": SIGNAL_GENERATION_STATUS_PASSED,
        "live_trading_authorized": False,
        "broker_execution_mode": "paper_only",
    }


def _signal_attr(signal: Any, field_name: str, default: Any = None) -> Any:
    if isinstance(signal, dict):
        return signal.get(field_name, default)
    return getattr(signal, field_name, default)


def _derive_market_run_health(decision_payload: dict[str, Any]) -> dict[str, Any]:
    """Classify a market report run so silent failures cannot look like success."""
    reasons: list[str] = []
    scanner_status = str(
        (decision_payload.get("scanner_data_quality") or {}).get("data_quality_status") or "UNKNOWN"
    ).upper()
    signal_status = str(decision_payload.get("signal_generation_status") or "UNKNOWN").upper()
    signals = list(decision_payload.get("signals") or [])

    if signal_status in {SIGNAL_GENERATION_STATUS_FAILED, SIGNAL_GENERATION_STATUS_BLOCKED_DATA_QUALITY}:
        reasons.append("signal_generation_failed")
        return {
            "run_health_status": RUN_HEALTH_FAILED,
            "success_status": "FAILED",
            "reasons": reasons,
        }

    if scanner_status in {"BLOCKED", "UNKNOWN"}:
        reasons.append(f"scanner_data_quality_{scanner_status.lower()}")
        return {
            "run_health_status": RUN_HEALTH_FAILED,
            "success_status": "FAILED",
            "reasons": reasons,
        }

    if not signals:
        reasons.append("signals_empty")
        return {
            "run_health_status": RUN_HEALTH_EMPTY_INPUT,
            "success_status": "FAILED",
            "reasons": reasons,
        }

    if scanner_status == "DEGRADED":
        reasons.append("scanner_data_quality_degraded")

    demo_or_fixture = any(
        str(_signal_attr(signal, "data_source", "")).lower() in {"demo", "fixture", "public_demo", "historical_demo"}
        or str(_signal_attr(signal, "score_source", "")).lower() in {"demo", "fixture", "public_demo", "demo_arithmetic_sequence"}
        or str(_signal_attr(signal, "thresholds_version", "")).lower() in {"demo", "fixture", "public_demo"}
        for signal in signals
    )
    if demo_or_fixture:
        reasons.append("demo_or_fixture_data_used")

    non_primary_fallback = any(
        str(_signal_attr(signal, "fallback_level", "primary")).lower() not in {"", "primary"}
        for signal in signals
    )
    if non_primary_fallback:
        reasons.append("non_primary_fallback_active")

    actionable_count = sum(1 for signal in signals if _signal_attr(signal, "action") == "BUY_WATCH")
    if reasons:
        status = RUN_HEALTH_DEGRADED_DATA if "scanner_data_quality_degraded" in reasons else RUN_HEALTH_FALLBACK_ACTIVE
        return {
            "run_health_status": status,
            "success_status": "DEGRADED",
            "reasons": sorted(set(reasons)),
        }

    if actionable_count == 0:
        return {
            "run_health_status": RUN_HEALTH_NO_TRADE_VALID,
            "success_status": "SUCCESS",
            "reasons": ["no_actionable_signals_with_complete_data"],
        }

    return {
        "run_health_status": RUN_HEALTH_OK,
        "success_status": "SUCCESS",
        "reasons": ["actionable_signals_generated"],
    }


def _is_empty_report_text(report: str) -> bool:
    lines = [line.strip() for line in report.splitlines() if line.strip()]
    if not lines:
        return True
    return len(lines) == 1 and lines[0].startswith("#")


def _enrich_metrics_with_structure(metrics: dict[str, Any] | None, bars_df: Any) -> dict[str, Any] | None:
    if metrics is None:
        return None
    enriched = dict(metrics)
    if bars_df is not None and hasattr(bars_df, "columns") and "low" in bars_df.columns:
        enriched["swing_low_3bar"] = latest_confirmed_swing_low_3bar(list(bars_df["low"]))
    return enriched


def _stamp_primary_market_data_provenance(metrics: dict[str, Any] | None) -> dict[str, Any] | None:
    if metrics is None:
        return None
    stamped = dict(metrics)
    stamped.setdefault("source", "polygon")
    stamped.setdefault("source_timestamp", datetime.now(UTC).isoformat())
    stamped.setdefault("fallback_level", "primary")
    stamped.setdefault("data_status", "OK")
    return stamped


def _load_intraday_bars(symbol: str, *, minutes: int = 5) -> list[dict[str, Any]]:
    """Load recent intraday Polygon bars when available.

    This is deliberately non-fatal. Free/limited Polygon plans may not provide
    the requested intraday aggregates.
    """
    try:
        from src.scanner import API_KEY
        import requests

        if not API_KEY:
            return []

        end_date = datetime.now(UTC).date()
        start_date = end_date - timedelta(days=5)
        url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/{minutes}/minute/{start_date}/{end_date}"
        params = {
            "adjusted": "true",
            "sort": "asc",
            "limit": 5000,
            "apiKey": API_KEY,
        }
        response = requests.get(url, params=params, timeout=30)
        if response.status_code == 429:
            print(f"WARNING: intraday VWAP rate limit for {symbol}")
            return []
        response.raise_for_status()
        payload = response.json()
        results = payload.get("results", []) if isinstance(payload, dict) else []
        return results if isinstance(results, list) else []
    except Exception as exc:
        print(f"WARNING: intraday VWAP unavailable for {symbol}: {type(exc).__name__}: {exc}")
        return []


def _enrich_metrics_with_intraday_context(
    metrics: dict[str, Any] | None,
    intraday_bars: list[dict[str, Any]] | None,
) -> dict[str, Any] | None:
    return enrich_metrics_with_vwap(metrics, intraday_bars)


def _load_scanner_metrics(decision_report: dict) -> dict[str, Any] | None:
    try:
        from src.scanner import build_symbol_metrics, calculate_20d_return, get_daily_bars
        import time

        benchmark_returns: dict[str, Any] = {}
        for bench in ["QQQ", "SPY", "GLD"]:
            df = get_daily_bars(bench)
            if df is not None and not df.empty:
                benchmark_returns[bench] = calculate_20d_return(df["close"])
            else:
                benchmark_returns[bench] = None
            time.sleep(2)

        scanner_metrics_map: dict[str, Any] = {}
        for symbol in _decision_symbols(decision_report):
            try:
                metrics = build_symbol_metrics(symbol, benchmark_returns)
                bars_df = get_daily_bars(symbol)
                metrics = _enrich_metrics_with_structure(metrics, bars_df)
                intraday_bars = _load_intraday_bars(symbol)
                metrics = _enrich_metrics_with_intraday_context(metrics, intraday_bars)
                scanner_metrics_map[symbol] = _stamp_primary_market_data_provenance(metrics)
                time.sleep(2)
            except Exception as exc:
                print(f"WARNING: scanner metric build failed for {symbol}: {type(exc).__name__}: {exc}")
                scanner_metrics_map[symbol] = None
        return scanner_metrics_map
    except Exception as exc:
        print(f"WARNING: scanner metric loading failed: {type(exc).__name__}: {exc}")
        return None


def _enforce_scanner_data_quality(scanner_diagnostics: Any) -> None:
    status = str(getattr(scanner_diagnostics, "data_quality_status", "UNKNOWN") or "UNKNOWN").upper()
    if status not in BLOCKING_SCANNER_DATA_QUALITY_STATUSES:
        return

    warning_lines = []
    if hasattr(scanner_diagnostics, "warning_lines"):
        warning_lines = [str(line) for line in scanner_diagnostics.warning_lines()]

    detail = "; ".join(warning_lines) if warning_lines else "no diagnostic detail available"
    raise ReportDataQualityBlockedError(
        f"Scanner data quality status {status} blocks report generation: {detail}"
    )


def _merge_signal_levels_into_decisions(decision_report: dict, signals: list[Any]) -> None:
    signals_by_symbol = {signal.symbol: signal for signal in signals}
    for item in decision_report.get("decisions", []):
        signal = signals_by_symbol.get(item.get("symbol"))
        if not signal:
            continue
        signal_payload = asdict(signal)
        for key in (
            "signal_id",
            "action",
            "close",
            "entry_trigger",
            "entry_type",
            "entry_reason",
            "stop_loss",
            "stop_model",
            "stop_reason",
            "target_1",
            "target_2",
            "exit_model",
            "exit_reason",
            "risk_reward",
            "atr_pct",
            "valid_until",
        ):
            item[key] = signal_payload.get(key)


def _set_signal_generation_status(
    decision_payload: dict[str, Any],
    decision_report: dict[str, Any],
    *,
    status: str,
    evidence: dict[str, Any],
) -> None:
    decision_payload["signal_generation_status"] = status
    decision_payload["signal_generation_health"] = evidence
    decision_report["signal_generation_status"] = status
    decision_report["signal_generation_health"] = evidence


def _build_market_payload(report_type: str) -> tuple[dict, dict | None]:
    market_regime = build_market_regime_summary(report_type)
    screener = build_screener_snapshot(report_type)
    cross_asset = build_cross_asset_report()
    decision_report = build_decision_report(market_regime=market_regime, screener=screener)
    decision_payload = {"decision_report": decision_report, "market_regime": market_regime.get("regime", "Unknown")}

    raw_scanner_metrics = _load_scanner_metrics(decision_report)
    scanner_metrics_map, scanner_diagnostics = normalize_scanner_metrics_map(
        raw_scanner_metrics,
        _decision_symbols(decision_report),
    )
    decision_payload["scanner_metrics_diagnostics"] = scanner_diagnostics
    decision_payload["scanner_data_quality"] = scanner_diagnostics.as_summary()
    decision_report["scanner_data_quality"] = scanner_diagnostics.as_summary()
    if scanner_diagnostics.has_warnings:
        for warning in scanner_diagnostics.warning_lines():
            print(f"WARNING: {warning}")

    try:
        _enforce_scanner_data_quality(scanner_diagnostics)
    except ReportDataQualityBlockedError:
        evidence = {
            "stage": "signal_generation",
            "status": SIGNAL_GENERATION_STATUS_BLOCKED_DATA_QUALITY,
            "live_trading_authorized": False,
            "broker_execution_mode": "paper_only",
        }
        _set_signal_generation_status(
            decision_payload,
            decision_report,
            status=SIGNAL_GENERATION_STATUS_BLOCKED_DATA_QUALITY,
            evidence=evidence,
        )
        raise

    try:
        from src.signals.signal_generator import build_signals
        signals = build_signals(
            decision_report=decision_report,
            scanner_metrics_map=scanner_metrics_map,
            market_regime=decision_payload["market_regime"],
        )
        _merge_signal_levels_into_decisions(decision_report, signals)
        decision_payload["signals"] = signals
        _set_signal_generation_status(
            decision_payload,
            decision_report,
            status=SIGNAL_GENERATION_STATUS_PASSED,
            evidence=_signal_generation_success_evidence(),
        )
        run_health = _derive_market_run_health(decision_payload)
        decision_payload["run_health"] = run_health
        decision_report["run_health"] = run_health
    except Exception as exc:
        evidence = _signal_generation_failure_evidence(exc)
        _set_signal_generation_status(
            decision_payload,
            decision_report,
            status=SIGNAL_GENERATION_STATUS_FAILED,
            evidence=evidence,
        )
        _raise_signal_generation_failed(exc)

    payload = {
        "report_type": report_type,
        "market_regime": market_regime,
        "cross_asset": cross_asset,
        "screener": screener,
        "decision_report": decision_report,
    }
    return payload, decision_payload


def build_report(report_type: str) -> tuple[str, dict | None]:
    if report_type == "weekly":
        return format_report({"report_type": report_type, "weekly_summary": build_weekly_summary()}), None
    payload, decision_payload = _build_market_payload(report_type)
    return format_report(payload), decision_payload


def persist_scoring_adjustments(report_type: str, decision_payload: dict) -> None:
    try:
        from src.scoring.adjustment_history import append_scoring_adjustments
        run_id = f"{report_type}-{datetime.now(UTC).strftime('%Y-%m-%dT%H:%M:%SZ')}"
        path = append_scoring_adjustments(decision_report=decision_payload["decision_report"], report_type=report_type, run_id=run_id)
        print(f"Scoring adjustment history updated: {path}")
    except Exception as exc:
        print(f"WARNING: Scoring adjustment history failed (non-fatal): {type(exc).__name__}: {exc}")


def generate_signals(decision_payload: dict) -> None:
    try:
        from src.signals.signal_generator import build_signals, save_signals
        signals = decision_payload.get("signals")
        if signals is None:
            diagnostics = decision_payload.get("scanner_metrics_diagnostics")
            if diagnostics is not None:
                _enforce_scanner_data_quality(diagnostics)
            signals = build_signals(
                decision_report=decision_payload["decision_report"],
                scanner_metrics_map=None,
                market_regime=decision_payload["market_regime"],
            )
        json_path, md_path = save_signals(
            signals,
            date_str=datetime.now(UTC).strftime("%Y-%m-%d"),
            data_quality=decision_payload.get("scanner_data_quality"),
        )
        decision_payload["signal_generation_status"] = SIGNAL_GENERATION_STATUS_PASSED
        decision_payload["signal_generation_health"] = _signal_generation_success_evidence()
        print(f"Signals written: {json_path}, {md_path}")
        print(f"  {sum(1 for signal in signals if signal.action == 'BUY_WATCH')} actionable, {sum(1 for signal in signals if signal.action != 'BUY_WATCH')} no-trade")
    except ReportDataQualityBlockedError:
        raise
    except SignalGenerationFailedError:
        raise
    except Exception as exc:
        _raise_signal_generation_failed(exc)


def main() -> int:
    args = parse_args()
    try:
        report, decision_payload = build_report(args.type)
        if _is_empty_report_text(report):
            print("ERROR: silent failure detected: empty report", file=sys.stderr)
            return 4
        if args.output:
            output_path = write_report_text_guarded(args.output, report, repo_root=ROOT_DIR)
            print(f"Report written to {output_path}")
        else:
            print(report)
        if args.type in MARKET_REPORT_TYPES and decision_payload is not None:
            generate_signals(decision_payload)
        return 0
    except ReportDataQualityBlockedError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    except SignalGenerationFailedError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        print(json.dumps(exc.evidence, sort_keys=True), file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
