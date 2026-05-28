"""Public/private edge boundary scanner.

IP1 provides a conservative repository hygiene gate that detects likely
private-edge terms or parameter leaks in public-safe project artefacts.
It does not classify legal IP. It is intended as a deterministic CI/PR
signal before code is published or merged.
"""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Iterable


class IpBoundarySeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


class IpBoundaryStatus(str, Enum):
    PASS = "PASS"
    WARN = "WARN"
    FAIL = "FAIL"


DEFAULT_PUBLIC_SAFE_PATHS: tuple[str, ...] = (
    "README.md",
    "ROADMAP.md",
    "docs/",
    "scripts/",
    "src/",
    "tests/",
    ".github/",
)

DEFAULT_IGNORED_PATHS: tuple[str, ...] = (
    ".git/",
    ".venv/",
    "venv/",
    "__pycache__/",
    ".pytest_cache/",
    ".mypy_cache/",
    "reports/",
    "artifacts/",
    "data/private/",
    "private/",
)

DEFAULT_FORBIDDEN_TERMS: tuple[str, ...] = (
    "alpha_weight",
    "alpha_weights",
    "private_edge",
    "proprietary_edge",
    "secret_threshold",
    "production_threshold",
    "live_signal_threshold",
    "live_entry_threshold",
    "proprietary_setup",
    "hidden_edge",
    "private_factor",
    "model_weight_secret",
    "edge_formula",
)

DEFAULT_SUSPICIOUS_PATTERNS: tuple[str, ...] = (
    r"edge[_-]?score\s*=\s*[0-9]",
    r"alpha[_-]?weight[s]?\s*=\s*\{",
    r"live[_-]?threshold\s*=\s*[0-9]",
    r"production[_-]?threshold\s*=\s*[0-9]",
    r"secret[_-]?threshold\s*=\s*[0-9]",
)

DEFAULT_TEXT_EXTENSIONS: tuple[str, ...] = (
    ".md",
    ".py",
    ".txt",
    ".yml",
    ".yaml",
    ".json",
    ".toml",
    ".ini",
    ".cfg",
)


@dataclass(frozen=True)
class IpBoundaryPolicy:
    public_safe_paths: tuple[str, ...] = DEFAULT_PUBLIC_SAFE_PATHS
    ignored_paths: tuple[str, ...] = DEFAULT_IGNORED_PATHS
    forbidden_terms: tuple[str, ...] = DEFAULT_FORBIDDEN_TERMS
    suspicious_patterns: tuple[str, ...] = DEFAULT_SUSPICIOUS_PATTERNS
    text_extensions: tuple[str, ...] = DEFAULT_TEXT_EXTENSIONS
    fail_on_forbidden_term: bool = True
    warn_on_suspicious_pattern: bool = True

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class IpBoundaryFinding:
    severity: IpBoundarySeverity
    code: str
    path: str
    line: int
    match: str
    message: str

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["severity"] = self.severity.value
        return payload


@dataclass(frozen=True)
class IpBoundaryScanReport:
    passed: bool
    status: IpBoundaryStatus
    scanned_file_count: int
    finding_count: int
    findings: list[IpBoundaryFinding] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "status": self.status.value,
            "scanned_file_count": self.scanned_file_count,
            "finding_count": self.finding_count,
            "findings": [finding.to_dict() for finding in self.findings],
            "notes": list(self.notes),
        }


def scan_ip_boundary(
    root: Path | str,
    *,
    policy: IpBoundaryPolicy | None = None,
) -> IpBoundaryScanReport:
    """Scan public-safe files for private-edge indicators."""

    scan_root = Path(root)
    active_policy = policy or IpBoundaryPolicy()
    findings: list[IpBoundaryFinding] = []
    scanned_file_count = 0

    for path in sorted(_iter_candidate_files(scan_root, active_policy)):
        scanned_file_count += 1
        relative_path = _relative_posix(path, scan_root)
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        findings.extend(_scan_text(relative_path, text, active_policy))

    has_errors = any(finding.severity == IpBoundarySeverity.ERROR for finding in findings)
    has_warnings = any(finding.severity == IpBoundarySeverity.WARNING for finding in findings)
    status = IpBoundaryStatus.FAIL if has_errors else IpBoundaryStatus.WARN if has_warnings else IpBoundaryStatus.PASS

    return IpBoundaryScanReport(
        passed=not has_errors,
        status=status,
        scanned_file_count=scanned_file_count,
        finding_count=len(findings),
        findings=findings,
        notes=[
            "public_private_edge_boundary_only",
            "conservative_ci_guardrail",
            "does_not_classify_legal_ip",
            "does_not_execute_trading_logic",
        ],
    )


