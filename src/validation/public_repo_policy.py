"""Public repository hygiene policy checks.

IP2 turns the public/private edge handling policy into a small deterministic
validation layer that can be used by CI, tests and PR review automation.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Iterable


class PublicRepoPolicySeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


class PublicRepoPolicyStatus(str, Enum):
    PASS = "PASS"
    WARN = "WARN"
    FAIL = "FAIL"


DEFAULT_REQUIRED_POLICY_SECTIONS: tuple[str, ...] = (
    "Public repository may contain",
    "Public repository must not contain",
    "Demo defaults rule",
    "PR review checklist",
    "Telegram and report policy",
    "Private edge handling",
    "Artifact hygiene",
    "Required checks",
    "Escalation rule",
)

DEFAULT_REQUIRED_NO_LIVE_LANGUAGE: tuple[str, ...] = (
    "does not grant live trading permission",
    "Research / Paper Observation Only. No live trading authorization.",
)


@dataclass(frozen=True)
class PublicRepoPolicyFinding:
    severity: PublicRepoPolicySeverity
    code: str
    message: str
    detail: str | None = None

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["severity"] = self.severity.value
        return payload


@dataclass(frozen=True)
class PublicRepoPolicyReport:
    passed: bool
    status: PublicRepoPolicyStatus
    policy_path: str
    finding_count: int
    findings: list[PublicRepoPolicyFinding] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "status": self.status.value,
            "policy_path": self.policy_path,
            "finding_count": self.finding_count,
            "findings": [finding.to_dict() for finding in self.findings],
            "notes": list(self.notes),
        }


def validate_public_repo_policy(
    policy_path: Path | str,
    *,
    required_sections: Iterable[str] = DEFAULT_REQUIRED_POLICY_SECTIONS,
    required_no_live_language: Iterable[str] = DEFAULT_REQUIRED_NO_LIVE_LANGUAGE,
) -> PublicRepoPolicyReport:
    path = Path(policy_path)
    findings: list[PublicRepoPolicyFinding] = []

    if not path.exists():
        findings.append(
            PublicRepoPolicyFinding(
                severity=PublicRepoPolicySeverity.ERROR,
                code="missing_policy_document",
                message="public repository hygiene policy document is missing",
                detail=str(path),
            )
        )
        return _build_report(path, findings)

    text = path.read_text(encoding="utf-8")
    if not text.strip():
        findings.append(
            PublicRepoPolicyFinding(
                severity=PublicRepoPolicySeverity.ERROR,
                code="empty_policy_document",
                message="public repository hygiene policy document is empty",
                detail=str(path),
            )
        )

    for section in required_sections:
        if section not in text:
            findings.append(
                PublicRepoPolicyFinding(
                    severity=PublicRepoPolicySeverity.ERROR,
                    code="missing_required_policy_section",
                    message="required policy section is missing",
                    detail=section,
                )
            )

    for phrase in required_no_live_language:
        if phrase not in text:
            findings.append(
                PublicRepoPolicyFinding(
                    severity=PublicRepoPolicySeverity.ERROR,
                    code="missing_no_live_trading_language",
                    message="required no-live-trading language is missing",
                    detail=phrase,
                )
            )

    return _build_report(path, findings)


def write_public_repo_policy_report(
    report: PublicRepoPolicyReport,
    *,
    json_path: Path,
    markdown_path: Path,
) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report.to_dict(), indent=2, sort_keys=True), encoding="utf-8")
    markdown_path.write_text(render_public_repo_policy_markdown(report), encoding="utf-8")


def render_public_repo_policy_markdown(report: PublicRepoPolicyReport) -> str:
    lines = [
        "# IP2 Public Repository Hygiene Policy Validation",
        "",
        f"- Status: `{report.status.value}`",
        f"- Passed: `{report.passed}`",
        f"- Policy path: `{report.policy_path}`",
        f"- Findings: `{report.finding_count}`",
        "",
    ]

    if report.findings:
        lines.append("## Findings")
        lines.append("")
        lines.append("| Severity | Code | Detail | Message |")
        lines.append("|---|---|---|---|")
        for finding in report.findings:
            lines.append(
                f"| {finding.severity.value} | {finding.code} | {finding.detail or ''} | {finding.message} |"
            )
        lines.append("")
    else:
        lines.append("Policy document contains the required public/private edge handling sections.")
        lines.append("")

    lines.append("## Notes")
    lines.extend(f"- {note}" for note in report.notes)
    lines.append("")
    return "\n".join(lines)


def _build_report(path: Path, findings: list[PublicRepoPolicyFinding]) -> PublicRepoPolicyReport:
    has_errors = any(finding.severity == PublicRepoPolicySeverity.ERROR for finding in findings)
    has_warnings = any(finding.severity == PublicRepoPolicySeverity.WARNING for finding in findings)
    status = PublicRepoPolicyStatus.FAIL if has_errors else PublicRepoPolicyStatus.WARN if has_warnings else PublicRepoPolicyStatus.PASS
    return PublicRepoPolicyReport(
        passed=not has_errors,
        status=status,
        policy_path=str(path),
        finding_count=len(findings),
        findings=findings,
        notes=[
            "policy_validation_only",
            "does_not_classify_legal_ip",
            "does_not_execute_trading_logic",
            "does_not_authorize_live_trading",
        ],
    )
