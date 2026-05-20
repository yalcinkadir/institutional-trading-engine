from src.bridge.scanner_market_snapshot_builder import (
    scanner_market_snapshot_builder,
)
from src.bridge.scanner_to_orchestrator import (
    scanner_to_orchestrator_bridge,
)
from src.runtime.runtime_state import runtime_state


class LiveRuntimeCycle:
    def run_cycle(self, metrics_map):
        snapshot = scanner_market_snapshot_builder.build(metrics_map)

        orchestrator_inputs = (
            scanner_to_orchestrator_bridge.build_inputs(snapshot)
        )

        decision = {
            "market_regime_score": orchestrator_inputs.market_regime_score,
            "volatility_level": orchestrator_inputs.volatility_level,
            "equity_strength": orchestrator_inputs.equity_strength,
        }

        runtime_state.update(decision)

        return {
            "snapshot": snapshot.to_persistence_payload(),
            "decision": decision,
        }


live_runtime_cycle = LiveRuntimeCycle()
