def setup_readiness_label(metrics):
    if not metrics:
        return "N/A"

    trend = metrics["trend"]
    rsi = metrics["rsi14"]
    atr_pct = metrics["atr_pct"]
    rs_spread = metrics["rs_spread"]
    rvol = metrics["rvol"]
    close = metrics["close"]
    sma20 = metrics["sma20"]
    sma50 = metrics["sma50"]

    if trend in ["Mixed", "Downtrend"] or metrics["rs_label"] == "Weak":
        return "Weak - Avoid"

    if pd.notna(atr_pct) and atr_pct > 5:
        return "High Volatility Caution"

    near_sma20 = pd.notna(sma20) and abs((close - sma20) / sma20) <= 0.03
    near_sma50 = pd.notna(sma50) and abs((close - sma50) / sma50) <= 0.03

    if (
        trend in ["Strong Uptrend", "Uptrend"]
        and pd.notna(rsi) and 45 <= rsi <= 65
        and pd.notna(rs_spread) and rs_spread >= -2
        and (near_sma20 or near_sma50)
    ):
        return "Pullback Candidate"

    if (
        trend in ["Strong Uptrend", "Uptrend"]
        and pd.notna(rsi) and 52 <= rsi <= 68
        and pd.notna(rs_spread) and rs_spread >= 0
        and pd.notna(rvol) and rvol >= 1.0
    ):
        return "Breakout Watch"

    if (
        trend == "Strong Uptrend"
        and pd.notna(rsi) and 65 < rsi < 70
        and pd.notna(rs_spread) and rs_spread >= 0
        and pd.notna(rvol) and rvol >= 0.9
    ):
        return "Trend Strong, Entry Unclear"

    if trend in ["Strong Uptrend", "Uptrend"] and pd.notna(rsi) and rsi >= 70:
        return "Extended - Avoid Chase"

    return "Not Ready"
