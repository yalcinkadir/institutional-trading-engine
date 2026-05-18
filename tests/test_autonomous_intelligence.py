from src.autonomy.regime_forecasting import forecast_regime_shift
from src.autonomy.risk_adaptation import adapt_risk_profile
from src.autonomy.scenario_engine import build_market_scenarios
from src.autonomy.watchlist_planner import build_dynamic_watchlist


def test_market_scenarios():
    result = build_market_scenarios(
        market_regime="Bullish",
        vix=14,
        breadth_percent=72,
    )

    assert result["scenario_count"] >= 1


def test_regime_forecast():
    result = forecast_regime_shift(
        current_regime="Bullish",
        vix_trend="rising",
        breadth_trend="weakening",
    )

    assert result["forecast_regime"] in {"Neutral", "Defensive"}


def test_watchlist_planner():
    result = build_dynamic_watchlist(
        leaders=[{"ticker": "NVDA"}],
        weak_names=[{"ticker": "INTC"}],
        market_regime="Bullish",
    )

    assert result["focus"] == "aggressive_growth"


def test_risk_adaptation():
    result = adapt_risk_profile(
        market_regime="Risk-Off",
        vix=30,
        portfolio_correlation=0.9,
    )

    assert result["risk_multiplier"] < 1
    assert result["profile"] == "Defensive"
