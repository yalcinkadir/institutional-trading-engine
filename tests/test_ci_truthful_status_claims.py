from __future__ import annotations

from pathlib import Path

from scripts.validate_ci_truthful_status_claims import validate_file


def test_blocks_repository_wide_ci_green_claim_without_evidence(tmp_path: Path) -> None:
    doc = tmp_path / "CHANGELOG.md"
    doc.write_text(
        "# CHANGELOG\n\n"
        "## Release\n\n"
        "Full regression green.\n",
        encoding="utf-8",
    )

    errors = validate_file(doc)

    assert errors
    assert "unsupported repository-wide CI-green claim" in errors[0]


def test_allows_repository_wide_claim_with_run_evidence(tmp_path: Path) -> None:
    doc = tmp_path / "CHANGELOG.md"
    doc.write_text(
        "# CHANGELOG\n\n"
        "## Release\n\n"
        "Full regression green.\n"
        "Evidence: https://github.com/yalcinkadir/institutional-trading-engine/actions/runs/27136731016/job/80090910116\n",
        encoding="utf-8",
    )

    assert validate_file(doc) == []


def test_allows_feature_level_ci_green_status_labels(tmp_path: Path) -> None:
    doc = tmp_path / "ROADMAP.md"
    doc.write_text(
        "# ROADMAP\n\n"
        "| ID | Status |\n"
        "|---|---|\n"
        "| PO9 | Done / CI-green |\n"
        "| P132 | implemented and CI-green |\n",
        encoding="utf-8",
    )

    assert validate_file(doc) == []


def test_blocks_main_green_without_commit_or_run_evidence(tmp_path: Path) -> None:
    doc = tmp_path / "README.md"
    doc.write_text("main is green\n", encoding="utf-8")

    errors = validate_file(doc)

    assert errors
    assert "main is green" in errors[0]


def test_allows_main_green_with_commit_evidence(tmp_path: Path) -> None:
    doc = tmp_path / "README.md"
    doc.write_text(
        "main is green\n"
        "Evidence commit: d8c3193\n",
        encoding="utf-8",
    )

    assert validate_file(doc) == []
