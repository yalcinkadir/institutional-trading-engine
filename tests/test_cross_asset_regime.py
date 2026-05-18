from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cross_asset_regime import (  # noqa: E402
    CrossAssetInput,
    evaluate_cross_asset_regime,
)


def test_cross_asset_risk_off_detects_macro_stress():
    regime = evaluate_cross_asset_regime(
        dollar=CrossAssetInput("UUP", 0.06, True, True),
        long_bonds=CrossAssetInput("TLT", -0.08, False, False),
        high_yield=CrossAssetInput("HYG", -0.05, False, False),
        investment_grade=CrossAssetInput("LQD", -0.01, False, False),
        small_caps=CrossAssetInput("IWM", -0.07, False, False),
        growth=CrossAssetInput("QQQ", 0.01, True, True),
        gold=CrossAssetInput("GLD", 0.08, True, True),
        equities=CrossAssetInput("SPY", -0.03, False, False),
    )

    assert regime.regime == "cross_asset_risk_off"
    assert regime.risk_off_score > regime.risk_on_score
    assert "strong_usd_pressure" in regime.warnings
    assert "duration_rate_stress" in regime.warnings


def test_cross_asset_risk_on_detects_supportive_environment():
    regime = evaluate_cross_asset_regime(
        dollar=CrossAssetInput("UUP", -0.02, False, False),
        long_bonds=CrossAssetInput("TLT", 0.03, True, True),
        high_yield=CrossAssetInput("HYG", 0.05, True, True),
        investment_grade=CrossAssetInput("LQD", 0.01, True, True),
        small_caps=CrossAssetInput("IWM", 0.06, True, True),
        growth=CrossAssetInput("QQQ", 0.03, True, True),
        gold=CrossAssetInput("GLD", -0.03, False, False),
        equities=CrossAssetInput("SPY", 0.05, True, True),
    )

    assert regime.regime == "cross_asset_risk_on"
    assert regime.risk_on_score > regime.risk_off_score
    assert "credit_risk_appetite_supportive" in regime.confirmations
    assert "equity_trend_supportive" in regime.confirmations
