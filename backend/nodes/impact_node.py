"""
LangGraph Impact Node.

This node evaluates the operational and business impact of each
identified supply chain risk and stores the resulting impact
analyses in the workflow state.
"""

from __future__ import annotations

import logging

from backend.agents.supply_chain_impact_agent import (
    supply_chain_impact_agent,
)
from backend.graphs.state import SupplyChainState

logger = logging.getLogger(__name__)


def impact_node(
    state: SupplyChainState,
) -> SupplyChainState:
    """
    Execute deterministic supply chain impact analysis.

    Workflow
    --------
    RiskAnalysis[]
            ↓
    SupplyChainImpactAgent
            ↓
    ImpactAnalysis[]
            ↓
    Updated State
    """

    logger.info("Executing Impact Node.")

    risk_analyses = state.get("risk_analysis")

    if not risk_analyses:
        logger.warning(
            "No risk analysis available for impact assessment."
        )

        return {
            **state,
            "impact_analysis": [],
        }

    try:
        impact_results = [
            supply_chain_impact_agent.analyze(risk)
            for risk in risk_analyses
        ]

        logger.info(
            "Generated %d impact analyses.",
            len(impact_results),
        )

        return {
            **state,
            "impact_analysis": impact_results,
        }

    except Exception:
        logger.exception(
            "Impact Node execution failed."
        )

        return {
            **state,
            "impact_analysis": [],
        }
