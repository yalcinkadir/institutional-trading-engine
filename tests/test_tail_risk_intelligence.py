from src.risk.portfolio_stress_testing import (
    PortfolioStressTester,
    StressScenario,
)
from src.risk.tail_risk_engine import (
    TailRiskEngine,
    TailRiskInputs,
)


def test_tail_risk_crisis_regime():
    engine = TailRiskEngine()

    result = engine.assess(
        TailRiskInputs(
            vix_level=40,
            gap_risk_percent=70,
            liquidity_stress_percent=80,
            correlation_risk_percent=75,
            event_risk_percent=60,
        )
    )

    assert result.regime in ["crisis", "panic"]
    assert result.exposure_multiplier <= 0.35


def test_portfolio_stress_testing():
    tester = PortfolioStressTester()

    result = tester.simulate(
        portfolio_beta=1.3,
        scenario=StressScenario(
            market_drop_percent=20,
            volatility_spike_percent=60,
            correlation_breakdown_percent=80,
        ),
    )

    assert result.projected_drawdown_percent > 20
    assert result.projected_portfolio_stress in ["high", "severe"]
