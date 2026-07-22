import os
import sys
import json
from unittest.mock import patch

sys.path.append(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
    )
)

from backend.agents.news_filter_agent import news_filter_agent
from backend.agents.news_agent import news_agent
from backend.models.search import SearchResult, NewsCollection
from backend.models.agent_contracts import StructuredNews

def sample_article() -> SearchResult:
    """Create a sample news article for testing."""
    return SearchResult(
        title="Heavy rainfall disrupts limestone transportation",
        url="https://example.com/news",
        published_date="2026-07-14",
        content="Heavy rainfall caused major highway closures affecting limestone transportation to multiple cement plants.",
        score=0.95,
    )


@patch("backend.agents.news_filter_agent.LLMClient.generate")
def test_relevant_article(mock_generate):
    """Test relevant article response."""

    mock_generate.return_value = json.dumps({
        "is_relevant": True,
        "reason": "Transportation disruption affects supply chain."
    })

    is_relevant, reason = news_filter_agent.is_relevant(sample_article())

    assert is_relevant is True
    assert reason == "Transportation disruption affects supply chain."


@patch("backend.agents.news_filter_agent.LLMClient.generate")
def test_irrelevant_article(mock_generate):
    """Test irrelevant article response."""

    mock_generate.return_value = json.dumps({
        "is_relevant": False,
        "reason": "Entertainment news."
    })

    is_relevant, reason = news_filter_agent.is_relevant(sample_article())

    assert is_relevant is False
    assert reason == "Entertainment news."


@patch("backend.agents.news_filter_agent.LLMClient.generate")
def test_invalid_json_response(mock_generate):
    """Invalid JSON should fail open."""

    mock_generate.return_value = "INVALID JSON"

    is_relevant, reason = news_filter_agent.is_relevant(sample_article())

    assert is_relevant is True
    assert "Invalid JSON" in reason


@patch("backend.agents.news_filter_agent.LLMClient.generate")
def test_llm_exception(mock_generate):
    """LLM exceptions should fail open."""

    mock_generate.side_effect = RuntimeError("LLM unavailable")

    is_relevant, reason = news_filter_agent.is_relevant(sample_article())

    assert is_relevant is True
    assert "News filtering failed" in reason


def test_process_news():
    news = news_agent.fetch_news(
        query="cement supply chain disruption",
        max_results=3,
    )

    processed_news = news_filter_agent.process_news(news)

    assert isinstance(processed_news, NewsCollection)
    assert processed_news.query != ""
    assert isinstance(processed_news.results, list)

    for article in processed_news.results:
        assert article.title != ""
        assert article.content != ""
        assert str(article.url) != ""
        assert isinstance(article.score, float)

def test_prepare_agent_input():
    news = news_agent.fetch_news(
        query="cement supply chain disruption",
        max_results=3,
    )

    agent_input = news_filter_agent.prepare_agent_input(news)

    assert isinstance(agent_input, StructuredNews)
    assert agent_input.query != ""
    assert isinstance(agent_input.articles, list)
    assert agent_input.article_count == len(agent_input.articles)

def test_filter_relevant_articles():
    news = NewsCollection(
        query="test",
        results=[
            SearchResult(
                title="Relevant Article",
                url="https://example.com/1",
                published_date="2026-07-09",
                content="This article discusses raw material shortages in the cement supply chain.",
                score=0.9,
            ),
            SearchResult(
                title="Irrelevant Article",
                url="https://example.com/2",
                published_date="2026-07-09",
                content="This article is about celebrity news and has nothing to do with supply chains.",
                score=0.8,
            ),
        ],
    )

    processed = news_filter_agent.process_news(news)

    assert len(processed.results) == 1
    assert processed.results[0].title == "Relevant Article"

def test_duplicate_removal():
    news = NewsCollection(
        query="test",
        results=[
            SearchResult(
                title="Cement plant shut down",
                url="https://example.com/1",
                published_date="2026-07-09",
                content="A major cement plant shut down due to raw material shortages.",
                score=0.9,
            ),
            SearchResult(
                title="Cement plant shut down again",
                url="https://example.com/1",
                published_date="2026-07-09",
                content="A major cement plant shut down due to raw material shortages.",
                score=0.8,
            ),
        ],
    )

    processed = news_filter_agent.process_news(news)

    assert len(processed.results) == 1

def test_filter_empty_articles():
    news = NewsCollection(
        query="test",
        results=[
            SearchResult(
                title="",
                url="https://example.com/1",
                published_date="2026-07-09",
                content="",
                score=0.8,
            ),
            SearchResult(
                title="Relevant Article",
                url="https://example.com/2",
                published_date="2026-07-09",
                content="This article discusses raw material shortages in the cement supply chain.",
                score=0.9,
            ),
        ],
    )

    processed = news_filter_agent.process_news(news)

    assert len(processed.results) == 1
    assert processed.results[0].title == "Relevant Article"

if __name__ == "__main__":
    print("=" * 60)
    print("NEWS FILTER AGENT TEST")
    print("=" * 60)
    
    print("\nRunning test_process_news (Integration Test) ...")
    test_process_news()
    print("test_process_news completed successfully.")
    
    print("\nRunning test_filter_relevant_articles ...")
    test_filter_relevant_articles()
    print("test_filter_relevant_articles completed successfully.")
    
    print("\nRunning test_duplicate_removal ...")
    test_duplicate_removal()
    print("test_duplicate_removal completed successfully.")
    
    print("\n" + "=" * 60)
    print("ALL SELECTED TESTS PASSED")
    print("=" * 60)

