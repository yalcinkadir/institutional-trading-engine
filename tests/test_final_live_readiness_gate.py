import json

from src.validation.final_live_readiness_gate import (
    MAX_LIVE_DRAWDOWN_MULTIPLE,
    READINESS_NOT_READY,
    READINESS_OBSERVATION_ONLY,
    READINESS_REVIEW_READY,
    FinalReadinessEvidence,
    default_capital_risk_phases,
    evaluate_final_live_readiness,
    render_final_live_readiness_markdown,
    write_final_live_readiness_report,
)


def _passing_evidence() -> FinalReadinessEvidence:
    return FinalReadinessEvidence(
        historical_edge_passed=True,
        regime_phase_passed=True,
        walk_forward_passed=True,
        execution_realism_passed=True,
        out_of_sample_passed=True,
        paper_observation_passed=True,
        paper_observation_months=6,
        paper_vs_backtest_ratio=0.9,
        manual_review_completed=True,
        risk_limits_defined=True,
        kill_switch_defined=True,
        live_drawdown_limit_multiple=1.5,
    )


def test_final_readiness_passes_when_all_gates_pass() -> None:
    report = evaluate_final_live_readiness(_passing_evidence())

    assert report.ready is True
    assert report.readiness_level == READINESS_REVIEW_READY
    assert all(gate.passed for gate in report.gates)


def test_final_readiness_fails_closed_with_missing_evidence() -> None:
    report = evaluate_final_live_readiness(FinalReadinessEvidence())

    assert report.ready is False
    assert report.readiness_level == READINESS_NOT_READY
    assert any(gate.name == "historical_edge_validation" and not gate.passed for gate in report.gates)
    assert any(gate.name == "kill_switch_defined" and not gate.passed for gate in report.gates)


def test_observation_only_level_when_validation_passes_but_review_not_complete() -> None:
    evidence = FinalReadinessEvidence(
        historical_edge_passed=True,
        regime_phase_passed=True,
        walk_forward_passed=True,
        execution_realism_passed=True,
        out_of_sample_passed=True,
        paper_observation_passed=False,
        paper_observation_months=1,
    )

    report = evaluate_final_live_readiness(evidence)

    assert report.ready is False
    assert report.readiness_level == READINESS_OBSERVATION_ONLY


def test_minimum_paper_observation_duration_is_required() -> None:
    evidence = _passing_evidence().__class__(
        **{**_passing_evidence().to_dict(), "paper_observation_months": 2.9}
    )

    report = evaluate_final_live_readiness(evidence)

    assert report.ready is False
    assert any(gate.name == "minimum_paper_observation_duration" and not gate.passed for gate in report.gates)


def test_paper_vs_backtest_ratio_must_be_at_least_85_percent() -> None:
    evidence = _passing_evidence().__class__(
        **{**_passing_evidence().to_dict(), "paper_vs_backtest_ratio": 0.84}
    )

    report = evaluate_final_live_readiness(evidence)

    assert report.ready is False
    assert any(gate.name == "paper_vs_backtest_stability" and not gate.passed for gate in report.gates)


def test_drawdown_kill_switch_must_not_exceed_limit() -> None:
    evidence = _passing_evidence().__class__(
        **{**_passing_evidence().to_dict(), "live_drawdown_limit_multiple": MAX_LIVE_DRAWDOWN_MULTIPLE + 0.1}
    )

    report = evaluate_final_live_readiness(evidence)

    assert report.ready is False
    assert any(gate.name == "drawdown_kill_switch_limit" and not gate.passed for gate in report.gates)


def test_capital_risk_phases_are_staged() -> None:
    phases = default_capital_risk_phases()

    assert [phase.max_size_fraction for phase in phases] == [0.5, 0.75, 1.0]
    assert phases[0].phase == "months_1_to_3"
    assert phases[1].minimum_duration_months == 3


def test_markdown_contains_gates_capital_phases_and_guardrails() -> None:
    report = evaluate_final_live_readiness(_passing_evidence())

    markdown = render_final_live_readiness_markdown(report)

    assert "# Final Live Readiness Gate" in markdown
    assert "Capital Risk Phases" in markdown
    assert "Kill Switch Rules" in markdown
    assert "Code quality is not trading edge" in markdown


def test_write_final_live_readiness_report(tmp_path) -> None:
    report = evaluate_final_live_readiness(_passing_evidence())
    json_path = tmp_path / "final-readiness.json"
    markdown_path = tmp_path / "final-readiness.md"

    write_final_live_readiness_report(report, json_path=json_path, markdown_path=markdown_path)

    data = json.loads(json_path.read_text(encoding="utf-8"))
    assert data["ready"] is True
    assert data["readiness_level"] == READINESS_REVIEW_READY
    assert markdown_path.read_text(encoding="utf-8").startswith("# Final Live Readiness Gate")
