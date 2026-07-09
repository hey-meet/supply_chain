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
