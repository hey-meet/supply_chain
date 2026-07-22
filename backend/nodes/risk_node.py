"""
LangGraph Risk Node.

This node performs AI-powered risk classification on the filtered
news articles and stores the results in the workflow state.
"""

from __future__ import annotations

import logging

from backend.agents.risk_agent import RiskClassificationAgent
from backend.graphs.state import SupplyChainState
from backend.models.search import SearchResult

logger = logging.getLogger(__name__)

risk_agent = RiskClassificationAgent()


def risk_node(
    state: SupplyChainState,
) -> SupplyChainState:
    """
    Execute AI-powered risk classification.

    Workflow
    --------
    StructuredNews
            ↓
    RiskClassificationAgent
            ↓
    RiskAnalysis[]
            ↓
    Updated State
    """

    logger.info("Executing Risk Node.")

    structured_news = state.get("filtered_news")

    if structured_news is None:
        logger.warning(
            "No structured news available."
        )

        return {
            **state,
            "risk_analysis": [],
        }

    try:
        search_results = [
            SearchResult(
                title=article.title,
                content=article.content,
                url=article.url,
                published_date=article.published_date,
                score=article.search_score,
            )
            for article in structured_news.articles
        ]

        risk_analysis = risk_agent.classify_risks(
            search_results
        )

        logger.info(
            "Generated %d risk assessments.",
            len(risk_analysis),
        )

        return {
            **state,
            "risk_analysis": risk_analysis,
        }

    except Exception:
        logger.exception(
            "Risk Node execution failed."
        )

        return {
            **state,
            "risk_analysis": [],
        }
