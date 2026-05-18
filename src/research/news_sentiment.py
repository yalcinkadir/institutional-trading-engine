from __future__ import annotations


def analyze_news_sentiment(articles: list[dict]) -> dict:
    if not articles:
        return {
            "article_count": 0,
            "sentiment_score": 0,
            "classification": "No Data",
        }

    score_map = {
        "positive": 1,
        "neutral": 0,
        "negative": -1,
    }

    total = sum(score_map.get(article.get("sentiment", "neutral"), 0) for article in articles)
    sentiment_score = round((total / len(articles)) * 100, 2)

    if sentiment_score >= 40:
        classification = "Positive News Flow"
    elif sentiment_score <= -40:
        classification = "Negative News Flow"
    else:
        classification = "Neutral News Flow"

    return {
        "article_count": len(articles),
        "sentiment_score": sentiment_score,
        "classification": classification,
    }
