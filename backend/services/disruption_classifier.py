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

# -----------------------------------------------------------------------
# STEP 2: Detect which risk categories match the article content
# -----------------------------------------------------------------------
def detect_risk_categories(content: str) -> list[str]:
    """
    Scans the article content for keywords belonging to each risk
    category and returns every category that has a match.

    Args:
        content (str): The article's text.

    Returns:
        list[str]: Matching category names, e.g. ["Flood", "Road Closure"].
        If nothing matches, returns ["Safe / No Risk"].
    """
    if not content:
        return [SAFE_CATEGORY]

    text = content.lower()
    matched_categories = []

    for category, keywords in RISK_CATEGORY_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            matched_categories.append(category)

    return matched_categories if matched_categories else [SAFE_CATEGORY]


# -----------------------------------------------------------------------
# STEP 3: Decide the severity of the disruption
# -----------------------------------------------------------------------
def assign_severity(content: str, matched_categories: list[str]) -> str:
    """
    Figures out how severe the disruption is.

    How it decides (in order):
        1. If nothing risky was matched -> "Low".
        2. If the text contains an explicit severity word (e.g. "severe",
           "minor") -> use that word's severity level.
        3. Otherwise, fall back on a simple rule: more than one matched
           category -> "High", exactly one -> "Medium".

    Args:
        content (str): The article's text.
        matched_categories (list[str]): Categories from detect_risk_categories().

    Returns:
        str: One of "Low", "Medium", "High", "Critical".
    """
    if matched_categories == [SAFE_CATEGORY]:
        return "Low"

    text = (content or "").lower()

    for level, words in SEVERITY_KEYWORDS.items():
        if any(word in text for word in words):
            return level

    # No explicit severity word found — fall back on category count.
    return "High" if len(matched_categories) > 1 else "Medium"

