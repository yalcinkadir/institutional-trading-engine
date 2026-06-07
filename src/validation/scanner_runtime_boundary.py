from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping


STATIC_WATCHLIST = "static_watchlist"
DYNAMIC_SCANNER = "dynamic_scanner"
VALID_SELECTION_MODES = {STATIC_WATCHLIST, DYNAMIC_SCANNER}


@dataclass(frozen=True)
class ScannerRuntimeBoundaryResult:
    valid: bool
    errors: tuple[str, ...]
    warnings: tuple[str, ...]
    summary: dict[str, Any]


def _as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y"}
    return bool(value)


def _non_empty(value: Any) -> bool:
    return value is not None and str(value).strip() != ""


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
