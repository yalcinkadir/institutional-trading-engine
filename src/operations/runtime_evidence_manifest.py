"""
Runtime Evidence Manifest.

PSR1 introduces a daily evidence manifest for paper/observation runtime output.

The manifest is intentionally simple, deterministic and public-safe:
- it stores file metadata and SHA256 hashes
- it records missing required evidence artifacts
- it marks the day PASS only when all required artifacts exist
- it explicitly states that live trading is not authorized by code

This module does not fetch market data, place orders or infer trading edge.
It only records evidence integrity for auditability.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any, Iterable

SCHEMA_VERSION = "PSR1_RUNTIME_EVIDENCE_MANIFEST_V1"
DEFAULT_MANIFEST_DIR = Path("reports/evidence/manifests")


@dataclass(frozen=True)
class EvidenceArtifact:
    """Metadata for one evidence artifact."""

    path: str
    category: str
    required: bool
    exists: bool
    sha256: str | None
    size_bytes: int | None


@dataclass(frozen=True)
class RuntimeEvidenceManifest:
    """Daily runtime evidence manifest."""

    schema_version: str
    trading_date: str
    created_at: str
    observation_mode: str
    live_trading_authorized: bool
    status: str
    missing_required_artifacts: list[str]
    artifacts: list[EvidenceArtifact]
    notes: list[str]

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["artifacts"] = [asdict(artifact) for artifact in self.artifacts]
        return payload


def utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


def _normalize_path(path: str | Path) -> Path:
    return Path(path)


def sha256_file(path: str | Path) -> str:
    """Return SHA256 hash for a file."""
    file_path = _normalize_path(path)
    digest = hashlib.sha256()

    with file_path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()


def build_artifact(
    path: str | Path,
    *,
    category: str,
    required: bool,
) -> EvidenceArtifact:
    """Build metadata for one artifact path."""
    file_path = _normalize_path(path)
    exists = file_path.exists() and file_path.is_file()

    return EvidenceArtifact(
        path=file_path.as_posix(),
        category=category,
        required=required,
        exists=exists,
        sha256=sha256_file(file_path) if exists else None,
        size_bytes=file_path.stat().st_size if exists else None,
    )


def _build_artifacts(
    paths: Iterable[str | Path],
    *,
    category: str,
    required: bool,
) -> list[EvidenceArtifact]:
    return [
        build_artifact(path, category=category, required=required)
        for path in sorted((Path(item) for item in paths), key=lambda value: value.as_posix())
    ]


def build_runtime_evidence_manifest(
    *,
    trading_date: str | date,
    required_inputs: Iterable[str | Path] = (),
    required_outputs: Iterable[str | Path] = (),
    required_governance_state: Iterable[str | Path] = (),
    optional_artifacts: Iterable[str | Path] = (),
    observation_mode: str = "paper_observation",
    created_at: str | None = None,
    notes: Iterable[str] = (),
) -> RuntimeEvidenceManifest:
    """
    Build a daily runtime evidence manifest.

    Status semantics:
    - PASS: every required input/output/governance artifact exists
    - FAIL: at least one required artifact is missing
    """
    trading_date_str = (
        trading_date.isoformat() if isinstance(trading_date, date) else str(trading_date)
    )

    artifacts: list[EvidenceArtifact] = []
    artifacts.extend(
        _build_artifacts(required_inputs, category="required_input", required=True)
    )
    artifacts.extend(
        _build_artifacts(required_outputs, category="required_output", required=True)
    )
    artifacts.extend(
        _build_artifacts(
            required_governance_state,
            category="required_governance_state",
            required=True,
        )
    )
    artifacts.extend(
        _build_artifacts(optional_artifacts, category="optional_artifact", required=False)
    )

    missing_required = [
        artifact.path
        for artifact in artifacts
        if artifact.required and not artifact.exists
    ]

    status = "PASS" if not missing_required else "FAIL"

    return RuntimeEvidenceManifest(
        schema_version=SCHEMA_VERSION,
        trading_date=trading_date_str,
        created_at=created_at or utc_now_iso(),
        observation_mode=observation_mode,
        live_trading_authorized=False,
        status=status,
        missing_required_artifacts=missing_required,
        artifacts=artifacts,
        notes=list(notes),
    )


def write_runtime_evidence_manifest(
    manifest: RuntimeEvidenceManifest,
    *,
    output_dir: str | Path = DEFAULT_MANIFEST_DIR,
) -> Path:
    """Write manifest JSON to reports/evidence/manifests/YYYY-MM-DD-runtime-evidence-manifest.json."""
    target_dir = Path(output_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    output_path = target_dir / f"{manifest.trading_date}-runtime-evidence-manifest.json"
    output_path.write_text(
        json.dumps(manifest.to_dict(), indent=2, sort_keys=True),
        encoding="utf-8",
    )

    latest_path = target_dir / "latest-runtime-evidence-manifest.json"
    latest_path.write_text(
        json.dumps(manifest.to_dict(), indent=2, sort_keys=True),
        encoding="utf-8",
    )

    return output_path


def load_runtime_evidence_manifest(path: str | Path) -> RuntimeEvidenceManifest:
    """Load a runtime evidence manifest from JSON."""
    payload = json.loads(Path(path).read_text(encoding="utf-8"))

    artifacts = [
        EvidenceArtifact(
            path=str(item["path"]),
            category=str(item["category"]),
            required=bool(item["required"]),
            exists=bool(item["exists"]),
            sha256=item.get("sha256"),
            size_bytes=item.get("size_bytes"),
        )
        for item in payload.get("artifacts", [])
    ]

    return RuntimeEvidenceManifest(
        schema_version=str(payload["schema_version"]),
        trading_date=str(payload["trading_date"]),
        created_at=str(payload["created_at"]),
        observation_mode=str(payload["observation_mode"]),
        live_trading_authorized=bool(payload["live_trading_authorized"]),
        status=str(payload["status"]),
        missing_required_artifacts=[
            str(item) for item in payload.get("missing_required_artifacts", [])
        ],
        artifacts=artifacts,
        notes=[str(item) for item in payload.get("notes", [])],
    )


def validate_runtime_evidence_manifest(manifest: RuntimeEvidenceManifest) -> dict[str, Any]:
    """Validate manifest consistency."""
    errors: list[str] = []

    if manifest.schema_version != SCHEMA_VERSION:
        errors.append("invalid_schema_version")

    if manifest.live_trading_authorized:
        errors.append("live_trading_authorized_must_be_false")

    missing_required = [
        artifact.path
        for artifact in manifest.artifacts
        if artifact.required and not artifact.exists
    ]

    if missing_required != manifest.missing_required_artifacts:
        errors.append("missing_required_artifacts_mismatch")

    expected_status = "PASS" if not missing_required else "FAIL"
    if manifest.status != expected_status:
        errors.append("status_mismatch")

    return {
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
    }