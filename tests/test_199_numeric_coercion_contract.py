from __future__ import annotations

from decimal import Decimal

from src.validation.historical_edge_validation import (
    NumericCoercionResult,
    coerce_finite_float,
    coerce_finite_float_or_default,
    extract_r_values,
)
from src.scoring.setup_score_engine import calculate_setup_score
from src.signals.scanner_metrics_pipeline import normalize_scanner_metrics_map


def test_199_coerce_finite_float_contract() -> None:
    assert coerce_finite_float(None) is None
    assert coerce_finite_float("") is None
    assert coerce_finite_float("   ") is None
    assert coerce_finite_float("12.5") == 12.5
    assert coerce_finite_float(Decimal("3.25")) == 3.25
    assert coerce_finite_float("bad") is None
    assert coerce_finite_float(float("nan")) is None
    assert coerce_finite_float(float("inf")) is None
    assert coerce_finite_float(float("-inf")) is None


def test_199_coerce_finite_float_strict_contract() -> None:
    result = coerce_finite_float("bad", strict=True)

    assert isinstance(result, NumericCoercionResult)
    assert result.ok is False
    assert result.value is None
    assert result.reason == "invalid_float"
    assert result.raw_value == "bad"

    valid = coerce_finite_float("7.5", strict=True)
    assert valid.ok is True
    assert valid.value == 7.5
    assert valid.reason is None


def test_199_default_coercion_uses_same_non_finite_rules() -> None:
    assert coerce_finite_float_or_default(None, 10.0) == 10.0
    assert coerce_finite_float_or_default("", 10.0) == 10.0
    assert coerce_finite_float_or_default("bad", 10.0) == 10.0
    assert coerce_finite_float_or_default(float("nan"), 10.0) == 10.0
    assert coerce_finite_float_or_default(float("inf"), 10.0) == 10.0
    assert coerce_finite_float_or_default("12.5", 10.0) == 12.5


def test_199_historical_edge_extraction_rejects_non_finite_values() -> None:
    records = [
        {"result_r": "1.25"},
        {"result_r": float("nan")},
        {"result_r": float("inf")},
        {"result_r": "bad"},
        {"r_multiple": "-0.5"},
    ]

    assert extract_r_values(records) == [1.25, -0.5]


def test_199_scanner_metrics_pipeline_rejects_non_finite_required_metrics() -> None:
    normalized, diagnostics = normalize_scanner_metrics_map(
        {
            "AAPL": {
                "close": float("nan"),
                "atr14": "2.5",
                "source": "polygon",
                "source_timestamp": "2026-06-12T12:00:00+00:00",
                "fallback_level": "primary",
                "data_status": "OK",
            }
        },
        ["AAPL"],
        now_utc=None,
    )

    assert normalized["AAPL"]["close"] is None
    assert diagnostics.data_quality_status == "BLOCKED"
    assert diagnostics.missing_required_fields["AAPL"] == ["close"]


def test_199_setup_score_uses_canonical_default_coercion() -> None:
    result = calculate_setup_score(
        "AAPL",
        {
            "trend": "Strong Uptrend",
            "rs_spread": float("nan"),
            "rs_label": "Leader",
            "rsi14": float("inf"),
            "rvol": "bad",
            "atr_pct": "2.0",
            "risk_reward": "2.5",
            "warnings": [],
        },
    )

    assert 0.0 <= result.score <= 100.0
    assert result.contributions["relative_strength"] >= 0.0
    assert result.contributions["momentum_quality"] >= 0.0
    assert result.contributions["volume_confirmation"] >= 0.0
