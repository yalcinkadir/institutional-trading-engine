# BT139 BT131 Sample Expansion Report

## Executive Summary

- Evidence quality: INSUFFICIENT_SAMPLE
- Promotion allowed: False
- Trade count: 24
- Symbol count: 8
- Setup count: 1
- Signal-day count: 6
- Signal-day cluster count: 5
- Max cluster size: 7
- Sample window: 2024-03-28 to 2025-11-19
- Broker execution mode: paper_only
- Live trading authorized: False
- Production rule change allowed: False

## Promotion Block Reasons

- trade_count=24 below early_min_trade_count=50
- sample quality below REVIEWABLE_SAMPLE

## Symbol Coverage

| Symbol | Trade Count |
|---|---|
| AAPL | 3 |
| GLD | 3 |
| META | 3 |
| MSFT | 3 |
| MU | 3 |
| NVDA | 3 |
| QQQ | 3 |
| SLV | 3 |

## Setup Coverage

| Setup | Trade Count |
|---|---|
| historical_pullback_continuation | 24 |

## Asset Group Coverage

| Asset Group | Trade Count |
|---|---|
| index_etf | 3 |
| mega_cap_tech | 9 |
| metals_etf | 6 |
| semiconductor_or_hardware | 6 |

## Market Regime Coverage

| Regime | Trade Count |
|---|---|
| UNKNOWN | 24 |

## Concentrated Signal Days

| Signal Date | Cluster Size | Symbols | Outcomes |
|---|---|---|---|
| 2024-03-28 | 7 | GLD, META, MSFT, MU, NVDA, QQQ, SLV | {"EXPIRED": 1, "STOP_HIT": 4, "TARGET_2_HIT": 2} |
| 2024-06-24 | 6 | AAPL, MSFT, MU, NVDA, QQQ, SLV | {"EXPIRED": 2, "STOP_HIT": 3, "TARGET_2_HIT": 1} |
| 2024-09-17 | 5 | GLD, META, MSFT, QQQ, SLV | {"EXPIRED": 2, "STOP_HIT": 2, "TARGET_2_HIT": 1} |
| 2024-12-10 | 3 | AAPL, GLD, META | {"STOP_HIT": 3} |
| 2025-06-03 | 2 | MU, NVDA | {"TARGET_2_HIT": 2} |

## Missing Field Reasons

