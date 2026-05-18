from src.governance.compliance_engine import evaluate_compliance
from src.governance.exposure_policy import enforce_exposure_policy
from src.governance.kill_switch import evaluate_kill_switch
from src.governance.risk_limits import validate_risk_limits


def test_risk_limits():
    result = validate_risk_limits(
        portfolio_drawdown_percent=12,
        max_drawdown_percent=10,
        daily_loss_percent=3,
        max_daily_loss_percent=5,
    )

    assert result["status"] == "BREACH"
    assert "max_drawdown_breached" in result["breaches"]


def test_compliance_engine():
    result = evaluate_compliance(
        leverage=6,
        max_leverage=5,
        restricted_assets=["XYZ"],
        portfolio_assets=["NVDA", "XYZ"],
    )

    assert result["status"] == "NON_COMPLIANT"
    assert "restricted_assets_detected" in result["violations"]


def test_kill_switch():
    result = evaluate_kill_switch(
        vix=45,
        drawdown_percent=22,
        severe_anomaly_count=6,
    )

    assert result["kill_switch"] is True
    assert len(result["reasons"]) >= 2


def test_exposure_policy():
    result = enforce_exposure_policy(
        sector_exposure_percent=45,
        max_sector_exposure_percent=35,
        single_position_percent=18,
        max_single_position_percent=15,
    )

    assert result["status"] == "REVIEW_REQUIRED"
    assert "sector_exposure_exceeded" in result["warnings"]
