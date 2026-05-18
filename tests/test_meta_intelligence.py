from src.meta.decision_audit import audit_decisions
from src.meta.model_drift import detect_model_drift
from src.meta.self_evaluation import perform_self_evaluation
from src.meta.system_health import evaluate_system_health


def test_system_health():
    result = evaluate_system_health(
        successful_runs=95,
        failed_runs=5,
        average_report_quality_score=88,
        data_fallback_rate=10,
    )

    assert result["health_score"] >= 80
    assert result["status"] in {"Healthy", "Stable"}


def test_model_drift():
    result = detect_model_drift(
        historical_accuracy=85,
        current_accuracy=70,
    )

    assert result["classification"] in {
        "Moderate Drift",
        "Severe Drift",
    }


def test_decision_audit():
    result = audit_decisions(
        [
            {"quality_score": 90},
            {"quality_score": 80},
            {"quality_score": 70},
        ]
    )

    assert result["average_quality"] >= 75
    assert result["audit_status"] in {
        "Institutional Grade",
        "Good",
    }


def test_self_evaluation():
    result = perform_self_evaluation(
        system_health_score=85,
        signal_quality_score=80,
        drift_classification="Stable",
    )

    assert result["self_evaluation_score"] >= 75
    assert result["classification"] in {
        "Institutional Grade",
        "Operationally Strong",
    }
