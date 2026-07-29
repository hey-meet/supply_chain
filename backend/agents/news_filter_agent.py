import json
import logging

from backend.prompts.prompt_manager import prompt_manager
from backend.services.llm_client import LLMClient
from backend.models.search import SearchResult, NewsCollection
from backend.models.agent_contracts import StructuredNews
from backend.models.news import NewsArticle

logger = logging.getLogger(__name__)


class NewsFilterAgent:
    """
    AI agent responsible for determining whether a news article
    is relevant to the cement manufacturing supply chain.

    This is the first stage of the enterprise AI pipeline.
    """

    def __init__(self):
        self.llm = LLMClient()

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

    def is_relevant(
        self,
        article: SearchResult,
    ) -> tuple[bool, str]:
        """
        Determine whether a news article is relevant for
        downstream AI processing.

        Returns:
            tuple[bool, str]:
                (is_relevant, reason)
        """

        prompt = prompt_manager.render(
            template_name="news_filter.txt",
            variables={
                "title": article.title,
                "content": article.content,
            },
        )

        try:
            response = self.llm.generate(prompt)
            
            # Clean potential markdown fences securely
            clean_response = (
                response.replace("```json", "")
                .replace("```", "")
                .strip()
            )
            
            result = json.loads(clean_response)

            is_relevant = bool(
                result.get("is_relevant", True)
            )

            reason = result.get(
                "reason",
                "No reason provided.",
            )

            return is_relevant, reason

        except json.JSONDecodeError:
            logger.warning(
                "News Filter Agent returned invalid JSON."
            )
            return (
                True,
                "Invalid JSON returned by LLM. Article kept by default.",
            )

        except Exception as exc:
            logger.exception(
                "News Filter Agent execution failed."
            )

            return (
                True,
                f"News filtering failed: {exc}",
            )

    def filter_by_ai_relevance(
        self,
        articles: list[SearchResult],
    ) -> list[SearchResult]:
        """
        Filter articles using the News Filter Agent in parallel.
        """
        if not articles:
            return []

        from concurrent.futures import ThreadPoolExecutor

        def check_relevance(article):
            try:
                is_relevant, _ = self.is_relevant(article)
                return article, is_relevant
            except Exception as e:
                logger.error("Error checking relevance for article %r: %s", article.title, e)
                return article, True # Fallback: keep article if check fails

        relevant_articles: list[SearchResult] = []
        with ThreadPoolExecutor(max_workers=min(len(articles), 10)) as executor:
            results = executor.map(check_relevance, articles)
            for article, is_relevant in results:
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
        2. Filter out raw articles lacking basic validation (title/content)
        3. Filter articles via AI relevance checks
        4. Remove duplicate articles using URL tracking
        5. Clean article content text structure
        6. Normalize metadata formats
        """
        results = news_data.results

        results = self.filter_relevant_articles(results)

        results = self.filter_by_ai_relevance(results)

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


news_filter_agent = NewsFilterAgent()
