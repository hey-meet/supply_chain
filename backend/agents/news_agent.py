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

    def filter_relevant_articles(
        self,
        articles: list[SearchResult],
    ) -> list[SearchResult]:
        """
        Filter out articles that do not contain enough information
        for downstream AI processing.
        """

        filtered_articles = []

        for article in articles:
            if not article.title.strip():
                continue

            if not article.content.strip():
                continue

            filtered_articles.append(article)

        return filtered_articles

    def remove_duplicates(
        self,
        articles: list[SearchResult],
    ) -> list[SearchResult]:
        """
        Remove duplicate articles using URL as the unique identifier.
        """

        unique_articles = []
        seen_urls = set()

        for article in articles:
            url = article.url.strip()

            if url in seen_urls:
                continue

            seen_urls.add(url)
            unique_articles.append(article)

        return unique_articles

    def clean_content(
        self,
        article: SearchResult,
    ) -> SearchResult:
        """
        Clean article content before AI processing.
        """

        article.title = " ".join(article.title.split())
        article.content = " ".join(article.content.split())

        return article

    def normalize_metadata(
        self,
        article: SearchResult,
    ) -> SearchResult:
        """
        Normalize metadata into a consistent format.
        """

        article.url = article.url.strip()

        article.score = float(article.score or 0.0)

        if article.published_date:
            article.published_date = article.published_date.strip()

        return article

    def process_news(
        self,
        news_data: dict,
    ) -> NewsCollection:
        """
        Process raw search results into structured news objects.

        Processing Steps
        ----------------
        1. Convert raw response into SearchResult models
        2. Filter irrelevant articles
        3. Remove duplicate articles
        4. Clean article content
        5. Normalize metadata
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

        results = self.filter_relevant_articles(results)

        results = self.remove_duplicates(results)

        results = [
            self.clean_content(article)
            for article in results
        ]

        results = [
            self.normalize_metadata(article)
            for article in results
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
        Prepare structured output for downstream AI agents.
        """

        processed_news = self.process_news(news_data)

        return {
            "query": processed_news.query,
            "articles": processed_news.results,
            "article_count": len(processed_news.results),
        }


news_agent = NewsIntelligenceAgent()