from pathlib import Path

from src.validation.sequential_edge_decay import (
    SequentialEdgeDecayConfig,
    render_sequential_edge_decay_markdown,
    run_sequential_edge_decay_test,
    write_sequential_edge_decay_report,
)


def test_sequential_edge_decay_accepts_baseline_when_forward_is_strong():
    values = [1.0] * 45 + [-1.0] * 15

    report = run_sequential_edge_decay_test(
        values,
        config=SequentialEdgeDecayConfig(
            baseline_win_rate=0.60,
            degraded_win_rate=0.40,
            min_observations=20,
        ),
    )

    assert report.passed is True
    assert report.metrics.decision == "accept_baseline_edge"
    assert report.metrics.win_rate == 0.75


def test_sequential_edge_decay_fails_when_degraded_edge_is_accepted():
    values = [1.0] * 15 + [-1.0] * 45

    report = run_sequential_edge_decay_test(
        values,
        config=SequentialEdgeDecayConfig(
            baseline_win_rate=0.60,
            degraded_win_rate=0.40,
            min_observations=20,
            require_positive_expectancy=False,
        ),
    )

    assert report.passed is False
    assert report.metrics.decision == "accept_degraded_edge"
    gate = next(gate for gate in report.gates if gate.name == "no_degraded_edge_decision")
    assert gate.passed is False


def test_sequential_edge_decay_fails_on_minimum_observations():
    report = run_sequential_edge_decay_test(
        [1.0, -1.0],
        config=SequentialEdgeDecayConfig(min_observations=20, require_positive_expectancy=False),
    )

    assert report.passed is False
    gate = next(gate for gate in report.gates if gate.name == "minimum_observations")
    assert gate.passed is False


def test_sequential_edge_decay_fails_on_negative_expectancy():
    values = [1.0] * 10 + [-1.0] * 15

    report = run_sequential_edge_decay_test(
        values,
        config=SequentialEdgeDecayConfig(
            baseline_win_rate=0.55,
            degraded_win_rate=0.45,
            min_observations=20,
            max_observations=250,
        ),
    )

    assert report.passed is False
    gate = next(gate for gate in report.gates if gate.name == "positive_expectancy")
    assert gate.passed is False


def test_sequential_edge_decay_can_continue_observation():
    values = [1.0, -1.0] * 15

    report = run_sequential_edge_decay_test(
        values,
        config=SequentialEdgeDecayConfig(
            baseline_win_rate=0.55,
            degraded_win_rate=0.45,
            min_observations=20,
            require_positive_expectancy=False,
        ),
    )

    assert report.passed is True
    assert report.metrics.decision == "continue_observation"


def test_sequential_edge_decay_marks_inconclusive_at_max_observations():
    values = [1.0, -1.0] * 15

    report = run_sequential_edge_decay_test(
        values,
        config=SequentialEdgeDecayConfig(
            baseline_win_rate=0.55,
            degraded_win_rate=0.45,
            min_observations=20,
            max_observations=30,
            require_positive_expectancy=False,
        ),
    )

    assert report.passed is True
    assert report.metrics.decision == "inconclusive_max_observations"


def test_sequential_edge_decay_accepts_dict_records_and_paper_r_alias():
    values = [{"paper_r": 1.0}] * 45 + [{"paper_r": -1.0}] * 15

    report = run_sequential_edge_decay_test(
        values,
        config=SequentialEdgeDecayConfig(
            baseline_win_rate=0.60,
            degraded_win_rate=0.40,
            min_observations=20,
        ),
    )

    assert report.passed is True
    assert report.metrics.observations == 60


def test_markdown_contains_sprt_decision_and_gates():
    values = [1.0] * 45 + [-1.0] * 15
    report = run_sequential_edge_decay_test(
        values,
        config=SequentialEdgeDecayConfig(
            baseline_win_rate=0.60,
            degraded_win_rate=0.40,
            min_observations=20,
        ),
    )

    markdown = render_sequential_edge_decay_markdown(report)

    assert "# Sequential Edge Decay Test" in markdown
    assert "Log-likelihood ratio" in markdown
    assert "no_degraded_edge_decision" in markdown


def test_write_sequential_edge_decay_report_outputs_json_and_markdown(tmp_path: Path):
    values = [1.0] * 45 + [-1.0] * 15
    report = run_sequential_edge_decay_test(
        values,
        config=SequentialEdgeDecayConfig(
            baseline_win_rate=0.60,
            degraded_win_rate=0.40,
            min_observations=20,
        ),
    )
    json_path = tmp_path / "sequential_edge_decay.json"
    markdown_path = tmp_path / "sequential_edge_decay.md"

    write_sequential_edge_decay_report(report, json_path=json_path, markdown_path=markdown_path)

    assert json_path.exists()
    assert markdown_path.exists()
    assert '"passed": true' in json_path.read_text(encoding="utf-8")
    assert "Sequential Edge Decay Test" in markdown_path.read_text(encoding="utf-8")
