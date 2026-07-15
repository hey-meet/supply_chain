import os
import sys
from unittest.mock import patch

sys.path.append(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
    )
)

from backend.agents.executive_summary_agent import (
    executive_summary_agent,
)
from backend.models.agent_contracts import (
    ExecutiveSummaryAgentInput,
)
from backend.models.news import NewsArticle


def sample_article() -> NewsArticle:
    """Create a sample news article."""

    return NewsArticle(
        title="Heavy rainfall disrupts limestone transportation",
        content=(
            "Heavy rainfall caused major highway closures affecting "
            "limestone transportation to multiple cement plants."
        ),
        source="Reuters",
        url="https://example.com/news",
        published_date="2026-07-15",
        location=None,
        search_score=0.95,
    )


@patch("backend.agents.executive_summary_agent.LLMClient.generate")
def test_generate_single_summary(mock_generate):
    """Test executive summary generation."""

    mock_generate.return_value = (
        "Heavy rainfall disrupted limestone transportation, "
        "creating logistics challenges for the cement industry."
    )

    agent_input = ExecutiveSummaryAgentInput(
        articles=[sample_article()]
    )

    result = executive_summary_agent.generate(agent_input)

    assert len(result.summaries) == 1
    assert "Heavy rainfall" in result.summaries[0]


@patch("backend.agents.executive_summary_agent.LLMClient.generate")
def test_generate_multiple_summaries(mock_generate):
    """Test generation for multiple news articles."""

    mock_generate.return_value = (
        "Executive disruption summary."
    )

    agent_input = ExecutiveSummaryAgentInput(
        articles=[
            sample_article(),
            sample_article(),
        ]
    )

    result = executive_summary_agent.generate(agent_input)

    assert len(result.summaries) == 2


@patch("backend.agents.executive_summary_agent.LLMClient.generate")
def test_empty_article_list(mock_generate):
    """Empty input should return empty summaries."""

    agent_input = ExecutiveSummaryAgentInput(
        articles=[]
    )

    result = executive_summary_agent.generate(agent_input)

    assert result.summaries == []
    mock_generate.assert_not_called()


@patch("backend.agents.executive_summary_agent.LLMClient.generate")
def test_llm_exception(mock_generate):
    """LLM failures should return an error summary."""

    mock_generate.side_effect = RuntimeError(
        "LLM unavailable"
    )

    agent_input = ExecutiveSummaryAgentInput(
        articles=[sample_article()]
    )

    result = executive_summary_agent.generate(agent_input)

    assert len(result.summaries) == 1
    assert "ERROR" in result.summaries[0]