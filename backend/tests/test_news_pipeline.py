from backend.agents.news_agent import news_agent
from backend.agents.news_filter_agent import news_filter_agent
from backend.models.agent_contracts import StructuredNews
from backend.models.search import NewsCollection


def test_end_to_end_news_pipeline():
    """
    Validate the complete News Intelligence pipeline.

    Flow:
        Query
          ↓
    SearchService
          ↓
    NewsCollection
          ↓
    NewsIntelligenceAgent
          ↓
    StructuredNews
    """

    query = "cement supply chain disruption"

    # Step 1: Fetch news
    news = news_agent.fetch_news(
        query=query,
        max_results=5,
    )

    assert isinstance(news, NewsCollection)
    assert news.query == query
    assert len(news.results) > 0

    # Step 2: Process news
    processed = news_filter_agent.process_news(news)

    assert isinstance(processed, NewsCollection)
    assert len(processed.results) > 0

    # Step 3: Prepare structured output
    structured = news_filter_agent.prepare_agent_input(processed)

    assert isinstance(structured, StructuredNews)

    # Step 4: Validate consistency
    assert structured.query == query
    assert structured.article_count == len(structured.articles)

    # Step 5: Validate article schema
    for article in structured.articles:
        assert article.title.strip()
        assert article.content.strip()
        assert article.url is not None
        assert article.search_score >= 0