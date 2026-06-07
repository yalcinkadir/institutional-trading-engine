from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping


@dataclass(frozen=True)
class FeatureConnectivityMatrixGuardResult:
    valid: bool
    errors: tuple[str, ...]
    warnings: tuple[str, ...]
    summary: dict[str, Any]


@dataclass(frozen=True)
class ScannerRuntimeBoundaryResult:
    valid: bool
    errors: tuple[str, ...]
    warnings: tuple[str, ...]
    summary: dict[str, Any]


REQUIRED_FEATURE_FIELDS = (
    "feature_id",
    "feature_name",
    "owner_phase",
    "runtime_gate",
    "guard_test",
    "evidence_artifact",
    "documentation_ref",
)

VALID_STATUSES = {"planned", "implemented", "ci_green", "retired"}

STATIC_WATCHLIST = "static_watchlist"
DYNAMIC_SCANNER = "dynamic_scanner"
VALID_SELECTION_MODES = {STATIC_WATCHLIST, DYNAMIC_SCANNER}


def _as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y"}
    return bool(value)


def _non_empty(value: Any) -> bool:
    return value is not None and str(value).strip() != ""


def _normalise_feature(feature: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "feature_id": str(feature.get("feature_id", "")).strip(),
        "feature_name": str(feature.get("feature_name", "")).strip(),
        "owner_phase": str(feature.get("owner_phase", "")).strip(),
        "status": str(feature.get("status", "planned")).strip().lower(),
        "runtime_gate": str(feature.get("runtime_gate", "")).strip(),
        "guard_test": str(feature.get("guard_test", "")).strip(),
        "evidence_artifact": str(feature.get("evidence_artifact", "")).strip(),
        "documentation_ref": str(feature.get("documentation_ref", "")).strip(),
        "upstream_dependencies": tuple(str(item).strip() for item in feature.get("upstream_dependencies", ()) if str(item).strip()),
        "downstream_consumers": tuple(str(item).strip() for item in feature.get("downstream_consumers", ()) if str(item).strip()),
        "live_trading_authorized": _as_bool(feature.get("live_trading_authorized", False)),
        "broker_execution_mode": str(feature.get("broker_execution_mode", "paper_only")).strip() or "paper_only",
    }


def validate_feature_connectivity_matrix(features: Iterable[Mapping[str, Any]]) -> FeatureConnectivityMatrixGuardResult:
    normalised = [_normalise_feature(feature) for feature in features]
    errors: list[str] = []
    warnings: list[str] = []

    if not normalised:
        errors.append("empty_feature_connectivity_matrix")

    seen: set[str] = set()
    feature_ids = {feature["feature_id"] for feature in normalised if feature["feature_id"]}

    for index, feature in enumerate(normalised, start=1):
        feature_id = feature["feature_id"] or f"row_{index}"

        for field in REQUIRED_FEATURE_FIELDS:
            if not _non_empty(feature[field]):
                errors.append(f"{feature_id}:missing_{field}")

        if feature["feature_id"] in seen:
            errors.append(f"{feature_id}:duplicate_feature_id")
        if feature["feature_id"]:
            seen.add(feature["feature_id"])

        if feature["status"] not in VALID_STATUSES:
            errors.append(f"{feature_id}:invalid_status")

        if feature["status"] in {"implemented", "ci_green"}:
            for field in ("runtime_gate", "guard_test", "evidence_artifact", "documentation_ref"):
                if not _non_empty(feature[field]):
                    errors.append(f"{feature_id}:implemented_feature_missing_{field}")

        if feature["status"] == "ci_green" and not str(feature["guard_test"]).startswith("tests/"):
            errors.append(f"{feature_id}:ci_green_feature_without_test_path")

        if feature["live_trading_authorized"] is not False:
            errors.append(f"{feature_id}:live_trading_must_remain_false")

        if feature["broker_execution_mode"] != "paper_only":
            errors.append(f"{feature_id}:broker_execution_mode_must_be_paper_only")

        missing_dependencies = [dep for dep in feature["upstream_dependencies"] if dep not in feature_ids]
        if missing_dependencies:
            errors.append(f"{feature_id}:unknown_upstream_dependencies:{','.join(missing_dependencies)}")

        if not feature["upstream_dependencies"] and feature["status"] == "ci_green":
            warnings.append(f"{feature_id}:no_upstream_dependencies_declared")

        if not feature["downstream_consumers"] and feature["status"] == "ci_green":
            warnings.append(f"{feature_id}:no_downstream_consumers_declared")

    summary = {
        "feature_connectivity_matrix_status": "PASS" if not errors else "BLOCKED",
        "feature_count": len(normalised),
        "ci_green_feature_count": sum(1 for feature in normalised if feature["status"] == "ci_green"),
        "implemented_feature_count": sum(1 for feature in normalised if feature["status"] in {"implemented", "ci_green"}),
        "live_trading_authorized": False,
        "broker_execution_mode": "paper_only",
        "features": normalised,
    }

    return FeatureConnectivityMatrixGuardResult(
        valid=not errors,
        errors=tuple(errors),
        warnings=tuple(warnings),
        summary=summary,
    )


