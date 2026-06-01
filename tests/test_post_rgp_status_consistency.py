from __future__ import annotations

from pathlib import Path

RGP_IDS = tuple(f"RGP{index}" for index in range(1, 13))
ROOT = Path(__file__).resolve().parents[1]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def _line_containing(document: str, token: str) -> str:
    for line in document.splitlines():
        if token in line:
            return line
    raise AssertionError(f"Missing line containing {token!r}")


def test_readme_marks_every_rgp_item_ci_green_after_post_rgp_review() -> None:
    readme = _read("README.md")

    for rgp_id in RGP_IDS:
        line = _line_containing(readme, f"{rgp_id}:")
        assert "CI-green" in line
        assert "CI-wired" not in line
        assert "Pending" not in line


def test_roadmap_marks_every_rgp_item_done_ci_green_after_post_rgp_review() -> None:
    roadmap = _read("ROADMAP.md")

    for rgp_id in RGP_IDS:
        line = _line_containing(roadmap, f"| {rgp_id} |")
        assert "Done / CI-green" in line
        assert "CI-wired" not in line
        assert "Pending" not in line


def test_changelog_contains_post_rgp_green_closure_entry() -> None:
    changelog = _read("CHANGELOG.md")

    assert "## Post-RGP Stabilization Review" in changelog
    assert "RGP1-RGP12" in changelog
    assert "Done / CI-green" in changelog
    assert "Live trading authorization: unchanged; not granted by code." in changelog
