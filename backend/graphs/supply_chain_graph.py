"""
Supply Chain Monitoring LangGraph.

Defines the complete workflow for the Autonomous Supply Chain
Disruption Monitoring System.
"""

from __future__ import annotations

from langgraph.graph import END, START, StateGraph

from backend.nodes.executive_node import executive_node
from backend.nodes.filter_node import filter_node
from backend.nodes.impact_node import impact_node
from backend.nodes.mitigation_node import mitigation_node
from backend.nodes.news_node import news_node
from backend.nodes.risk_node import risk_node
from backend.graphs.state import SupplyChainState


def build_supply_chain_graph():
    """
    Build and compile the Supply Chain Monitoring workflow.

    Workflow
    --------

    START
      │
      ▼
    News Node
      │
      ▼
    Filter Node
      │
      ▼
    Risk Classification Node
      │
      ▼
    Supply Chain Impact Node
      │
      ▼
    Mitigation Planning Node
      │
      ▼
    Executive Summary Node
      │
      ▼
     END
    """

    workflow = StateGraph(SupplyChainState)

    # Register Nodes
    workflow.add_node("news", news_node)
    workflow.add_node("filter", filter_node)
    workflow.add_node("risk", risk_node)
    workflow.add_node("impact", impact_node)
    workflow.add_node("mitigation", mitigation_node)
    workflow.add_node("executive", executive_node)

    # Define Workflow
    workflow.add_edge(START, "news")
    workflow.add_edge("news", "filter")
    workflow.add_edge("filter", "risk")
    workflow.add_edge("risk", "impact")
    workflow.add_edge("impact", "mitigation")
    workflow.add_edge("mitigation", "executive")
    workflow.add_edge("executive", END)

    return workflow.compile()


# Compiled graph instance
supply_chain_graph = build_supply_chain_graph()