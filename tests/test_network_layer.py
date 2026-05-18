from src.network.agent_coordination import coordinate_agents
from src.network.consensus_engine import build_consensus
from src.network.distributed_analysis import combine_distributed_analysis
from src.network.intelligence_sharing import share_intelligence


def test_agent_coordination():
    result = coordinate_agents(
        agents=[
            {
                "name": "macro_agent",
                "role": "macro",
                "capabilities": ["macro", "risk"],
            },
            {
                "name": "research_agent",
                "role": "research",
                "capabilities": ["research", "general"],
            },
        ],
        task="research",
    )

    assert result["assigned_count"] >= 1


def test_consensus_engine():
    result = build_consensus(
        ["bullish", "bullish", "neutral"]
    )

    assert result["consensus"] == "Bullish Consensus"
    assert result["confidence"] > 60


def test_distributed_analysis():
    result = combine_distributed_analysis(
        [
            {"score": 90},
            {"score": 70},
            {"score": 80},
        ]
    )

    assert result["average_score"] == 80
    assert result["classification"] == "Strong Opportunity"


def test_intelligence_sharing():
    result = share_intelligence(
        sender="macro_agent",
        receivers=["risk_agent", "execution_agent"],
        payload={"regime": "Bullish", "vix": 15},
    )

    assert result["transmission_count"] == 2
