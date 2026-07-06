from unittest.mock import patch

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
