import json
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),"..",".."))
from backend.agents.news_agent import news_agent
from backend.models.agent_contracts import StructuredNews
from backend.models.search import NewsCollection, SearchResult


def test_fetch_news():
    response = news_agent.fetch_news(
        query="cement supply chain disruption",
        max_results=3,
    )

    assert isinstance(response, NewsCollection)
    assert response.query != ""
    assert isinstance(response.results, list)


def test_process_news():
    news = news_agent.fetch_news(
        query="cement supply chain disruption",
        max_results=3,
    )

    processed_news = news_agent.process_news(news)

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

    agent_input = news_agent.prepare_agent_input(news)

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

    processed = news_agent.process_news(news)

    assert len(processed.results) == 2
    assert processed.results[0].title == "Relevant Article"

def test_ask_llm_is_relevant():
    relevant_article = SearchResult(
        title="Relevant Article",
        url="https://example.com/1",
        published_date="2026-07-09",
        content="This article discusses raw material shortages in the cement supply chain.",
        score=0.9,
    )

    irrelevant_article = SearchResult(
        title="Irrelevant Article",
        url="https://example.com/2",
        published_date="2026-07-09",
        content="This article is about celebrity news and has nothing to do with supply chains.",
        score=0.8,
    )

    assert news_agent._ask_llm_is_relevant(relevant_article)[0] is True
    assert news_agent._ask_llm_is_relevant(irrelevant_article)[0] is False

def test_duplicate_removal():
    news = NewsCollection(
        query="test",
        results=[
            SearchResult(
                title="News 1",
                url="https://example.com/1",
                published_date="2026-07-09",
                content="Sample content",
                score=0.9,
            ),
            SearchResult(
                title="News 1 Duplicate",
                url="https://example.com/1",
                published_date="2026-07-09",
                content="Duplicate content",
                score=0.8,
            ),
        ],
    )

    processed = news_agent.process_news(news)

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
                title="Valid Article",
                url="https://example.com/2",
                published_date="2026-07-09",
                content="Valid content",
                score=0.9,
            ),
        ],
    )

    processed = news_agent.process_news(news)

    assert len(processed.results) == 1
    assert processed.results[0].title == "Valid Article"
