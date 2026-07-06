from backend.services.tavily_client import tavily_client


class SearchService:
    """Service layer for retrieving logistics and supply chain news."""

    def search_news(
        self,
        query: str,
        max_results: int = 5,
    ) -> dict:
        """Search news using a custom query."""
        return tavily_client.search(
            query=query,
            topic="news",
            max_results=max_results,
        )


search_service = SearchService()