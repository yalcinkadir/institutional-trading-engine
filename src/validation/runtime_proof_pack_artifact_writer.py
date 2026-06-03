from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping


@dataclass(frozen=True)
class RuntimeProofPackArtifactWriterResult:
    valid: bool
    errors: tuple[str, ...]
    artifact_path: str
    retention_index_path: str
    summary: dict[str, Any]


def _utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


def _stable_json(data: Mapping[str, Any]) -> str:
    return json.dumps(data, sort_keys=True, indent=2, ensure_ascii=False) + "\n"


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _safe_slug(value: str) -> str:
    slug = "".join(char.lower() if char.isalnum() else "-" for char in value.strip())
    slug = "-".join(part for part in slug.split("-") if part)
    return slug or "runtime-proof-pack"


def _load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_runtime_proof_pack_artifact(
    *,
    output_dir: str | Path,
    proof_pack_id: str,
    observation_window: str,
    proof_pack_summary: Mapping[str, Any],
    retention_days: int = 365,
    created_at_utc: str | None = None,
    live_trading_authorized: bool = False,
    broker_execution_mode: str = "paper_only",
) -> RuntimeProofPackArtifactWriterResult:
    errors: list[str] = []

    if not str(proof_pack_id).strip():
        errors.append("missing_proof_pack_id")
    if not str(observation_window).strip():
        errors.append("missing_observation_window")
    if not isinstance(proof_pack_summary, Mapping) or not proof_pack_summary:
        errors.append("missing_proof_pack_summary")
    if retention_days < 1:
        errors.append("invalid_retention_days")
    if live_trading_authorized is not False:
        errors.append("live_trading_must_remain_false")
    if broker_execution_mode != "paper_only":
        errors.append("broker_execution_mode_must_be_paper_only")

    output_root = Path(output_dir)
    artifact_path = output_root / "runtime_proof_pack" / f"{_safe_slug(proof_pack_id)}.json"
    retention_index_path = output_root / "runtime_proof_pack_retention_index.json"

    if errors:
        return RuntimeProofPackArtifactWriterResult(
            valid=False,
            errors=tuple(errors),
            artifact_path=str(artifact_path),
            retention_index_path=str(retention_index_path),
            summary={
                "artifact_writer_status": "BLOCKED",
                "live_trading_authorized": False,
                "broker_execution_mode": "paper_only",
            },
        )

    created_at = created_at_utc or _utc_now()
    payload = {
        "proof_pack_id": proof_pack_id,
        "observation_window": observation_window,
        "created_at_utc": created_at,
        "retention_days": retention_days,
        "live_trading_authorized": False,
        "broker_execution_mode": "paper_only",
        "proof_pack_summary": dict(proof_pack_summary),
    }
    artifact_text = _stable_json(payload)
    artifact_sha256 = _sha256_text(artifact_text)

    output_root.mkdir(parents=True, exist_ok=True)
    artifact_path.parent.mkdir(parents=True, exist_ok=True)
    artifact_path.write_text(artifact_text, encoding="utf-8")

    index = _load_json(retention_index_path, {"artifacts": []})
    artifacts = list(index.get("artifacts", []))
    artifacts = [entry for entry in artifacts if entry.get("proof_pack_id") != proof_pack_id]
    artifacts.append(
        {
            "proof_pack_id": proof_pack_id,
            "observation_window": observation_window,
            "artifact_path": artifact_path.as_posix(),
            "sha256": artifact_sha256,
            "created_at_utc": created_at,
            "retention_days": retention_days,
            "retention_class": "runtime_proof_pack",
            "live_trading_authorized": False,
            "broker_execution_mode": "paper_only",
        }
    )
    artifacts.sort(key=lambda item: (item["observation_window"], item["proof_pack_id"]))

    index_payload = {
        "retention_index_status": "ACTIVE",
        "artifact_count": len(artifacts),
        "live_trading_authorized": False,
        "broker_execution_mode": "paper_only",
        "artifacts": artifacts,
    }
    retention_index_path.write_text(_stable_json(index_payload), encoding="utf-8")

    return RuntimeProofPackArtifactWriterResult(
        valid=True,
        errors=(),
        artifact_path=str(artifact_path),
        retention_index_path=str(retention_index_path),
        summary={
            "artifact_writer_status": "WRITTEN",
            "proof_pack_id": proof_pack_id,
            "observation_window": observation_window,
            "artifact_sha256": artifact_sha256,
            "retention_days": retention_days,
            "live_trading_authorized": False,
            "broker_execution_mode": "paper_only",
        },
    )
