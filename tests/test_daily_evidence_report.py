from pathlib import Path

from src.validation.daily_evidence_report import (
    DailyEvidenceConfig,
    build_daily_evidence_report,
    load_component_reports,
    render_daily_evidence_markdown,
    write_daily_evidence_report,
)


def _component(passed: bool = True, **metrics):
    return {"passed": passed, "metrics": metrics or {"observations": 30}}


def _all_components(passed: bool = True):
    return {
        "reconciliation": _component(passed, observation_days=30, action_mismatch_rate=0.0),
        "performance_drift": _component(passed, forward_expectancy_r=0.25, z_score=0.4),
        "edge_decay": _component(passed, observations=30, decision="continue_observation"),
        "regime_change": _component(passed, latest_regime="neutral", state="stable"),
        "risk_attribution": _component(passed, portfolio_r=1.2, unknown_sector_count=0),
        "monte_carlo": _component(passed, observed_expectancy_r=0.2, drawdown_p95_r=1.0),
    }


def test_daily_evidence_report_passes_when_all_components_pass():
    report = build_daily_evidence_report(_all_components(), report_date="2026-05-25")

    assert report.passed is True
    assert report.metrics.overall_status == "PASS"
    assert report.metrics.components_expected == 6
    assert report.metrics.components_present == 6
    assert report.metrics.components_passed == 6
    assert report.metrics.components_failed == 0
    assert report.metrics.components_missing == 0


def test_daily_evidence_report_fails_when_required_component_missing():
    components = _all_components()
    components.pop("monte_carlo")

    report = build_daily_evidence_report(components, report_date="2026-05-25")

    assert report.passed is False
    assert report.metrics.components_missing == 1
    gate = next(gate for gate in report.gates if gate.name == "required_components_present")
    assert gate.passed is False


def test_daily_evidence_report_fails_when_component_fails():
    components = _all_components()
    components["regime_change"] = _component(False, latest_regime="risk_off", state="regime_change_alert")

    report = build_daily_evidence_report(components, report_date="2026-05-25")

    assert report.passed is False
    assert report.metrics.components_failed == 1
    failed_component = next(component for component in report.components if component.name == "regime_change")
    assert failed_component.status == "FAIL"
    gate = next(gate for gate in report.gates if gate.name == "failed_components")
    assert gate.passed is False


def test_daily_evidence_report_can_skip_non_required_component():
    components = _all_components()
    components.pop("risk_attribution")

    report = build_daily_evidence_report(
        components,
        report_date="2026-05-25",
        config=DailyEvidenceConfig(require_risk_attribution=False),
    )

    assert report.passed is True
    skipped = next(component for component in report.components if component.name == "risk_attribution")
    assert skipped.status == "SKIPPED"


def test_daily_evidence_report_allows_configured_failed_component_tolerance():
    components = _all_components()
    components["performance_drift"] = _component(False, forward_expectancy_r=-0.1, z_score=3.0)

    report = build_daily_evidence_report(
        components,
        report_date="2026-05-25",
        config=DailyEvidenceConfig(max_failed_components=1),
    )

    assert report.passed is True
    assert report.metrics.components_failed == 1


def test_daily_evidence_report_extracts_key_metrics():
    report = build_daily_evidence_report(_all_components(), report_date="2026-05-25")

    drift = next(component for component in report.components if component.name == "performance_drift")
    assert drift.key_metrics["forward_expectancy_r"] == 0.25
    assert drift.key_metrics["z_score"] == 0.4


def test_load_component_reports_maps_known_file_names(tmp_path: Path):
    path = tmp_path / "monte_carlo_robustness.json"
    path.write_text('{"passed": true, "metrics": {"observed_expectancy_r": 0.2}}', encoding="utf-8")

    reports = load_component_reports([path])

    assert "monte_carlo" in reports
    assert reports["monte_carlo"]["passed"] is True


def test_markdown_contains_summary_components_and_gates():
    report = build_daily_evidence_report(_all_components(), report_date="2026-05-25")
    markdown = render_daily_evidence_markdown(report)

    assert "# Daily Evidence Report" in markdown
    assert "Components expected" in markdown
    assert "performance_drift" in markdown
    assert "required_components_present" in markdown


def test_write_daily_evidence_report_outputs_json_and_markdown(tmp_path: Path):
    report = build_daily_evidence_report(_all_components(), report_date="2026-05-25")
    json_path = tmp_path / "daily_evidence.json"
    markdown_path = tmp_path / "daily_evidence.md"

    write_daily_evidence_report(report, json_path=json_path, markdown_path=markdown_path)

    assert json_path.exists()
    assert markdown_path.exists()
    assert '"passed": true' in json_path.read_text(encoding="utf-8")
    assert "Daily Evidence Report" in markdown_path.read_text(encoding="utf-8")
