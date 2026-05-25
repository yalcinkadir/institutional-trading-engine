import pytest

from src.execution.slippage_model import SlippageConfig, SlippageModel, slippage_model


def test_square_root_impact_uses_regime_multiplier() -> None:
    model = SlippageModel()

    normal = model.estimate(
        volatility_percent=2.0,
        spread_percent=0.04,
        order_size_percent_adv=1.0,
        regime_label="neutral",
    )
    panic = model.estimate(
        volatility_percent=2.0,
        spread_percent=0.04,
        order_size_percent_adv=1.0,
        regime_label="panic_dislocation",
    )

    assert normal.market_impact_percent > 0
    assert panic.market_impact_percent > normal.market_impact_percent
    assert panic.estimated_slippage_percent > normal.estimated_slippage_percent
    assert panic.regime_multiplier == pytest.approx(3.5)


def test_spread_cost_is_separated_from_market_impact() -> None:
    model = SlippageModel()

    estimate = model.estimate(
        volatility_percent=2.0,
        spread_percent=0.04,
        order_size_percent_adv=0.0,
        regime_label="neutral",
    )

    assert estimate.spread_cost_percent == pytest.approx(0.03)
    assert estimate.market_impact_percent == 0.0
    assert estimate.estimated_slippage_percent == pytest.approx(0.03)
    assert estimate.execution_quality == "excellent"


def test_order_size_impact_is_square_root_not_linear() -> None:
    model = SlippageModel(SlippageConfig(spread_multiplier=0.0))

    one_percent_adv = model.estimate(
        volatility_percent=2.0,
        spread_percent=0.0,
        order_size_percent_adv=1.0,
        regime_label="normal",
    )
    four_percent_adv = model.estimate(
        volatility_percent=2.0,
        spread_percent=0.0,
        order_size_percent_adv=4.0,
        regime_label="normal",
    )

    assert four_percent_adv.market_impact_percent == pytest.approx(
        one_percent_adv.market_impact_percent * 2,
        rel=0.01,
    )


def test_unknown_regime_falls_back_to_neutral_multiplier() -> None:
    model = SlippageModel()

    unknown = model.estimate(
        volatility_percent=2.0,
        spread_percent=0.04,
        order_size_percent_adv=1.0,
        regime_label="unknown_regime",
    )
    neutral = model.estimate(
        volatility_percent=2.0,
        spread_percent=0.04,
        order_size_percent_adv=1.0,
        regime_label="neutral",
    )

    assert unknown.regime_multiplier == neutral.regime_multiplier
    assert unknown.estimated_slippage_percent == neutral.estimated_slippage_percent


def test_negative_inputs_are_clamped_to_zero() -> None:
    model = SlippageModel()

    estimate = model.estimate(
        volatility_percent=-2.0,
        spread_percent=-0.04,
        order_size_percent_adv=-1.0,
        regime_label="panic_dislocation",
    )

    assert estimate.estimated_slippage_percent == 0.0
    assert estimate.spread_cost_percent == 0.0
    assert estimate.market_impact_percent == 0.0
    assert estimate.execution_quality == "excellent"


def test_quality_thresholds_include_prohibitive_bucket() -> None:
    model = SlippageModel()

    estimate = model.estimate(
        volatility_percent=10.0,
        spread_percent=0.50,
        order_size_percent_adv=25.0,
        regime_label="panic_dislocation",
    )

    assert estimate.estimated_slippage_percent > 0.50
    assert estimate.execution_quality == "prohibitive"


def test_global_model_uses_current_version() -> None:
    estimate = slippage_model.estimate(
        volatility_percent=1.0,
        spread_percent=0.02,
        order_size_percent_adv=1.0,
    )

    assert estimate.model_version == "sqrt-impact-v1"
