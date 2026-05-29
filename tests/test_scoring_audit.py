from src.validation.scoring_audit import audit_score_systems


def test_public_score_systems_are_auditable():
    report = audit_score_systems()
    assert report.passed
