from dataclasses import dataclass

from src.runtime.runtime_market_snapshot import RuntimeMarketSnapshot


@dataclass(frozen=True)
class InstitutionalDecisionInputs:
    market_regime_score: float
    volatility_level: float
    equity_strength: float


class ScannerToOrchestratorBridge:
    def build_inputs(self, snapshot: RuntimeMarketSnapshot):
        spy_rsi = snapshot.spy_metrics.get("rsi14", 50)
        qqq_rsi = snapshot.qqq_metrics.get("rsi14", 50)

        market_regime_score = round((spy_rsi + qqq_rsi) / 2, 2)

        volatility_level = snapshot.volatility_metrics.get("vix") or 20.0

        equity_strength = round(
            (spy_rsi * 0.5) + (qqq_rsi * 0.5),
            2,
        )

        return InstitutionalDecisionInputs(
            market_regime_score=market_regime_score,
            volatility_level=volatility_level,
            equity_strength=equity_strength,
        )


scanner_to_orchestrator_bridge = ScannerToOrchestratorBridge()
