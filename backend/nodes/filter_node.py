"""
LangGraph Filter Node.

This node filters and structures raw news articles using the
NewsFilterAgent and stores the processed output in the workflow state.
"""

from __future__ import annotations

import logging

from backend.agents.news_filter_agent import news_filter_agent
from backend.graphs.state import SupplyChainState

logger = logging.getLogger(__name__)


def filter_node(
    state: SupplyChainState,
) -> SupplyChainState:
    """
    Process raw news into structured articles for downstream AI agents.

    Workflow
    --------
    NewsCollection
            ↓
    NewsFilterAgent
            ↓
    StructuredNews
            ↓
    Updated State
    """

    logger.info("Executing Filter Node.")

    search_results = state.get("search_results")

    if search_results is None:
        logger.warning(
            "No search results found in workflow state."
        )

        return {
            **state,
            "filtered_news": None,
        }

    try:
        structured_news = (
            news_filter_agent.prepare_agent_input(
                search_results
            )
        )

        logger.info(
            "Prepared %d structured news articles.",
            structured_news.article_count,
        )

        return {
            **state,
            "filtered_news": structured_news,
        }

    except Exception:
        logger.exception(
            "Filter Node execution failed."
        )

        return {
            **state,
            "filtered_news": None,
        }   