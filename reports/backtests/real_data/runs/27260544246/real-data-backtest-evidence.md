# Historical Entry / Stop / Exit Backtest

## Evidence Pack

- Run ID: bt131-real-data-manual
- Data source: real_data
- Is demo: False
- Strategy version: historical-entry-exit-v1
- Input pack gate status: PASSED
- Input completeness status: OK
- Run health status: OK
- Coverage manifest: data/historical/metadata/coverage_manifest.json
- Survivorship universe: data/historical/metadata/bt131_runtime_universe.csv
- Trade plans: data/trade_plans/historical_trade_plans.json
- Input plans: 24
- Accepted plans: 24
- Rejected plans: 0
- Live trading authorized: False
- Broker execution mode: paper_only

## Metrics

- Total plans: 24
- Entry hit rate: 95.83%
- Expired without entry rate: 4.17%
- Stop hit rate: 50.00%
- Target 1 hit rate: 45.83%
- Target 2 hit rate: 25.00%
- False breakout rate: 50.00%
- Average R: 0.2763
- Expectancy R: 0.2763

## Rejected Trade Plans

No rejected trade plans.

## Results

| Signal | Symbol | Date | Outcome | R | Reason |
|---|---|---:|---|---:|---|
| hist_AAPL_ee1d13960990009b | AAPL | 2024-06-24 | TARGET_2_HIT | 3.0000 | target_2_hit |
| hist_AAPL_c7e18fc5dc59757a | AAPL | 2024-12-10 | STOP_HIT | -1.0000 | stop_hit |
| hist_AAPL_0cecb065d8318414 | AAPL | 2025-11-19 | EXPIRED | 0.1379 | expired_after_target_1_without_target_2 |
| hist_GLD_06be4dedfdece401 | GLD | 2024-03-28 | TARGET_2_HIT | 2.2802 | target_2_hit |
| hist_GLD_28d45cd3b8547165 | GLD | 2024-09-17 | EXPIRED | 1.3075 | no_exit_level_hit |
| hist_GLD_660f05be20c28798 | GLD | 2024-12-10 | STOP_HIT | -1.0873 | stop_hit |
| hist_META_2fb35123392bfbfb | META | 2024-03-28 | STOP_HIT | -1.0000 | stop_hit |
| hist_META_8010f0684d49c7c6 | META | 2024-09-17 | TARGET_2_HIT | 3.0000 | target_2_hit |
| hist_META_b215a7749494a8f2 | META | 2024-12-10 | STOP_HIT | -1.0000 | stop_hit |
| hist_MSFT_95f558162912119f | MSFT | 2024-03-28 | STOP_HIT | -1.0000 | stop_hit |
| hist_MSFT_5af359349d977127 | MSFT | 2024-06-24 | STOP_HIT | -1.0674 | stop_hit |
| hist_MSFT_22b4a6dd62e2670e | MSFT | 2024-09-17 | STOP_HIT | -1.0000 | stop_hit |
| hist_MU_fa92f04dbdc79618 | MU | 2024-03-28 | STOP_HIT | -1.0000 | stop_hit |
| hist_MU_7f56c7438fa2c834 | MU | 2024-06-24 | STOP_HIT | -1.0000 | stop_hit |
| hist_MU_9885e2b08fd8189f | MU | 2025-06-03 | TARGET_2_HIT | 3.0000 | target_2_hit |
| hist_NVDA_b227181e5ede3f9c | NVDA | 2024-03-28 | STOP_HIT | -1.0000 | stop_hit |
| hist_NVDA_7759b4f0c67a7da8 | NVDA | 2024-06-24 | EXPIRED | 0.0926 | no_exit_level_hit |
| hist_NVDA_c0b97b01956a0c74 | NVDA | 2025-06-03 | TARGET_2_HIT | 3.0000 | target_2_hit |
| hist_QQQ_74d2c1aae53e8e13 | QQQ | 2024-03-28 | EXPIRED | 0.0000 | entry_not_hit |
| hist_QQQ_7988a00265c0e355 | QQQ | 2024-06-24 | EXPIRED | 0.2026 | expired_after_target_1_without_target_2 |
| hist_QQQ_8e7aec5eaf6791d8 | QQQ | 2024-09-17 | EXPIRED | 1.1993 | no_exit_level_hit |
| hist_SLV_83a2f6f0c59b7da7 | SLV | 2024-03-28 | TARGET_2_HIT | 1.7389 | target_2_hit |
| hist_SLV_62aa0bac96783405 | SLV | 2024-06-24 | STOP_HIT | -1.1726 | stop_hit |
| hist_SLV_6e562d42e12f1da0 | SLV | 2024-09-17 | STOP_HIT | -1.0000 | same_bar_stop_first |
