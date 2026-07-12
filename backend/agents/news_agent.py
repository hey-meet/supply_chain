import json
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),"..",".."))
from backend.models.search import NewsCollection, SearchResult
from backend.services.search_service import search_service
from backend.models.agent_contracts import StructuredNews
from backend.models.news import NewsArticle
from backend.services.news_ingestion import extract_domain
from backend.prompts.news_filter import build_relevance_prompt

try:
    from backend.services.llm_client import LLMClient
except ImportError:
    LLMClient = None

MIN_CONTENT_LENGTH = 40


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

    def filter_relevant_articles(
        self,
        articles: list[SearchResult],
    ) -> list[SearchResult]:
        """
        Filter out articles that do not contain enough information
        for downstream AI processing.
        """
        filtered_articles: list[SearchResult] = []

        for article in articles:
            if not article.title.strip():
                continue

            if not article.content.strip():
                continue

            filtered_articles.append(article)

        return filtered_articles

    
    def _ask_llm_is_relevant(self, article: SearchResult) -> tuple[bool, str]:
        """
        Asks the LLM whether ONE article is relevant to cement supply
        chain disruptions, using the prompt defined in news_filter.py.
 
        Returns:
            tuple[bool, str]: (is_relevant, reason). If the LLM call or
            response parsing fails for any reason, this FAILS OPEN —
            returns (True, "...") so a broken AI call doesn't silently
            drop real data. The article can still be filtered out later
            by the Risk Classification Agent if it truly isn't relevant.
        """
        prompt = build_relevance_prompt(article.title, article.content)
 
        try:
            llm_client = LLMClient()
            raw_response = llm_client.generate(prompt)
            parsed = json.loads(raw_response)
            return bool(parsed.get("is_relevant", True)), parsed.get("reason", "")
        except Exception as exc:
            return True, f"AI relevance check failed, kept by default ({exc})"
            
    def filter_by_ai_relevance(
        self,
        articles: list[SearchResult],
    ) -> list[SearchResult]:
        """
        Filter articles using AI relevance checks.
        """
        if LLMClient is None:
            return articles
 
        relevant_articles: list[SearchResult] = []
        for article in articles:
            is_relevant, _reason = self._ask_llm_is_relevant(article)
            if is_relevant:
                relevant_articles.append(article)
 
        return relevant_articles
    

    def remove_duplicates(
        self,
        articles: list[SearchResult],
    ) -> list[SearchResult]:
        """
        Remove duplicate articles using URL as the unique identifier.
        """
        unique_articles: list[SearchResult] = []
        # Added explicit type definition for the hash set tracker
        seen_urls: set[str] = set()

        for article in articles:
            url = str(article.url)

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
        # HttpUrl is already validated by Pydantic.
        article.score = float(article.score or 0.0)

        if article.published_date:
            article.published_date = article.published_date.strip()

        return article

    def process_news(
        self,
        news_data: NewsCollection,
    ) -> NewsCollection:
        """
        Process raw search results into structured news objects.

        Processing Steps
            ----------------
        1. Extract SearchResult models from NewsCollection
        2. Filter irrelevant articles
        3. Remove duplicate articles
        4. Clean article content
        5. Normalize metadata
        """
        results = news_data.results

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
            query=news_data.query,
            results=results,
        )

    def prepare_agent_input(
        self,
        news_data: NewsCollection,
    ) -> StructuredNews:
        """
        Prepare structured output for downstream AI agents.
        """
        processed_news = self.process_news(news_data)

        articles = [
            NewsArticle(
                title=article.title,
                content=article.content,
                source=None,
                url=article.url,
                published_date=article.published_date,
                location=None,
                search_score=article.score,
            )
            for article in processed_news.results
        ]

        return StructuredNews(
            query=processed_news.query,
            articles=articles,
            article_count=len(articles),
        )

news_agent = NewsIntelligenceAgent()
