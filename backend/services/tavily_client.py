from tavily import TavilyClient

from backend.config.settings import settings


class TavilySearchClient:
    """Reusable client for interacting with the Tavily Search API."""

    def __init__(self):
        self.client = TavilyClient(api_key=settings.TAVILY_API_KEY)

    def search(
        self,
        query: str,
        *,
        topic: str = "general",
        max_results: int = 5,
    ) -> dict:
        """
        Execute a Tavily search request.

        Args:
            query: Search query.
            topic: Search topic ("general" or "news").
            max_results: Maximum number of search results.

        Returns:
            Raw Tavily API response.

        Raises:
            RuntimeError: If the Tavily request fails.
        """
        try:
            return self.client.search(
                query=query,
                topic=topic,
                max_results=max_results,
            )
        except Exception as exc:
            raise RuntimeError(f"Tavily search failed: {exc}") from exc


tavily_client = TavilySearchClient()