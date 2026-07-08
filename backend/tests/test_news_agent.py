from backend.agents.news_agent import news_agent
from backend.models.search import NewsCollection


def test_fetch_news():
    response = news_agent.fetch_news(
        query="cement supply chain disruption",
        max_results=3,
    )

    assert response is not None
    assert isinstance(response, dict)
    assert "results" in response


def test_process_news():
    raw_news = news_agent.fetch_news(
        query="cement supply chain disruption",
        max_results=3,
    )

    processed_news = news_agent.process_news(raw_news)

    assert isinstance(processed_news, NewsCollection)
    assert processed_news.query != ""
    assert isinstance(processed_news.results, list)

    for article in processed_news.results:
        assert article.title != ""
        assert article.content != ""
        assert article.url != ""
        assert isinstance(article.score, float)


def test_prepare_agent_input():
    raw_news = news_agent.fetch_news(
        query="cement supply chain disruption",
        max_results=3,
    )

    agent_input = news_agent.prepare_agent_input(raw_news)

    assert "query" in agent_input
    assert "articles" in agent_input
    assert "article_count" in agent_input

    assert agent_input["query"] != ""
    assert isinstance(agent_input["articles"], list)
    assert agent_input["article_count"] == len(agent_input["articles"])


def test_duplicate_removal():
    raw_news = {
        "query": "test",
        "results": [
            {
                "title": "News 1",
                "url": "https://example.com/1",
                "published_date": "2026-07-09",
                "content": "Sample content",
                "score": 0.9,
            },
            {
                "title": "News 1 Duplicate",
                "url": "https://example.com/1",
                "published_date": "2026-07-09",
                "content": "Duplicate content",
                "score": 0.8,
            },
        ],
    }

    processed = news_agent.process_news(raw_news)

    assert len(processed.results) == 1


def test_filter_empty_articles():
    raw_news = {
        "query": "test",
        "results": [
            {
                "title": "",
                "url": "https://example.com/1",
                "published_date": "2026-07-09",
                "content": "",
                "score": 0.8,
            },
            {
                "title": "Valid Article",
                "url": "https://example.com/2",
                "published_date": "2026-07-09",
                "content": "Valid content",
                "score": 0.9,
            },
        ],
    }

    processed = news_agent.process_news(raw_news)

    assert len(processed.results) == 1
    assert processed.results[0].title == "Valid Article"