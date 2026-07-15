import json
import logging

from backend.prompts.prompt_manager import prompt_manager
from backend.services.llm_client import LLMClient
from backend.models.search import SearchResult


logger = logging.getLogger(__name__)


class NewsFilterAgent:
    """
    AI agent responsible for determining whether a news article
    is relevant to the cement manufacturing supply chain.

    This is the first stage of the enterprise AI pipeline.
    """

    def __init__(self):
        self.llm = LLMClient()

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
            result = json.loads(response)

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


news_filter_agent = NewsFilterAgent()