from pathlib import Path

from scripts.create_backup import create_backup


def test_create_backup(tmp_path):
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)

    sample_report = reports_dir / "sample.md"
    sample_report.write_text("test report", encoding="utf-8")

    output_dir = tmp_path / "backups"
    archive = create_backup(
        output_dir=output_dir,
        name_prefix="test-backup",
    )

    assert archive.exists()
    assert archive.suffix == ".zip"
