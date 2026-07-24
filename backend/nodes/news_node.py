"""
LangGraph News Node.

This node is responsible for retrieving the latest supply chain news
using the NewsIntelligenceAgent and storing the results in the workflow state.
"""

from __future__ import annotations

import logging

from backend.agents.news_agent import news_agent
from backend.graphs.state import SupplyChainState

logger = logging.getLogger(__name__)


def news_node(state: SupplyChainState) -> SupplyChainState:
    """
    Retrieve the latest news articles and update the workflow state.

    Workflow:
        State
            ↓
        NewsIntelligenceAgent
            ↓
        NewsCollection
            ↓
        Updated State
    """

    logger.info("Executing News Node.")

    query = state.get(
        "query",
        "latest supply chain disruptions cement manufacturing",
    )

    try:
        search_results = news_agent.fetch_news(
            query=query,
            max_results=5,
        )

        logger.info(
            "Retrieved %d news articles.",
            len(search_results.results),
        )

        return {
            **state,
            "search_results": search_results,
        }

    except Exception:
        logger.exception(
            "News Node execution failed."
        )

        return {
            **state,
            "search_results": None,
        }