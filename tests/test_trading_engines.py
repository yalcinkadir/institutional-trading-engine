from src.scoring.setup_readiness import calculate_setup_readiness
from src.scoring.confidence_score import calculate_confidence_score
from src.trading.entry_engine import evaluate_entry
from src.trading.risk_engine import calculate_position_risk


def test_setup_readiness_ready_status():
    result = calculate_setup_readiness(
        asset_score=85,
        above_sma50=True,
        above_sma200=True,
        relative_strength_class="Leader",
        rvol=1.5,
        atr_percent=3.5,
        market_regime="Bullish",
    )

    assert result["status"] == "READY"
    assert result["score"] >= 80
    assert len(result["reasons"]) > 0


def test_confidence_score_high_level():
    result = calculate_confidence_score(
        setup_score=88,
        market_health_score=82,
        vix=14,
        breadth_percent=72,
    )

    assert result["confidence"] >= 80
    assert result["level"] in {"High", "Very High"}


def test_entry_engine_enter_signal():
    result = evaluate_entry(
        setup_status="READY",
        confidence_level="High",
        market_regime="Bullish",
    )

    assert result["action"] == "ENTER"
    assert result["aggressive_mode"] is True


def test_risk_engine_position_size():
    result = calculate_position_risk(
        account_size=10000,
        risk_percent=1,
        entry_price=100,
        stop_price=95,
    )

    assert result["risk_amount"] == 100
    assert result["risk_per_share"] == 5
    assert result["shares"] == 20