| Field | Example Missing Signal IDs |
|---|---|
| entry_price | hist_QQQ_74d2c1aae53e8e13 |
| max_adverse_excursion_r | hist_QQQ_74d2c1aae53e8e13 |
| max_favorable_excursion_r | hist_QQQ_74d2c1aae53e8e13 |
| atr14_at_signal | hist_AAPL_ee1d13960990009b, hist_AAPL_c7e18fc5dc59757a, hist_AAPL_0cecb065d8318414, hist_GLD_06be4dedfdece401, hist_GLD_28d45cd3b8547165, hist_GLD_660f05be20c28798, hist_META_2fb35123392bfbfb, hist_META_8010f0684d49c7c6, hist_META_b215a7749494a8f2, hist_MSFT_95f558162912119f, hist_MSFT_5af359349d977127, hist_MSFT_22b4a6dd62e2670e, hist_MU_fa92f04dbdc79618, hist_MU_7f56c7438fa2c834, hist_MU_9885e2b08fd8189f, hist_NVDA_b227181e5ede3f9c, hist_NVDA_7759b4f0c67a7da8, hist_NVDA_c0b97b01956a0c74, hist_QQQ_74d2c1aae53e8e13, hist_QQQ_7988a00265c0e355, hist_QQQ_8e7aec5eaf6791d8, hist_SLV_83a2f6f0c59b7da7, hist_SLV_62aa0bac96783405, hist_SLV_6e562d42e12f1da0 |
| volume | hist_AAPL_ee1d13960990009b, hist_AAPL_c7e18fc5dc59757a, hist_AAPL_0cecb065d8318414, hist_GLD_06be4dedfdece401, hist_GLD_28d45cd3b8547165, hist_GLD_660f05be20c28798, hist_META_2fb35123392bfbfb, hist_META_8010f0684d49c7c6, hist_META_b215a7749494a8f2, hist_MSFT_95f558162912119f, hist_MSFT_5af359349d977127, hist_MSFT_22b4a6dd62e2670e, hist_MU_fa92f04dbdc79618, hist_MU_7f56c7438fa2c834, hist_MU_9885e2b08fd8189f, hist_NVDA_b227181e5ede3f9c, hist_NVDA_7759b4f0c67a7da8, hist_NVDA_c0b97b01956a0c74, hist_QQQ_74d2c1aae53e8e13, hist_QQQ_7988a00265c0e355, hist_QQQ_8e7aec5eaf6791d8, hist_SLV_83a2f6f0c59b7da7, hist_SLV_62aa0bac96783405, hist_SLV_6e562d42e12f1da0 |
| avg_volume_20 | hist_AAPL_ee1d13960990009b, hist_AAPL_c7e18fc5dc59757a, hist_AAPL_0cecb065d8318414, hist_GLD_06be4dedfdece401, hist_GLD_28d45cd3b8547165, hist_GLD_660f05be20c28798, hist_META_2fb35123392bfbfb, hist_META_8010f0684d49c7c6, hist_META_b215a7749494a8f2, hist_MSFT_95f558162912119f, hist_MSFT_5af359349d977127, hist_MSFT_22b4a6dd62e2670e, hist_MU_fa92f04dbdc79618, hist_MU_7f56c7438fa2c834, hist_MU_9885e2b08fd8189f, hist_NVDA_b227181e5ede3f9c, hist_NVDA_7759b4f0c67a7da8, hist_NVDA_c0b97b01956a0c74, hist_QQQ_74d2c1aae53e8e13, hist_QQQ_7988a00265c0e355, hist_QQQ_8e7aec5eaf6791d8, hist_SLV_83a2f6f0c59b7da7, hist_SLV_62aa0bac96783405, hist_SLV_6e562d42e12f1da0 |
| market_regime | hist_AAPL_ee1d13960990009b, hist_AAPL_c7e18fc5dc59757a, hist_AAPL_0cecb065d8318414, hist_GLD_06be4dedfdece401, hist_GLD_28d45cd3b8547165, hist_GLD_660f05be20c28798, hist_META_2fb35123392bfbfb, hist_META_8010f0684d49c7c6, hist_META_b215a7749494a8f2, hist_MSFT_95f558162912119f, hist_MSFT_5af359349d977127, hist_MSFT_22b4a6dd62e2670e, hist_MU_fa92f04dbdc79618, hist_MU_7f56c7438fa2c834, hist_MU_9885e2b08fd8189f, hist_NVDA_b227181e5ede3f9c, hist_NVDA_7759b4f0c67a7da8, hist_NVDA_c0b97b01956a0c74, hist_QQQ_74d2c1aae53e8e13, hist_QQQ_7988a00265c0e355, hist_QQQ_8e7aec5eaf6791d8, hist_SLV_83a2f6f0c59b7da7, hist_SLV_62aa0bac96783405, hist_SLV_6e562d42e12f1da0 |
| asset_group | hist_AAPL_ee1d13960990009b, hist_AAPL_c7e18fc5dc59757a, hist_AAPL_0cecb065d8318414, hist_GLD_06be4dedfdece401, hist_GLD_28d45cd3b8547165, hist_GLD_660f05be20c28798, hist_META_2fb35123392bfbfb, hist_META_8010f0684d49c7c6, hist_META_b215a7749494a8f2, hist_MSFT_95f558162912119f, hist_MSFT_5af359349d977127, hist_MSFT_22b4a6dd62e2670e, hist_MU_fa92f04dbdc79618, hist_MU_7f56c7438fa2c834, hist_MU_9885e2b08fd8189f, hist_NVDA_b227181e5ede3f9c, hist_NVDA_7759b4f0c67a7da8, hist_NVDA_c0b97b01956a0c74, hist_QQQ_74d2c1aae53e8e13, hist_QQQ_7988a00265c0e355, hist_QQQ_8e7aec5eaf6791d8, hist_SLV_83a2f6f0c59b7da7, hist_SLV_62aa0bac96783405, hist_SLV_6e562d42e12f1da0 |

## Safety Notes

- BT139 is evidence-expansion only and does not modify production trading rules.
- No live trading authorization.
- broker_execution_mode remains paper_only.
- Downstream strategy variants remain blocked below REVIEWABLE_SAMPLE.
