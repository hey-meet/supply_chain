from backend.models.search import NewsCollection, SearchResult
from backend.services.search_service import search_service


class NewsIntelligenceAgent:
    """Agent responsible for retrieving and preparing news data."""

    def fetch_news(
        self,
        query: str,
        max_results: int = 5,
    ) -> dict:
        """
        Fetch news from the Search Service.
        """
        return search_service.search_news(
            query=query,
            max_results=max_results,
        )

    def process_news(
        self,
        news_data: dict,
    ) -> NewsCollection:
        """
        Process raw Tavily response into structured search models.

        Phase 1:
        - Validate response
        - Convert results into Pydantic models
        - Prepare data for downstream AI agents

        (LLM processing will be added in Day 3.)
        """

        results = [
            SearchResult(
                title=item.get("title", ""),
                url=item.get("url", ""),
                published_date=item.get("published_date"),
                content=item.get("content", ""),
                score=item.get("score", 0.0),
            )
            for item in news_data.get("results", [])
        ]

        return NewsCollection(
            query=news_data.get("query", ""),
            results=results,
        )

    def prepare_agent_input(
        self,
        news_data: dict,
    ) -> dict:
        """
        Prepare structured input for downstream AI agents.
        """

        processed_news = self.process_news(news_data)

        return {
            "query": processed_news.query,
            "news": processed_news.results,
            "total_results": len(processed_news.results),
        }


news_agent = NewsIntelligenceAgent()