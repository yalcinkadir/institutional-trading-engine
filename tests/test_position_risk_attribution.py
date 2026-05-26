from pathlib import Path

from src.validation.position_risk_attribution import (
    PositionRiskAttributionConfig,
    attribute_position_risk,
    render_position_risk_attribution_markdown,
    write_position_risk_attribution_report,
)


def _records():
    return [
        {
            "symbol": "AAPL",
            "sector": "Technology",
            "weight": 0.50,
            "result_r": 1.20,
            "beta": 1.10,
            "market_return_r": 0.20,
            "factor_exposures": {"growth": 0.60},
            "factor_returns": {"growth": 0.30},
        },
        {
            "symbol": "XLF",
            "sector": "Financials",
            "weight": 0.50,
            "result_r": -0.20,
            "beta": 0.90,
            "market_return_r": 0.20,
            "factor_exposures": {"value": 0.50},
            "factor_returns": {"value": -0.10},
        },
    ]


def test_position_risk_attribution_passes_for_balanced_positions():
    report = attribute_position_risk(_records())

    assert report.passed is True
    assert report.metrics.positions == 2
    assert report.metrics.portfolio_r == 0.5
    assert report.metrics.beta_contribution_r == 0.2
    assert report.metrics.factor_contribution_r == 0.065
    assert report.metrics.unknown_sector_count == 0
    assert report.metrics.sector_contributions["technology"] == 0.6
    assert report.metrics.sector_contributions["financials"] == -0.1


def test_position_risk_attribution_fails_without_positions():
    report = attribute_position_risk([], config=PositionRiskAttributionConfig(min_positions=1))

    assert report.passed is False
    gate = next(gate for gate in report.gates if gate.name == "minimum_positions")
    assert gate.passed is False


def test_position_risk_attribution_fails_on_unknown_sector():
    records = _records()
    records[0]["sector"] = ""

    report = attribute_position_risk(records)

    assert report.passed is False
    gate = next(gate for gate in report.gates if gate.name == "known_sector_coverage")
    assert gate.passed is False
    assert report.metrics.unknown_sector_count == 1


def test_position_risk_attribution_fails_on_single_name_concentration():
    records = _records()
    records[0]["result_r"] = 5.0

    report = attribute_position_risk(
        records,
        config=PositionRiskAttributionConfig(max_single_name_contribution_r=1.0),
    )

    assert report.passed is False
    gate = next(gate for gate in report.gates if gate.name == "single_name_concentration")
    assert gate.passed is False


def test_position_risk_attribution_fails_on_sector_concentration():
    records = _records()
    records.append(
        {
            "symbol": "MSFT",
            "sector": "Technology",
            "weight": 0.50,
            "result_r": 4.0,
            "beta": 1.0,
            "market_return_r": 0.10,
        }
    )

    report = attribute_position_risk(
        records,
        config=PositionRiskAttributionConfig(
            max_single_name_contribution_r=10.0,
            max_sector_contribution_r=1.0,
        ),
    )

    assert report.passed is False
    gate = next(gate for gate in report.gates if gate.name == "sector_concentration")
    assert gate.passed is False


def test_position_risk_attribution_fails_on_factor_concentration():
    records = _records()
    records[0]["factor_returns"] = {"growth": 5.0}

    report = attribute_position_risk(
        records,
        config=PositionRiskAttributionConfig(max_factor_contribution_r=1.0),
    )

    assert report.passed is False
    gate = next(gate for gate in report.gates if gate.name == "factor_concentration")
    assert gate.passed is False


def test_position_risk_attribution_accepts_alias_fields():
    records = [
        {
            "ticker": "spy",
            "gics_sector": "ETF",
            "position_weight": 1.0,
            "paper_r": 0.5,
            "market_beta": 1.0,
            "benchmark_r": 0.2,
            "factors": {"market": 1.0},
            "factor_returns": {"market": 0.1},
        }
    ]

    report = attribute_position_risk(records)

    assert report.passed is True
    assert report.metrics.position_attributions[0].symbol == "SPY"
    assert report.metrics.sector_contributions["etf"] == 0.5


def test_markdown_contains_gates_and_contribution_tables():
    report = attribute_position_risk(_records())
    markdown = render_position_risk_attribution_markdown(report)

    assert "# Position-Level Risk Attribution" in markdown
    assert "single_name_concentration" in markdown
    assert "Sector Contributions" in markdown
    assert "Factor Contributions" in markdown


def test_write_position_risk_attribution_report_outputs_json_and_markdown(tmp_path: Path):
    report = attribute_position_risk(_records())
    json_path = tmp_path / "position_risk_attribution.json"
    markdown_path = tmp_path / "position_risk_attribution.md"

    write_position_risk_attribution_report(report, json_path=json_path, markdown_path=markdown_path)

    assert json_path.exists()
    assert markdown_path.exists()
    assert '"passed": true' in json_path.read_text(encoding="utf-8")
    assert "Position-Level Risk Attribution" in markdown_path.read_text(encoding="utf-8")
