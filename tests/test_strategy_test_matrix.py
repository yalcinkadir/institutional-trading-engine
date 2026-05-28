from pathlib import Path

from src.validation.strategy_test_matrix import (
    RESEARCH_ONLY_FOOTER,
    StrategyMatrixCase,
    StrategyTestMatrixConfig,
    build_strategy_test_matrix,
    demo_strategy_test_matrix_cases,
    load_strategy_test_matrix_json,
    render_strategy_test_matrix_markdown,
    write_strategy_test_matrix_report,
)


def test_demo_strategy_test_matrix_passes_all_public_safe_gates():
    report = build_strategy_test_matrix(demo_strategy_test_matrix_cases())

    assert report.passed is True
    assert report.metrics.total_cases == 6
    assert report.metrics.strategy_count == 2
    assert "risk_on" in report.metrics.regimes
    assert "risk_off" in report.metrics.regimes
    assert "paper_observation" in report.metrics.data_modes
    assert RESEARCH_ONLY_FOOTER == report.footer


def test_strategy_test_matrix_fails_when_required_fields_are_missing():
    report = build_strategy_test_matrix(
        [
            {
                "case_id": "BT2-BAD-001",
                "strategy_id": "trend_demo",
                "sleeve": "core_trend_demo",
                "regime": "risk_on",
                "setup_family": "breakout",
                "asset_class": "equity_index_demo",
                "data_mode": "synthetic",
                "validation_stage": "backtest",
                "expected_gate": "",
                "tags": ["demo", "public_safe"],
            }
        ],
        config=StrategyTestMatrixConfig(
            min_cases_per_strategy=1,
            required_regimes=("risk_on",),
            required_setup_families=("breakout",),
            required_validation_stages=("backtest",),
            required_data_modes=("synthetic",),
        ),
    )

    assert report.passed is False
    gate = next(gate for gate in report.gates if gate.name == "required_fields_complete")
    assert gate.passed is False


def test_strategy_test_matrix_fails_when_minimum_cases_per_strategy_is_not_met():
    report = build_strategy_test_matrix(
        demo_strategy_test_matrix_cases()[:2],
        config=StrategyTestMatrixConfig(
            min_cases_per_strategy=3,
            required_regimes=("risk_on", "neutral"),
            required_setup_families=("breakout", "pullback"),
            required_validation_stages=("backtest", "paper_observation"),
            required_data_modes=("synthetic", "paper_observation"),
        ),
    )

    assert report.passed is False
    gate = next(gate for gate in report.gates if gate.name == "minimum_cases_per_strategy")
    assert gate.passed is False


def test_strategy_test_matrix_fails_when_required_coverage_is_missing():
    report = build_strategy_test_matrix(
        demo_strategy_test_matrix_cases()[:3],
        config=StrategyTestMatrixConfig(required_regimes=("risk_on", "neutral", "panic_demo"), min_cases_per_strategy=1),
    )

    assert report.passed is False
    gate = next(gate for gate in report.gates if gate.name == "required_regime_coverage")
    assert gate.passed is False
    assert "panic_demo" in gate.message


def test_strategy_test_matrix_blocks_live_authorization_terms():
    clean_case = demo_strategy_test_matrix_cases()[0]
    bad_case = StrategyMatrixCase(
        case_id="BT2-BAD-002",
        strategy_id="trend_demo",
        sleeve="core_trend_demo",
        regime="risk_on",
        setup_family="breakout",
        asset_class="equity_index_demo",
        data_mode="synthetic",
        validation_stage="backtest",
        expected_gate="research_review",
        notes="This case must not become live_authorized.",
        tags=("demo", "public_safe"),
    )

    report = build_strategy_test_matrix(
        [clean_case, bad_case],
        config=StrategyTestMatrixConfig(
            min_cases_per_strategy=1,
            required_regimes=("risk_on",),
            required_setup_families=("breakout",),
            required_validation_stages=("backtest",),
            required_data_modes=("synthetic",),
        ),
    )

    assert report.passed is False
    gate = next(gate for gate in report.gates if gate.name == "no_live_trading_authorization")
    assert gate.passed is False


def test_strategy_test_matrix_blocks_private_or_proprietary_terms():
    blocked_term = "_".join(("private", "edge"))
    bad_case = StrategyMatrixCase(
        case_id="BT2-BAD-003",
        strategy_id="trend_demo",
        sleeve="core_trend_demo",
        regime="risk_on",
        setup_family="breakout",
        asset_class="equity_index_demo",
        data_mode="synthetic",
        validation_stage="backtest",
        expected_gate="research_review",
        notes=f"Do not expose {blocked_term} material.",
        tags=("demo", "public_safe"),
    )

    report = build_strategy_test_matrix(
        [bad_case],
        config=StrategyTestMatrixConfig(
            min_cases_per_strategy=1,
            required_regimes=("risk_on",),
            required_setup_families=("breakout",),
            required_validation_stages=("backtest",),
            required_data_modes=("synthetic",),
        ),
    )

    assert report.passed is False
    gate = next(gate for gate in report.gates if gate.name == "no_private_or_proprietary_terms")
    assert gate.passed is False


def test_strategy_test_matrix_requires_demo_public_safe_tags_by_default():
    raw_case = demo_strategy_test_matrix_cases()[0].to_dict()
    raw_case["tags"] = ["demo"]

    report = build_strategy_test_matrix(
        [raw_case],
        config=StrategyTestMatrixConfig(
            min_cases_per_strategy=1,
            required_regimes=("risk_on",),
            required_setup_families=("breakout",),
            required_validation_stages=("backtest",),
            required_data_modes=("synthetic",),
        ),
    )

    assert report.passed is False
    gate = next(gate for gate in report.gates if gate.name == "public_demo_only")
    assert gate.passed is False


def test_load_strategy_test_matrix_json_accepts_cases_payload(tmp_path: Path):
    path = tmp_path / "strategy_matrix.json"
    path.write_text(
        """
        {
          "cases": [
            {
              "case_id": "BT2-LOAD-001",
              "strategy_id": "trend_demo",
              "sleeve": "core_trend_demo",
              "regime": "risk_on",
              "setup_family": "breakout",
              "asset_class": "equity_index_demo",
              "data_mode": "synthetic",
              "validation_stage": "backtest",
              "expected_gate": "research_review",
              "tags": ["demo", "public_safe"]
            }
          ]
        }
        """,
        encoding="utf-8",
    )

    cases = load_strategy_test_matrix_json(path)

    assert len(cases) == 1
    assert cases[0].case_id == "BT2-LOAD-001"
    assert cases[0].tags == ("demo", "public_safe")


def test_markdown_contains_gates_cases_and_footer():
    report = build_strategy_test_matrix(demo_strategy_test_matrix_cases())
    markdown = render_strategy_test_matrix_markdown(report)

    assert "# BT2 Strategy Test Matrix" in markdown
    assert "required_regime_coverage" in markdown
    assert "BT2-DEMO-001" in markdown
    assert RESEARCH_ONLY_FOOTER in markdown


def test_write_strategy_test_matrix_report_outputs_json_and_markdown(tmp_path: Path):
    report = build_strategy_test_matrix(demo_strategy_test_matrix_cases())
    json_path = tmp_path / "strategy_test_matrix.json"
    markdown_path = tmp_path / "strategy_test_matrix.md"

    write_strategy_test_matrix_report(report, json_path=json_path, markdown_path=markdown_path)

    assert json_path.exists()
    assert markdown_path.exists()
    assert '"passed": true' in json_path.read_text(encoding="utf-8")
    assert "BT2 Strategy Test Matrix" in markdown_path.read_text(encoding="utf-8")
