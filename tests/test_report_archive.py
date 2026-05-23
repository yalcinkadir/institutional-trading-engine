from __future__ import annotations

import json
from pathlib import Path

from src.operations.report_archive import archive_reports, render_archive_markdown


def _write(path: Path, content: str = "{}") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def test_archive_reports_copies_existing_files_and_writes_manifest(tmp_path: Path) -> None:
    report_a = tmp_path / "reports/backtests/a.json"
    report_b = tmp_path / "reports/readiness/b.md"
    _write(report_a, '{"ok": true}')
    _write(report_b, "# Ready")

    archive_root = tmp_path / "reports/archive"
    manifest = archive_reports(
        report_paths=[report_a, report_b],
        archive_root=archive_root,
        archive_id="test-archive",
    )

    assert manifest.archive_id == "test-archive"
    assert len(manifest.copied_files) == 2
    assert manifest.missing_files == []
    archive_dir = archive_root / "test-archive"
    assert (archive_dir / "manifest.json").exists()
    assert (archive_dir / "manifest.md").exists()
    assert json.loads((archive_dir / "manifest.json").read_text(encoding="utf-8"))["archive_id"] == "test-archive"


def test_archive_reports_records_missing_files(tmp_path: Path) -> None:
    existing = tmp_path / "reports/backtests/existing.json"
    missing = tmp_path / "reports/backtests/missing.json"
    _write(existing, '{"ok": true}')

    manifest = archive_reports(
        report_paths=[existing, missing],
        archive_root=tmp_path / "archive",
        archive_id="missing-case",
    )

    assert len(manifest.copied_files) == 1
    assert manifest.missing_files == [str(missing)]
    markdown = render_archive_markdown(manifest)
    assert "missing.json" in markdown
    assert "Copied Files" in markdown


def test_archive_reports_uses_nested_relative_paths(tmp_path: Path) -> None:
    source = tmp_path / "reports/scheduled-runs/report.md"
    _write(source, "# Report")
    archive_root = tmp_path / "archive"

    manifest = archive_reports(
        report_paths=[source],
        archive_root=archive_root,
        archive_id="nested",
    )

    copied_path = Path(manifest.copied_files[0].archived_path)
    assert copied_path.exists()
    assert copied_path.name == "report.md"
    assert copied_path.read_text(encoding="utf-8") == "# Report"
