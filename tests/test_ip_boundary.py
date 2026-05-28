from pathlib import Path

from src.validation.ip_boundary import (
    IpBoundaryPolicy,
    IpBoundarySeverity,
    IpBoundaryStatus,
    load_ip_boundary_policy,
    render_ip_boundary_markdown,
    scan_ip_boundary,
    write_ip_boundary_report,
)


def test_ip_boundary_passes_public_safe_framework_files(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("Institutional framework documentation\n", encoding="utf-8")
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "module.py").write_text("PUBLIC_THRESHOLD = 1\n", encoding="utf-8")

    report = scan_ip_boundary(tmp_path)

    assert report.passed is True
    assert report.status == IpBoundaryStatus.PASS
    assert report.finding_count == 0
    assert report.scanned_file_count == 2


def test_ip_boundary_fails_on_forbidden_private_edge_term(tmp_path: Path) -> None:
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "strategy.md").write_text(
        "Do not publish private_edge values here.\n",
        encoding="utf-8",
    )

    report = scan_ip_boundary(tmp_path)

    assert report.passed is False
    assert report.status == IpBoundaryStatus.FAIL
    assert report.findings[0].severity == IpBoundarySeverity.ERROR
    assert report.findings[0].code == "forbidden_private_edge_term"
    assert report.findings[0].path == "docs/strategy.md"


def test_ip_boundary_warns_on_suspicious_edge_assignment(tmp_path: Path) -> None:
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "score.py").write_text("edge_score = 0.91\n", encoding="utf-8")

    report = scan_ip_boundary(tmp_path)

    assert report.passed is True
    assert report.status == IpBoundaryStatus.WARN
    assert report.findings[0].severity == IpBoundarySeverity.WARNING
    assert report.findings[0].code == "suspicious_edge_pattern"


def test_ip_boundary_ignores_private_and_report_paths(tmp_path: Path) -> None:
    (tmp_path / "private").mkdir()
    (tmp_path / "private" / "edge.py").write_text("private_edge = 1\n", encoding="utf-8")
    (tmp_path / "reports").mkdir()
    (tmp_path / "reports" / "daily.md").write_text("secret_threshold = 1\n", encoding="utf-8")

    report = scan_ip_boundary(tmp_path)

    assert report.passed is True
    assert report.status == IpBoundaryStatus.PASS
    assert report.scanned_file_count == 0


def test_ip_boundary_supports_custom_policy_file(tmp_path: Path) -> None:
    policy_path = tmp_path / ".ip-boundary.yml"
    policy_path.write_text(
        "forbidden_terms:\n"
        "  - custom_secret\n"
        "public_safe_paths:\n"
        "  - docs/\n"
        "ignored_paths:\n"
        "  - reports/\n"
        "suspicious_patterns:\n"
        "  - custom_score\\s*=\\s*[0-9]\n",
        encoding="utf-8",
    )
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "a.md").write_text("custom_secret\n", encoding="utf-8")

    policy = load_ip_boundary_policy(policy_path)
    report = scan_ip_boundary(tmp_path, policy=policy)

    assert report.passed is False
    assert report.findings[0].match == "custom_secret"


def test_ip_boundary_writes_json_and_markdown_reports(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("safe docs\n", encoding="utf-8")
    report = scan_ip_boundary(tmp_path)
    json_path = tmp_path / "out" / "ip.json"
    markdown_path = tmp_path / "out" / "ip.md"

    write_ip_boundary_report(report, json_path=json_path, markdown_path=markdown_path)

    assert json_path.exists()
    assert markdown_path.exists()
    assert "# IP1 Public / Private Edge Boundary Report" in render_ip_boundary_markdown(report)
