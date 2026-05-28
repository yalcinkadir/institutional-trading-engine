from pathlib import Path

from src.validation.public_repo_policy import (
    PublicRepoPolicyStatus,
    render_public_repo_policy_markdown,
    validate_public_repo_policy,
    write_public_repo_policy_report,
)


VALID_POLICY = """
# Policy

This document does not grant live trading permission.

## Public repository may contain
framework code

## Public repository must not contain
private edge

## Demo defaults rule
demo only

## PR review checklist
check PRs

## Telegram and report policy
Research / Paper Observation Only. No live trading authorization.

## Private edge handling
private modules

## Artifact hygiene
synthetic examples only

## Required checks
pytest

## Escalation rule
remove leak
"""


def test_public_repo_policy_passes_when_required_sections_exist(tmp_path: Path) -> None:
    policy_path = tmp_path / "policy.md"
    policy_path.write_text(VALID_POLICY, encoding="utf-8")

    report = validate_public_repo_policy(policy_path)

    assert report.passed is True
    assert report.status == PublicRepoPolicyStatus.PASS
    assert report.finding_count == 0


def test_public_repo_policy_fails_when_missing_document(tmp_path: Path) -> None:
    report = validate_public_repo_policy(tmp_path / "missing.md")

    assert report.passed is False
    assert report.status == PublicRepoPolicyStatus.FAIL
    assert report.findings[0].code == "missing_policy_document"


def test_public_repo_policy_fails_when_required_section_missing(tmp_path: Path) -> None:
    policy_path = tmp_path / "policy.md"
    policy_path.write_text("This document does not grant live trading permission.\n", encoding="utf-8")

    report = validate_public_repo_policy(policy_path)

    assert report.passed is False
    assert report.status == PublicRepoPolicyStatus.FAIL
    assert any(finding.code == "missing_required_policy_section" for finding in report.findings)


def test_public_repo_policy_fails_without_no_live_language(tmp_path: Path) -> None:
    policy_path = tmp_path / "policy.md"
    text = VALID_POLICY.replace("This document does not grant live trading permission.", "")
    policy_path.write_text(text, encoding="utf-8")

    report = validate_public_repo_policy(policy_path)

    assert report.passed is False
    assert any(finding.code == "missing_no_live_trading_language" for finding in report.findings)


def test_public_repo_policy_writes_reports(tmp_path: Path) -> None:
    policy_path = tmp_path / "policy.md"
    policy_path.write_text(VALID_POLICY, encoding="utf-8")
    report = validate_public_repo_policy(policy_path)
    json_path = tmp_path / "out" / "policy.json"
    markdown_path = tmp_path / "out" / "policy.md"

    write_public_repo_policy_report(report, json_path=json_path, markdown_path=markdown_path)

    assert json_path.exists()
    assert markdown_path.exists()
    assert "# IP2 Public Repository Hygiene Policy Validation" in render_public_repo_policy_markdown(report)
