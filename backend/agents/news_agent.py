import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),"..",".."))
from backend.models.search import NewsCollection, SearchResult
from backend.services.search_service import search_service


class NewsIntelligenceAgent:
    """Agent responsible for retrieving and preparing news data."""

    def fetch_news(
        self,
        query: str,
        max_results: int = 5,
    ) -> NewsCollection:
        """
        Fetch news from the Search Service.
        """
        return search_service.search_news(
            query=query,
            max_results=max_results,
        )

    def parse_search_results(self, news_data: dict) -> list[SearchResult]:
        """
        Convert raw Tavily search results into SearchResult objects.
        Kept for backward compatibility with existing tests.
        """
        # Assigned to an explicitly typed variable before returning for readability/debugging
        results: list[SearchResult] = [
            SearchResult(
                title=item.get("title", ""),
                url=item.get("url", ""),
                published_date=item.get("published_date"),
                content=item.get("content", ""),
                score=item.get("score", 0.0),
            )
            for item in news_data.get("results", [])
        ]
        return results

news_agent = NewsIntelligenceAgent()
