import os
import re
from urllib.parse import urlparse

# -----------------------------------------------------------------------
# STEP 1: Clean & preprocess article text
# -----------------------------------------------------------------------
def clean_text(text: str) -> str:
    """
    Cleans the input text by removing unwanted characters and formatting.

    Args:
        text (str): The input text to be cleaned.

    Returns:
        str: Cleaned text.
    """
    if not text:
        return ""
    
    text = re.sub(r"<[^>]+>", "", text)  # Remove HTML tags

    text = re.sub(r"\s+", " ", text)  # Replace multiple whitespace with single space

    return text.strip()

# -----------------------------------------------------------------------
# STEP 2: Extract domain from URL
# -----------------------------------------------------------------------

def extract_domain(url: str) -> str:
    """
    Extracts the domain from a given URL.

    Args:
        url (str): The input URL.

    Returns:
        str: The extracted domain.
    """
    if not url:
        return "unknown"
    
    domain = urlparse(url).netloc # Extract the domain from the parsed URL
    
    return domain.replace("www.", "") if domain else "unknown"  # Remove 'www.' prefix if present


_stopwords = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "is", "are", "was", "were", "by", "from", "as", "it",
    "this", "that", "has", "have", "will", "be", "its", "after", "over",
}

# -----------------------------------------------------------------------
# STEP 3: Extract keywords from cleaned text
# -----------------------------------------------------------------------
def extract_keywords(text: str, top_n: int = 5) -> list[str]:
    """
    Extracts the top N keywords from the input text.

    Args:
        text (str): The input text from which to extract keywords.
        top_n (int): The number of top keywords to return.

    Returns:
        list[str]: A list of extracted keywords.
    """
    if not text:
        return []
    
    # Normalize text to lowercase and split into words
    words = re.findall(r"[a-zA-Z]+", text.lower())
    meaningful_words = [w for w in words if w not in _stopwords and len(w) > 3]
    
    # Count word frequencies
    word_counts = {}

    for word in meaningful_words:
        word_counts[word] = word_counts.get(word, 0) + 1

    # Sort words by frequency and return the top N keywords
    sorted_keywords = sorted(word_counts.items(), key=lambda item: item[1], reverse=True)

    return [word for word, count in sorted_keywords[:top_n]]

# -----------------------------------------------------------------------
# STEP 4: Extract location from cleaned text
# -----------------------------------------------------------------------
def extract_location(text: str) -> str | None:
    """
    Extracts a location from the input text using a simple regex pattern.

    Args:
        text (str): The input text from which to extract a location.

    Returns:
        str | None: The extracted location if found, otherwise None.
    """
    
    return None

# -----------------------------------------------------------------------
# STEP 5: Build one structured news object
# -----------------------------------------------------------------------
def build_structured_article(raw_article: dict) -> dict:
    """
    Builds a structured article object from the raw article data.

    Args:
        raw_article (dict): The raw article data.
        
    Returns:
        dict: A structured article object containing cleaned text, domain, keywords, and location.
    """
    title = clean_text(raw_article.get("title", ""))
    content = clean_text(raw_article.get("content", ""))
    url = raw_article.get("url", "")
 
    return {
        "title": title,
        "content": content,
        "domain": extract_domain(url),
        "published_date": raw_article.get("published_date"),
        "url": url,
        "location": extract_location(content),
        "keywords": extract_keywords(content),
    }


def process_raw_articles(raw_articles: list[dict]) -> list[dict]:
    """
    Processes a list of raw articles and returns a list of structured articles.

    Args:
        raw_articles (list[dict]): A list of raw article data.

    Returns:
        list[dict]: A list of structured article objects.
    """
    return [build_structured_article(article) for article in raw_articles]


if __name__ == "__main__":
    sample_raw_articles = [
        {
            "title": "  Heavy Rainfall Shuts Down Highway  ",
            "url": "https://www.example.com/news/1",
            "content": "<p>Heavy rain has caused a road closure near the plant.</p>",
            "published_date": "2026-07-01",
        }
    ]
 
    processed = process_raw_articles(sample_raw_articles)
    for article in processed:
        print(article)
