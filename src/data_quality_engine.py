"""
Data Quality Engine.

Institutional decision systems must evaluate whether their input data is
trustworthy enough for risk-taking.

This module detects:
- missing required data
- stale data
- incomplete bar history
- anomalous price/volume moves
- inconsistent source values
- market session issues

The output can be used to reduce confidence, block aggressive risk or require
manual review.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class DataFeedSnapshot:
    source: str
    symbol: str
    timestamp_utc: str
    close: float | None
    volume: float | None
    bars_count: int
    expected_bars_count: int
    price_change_percent: float | None = None
    volume_zscore: float | None = None


@dataclass(frozen=True)
class DataQualityAssessment:
    quality_state: str
    quality_score: int
    confidence_multiplier: float
    require_manual_review: bool
    warnings: tuple[str, ...]
    confirmations: tuple[str, ...]


def _parse_utc(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _hours_old(now_utc: str, timestamp_utc: str) -> float:
    now = _parse_utc(now_utc)
    then = _parse_utc(timestamp_utc)
    return (now - then).total_seconds() / 3600


def evaluate_data_quality(
    snapshots: list[DataFeedSnapshot],
    *,
    now_utc: str,
    max_stale_hours: float = 36,
    cross_source_price_tolerance_percent: float = 1.0,
) -> DataQualityAssessment:
    warnings: list[str] = []
    confirmations: list[str] = []
    score = 100

    if not snapshots:
        return DataQualityAssessment(
            quality_state="data_unavailable",
            quality_score=0,
            confidence_multiplier=0.0,
            require_manual_review=True,
            warnings=("no_data_snapshots",),
            confirmations=(),
        )

    for item in snapshots:
        if item.close is None or item.close <= 0:
            score -= 25
            warnings.append(f"missing_or_invalid_close:{item.symbol}:{item.source}")

        if item.volume is None or item.volume < 0:
            score -= 10
            warnings.append(f"missing_or_invalid_volume:{item.symbol}:{item.source}")

        if item.bars_count < item.expected_bars_count * 0.9:
            score -= 15
            warnings.append(f"incomplete_bar_history:{item.symbol}:{item.source}")

        age = _hours_old(now_utc, item.timestamp_utc)
        if age > max_stale_hours:
            score -= 20
            warnings.append(f"stale_data:{item.symbol}:{item.source}:{round(age, 2)}h")

        if item.price_change_percent is not None and abs(item.price_change_percent) >= 25:
            score -= 15
            warnings.append(f"price_anomaly:{item.symbol}:{item.source}")

        if item.volume_zscore is not None and abs(item.volume_zscore) >= 5:
            score -= 10
            warnings.append(f"volume_anomaly:{item.symbol}:{item.source}")

    by_symbol: dict[str, list[DataFeedSnapshot]] = {}
    for item in snapshots:
        by_symbol.setdefault(item.symbol, []).append(item)

    for symbol, items in by_symbol.items():
        closes = [item.close for item in items if item.close is not None and item.close > 0]
        if len(closes) >= 2:
            max_close = max(closes)
            min_close = min(closes)
            diff_percent = ((max_close / min_close) - 1) * 100 if min_close else 0
            if diff_percent > cross_source_price_tolerance_percent:
                score -= 20
                warnings.append(f"cross_source_price_mismatch:{symbol}:{round(diff_percent, 4)}")

    score = max(0, min(100, score))

    if score >= 85:
        state = "data_quality_high"
        confidence = 1.0
        review = False
        confirmations.append("data_quality_supportive")
    elif score >= 70:
        state = "data_quality_acceptable"
        confidence = 0.85
        review = False
    elif score >= 50:
        state = "data_quality_degraded"
        confidence = 0.6
        review = True
    elif score >= 30:
        state = "data_quality_poor"
        confidence = 0.35
        review = True
    else:
        state = "data_quality_blocking"
        confidence = 0.0
        review = True

    return DataQualityAssessment(
        quality_state=state,
        quality_score=score,
        confidence_multiplier=round(confidence, 4),
        require_manual_review=review,
        warnings=tuple(dict.fromkeys(warnings)),
        confirmations=tuple(dict.fromkeys(confirmations)),
    )
