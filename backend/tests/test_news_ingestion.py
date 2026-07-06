import os
import sys
from unittest.mock import patch
sys.path.append(os.path.join(os.path.dirname(__file__),"..",".."))
from services.news_ingestion import (
    clean_text,
    extract_domain,
    extract_keywords,)

FAKE_TAVILY_RESPONSE = {
    "results": [
        {
            "title": "  Heavy Rainfall Shuts Down Highway  ",
            "url": "https://www.example.com/news/1",
            "content": "<p>Heavy rain has caused a road closure near the plant.</p>",
            "published_date": "2026-07-01",
        },
        {
            "title": "Port Congestion Delays Shipments",
            "url": "https://ports-news.com/news/2",
            "content": "Ships are waiting longer than usual to unload cargo at the port.",
            "published_date": "2026-07-02",
        },
    ]
}

def test_clean_text_removes_html_and_extra_spaces():
    dirty_text = "  Hello   <b>World</b>  \n\n  "
    result = clean_text(dirty_text)
    assert result == "Hello World"
 

def test_extract_domain_returns_domain_without_www():
    assert extract_domain("https://www.reuters.com/world/story") == "reuters.com"
 
def test_extract_keywords_returns_relevant_words():
    text = "Heavy rainfall causes highway closure. Rainfall continues near the plant."
    keywords = extract_keywords(text, top_n=3)
 
    assert isinstance(keywords, list)
    assert len(keywords) <= 3
    assert "rainfall" in keywords  # appears twice, should be picked up


if __name__ == "__main__":
    test_clean_text_removes_html_and_extra_spaces()
    test_extract_domain_returns_domain_without_www()
    test_extract_keywords_returns_relevant_words()
    print("All tests passed!")
