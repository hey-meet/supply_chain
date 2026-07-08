import os
import sys
import json
from unittest.mock import patch
sys.path.append(os.path.join(os.path.dirname(__file__),"..",".."))
from backend.services.news_ingestion import (
    clean_text,
    extract_domain,
    extract_keywords,
    extract_location,
    build_structured_article,
    process_raw_articles,
    extract_articles_from_search_result,
    )

SAMPLE_RAW_ARTICLES = [
    {
        "title": "  Heavy Rainfall Shuts Down Highway  ",
        "url": "https://www.reuters.com/world/story",
        "content": "<p>Heavy rain has caused a road closure near the plant.</p>",
        "published_date": "2026-07-01",
    },
    {
        "title": "Port Congestion Delays Shipments",
        "url": "https://ports-news.com/news/2",
        "content": "Ships are waiting longer than usual to unload cargo.",
        "published_date": "2026-07-02",
    },
]

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


def test_extract_location():
    assert extract_location("Heavy rain has flooded Gujarat this week.") == "Gujarat"
    assert extract_location("A strike hit the port of Shanghai.") == "Shanghai"
    assert extract_location("No location mentioned here at all.") is None
    assert extract_location("") is None

def test_build_structured_article():
    structured = build_structured_article(SAMPLE_RAW_ARTICLES[0])
 
    expected_fields = {"title", "content", "domain", "published_date", "url", "location", "keywords"}
    assert expected_fields.issubset(structured.keys())
    assert structured["title"] == "Heavy Rainfall Shuts Down Highway"
    assert structured["domain"] == "reuters.com"
    assert structured["content"] == "Heavy rain has caused a road closure near the plant."
 
 
def test_process_raw_articles():
    results = process_raw_articles(SAMPLE_RAW_ARTICLES)
    assert len(results) == 2
    assert process_raw_articles([]) == []
 
    # Print the final structured output so you can see it clearly.
    print("\n----- STRUCTURED NEWS OBJECTS -----")
    print(json.dumps(results, indent=2))
    print("------------------------------------\n")


def test_extract_articles_from_search_result_uses_results_field():
    search_result = {
        "results": [
            {"title": "Rain disrupts port", "content": "Heavy rains hit the port", "url": "https://example.com/1", "published_date": "2026-07-01"}
        ]
    }

    articles = extract_articles_from_search_result(search_result)
    assert len(articles) == 1
    assert articles[0]["title"] == "Rain disrupts port"

    
if __name__ == "__main__":
    test_clean_text_removes_html_and_extra_spaces()
    test_extract_domain_returns_domain_without_www()
    test_extract_keywords_returns_relevant_words()
    test_extract_location()
    test_build_structured_article()
    test_process_raw_articles()
    print("All tests passed!")
