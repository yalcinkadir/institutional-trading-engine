from src.runtime.runtime_market_snapshot import RuntimeMarketSnapshot


class ScannerMarketSnapshotBuilder:
    def build(self, metrics_map):
        spy_metrics = metrics_map.get("SPY", {})
        qqq_metrics = metrics_map.get("QQQ", {})

        return RuntimeMarketSnapshot.create(
            spy_metrics=spy_metrics,
            qqq_metrics=qqq_metrics,
            market_metrics={
                "symbols_scanned": len(metrics_map),
            },
            sector_metrics={},
            volatility_metrics={
                "vix": metrics_map.get("VIX", {}).get("close")
            },
        )


scanner_market_snapshot_builder = ScannerMarketSnapshotBuilder()
