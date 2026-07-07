from backend.services.tavily_client import tavily_client


def test_tavily_search():
    response = tavily_client.search(
        query="cement supply chain disruption",
        topic="news",
        max_results=3,
    )

    assert response is not None
    assert "results" in response
    assert isinstance(response["results"], list)