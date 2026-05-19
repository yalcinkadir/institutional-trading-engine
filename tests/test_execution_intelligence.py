from src.execution.entry_timing import evaluate_entry_timing
from src.execution.liquidity_engine import evaluate_liquidity
from src.execution.liquidity_intelligence import (
    LiquidityInputs,
    LiquidityIntelligence,
)
from src.execution.slippage_model import SlippageModel
from src.execution.volatility_filter import evaluate_volatility_filter


def test_liquidity_engine():
    result = evaluate_liquidity(
        average_volume=2_000_000,
        dollar_volume=120_000_000,
    )

    assert result["liquidity_score"] == 100
    assert result["classification"] == "Institutional Liquidity"


def test_advanced_liquidity_intelligence():
    intelligence = LiquidityIntelligence()

    result = intelligence.evaluate(
        LiquidityInputs(
            average_daily_volume_millions=2,
            bid_ask_spread_percent=1.5,
            volatility_percent=8,
            order_size_percent_adv=15,
        )
    )

    assert result.execution_risk == "high"
    assert result.recommended_execution_style == "passive"


def test_slippage_model():
    model = SlippageModel()

    result = model.estimate(
        volatility_percent=10,
        spread_percent=1.2,
        order_size_percent_adv=8,
    )

    assert result.execution_quality == "poor"


def test_entry_timing_engine():
    result = evaluate_entry_timing(
        minutes_after_open=45,
        relative_volume=1.5,
        volatility_percent=2,
    )

    assert result["timing_score"] >= 80
    assert result["classification"] == "Optimal"


def test_volatility_filter():
    result = evaluate_volatility_filter(
        atr_percent=3,
        vix=15,
    )

    assert result["volatility_score"] >= 80
    assert result["classification"] == "Stable"