def _normalise_symbols(symbols: Iterable[Any] | None) -> tuple[str, ...]:
    if symbols is None:
        return ()
    return tuple(str(symbol).strip().upper() for symbol in symbols if str(symbol).strip())


def build_selection_metadata(
    *,
    selection_mode: str,
    selected_symbols: Iterable[Any],
    selection_reason: str,
    scanner_contract_ref: str = "",
    live_trading_authorized: bool = False,
    broker_execution_mode: str = "paper_only",
) -> dict[str, Any]:
    mode = str(selection_mode).strip().lower()
    symbols = _normalise_symbols(selected_symbols)

    return {
        "selection_mode": mode,
        "selected_symbols": list(symbols),
        "selection_reason": str(selection_reason).strip(),
        "scanner_contract_ref": str(scanner_contract_ref).strip(),
        "live_trading_authorized": False,
        "broker_execution_mode": "paper_only",
    }


def attach_selection_metadata(
    payload: Mapping[str, Any],
    *,
    selection_mode: str,
    selected_symbols: Iterable[Any],
    selection_reason: str,
    scanner_contract_ref: str = "",
    live_trading_authorized: bool = False,
    broker_execution_mode: str = "paper_only",
) -> dict[str, Any]:
    enriched = dict(payload)
    enriched.update(
        build_selection_metadata(
            selection_mode=selection_mode,
            selected_symbols=selected_symbols,
            selection_reason=selection_reason,
            scanner_contract_ref=scanner_contract_ref,
            live_trading_authorized=live_trading_authorized,
            broker_execution_mode=broker_execution_mode,
        )
    )
    return enriched


def validate_scanner_runtime_boundary(
    payload: Mapping[str, Any],
    *,
    artifact_kind: str = "runtime_report",
) -> ScannerRuntimeBoundaryResult:
    errors: list[str] = []
    warnings: list[str] = []

    mode = str(payload.get("selection_mode", "")).strip().lower()
    symbols = _normalise_symbols(payload.get("selected_symbols"))
    reason = str(payload.get("selection_reason", "")).strip()
    scanner_contract_ref = str(payload.get("scanner_contract_ref", "")).strip()

    if mode not in VALID_SELECTION_MODES:
        errors.append(f"{artifact_kind}:missing_or_invalid_selection_mode")
    if not symbols:
        errors.append(f"{artifact_kind}:missing_selected_symbols")
    if not reason:
        errors.append(f"{artifact_kind}:missing_selection_reason")

    if mode == STATIC_WATCHLIST:
        warnings.append(f"{artifact_kind}:static_watchlist_is_research_setup_not_dynamic_scanner")
        if _as_bool(payload.get("dynamic_scanner_claimed", False)):
            errors.append(f"{artifact_kind}:static_watchlist_must_not_claim_dynamic_scanner")
        if _as_bool(payload.get("trading_edge_claimed", False)):
            errors.append(f"{artifact_kind}:static_watchlist_must_not_claim_trading_edge")

    if mode == DYNAMIC_SCANNER and not scanner_contract_ref:
        errors.append(f"{artifact_kind}:dynamic_scanner_requires_contract_ref")

    if _as_bool(payload.get("live_trading_authorized", False)) is not False:
        errors.append(f"{artifact_kind}:live_trading_must_remain_false")

    if str(payload.get("broker_execution_mode", "paper_only")).strip() != "paper_only":
        errors.append(f"{artifact_kind}:broker_execution_mode_must_be_paper_only")

    summary = {
        "scanner_runtime_boundary_status": "PASS" if not errors else "BLOCKED",
        "artifact_kind": artifact_kind,
        "selection_mode": mode,
        "selected_symbol_count": len(symbols),
        "selected_symbols": list(symbols),
        "scanner_contract_ref": scanner_contract_ref,
        "live_trading_authorized": False,
        "broker_execution_mode": "paper_only",
    }

    return ScannerRuntimeBoundaryResult(
        valid=not errors,
        errors=tuple(errors),
        warnings=tuple(warnings),
        summary=summary,
    )
