"""Scanner-to-signal metrics pipeline helpers.

Signal quality engines require numeric `close` and `atr14` values. This module
normalizes scanner output before it is passed into signal generation and creates
visible diagnostics for missing required data.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any


REQUIRED_SIGNAL_METRICS = ("close", "atr14")
OPTIONAL_SIGNAL_METRICS = (
    "atr_pct",
    "entry",
    "entry_type",
    "stop_loss",
    "exit_1",
    "exit_2",
    "high",
    "low",
    "volume",
    "rvol",
    "vwap",
)


@dataclass(frozen=True)
class ScannerMetricsDiagnostics:
    total_symbols: int
    valid_symbols: int
    missing_symbols: list[str] = field(default_factory=list)
    missing_required_fields: dict[str, list[str]] = field(default_factory=dict)

    @property
    def has_warnings(self) -> bool:
        return bool(self.missing_symbols or self.missing_required_fields)

    def warning_lines(self) -> list[str]:
        lines: list[str] = []
        for symbol in self.missing_symbols:
            lines.append(f"scanner_metrics_missing:{symbol}")
        for symbol, fields in self.missing_required_fields.items():
            lines.append(f"scanner_metrics_incomplete:{symbol}:{','.join(fields)}")
        return lines


def _safe_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        result = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(result) or math.isinf(result):
        return None
    return result


def normalize_symbol_metrics(metrics: dict[str, Any] | None) -> dict[str, Any] | None:
    """Normalize a raw scanner metrics row for signal generation.

    Numeric values are converted to floats where possible. Pandas `NA`, NaN and
    infinity are converted to `None`. Non-numeric labels such as `entry_type` are
    preserved.
    """
    if not metrics:
        return None

    normalized: dict[str, Any] = {}
    for key in (*REQUIRED_SIGNAL_METRICS, *OPTIONAL_SIGNAL_METRICS):
        if key not in metrics:
            continue
        if key == "entry_type":
            normalized[key] = metrics.get(key)
        else:
            normalized[key] = _safe_float(metrics.get(key))

    if "symbol" in metrics:
        normalized["symbol"] = metrics.get("symbol")
    if "warnings" in metrics:
        normalized["warnings"] = metrics.get("warnings") or []

    return normalized


def normalize_scanner_metrics_map(
    scanner_metrics_map: dict[str, Any] | None,
    expected_symbols: list[str],
) -> tuple[dict[str, dict[str, Any]], ScannerMetricsDiagnostics]:
    """Normalize scanner metrics map and return diagnostics.

    Missing or incomplete metrics are not fatal. They are made visible through
    diagnostics so report generation can continue without silently hiding the
    operational issue.
    """
    source = scanner_metrics_map or {}
    normalized: dict[str, dict[str, Any]] = {}
    missing_symbols: list[str] = []
    missing_required_fields: dict[str, list[str]] = {}

    for symbol in expected_symbols:
        row = normalize_symbol_metrics(source.get(symbol))
        if row is None:
            missing_symbols.append(symbol)
            continue

        missing_fields = [
            field for field in REQUIRED_SIGNAL_METRICS
            if row.get(field) is None
        ]
        if missing_fields:
            missing_required_fields[symbol] = missing_fields

        normalized[symbol] = row

    valid_symbols = sum(
        1 for symbol in expected_symbols
        if symbol in normalized and symbol not in missing_required_fields
    )

    diagnostics = ScannerMetricsDiagnostics(
        total_symbols=len(expected_symbols),
        valid_symbols=valid_symbols,
        missing_symbols=missing_symbols,
        missing_required_fields=missing_required_fields,
    )
    return normalized, diagnostics
