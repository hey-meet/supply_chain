from backend.models.search import NewsCollection, SearchResult
from backend.services.tavily_client import tavily_client


class SearchService:
    """Service layer for retrieving logistics and supply chain news."""

    def search_news(
        self,
        query: str,
        max_results: int = 5,
    ) -> NewsCollection:
        """Search news using a custom query."""

        response = tavily_client.search(
            query=query,
            topic="news",
            max_results=max_results,
        )

        results = []

        for item in response.get("results", []):
            results.append(
                SearchResult(
                    title=item.get("title", ""),
                    url=item.get("url"),
                    published_date=item.get("published_date"),
                    content=item.get("content", ""),
                    score=item.get("score", 0.0),
                )
            )

        return NewsCollection(
            query=query,
            results=results,
        )

    def search_logistics_news(self, max_results: int = 5) -> NewsCollection:
        """Retrieve recent logistics-related news."""
        return self.search_news(
            query="latest logistics disruptions transportation freight shipping",
            max_results=max_results,
        )

    def search_supply_chain_news(self, max_results: int = 5) -> NewsCollection:
        """Retrieve recent supply chain news."""
        return self.search_news(
            query="latest supply chain disruptions cement manufacturing",
            max_results=max_results,
        )

    def search_weather_news(self, max_results: int = 5) -> NewsCollection:
        """Retrieve weather events affecting transportation and logistics."""
        return self.search_news(
            query="extreme weather affecting logistics transportation India",
            max_results=max_results,
        )

    def search_commodity_news(self, max_results: int = 5) -> NewsCollection:
        """Retrieve commodity market news relevant to cement manufacturing."""
        return self.search_news(
            query="coal diesel gypsum fly ash commodity price news",
            max_results=max_results,
        )


search_service = SearchService()