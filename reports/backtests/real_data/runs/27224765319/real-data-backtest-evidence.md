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
- Stop hit rate: 45.83%
- Target 1 hit rate: 45.83%
- Target 2 hit rate: 29.17%
- False breakout rate: 50.00%
- Average R: 0.4898
- Expectancy R: 0.4898

## Rejected Trade Plans

No rejected trade plans.

## Results

| Signal | Symbol | Date | Outcome | R | Reason |
|---|---|---:|---|---:|---|
| hist_AAPL_c71a612fbdc3e7c9 | AAPL | 2024-06-21 | TARGET_2_HIT | 3.0000 | target_2_hit |
| hist_AAPL_42f38c8cd6b5b1ac | AAPL | 2024-12-05 | TARGET_2_HIT | 3.0000 | target_2_hit |
| hist_AAPL_ae0dea559ffba888 | AAPL | 2025-08-19 | EXPIRED | 0.8705 | no_exit_level_hit |
| hist_GLD_06be4dedfdece401 | GLD | 2024-03-28 | TARGET_2_HIT | 2.2802 | target_2_hit |
| hist_GLD_802acd359b8a62e4 | GLD | 2024-09-13 | EXPIRED | 0.9052 | no_exit_level_hit |
| hist_GLD_4dfa5acf9ed115dc | GLD | 2025-03-04 | TARGET_2_HIT | 3.0000 | target_2_hit |
| hist_META_2fb35123392bfbfb | META | 2024-03-28 | STOP_HIT | -1.0000 | stop_hit |
| hist_META_72388f9905871a66 | META | 2024-09-13 | TARGET_2_HIT | 3.0000 | target_2_hit |
| hist_META_6efb3a3436c4ee69 | META | 2024-12-05 | STOP_HIT | -1.0000 | stop_hit |
| hist_MSFT_95f558162912119f | MSFT | 2024-03-28 | STOP_HIT | -1.0000 | stop_hit |
| hist_MSFT_02cebfd376d81531 | MSFT | 2024-06-21 | STOP_HIT | -1.2993 | stop_hit |
| hist_MSFT_95bd33a9c9108992 | MSFT | 2024-09-13 | STOP_HIT | -1.0000 | stop_hit |
| hist_MU_fa92f04dbdc79618 | MU | 2024-03-28 | STOP_HIT | -1.0000 | stop_hit |
| hist_MU_00b111b03e4d027d | MU | 2024-06-21 | STOP_HIT | -1.0000 | stop_hit |
| hist_MU_dc1f013ce5c74066 | MU | 2025-08-19 | TARGET_2_HIT | 3.0000 | target_2_hit |
| hist_NVDA_b227181e5ede3f9c | NVDA | 2024-03-28 | STOP_HIT | -1.0000 | stop_hit |
| hist_NVDA_2ef7d4e70a2d4204 | NVDA | 2024-06-21 | EXPIRED | -0.3356 | no_exit_level_hit |
| hist_NVDA_072f428f0e72e1ad | NVDA | 2024-09-13 | EXPIRED | 1.9083 | expired_after_target_1_without_target_2 |
| hist_QQQ_74d2c1aae53e8e13 | QQQ | 2024-03-28 | EXPIRED | 0.0000 | entry_not_hit |
| hist_QQQ_d664986f14290dac | QQQ | 2024-06-21 | STOP_HIT | -1.0000 | stop_hit |
| hist_QQQ_9e573f59bab9a84c | QQQ | 2024-09-13 | EXPIRED | 0.8093 | no_exit_level_hit |
| hist_SLV_83a2f6f0c59b7da7 | SLV | 2024-03-28 | TARGET_2_HIT | 1.7389 | target_2_hit |
| hist_SLV_d834042925731b9b | SLV | 2024-06-21 | STOP_HIT | -1.1231 | stop_hit |
| hist_SLV_b48496e6dfbc4a19 | SLV | 2024-09-13 | STOP_HIT | -1.0000 | same_bar_stop_first |
