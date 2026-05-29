"""GOV7-GOV10 pre-live hygiene validators.

These helpers are intentionally small and deterministic. They protect the
Paper Observation phase from subtle governance drift before additional
strategy complexity is added.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal, ROUND_HALF_UP
from typing import Any, Iterable, Mapping


GOV7_GOV10_VALIDATION_VERSION = "gov7-gov10-2026.05.29-v1"

VIX_INVERSION_DIRECT = "DIRECT"
VIX_INVERSION_PARTIAL = "PARTIAL"
VIX_INVERSION_NONE = "NONE"
VIX_INVERSION_UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class AdaptiveWeightingResult:
    weights: dict[str, float]
    sum_after_rounding: float
    adjusted_key: str | None
    issues: list[str] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return not self.issues and round(self.sum_after_rounding, 8) == 1.0


@dataclass(frozen=True)
class VixTermStructureResult:
    mode: str
    is_inverted: bool
    severity: str
    message: str
    issues: list[str] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return not self.issues


@dataclass(frozen=True)
class DuplicateModuleMarker:
    module_path: str
    status: str
    owner_module: str
    replacement_module: str | None
    rationale: str


@dataclass(frozen=True)
class DuplicateModuleRegistryResult:
    markers: list[DuplicateModuleMarker]
    issues: list[str] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return not self.issues


@dataclass(frozen=True)
class CumulativeDriftResult:
    max_abs_daily_drift: float
    cumulative_abs_drift: float
    threshold: float
    breached: bool
    message: str
    observations: int



def normalize_public_weights_exact(
    weights: Mapping[str, float],
    *,
    decimals: int = 4,
) -> AdaptiveWeightingResult:
    """Normalize and round public/demo weights so the published sum is exactly 1.0."""

    if not weights:
        return AdaptiveWeightingResult(weights={}, sum_after_rounding=0.0, adjusted_key=None, issues=["missing_weights"])
    if decimals < 0:
        return AdaptiveWeightingResult(weights={}, sum_after_rounding=0.0, adjusted_key=None, issues=["invalid_decimals"])

    decimal_weights: dict[str, Decimal] = {}
    issues: list[str] = []
    for key, value in weights.items():
        try:
            decimal_value = Decimal(str(value))
        except Exception:  # pragma: no cover - defensive conversion guard
            issues.append(f"invalid_weight:{key}")
            continue
        if decimal_value < 0:
            issues.append(f"negative_weight:{key}")
        decimal_weights[str(key)] = decimal_value

    total = sum(decimal_weights.values(), Decimal("0"))
    if total <= 0:
        issues.append("non_positive_weight_sum")
    if issues:
        return AdaptiveWeightingResult(weights={}, sum_after_rounding=0.0, adjusted_key=None, issues=issues)

    quant = Decimal("1").scaleb(-decimals)
    normalized = {
        key: (value / total).quantize(quant, rounding=ROUND_HALF_UP)
        for key, value in decimal_weights.items()
    }
    rounded_sum = sum(normalized.values(), Decimal("0"))
    diff = Decimal("1") - rounded_sum

    adjusted_key = max(normalized.keys(), key=lambda item: normalized[item])
    normalized[adjusted_key] = (normalized[adjusted_key] + diff).quantize(quant, rounding=ROUND_HALF_UP)

    final_sum = sum(normalized.values(), Decimal("0"))
    result = {key: float(value) for key, value in normalized.items()}
    return AdaptiveWeightingResult(
        weights=result,
        sum_after_rounding=float(final_sum),
        adjusted_key=adjusted_key,
        issues=[] if final_sum == Decimal("1") else ["rounded_weight_sum_not_one"],
    )


def classify_vix_term_structure(
    *,
    front_month_vix: float | None,
    second_month_vix: float | None,
    direct_inversion_threshold: float = 0.0,
    partial_inversion_threshold: float = -0.5,
) -> VixTermStructureResult:
    """Classify VIX term-structure inversion with explicit mode semantics."""

    if front_month_vix is None or second_month_vix is None:
        return VixTermStructureResult(
            mode=VIX_INVERSION_UNKNOWN,
            is_inverted=False,
            severity="UNKNOWN",
            message="VIX term structure unavailable; inversion mode cannot be classified.",
            issues=["missing_vix_term_structure"],
        )

    spread = float(second_month_vix) - float(front_month_vix)
    if spread < direct_inversion_threshold:
        return VixTermStructureResult(
            mode=VIX_INVERSION_DIRECT,
            is_inverted=True,
            severity="HIGH",
            message="Direct inversion: front-month VIX is above second-month VIX.",
        )
    if spread <= abs(partial_inversion_threshold):
        return VixTermStructureResult(
            mode=VIX_INVERSION_PARTIAL,
            is_inverted=False,
            severity="MEDIUM",
            message="Partial compression: VIX curve is close to inversion but not directly inverted.",
        )
    return VixTermStructureResult(
        mode=VIX_INVERSION_NONE,
        is_inverted=False,
        severity="LOW",
        message="No VIX term-structure inversion detected.",
    )


def validate_duplicate_module_markers(markers: Iterable[DuplicateModuleMarker]) -> DuplicateModuleRegistryResult:
    """Validate that duplicate/overlapping modules have explicit ownership markers."""

    marker_list = list(markers)
    issues: list[str] = []
    if not marker_list:
        issues.append("missing_duplicate_module_markers")

    valid_statuses = {"ACTIVE", "DEPRECATED", "SHADOWED", "CONSOLIDATE"}
    for marker in marker_list:
        if marker.status not in valid_statuses:
            issues.append(f"invalid_status:{marker.module_path}")
        if not marker.owner_module:
            issues.append(f"missing_owner_module:{marker.module_path}")
        if marker.status in {"DEPRECATED", "SHADOWED", "CONSOLIDATE"} and not marker.replacement_module:
            issues.append(f"missing_replacement_module:{marker.module_path}")
        if not marker.rationale:
            issues.append(f"missing_rationale:{marker.module_path}")

    return DuplicateModuleRegistryResult(markers=marker_list, issues=issues)


def evaluate_cumulative_paper_observation_drift(
    daily_drifts: Iterable[float],
    *,
    cumulative_threshold: float,
) -> CumulativeDriftResult:
    """Detect small persistent drift that can evade max-daily-drift checks."""

    values = [float(value) for value in daily_drifts]
    max_abs_daily_drift = max((abs(value) for value in values), default=0.0)
    cumulative_abs_drift = sum(abs(value) for value in values)
    breached = cumulative_abs_drift > cumulative_threshold
    message = (
        "cumulative_drift_breach"
        if breached
        else "cumulative_drift_within_threshold"
    )
    return CumulativeDriftResult(
        max_abs_daily_drift=max_abs_daily_drift,
        cumulative_abs_drift=cumulative_abs_drift,
        threshold=float(cumulative_threshold),
        breached=breached,
        message=message,
        observations=len(values),
    )
