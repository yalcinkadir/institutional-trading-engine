from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PR_TEMPLATE = REPO_ROOT / ".github" / "pull_request_template.md"
LICENSE_FILE = REPO_ROOT / "LICENSE"
DISCLAIMER = REPO_ROOT / "DISCLAIMER.md"
README = REPO_ROOT / "README.md"
ROADMAP = REPO_ROOT / "ROADMAP.md"
CHANGELOG = REPO_ROOT / "CHANGELOG.md"


REQUIRED_PR_TEMPLATE_PHRASES = [
    "IP9 Public Edge Review",
    "No proprietary thresholds, setup maps, scoring weights, exit profiles or production-like parameters",
    "public-demo defaults or synthetic fixtures",
    "Generated reports, raw evidence, provider extracts, ranked opportunity output and local artifacts are not committed",
    "Research/paper-only and no-live-trading language remains intact",
    "python scripts/check_ip_boundary.py --root . --no-write",
]


REQUIRED_DISCLAIMER_PHRASES = [
    "No financial advice",
    "Research / paper observation only",
    "Public demo defaults only",
    "No performance guarantee",
    "Live trading restriction",
    "does not grant live trading permission",
]


def test_ip9_pr_template_contains_public_edge_review_checklist() -> None:
    content = PR_TEMPLATE.read_text(encoding="utf-8")

    missing = [phrase for phrase in REQUIRED_PR_TEMPLATE_PHRASES if phrase not in content]

    assert missing == []


def test_ip10_license_and_research_disclaimer_exist() -> None:
    license_text = LICENSE_FILE.read_text(encoding="utf-8")
    disclaimer_text = DISCLAIMER.read_text(encoding="utf-8")

    assert "MIT License" in license_text
    assert "THE SOFTWARE IS PROVIDED" in license_text

    missing = [phrase for phrase in REQUIRED_DISCLAIMER_PHRASES if phrase not in disclaimer_text]

    assert missing == []


def test_ip9_ip10_are_documented_in_project_status_files() -> None:
    readme = README.read_text(encoding="utf-8")
    roadmap = ROADMAP.read_text(encoding="utf-8")
    changelog = CHANGELOG.read_text(encoding="utf-8")

    assert "IP9/IP10" in readme
    assert "IP9" in roadmap and "Done / CI-wired" in roadmap
    assert "IP10" in roadmap and "Done / CI-wired" in roadmap
    assert "IP9/IP10 Public Repository Governance" in changelog