def load_ip_boundary_policy(path: Path | str) -> IpBoundaryPolicy:
    """Load policy from a small YAML-like key/list file.

    The project intentionally avoids a runtime YAML dependency here. The parser
    supports the simple list-only policy shape used by .ip-boundary.yml.
    """

    policy_path = Path(path)
    if not policy_path.exists():
        return IpBoundaryPolicy()

    raw = _parse_simple_yaml_lists(policy_path.read_text(encoding="utf-8"))
    return IpBoundaryPolicy(
        public_safe_paths=tuple(raw.get("public_safe_paths", DEFAULT_PUBLIC_SAFE_PATHS)),
        ignored_paths=tuple(raw.get("ignored_paths", DEFAULT_IGNORED_PATHS)),
        forbidden_terms=tuple(raw.get("forbidden_terms", DEFAULT_FORBIDDEN_TERMS)),
        suspicious_patterns=tuple(raw.get("suspicious_patterns", DEFAULT_SUSPICIOUS_PATTERNS)),
    )


def write_ip_boundary_report(
    report: IpBoundaryScanReport,
    *,
    json_path: Path,
    markdown_path: Path,
) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report.to_dict(), indent=2, sort_keys=True), encoding="utf-8")
    markdown_path.write_text(render_ip_boundary_markdown(report), encoding="utf-8")


def render_ip_boundary_markdown(report: IpBoundaryScanReport) -> str:
    lines = [
        "# IP1 Public / Private Edge Boundary Report",
        "",
        f"- Status: `{report.status.value}`",
        f"- Passed: `{report.passed}`",
        f"- Scanned files: `{report.scanned_file_count}`",
        f"- Findings: `{report.finding_count}`",
        "",
    ]

    if report.findings:
        lines.append("## Findings")
        lines.append("")
        lines.append("| Severity | Code | Path | Line | Match |")
        lines.append("|---|---|---|---:|---|")
        for finding in report.findings:
            lines.append(
                f"| {finding.severity.value} | {finding.code} | {finding.path} | {finding.line} | `{finding.match}` |"
            )
        lines.append("")
    else:
        lines.append("No private-edge indicators detected in public-safe files.")
        lines.append("")

    lines.append("## Notes")
    lines.extend(f"- {note}" for note in report.notes)
    lines.append("")
    return "\n".join(lines)


def _iter_candidate_files(root: Path, policy: IpBoundaryPolicy) -> Iterable[Path]:
    if root.is_file():
        if _is_text_file(root, policy):
            yield root
        return

    for path in root.rglob("*"):
        if not path.is_file():
            continue
        relative_path = _relative_posix(path, root)
        if _is_ignored(relative_path, policy.ignored_paths):
            continue
        if not _is_public_safe(relative_path, policy.public_safe_paths):
            continue
        if not _is_text_file(path, policy):
            continue
        yield path


def _scan_text(path: str, text: str, policy: IpBoundaryPolicy) -> list[IpBoundaryFinding]:
    findings: list[IpBoundaryFinding] = []
    forbidden_terms = {term.lower() for term in policy.forbidden_terms}
    compiled_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in policy.suspicious_patterns]

    for line_number, line in enumerate(text.splitlines(), start=1):
        lower_line = line.lower()
        for term in forbidden_terms:
            if term in lower_line:
                severity = IpBoundarySeverity.ERROR if policy.fail_on_forbidden_term else IpBoundarySeverity.WARNING
                findings.append(
                    IpBoundaryFinding(
                        severity=severity,
                        code="forbidden_private_edge_term",
                        path=path,
                        line=line_number,
                        match=term,
                        message="private-edge indicator found in public-safe file",
                    )
                )
        if policy.warn_on_suspicious_pattern:
            for pattern in compiled_patterns:
                match = pattern.search(line)
                if match:
                    findings.append(
                        IpBoundaryFinding(
                            severity=IpBoundarySeverity.WARNING,
                            code="suspicious_edge_pattern",
                            path=path,
                            line=line_number,
                            match=match.group(0),
                            message="suspicious edge-like parameter assignment found",
                        )
                    )
    return findings


def _parse_simple_yaml_lists(text: str) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    current_key: str | None = None
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.endswith(":"):
            current_key = line[:-1].strip()
            result[current_key] = []
            continue
        if line.startswith("-") and current_key:
            value = line[1:].strip().strip('"').strip("'")
            result[current_key].append(value)
    return result


def _relative_posix(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def _is_public_safe(relative_path: str, prefixes: Iterable[str]) -> bool:
    return any(relative_path == prefix.rstrip("/") or relative_path.startswith(prefix) for prefix in prefixes)


def _is_ignored(relative_path: str, prefixes: Iterable[str]) -> bool:
    return any(relative_path == prefix.rstrip("/") or relative_path.startswith(prefix) for prefix in prefixes)


def _is_text_file(path: Path, policy: IpBoundaryPolicy) -> bool:
    return path.suffix.lower() in policy.text_extensions or path.name in {"README", "LICENSE"}
