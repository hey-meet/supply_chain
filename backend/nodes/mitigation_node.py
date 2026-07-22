"""
LangGraph Mitigation Node.

This node generates deterministic mitigation plans for each
identified supply chain impact and stores the resulting plans
in the workflow state.
"""

from __future__ import annotations

import logging

from backend.agents.mitigation_planning_agent import (
    mitigation_planning_agent,
)
from backend.graphs.state import SupplyChainState

logger = logging.getLogger(__name__)


def mitigation_node(
    state: SupplyChainState,
) -> SupplyChainState:
    """
    Execute mitigation planning.

    Workflow
    --------
    ImpactAnalysis[]
            ↓
    MitigationPlanningAgent
            ↓
    MitigationPlan[]
            ↓
    Updated State
    """

    logger.info("Executing Mitigation Node.")

    impact_analyses = state.get("impact_analysis")

    if not impact_analyses:
        logger.warning(
            "No impact analysis available for mitigation planning."
        )

        return {
            **state,
            "mitigation_plan": [],
        }

    try:
        mitigation_plans = [
            mitigation_planning_agent.analyze(
                impact
            )
            for impact in impact_analyses
        ]

        logger.info(
            "Generated %d mitigation plans.",
            len(mitigation_plans),
        )

        return {
            **state,
            "mitigation_plan": mitigation_plans,
        }

    except Exception:
        logger.exception(
            "Mitigation Node execution failed."
        )

        return {
            **state,
            "mitigation_plan": [],
        }