from src.execution.entry_timing import evaluate_entry_timing
from src.execution.liquidity_engine import evaluate_liquidity
from src.execution.slippage_model import estimate_slippage
from src.execution.volatility_filter import evaluate_volatility_filter


def test_liquidity_engine():
    result = evaluate_liquidity(
        average_volume=2_000_000,
        dollar_volume=120_000_000,
    )

    assert result["liquidity_score"] == 100
    assert result["classification"] == "Institutional Liquidity"


def test_slippage_model():
    result = estimate_slippage(
        spread_percent=0.1,
        volatility_percent=0.5,
        order_size_percent_of_volume=0.2,
    )

    assert result["estimated_slippage_percent"] < 1
    assert result["classification"] in {"Low", "Moderate"}


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
