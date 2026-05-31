"""
Runtime Evidence Manifest Guard.

PSR2 turns the PSR1 manifest into an enforceable observation-day gate.

The guard fails closed when:
- the manifest file is missing
- the manifest JSON is invalid
- the manifest schema is invalid
- manifest status is not PASS
- required artifacts are missing
- live_trading_authorized is ever true

This module is intentionally small and deterministic.
It does not fetch market data, place orders or infer edge.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from src.operations.runtime_evidence_manifest import (
    RuntimeEvidenceManifest,
    load_runtime_evidence_manifest,
    validate_runtime_evidence_manifest,
)

DEFAULT_MANIFEST_DIR = Path("reports/evidence/manifests")


@dataclass(frozen=True)
class RuntimeEvidenceManifestGuardResult:
    """Result of one manifest guard evaluation."""

    status: str
    manifest_path: str
    trading_date: str | None
    errors: list[str]
    missing_required_artifacts: list[str]
    manifest_status: str | None
    live_trading_authorized: bool | None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @property
    def passed(self) -> bool:
        return self.status == "PASS"


def manifest_path_for_date(
    trading_date: str,
    *,
    manifest_dir: str | Path = DEFAULT_MANIFEST_DIR,
) -> Path:
    """Return expected manifest path for a trading date."""
    return Path(manifest_dir) / f"{trading_date}-runtime-evidence-manifest.json"


def evaluate_runtime_evidence_manifest_file(
    manifest_path: str | Path,
) -> RuntimeEvidenceManifestGuardResult:
    """Evaluate one runtime evidence manifest file."""
    path = Path(manifest_path)

    if not path.exists():
        return RuntimeEvidenceManifestGuardResult(
            status="FAIL",
            manifest_path=path.as_posix(),
            trading_date=None,
            errors=["manifest_missing"],
            missing_required_artifacts=[],
            manifest_status=None,
            live_trading_authorized=None,
        )

    try:
        manifest = load_runtime_evidence_manifest(path)
    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        return RuntimeEvidenceManifestGuardResult(
            status="FAIL",
            manifest_path=path.as_posix(),
            trading_date=None,
            errors=["manifest_invalid_json_or_schema", exc.__class__.__name__],
            missing_required_artifacts=[],
            manifest_status=None,
            live_trading_authorized=None,
        )

    return evaluate_runtime_evidence_manifest(manifest, manifest_path=path)


def evaluate_runtime_evidence_manifest(
    manifest: RuntimeEvidenceManifest,
    *,
    manifest_path: str | Path,
) -> RuntimeEvidenceManifestGuardResult:
    """Evaluate an already loaded runtime evidence manifest."""
    validation = validate_runtime_evidence_manifest(manifest)
    errors = list(validation.get("errors", []))

    if manifest.status != "PASS":
        errors.append("manifest_status_not_pass")

    if manifest.missing_required_artifacts:
        errors.append("required_artifacts_missing")

    if manifest.live_trading_authorized:
        errors.append("live_trading_authorized_must_be_false")

    unique_errors = list(dict.fromkeys(errors))
    status = "PASS" if not unique_errors else "FAIL"

    return RuntimeEvidenceManifestGuardResult(
        status=status,
        manifest_path=Path(manifest_path).as_posix(),
        trading_date=manifest.trading_date,
        errors=unique_errors,
        missing_required_artifacts=list(manifest.missing_required_artifacts),
        manifest_status=manifest.status,
        live_trading_authorized=manifest.live_trading_authorized,
    )


def evaluate_runtime_evidence_manifest_for_date(
    trading_date: str,
    *,
    manifest_dir: str | Path = DEFAULT_MANIFEST_DIR,
) -> RuntimeEvidenceManifestGuardResult:
    """Evaluate expected manifest for one trading date."""
    return evaluate_runtime_evidence_manifest_file(
        manifest_path_for_date(trading_date, manifest_dir=manifest_dir)
    )


def write_manifest_guard_report(
    result: RuntimeEvidenceManifestGuardResult,
    *,
    output_path: str | Path,
) -> Path:
    """Write guard result as JSON report."""
    target = Path(output_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(result.to_dict(), indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return target