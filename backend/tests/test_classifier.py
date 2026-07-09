import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),"..",".."))
from backend.services.disruption_classifier import (
    RISK_CATEGORY_KEYWORDS,
    detect_risk_categories,
    assign_severity,
    classify_article,
    classify_articles,
    classify_articles_to_json,
)


SAMPLE_RAW_ARTICLES = [
    {
        "title": "Heavy rainfall causes severe highway closure near Plant A",
        "url": "https://example.com/news/1",
        "content": "Heavy rainfall has caused severe flooding and a road "
                    "closure near Plant A, disrupting limestone deliveries.",
        "published_date": "2026-07-01",
    },
    {
        "title": "Everything normal at the port today",
        "url": "https://example.com/news/2",
        "content": "Operations at the port continued smoothly with no delays.",
        "published_date": "2026-07-02",
    },
]

def test_detect_risk_categories_matches_flood_and_road_closure():
    content = "Heavy flooding and a road closure hit the region."
    categories = detect_risk_categories(content)
    assert "Flood" in categories
    assert "Road Closure" in categories


def test_detect_risk_categories_returns_safe_when_no_match():
    assert detect_risk_categories("Everything is calm and normal today.") == ["Safe / No Risk"]
    assert detect_risk_categories("") == ["Safe / No Risk"]


def test_assign_severity_uses_severity_keywords():
    assert assign_severity("A severe flood hit the area.", ["Flood"]) == "High"
    assert assign_severity("A minor delay was reported.", ["Port Congestion"]) == "Low"

def test_assign_severity_falls_back_on_category_count():
    # No severity keyword present, so it falls back to category count.
    assert assign_severity("flood and road closure", ["Flood", "Road Closure"]) == "High"
    assert assign_severity("flood", ["Flood"]) == "Medium"


def test_assign_severity_is_low_when_safe():
    assert assign_severity("nothing happened", ["Safe / No Risk"]) == "Low"


def test_classify_article_returns_expected_schema():
    article = {
        "title": "Flood hits region",
        "content": "A severe flood has disrupted transport.",
        "domain": "example.com",
        "published_date": "2026-07-01",
        "url": "https://example.com/1",
        "location": "Gujarat",
        "keywords": ["flood", "transport"],
    }
    result = classify_article(article)

    expected_fields = {
        "title", "content", "domain", "published_date", "url",
        "location", "risk_categories", "severity", "keywords",
    }
    assert expected_fields == set(result.keys())
    assert "Flood" in result["risk_categories"]
    assert result["severity"] == "High"


def test_classify_articles_runs_full_pipeline():
    results = classify_articles(SAMPLE_RAW_ARTICLES)
    assert len(results) == 2
    assert "Flood" in results[0]["risk_categories"]
    assert results[0]["severity"] == "High"

if __name__ == "__main__":
    # Run the tests and print the classification results for inspection.
    test_detect_risk_categories_matches_flood_and_road_closure()
    test_detect_risk_categories_returns_safe_when_no_match()
    test_assign_severity_uses_severity_keywords()
    test_assign_severity_falls_back_on_category_count()
    test_assign_severity_is_low_when_safe()
    test_classify_article_returns_expected_schema()
    test_classify_articles_runs_full_pipeline()
    print("All tests passed!")
