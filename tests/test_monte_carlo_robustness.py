from pathlib import Path

from src.validation.monte_carlo_robustness import (
    MonteCarloRobustnessConfig,
    render_monte_carlo_robustness_markdown,
    run_monte_carlo_robustness,
    write_monte_carlo_robustness_report,
)


def _strong_values():
    return [1.0, 0.8, 0.6, -0.2, 0.4, -0.1] * 10


def test_monte_carlo_robustness_passes_for_stable_positive_sample():
    report = run_monte_carlo_robustness(
        _strong_values(),
        config=MonteCarloRobustnessConfig(
            simulations=300,
            seed=7,
            min_observations=30,
            min_bootstrap_expectancy_lower_r=0.0,
            max_drawdown_p95_r=5.0,
            min_permutation_p_value=0.0,
        ),
    )

    assert report.passed is True
    assert report.metrics.observations == 60
    assert report.metrics.observed_expectancy_r > 0
    assert report.metrics.bootstrap_expectancy_lower_r > 0


def test_monte_carlo_robustness_fails_on_small_sample():
    report = run_monte_carlo_robustness(
        [1.0, -0.2],
        config=MonteCarloRobustnessConfig(
            min_observations=30,
            require_positive_observed_expectancy=False,
            min_bootstrap_expectancy_lower_r=-10.0,
            min_permutation_p_value=0.0,
        ),
    )

    assert report.passed is False
    gate = next(gate for gate in report.gates if gate.name == "minimum_observations")
    assert gate.passed is False


def test_monte_carlo_robustness_fails_on_negative_expectancy():
    values = [-0.5, -0.2, 0.1, -0.1] * 10

    report = run_monte_carlo_robustness(
        values,
        config=MonteCarloRobustnessConfig(
            simulations=200,
            min_observations=30,
            min_bootstrap_expectancy_lower_r=-10.0,
            min_permutation_p_value=0.0,
        ),
    )

    assert report.passed is False
    gate = next(gate for gate in report.gates if gate.name == "positive_observed_expectancy")
    assert gate.passed is False


def test_monte_carlo_robustness_fails_on_bootstrap_lower_bound():
    values = [1.0, -0.9, 0.8, -0.7, 0.6, -0.5] * 10

    report = run_monte_carlo_robustness(
        values,
        config=MonteCarloRobustnessConfig(
            simulations=300,
            seed=11,
            min_observations=30,
            min_bootstrap_expectancy_lower_r=0.2,
            min_permutation_p_value=0.0,
            max_drawdown_p95_r=99.0,
        ),
    )

    assert report.passed is False
    gate = next(gate for gate in report.gates if gate.name == "bootstrap_expectancy_lower_bound")
    assert gate.passed is False


def test_monte_carlo_robustness_fails_on_drawdown_tail():
    values = [1.0, -1.0] * 30

    report = run_monte_carlo_robustness(
        values,
        config=MonteCarloRobustnessConfig(
            simulations=300,
            seed=13,
            min_observations=30,
            require_positive_observed_expectancy=False,
            min_bootstrap_expectancy_lower_r=-99.0,
            min_permutation_p_value=0.0,
            max_drawdown_p95_r=1.0,
        ),
    )

    assert report.passed is False
    gate = next(gate for gate in report.gates if gate.name == "drawdown_p95_r")
    assert gate.passed is False


def test_monte_carlo_robustness_accepts_dict_records_and_paper_r_alias():
    records = [{"paper_r": value} for value in _strong_values()]

    report = run_monte_carlo_robustness(
        records,
        config=MonteCarloRobustnessConfig(
            simulations=200,
            min_observations=30,
            min_permutation_p_value=0.0,
        ),
    )

    assert report.passed is True
    assert report.metrics.observations == 60


def test_monte_carlo_robustness_is_deterministic_for_seed():
    config = MonteCarloRobustnessConfig(
        simulations=200,
        seed=99,
        min_observations=30,
        min_permutation_p_value=0.0,
    )

    first = run_monte_carlo_robustness(_strong_values(), config=config)
    second = run_monte_carlo_robustness(_strong_values(), config=config)

    assert first.metrics.to_dict() == second.metrics.to_dict()


def test_markdown_contains_monte_carlo_gates():
    report = run_monte_carlo_robustness(
        _strong_values(),
        config=MonteCarloRobustnessConfig(simulations=100, min_observations=30, min_permutation_p_value=0.0),
    )
    markdown = render_monte_carlo_robustness_markdown(report)

    assert "# Monte Carlo Robustness Suite" in markdown
    assert "Bootstrap expectancy lower R" in markdown
    assert "drawdown_p95_r" in markdown


def test_write_monte_carlo_robustness_report_outputs_json_and_markdown(tmp_path: Path):
    report = run_monte_carlo_robustness(
        _strong_values(),
        config=MonteCarloRobustnessConfig(simulations=100, min_observations=30, min_permutation_p_value=0.0),
    )
    json_path = tmp_path / "monte_carlo_robustness.json"
    markdown_path = tmp_path / "monte_carlo_robustness.md"

    write_monte_carlo_robustness_report(report, json_path=json_path, markdown_path=markdown_path)

    assert json_path.exists()
    assert markdown_path.exists()
    assert '"passed": true' in json_path.read_text(encoding="utf-8")
    assert "Monte Carlo Robustness Suite" in markdown_path.read_text(encoding="utf-8")
