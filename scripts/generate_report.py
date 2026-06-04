#!/usr/bin/env python3
"""Generate Institutional Trading Engine reports + signals."""

from __future__ import annotations

import argparse
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


class ReportDataQualityBlockedError(RuntimeError):
    """Raised when scanner data quality is too poor for a green report run."""


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

    _enforce_scanner_data_quality(scanner_diagnostics)

    try:
        from src.signals.signal_generator import build_signals
        signals = build_signals(
            decision_report=decision_report,
            scanner_metrics_map=scanner_metrics_map,
            market_regime=decision_payload["market_regime"],
        )
        _merge_signal_levels_into_decisions(decision_report, signals)
        decision_payload["signals"] = signals
    except Exception as exc:
        print(f"WARNING: Signal level preparation failed (non-fatal): {type(exc).__name__}: {exc}")
        decision_payload["signals"] = []

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
        print(f"Signals written: {json_path}, {md_path}")
        print(f"  {sum(1 for signal in signals if signal.action == 'BUY_WATCH')} actionable, {sum(1 for signal in signals if signal.action != 'BUY_WATCH')} no-trade")
    except ReportDataQualityBlockedError:
        raise
    except Exception as exc:
        print(f"WARNING: Signal generation failed (non-fatal): {type(exc).__name__}: {exc}")


def main() -> int:
    args = parse_args()
    try:
        report, decision_payload = build_report(args.type)
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


if __name__ == "__main__":
    raise SystemExit(main())
