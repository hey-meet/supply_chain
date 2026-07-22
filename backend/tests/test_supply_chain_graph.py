"""
Integration test for the complete Supply Chain LangGraph workflow.
"""

from backend.graphs.supply_chain_graph import supply_chain_graph


def test_supply_chain_workflow():
    """
    Verify that the complete LangGraph workflow executes successfully.
    """

    initial_state = {
        "query": (
            "Heavy rainfall causing limestone transportation delays "
            "in Gujarat cement plants"
        )
    }

    result = supply_chain_graph.invoke(initial_state)

    assert result is not None

    # Initial input
    assert result["query"] == initial_state["query"]

    # News
    assert "search_results" in result
    assert result["search_results"] is not None

    # Filtered News
    assert "filtered_news" in result
    assert result["filtered_news"] is not None

    # Risk Analysis
    assert "risk_analysis" in result
    assert isinstance(result["risk_analysis"], list)

    # Impact Analysis
    assert "impact_analysis" in result
    assert isinstance(result["impact_analysis"], list)

    # Mitigation Plans
    assert "mitigation_plan" in result
    assert isinstance(result["mitigation_plan"], list)

    # Executive Summary
    assert "executive_summary" in result