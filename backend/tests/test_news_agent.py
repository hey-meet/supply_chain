from backend.agents.news_agent import news_agent


def test_fetch_news():
    response = news_agent.fetch_news(
        query="cement supply chain disruption",
        max_results=3,
    )

    assert response is not None
    assert "results" in response


def test_process_news():
    raw_news = news_agent.fetch_news(
        query="cement supply chain disruption",
        max_results=3,
    )

    processed_news = news_agent.process_news(raw_news)

    assert processed_news.query != ""
    assert len(processed_news.results) > 0


def test_prepare_agent_input():
    raw_news = news_agent.fetch_news(
        query="cement supply chain disruption",
        max_results=3,
    )

    agent_input = news_agent.prepare_agent_input(raw_news)

    assert "query" in agent_input
    assert "news" in agent_input
    assert "total_results" in agent_input
    assert agent_input["total_results"] == len(agent_input["news"])