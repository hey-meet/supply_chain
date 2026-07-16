import os
import sys
import json
from unittest.mock import patch

sys.path.append(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
    )
)

from backend.agents.news_filter_agent import news_filter_agent
from backend.models.search import SearchResult

def sample_article() -> SearchResult:
    """Create a sample news article for testing."""
    return SearchResult(
        title="Heavy rainfall disrupts limestone transportation",
        url="https://example.com/news",
        published_date="2026-07-14",
        content="Heavy rainfall caused major highway closures affecting limestone transportation to multiple cement plants.",
        score=0.95,
    )


@patch("backend.agents.news_filter_agent.LLMClient.generate")
def test_relevant_article(mock_generate):
    """Test relevant article response."""

    mock_generate.return_value = json.dumps({
        "is_relevant": True,
        "reason": "Transportation disruption affects supply chain."
    })

    is_relevant, reason = news_filter_agent.is_relevant(sample_article())

    assert is_relevant is True
    assert reason == "Transportation disruption affects supply chain."


@patch("backend.agents.news_filter_agent.LLMClient.generate")
def test_irrelevant_article(mock_generate):
    """Test irrelevant article response."""

    mock_generate.return_value = json.dumps({
        "is_relevant": False,
        "reason": "Entertainment news."
    })

    is_relevant, reason = news_filter_agent.is_relevant(sample_article())

    assert is_relevant is False
    assert reason == "Entertainment news."


@patch("backend.agents.news_filter_agent.LLMClient.generate")
def test_invalid_json_response(mock_generate):
    """Invalid JSON should fail open."""

    mock_generate.return_value = "INVALID JSON"

    is_relevant, reason = news_filter_agent.is_relevant(sample_article())

    assert is_relevant is True
    assert "Invalid JSON" in reason


@patch("backend.agents.news_filter_agent.LLMClient.generate")
def test_llm_exception(mock_generate):
    """LLM exceptions should fail open."""

    mock_generate.side_effect = RuntimeError("LLM unavailable")

    is_relevant, reason = news_filter_agent.is_relevant(sample_article())

    assert is_relevant is True
    assert "News filtering failed" in reason