from __future__ import annotations

from pathlib import Path
import importlib

import pytest

from src.report_output_boundary import ReportOutputBoundaryError


def test_generate_report_uses_guarded_writer_for_output(monkeypatch, tmp_path: Path) -> None:
    generate_report = importlib.import_module("scripts.generate_report")
    output = tmp_path / "reports" / "generated" / "example.md"
    calls: dict[str, object] = {}

    monkeypatch.setattr(generate_report, "build_report", lambda report_type: ("demo report", None))
    monkeypatch.setattr(
        generate_report,
        "parse_args",
        lambda: type("Args", (), {"type": "weekly", "output": str(output)})(),
    )

    def fake_guarded_write(path: str, content: str, *, repo_root: Path) -> Path:
        calls["path"] = path
        calls["content"] = content
        calls["repo_root"] = repo_root
        return Path(path)

    monkeypatch.setattr(generate_report, "write_report_text_guarded", fake_guarded_write)

    assert generate_report.main() == 0
    assert calls["path"] == str(output)
    assert calls["content"] == "demo report"
    assert calls["repo_root"] == generate_report.ROOT_DIR


def test_generate_report_propagates_output_boundary_error(monkeypatch) -> None:
    generate_report = importlib.import_module("scripts.generate_report")

    monkeypatch.setattr(generate_report, "build_report", lambda report_type: ("demo report", None))
    monkeypatch.setattr(
        generate_report,
        "parse_args",
        lambda: type("Args", (), {"type": "weekly", "output": "blocked.md"})(),
    )

    def fake_guarded_write(*args: object, **kwargs: object) -> Path:
        raise ReportOutputBoundaryError("protected public artifact")

    monkeypatch.setattr(generate_report, "write_report_text_guarded", fake_guarded_write)

    with pytest.raises(ReportOutputBoundaryError):
        generate_report.main()
