"""
test_knowledge_graph_agent.py

Tests for the Knowledge Graph Agent, run against the REAL data files
in backend/data/ (not mocked), since this agent's whole job is to
correctly represent that real data as a graph.
"""

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from backend.agents.knowledge_graph_agent import KnowledgeGraphAgent


def _build_agent() -> KnowledgeGraphAgent:
    return KnowledgeGraphAgent()


# -----------------------------------------------------------------------
# Graph construction
# -----------------------------------------------------------------------
def test_graph_builds_expected_node_counts():
    agent = _build_agent()
    summary = agent.summary()

    assert summary["node_counts"]["plant"] == 3
    assert summary["node_counts"]["supplier"] == 5
    assert summary["node_counts"]["warehouse"] == 3
    assert summary["node_counts"]["distribution_center"] == 3
    assert summary["node_counts"]["material"] == 6
    assert summary["total_nodes"] == 20


def test_graph_has_edges():
    agent = _build_agent()
    summary = agent.summary()
    assert summary["total_edges"] > 0
