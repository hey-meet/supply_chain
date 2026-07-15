from datetime import datetime
import hashlib
import logging

from backend.models.agent_contracts import (
    ExecutiveSummaryAgentInput,
    ExecutiveSummaryAgentOutput,
)
from backend.prompts.prompt_manager import prompt_manager
from backend.services.llm_client import LLMClient


logger = logging.getLogger(__name__)


class ExecutiveSummaryAgent:
    """
    AI agent responsible for generating executive-level
    disruption summaries from validated news articles.
    """

    def __init__(self):
        self.llm = LLMClient()

    def generate_summary(
        self,
        article,
    ) -> str:
        """
        Generate an executive summary for a single news article.
        """

        event_id = hashlib.sha256(
            article.title.encode("utf-8")
        ).hexdigest()[:12]

        generated_timestamp = datetime.utcnow().isoformat()

        prompt = prompt_manager.render(
            template_name="executive_summary.txt",
            variables={
                "news_article": (
                    f"Title: {article.title}\n\n"
                    f"Content: {article.content}"
                ),
                "event_id": event_id,
                "generated_timestamp": generated_timestamp,
            },
        )

        try:
            return self.llm.generate(prompt).strip()

        except Exception as exc:
            logger.exception(
                "Executive Summary Agent failed."
            )

            return (
                "ERROR: Failed to generate executive summary. "
                f"Reason: {exc}"
            )

    def generate(
        self,
        agent_input: ExecutiveSummaryAgentInput,
    ) -> ExecutiveSummaryAgentOutput:
        """
        Generate executive summaries for all processed news articles.
        """

        summaries: list[str] = []

        for article in agent_input.articles:
            summaries.append(
                self.generate_summary(article)
            )

        return ExecutiveSummaryAgentOutput(
            summaries=summaries,
        )


executive_summary_agent = ExecutiveSummaryAgent()