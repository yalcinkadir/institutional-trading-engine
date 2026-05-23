"""Persistent report archive support for validation artifacts.

P29 copies selected local reports into a timestamped archive directory and writes
manifest files. It never calls Polygon, a broker, or any external storage.
"""

from __future__ import annotations

import json
import shutil
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_REPORT_PATHS = [
    Path("reports/backtests/historical-entry-exit-backtest.json"),
    Path("reports/backtests/historical-entry-exit-backtest.md"),
    Path("reports/backtests/out-of-sample-validation.json"),
    Path("reports/backtests/out-of-sample-validation.md"),
    Path("reports/paper-live/paper-live-observation.json"),
    Path("reports/paper-live/paper-live-observation.md"),
    Path("reports/readiness/operational-readiness-review.json"),
    Path("reports/readiness/operational-readiness-review.md"),
    Path("reports/scheduled-runs/scheduled-decision-support-dry-run.json"),
    Path("reports/scheduled-runs/scheduled-decision-support-dry-run.md"),
    Path("data/portfolio_state.json"),
]


@dataclass(frozen=True)
class ArchivedFile:
    source_path: str
    archived_path: str
    size_bytes: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ReportArchiveManifest:
    archive_id: str
    generated_at_utc: str
    archive_dir: str
    copied_files: list[ArchivedFile] = field(default_factory=list)
    missing_files: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "archive_id": self.archive_id,
            "generated_at_utc": self.generated_at_utc,
            "archive_dir": self.archive_dir,
            "copied_files": [item.to_dict() for item in self.copied_files],
            "missing_files": self.missing_files,
            "notes": self.notes,
        }


def _safe_relative_path(path: Path) -> Path:
    parts = [part for part in path.parts if part not in ("..", "")]
    if path.is_absolute():
        parts = [part for part in path.parts if part not in (path.anchor, "..", "")]
    return Path(*parts)


def build_archive_id(prefix: str = "archive") -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"{prefix}-{stamp}"


def archive_reports(
    *,
    report_paths: list[Path] | None = None,
    archive_root: Path = Path("reports/archive"),
    archive_id: str | None = None,
) -> ReportArchiveManifest:
    selected_paths = report_paths or DEFAULT_REPORT_PATHS
    archive_id = archive_id or build_archive_id()
    archive_dir = archive_root / archive_id
    archive_dir.mkdir(parents=True, exist_ok=True)

    copied: list[ArchivedFile] = []
    missing: list[str] = []

    for source in selected_paths:
        if not source.exists() or not source.is_file():
            missing.append(str(source))
            continue
        relative = _safe_relative_path(source)
        target = archive_dir / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        copied.append(
            ArchivedFile(
                source_path=str(source),
                archived_path=str(target),
                size_bytes=target.stat().st_size,
            )
        )

    manifest = ReportArchiveManifest(
        archive_id=archive_id,
        generated_at_utc=datetime.now(timezone.utc).isoformat(),
        archive_dir=str(archive_dir),
        copied_files=copied,
        missing_files=missing,
        notes=[
            "Archive is a local/pipeline artifact copy only.",
            "No external storage, broker call, or trading authorization is performed.",
        ],
    )
    write_archive_manifest(manifest, archive_dir=archive_dir)
    return manifest


def render_archive_markdown(manifest: ReportArchiveManifest) -> str:
    lines = [
        "# Report Archive Manifest",
        "",
        f"Archive ID: `{manifest.archive_id}`",
        f"Generated at UTC: `{manifest.generated_at_utc}`",
        f"Archive directory: `{manifest.archive_dir}`",
        "",
        "## Copied Files",
        "",
        "| Source | Archived Path | Size Bytes |",
        "|---|---|---:|",
    ]
    for item in manifest.copied_files:
        lines.append(f"| {item.source_path} | {item.archived_path} | {item.size_bytes} |")
    lines.extend(["", "## Missing Files", ""])
    if manifest.missing_files:
        for path in manifest.missing_files:
            lines.append(f"- {path}")
    else:
        lines.append("None")
    lines.extend(["", "## Notes", ""])
    for note in manifest.notes:
        lines.append(f"- {note}")
    return "\n".join(lines) + "\n"


def write_archive_manifest(manifest: ReportArchiveManifest, *, archive_dir: Path) -> None:
    archive_dir.mkdir(parents=True, exist_ok=True)
    (archive_dir / "manifest.json").write_text(json.dumps(manifest.to_dict(), indent=2), encoding="utf-8")
    (archive_dir / "manifest.md").write_text(render_archive_markdown(manifest), encoding="utf-8")
