from __future__ import annotations

from src.validation.position_forward_evidence_attribution import build_position_forward_evidence_attribution
from src.validation.position_risk_attribution import attribute_position_risk


def _risk_report():
    return attribute_position_risk(
        [
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
                "symbol": "MSFT",
                "sector": "Technology",
                "weight": 0.50,
                "result_r": 0.40,
                "beta": 1.00,
                "market_return_r": 0.20,
                "factor_exposures": {"quality": 0.50},
                "factor_returns": {"quality": 0.20},
            },
        ]
    )


def _decision_records():
    return [
        {
            "symbol": "AAPL",
            "market_state": "bullish",
            "setup_type": "momentum_breakout",
            "decision": "approved",
            "risk_tier": "tier_1",
            "setup_score": 87,
            "regime_alignment": 0.82,
            "asymmetry_score": 0.76,
            "data_confidence": 0.91,
            "result_1d": 0.25,
            "result_5d": 1.20,
            "result_20d": 1.80,
            "mfe": 2.10,
            "mae": -0.35,
        },
        {
            "symbol": "MSFT",
            "market_state": "bullish",
            "setup_type": "quality_pullback",
            "decision": "approved",
            "risk_tier": "tier_1",
            "setup_score": 79,
            "regime_alignment": 0.74,
            "asymmetry_score": 0.68,
            "data_confidence": 0.88,
            "result_1d": 0.10,
            "result_5d": 0.40,
            "result_20d": 0.55,
            "mfe": 0.90,
            "mae": -0.20,
        },
    ]


def test_pfa1_builds_review_ready_position_forward_attribution() -> None:
    result = build_position_forward_evidence_attribution(
        risk_report=_risk_report(),
        decision_records=_decision_records(),
        observation_window="2026-06",
        evidence_manifest_path="reports/monthly_paper_observation_review/2026-06.json",
        live_trading_authorized=False,
        broker_execution_mode="paper_only",
    )

    assert result.valid is True
    assert result.errors == ()
    assert result.summary["position_forward_attribution_status"] == "REVIEW_READY"
    assert result.summary["approved_for_forward_review"] is True
    assert result.summary["position_count"] == 2
    assert result.summary["matched_position_count"] == 2
    assert result.summary["unmatched_symbols"] == []
    assert result.summary["portfolio_outcome"]["total_result_5d"] == 1.6
    assert result.summary["position_attributions"][0]["symbol"] == "AAPL"
    assert result.summary["position_attributions"][0]["risk_contribution_r"] == 0.6
    assert result.summary["position_attributions"][0]["result_5d"] == 1.2
    assert result.summary["live_trading_authorized"] is False
    assert result.summary["broker_execution_mode"] == "paper_only"


def test_pfa1_blocks_when_position_has_no_forward_outcome_record() -> None:
    result = build_position_forward_evidence_attribution(
        risk_report=_risk_report(),
        decision_records=[_decision_records()[0]],
        observation_window="2026-06",
        evidence_manifest_path="reports/monthly_paper_observation_review/2026-06.json",
    )

    assert result.valid is False
    assert "unmatched_position_symbols" in result.errors
    assert result.summary["unmatched_symbols"] == ["MSFT"]
    assert result.summary["position_forward_attribution_status"] == "BLOCKED"


def test_pfa1_blocks_when_risk_report_failed() -> None:
    failed_report = attribute_position_risk([])

    result = build_position_forward_evidence_attribution(
        risk_report=failed_report,
        decision_records=_decision_records(),
        observation_window="2026-06",
        evidence_manifest_path="reports/monthly_paper_observation_review/2026-06.json",
    )

    assert result.valid is False
    assert "risk_attribution_report_failed" in result.errors
    assert result.summary["risk_report_passed"] is False


def test_pfa1_blocks_missing_required_review_identity() -> None:
    result = build_position_forward_evidence_attribution(
        risk_report=_risk_report(),
        decision_records=_decision_records(),
        observation_window="",
        evidence_manifest_path="",
    )

    assert result.valid is False
    assert "missing_observation_window" in result.errors
    assert "missing_evidence_manifest_path" in result.errors


def test_pfa1_preserves_paper_only_safety_boundary() -> None:
    result = build_position_forward_evidence_attribution(
        risk_report=_risk_report(),
        decision_records=_decision_records(),
        observation_window="2026-06",
        evidence_manifest_path="reports/monthly_paper_observation_review/2026-06.json",
        live_trading_authorized=True,
        broker_execution_mode="live",
    )

    assert result.valid is False
    assert "live_trading_must_remain_false" in result.errors
    assert "broker_execution_mode_must_be_paper_only" in result.errors
    assert result.summary["live_trading_authorized"] is False
    assert result.summary["broker_execution_mode"] == "paper_only"
