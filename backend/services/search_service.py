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

    def search_logistics_news(self, max_results: int = 5) -> dict:
        """Retrieve recent logistics-related news."""
        return self.search_news(
            query="latest logistics disruptions transportation freight shipping",
            max_results=max_results,
        )

    def search_supply_chain_news(self, max_results: int = 5) -> dict:
        """Retrieve recent supply chain news."""
        return self.search_news(
            query="latest supply chain disruptions cement manufacturing",
            max_results=max_results,
        )

    def search_weather_news(self, max_results: int = 5) -> dict:
        """Retrieve weather events affecting transportation and logistics."""
        return self.search_news(
            query="extreme weather affecting logistics transportation India",
            max_results=max_results,
        )

    def search_commodity_news(self, max_results: int = 5) -> dict:
        """Retrieve commodity market news relevant to cement manufacturing."""
        return self.search_news(
            query="coal diesel gypsum fly ash commodity price news",
            max_results=max_results,
        )


search_service = SearchService()