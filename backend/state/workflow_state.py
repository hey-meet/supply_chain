"""
Workflow State Definition

This module defines the shared state that flows through the
entire LangGraph pipeline.

Every agent reads from and writes to this state.
"""

from typing import TypedDict, List, Dict, Any, Optional


class WorkflowState(TypedDict, total=False):
    """
    Shared state passed between all AI agents.

    Pipeline:

    Search
        ↓
    News Intelligence
        ↓
    News Filtering
        ↓
    Risk Classification
        ↓
    Supply Chain Impact
        ↓
    Mitigation Planning
        ↓
    Executive Summary
    """

    # ==========================================================
    # USER REQUEST
    # ==========================================================

    query: str

    # ==========================================================
    # SEARCH LAYER
    # ==========================================================

    search_results: List[Dict[str, Any]]

    # ==========================================================
    # NEWS PROCESSING
    # ==========================================================

    filtered_articles: List[Dict[str, Any]]

    news_analysis: Dict[str, Any]

    # ==========================================================
    # RISK ANALYSIS
    # ==========================================================

    risk_assessment: Dict[str, Any]

    # ==========================================================
    # SUPPLY CHAIN IMPACT
    # ==========================================================

    impact_analysis: Dict[str, Any]

    # ==========================================================
    # INVENTORY ANALYSIS
    # ==========================================================

    inventory_analysis: Dict[str, Any]

    # ==========================================================
    # MITIGATION PLANNING
    # ==========================================================

    mitigation_plan: Dict[str, Any]

    # ==========================================================
    # EXECUTIVE SUMMARY
    # ==========================================================

    executive_summary: Dict[str, Any]

    # ==========================================================
    # CONFIDENCE SCORES
    # ==========================================================

    confidence_scores: Dict[str, float]

    # ==========================================================
    # EXECUTION TRACE
    # ==========================================================

    execution_trace: List[Dict[str, Any]]

    # ==========================================================
    # RUNTIME METRICS
    # ==========================================================

    runtime_metrics: Dict[str, Any]

    # ==========================================================
    # FINAL RESPONSE
    # ==========================================================

    final_response: Optional[Dict[str, Any]]