"""
LangGraph Executive Summary Node.

This node generates executive-level summaries for the processed
news articles and stores the results in the workflow state.
"""

from __future__ import annotations

import logging

from backend.agents.executive_summary_agent import (
    executive_summary_agent,
)
from backend.graphs.state import SupplyChainState
from backend.models.agent_contracts import (
    ExecutiveSummaryAgentInput,
)

logger = logging.getLogger(__name__)


def executive_node(
    state: SupplyChainState,
) -> SupplyChainState:
    """
    Generate executive summaries.

    Workflow
    --------
    StructuredNews
            ↓
    ExecutiveSummaryAgent
            ↓
    ExecutiveSummaryAgentOutput
            ↓
    Updated State
    """

    logger.info("Executing Executive Summary Node.")

    structured_news = state.get("filtered_news")

    if structured_news is None or not structured_news.articles:
        logger.warning(
            "No structured news available for executive summary generation."
        )

        return {
            **state,
            "executive_summary": None,
        }

    try:
        agent_input = ExecutiveSummaryAgentInput(
            articles=structured_news.articles,
        )

        summary = executive_summary_agent.generate(
            agent_input
        )

        logger.info(
            "Generated %d executive summaries.",
            len(summary.summaries),
        )

        return {
            **state,
            "executive_summary": summary,
        }

    except Exception:
        logger.exception(
            "Executive Summary Node execution failed."
        )

        return {
            **state,
            "executive_summary": None,
        }