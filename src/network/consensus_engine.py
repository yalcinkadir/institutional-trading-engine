from __future__ import annotations


def build_consensus(votes: list[str]) -> dict:
    bullish = votes.count("bullish")
    bearish = votes.count("bearish")
    neutral = votes.count("neutral")

    if bullish > bearish and bullish > neutral:
        consensus = "Bullish Consensus"
    elif bearish > bullish and bearish > neutral:
        consensus = "Bearish Consensus"
    else:
        consensus = "Neutral Consensus"

    total_votes = max(len(votes), 1)
    strongest = max(bullish, bearish, neutral)
    confidence = round((strongest / total_votes) * 100, 2)

    return {
        "consensus": consensus,
        "confidence": confidence,
        "vote_count": len(votes),
    }
