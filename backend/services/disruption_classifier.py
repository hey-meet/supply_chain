"""
    NOTE: This can later be replaced with an LLM-based classifier (an
    AI model reading the article and deciding the category/severity
    itself) without changing how other files call classify_article() —
    the function name and output shape would stay exactly the same.
"""

import json
try:
    from news_ingestion import extract_articles_from_search_result, process_raw_articles
    from search_service import search_service
except ImportError as e:
    from backend.services.news_ingestion import extract_articles_from_search_result, process_raw_articles
    from backend.services.search_service import search_service

# -----------------------------------------------------------------------
# STEP 1: Define the disruption risk categories
# -----------------------------------------------------------------------
RISK_CATEGORY_KEYWORDS = {
    "Flood": ["flood", "flooding", "inundated", "submerged"],
    "Heavy Rainfall": ["heavy rainfall", "heavy rain", "downpour", "monsoon"],
    "Road Closure": ["road closure", "highway closed", "road blocked", "route blocked"],
    "Railway Strike": ["railway strike", "rail strike", "train strike"],
    "Port Congestion": ["port congestion", "port delay", "vessel backlog", "ship queue"],
    "Fuel Price Increase": ["fuel price", "diesel price", "petrol price", "fuel cost"],
    "Coal Price Increase": ["coal price", "coal cost"],
    "Supplier Shutdown": ["supplier shutdown", "factory shutdown", "plant closure", "production halt"],
    "Political Conflict": ["conflict", "war", "political unrest", "protest", "sanctions"],
    "Natural Disaster": ["earthquake", "cyclone", "hurricane", "tsunami", "wildfire"],
}

# The fallback category when nothing matches.
SAFE_CATEGORY = "Safe / No Risk"

# Words that hint at how severe a disruption is, checked in this order
SEVERITY_KEYWORDS = {
    "Critical": ["catastrophic", "critical", "devastating", "extensive damage"],
    "High": ["severe", "major", "significant", "serious"],
    "Medium": ["moderate", "partial disruption", "some delay"],
    "Low": ["minor", "slight", "limited"],
}
