from src.setup_scoring import calculate_asymmetry_score, score_setup


def _bars(start=100.0, drift=0.4, volume=1_000_000, count=240):
    bars = []
    close = start

    for index in range(count):
        close += drift
        bars.append(
            {
                "c": round(close, 2),
                "h": round(close + 1.5, 2),
                "l": round(close - 1.5, 2),
                "v": volume + (index * 1000),
            }
        )

    return bars


def test_score_setup_detects_strong_trend_and_positive_relative_strength():
    asset = _bars(drift=0.9)
    benchmark = _bars(drift=0.3)

    result = score_setup("NVDA", asset, benchmark)

    assert result.setup_score > 65
    assert result.regime_alignment > 0.6
    assert result.relative_strength_20d > 0
    assert result.trend_quality > 0.7
    assert result.data_confidence > 0.9
    assert "strong_trend_structure" in result.notes
    assert "outperforming_benchmark_20d" in result.notes


def test_score_setup_flags_weak_asymmetry_when_price_is_extended_near_recent_high():
    asset = _bars(drift=0.9)
    benchmark = _bars(drift=0.3)

    result = score_setup("NVDA", asset, benchmark)

    assert result.asymmetry_score == 0.0
    assert "weak_asymmetry" in result.notes


def test_asymmetry_uses_absolute_downside_distance_below_sma50():
    downtrend_asset = _bars(start=250.0, drift=-0.5)

    asymmetry = calculate_asymmetry_score(downtrend_asset)

    assert asymmetry < 0.35


def test_score_setup_handles_insufficient_history():
    short_asset = _bars(count=20)
    short_benchmark = _bars(count=20)

    result = score_setup("TEST", short_asset, short_benchmark)

    assert result.setup_score == 0.0
    assert result.data_confidence == 0.0
    assert "insufficient_history" in result.notes


def test_ev11_missing_long_horizon_indicators_are_conservative_not_optimistic():
    asset = _bars(drift=0.9, count=120)
    benchmark = _bars(drift=0.3, count=120)

    result = score_setup("PARTIAL", asset, benchmark)

    assert result.trend_quality == 0.0
    assert result.asymmetry_score == 0.0
    assert result.data_confidence <= 0.5
    assert result.setup_score < 45
    assert result.regime_alignment <= 0.5
    assert "conservative_missing_long_horizon_trend" in result.notes
    assert "conservative_missing_long_horizon_asymmetry" in result.notes
    assert "weak_asymmetry" in result.notes


def test_ev11_invalid_close_values_do_not_create_optimistic_scores():
    asset = _bars(drift=0.9, count=120)
    benchmark = _bars(drift=0.3, count=120)
    for index in range(0, len(asset), 10):
        asset[index]["c"] = "invalid"

    result = score_setup("BAD_CLOSES", asset, benchmark)

    assert result.trend_quality == 0.0
    assert result.asymmetry_score == 0.0
    assert result.data_confidence <= 0.5
    assert "missing_or_invalid_close_data" in result.notes
    assert "conservative_missing_long_horizon_trend" in result.notes
    assert "conservative_missing_long_horizon_asymmetry" in result.notes
