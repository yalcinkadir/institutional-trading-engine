from __future__ import annotations

from dataclasses import dataclass

from src.cross_asset.cross_asset_intelligence import (
    CrossAssetInputs,
    cross_asset_intelligence,
)
from src.decision.confidence_weighted_execution import confidence_weighted_execution
from src.decision.probabilistic_decision_engine import probabilistic_decision_engine
from src.execution.liquidity_intelligence import LiquidityInputs, liquidity_intelligence
from src.execution.slippage_model import SlippageModel
from src.fusion.multi_factor_fusion_engine import FusionInputs, multi_factor_fusion_engine
from src.macro.macro_regime_fusion import MacroRegimeInputs, macro_regime_fusion_engine
from src.portfolio.adaptive_portfolio_intelligence import (
    PortfolioExposure,
    adaptive_portfolio_intelligence,
)
from src.risk.tail_risk_engine import TailRiskInputs, tail_risk_engine


@dataclass(frozen=True)
class InstitutionalDecisionInputs:
    market_regime_score: float
    equity_strength: float
    bond_strength: float
    dollar_strength: float
    gold_strength: float
    volatility_level: float
    gap_risk_percent: float
    liquidity_stress_percent: float
    correlation_risk_percent: float
    event_risk_percent: float
    average_daily_volume_millions: float
    bid_ask_spread_percent: float
    order_size_percent_adv: float
    feature_alpha_score: float
    portfolio_sector_exposure_percent: float
    portfolio_volatility_exposure_percent: float
    portfolio_concentration_percent: float
    portfolio_correlation_percent: float


@dataclass(frozen=True)
class InstitutionalDecisionResult:
    macro_regime: str
    cross_asset_regime: str
    tail_risk_regime: str
    liquidity_risk: str
    fusion_classification: str
    probabilistic_classification: str
    execution_aggressiveness: str
    final_exposure_percent: float
    explanation: str


class InstitutionalDecisionOrchestrator:
    def evaluate(
        self,
        inputs: InstitutionalDecisionInputs,
    ) -> InstitutionalDecisionResult:
        cross_asset = cross_asset_intelligence.evaluate(
            CrossAssetInputs(
                equity_strength=inputs.equity_strength,
                bond_strength=inputs.bond_strength,
                dollar_strength=inputs.dollar_strength,
                gold_strength=inputs.gold_strength,
                volatility_level=inputs.volatility_level,
            )
        )

        tail_risk = tail_risk_engine.assess(
            TailRiskInputs(
                vix_level=inputs.volatility_level,
                gap_risk_percent=inputs.gap_risk_percent,
                liquidity_stress_percent=inputs.liquidity_stress_percent,
                correlation_risk_percent=inputs.correlation_risk_percent,
                event_risk_percent=inputs.event_risk_percent,
            )
        )

        liquidity = liquidity_intelligence.evaluate(
            LiquidityInputs(
                average_daily_volume_millions=inputs.average_daily_volume_millions,
                bid_ask_spread_percent=inputs.bid_ask_spread_percent,
                volatility_percent=inputs.volatility_level,
                order_size_percent_adv=inputs.order_size_percent_adv,
            )
        )

        portfolio = adaptive_portfolio_intelligence.evaluate(
            PortfolioExposure(
                sector_exposure_percent=inputs.portfolio_sector_exposure_percent,
                volatility_exposure_percent=inputs.portfolio_volatility_exposure_percent,
                concentration_percent=inputs.portfolio_concentration_percent,
                correlation_percent=inputs.portfolio_correlation_percent,
            )
        )

        macro = macro_regime_fusion_engine.evaluate(
            MacroRegimeInputs(
                market_regime_score=inputs.market_regime_score,
                cross_asset_score=cross_asset.cross_asset_score,
                tail_risk_score=tail_risk.tail_risk_score,
                liquidity_score=liquidity.liquidity_score,
                volatility_level=inputs.volatility_level,
            )
        )

        slippage = SlippageModel().estimate(
            volatility_percent=inputs.volatility_level,
            spread_percent=inputs.bid_ask_spread_percent,
            order_size_percent_adv=inputs.order_size_percent_adv,
        )

        execution_confidence = max(
            0.0,
            min(
                100.0,
                liquidity.liquidity_score - slippage.estimated_slippage_percent,
            ),
        )

        fusion = multi_factor_fusion_engine.evaluate(
            FusionInputs(
                regime_score=macro.macro_score,
                tail_risk_score=tail_risk.tail_risk_score,
                liquidity_score=liquidity.liquidity_score,
                feature_alpha_score=inputs.feature_alpha_score,
                portfolio_risk_score=portfolio.risk_score,
                execution_confidence=execution_confidence,
            )
        )

        probability = probabilistic_decision_engine.evaluate(
            signal_score=fusion.confidence,
            risk_score=max(tail_risk.tail_risk_score, portfolio.risk_score),
            regime_confidence=macro.macro_score,
        )

        execution_plan = confidence_weighted_execution.generate(probability)

        final_exposure = (
            execution_plan.exposure_percent
            * tail_risk.exposure_multiplier
            * portfolio.recommended_exposure_multiplier
        )

        explanation = (
            f"macro={macro.macro_regime}; "
            f"cross_asset={cross_asset.regime_alignment}; "
            f"tail_risk={tail_risk.regime}; "
            f"liquidity={liquidity.execution_risk}; "
            f"fusion={fusion.classification}; "
            f"probability={probability.classification}"
        )

        return InstitutionalDecisionResult(
            macro_regime=macro.macro_regime,
            cross_asset_regime=cross_asset.regime_alignment,
            tail_risk_regime=tail_risk.regime,
            liquidity_risk=liquidity.execution_risk,
            fusion_classification=fusion.classification,
            probabilistic_classification=probability.classification,
            execution_aggressiveness=execution_plan.execution_aggressiveness,
            final_exposure_percent=round(final_exposure, 2),
            explanation=explanation,
        )


institutional_decision_orchestrator = InstitutionalDecisionOrchestrator()
