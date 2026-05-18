from __future__ import annotations


class MarketHealthScore:
    def __init__(
        self,
        spy_above_sma50: bool,
        spy_above_sma200: bool,
        qqq_above_sma50: bool,
        qqq_above_sma200: bool,
        vix: float,
        breadth_percent: float,
    ) -> None:
        self.spy_above_sma50 = spy_above_sma50
        self.spy_above_sma200 = spy_above_sma200
        self.qqq_above_sma50 = qqq_above_sma50
        self.qqq_above_sma200 = qqq_above_sma200
        self.vix = vix
        self.breadth_percent = breadth_percent

    def calculate(self) -> dict:
        score = 0

        trend_points = sum([
            self.spy_above_sma50,
            self.spy_above_sma200,
            self.qqq_above_sma50,
            self.qqq_above_sma200,
        ]) * 15

        score += trend_points

        if self.vix < 15:
            score += 25
        elif self.vix < 20:
            score += 15
        elif self.vix < 25:
            score += 5

        if self.breadth_percent >= 70:
            score += 15
        elif self.breadth_percent >= 50:
            score += 10
        elif self.breadth_percent >= 35:
            score += 5

        score = min(score, 100)

        if score >= 80:
            regime = "Strong Bullish"
        elif score >= 65:
            regime = "Bullish"
        elif score >= 45:
            regime = "Neutral"
        elif score >= 30:
            regime = "Defensive"
        else:
            regime = "Risk-Off"

        return {
            "score": score,
            "regime": regime,
        }
