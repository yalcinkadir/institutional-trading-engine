from src.validation.scoring_audit import (
    PUBLIC_SCORE_SYSTEMS,
    ScoreConsumer,
    ScoreSystemDefinition,
    ScoreSystemKind,
    audit_score_systems,
    render_score_audit_markdown,
)


def test_public_score_systems_are_auditable_and_pass_cleanly():
    report = audit_score_systems()

    assert report.passed
    assert not report.issues
    names = {definition.name for definition in report.definitions}
    assert "live_setup_scoring" in names
    assert "decision_engine_tier_gate" in names
    assert "report_ranking_score" in names


def test_report_ranking_score_is_not_decision_authoritative():
    report_score = next(definition for definition in PUBLIC_SCORE_SYSTEMS if definition.name == "report_ranking_score")

    assert report_score.kind == ScoreSystemKind.REPORT_ONLY
    assert not report_score.decision_authoritative
    assert report_score.consumers == (ScoreConsumer.REPORTING,)


def test_decision_engine_tier_gate_is_authoritative_for_paper_gate():
    tier_gate = next(definition for definition in PUBLIC_SCORE_SYSTEMS if definition.name == "decision_engine_tier_gate")

    assert tier_gate.decision_authoritative
    assert ScoreConsumer.PAPER_EXECUTION_GATE in tier_gate.consumers


def test_scoring_audit_flags_report_only_score_marked_authoritative():
    definitions = (
        ScoreSystemDefinition(
            name="sample_report_score",
            module_path="reports/example.py",
            score_field="ranking_score",
            kind=ScoreSystemKind.REPORT_ONLY,
            scale="presentation_only",
            consumers=(ScoreConsumer.REPORTING,),
            decision_authoritative=True,
        ),
    )

    report = audit_score_systems(definitions)

    assert not report.passed
    assert any(issue.code == "report_score_marked_authoritative" for issue in report.issues)


def test_scoring_audit_flags_non_authoritative_score_feeding_paper_gate():
    definitions = (
        ScoreSystemDefinition(
            name="sample_gate_score",
            module_path="reports/example.py",
            score_field="ranking_score",
            kind=ScoreSystemKind.REPORT_ONLY,
            scale="presentation_only",
            consumers=(ScoreConsumer.PAPER_EXECUTION_GATE,),
            decision_authoritative=False,
        ),
    )

    report = audit_score_systems(definitions)

    assert not report.passed
    assert any(issue.code == "non_authoritative_execution_gate_score" for issue in report.issues)


def test_score_audit_markdown_renders_separation_boundary():
    markdown = render_score_audit_markdown(audit_score_systems())

    assert "# CL2 Scoring System Audit" in markdown
    assert "report_ranking_score" in markdown
    assert "Decision-authoritative: **false**" in markdown
