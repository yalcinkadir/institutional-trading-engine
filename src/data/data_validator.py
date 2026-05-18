from __future__ import annotations


def validate_price_bars(bars: list[dict], min_bars: int = 50) -> dict:
    errors: list[str] = []
    warnings: list[str] = []

    if len(bars) < min_bars:
        errors.append("insufficient_bar_history")

    required_fields = {"o", "h", "l", "c", "v"}

    for index, bar in enumerate(bars):
        missing = required_fields - set(bar.keys())
        if missing:
            errors.append(f"bar_{index}_missing_fields:{','.join(sorted(missing))}")
            continue

        open_price = float(bar["o"])
        high = float(bar["h"])
        low = float(bar["l"])
        close = float(bar["c"])
        volume = float(bar["v"])

        if min(open_price, high, low, close) <= 0:
            errors.append(f"bar_{index}_non_positive_price")

        if high < low:
            errors.append(f"bar_{index}_high_below_low")

        if close > high or close < low:
            errors.append(f"bar_{index}_close_outside_range")

        if volume < 0:
            errors.append(f"bar_{index}_negative_volume")
        elif volume == 0:
            warnings.append(f"bar_{index}_zero_volume")

    return {
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "bar_count": len(bars),
    }
