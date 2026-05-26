from pathlib import Path

from src.validation.performance_drift_detection import (
    PerformanceDriftConfig,
    detect_performance_drift,
    render_performance_drift_markdown,
    write_performance_drift_report,
)


def test_drift_detection_passes_when_forward_matches_baseline():
    backtest = [1.0, -0.5, 0.8, -0.2] * 10
    forward = [1.0, -0.5, 0.8, -0.2] * 4

    report = detect_performance_drift(
        backtest,
        forward,
        config=PerformanceDriftConfig(
            min_backtest_observations=30,
            min_forward_observations=10,
        ),
    )

    assert report.passed is True
    assert report.metrics.backtest_observations == 40
    assert report.metrics.forward_observations == 16
    assert report.metrics.expectancy_drift_r == 0.0
    assert report.metrics.win_rate_drift == 0.0


def test_drift_detection_fails_on_small_samples():
    report = detect_performance_drift(
        [1.0, -0.5],
        [1.0],
        config=PerformanceDriftConfig(
            min_backtest_observations=30,
            min_forward_observations=10,
            require_positive_forward_expectancy=False,
        ),
    )

    assert report.passed is False
    assert next(g for g in report.gates if g.name == "minimum_backtest_observations").passed is False
    assert next(g for g in report.gates if g.name == "minimum_forward_observations").passed is False


def test_drift_detection_fails_on_negative_forward_expectancy():
    backtest = [1.0, -0.5, 0.8, -0.2] * 10
    forward = [-0.3, -0.4, -0.2, -0.5] * 3

    report = detect_performance_drift(
        backtest,
        forward,
        config=PerformanceDriftConfig(
            min_backtest_observations=30,
            min_forward_observations=10,
            max_abs_expectancy_drift_r=2.0,
            max_abs_win_rate_drift=1.0,
            max_abs_cumulative_drift_r=100.0,
            max_abs_z_score=99.0,
        ),
    )

    assert report.passed is False
    gate = next(g for g in report.gates if g.name == "positive_forward_expectancy")
    assert gate.passed is False


def test_drift_detection_fails_on_expectancy_drift():
    backtest = [1.0, -0.5, 0.8, -0.2] * 10
    forward = [0.1, -0.1, 0.0, -0.2] * 4

    report = detect_performance_drift(
        backtest,
        forward,
        config=PerformanceDriftConfig(
            min_backtest_observations=30,
            min_forward_observations=10,
            max_abs_expectancy_drift_r=0.05,
            max_abs_win_rate_drift=1.0,
            max_abs_cumulative_drift_r=100.0,
            max_abs_z_score=99.0,
            require_positive_forward_expectancy=False,
        ),
    )

    assert report.passed is False
    gate = next(g for g in report.gates if g.name == "expectancy_drift_r")
    assert gate.passed is False


def test_drift_detection_fails_on_win_rate_drift():
    backtest = [1.0, -0.5, 0.8, -0.2] * 10
    forward = [-0.1, -0.2, -0.3, -0.4] * 4

    report = detect_performance_drift(
        backtest,
        forward,
        config=PerformanceDriftConfig(
            min_backtest_observations=30,
            min_forward_observations=10,
            max_abs_expectancy_drift_r=99.0,
            max_abs_win_rate_drift=0.1,
            max_abs_cumulative_drift_r=100.0,
            max_abs_z_score=99.0,
            require_positive_forward_expectancy=False,
        ),
    )

    assert report.passed is False
    gate = next(g for g in report.gates if g.name == "win_rate_drift")
    assert gate.passed is False


def test_drift_detection_accepts_dict_records_and_paper_r_alias():
    backtest = [{"result_r": value} for value in ([1.0, -0.5, 0.8, -0.2] * 10)]
    forward = [{"paper_r": value} for value in ([1.0, -0.5, 0.8, -0.2] * 4)]

    report = detect_performance_drift(
        backtest,
        forward,
        config=PerformanceDriftConfig(min_backtest_observations=30, min_forward_observations=10),
    )

    assert report.passed is True
    assert report.metrics.forward_observations == 16


def test_markdown_contains_drift_gates():
    backtest = [1.0, -0.5, 0.8, -0.2] * 10
    forward = [1.0, -0.5, 0.8, -0.2] * 4
    report = detect_performance_drift(
        backtest,
        forward,
        config=PerformanceDriftConfig(min_backtest_observations=30, min_forward_observations=10),
    )

    markdown = render_performance_drift_markdown(report)

    assert "# Performance Drift Detection" in markdown
    assert "expectancy_drift_r" in markdown
    assert "z_score" in markdown


def test_write_drift_report_outputs_json_and_markdown(tmp_path: Path):
    backtest = [1.0, -0.5, 0.8, -0.2] * 10
    forward = [1.0, -0.5, 0.8, -0.2] * 4
    report = detect_performance_drift(
        backtest,
        forward,
        config=PerformanceDriftConfig(min_backtest_observations=30, min_forward_observations=10),
    )
    json_path = tmp_path / "drift.json"
    markdown_path = tmp_path / "drift.md"

    write_performance_drift_report(report, json_path=json_path, markdown_path=markdown_path)

    assert json_path.exists()
    assert markdown_path.exists()
    assert '"passed": true' in json_path.read_text(encoding="utf-8")
    assert "Performance Drift Detection" in markdown_path.read_text(encoding="utf-8")
