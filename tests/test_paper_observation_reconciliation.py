from pathlib import Path

from src.validation.paper_observation_reconciliation import (
    PaperObservationConfig,
    reconcile_paper_observation,
    render_paper_observation_markdown,
    write_paper_observation_report,
)


def _records(days: int = 3):
    rows = []
    for day in range(1, days + 1):
        rows.extend(
            [
                {
                    "date": f"2026-06-{day:02d}",
                    "expected_action": "enter_long",
                    "paper_action": "buy",
                    "expected_r": 1.0,
                    "paper_r": 0.95,
                },
                {
                    "date": f"2026-06-{day:02d}",
                    "expected_action": "skip",
                    "paper_action": "skip",
                    "expected_r": 0.0,
                    "paper_r": 0.0,
                },
            ]
        )
    return rows


def test_reconciliation_passes_for_clean_observation_fixture():
    report = reconcile_paper_observation(
        _records(days=3),
        config=PaperObservationConfig(min_observation_days=3),
    )

    assert report.passed is True
    assert report.observation_only is True
    assert report.metrics.observation_days == 3
    assert report.metrics.total_records == 6
    assert report.metrics.action_mismatch_rate == 0.0
    assert report.metrics.unresolved_records == 0
    assert report.metrics.paper_total_r == 2.85
    assert report.metrics.expected_total_r == 3.0


def test_reconciliation_fails_when_observation_only_disabled():
    report = reconcile_paper_observation(
        _records(days=3),
        config=PaperObservationConfig(min_observation_days=3),
        observation_only=False,
    )

    assert report.passed is False
    gate = next(gate for gate in report.gates if gate.name == "observation_only_mode")
    assert gate.passed is False


def test_reconciliation_fails_on_action_mismatch_rate():
    records = _records(days=3)
    records[0]["paper_action"] = "skip"

    report = reconcile_paper_observation(
        records,
        config=PaperObservationConfig(
            min_observation_days=3,
            max_action_mismatch_rate=0.01,
        ),
    )

    assert report.passed is False
    gate = next(gate for gate in report.gates if gate.name == "action_mismatch_rate")
    assert gate.passed is False
    assert report.metrics.action_mismatches == 1


def test_reconciliation_fails_on_unresolved_records():
    records = _records(days=3)
    records.append({"date": "2026-06-04", "expected_action": "enter_long"})

    report = reconcile_paper_observation(
        records,
        config=PaperObservationConfig(min_observation_days=3),
    )

    assert report.passed is False
    gate = next(gate for gate in report.gates if gate.name == "unresolved_records")
    assert gate.passed is False
    assert report.metrics.unresolved_records == 1


def test_reconciliation_fails_on_daily_drift():
    records = _records(days=3)
    records[0]["paper_r"] = -2.0

    report = reconcile_paper_observation(
        records,
        config=PaperObservationConfig(
            min_observation_days=3,
            max_abs_daily_drift_r=0.5,
        ),
    )

    assert report.passed is False
    gate = next(gate for gate in report.gates if gate.name == "max_abs_daily_drift_r")
    assert gate.passed is False


def test_markdown_contains_metrics_and_gates():
    report = reconcile_paper_observation(
        _records(days=3),
        config=PaperObservationConfig(min_observation_days=3),
    )
    markdown = render_paper_observation_markdown(report)

    assert "# Paper Observation Daily Reconciliation" in markdown
    assert "Observation-only mode" in markdown
    assert "minimum_observation_days" in markdown
    assert "action_mismatch_rate" in markdown


def test_write_report_outputs_json_and_markdown(tmp_path: Path):
    report = reconcile_paper_observation(
        _records(days=3),
        config=PaperObservationConfig(min_observation_days=3),
    )
    json_path = tmp_path / "paper_observation.json"
    markdown_path = tmp_path / "paper_observation.md"

    write_paper_observation_report(
        report,
        json_path=json_path,
        markdown_path=markdown_path,
    )

    assert json_path.exists()
    assert markdown_path.exists()
    assert '"observation_only": true' in json_path.read_text(encoding="utf-8")
    assert "Paper Observation Daily Reconciliation" in markdown_path.read_text(encoding="utf-8")
