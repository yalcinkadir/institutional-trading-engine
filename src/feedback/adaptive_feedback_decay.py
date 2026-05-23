from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timezone
from typing import Any, Iterable

DECAY_FACTOR = 0.5
DECAY_HALF_LIFE_STABLE = 30
DECAY_HALF_LIFE_REGIME_SHIFT = 10
REGIME_SHIFT_RECOVERY_DAYS = 5
MIN_WEIGHT_FLOOR = 0.05


@dataclass(frozen=True)
class FeedbackDecayConfig:
    decay_factor: float = DECAY_FACTOR
    stable_half_life_days: int = DECAY_HALF_LIFE_STABLE
    regime_shift_half_life_days: int = DECAY_HALF_LIFE_REGIME_SHIFT
    regime_shift_recovery_days: int = REGIME_SHIFT_RECOVERY_DAYS
    min_weight_floor: float = MIN_WEIGHT_FLOOR


@dataclass(frozen=True)
class WeightedFeedbackRecord:
    record: dict[str, Any]
    age_in_days: float
    weight: float
    half_life_days: int
    regime_shift_active: bool


@dataclass(frozen=True)
class WeightedPerformance:
    weighted_sum: float
    total_weight: float
    adjusted_performance: float
    record_count: int


def calculate_decay_weight(
    age_in_days: float,
    *,
    half_life_days: int = DECAY_HALF_LIFE_STABLE,
    decay_factor: float = DECAY_FACTOR,
    min_weight_floor: float = MIN_WEIGHT_FLOOR,
) -> float:
    if half_life_days <= 0:
        raise ValueError("half_life_days must be greater than 0")
    if not 0 < decay_factor <= 1:
        raise ValueError("decay_factor must be in the interval (0, 1]")
    if not 0 <= min_weight_floor <= 1:
        raise ValueError("min_weight_floor must be in the interval [0, 1]")

    age = max(0.0, float(age_in_days))
    raw_weight = decay_factor ** (age / half_life_days)
    return max(min_weight_floor, raw_weight)


def half_life_for_regime_state(
    *,
    regime_shift_active: bool = False,
    days_since_regime_shift: int | None = None,
    config: FeedbackDecayConfig = FeedbackDecayConfig(),
) -> int:
    if not regime_shift_active:
        return config.stable_half_life_days

    if days_since_regime_shift is None:
        return config.regime_shift_half_life_days

    if days_since_regime_shift < config.regime_shift_recovery_days:
        return config.regime_shift_half_life_days

    return config.stable_half_life_days


def apply_feedback_decay(
    records: Iterable[dict[str, Any]],
    *,
    as_of: date | datetime | str | None = None,
    timestamp_field: str = "closed_at",
    regime_shift_active: bool = False,
    days_since_regime_shift: int | None = None,
    config: FeedbackDecayConfig = FeedbackDecayConfig(),
) -> list[WeightedFeedbackRecord]:
    reference_date = _parse_date(as_of) or datetime.now(timezone.utc).date()
    half_life_days = half_life_for_regime_state(
        regime_shift_active=regime_shift_active,
        days_since_regime_shift=days_since_regime_shift,
        config=config,
    )

    weighted_records: list[WeightedFeedbackRecord] = []
    for record in records:
        if not isinstance(record, dict):
            continue
        record_date = _parse_date(record.get(timestamp_field)) or reference_date
        age_in_days = max(0.0, float((reference_date - record_date).days))
        weight = calculate_decay_weight(
            age_in_days,
            half_life_days=half_life_days,
            decay_factor=config.decay_factor,
            min_weight_floor=config.min_weight_floor,
        )
        weighted_records.append(
            WeightedFeedbackRecord(
                record=dict(record),
                age_in_days=age_in_days,
                weight=round(weight, 6),
                half_life_days=half_life_days,
                regime_shift_active=regime_shift_active,
            )
        )

    return weighted_records


def calculate_weighted_performance(
    records: Iterable[dict[str, Any]],
    *,
    result_field: str = "result_r",
    as_of: date | datetime | str | None = None,
    timestamp_field: str = "closed_at",
    regime_shift_active: bool = False,
    days_since_regime_shift: int | None = None,
    config: FeedbackDecayConfig = FeedbackDecayConfig(),
) -> WeightedPerformance:
    weighted_records = apply_feedback_decay(
        records,
        as_of=as_of,
        timestamp_field=timestamp_field,
        regime_shift_active=regime_shift_active,
        days_since_regime_shift=days_since_regime_shift,
        config=config,
    )

    weighted_sum = 0.0
    total_weight = 0.0
    for item in weighted_records:
        result = _safe_float(item.record.get(result_field))
        if result is None:
            continue
        weighted_sum += result * item.weight
        total_weight += item.weight

    adjusted_performance = weighted_sum / total_weight if total_weight > 0 else 0.0
    return WeightedPerformance(
        weighted_sum=round(weighted_sum, 6),
        total_weight=round(total_weight, 6),
        adjusted_performance=round(adjusted_performance, 6),
        record_count=len(weighted_records),
    )


def _parse_date(value: Any) -> date | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        if value.tzinfo is None:
            return value.date()
        return value.astimezone(timezone.utc).date()
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return None
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"
        try:
            return datetime.fromisoformat(text).date()
        except ValueError:
            try:
                return date.fromisoformat(text[:10])
            except ValueError:
                return None
    return None


def _safe_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None
