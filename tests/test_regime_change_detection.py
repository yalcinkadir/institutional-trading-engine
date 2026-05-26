from pathlib import Path

from src.validation.regime_change_detection import (
    RegimeChangeConfig,
    detect_regime_change,
    render_regime_change_markdown,
    write_regime_change_report,
)


def _stable_records(count: int = 30):
    return [
        {
            "regime": "neutral",
            "volatility": 0.18,
            "correlation": 0.35,
            "drawdown": 0.02,
        }
        for _ in range(count)
    ]


def test_regime_change_detection_passes_for_stable_regime():
    report = detect_regime_change(_stable_records())

    assert report.passed is True
    assert report.metrics.state == "stable"
    assert report.metrics.latest_regime == "neutral"
    assert report.metrics.label_change_count == 0


def test_regime_change_detection_fails_on_small_sample():
    report = detect_regime_change(_stable_records(5), config=RegimeChangeConfig(min_observations=20))

    assert report.passed is False
    gate = next(gate for gate in report.gates if gate.name == "minimum_observations")
    assert gate.passed is False


def test_regime_change_detection_fails_when_latest_regime_unknown():
    records = _stable_records(25)
    records[-1]["regime"] = ""

    report = detect_regime_change(records)

    assert report.passed is False
    assert report.metrics.state == "unknown_regime"
    gate = next(gate for gate in report.gates if gate.name == "latest_regime_known")
    assert gate.passed is False


def test_regime_change_detection_fails_on_label_churn():
    records = []
    for index in range(30):
        records.append(
            {
                "regime": "neutral" if index % 2 == 0 else "risk_off",
                "volatility": 0.20,
                "correlation": 0.40,
                "drawdown": 0.03,
            }
        )

    report = detect_regime_change(records, config=RegimeChangeConfig(max_label_change_rate=0.35))

    assert report.passed is False
    gate = next(gate for gate in report.gates if gate.name == "label_change_rate")
    assert gate.passed is False


def test_regime_change_detection_fails_on_volatility_jump():
    records = _stable_records(20)
    records.extend(
        {
            "regime": "risk_off",
            "volatility": 0.50,
            "correlation": 0.36,
            "drawdown": 0.03,
        }
        for _ in range(10)
    )

    report = detect_regime_change(records, config=RegimeChangeConfig(max_volatility_jump=0.50))

    assert report.passed is False
    gate = next(gate for gate in report.gates if gate.name == "volatility_jump")
    assert gate.passed is False
    assert report.metrics.state in {"regime_change_watch", "regime_change_alert"}


def test_regime_change_detection_fails_on_correlation_jump():
    records = _stable_records(20)
    records.extend(
        {
            "regime": "neutral",
            "volatility": 0.18,
            "correlation": 0.80,
            "drawdown": 0.02,
        }
        for _ in range(10)
    )

    report = detect_regime_change(records, config=RegimeChangeConfig(max_correlation_jump=0.20))

    assert report.passed is False
    gate = next(gate for gate in report.gates if gate.name == "correlation_jump")
    assert gate.passed is False


def test_regime_change_detection_fails_on_drawdown_jump():
    records = _stable_records(20)
    records.extend(
        {
            "regime": "risk_off",
            "volatility": 0.19,
            "correlation": 0.36,
            "drawdown": 0.15,
        }
        for _ in range(10)
    )

    report = detect_regime_change(records, config=RegimeChangeConfig(max_drawdown_jump=0.08))

    assert report.passed is False
    gate = next(gate for gate in report.gates if gate.name == "drawdown_jump")
    assert gate.passed is False


def test_regime_change_detection_accepts_alias_fields():
    records = [
        {
            "regime_label": "low-vol bull",
            "vix": 0.16,
            "cross_asset_correlation": 0.25,
            "drawdown_pct": 0.01,
        }
        for _ in range(25)
    ]

    report = detect_regime_change(records)

    assert report.passed is True
    assert report.metrics.latest_regime == "low_vol_bull"


def test_markdown_contains_regime_change_gates():
    report = detect_regime_change(_stable_records())
    markdown = render_regime_change_markdown(report)

    assert "# Regime Change Detection" in markdown
    assert "Change score" in markdown
    assert "latest_regime_known" in markdown


def test_write_regime_change_report_outputs_json_and_markdown(tmp_path: Path):
    report = detect_regime_change(_stable_records())
    json_path = tmp_path / "regime_change.json"
    markdown_path = tmp_path / "regime_change.md"

    write_regime_change_report(report, json_path=json_path, markdown_path=markdown_path)

    assert json_path.exists()
    assert markdown_path.exists()
    assert '"passed": true' in json_path.read_text(encoding="utf-8")
    assert "Regime Change Detection" in markdown_path.read_text(encoding="utf-8")
